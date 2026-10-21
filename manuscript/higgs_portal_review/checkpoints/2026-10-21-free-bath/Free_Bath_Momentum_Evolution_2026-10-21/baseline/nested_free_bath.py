"""Nested Galerkin diagnostics for a declared ideal MB free-fermion bath.

Continuation of Baird/ZoraASI Note 52 and its 2026-10-20 free-bath report.
Independent explicit-boost quadrature. No QCD medium, abundance or full-gap
claim. All rates are numerical trial-space values, NOT lower gap bounds.
Natural GeV units. Fixed bath: only total scalar number is conserved.
"""
from __future__ import annotations
import argparse
import json
import math
import time
from dataclasses import dataclass, asdict
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh, null_space
from scipy.special import kve, roots_genlaguerre, roots_legendre

MASS = (10., 11.5)
MH = 125.
K = .001
FERMIONS = [('e', .00051099895, 1), ('mu', .1056583755, 1),
            ('tau', 1.77686, 1), ('u', .002, 3), ('d', .005, 3),
            ('s', .100, 3), ('c', 1.300, 3), ('b', 4.200, 3)]


@dataclass(frozen=True)
class Resolution:
    q: int = 40
    boost: int = 12
    scattering: int = 12
    direction: int = 4
    azimuth: int = 8


def hubble(T):
    return math.sqrt(8*math.pi**3*60/90)*T*T/1.2209e19


@lru_cache(None)
def metric_data(T):
    """Direct one-dimensional MB integrals; no Bessel moment identities."""
    scalar = np.zeros((6, 6)); drift = np.zeros((4, 4)); quadri = np.zeros((2, 2))
    norm = sum(m*m*T*math.exp(-(m-MASS[0])/T)*kve(2,m/T)/(2*math.pi**2) for m in MASS)
    for i,m in enumerate(MASS):
        def w(u):
            E=m+T*u
            return math.sqrt(T*u*(2*m+T*u))*E*T*math.exp(-u-(m-MASS[0])/T)/(2*math.pi**2)/norm
        moments=[quad(lambda u,k=k:w(u)*u**k,0,120,epsabs=1e-11,epsrel=2e-12)[0] for k in range(5)]
        pm=[quad(lambda u,k=k:w(u)*(u*u+2*m/T*u)/3*u**k,0,120,epsabs=1e-11,epsrel=2e-12)[0] for k in range(3)]
        for a in range(3):
            for b in range(3): scalar[2*a+i,2*b+i]=moments[a+b]
        for a in range(2):
            for b in range(2): drift[2*a+i,2*b+i]=pm[a+b]
        quadri[i,i]=quad(lambda u:w(u)*4/45*(u*u+2*m/T*u)**2,0,120,epsabs=1e-10,epsrel=2e-12)[0]
    return scalar, drift, quadri


@lru_cache(None)
def nodes(res):
    c,cw=roots_legendre(res.scattering)
    z,zw=roots_legendre(res.direction)
    phi=2*math.pi*np.arange(res.azimuth)/res.azimuth
    b=np.stack(np.broadcast_arrays(np.sqrt(1-z[:,None]**2)*np.cos(phi)[None,:],
                                   np.sqrt(1-z[:,None]**2)*np.sin(phi)[None,:],z[:,None]),axis=-1).reshape(-1,3)
    bw=np.broadcast_to(zw[:,None]/2/res.azimuth,(res.direction,res.azimuth)).ravel()
    v,vw=roots_genlaguerre(res.boost,.5)
    return c,cw,b,bw,v,vw


