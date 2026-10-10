"""Independent integral checks for Note 47's scalar box, not a second QFT derivation."""
import math
import numpy as np
from scipy.integrate import quad
from scipy.special import roots_legendre


def log_box(S:float,T:float,U:float) -> complex:
    """J = integral log[(1-Sw)(1-Uw)/(1-rho*w)]/[T+SU*w], w=x(1-x).

    Separate logarithms retain each -i0 branch. The timelike roots are
    explicitly split; no multiplication followed by one principal log.
    This representation is derived separately from the dilogarithm sum.
    """
    if not all(math.isfinite(v) and v>0 for v in (S,T,U)):raise ValueError('positive invariants required')
    terms=[(S,1),(U,1),(S+T+U,-1)];cuts={0.,.5,1.};rr={}
    for A,_ in terms:
        if A>=4:
            b=math.sqrt(1-4/A);rm=2/A/(1+b);rp=1-rm
            cuts.update((rm,rp));rr[A]=(rm,rp)
    def integrand(x):
        total=0j
        for A,sign in terms:
            val=A*(x-rr[A][0])*(x-rr[A][1]) if A in rr else 1-A*x*(1-x)
            if val==0: # only reached at a measure-zero floating endpoint
                return 0j
            total+=sign*complex(math.log(abs(val)),-math.pi if val<0 else 0.)
        return total/(T+S*U*x*(1-x))
    ans=0j;cs=sorted(cuts)
    for lo,hi in zip(cs,cs[1:]):
        if hi<=lo:continue
        def fun(t):
            ph=math.pi*t/2;x=lo+(hi-lo)*math.sin(ph)**2
            jac=(hi-lo)*math.pi*math.sin(ph)*math.cos(ph)
            return jac*integrand(x)
        ans+=quad(lambda t:fun(t).real,0,1,epsabs=3e-13,epsrel=3e-12,limit=150)[0]
        ans+=1j*quad(lambda t:fun(t).imag,0,1,epsabs=3e-13,epsrel=3e-12,limit=150)[0]
    return ans


def simplex_box(S:float,T:float,U:float,n:int=20) -> float:
    """Independent 3D Feynman-parameter box below the first threshold only."""
    rho=S+T+U
    if min(S,T,U)<=0 or rho>=3:raise ValueError('this check is below threshold, rho<3')
    u,w=roots_legendre(n);u=(u+1)/2;w=w/2
    a,b,c=np.meshgrid(u,u,u,indexing='ij')
    wa,wb,wc=np.meshgrid(w,w,w,indexing='ij')
    x1=a;x2=(1-a)*b;x3=(1-a)*(1-b)*c;x4=(1-a)*(1-b)*(1-c)
    D=1-S*x1*x3-U*x2*x4-rho*x1*x4
    return float(np.sum(wa*wb*wc*(1-a)**2*(1-b)/D**2))
