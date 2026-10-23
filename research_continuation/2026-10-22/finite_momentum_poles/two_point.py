"""Quadratic external-momentum kernels of the pinned warped Dirac family.

z=p_E^2/Lambda^2, continued by z=-s-i0. No quantum contour is asserted.
Metric conventions: h_TT normalized by h_mu_nu h_mu_nu, tau=theta.h/sqrt(3).
Quadratic Fourier density in X=Lambda x, divided by kappa, = (h_TT K2 h_TT + (tau,dq)^T K (tau,dq))/2.
"""
from functools import lru_cache
import numpy as np
from scipy.linalg import eigh
from numpy.polynomial.legendre import leggauss
import mode_sums as m
import vacuum as v
import all_scalars as full


@lru_cache(maxsize=None)
def rule(quadrature):
    t,w=leggauss(quadrature)
    return (t+1)/2,w/2


def basic(x, quadrature=96):
    """F=int exp(-x u), J=(1-F)/x, and derivatives; removable values explicit."""
    x=np.asarray(x);t,w=rule(quadrature);u=t*(1-t)
    F=np.sum(w*np.exp(-x[...,None]*u),axis=-1)
    Fp=-np.sum(w*u*np.exp(-x[...,None]*u),axis=-1)
    J=np.zeros_like(F);Jp=np.zeros_like(F)
    small=abs(x)<.1
    if np.any(small):
        # Integral moments: int u^n = (n!)^2/(2n+1)!.
        from math import factorial
        xs=x[small]; j=np.zeros_like(xs,dtype=F.dtype); jp=j.copy()
        for k in range(18):
            c=(-1)**k*factorial(k+1)/factorial(2*k+3)
            j+=c*xs**k
            if k:jp+=k*c*xs**(k-1)
        J[small]=j;Jp[small]=jp
    if np.any(~small):
        xx=x[~small];fm1=np.sum(w*np.expm1(-xx[...,None]*u),axis=-1)
        J[~small]=-fm1/xx
        Jp[~small]=(fm1-xx*Fp[~small])/xx**2
    return F,J,Fp,Jp


