"""Reversible cell discretization of the fixed ideal MB free-bath operator.

Two isotropic singlet species; x=(E-m)/T. Positive equilibrium event weights
are routed to cell indicator functions, including a final semi-infinite bin.
This is a fixed-temperature linear scattering problem, not cosmological
evolution or a full-spectrum certificate.
"""
from __future__ import annotations
import argparse
import json
import math
import time
from dataclasses import dataclass,asdict
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import roots_genlaguerre,roots_legendre,kve
from scipy.linalg import eigh

MASS=(10.,11.5)
FERMIONS=[('e',.00051099895,1),('mu',.1056583755,1),('tau',1.77686,1),
          ('u',.002,3),('d',.005,3),('s',.100,3),('c',1.300,3),('b',4.200,3)]
MH=125.; K=.001

@dataclass(frozen=True)
class Resolution:
    q:int=32
    boost:int=24
    scattering:int=16
    direction:int=12
    azimuth:int=16

def hubble(T):
    return math.sqrt(8*math.pi**3*60/90)*T*T/1.2209e19

def cell_data(T,edges):
    """Numerically exact 1-D MB cell masses and conditional energy moments."""
    norm=sum(m*m*T*math.exp(-(m-MASS[0])/T)*kve(2,m/T)/(2*math.pi**2) for m in MASS)
    b=len(edges)-1
    data=np.zeros((2,b,3))
    for i,m in enumerate(MASS):
        def w(x):
            E=m+T*x
            return math.sqrt(T*x*(2*m+T*x))*E*T*math.exp(-x-(m-MASS[0])/T)/(2*math.pi**2)/norm
        for a,(lo,hi) in enumerate(zip(edges[:-1],edges[1:])):
            for power in range(3):
                data[i,a,power]=quad(lambda x:w(x)*x**power,lo,hi,epsabs=1e-15,epsrel=3e-12)[0]
    return data

def collision_graph(T,edges,res):
    """Event histogram, with full boost/scattering orientation quadrature."""
    nbin=len(edges)-1; size=2*nbin
    event=np.zeros((size,size)); per_flavor={}
    cs,cw=roots_legendre(res.scattering)
    zs,zw=roots_legendre(res.direction)
    cp=np.cos(2*math.pi*np.arange(res.azimuth)/res.azimuth)
    v,vw=roots_genlaguerre(res.boost,.5)
    # Orientation cosine of final center-of-mass scalar relative to boost.
    zfinal=cs[:,None,None]*zs[None,:,None]+np.sqrt(1-cs[:,None,None]**2)*np.sqrt(1-zs[None,:,None]**2)*cp[None,None,:]
    norm=kve(2,MASS[0]/T)+(MASS[1]/MASS[0])**2*math.exp(-(MASS[1]-MASS[0])/T)*kve(2,MASS[1]/T)
    for name,mf,Nc in FERMIONS:
        flavor=np.zeros_like(event)
        for i,j in [(0,0),(1,0),(1,1)]:
            mi,mj=MASS[i],MASS[j]
            q0=max(mi,mj)+mf
            alpha=1. if i==j else .5
            xs,weights=roots_genlaguerre(res.q,alpha)
            pref=Nc*4*T/(8*math.pi**2*MASS[0]**2*norm)*math.exp(-(q0-MASS[0])/T)
            for x,qw in zip(xs,weights):
                q=q0+T*x; s=q*q;z=q/T
                ai=(s+mi*mi-mf*mf)/(2*q);aj=(s+mj*mj-mf*mf)/(2*q)
                pi=math.sqrt(max(0,(s-(mi+mf)**2)*(s-(mi-mf)**2)))/(2*q)
                pj=math.sqrt(max(0,(s-(mj+mf)**2)*(s-(mj-mf)**2)))/(2*q)
                g=1+v/z; u=np.sqrt(v*(2*z+v))/z
                xi=(g[:,None]*ai+u[:,None]*pi*zs[None,:]-mi)/T
                xj=(g[:,None,None,None]*aj+u[:,None,None,None]*pj*zfinal[None,:,:,:]-mj)/T
                ia=i*nbin+np.searchsorted(edges[1:-1],xi)
                jb=j*nbin+np.searchsorted(edges[1:-1],xj)
                pairs=ia[:,None,:,None]*size+jb
                t=mi*mi+mj*mj-2*ai*aj+2*pi*pj*cs
                if np.max(t)>1e-9:raise ValueError('unexpected timelike transfer')
                amplitude=K*K*mf*mf*(4*mf*mf-t)/(MH*MH-t)**2
                angular=cw*2*pi*pj*amplitude/(16*math.pi)*(.5 if i==j else 1.)
                # kve(1,z) cancels exactly between q and boost weights.
                wq=pref*qw*x**(-alpha)
                wb=vw*np.sqrt(2*z+v)/z
                w=wq*wb[:,None,None,None]*angular[None,:,None,None]*zw[None,None,:,None]/(2*res.azimuth)
                values=np.broadcast_to(w,pairs.shape)
                flavor+=np.bincount(pairs.ravel(),weights=values.ravel(),minlength=size*size).reshape(size,size)
        event+=flavor
        per_flavor[name]=float(flavor.sum())
    W=event+event.T
    D=np.diag(W.sum(axis=1))-W
    return D,per_flavor

