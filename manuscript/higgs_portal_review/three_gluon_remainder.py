"""Note 47: source-audited coherent massive-loop three-gluon finite remainder.

The C_i helicity combinations transcribe hep-ph/9504378 (C.5)-(C.10).
The printed (C.14) has a factor mismatch against those combinations in its
heavy-mass/collinear limits. Here the common 1/2 is DERIVED from soft-emission
normalization and identical-state phase space, NOT silently ascribed to C.14.
This is a finite subtracted real piece, not the full NLO rate or a probability.
"""
from __future__ import annotations
import math
from functools import lru_cache
import numpy as np
from scipy.special import spence, roots_legendre
import heavy_quark_thermal as h
import gluon_loop_thermal as g

COMPONENTS=('bb','cc','bc','coherent')


def fg(t):
    """Timelike functions with the source m^2 -> m^2-i0 prescription."""
    t=np.asarray(t,dtype=complex)
    f=np.arcsin(np.sqrt(t))**2
    return f,np.sqrt(1/t-1)*np.arcsin(np.sqrt(t))


def box_i3(S,T,U,X):
    root=np.sqrt(1+4*T/(S*U))
    bm=-2*T/(S*U)/(1+root);bp=1-bm
    ar=np.sqrt(1-4/X);am=2/X/(1+ar);ap=1-am
    li=lambda z:spence(1-z)
    v=(li(bm/(bm-am))-li(bp/(bp-ap))+li(bm/(bm-ap))-li(bp/(bp-am))
       +np.log(-bp/bm)*np.log1p(X*T/(S*U)))
    return 2*v/(S*U*(bp-bm))


def box_j(S,T,U):
    """Dimensionless equal-internal-mass one-mass box, source (C.9).

    S,T,U are already complex with their common positive infinitesimal.
    An independently integrated log representation is supplied in tests.
    """
    return box_i3(S,T,U,S)+box_i3(S,T,U,U)-box_i3(S,T,U,S+T+U)


def coefficients(S,T,U):
    """Rows P_1j,P_4j of the CP-even source matrix; unmodified normalization."""
    S,T,U=np.broadcast_arrays(S,T,U);rho=S+T+U
    p=np.zeros((12,)+S.shape,complex);q=np.zeros_like(p)
    p[0]=-12*S*(U*T-S*S)/((U+S)*(T+S))
    p[1]=3*(4*U**3*T**3+8*U**3*T*T*S+4*U**3*T*S*S
        +8*U*U*T**3*S+15*U*U*T*T*S*S+4*U*U*T*T*S
        +8*U*U*T*S**3+8*U*U*T*S*S+U*U*S**4-4*U*U*S**3
        +4*U*T**3*S*S+8*U*T*T*S**3+8*U*T*T*S*S
        +8*U*T*S**4+16*U*T*S**3+4*U*S**5-8*U*S**4
        +T*T*S**4-4*T*T*S**3+4*T*S**5-8*T*S**4+3*S**6-12*S**5
        )/(S*(U+S)**2*(T+S)**2)
    p[2]=-3*(S-4)
    p[3]=-3*(4*U**3*T+8*U*U*T*S-U*U*S*S+4*U*U*S
        +4*U*T*S*S+8*U*S*S+S**4-4*S**3)/(S*(U+S)**2)
    p[4]=-3*(4*U*T**3+8*U*T*T*S+4*U*T*S*S-T*T*S*S
        +4*T*T*S+8*T*S*S+S**4-4*S**3)/(S*(T+S)**2)
    p[5]=-12*U*T*(U*U*T+2*U*U*S+U*T*T+4*U*T*S+5*U*S*S
        +2*T*T*S+5*T*S*S+4*S**3)/((U+S)**2*(T+S)**2)
    p[7]=12*U*T*(U+2*S)/(U+S)**2
    p[8]=12*U*T*(T+2*S)/(T+S)**2
    p[9]=3*U*S*(4-S)/2;p[10]=3*T*S*(4-S)/2
    p[11]=-3*U*T/S*(4*U*T-S*S+12*S)/2
    q[0]=12*rho;q[1]=-9*(4-rho);q[2:5]=3*(4-rho)
    q[9]=3*U*S*(4-rho)/2;q[10]=3*T*S*(4-rho)/2;q[11]=3*U*T*(4-rho)/2
    return p,q


