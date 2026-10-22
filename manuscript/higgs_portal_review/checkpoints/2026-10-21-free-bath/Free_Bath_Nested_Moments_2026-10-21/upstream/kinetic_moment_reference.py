"""Independent numerical representations of Note 52 moment identities.

Explicit Lorentz boosts and orientation quadrature, rather than the main
code's Bessel-reduced energy/spatial Gram formulas. The amplitude and model
are shared external inputs; this is not a second Feynman-diagram calculation.
"""
import math
import numpy as np
from scipy.integrate import quad
from scipy.special import roots_legendre


def scalar_stats(T,m):
    # Dimensionless kinetic energy u=(E-m)/T; density of states p*E*dE.
    def weight(u):
        E=m+T*u
        return math.sqrt(T*u*(2*m+T*u))*E*math.exp(-u)
    z=quad(weight,0,100,epsabs=1e-12,epsrel=1e-12)[0]
    mu=quad(lambda u:u*weight(u),0,100,epsabs=1e-12,epsrel=1e-12)[0]/z
    var=quad(lambda u:(u-mu)**2*weight(u),0,100,epsabs=1e-12,epsrel=1e-12)[0]/z
    pz=quad(lambda u:((m+T*u)**2-m*m)/3/T**2*weight(u),0,100,epsabs=1e-12,epsrel=1e-12)[0]/z
    return m+T*mu,var,pz


def boost_stats(z):
    def weight(eta):
        return math.sinh(eta)**2*math.exp(-z*(math.cosh(eta)-1))
    norm=quad(weight,0,4,epsabs=1e-14,epsrel=1e-13)[0]
    mean=quad(lambda e:math.cosh(e)*weight(e),0,4,epsabs=1e-14,epsrel=1e-13)[0]/norm
    second=quad(lambda e:math.cosh(e)**2*weight(e),0,4,epsabs=1e-14,epsrel=1e-13)[0]/norm
    u2=quad(lambda e:math.sinh(e)**2*weight(e),0,4,epsabs=1e-14,epsrel=1e-13)[0]/norm
    return mean,second,u2


def direct_jump_gram(q,T,ml,pair,model,n_eta=80,n_angle=20):
    """Direct CM angle + boost rapidity/direction quadrature at fixed q.
    Averaging a final common spatial rotation gives vector dot products/3.
    This computes all 6x6 entries without the production boost formulas.
    """
    if pair=='21': i,j,coupling=1,0,model.k12
    elif pair=='11': i,j,coupling=0,0,model.k11
    elif pair=='22': i,j,coupling=1,1,model.k22
    else: raise ValueError('unsupported pair')
    ms=[model.m1,model.m2];mi,mj=ms[i],ms[j];s=q*q
    ai=(s+mi*mi-ml*ml)/(2*q);aj=(s+mj*mj-ml*ml)/(2*q)
    pi=math.sqrt(max(0,(s-(mi+ml)**2)*(s-(mi-ml)**2)))/(2*q)
    pj=math.sqrt(max(0,(s-(mj+ml)**2)*(s-(mj-ml)**2)))/(2*q)
    ebar=[scalar_stats(T,m)[0] for m in ms]
    cn,cw=roots_legendre(n_angle)
    en,ew=roots_legendre(n_eta);eta=1.5*(en+1);ew=1.5*ew
    zn,zw=roots_legendre(8)
    phi=2*math.pi*np.arange(8)/8
    bhat=np.array([np.sqrt(1-zn[:,None]**2)*np.cos(phi)[None,:],
                   np.sqrt(1-zn[:,None]**2)*np.sin(phi)[None,:],
                   np.broadcast_to(zn[:,None],(8,8))]).transpose(1,2,0)
    gamma_=np.cosh(eta);u=np.sinh(eta)
    bw=ew*u*u*np.exp(-q/T*(gamma_-1));bw/=sum(bw)
    weights=bw[:,None,None]*zw[None,:,None]/2/8
    grams=np.zeros((6,6))
    vi=np.array([0,0,pi])
    for c,w in zip(cn,cw):
        vj=np.array([pj*math.sqrt(1-c*c),0,pj*c])
        bi=np.einsum('...i,i->...',bhat,vi)
        bj=np.einsum('...i,i->...',bhat,vj)
        Ei=gamma_[:,None,None]*ai+u[:,None,None]*bi[None,:,:]
        Ej=gamma_[:,None,None]*aj+u[:,None,None]*bj[None,:,:]
        pli=vi+( (gamma_[:,None,None]-1)*bi[None,:,:]+u[:,None,None]*ai)[...,None]*bhat[None,...]
        plj=vj+( (gamma_[:,None,None]-1)*bj[None,:,:]+u[:,None,None]*aj)[...,None]*bhat[None,...]
        v=np.zeros(Ei.shape+(4,));v[...,i]+=1;v[...,j]-=1
        v[...,2+i]+=(Ei-ebar[i])/T;v[...,2+j]-=(Ej-ebar[j])/T
        block=np.zeros((6,6))
        block[:4,:4]=np.einsum('abc,abci,abcj->ij',np.broadcast_to(weights,Ei.shape),v,v)
        if i==j:
            block[4+i,4+i]=np.sum(weights*np.sum((pli-plj)**2,axis=-1))/(3*T*T)
        else:
            block[4+i,4+i]=np.sum(weights*np.sum(pli*pli,axis=-1))/(3*T*T)
            block[4+j,4+j]=np.sum(weights*np.sum(plj*plj,axis=-1))/(3*T*T)
            block[4+i,4+j]=block[4+j,4+i]=-np.sum(weights*np.sum(pli*plj,axis=-1))/(3*T*T)
        # t from the scalar four-momenta, independent endpoint formula.
        t=mi*mi+mj*mj-2*ai*aj+2*pi*pj*c
        amp=coupling**2*ml**2*(4*ml*ml-t)/(model.mh**2-t)**2
        grams+=w*(2*pi*pj)*amp/(16*math.pi)*block
    return (0.5 if i==j else 1.)*grams