def jump_forms(q,T,mf,pair,res):
    """Explicit boost average of scalar, vector, tensor polynomial jumps.

    Energy-polynomial degree 2; drift radial degree 1; quadrupole degree 0.
    A final isotropic rotation is integrated by exact scalar invariants.
    """
    i,j=pair;mi,mj=MASS[i],MASS[j];s=q*q
    ai=(s+mi*mi-mf*mf)/(2*q);aj=(s+mj*mj-mf*mf)/(2*q)
    pi=math.sqrt(max(0,(s-(mi+mf)**2)*(s-(mi-mf)**2)))/(2*q)
    pj=math.sqrt(max(0,(s-(mj+mf)**2)*(s-(mj-mf)**2)))/(2*q)
    if pi*pj==0: return np.zeros(56)
    cs,cw,b,bw,v,vw=nodes(res)
    z=q/T;g=1+v/z;u=np.sqrt(v*(2*z+v))/z
    # sinh(eta)^2 exp[-z cosh(eta)] deta; exp(-z) cancels.
    w=(vw*np.sqrt(2*z+v)/(z*kve(1,z)))[:,None]*bw[None,:]
    vi=np.array([0.,0.,pi]);bi=b@vi
    ei=g[:,None]*ai+u[:,None]*bi[None,:]
    pli=vi+((g[:,None]-1)*bi[None,:]+u[:,None]*ai)[...,None]*b[None,:,:]
    xi=(ei-mi)/T
    spi=np.stack([np.ones_like(xi),xi,xi*xi],axis=-1)
    di=np.stack([np.ones_like(xi),xi],axis=-1)
    pii=np.sum(pli*pli,axis=-1)
    S=np.zeros((6,6)); V=np.zeros((4,4)); Q=np.zeros((2,2))
    for c,aw in zip(cs,cw):
        vj=np.array([pj*math.sqrt(1-c*c),0.,pj*c]);bj=b@vj
        ej=g[:,None]*aj+u[:,None]*bj[None,:]
        plj=vj+((g[:,None]-1)*bj[None,:]+u[:,None]*aj)[...,None]*b[None,:,:]
        xj=(ej-mj)/T
        spj=np.stack([np.ones_like(xj),xj,xj*xj],axis=-1)
        dj=np.stack([np.ones_like(xj),xj],axis=-1)
        jump=np.zeros(xi.shape+(6,))
        jump[...,i::2]+=spi;jump[...,j::2]-=spj
        vector=np.zeros(xi.shape+(4,3))
        vector[...,i::2,:]+=di[...,None]*pli[...,None,:]/T
        vector[...,j::2,:]-=dj[...,None]*plj[...,None,:]/T
        pjj=np.sum(plj*plj,axis=-1);pij=np.sum(pli*plj,axis=-1)
        qii=4/45*pii*pii/T**4;qjj=4/45*pjj*pjj/T**4
        qij=2/15*(pij*pij-pii*pjj/3)/T**4
        # Spin-averaged amplitude. Two spins and both charges are in prefactor.
        t=mi*mi+mj*mj-2*ai*aj+2*pi*pj*c
        if t>1e-9: raise ValueError('unexpected timelike free scattering')
        amp=K*K*mf*mf*(4*mf*mf-t)/(MH*MH-t)**2
        f=aw*2*pi*pj*amp/(16*math.pi)*(0.5 if i==j else 1.)
        S+=f*np.einsum('ab,abk,abl->kl',w,jump,jump,optimize=True)
        V+=f*np.einsum('ab,abkc,ablc->kl',w,vector,vector,optimize=True)/3
        if i==j: Q[i,i]+=f*np.sum(w*(qii+qjj-2*qij))
        else:
            Q[i,i]+=f*np.sum(w*qii);Q[j,j]+=f*np.sum(w*qjj)
            Q[i,j]-=f*np.sum(w*qij);Q[j,i]=Q[i,j]
    return np.concatenate([S.ravel(),V.ravel(),Q.ravel()])