class TwoPoint:
    def __init__(self,x,H,profile='minus',levels=12,quadrature=64,all_fields=False):
        self.x=np.array(x,float);self.H=np.array(H,float)/(4*np.pi**2)
        self.profile=profile;self.levels=levels;self.quadrature=quadrature
        self.n=9 if all_fields else 3
        if self.H.shape!=(self.n,self.n):raise ValueError('Hessian size')
        t,w=leggauss(quadrature);self.t=(t+1)/2;self.wt=w/2
        self.u=self.t*(1-self.t); self.rates=v.NODES.copy();self.weights=v.WEIGHTS[profile].copy()
        nr=len(self.rates);N=self.n
        self.heat=np.zeros(nr);self.mass_tangent=np.zeros((nr,N))
        self.TT=np.zeros((nr,quadrature,N,N));self.AA=self.TT.copy()
        R,hd,hu=self.x
        for kind,mult in [('quark',12),('lepton',4),('single0',12)]:
            bs=m.blocks(kind,levels);es=[]
            for b in bs:
                B=b['D']/R
                if b['S']:B=B+hd*b['S'][0]
                if len(b['S'])>1:B=B+hu*b['S'][1]
                es.append(eigh(B,check_finite=False))
            for i,b in enumerate(bs):
                ev,U=es[i]
                for j in range(i,len(bs)):
                    if not all_fields and j!=i:continue
                    bc=bs[j]
                    if abs(b['k2']-bc['k2'])>2:continue
                    ev2,U2=es[j];T=np.zeros((N,len(ev),len(ev2)),complex)
                    if i==j:T[0]=U.T@(-b['D']/R**2)@U
                    if all_fields and kind!='single0':
                        T[1:]=np.array([U.T@s@U2 for s in full.tangent_matrices(kind,levels,i,j)])
                    elif not all_fields:
                        for k,S in enumerate(b['S']):T[k+1]=U.T@S@U
                    A=(ev[None,:,None]+ev2[None,None,:])*T
                    tt=np.einsum('Aij,Bij->ijAB',T,T.conj()).real
                    aa=np.einsum('Aij,Bij->ijAB',A,A.conj()).real
                    fac=mult*(1 if i==j else 2)
                    energies=self.t[:,None,None]*ev[None,:,None]**2+(1-self.t[:,None,None])*ev2[None,None,:]**2
                    for k,a in enumerate(self.rates):
                        if i==j:
                            he=np.exp(-a*ev**2)
                            self.heat[k]+=mult*he.sum()
                            self.mass_tangent[k]+=mult*np.einsum('i,Aii->A',he,A).real
                        he=np.exp(-a*energies)
                        self.TT[k]+=fac*np.einsum('tij,ijAB->tAB',he,tt,optimize=True)
                        self.AA[k]+=fac*np.einsum('tij,ijAB->tAB',he,aa,optimize=True)
        self.f=float(np.dot(self.weights/self.rates,self.heat)/(48*np.pi**2))
        self.df=-np.einsum('a,aA->A',self.weights,self.mass_tangent)/(48*np.pi**2)
        self.GJ=self.scalar(0.)[1]
        self.GE=self.GJ+1.5*np.outer(self.df,self.df)/self.f

    def gravity(self,z):
        F,J,Fp,Jp=basic(self.rates*z,self.quadrature)
        coeff=self.weights*self.heat/(16*np.pi**2*self.rates)
        a=np.dot(coeff,F-4*J);b=np.dot(coeff,-F/2+5*J)
        ap=np.dot(coeff*self.rates,Fp-4*Jp);bp=np.dot(coeff*self.rates,-Fp/2+5*Jp)
        c=np.einsum('a,a,aA->A',self.weights,J,self.mass_tangent)/(16*np.pi**2)
        cp=np.einsum('a,a,a,aA->A',self.weights,self.rates,Jp,self.mass_tangent)/(16*np.pi**2)
        return a,b,c,ap,bp,cp

    def scalar(self,z):
        au=self.rates[:,None]*self.u[None,:];ex=np.exp(-au*z)
        weight=self.weights[:,None]*self.wt[None,:]/(8*np.pi**2)
        delta=np.einsum('at,atAB->AB',weight*z*ex,self.TT)+np.einsum('at,atAB->AB',weight*np.expm1(-au*z),self.AA)
        prime=np.einsum('at,atAB->AB',weight*(1-au*z)*ex,self.TT)-np.einsum('at,atAB->AB',weight*au*ex,self.AA)
        return self.H+delta,prime

    def operator(self,z):
        a,b,c,ap,bp,cp=self.gravity(z);J,Jp=self.scalar(z)
        K=np.zeros((self.n+1,self.n+1),dtype=np.result_type(z,float))
        Kp=K.copy();K[0,0]=-z*b/2;Kp[0,0]=-(b+z*bp)/2
        K[0,1:]=K[1:,0]=np.sqrt(3)*z*c
        Kp[0,1:]=Kp[1:,0]=np.sqrt(3)*(c+z*cp)
        K[1:,1:]=J;Kp[1:,1:]=Jp
        return K,Kp,z*a/4,(a+z*ap)/4

    def regular(self,z):
        """Entire bordered matrix with trivial metric z factored from first row.
        det K(z)=z det regular(z). It is not a physical kinetic matrix.
        """
        _,b,c,_,_,_=self.gravity(z);J,_=self.scalar(z)
        K=np.zeros((self.n+1,self.n+1),dtype=np.result_type(z,float))
        K[0,0]=-b/2;K[0,1:]=np.sqrt(3)*c
        K[1:,0]=np.sqrt(3)*z*c;K[1:,1:]=J
        return K

    def schur(self,z):
        _,b,c,_,bp,cp=self.gravity(z);J,Jp=self.scalar(z)
        cc=np.outer(c,c);cross=np.outer(cp,c)+np.outer(c,cp)
        return J+6*z*cc/b,Jp+6*cc/b+6*z*cross/b-6*z*cc*bp/b**2

    def determinant(self,z):
        return np.linalg.det(self.regular(z))

    def residue(self,z):
        """Real simple root: q^T G_E(0) q=1 fixes normalization of null vector."""
        K,Kp,_,_=self.operator(float(z)); vals,U=eigh(K)
        vv=U[:,np.argmin(abs(vals))];vv/=np.sqrt(vv[1:]@self.GE@vv[1:])
        slope=float(vv@Kp@vv)
        return {'z':float(z),'s_mass2_over_Lambda2':float(-z),
                'null_vector_tau_R_hd_hu':vv.tolist(),'slope':slope,'residue_sign':int(np.sign(slope)),
                'relative_residue':float(1/slope),'null_residual':float(np.linalg.norm(K@vv)),
                'scalar_residue_matrix':(np.outer(vv[1:],vv[1:])/slope).tolist()}

    def determinant_prime(self,z):
        _,b,c,_,bp,cp=self.gravity(z);J,Jp=self.scalar(z)
        R=self.regular(z);Rp=np.zeros_like(R)
        Rp[0,0]=-bp/2;Rp[0,1:]=np.sqrt(3)*cp
        Rp[1:,0]=np.sqrt(3)*(c+z*cp);Rp[1:,1:]=Jp
        value=0j if np.iscomplexobj(R) else 0.
        for i in range(self.n+1):
            M=R.copy();M[:,i]=Rp[:,i];value+=np.linalg.det(M)
        return value
