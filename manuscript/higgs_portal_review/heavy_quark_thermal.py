"""Note 40: bottom/charm scalar-current thermal contribution, not total QCD.

Leading-power NLO coefficient with two-loop MS running; inherited two-singlet
benchmark. A separate massive-Born phase factor is a sensitivity diagnostic,
NOT a finite-mass NLO calculation. No HDECAY/RunDec executable or Omnes data
is imported. Requires SciPy. Energies GeV, thermal rates GeV^-2.

Primary formulas: hep-ph/0004189 Eqs. (1),(2),(6),(7);
hep-ph/0511063v2 Eq. (3). Historical inputs: 0907.2110v2 Sec. IV.
"""
from __future__ import annotations
import math
from functools import lru_cache
from typing import Callable
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gamma, gammaincc, kv, kve

M1, M2, MH, GH, V = 10.0, 11.5, 125.0, 0.0041, 246.0
PAIRS = {"11": (M1, M1, 0.001), "12": (M1, M2, -0.001),
         "22": (M2, M2, 0.001)}
# Frozen historical central inputs, NOT latest fits, EFT predictions, or errors.
MZ, ALPHA_MZ = 91.1876, 0.1189
MB_AT_10, MC_AT_3, MATCH_B = 3.610, 0.986, 4.163
W_CUT = 90.0


def rg_coefficients(nf: int) -> tuple[float, float, float, float]:
    """a=alpha_s/pi; derivative with respect to log(mu^2)."""
    if type(nf) is not int or nf not in (4, 5):
        raise ValueError("only nf=4 or 5 is implemented")
    return (11 - 2*nf/3)/4, (102 - 38*nf/3)/16, 1., (202/3 - 20*nf/9)/16


def a_fixed_nf(mu: float, mu0: float, a0: float, nf: int) -> float:
    """Exact implicit solution of the TWO-LOOP-TRUNCATED beta ODE."""
    if not all(math.isfinite(x) and x > 0 for x in (mu, mu0, a0)):
        raise ValueError("positive finite RG boundary inputs required")
    b0, b1, _, _ = rg_coefficients(nf)
    c = b1/b0
    def F(a: float) -> float:
        return 1/a + c*math.log(a/(1+c*a))
    target = F(a0) + 2*b0*math.log(mu/mu0)
    if target <= F(1.):
        raise ValueError("requested scale outside perturbative solver bracket")
    return brentq(lambda a: F(a)-target, 1e-9, 1., xtol=2e-15, rtol=1e-14)


@lru_cache(maxsize=16384)
def alpha_s(mu: float) -> float:
    """Two-loop alpha with nf=4 below MATCH_B, nf=5 above; continuity matching.

    The numerical matching is at the declared scale only. High-order matching
    and a top-threshold transition are deliberately not implemented.
    """
    if not math.isfinite(mu) or not 3. <= mu <= 160.:
        raise ValueError("RG scale must lie in [3,160] GeV")
    if mu >= MATCH_B:
        return math.pi*a_fixed_nf(mu, MZ, ALPHA_MZ/math.pi, 5)
    a_b = a_fixed_nf(MATCH_B, MZ, ALPHA_MZ/math.pi, 5)
    return math.pi*a_fixed_nf(mu, MATCH_B, a_b, 4)


def mass_ratio(a: float, a0: float, nf: int) -> float:
    """Exact mass ratio for the same two-loop-truncated beta/gamma ODEs."""
    if not all(math.isfinite(x) and x > 0 for x in (a, a0)):
        raise ValueError("positive finite running couplings required")
    b0, b1, g0, g1 = rg_coefficients(nf)
    return (a/a0)**(g0/b0)*((b0+b1*a)/(b0+b1*a0))**(g1/b1-g0/b0)