def collision_forms(T,mf,pair,res):
    i,j=pair;q0=max(MASS[i],MASS[j])+mf
    alpha=1. if i==j else .5
    w,weights=roots_genlaguerre(res.q,alpha)
    norm=kve(2,MASS[0]/T)+(MASS[1]/MASS[0])**2*math.exp(-(MASS[1]-MASS[0])/T)*kve(2,MASS[1]/T)
    pref=4*T/(8*math.pi**2*MASS[0]**2*norm)*math.exp(-(q0-MASS[0])/T)
    result=np.zeros(56)
    for x,weight in zip(w,weights):
        q=q0+T*x
        result+=weight*x**(-alpha)*kve(1,q/T)*jump_forms(q,T,mf,pair,res)
    return pref*result


def eigenvalues(D,G,number_null=False):
    # Cholesky congruence, then analytic conserved vector projection.
    from scipy.linalg import cholesky,solve_triangular
    L=cholesky(G,lower=True)
    A=solve_triangular(L,D,lower=True)
    A=solve_triangular(L,A.T,lower=True).T
    A=(A+A.T)/2
    if number_null:
        v=np.zeros(G.shape[0]);v[:2]=1
        Q=null_space((L.T@v)[None,:])
        A=Q.T@A@Q
    return np.linalg.eigvalsh(A)


def summarize(T,flat):
    S=flat[:36].reshape(6,6);V=flat[36:52].reshape(4,4);Q=flat[52:].reshape(2,2)
    GS,GV,GQ=metric_data(T);H=hubble(T)
    n=np.array([1.,1.,0,0,0,0])
    return dict(counts_over_H=eigenvalues(S[:2,:2],GS[:2,:2],True)[0]/H,
        scalar_degree1_over_H=(eigenvalues(S[:4,:4],GS[:4,:4],True)/H).tolist(),
        scalar_degree2_over_H=(eigenvalues(S,GS,True)/H).tolist(),
        drift_degree0_over_H=(eigenvalues(V[:2,:2],GV[:2,:2])/H).tolist(),
        drift_degree1_over_H=(eigenvalues(V,GV)/H).tolist(),
        quadrupole_degree0_over_H=(eigenvalues(Q,GQ)/H).tolist(),
        number_null_relative_residual=float(np.linalg.norm(S@n)/max(np.linalg.norm(S),1e-300)),
        symmetric_relative_residual=float(np.linalg.norm(S-S.T)/np.linalg.norm(S)),
        gram_scalar_per_N_GeV=S.tolist(),gram_drift_per_N_GeV=V.tolist(),
        gram_quadrupole_per_N_GeV=Q.tolist())


def run(T,res):
    if not 1/3<=T<=.5: raise ValueError('declared T interval is [1/3,.5] GeV')
    start=time.time();total=np.zeros(56);lep=np.zeros(56);contributions={}
    for name,mf,Nc in FERMIONS:
        f=sum((collision_forms(T,mf,pair,res) for pair in [(0,0),(1,0),(1,1)]),start=np.zeros(56))*Nc
        contributions[name]=summarize(T,f);total+=f
        if Nc==1:lep+=f
    return dict(T_GeV=T,resolution=asdict(res),elapsed_s=time.time()-start,
                model='ideal MB bath, exact vacuum tree recoil, fixed gstar=60',
                leptons=summarize(T,lep),leptons_plus_free_quarks=summarize(T,total),
                contributions=contributions,full_spectral_gap_certified=False,
                QCD_medium_calculated=False,cosmological_abundance_calculated=False)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--temperature',type=float,default=.4)
    p.add_argument('--q',type=int,default=40);p.add_argument('--boost',type=int,default=12)
    p.add_argument('--scattering',type=int,default=12);p.add_argument('--direction',type=int,default=4)
    p.add_argument('--azimuth',type=int,default=8);p.add_argument('--output',default='nested_results.json')
    a=p.parse_args();r=run(a.temperature,Resolution(a.q,a.boost,a.scattering,a.direction,a.azimuth))
    Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['T_GeV','resolution','elapsed_s']},indent=2))
    for model in ['leptons','leptons_plus_free_quarks']:
        print(model,json.dumps({k:v for k,v in r[model].items() if 'gram_' not in k},indent=2))
