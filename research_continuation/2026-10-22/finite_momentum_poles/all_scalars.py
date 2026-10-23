"""All eight real lowest-harmonic scalar directions at a neutral background.

Coordinates: R, Re dN, Re uN, Im dN, Im uN, Re dC, Re uC, Im dC, Im uC.
The up coordinates are those of the conjugate-up Yukawa insertion. This is
an invertible real-coordinate convention and does not change inertia/masses.
"""
from functools import lru_cache
import numpy as np
from scipy.linalg import eigh
import mode_sums as m
import vacuum as v

NAMES=['R','Re_dN','Re_uN','Im_dN','Im_uN','Re_dC','Re_uC','Im_dC','Im_uC']


@lru_cache(maxsize=None)
def tangent_matrices(kind,levels,i,j):
    bs=m.blocks(kind,levels); b,c=bs[i],bs[j]
    T=np.zeros((8,len(b['basis']),len(c['basis'])),complex)
    # field slot, right-flavour index, harmonic m, imaginary flag
    specs=[(0,1,-.5,False),(2,1,-.5,True),(4,1,.5,False),(6,1,.5,True)]
    if kind=='quark': specs += [(1,2,.5,False),(3,2,.5,True),(5,2,-.5,False),(7,2,-.5,True)]
    for ii,(f,*st) in enumerate(b['basis']):
        for jj,(g,*ss) in enumerate(c['basis']):
            for slot,right,mh,imag in specs:
                if f==0 and g==right:
                    T[slot,ii,jj]=st[0]*m.yukawa_element(st,ss,mh)*(1j if imag else 1.)
                elif f==right and g==0:
                    T[slot,ii,jj]=st[0]*m.yukawa_element(ss,st,mh)*(-1j if imag else 1.)
    return T


def full_geometry_hessian(x,alpha,c,profile='minus',levels=12):
    R,hd,hu=x;f=0.;df=np.zeros(9);G=np.zeros((9,9));H=np.zeros((9,9))
    for kind,n in [('quark',12),('lepton',4),('single0',12)]:
        bs=m.blocks(kind,levels);eigens=[]
        for b in bs:
            B=b['D']/R
            if b['S']: B=B+hd*b['S'][0]
            if len(b['S'])>1: B=B+hu*b['S'][1]
            ev,U=eigh(B,check_finite=False)
            _,gp,gpp=v.profile_functions(ev,v.WEIGHTS[profile])
            eigens.append((ev,U,gp,gpp))
            H[0,0]+=n/2*np.dot(gp,np.diag(U.T@(2*b['D']/R**3)@U))
        for i,b in enumerate(bs):
            ev,U,gp,gpp=eigens[i]
            for j in range(i,len(bs)):
                bc=bs[j]
                if abs(b['k2']-bc['k2'])>2:continue
                ev2,U2,gp2,gpp2=eigens[j]
                T=np.zeros((9,len(ev),len(ev2)),complex)
                if i==j:T[0]=U.T@(-b['D']/R**2)@U
                if kind!='single0':
                    T[1:]=np.array([U.T@s@U2 for s in tangent_matrices(kind,levels,i,j)])
                fac=1 if i==j else 2
                A=(ev[None,:,None]+ev2[None,None,:])*T
                delta=ev[:,None]-ev2[None,:]
                near=abs(delta)<1e-7*(1+np.maximum(abs(ev[:,None]),abs(ev2[None,:])))
                div=np.divide(gp[:,None]-gp2[None,:],delta,out=np.zeros_like(delta),where=~near)
                div[near]=((gpp[:,None]+gpp2[None,:])/2)[near]
                H+=fac*n/2*np.einsum('ij,aij,bij->ab',div,T,T.conj()).real
                for a,w in zip(v.NODES,v.WEIGHTS[profile]):
                    if i==j:
                        heat=np.exp(-a*ev**2)
                        f+=n*w*heat.sum()/(48*np.pi**2*a)
                        df+=-n*w*np.einsum('i,aii->a',2*ev*heat,T).real/(48*np.pi**2)
                    # Reuse the analytic divided differences on the concatenated energies.
                    if i==j:
                        I0,Iu,_=m.heat_moments(ev**2,a)
                    else:
                        I0,Iu,_=m.heat_moments(np.r_[ev**2,ev2**2],a)
                        I0=I0[:len(ev),len(ev):];Iu=Iu[:len(ev),len(ev):]
                    G+=fac*n*w*(np.einsum('ij,aij,bij->ab',I0,T,T.conj())
                                -a*np.einsum('ij,aij,bij->ab',Iu,A,A.conj())).real/(8*np.pi**2)
    counts=np.tile([16.,12.],4);h=np.r_[hd,hu,np.zeros(6)]
    H[0,0]+=2*alpha*(counts@h**2)-2*c
    H[0,1:]+=4*alpha*R*counts*h;H[1:,0]+=4*alpha*R*counts*h
    H[1:,1:]+=np.diag(2*alpha*R*R*counts)
    E=G+1.5*np.outer(df,df)/f
    return f,df,(G+G.T)/2,(E+E.T)/2,(H+H.T)/2
