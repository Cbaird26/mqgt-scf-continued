"""Two-external-derivative radion/scalar dynamics of the declared warped family.

The inherited internal spectral matrices are unchanged. This module extends
their derivatives to R, derives the nonminimal gravitational coefficient,
and performs the Einstein-frame transformation. No finite-momentum metric
propagator or omitted-bosonic-mode stability is asserted.
"""
import numpy as np
from scipy.linalg import eigh
import vacuum as v
import mode_sums as m

SECTORS = [('quark',12),('lepton',4),('single0',12)]


def spectral_geometry(x, profile='minus', levels=12):
    """Return f=F/(kappa Lambda^2), df, Jordan G, Einstein G at f0=f(x).

    Lorentzian L_J = kappa Lambda^2/2 [f R4 - G_AB dq^A dq^B] - V.
    q=(R,h_d,h_u); Einstein coefficient evaluated with equal vacuum units.
    """
    R,hd,hu=np.asarray(x,float)
    f=0.;df=np.zeros(3);G=np.zeros((3,3))
    for kind,n in SECTORS:
        for b in m.blocks(kind,levels):
            D=b['D'];zero=np.zeros_like(D)
            Sd=b['S'][0] if b['S'] else zero
            Su=b['S'][1] if len(b['S'])>1 else zero
            B=D/R+hd*Sd+hu*Su
            ev,U=eigh(B,check_finite=False)
            deriv=np.array([U.T@z@U for z in (-D/R**2,Sd,Su)])
            anti=(ev[None,:,None]+ev[None,None,:])*deriv
            for a,w in zip(v.NODES,v.WEIGHTS[profile]):
                heat=np.exp(-a*ev*ev)
                f+=n*w*np.sum(heat)/(48*np.pi**2*a)
                df+=-n*w*np.einsum('i,aii->a',2*ev*heat,deriv)/(48*np.pi**2)
                I0,Iu,_=m.heat_moments(ev*ev,a)
                G+=n*w*(np.einsum('ij,aij,bji->ab',I0,deriv,deriv)
                         -a*np.einsum('ij,aij,bji->ab',Iu,anti,anti))/(8*np.pi**2)
    G=(G+G.T)/2
    conformal=1.5*np.outer(df,df)/f
    return f,df,G,G+conformal


def unbroken_heat_control(R,profile='minus',levels=80):
    """Independent diagonal n=0,1,2 heat-sum calculation of f,df,G_RR."""
    f=df=g=0.
    for n,N in [(0,12),(1,28),(2,16)]:
        ell=np.arange(1,levels+1,dtype=float)
        e=ell*(ell+n)/R**2
        degeneracy=2*(2*ell+n)
        for a,w in zip(v.NODES,v.WEIGHTS[profile]):
            h=np.exp(-a*e)
            # N counts physical copies; each complete Dirac trace has n zero modes.
            f+=N*w*(n+degeneracy@h)/(48*np.pi**2*a)
            df+=N*w*(degeneracy@(2*e*h/R))/(48*np.pi**2)
            g+=N*w*(degeneracy@(e*h*(1-2*a*e/3)))/(8*np.pi**2*R**2)
    return f,df,g,g+1.5*df*df/f


def eigenmodes(H,G):
    """Two-derivative squared masses / Lambda^2; G-orthonormal vectors."""
    return eigh(np.asarray(H)/(4*np.pi**2),G,check_finite=True)


def geometry_in_H_coordinates(x, G):
    """q=(R,h) from y=(R,H_d/Lambda,H_u/Lambda), h_i=y_i/R."""
    R=x[0]
    J=np.array([[1.,0.,0.],[-x[1]/R,1/R,0.],[-x[2]/R,0.,1/R]])
    return J.T@G@J,J


def fixed_metric_momentum_delta(x, q2, profile='minus', levels=12, quadrature=48):
    """Exact scalar/radius 2-point kernel difference at fixed flat g_J.

    Returns (Pi(q2)-Pi(0))/q2, dimensionless, approaching G_J.
    q2 is Euclidean p^2/Lambda^2; this excludes gravitational response.
    It is a derivative-expansion diagnostic, not an Einstein-frame propagator.
    """
    from numpy.polynomial.legendre import leggauss
    R,hd,hu=x;z,wq=leggauss(quadrature);s=(z+1)/2;wq=wq/2
    out=np.zeros((3,3))
    for kind,n in SECTORS:
        for b in m.blocks(kind,levels):
            D=b['D'];zero=np.zeros_like(D)
            Sd=b['S'][0] if b['S'] else zero
            Su=b['S'][1] if len(b['S'])>1 else zero
            ev,U=eigh(D/R+hd*Sd+hu*Su,check_finite=False)
            T=np.array([U.T@z@U for z in (-D/R**2,Sd,Su)])
            A=(ev[None,:,None]+ev[None,None,:])*T
            for a,w in zip(v.NODES,v.WEIGHTS[profile]):
                i0=np.zeros((len(ev),len(ev)));delta=np.zeros_like(i0)
                for t,wt in zip(s,wq):
                    u=t*(1-t); heat=np.exp(-a*(t*ev[:,None]**2+(1-t)*ev[None,:]**2))
                    i0+=wt*heat*np.exp(-a*u*q2)
                    delta+=wt*heat*(np.expm1(-a*u*q2)/q2 if q2 else -a*u)
                out+=n*w*(np.einsum('ij,aij,bji->ab',i0,T,T)
                           +np.einsum('ij,aij,bji->ab',delta,A,A))/(8*np.pi**2)
    return (out+out.T)/2