def running_mass(flavor: str, mu: float) -> float:
    """MS masses from mb(10)=3.610 and mc(3)=0.986; central values only."""
    if flavor not in ("b", "c"):
        raise ValueError("only b and c scalar currents are included")
    if not math.isfinite(mu) or not 10. <= mu <= 160.:
        raise ValueError("mass evaluation scale must lie in [10,160] GeV")
    a = alpha_s(mu)/math.pi
    if flavor == "b":
        return MB_AT_10*mass_ratio(a, alpha_s(10.)/math.pi, 5)
    a_b, a_3 = alpha_s(MATCH_B)/math.pi, alpha_s(3.)/math.pi
    return MC_AT_3*mass_ratio(a_b, a_3, 4)*mass_ratio(a, a_b, 5)


def qcd_coefficient(Q: float, mu: float, alpha: float, order: int = 1) -> float:
    """Leading-power inclusive quark-current coefficient through O(alpha_s).

    2 log(mu^2/Q^2) follows from RG invariance of mbar(mu)^2 R.
    order=0 switches off the hard coefficient, NOT the mass running.
    """
    if type(order) is not int or order not in (0, 1):
        raise ValueError("only order 0 or 1 implemented")
    if not all(math.isfinite(x) and x > 0 for x in (Q, mu)) or not math.isfinite(alpha) or alpha < 0:
        raise ValueError("invalid hard-coefficient arguments")
    return 1. if order == 0 else 1. + alpha/math.pi*(17/3 + 2*math.log(mu*mu/(Q*Q)))


def current_weight(Q: float, flavor: str, scale: float = 1.,
                   order: int = 1, born_phase: bool = False) -> float:
    """S_q=3 mbar_q(mu)^2 R_q, GeV^2. Q=sqrt(s), mu=scale*Q.

    born_phase=True multiplies by [1-4 mbar(mu)^2/Q^2]^(3/2) as an
    explicitly non-systematic sensitivity diagnostic, not full massive NLO.
    """
    if not math.isfinite(Q) or not 20. <= Q <= 80.:
        raise ValueError("hard energy must lie in [20,80] GeV; no low-energy QCD")
    if not math.isfinite(scale) or not 0.5 <= scale <= 2.:
        raise ValueError("scale factor must lie in [0.5,2]")
    mu = scale*Q
    m = running_mass(flavor, mu)
    R = qcd_coefficient(Q, mu, alpha_s(mu), order)
    if R <= 0:
        raise ValueError("nonpositive truncated spectral coefficient")
    phase = max(0., 1-4*m*m/(Q*Q))**1.5 if born_phase else 1.
    return 3*m*m*R*phase


def _pair_setup(T: float, pair: str, cut: float) -> tuple[float, float, float]:
    if pair not in PAIRS:
        raise ValueError("pair must be 11, 12, or 22")
    if not math.isfinite(T) or not 1/3 <= T <= .5:
        raise ValueError("audited temperature window is [1/3,0.5] GeV")
    if not math.isfinite(cut) or not 0 < cut <= 100:
        raise ValueError("finite window must be in (0,100]")
    return PAIRS[pair]


def thermal_from_weight(T: float, pair: str, weight: Callable[[float], float],
                        cut: float = W_CUT, method: str = "w") -> tuple[float, float]:
    """Thermal average over a finite window for a supplied S(Q), in GeV^-2.

    w and Q methods use different variables, Jacobians and Bessel scaling.
    This numerical comparison does not independently derive the QFT amplitude.
    """
    mi, mj, k = _pair_setup(T, pair, cut)
    xi, xj = mi/T, mj/T
    a, b = xi+xj, abs(xi-xj)
    if method == "w":
        pref = k*k/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj))
        def f(w: float) -> float:
            y = a+w
            lam = w*(2*a+w)*(y*y-b*b)
            Q = T*y
            return math.exp(-w)*y*y*math.sqrt(max(0.,lam))*weight(Q)*kve(1,y)/((Q*Q-MH*MH)**2+(MH*GH)**2)
        v, e = quad(f, 0., cut, epsabs=1e-24, epsrel=2e-11, limit=300)
        return pref*v, pref*e
    if method == "Q":
        norm = 8*mi*mi*mj*mj*T*kv(2,xi)*kv(2,xj)
        def f(Q: float) -> float:
            s = Q*Q
            lam = (s-(mi+mj)**2)*(s-(mi-mj)**2)
            if lam <= 0:
                return 0.
            sig = k*k*s*weight(Q)/(8*math.pi*((s-MH*MH)**2+(MH*GH)**2)*math.sqrt(lam))
            return 2*sig*lam*kv(1,Q/T)
        v, e = quad(f, mi+mj, mi+mj+T*cut, epsabs=1e-55, epsrel=2e-11, limit=300)
        return v/norm, e/norm
    raise ValueError("method must be w or Q")


