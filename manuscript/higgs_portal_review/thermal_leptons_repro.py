"""Note 36: reproducible partial s1 s1 -> e/mu/tau thermal averaging.

Requires SciPy/NumPy. Fixed-width tree-level benchmark and ideal
Maxwell--Boltzmann bath; not a physical relic density or total annihilation.
All energies in GeV. Pair-counting factor 1/2 for identical incoming
particles belongs in a separately defined event density, not sigma*v.
"""
from __future__ import annotations
import math
from scipy.integrate import quad
from scipy.special import kve, roots_genlaguerre, gammaincc, gamma

M1, K11, MH, GH = 10.0, 0.001, 125.0, 0.0041
MASS = {"e": 0.00051099895, "mu": 0.1056583755, "tau": 1.77686}
W_CUT = 90.0

def sigma_v(s: float, mf: float) -> float:
    """Higgs-only tree-level sigma*v_Moller in the COM, GeV^-2."""
    if not all(map(math.isfinite, (s, mf))) or s < 4*M1*M1 or mf <= 0:
        raise ValueError("finite physical s and lepton mass required")
    if s <= 4*mf*mf:
        return 0.0
    beta_f = math.sqrt(1-4*mf*mf/s)
    denom = (s-MH*MH)**2+(MH*GH)**2
    return K11*K11*mf*mf*beta_f**3/(4*math.pi*denom)

def _weighted(w: float, x: float, mf: float) -> float:
    """Non-exponential integrand for Gauss--Laguerre alpha=1/2."""
    y=2*x+w
    return sigma_v((M1*y/x)**2,mf)*y**3*math.sqrt(4*x+w)*kve(1,y)

def _prefactor(x: float) -> float:
    if not math.isfinite(x) or x <= 0:
        raise ValueError("positive finite x required")
    return 1/(8*x**4*kve(2,x)**2)

def thermal_quad(x: float, mf: float, cut: float=W_CUT) -> tuple[float,float]:
    """Finite adaptive w window; returns (value, QUAD error estimate)."""
    if not math.isfinite(cut) or cut <= 0:
        raise ValueError("positive finite integration window required")
    pref=_prefactor(x)
    value, err=quad(lambda w: math.exp(-w)*math.sqrt(w)*_weighted(w,x,mf),
                    0.,cut,epsabs=1e-27,epsrel=2e-12,limit=400)
    return pref*value,pref*err

def thermal_laguerre(x: float,mf:float,n:int=64) -> float:
    if not isinstance(n,int) or n<8 or n>128:
        raise ValueError("8<=nodes<=128")
    pref=_prefactor(x)
    nodes, weights=roots_genlaguerre(n,.5)
    return float(pref*sum(float(weight)*_weighted(float(w),x,mf)
                          for w,weight in zip(nodes,weights)))

def tail_upper_bound(x:float,mf:float,cut:float=W_CUT) -> float:
    """Analytic positive tail bound for this fixed model; numeric value approximate.

    Bound sigma*v by the Breit--Wigner maximum, sqrt(w(4x+w)) by 2x+w,
    and the decreasing exp(y)*K1(y) by its value at the finite cutoff.
    """
    pref=_prefactor(x)
    if not math.isfinite(cut) or cut<=0 or not math.isfinite(mf) or mf<=0:
        raise ValueError("positive inputs required")
    maxsv=K11*K11*mf*mf/(4*math.pi*(MH*GH)**2)
    moment=0.
    for j in range(5):
        moment+=math.comb(4,j)*(2*x)**(4-j)*gamma(j+1)*gammaincc(j+1,cut)
    return pref*maxsv*kve(1,2*x+cut)*moment

def equilibrium_density(x:float) -> float:
    _prefactor(x)
    temperature=M1/x
    return M1*M1*temperature*math.exp(-x)*kve(2,x)/(2*math.pi**2)

def hubble(x:float,gstar:float=60.) -> float:
    if not math.isfinite(gstar) or gstar<=0:
        raise ValueError("positive gstar required")
    return math.sqrt(8*math.pi**3*gstar/90)*(M1/x)**2/1.2209e19

def summarize(x:float=20.) -> dict:
    vals={f:thermal_quad(x,m)[0] for f,m in MASS.items()}
    tails={f:tail_upper_bound(x,m) for f,m in MASS.items()}
    total=sum(vals.values())
    threshold=sum(sigma_v(4*M1*M1,m) for m in MASS.values())
    return dict(x=x,channels=vals,leptonic_partial=total,
                threshold_partial=threshold,ratio=total/threshold,
                formal_equilibrium_ratio=equilibrium_density(x)*total/hubble(x),
                tail_bound=sum(tails.values()))

if __name__=='__main__':
    for x in (10.,20.,30.):
        s=summarize(x)
        print('x=',x,'partials=',s['channels'],'total=',s['leptonic_partial'],
              'ratio=',s['ratio'],'n_eq*partial/H=',s['formal_equilibrium_ratio'],
              'fixed-model-tail-bound=',s['tail_bound'])
        for f,m in MASS.items():
            v=s['channels'][f]; gl=thermal_laguerre(x,m)
            print(' ',f,'quad vs GaussLaguerre rel=',abs(v-gl)/v)
