"""Expanding, isotropic ideal-free-bath scattering benchmark.

For constant g*=g*s=60, y=p/T is a comoving momentum coordinate and
eta=ln(T0/T)=ln(a/a0). Collisionless comoving cell populations are constant.
The reversible event form inherits the fixed-bath exact-boost quadrature.
No number-changing term is silently included in this scattering module.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.integrate import quad
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply
from scipy.special import kve, roots_genlaguerre, roots_legendre

MASS = np.array([10., 11.5])
FERMIONS = [('e', .00051099895, 1), ('mu', .1056583755, 1),
            ('tau', 1.77686, 1), ('u', .002, 3), ('d', .005, 3),
            ('s', .100, 3), ('c', 1.300, 3), ('b', 4.200, 3)]
MH = 125.
K = .001
T0 = .5
TF = 1/3


@dataclass(frozen=True)
class Resolution:
    q: int = 24
    boost: int = 16
    scattering: int = 12
    direction: int = 12
    azimuth: int = 16


def hubble(T):
    return math.sqrt(8 * math.pi**3 * 60 / 90) * T*T / 1.2209e19


def neq(T):
    return sum(m*m*T*kve(2, m/T)*math.exp(-m/T)/(2*math.pi**2) for m in MASS)


def cell_data(T, edges, order=16):
    """Equilibrium mass and moments on fixed y=p/T cells, including infinity.

    Columns: mass, mean-energy numerator, kinetic-energy numerator,
    pressure-per-particle numerator p^2/(3E). All divided by total n_eq.
    """
    nb = len(edges)-1
    result = np.zeros((2, nb, 4))
    norm = sum(m*m*T*kve(2,m/T)*math.exp(-(m-MASS[0])/T)/(2*math.pi**2) for m in MASS)
    nodes, weights = roots_legendre(order)
    lo, hi = edges[:-2], edges[1:-1]
    yy = (lo[:,None]+hi[:,None])/2 + (hi-lo)[:,None]*nodes[None,:]/2
    ww = (hi-lo)[:,None]*weights[None,:]/2
    for i,m in enumerate(MASS):
        p = T*yy
        ee = np.sqrt(m*m+p*p)
        kinetic = p*p/(ee+m)
        weight = T**3*yy*yy*np.exp(-(kinetic+m-MASS[0])/T)/(2*math.pi**2*norm)
        fields = [np.ones_like(yy), ee, kinetic, p*p/(3*ee)]
        for k,field in enumerate(fields):
            result[i,:-1,k] = np.sum(ww*weight*field,axis=1)
        ylo = edges[-2]
        xlo = (T*ylo)**2/(math.sqrt(m*m+(T*ylo)**2)+m)/T
        def integrand(x,k):
            E=m+T*x
            p=math.sqrt(T*x*(2*m+T*x))
            w=p*E*T*math.exp(-x-(m-MASS[0])/T)/(2*math.pi**2*norm)
            return w*[1.,E,T*x,p*p/(3*E)][k]
        for k in range(4):
            result[i,-1,k] = quad(integrand,xlo,np.inf,args=(k,),epsabs=1e-25,epsrel=2e-11)[0]
    return result


def collision_graph(T,edges,res):
    """Positive equilibrium event histogram normalized by total n_eq(T)."""
    nb=len(edges)-1; size=2*nb
    event=np.zeros((size,size))
    cs,cw=roots_legendre(res.scattering)
    zs,zw=roots_legendre(res.direction)
    cp=np.cos(2*math.pi*np.arange(res.azimuth)/res.azimuth)
    v,vw=roots_genlaguerre(res.boost,.5)
    zfinal=(cs[:,None,None]*zs[None,:,None]
            +np.sqrt(1-cs[:,None,None]**2)*np.sqrt(1-zs[None,:,None]**2)*cp[None,None,:])
    norm=(kve(2,MASS[0]/T)+(MASS[1]/MASS[0])**2
          *math.exp(-(MASS[1]-MASS[0])/T)*kve(2,MASS[1]/T))
    for name,mf,Nc in FERMIONS:
        for i,j in [(0,0),(1,0),(1,1)]:
            mi,mj=MASS[i],MASS[j]
            q0=max(mi,mj)+mf
            alpha=1. if i==j else .5
            xs,weights=roots_genlaguerre(res.q,alpha)
            pref=Nc*4*T/(8*math.pi**2*MASS[0]**2*norm)*math.exp(-(q0-MASS[0])/T)
            for x,qw in zip(xs,weights):
                q=q0+T*x;s=q*q;z=q/T
                ai=(s+mi*mi-mf*mf)/(2*q);aj=(s+mj*mj-mf*mf)/(2*q)
                pi=math.sqrt(max(0,(s-(mi+mf)**2)*(s-(mi-mf)**2)))/(2*q)
                pj=math.sqrt(max(0,(s-(mj+mf)**2)*(s-(mj-mf)**2)))/(2*q)
                g=1+v/z;u=np.sqrt(v*(2*z+v))/z
                Ei=g[:,None]*ai+u[:,None]*pi*zs[None,:]
                Ej=g[:,None,None,None]*aj+u[:,None,None,None]*pj*zfinal[None,:,:,:]
                yi=np.sqrt(np.maximum(0,(Ei-mi)*(Ei+mi)))/T
                yj=np.sqrt(np.maximum(0,(Ej-mj)*(Ej+mj)))/T
                ia=i*nb+np.searchsorted(edges[1:-1],yi)
                jb=j*nb+np.searchsorted(edges[1:-1],yj)
                pairs=ia[:,None,:,None]*size+jb
                tt=mi*mi+mj*mj-2*ai*aj+2*pi*pj*cs
                if np.max(tt)>1e-9:raise ValueError('unexpected timelike scattering transfer')
                amp=K*K*mf*mf*(4*mf*mf-tt)/(MH*MH-tt)**2
                angular=cw*2*pi*pj*amp/(16*math.pi)*(.5 if i==j else 1.)
                wq=pref*qw*x**(-alpha)
                wb=vw*np.sqrt(2*z+v)/z
                weight=wq*wb[:,None,None,None]*angular[None,:,None,None]*zw[None,None,:,None]/(2*res.azimuth)
                values=np.broadcast_to(weight,pairs.shape)
                event+=np.bincount(pairs.ravel(),weights=values.ravel(),minlength=size*size).reshape(size,size)
    W=event+event.T
    np.fill_diagonal(W,0.)
    return W


def make_bank(path, finite_bins=192, ymax=48., intervals=8,res=Resolution()):
    start=time.perf_counter()
    edges=np.r_[np.linspace(0,ymax,finite_bins+1),np.inf]
    eta=np.unique(np.r_[np.linspace(0,math.log(T0/TF),intervals+1), math.log(T0/.4)])
    conductances=[]
    for k,e in enumerate(eta):
        T=T0*math.exp(-e)
        begin=time.perf_counter()
        W=collision_graph(T,edges,res)/hubble(T)
        conductances.append(W)
        print(f'node {k+1}/{len(eta)} T={T:.8g} elapsed={time.perf_counter()-begin:.2f}s',flush=True)
    metadata=dict(T0_GeV=T0,Tf_GeV=TF,resolution=asdict(res),finite_bins_per_species=finite_bins,
                  ymax=ymax,eta_intervals=intervals,elapsed_seconds=time.perf_counter()-start,
                  conductance_units='D_per_Neq / H(T), offdiagonal magnitude; diagonal stored as zero',
                  scattering_only=True,gstar=60,gstar_s=60,coordinate='y=p/T, eta=ln(T0/T)')
    np.savez_compressed(path,edges=edges,eta=eta,conductances=np.array(conductances),metadata=json.dumps(metadata))
    Path(path).with_suffix('.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return metadata


def refine_temperature_bank(source,path,intervals=16):
    """Reuse existing graphs and add only missing nodes of a nested T grid."""
    with np.load(source) as z:
        metadata=json.loads(str(z['metadata']))
        oldeta=z['eta'].copy(); oldW=z['conductances'].copy();edges=z['edges'].copy()
    eta=np.unique(np.r_[np.linspace(0,math.log(T0/TF),intervals+1),math.log(T0/.4)])
    resolution=Resolution(**metadata['resolution'])
    conductances=[];start=time.perf_counter();added=0
    for e in eta:
        nearest=int(np.argmin(abs(oldeta-e)))
        if abs(oldeta[nearest]-e)<1e-12:
            conductances.append(oldW[nearest]);continue
        T=T0*math.exp(-e);begin=time.perf_counter()
        conductances.append(collision_graph(T,edges,resolution)/hubble(T))
        added+=1
        print(f'added node {added} T={T:.8g} elapsed={time.perf_counter()-begin:.2f}s',flush=True)
    extra=time.perf_counter()-start
    metadata.update(eta_intervals=intervals,parent_bank=Path(source).name,
                    additional_elapsed_seconds=extra,additional_temperature_nodes=added,
                    elapsed_seconds=metadata['elapsed_seconds']+extra)
    np.savez_compressed(path,edges=edges,eta=eta,conductances=np.array(conductances),metadata=json.dumps(metadata))
    Path(path).with_suffix('.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return metadata


class ScatteringBank:
    """Positive conductance interpolation with exact instantaneous cell metric."""
    def __init__(self,path,aggregation=1,temperature_stride=1,tail_ymax=None):
        with np.load(path) as z:
            self.metadata=json.loads(str(z['metadata']))
            self.edges=z['edges'].copy();self.eta=z['eta'].copy()
            self.W=z['conductances'].copy()
        if temperature_stride != 1:
            # Select nested regular nodes, while retaining the T=.4 snapshot node.
            regular=np.linspace(0,math.log(T0/TF),self.metadata['eta_intervals']+1)
            requested=np.r_[regular[::temperature_stride],regular[-1],math.log(T0/.4)]
            keep=[k for k,e in enumerate(self.eta) if np.min(np.abs(requested-e))<1e-12]
            self.eta=self.eta[keep];self.W=self.W[keep]
        oldnb=len(self.edges)-1
        if tail_ymax is None: tail_ymax=self.edges[-2]
        cut=int(np.flatnonzero(np.isclose(self.edges,tail_ymax))[0])
        if cut%aggregation:raise ValueError('Tail start index must divide aggregation')
        finite=cut//aggregation
        self.edges=np.r_[self.edges[:cut+1:aggregation],np.inf]
        nb=finite+1
        if aggregation!=1 or cut!=oldnb-1:
            P=np.zeros((2*oldnb,2*nb))
            for i in range(2):
                for a in range(oldnb):
                    P[i*oldnb+a,i*nb+min(a//aggregation,finite)]=1
            self.W=np.array([P.T@W@P for W in self.W])
            for W in self.W:np.fill_diagonal(W,0.)
        self.nbin=nb

    def conductance(self,eta):
        if eta < self.eta[0]-1e-12 or eta > self.eta[-1]+1e-12:
            raise ValueError('Temperature outside bank range')
        k=min(max(np.searchsorted(self.eta,eta)-1,0),len(self.eta)-2)
        weight=(eta-self.eta[k])/(self.eta[k+1]-self.eta[k])
        return (1-weight)*self.W[k]+weight*self.W[k+1]

    def generator(self,eta):
        T=T0*math.exp(-eta)
        data=cell_data(T,self.edges)
        pi=data[:,:,0].ravel()
        W=self.conductance(eta)
        Q=W.copy();np.fill_diagonal(Q,-W.sum(axis=1))
        Q/=pi[None,:]
        return Q,data


def collisionless_exact(T):
    """Direct continuum free streaming of the initial zero-mu MB distribution."""
    n0=neq(T0)
    # Integrate initial x=(E0-mi)/T0; all exponential tail mass is retained.
    result=[]
    for m in MASS:
        def integrand(x,k):
            E0=m+T0*x;p0=math.sqrt(T0*x*(2*m+T0*x))
            p=p0*T/T0;E=math.sqrt(m*m+p*p)
            w=p0*E0*T0*math.exp(-m/T0-x)/(2*math.pi**2*n0)
            return w*[1.,E,p*p/(E+m),p*p/(3*E)][k]
        result.append([quad(integrand,0,np.inf,args=(k,),epsabs=1e-12,epsrel=2e-11)[0] for k in range(4)])
    result=np.array(result)
    return dict(heavy_fraction=float(result[1,0]),mean_total_energy_GeV=float(result[:,1].sum()),
                mean_kinetic_energy_GeV=float(result[:,2].sum()),Tkin_over_T=float(result[:,3].sum()/T))


def observables(masses,T,edges,save_cells=False):
    data=cell_data(T,edges);pi=data[:,:,0].ravel()
    N=float(masses.sum());conditional=data.reshape(-1,4)[:,1:]/pi[:,None]
    species=masses.reshape(2,-1).sum(axis=1)
    r=species/N
    pi_species=pi.reshape(2,-1).sum(axis=1)
    same_species_mb=(data[:,:,0]/pi_species[:,None]*r[:,None]).ravel()
    moments=masses@conditional/N
    row=dict(T_GeV=T,eta=math.log(T0/T),scale_factor=T0/T,comoving_number_relative_to_initial=N,
             physical_number_GeV3=N*neq(T0)*(T/T0)**3,
             heavy_fraction=float(r[1]),mean_total_energy_GeV=float(moments[0]),
             mean_kinetic_energy_GeV=float(moments[1]),Tkin_over_T=float(moments[2]/T),
             total_variation_to_common_fugacity_MB=float(.5*np.abs(masses/N-pi).sum()),
             total_variation_to_same_species_MB=float(.5*np.abs(masses/N-same_species_mb).sum()),
             minimum_cell_mass=float(masses.min()),instantaneous_eq_heavy_fraction=float(pi_species[1]),
             instantaneous_eq_Tkin_over_T=float(data[:,:,3].sum()/T),
             instantaneous_eq_total_number_relative_to_initial=float(neq(T)/neq(T0)*(T0/T)**3))
    if save_cells:row['comoving_cell_masses']=masses.reshape(2,-1).tolist()
    return row


def evolve(bank,steps=96,save_every=4):
    end=math.log(T0/TF)
    # Include T=.4 exactly; this is an observation node, not a time-step interpolation.
    grid=np.unique(np.r_[np.linspace(0,end,steps+1),math.log(T0/.4)])
    initial=cell_data(T0,bank.edges)[:,:,0].ravel()
    mass=initial.copy()
    rows=[];free=[]
    for k,eta in enumerate(grid):
        T=T0*math.exp(-eta)
        save=(k==0 or k==len(grid)-1 or abs(T-.4)<1e-12)
        if save or k%save_every==0:
            row=observables(mass,T,bank.edges,save)
            rows.append(row)
            free.append(dict(T_GeV=T,exact=collisionless_exact(T),cell_closure=observables(initial,T,bank.edges,False)))
        if k+1==len(grid):break
        dt=grid[k+1]-eta
        Q,_=bank.generator(eta+dt/2)
        # No clipping or renormalization: conservation and positivity are checked.
        mass=expm_multiply(csr_matrix(Q*dt),mass,traceA=float(np.trace(Q)*dt))
    assert max(abs(r['comoving_number_relative_to_initial']-1) for r in rows)<2e-12
    assert min(r['minimum_cell_mass'] for r in rows)>-1e-16
    return dict(T0_GeV=T0,Tf_GeV=TF,steps=steps,actual_steps=len(grid)-1,
                finite_bins_per_species=bank.nbin-1,tail_start_y=float(bank.edges[-2]),
                temperature_nodes_GeV=(T0*np.exp(-bank.eta)).tolist(),
                initial_condition='zero-chemical-potential MB at T0=.5 GeV',
                coordinate='y=p/T; eta=ln(T0/T); g*=g*s=60',
                number_changing_included=False,decay_redistribution_included=False,
                collisions='elastic and paired scalar conversion on fixed ideal MB fermion bath at each T',
                rows=rows,collisionless_controls=free,
                all_number_and_positivity_checks_passed=True,
                observable_closure='Within each moving physical-momentum cell use instantaneous equilibrium conditional shape; direct continuum collisionless control quantifies observable reconstruction sensitivity.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    build=sub.add_parser('bank')
    build.add_argument('--output',required=True)
    build.add_argument('--bins',type=int,default=192)
    build.add_argument('--ymax',type=float,default=48.)
    build.add_argument('--intervals',type=int,default=8)
    for name,value in asdict(Resolution()).items():build.add_argument('--'+name,type=int,default=value)
    run=sub.add_parser('evolve')
    run.add_argument('--bank',required=True)
    run.add_argument('--output',required=True)
    run.add_argument('--aggregation',type=int,default=1)
    run.add_argument('--temperature-stride',type=int,default=1)
    run.add_argument('--steps',type=int,default=96)
    refine=sub.add_parser('refine-temperature')
    refine.add_argument('--bank',required=True)
    refine.add_argument('--output',required=True)
    refine.add_argument('--intervals',type=int,default=16)
    args=parser.parse_args()
    if args.command=='bank':
        metadata=make_bank(args.output,args.bins,args.ymax,args.intervals,
                           Resolution(args.q,args.boost,args.scattering,args.direction,args.azimuth))
        print(json.dumps(metadata,indent=2))
    elif args.command=='refine-temperature':
        print(json.dumps(refine_temperature_bank(args.bank,args.output,args.intervals),indent=2))
    else:
        bank=ScatteringBank(args.bank,args.aggregation,args.temperature_stride)
        result=evolve(bank,args.steps)
        Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result['rows'][-1].items() if k!='comoving_cell_masses'},indent=2))