def thermal_quark(T: float, pair: str, flavor: str, scale: float = 1.,
                  order: int = 1, born_phase: bool = False,
                  method: str = "w", cut: float = W_CUT) -> tuple[float, float]:
    return thermal_from_weight(T, pair,
        lambda Q: current_weight(Q, flavor, scale, order, born_phase), cut, method)


def formal_tail_bound(T: float, pair: str, flavor: str,
                      scale: float = 1., cut: float = W_CUT) -> float:
    """Tail bound ONLY for formal fixed-nf5 continuation of this NLO proxy.

    Does not bound missing physical channels or top-threshold corrections.
    For fixed scale in [0.5,2], S(Q) decreases above the initial Q threshold.
    """
    mi, mj, k = _pair_setup(T, pair, cut)
    xi, xj = mi/T, mj/T
    a = xi+xj
    smax = current_weight(mi+mj, flavor, scale)
    moment = sum(math.comb(4,j)*a**(4-j)*gamma(j+1)*gammaincc(j+1,cut) for j in range(5))
    pref = k*k/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj))
    return pref*smax*kve(1,a+cut)*moment/(MH*GH)**2


def equilibrium_weights(T: float) -> dict[str, float]:
    _pair_setup(T, "11", W_CUT)
    q = (M2/M1)**2*math.exp(-(M2-M1)/T)*kve(2,M2/T)/kve(2,M1/T)
    r2 = q/(1+q)
    return {"11": (1-r2)**2, "12": 2*r2*(1-r2), "22": r2*r2}


def summary(T: float = .5) -> dict:
    weights = equilibrium_weights(T)
    variants = {}
    for label, scale, order, phase in (("central_LP_NLO",1.,1,False),
            ("mu_half",.5,1,False), ("mu_double",2.,1,False),
            ("running_Born_LP",1.,0,False), ("Born_phase_diagnostic",1.,1,True)):
        channels = {p: {q: thermal_quark(T,p,q,scale,order,phase)[0] for q in ("b","c")} for p in PAIRS}
        totals = {p: sum(channels[p].values()) for p in PAIRS}
        variants[label] = {"channels_GeV_minus2": channels, "pair_totals_GeV_minus2": totals,
                          "conditional_effective_GeV_minus2": sum(weights[p]*totals[p] for p in PAIRS)}
    checks = {}
    for p in PAIRS:
        checks[p] = {}
        for q in ("b","c"):
            w = thermal_quark(T,p,q)[0]
            direct = thermal_quark(T,p,q,method="Q")[0]
            checks[p][q] = {"Q_vs_w_relative": abs(direct/w-1),
                           "formal_tail_GeV_minus2": formal_tail_bound(T,p,q)}
    return {"temperature_GeV":T,
            "inputs": {"alpha_s_MZ":ALPHA_MZ,"MZ_GeV":MZ,"mb10_GeV":MB_AT_10,
                       "mc3_GeV":MC_AT_3,"matching_scale_GeV":MATCH_B},
            "running_at_20_GeV": {"alpha_s":alpha_s(20.),"mb_GeV":running_mass("b",20.),"mc_GeV":running_mass("c",20.)},
            "equilibrium_weights_ASSUMED":weights,"variants":variants,"numerical_checks":checks,
            "scope":"Leading-power NLO bottom/charm-current approximation only; not full massive NLO, full QCD, relic density, or a rigorous physical lower bound."}


if __name__ == "__main__":
    import json
    print(json.dumps(summary(), indent=2))