def aggregate_graph(D,data,factor):
    """Aggregate equal-width finite bins; retain last tail bin separately."""
    fine=(D.shape[0]//2)-1
    if fine%factor:raise ValueError('factor must divide finite bins')
    coarse=fine//factor
    P=np.zeros((2*(fine+1),2*(coarse+1)))
    for i in range(2):
        for a in range(fine):P[i*(fine+1)+a,i*(coarse+1)+a//factor]=1
        P[(i+1)*(fine+1)-1,(i+1)*(coarse+1)-1]=1
    collapsed=(P.T@data.reshape(-1,3)).reshape(2,coarse+1,3)
    return P.T@D@P,collapsed

def evolution(D,data,T,times=None):
    """Evolve relative occupation g=f/f_eq; generator is -G^-1 D/H."""
    if times is None:times=np.unique(np.r_[np.linspace(0,5,101),[.25,.5,1,2,5]])
    pi=data[:,:,0].ravel();m1=data[:,:,1].ravel(); H=hubble(T)
    sqrtpi=np.sqrt(pi)
    A=D/np.outer(sqrtpi,sqrtpi)/H
    A=(A+A.T)/2
    ev,U=eigh(A)
    # The constant equilibrium mode is known analytically, not inferred.
    # Small roundoff eigenvalues are retained; exact number is checked below.
    nbin=len(pi)//2
    r=pi.reshape(2,nbin).sum(axis=1)
    xmean=m1/pi
    species=np.repeat([0,1],nbin)
    energy_T=xmean+np.repeat(np.array(MASS)/T,nbin)
    mass_T=np.repeat(np.array(MASS)/T,nbin)
    energy_mean=float(np.dot(pi,energy_T))
    energy_second=float(np.sum(data[:,:,2].ravel()+2*mass_T*m1+mass_T*mass_T*pi))
    continuum_variances={'population':float(r[0]*r[1]),'temperature':energy_second-energy_mean**2}
    population=(species==1).astype(float)-r[1]
    temperature=energy_T-energy_mean
    initial={'population':1+.05*population,'temperature':1+.05*temperature}
    outputs={}
    for label,g0 in initial.items():
        perturbation=g0-1
        c=U.T@(sqrtpi*perturbation)
        rows=[]
        norm0=float(np.sum(pi*perturbation**2))
        for tau in times:
            g=1+(U@(np.exp(-ev*tau)*c))/sqrtpi
            mass=pi*g
            row={'tau_Ht':float(tau),'species_fractions':mass.reshape(2,nbin).sum(axis=1).tolist(),
                'total_number_relative_error':float(mass.sum()-1),
                'minimum_relative_occupation':float(g.min()),
                'autocorrelation_relative_to_initial':float(np.sum(pi*perturbation*(g-1))/norm0),
                'autocorrelation_divided_by_continuum_variance':float(np.sum(pi*perturbation*(g-1))/(.05**2*continuum_variances[label])),
                'chi2_relative_to_initial':float(np.sum(pi*(g-1)**2)/norm0),
                'mean_energy_excess_over_T':float(np.sum(pi*energy_T*(g-1))),
                'kinetic_x_excess':float(np.sum(m1*(g-1)))}
            if any(abs(tau-t)<1e-10 for t in [0,.25,.5,1,2,5]):row['g_by_species']=g.reshape(2,nbin).tolist()
            rows.append(row)
        outputs[label]={'epsilon':.05,'initial_g':g0.reshape(2,nbin).tolist(),
                        'initial_shape_variance':norm0/.05**2,
                        'continuum_initial_shape_variance':continuum_variances[label],
                        'initial_variance_retained_fraction':norm0/(.05**2*continuum_variances[label]),'rows':rows}
    return {'positive_eigenvalues_over_H':ev[1:].tolist(),'smallest_eigenvalue_over_H':float(ev[0]),
        'number_null_relative_residual':float(np.linalg.norm(D@np.ones(len(pi)))/np.linalg.norm(D)),
        'symmetry_relative_residual':float(np.linalg.norm(D-D.T)/np.linalg.norm(D)),
        'metric_total':float(pi.sum()),'equilibrium_species_fractions':r.tolist(),
        'conditional_energy_over_T':energy_T.reshape(2,nbin).tolist(),
        'count_only_rate_over_H':float(population@D@population/(np.sum(pi*population**2)*H)),
        'metric_tail_mass':float(data[:,-1,0].sum()),'initial_conditions':outputs}

def run(T=.4,finite_bins=64,tail_start=16.,res=Resolution()):
    start=time.time();edges=np.r_[np.linspace(0,tail_start,finite_bins+1),np.inf]
    data=cell_data(T,edges);D,flavors=collision_graph(T,edges,res)
    out={'T_GeV':T,'model':'fixed ideal MB lepton plus free-quark bath; tree Higgs scattering; gstar60',
        'resolution':asdict(res),'finite_bins_per_species':finite_bins,'tail_start_x':tail_start,
        'edges_x':[float(x) if np.isfinite(x) else None for x in edges],
        'cell_moments':data.tolist(),'D_per_N_GeV':D.tolist(),'event_measure_by_flavor_GeV':flavors,
        'elapsed_seconds':time.time()-start,'grids':{},'full_gap_certified':False,'expanding_background_evolved':False}
    for factor in [4,2,1]:
        if finite_bins%factor:continue
        Dc,dc=aggregate_graph(D,data,factor)
        out['grids'][str(finite_bins//factor)]=evolution(Dc,dc,T)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--temperature',type=float,default=.4);p.add_argument('--bins',type=int,default=64)
    p.add_argument('--tail-start',type=float,default=16.)
    for key,value in asdict(Resolution()).items():p.add_argument('--'+key,type=int,default=value)
    p.add_argument('--output',default='radial_results.json')
    a=p.parse_args();r=run(a.temperature,a.bins,a.tail_start,Resolution(a.q,a.boost,a.scattering,a.direction,a.azimuth))
    Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['T_GeV','resolution','elapsed_seconds']},indent=2))
    for grid,data in r['grids'].items():
        at1=next(x for x in data['initial_conditions']['temperature']['rows'] if x['tau_Ht']==1.)
        print(grid,data['positive_eigenvalues_over_H'][:3],at1['autocorrelation_relative_to_initial'])
