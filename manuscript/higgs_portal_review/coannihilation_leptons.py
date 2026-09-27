"""Research Note 39: charged-lepton partial thermal rates for 11/12/22.

Restricted two-real-singlet Higgs portal at the illustrative compressed point.
Requires SciPy. This is not a complete collision operator or relic density.
All energies are in GeV.
"""
from __future__ import annotations
import math
from scipy.integrate import quad
from scipy.special import kv, kve, gammaincc, gamma

M1, M2 = 10.0, 11.5
MH, GH = 125.0, 0.0041
K11, K12, K22 = 0.001, -0.001, 0.001
MASS = {"e": 0.00051099895, "mu": 0.1056583755, "tau": 1.77686}
W_CUT = 90.0


def _check_pair(T: float, mi: float, mj: float, kij: float, mf: float) -> None:
    vals=(T,mi,mj,kij,mf)
    if not all(math.isfinite(v) for v in vals) or T<=0 or mi<=0 or mj<=0 or mf<=0:
        raise ValueError("finite positive T/masses and finite coupling required")


def sigma_s(s: float, mi: float, mj: float, kij: float, mf: float) -> float:
    """Tree-level s_i s_j -> f fbar cross section in GeV^-2.

    Uses L_int superset -(v/2)h[K11 s1^2+2K12 s1s2+K22 s2^2]
    and -(mf/v)h fbar f. No initial-state pair-counting factor is inserted.
    """
    _check_pair(1.0,mi,mj,kij,mf)
    if not math.isfinite(s) or s < (mi+mj)**2:
        raise ValueError("s must be finite and above the initial threshold")
    if s <= 4*mf*mf or kij == 0:
        return 0.0
    lam=(s-(mi+mj)**2)*(s-(mi-mj)**2)
    if lam <= 0:
        return math.inf  # cross section diverges as 1/p_i at exact threshold
    beta_f=math.sqrt(1-4*mf*mf/s)
    denom=(s-MH*MH)**2+(MH*GH)**2
    return kij*kij*mf*mf*s*beta_f**3/(8*math.pi*denom*math.sqrt(lam))


def thermal_pair_quad(T: float, mi: float, mj: float, kij: float,
                      mf: float, cut: float=W_CUT) -> tuple[float,float]:
    """Finite-window MB thermal average and QUAD error estimate, GeV^-2.

    Implements the unequal-mass invariant integral after w=sqrt(s)/T-xi-xj.
    The omitted positive tail is separately bounded by tail_upper_bound().
    """
    _check_pair(T,mi,mj,kij,mf)
    if not math.isfinite(cut) or cut<=0:
        raise ValueError("positive finite cut required")
    xi,xj=mi/T,mj/T
    a=xi+xj
    b=abs(xi-xj)
    pref=kij*kij*mf*mf/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj))
    def integrand(w: float) -> float:
        y=a+w
        L=(y*y-a*a)*(y*y-b*b)
        if L<=0:
            return 0.0
        s=(T*y)**2
        if s<=4*mf*mf:
            return 0.0
        beta_f=math.sqrt(1-4*mf*mf/s)
        denom=(s-MH*MH)**2+(MH*GH)**2
        return math.exp(-w)*y*y*math.sqrt(L)*beta_f**3*kve(1,y)/denom
    value,err=quad(integrand,0.0,cut,epsabs=1e-30,epsrel=2e-12,limit=500)
    return pref*value,pref*err


def thermal_pair_direct(T: float, mi: float, mj: float, kij: float,
                        mf: float, cut: float=W_CUT) -> float:
    """Independent q=sqrt(s) finite-window implementation of the invariant formula."""
    _check_pair(T,mi,mj,kij,mf)
    if not math.isfinite(cut) or cut<=0:
        raise ValueError("positive finite cut required")
    xi,xj=mi/T,mj/T
    denom_norm=8*mi*mi*mj*mj*T*kv(2,xi)*kv(2,xj)
    q0=mi+mj
    q1=q0+T*cut
    def fq(q: float) -> float:
        s=q*q
        lam=(s-(mi+mj)**2)*(s-(mi-mj)**2)
        if lam<=0 or s<=4*mf*mf:
            return 0.0
        beta_f=math.sqrt(1-4*mf*mf/s)
        D=(s-MH*MH)**2+(MH*GH)**2
        sig=kij*kij*mf*mf*s*beta_f**3/(8*math.pi*D*math.sqrt(lam))
        return 2*q*sig*lam/q*kv(1,q/T)
    value,_=quad(fq,q0,q1,epsabs=1e-40,epsrel=2e-11,limit=500)
    return value/denom_norm


def tail_upper_bound(T: float, mi: float, mj: float, kij: float,
                     mf: float, cut: float=W_CUT) -> float:
    """Positive high-w tail bound for this fixed-width tree-level kernel."""
    _check_pair(T,mi,mj,kij,mf)
    if not math.isfinite(cut) or cut<=0:
        raise ValueError("positive finite cut required")
    xi,xj=mi/T,mj/T
    a=xi+xj
    pref=kij*kij*mf*mf/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj))
    moment=0.0
    for j in range(5):
        moment += math.comb(4,j)*a**(4-j)*gamma(j+1)*gammaincc(j+1,cut)
    return pref*kve(1,a+cut)*moment/(MH*GH)**2


def equilibrium_density(T: float, m: float) -> float:
    if not all(math.isfinite(v) for v in (T,m)) or T<=0 or m<=0:
        raise ValueError("positive finite T,m required")
    x=m/T
    return m*m*T*math.exp(-x)*kve(2,x)/(2*math.pi**2)


def equilibrium_fractions(T: float) -> tuple[float,float]:
    n1=equilibrium_density(T,M1); n2=equilibrium_density(T,M2)
    total=n1+n2
    return n1/total,n2/total


def leptonic_pair_partial(T: float, pair: str) -> float:
    table={"11":(M1,M1,K11),"12":(M1,M2,K12),"22":(M2,M2,K22)}
    if pair not in table:
        raise ValueError("pair must be 11, 12, or 22")
    mi,mj,k=table[pair]
    return sum(thermal_pair_quad(T,mi,mj,k,mf)[0] for mf in MASS.values())


def conditional_leptonic_sigma_eff(T: float) -> dict:
    r1,r2=equilibrium_fractions(T)
    rates={p:leptonic_pair_partial(T,p) for p in ("11","12","22")}
    weights={"11":r1*r1,"12":2*r1*r2,"22":r2*r2}
    pieces={p:weights[p]*rates[p] for p in rates}
    return {"T":T,"r1":r1,"r2":r2,"weights":weights,"rates":rates,
            "pieces":pieces,"sigma_eff":sum(pieces.values())}

if __name__ == "__main__":
    out=conditional_leptonic_sigma_eff(0.5)
    print(out)