def helicities(rho: float,x,y,regulator: float=1e-24):
    """Source's four C_i for one loop; x=s/Q^2, y=t/Q^2, z=1-x-y."""
    if not math.isfinite(rho) or rho<=0:raise ValueError('positive finite rho required')
    if not math.isfinite(regulator) or regulator<=0:raise ValueError('positive regulator required')
    x,y=np.broadcast_arrays(np.asarray(x,float),np.asarray(y,float));z=1-x-y
    if not np.all(np.isfinite(x)&np.isfinite(y)&(x>0)&(y>0)&(z>0)):
        raise ValueError('point must lie inside the massless decay triangle')
    rc=rho*(1+regulator*1j);S,T,U=rc*x,rc*y,rc*z
    fQ,gQ=fg(np.full_like(S,rc/4));fs,gs=fg(S/4);ft,gt=fg(T/4);fu,gu=fg(U/4)
    t=np.stack([np.ones_like(S),2*fQ,2*fs,2*ft,2*fu,2*(1-gQ),
                2*(1-gs),2*(1-gt),2*(1-gu),box_j(S,T,U),box_j(S,U,T),box_j(T,S,U)])
    p,q=coefficients(S,T,U)
    a1=np.sum(p*t,axis=0)/(2*rc*rc);a4=np.sum(q*t,axis=0)/(2*rc*rc)
    p2,_=coefficients(T,S,U)
    a2=-np.sum(p2*t[[0,1,3,2,4,5,7,6,8,11,10,9]],axis=0)/(2*rc*rc)
    p3,_=coefficients(U,T,S)
    a3=np.sum(p3*t[[0,1,4,3,2,5,8,7,6,9,11,10]],axis=0)/(2*rc*rc)
    return np.stack([a1,a2,a3,a4])


def _hard(Q,scale,scheme):
    g._hard(Q,scale)
    if scheme not in ('MSbar','pole1'):raise ValueError('scheme must be MSbar or pole1')
    return {q:h.running_mass(q,Q*scale) if scheme=='MSbar' else g.auxiliary_pole_mass(q) for q in ('b','c')}


def shape_components(Q: float,x,y,scale: float=1.,scheme: str='MSbar',printed: bool=False):
    """Unnormalized finite shape [A-P B]/(2xyz), bb/cc/bc/coherent.

    printed=True is an explicitly failing source-consistency diagnostic:
    [A-P B/2]/xyz as printed in (C.14), NOT a physical finite integrand.
    """
    masses=_hard(Q,scale,scheme);x,y=np.broadcast_arrays(x,y);z=1-x-y
    cb=helicities((Q/masses['b'])**2,x,y);cc=helicities((Q/masses['c'])**2,x,y)
    fb,fc=[g.form_factor((Q/(2*masses[q]))**2) for q in ('b','c')]
    A=np.stack([np.sum(abs(cb)**2,axis=0),np.sum(abs(cc)**2,axis=0),
                2*np.sum((cb*cc.conjugate()).real,axis=0)])
    B=np.array([abs(fb)**2,abs(fc)**2,2*(fb*fc.conjugate()).real])
    B=B.reshape((3,)+(1,)*np.ndim(x))
    P=1+x**4+y**4+z**4
    out=(A-.5*P*B)/(x*y*z) if printed else (A-P*B)/(2*x*y*z)
    return np.concatenate([out,np.sum(out,axis=0,keepdims=True)],axis=0)


@lru_cache(maxsize=32)
def nodes(n):
    if type(n) is not int or not 8<=n<=256:raise ValueError('8<=n<=256 integer required')
    a,b=roots_legendre(n);return (a+1)/2,b/2


