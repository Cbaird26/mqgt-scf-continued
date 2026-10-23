"""Independent continuum momentum-vertex checks for a single Dirac mass.

Uses explicit 4x4 gamma matrices and exact Gaussian polynomial quadrature.
Conformal g=e^(2 sigma) delta: Dhat=e^(-sigma/2) Dflat e^(-sigma/2)+gamma5 b.
Volume-preserving TT g=diag(1,e^(2 eta),e^(-2 eta),1).
Fields have cosine amplitudes. Output is Hessian kernel normalization, before
removing constant-potential metric contacts. Does not use curvature form factors.
"""
from itertools import product
import numpy as np
from numpy.polynomial.hermite import hermgauss
from numpy.polynomial.legendre import leggauss

s1=np.array([[0,1],[1,0]],complex);s2=np.array([[0,-1j],[1j,0]]);s3=np.diag([1.,-1.]);I2=np.eye(2)
G=np.array([np.kron(s1,I2),np.kron(s2,I2),np.kron(s3,s1),np.kron(s3,s2)])
G5=G[0]@G[1]@G[2]@G[3];I4=np.eye(4)


def raw(a,b,z,quadrature=64):
    p=np.sqrt(complex(z));q=np.array([p,0,0,0])
    xx,ww=hermgauss(3);inds=np.array(list(product(range(3),repeat=4)))
    ell=xx[inds]/np.sqrt(a);weights=np.prod(ww[inds],axis=1)/np.pi**2
    t,wt=leggauss(quadrature);t=(t+1)/2;wt=wt/2
    # One-point P'' vertices: their spin trace is sufficient.
    ksq=np.sum(ell*ell,axis=1)
    Q=np.array([4*(2*ksq+z/4),np.full(len(ell),4.),8*(ell[:,1]**2+ell[:,2]**2)])
    ans=np.diag(-a*(Q@weights)).astype(complex)
    for tt,w in zip(t,wt):
        k=ell-(1-tt)*q;kp=k+q
        D=-np.einsum('nm,mij->nij',k,G);Dp=-np.einsum('nm,mij->nij',kp,G)
        D0=D+b*G5;D0p=Dp+b*G5
        W=k[:,1,None,None]*G[1]-k[:,2,None,None]*G[2]
        dD=np.array([-(D+Dp)/4,np.broadcast_to(G5/2,D.shape),W/2])
        V=D0[None]@dD+dD@D0p[None]
        Vr=D0p[None]@dD+dD@D0[None]
        traces=np.einsum('Xnij,Ynji->nXY',V,Vr)
        ans+=2*a*a*w*np.exp(-a*tt*(1-tt)*z)*np.einsum('n,nXY->XY',weights,traces)
    return ans*np.exp(-a*b*b)/(16*np.pi**2*a*a)


def prediction(a,b,z):
    from two_point import basic
    F,J,_,_=basic(np.array([a*z]));F=F[0];J=J[0]
    he=np.exp(-a*b*b);f=he/(48*np.pi**2*a)
    aa=he*(F-4*J)/(16*np.pi**2*a)
    bb=he*(-F/2+5*J)/(16*np.pi**2*a)
    c=he*2*b*J/(16*np.pi**2)
    # scalar Hessian before the subtraction: second derivative of local potential.
    H=he*(4*b*b-2/a)/(8*np.pi**2)
    delta=he*(z*F+4*b*b*(F-1))/(8*np.pi**2)
    return np.array([[-6*z*bb,6*z*c,0],[6*z*c,H+delta,0],[0,0,2*z*aa]])


def check_one(a,b,z):
    rawz=raw(a,b,z);base=raw(a,b,0.)
    # Cancel W and W_A metric contacts, as at a flat stationary fixture.
    rawz[0,0]-=base[0,0];rawz[0,1]-=base[0,1];rawz[1,0]-=base[1,0]
    return rawz,prediction(a,b,z)