def finite_remainder(Q:float,scale:float=1.,scheme:str='MSbar',n:int=32,eps:float=0.):
    """Mapped quadrature over six equal sectors x<=y<=z, with branch splits.

    Returns four signed shape coefficients, not rates. eps>0 is only a
    diagnostic omitting strips where min(x,y,z)<eps. No all-domain rigorous
    numerical-error certificate or infinity-domain physics is claimed.
    """
    masses=_hard(Q,scale,scheme);u,w=nodes(n)
    if not math.isfinite(eps) or not 0<=eps<.1:raise ValueError('0<=eps<.1 required')
    thresholds=sorted(4*(m/Q)**2 for m in masses.values())
    # Changes to the y partitions also occur at x=(1-q)/2 or 1-2q;
    # for this hard domain both lie above x=1/3 and do not occur here.
    cuts=sorted({eps,1/3,*[a for a in thresholds if eps<a<1/3]})
    acc=np.zeros(4)
    for lo,hi in zip(cuts,cuts[1:]):
        # Linear map keeps the smallest x above the cancellation-dominated
        # machine endpoint; branch cusp convergence is checked by node scans.
        for x,wx in zip(lo+(hi-lo)*u,(hi-lo)*w):
            ylo=x;yhi=(1-x)/2
            yc=sorted({ylo,yhi,*[a for a in thresholds if ylo<a<yhi],
                       *[1-x-a for a in thresholds if ylo<1-x-a<yhi]})
            for yl,yh in zip(yc,yc[1:]):
                # Smooth square-root loop thresholds at interval endpoints.
                theta=.5*math.pi*u
                y=yl+(yh-yl)*np.sin(theta)**2
                wy=(yh-yl)*.5*math.pi*np.sin(2*theta)*w
                acc+=6*wx*np.sum(shape_components(Q,x,y,scale,scheme)*wy,axis=1)
    return acc


def current_components(Q:float,scale:float=1.,scheme:str='MSbar',n:int=32):
    a=h.alpha_s(scale*Q)/math.pi
    return a**3*Q**2/9*finite_remainder(Q,scale,scheme,n)


def thermal_components(T:float=.5,pair:str='11',scale:float=1.,scheme:str='MSbar',
                       angular_n:int=32,thermal_n:int=24,method:str='laguerre'):
    """Four finite-window components in GeV^-2; convergence checks not bounds.

    laguerre uses scaled Bessel functions and exp(-w)*sqrt(w) weight;
    Q uses unscaled Bessel functions and sqrt((Q-Qmin)/T) quadrature.
    Both retain w<=90 and do NOT certify the physical spectrum to infinity.
    """
    from scipy.special import roots_genlaguerre,kve,kv
    mi,mj,k=h._pair_setup(T,pair,h.W_CUT)
    if type(thermal_n) is not int or not 8<=thermal_n<=128:
        raise ValueError('thermal node count in [8,128] required')
    _hard(mi+mj,scale,scheme);nodes(angular_n)
    xi,xj=mi/T,mj/T;a=xi+xj;b=xi-xj
    acc=np.zeros(4)
    if method=='laguerre':
        us,ws=roots_genlaguerre(thermal_n,.5)
        pref=k*k/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj))
        for w,weight in zip(us,ws):
            if w>h.W_CUT:continue
            y=a+w;Q=T*y
            fac=y*y*math.sqrt((2*a+w)*(y*y-b*b))*kve(1,y)/((Q*Q-h.MH*h.MH)**2+(h.MH*h.GH)**2)
            acc+=weight*fac*current_components(float(Q),scale,scheme,angular_n)
        return pref*acc
    if method=='Q':
        us,ws=roots_legendre(thermal_n)
        ts=(us+1)*math.sqrt(h.W_CUT)/2;ws=ws*math.sqrt(h.W_CUT)/2
        norm=8*mi*mi*mj*mj*T*kv(2,xi)*kv(2,xj)
        for t,weight in zip(ts,ws):
            Q=mi+mj+T*t*t;s=Q*Q
            lam=(s-(mi+mj)**2)*(s-(mi-mj)**2)
            fac=(2*T*t)*k*k*s*math.sqrt(lam)*kv(1,Q/T)/(4*math.pi*((s-h.MH*h.MH)**2+(h.MH*h.GH)**2))
            acc+=weight*fac*current_components(float(Q),scale,scheme,angular_n)
        return acc/norm
    raise ValueError('method must be laguerre or Q')


if __name__ == '__main__':
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--Q',type=float,default=20.)
    parser.add_argument('--nodes',type=int,default=32)
    parser.add_argument('--pair',choices=['11','12','22'],default=None)
    args=parser.parse_args()
    values=(thermal_components(pair=args.pair,angular_n=args.nodes) if args.pair
            else finite_remainder(args.Q,n=args.nodes))
    print(json.dumps({'kind':'finite_thermal_remainder_GeV_minus2' if args.pair
                     else 'dimensionless_finite_shape',
                     'components':dict(zip(COMPONENTS,map(float,values))),
                     'complete_NLO_rate':False},indent=2))
