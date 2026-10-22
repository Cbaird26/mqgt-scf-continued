"""Note 51: tree-level charged-lepton conversion in a two-real-singlet portal.

Natural units, GeV. Exact vacuum t-channel Higgs propagator and finite
lepton masses; ideal common-temperature Maxwell-Boltzmann (MB) distributions.
Not a complete thermal network, proof of kinetic equilibrium, or relic density.
No previous QCD source file is imported or changed.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from functools import lru_cache
import math
from typing import Callable
from scipy.integrate import quad
from scipy.special import kv, kve, gamma, gammaincc, roots_legendre
from scipy.optimize import brentq

M1, M2, MH, K12 = 10.0, 11.5, 125.0, -0.001
LEPTONS = {"e": 0.00051099895, "mu": 0.1056583755, "tau": 1.77686}
G_LEPTON = 4  # two spins, both lepton charges; NOT an extra vertex multiplier
M_PLANCK = 1.2209e19  # inherited non-reduced convention, GeV
HBAR = 6.582119569e-25  # inherited GeV*s
GAMMA_DECAY_LEPTONIC = 3.060267688e-22  # prior vacuum e+mu partial, not total width
W_MAX = 90.0

@dataclass(frozen=True)
class RateResult:
    value_GeV: float
    quadrature_error_GeV: float
    omitted_tree_MB_tail_bound_GeV: float
    method: str
    w_max: float

def _positive(*values: float) -> None:
    if not all(math.isfinite(v) and v > 0 for v in values):
        raise ValueError("finite positive inputs required")

def _model(mi: float, mj: float, ml: float, coupling: float, mh: float) -> None:
    _positive(mi, mj, ml, mh)
    if not math.isfinite(coupling):
        raise ValueError("finite real coupling required")
    if ml > min(mi, mj):
        raise ValueError("declared kernel domain requires lepton lighter than either scalar")

def _temperature(T: float) -> None:
    if not math.isfinite(T) or not 1/3 <= T <= 0.5:
        raise ValueError("this thermal audit supports 1/3 <= T <= 0.5 GeV")

def kallen_initial(s: float, mi: float, ml: float) -> float:
    """Factorized Kallen function lambda(s,mi^2,ml^2), GeV^4."""
    return (s-(mi+ml)**2)*(s-(mi-ml)**2)

def t_limits(q: float, mi: float, mj: float, ml: float) -> tuple[float, float]:
    """Exact physical t interval. t=(p_lepton-p'_lepton)^2 <= 0.

    A rationalized forward endpoint avoids cancellation for electrons.
    q=sqrt(s); both initial and final two-body thresholds must be satisfied.
    """
    _model(mi,mj,ml,1.,MH)
    _positive(q)
    if q < max(mi,mj)+ml:
        raise ValueError("q below initial/final threshold")
    s=q*q
    li=max(0.,kallen_initial(s,mi,ml))
    lf=max(0.,kallen_initial(s,mj,ml))
    pi,pf=math.sqrt(li)/(2*q),math.sqrt(lf)/(2*q)
    Ei,Ef=(s+ml*ml-mi*mi)/(2*q),(s+ml*ml-mj*mj)/(2*q)
    if mi == mj:
        tp=0.
    else:
        de=(mj*mj-mi*mi)/(2*q)
        den=Ei*Ef-ml*ml+pi*pf
        if den <= 0:
            raise ArithmeticError("invalid forward-endpoint denominator")
        tp=-2*ml*ml*de*de/den
    return tp-4*pi*pf,tp

def matrix_element_sq(t: float, ml: float, coupling: float=K12,
                      mh: float=MH) -> float:
    """Initial lepton-spin averaged |M|^2; one lepton charge, no bath factors.

    L contains -v K12 h s1 s2 -(ml/v) h lbar l.
    (1/2)Tr[(k'+ml)(k+ml)] = 4ml^2-t.
    No Higgs width is inserted in the spacelike propagator.
    """
    _positive(mh)
    if not math.isfinite(ml) or ml < 0 or not math.isfinite(coupling):
        raise ValueError("nonnegative finite ml and finite coupling required")
    if not math.isfinite(t) or t > 0:
        raise ValueError("physical spacelike t<=0 required")
    return coupling**2*ml**2*(4*ml**2-t)/(mh**2-t)**2

def _log_remainder(d: float) -> float:
    """log(1+d)-d/(1+d) without cancellation for small positive d."""
    if d < 0.005:
        return math.fsum((-1)**n*(n-1)/n*d**n for n in range(2,12))
    return math.log1p(d)-d/(1+d)

def t_integral(q: float, mi: float, mj: float, ml: float,
               mh: float=MH, contact: bool=False) -> float:
    """Dimensionless integral of (4ml^2-t)/(mh^2-t)^2 over physical t.

    Contact=True replaces only the propagator by mh^-4; it is a diagnostic.
    The massive exact propagator is the default.
    """
    _model(mi,mj,ml,1.,mh)
    if not math.isfinite(q) or q < max(mi,mj)+ml:
        raise ValueError("finite q above both thresholds required")
    if q == max(mi,mj)+ml:
        return 0.
    tm,tp=t_limits(q,mi,mj,ml)
    lo,hi=-tp,-tm
    if contact:
        return (hi-lo)*(4*ml*ml+(hi+lo)/2)/mh**4
    r=lo/mh**2
    d=(hi-lo)/(mh**2+lo)
    a=4*ml*ml/mh**2
    return _log_remainder(d)+(a+r)/(1+r)*d/(1+d)

@lru_cache(maxsize=8)
def _angles(n: int):
    if type(n) is not int or n < 16:
        raise ValueError("at least 16 angular nodes required")
    return roots_legendre(n)

def t_integral_angular(q: float, mi: float, mj: float, ml: float,
                       mh: float=MH) -> float:
    """Independent CM-angle quadrature using unrearranged four-momenta."""
    if q <= max(mi,mj)+ml:
        return 0.
    s=q*q
    pi=math.sqrt(kallen_initial(s,mi,ml))/(2*q)
    pf=math.sqrt(kallen_initial(s,mj,ml))/(2*q)
    Ei=(s+ml*ml-mi*mi)/(2*q)
    Ef=(s+ml*ml-mj*mj)/(2*q)
    c,w=_angles(32)
    t=2*ml*ml-2*Ei*Ef+2*pi*pf*c
    return float(2*pi*pf*sum(w*(4*ml*ml-t)/(mh*mh-t)**2))

def reduced_kernel(q: float, mi: float, mj: float, ml: float,
                   coupling: float=K12, mh: float=MH,
                   contact: bool=False) -> float:
    """W=lambda_initial*sigma, GeV^2. Symmetric under mi<->mj."""
    _model(mi,mj,ml,coupling,mh)
    return coupling**2*ml**2/(16*math.pi)*t_integral(q,mi,mj,ml,mh,contact)

def cross_section(q: float, mi: float, mj: float, ml: float,
                  coupling: float=K12, mh: float=MH) -> float:
    """Cross section in GeV^-2 away from threshold.

    Exothermic sigma can diverge as 1/p_initial at its exact endpoint.
    Use reduced_kernel for integration there; do not evaluate 0/0.
    """
    _model(mi,mj,ml,coupling,mh)
    _positive(q)
    if q < max(mi,mj)+ml or coupling == 0:
        return 0.
    if q == max(mi,mj)+ml:
        raise ValueError("use reduced_kernel at exact threshold")
    return reduced_kernel(q,mi,mj,ml,coupling,mh)/kallen_initial(q*q,mi,ml)

def number_density_MB(T: float, mass: float, degeneracy: int=1) -> float:
    _positive(T,mass)
    if type(degeneracy) is not int or degeneracy <= 0:
        raise ValueError("positive integer degeneracy required")
    x=mass/T
    return degeneracy*mass*mass*T*math.exp(-x)*kve(2,x)/(2*math.pi**2)

def _prefactor(T,mi,mj,ml,coupling,mh):
    q0=max(mi,mj)+ml
    pref=(G_LEPTON*T*coupling**2*ml**2
          *math.exp(-(q0-mi)/T)/(128*math.pi**3*mi**2*kve(2,mi/T)))
    return q0,pref

def tail_bound(T: float, mi: float, mj: float, ml: float,
               coupling: float=K12, mh: float=MH, w_max: float=W_MAX) -> float:
    """Analytic bound on the omitted exact-vacuum-tree/MB integral.

    Since -s<=t<=0 and scalar masses >= ml,
      I(s) <= [4 ml^2 s+s^2/2]/mh^4.
    exp(y) K1(y) decreases. Integrate the resulting positive polynomial
    times exp(-w) with incomplete Gamma functions, w>w_max.
    This is not a bound on missing medium effects or additional reactions.
    """
    _temperature(T); _model(mi,mj,ml,coupling,mh); _positive(w_max)
    q0,pref=_prefactor(T,mi,mj,ml,coupling,mh)
    def moment(power):
        return sum(math.comb(power,j)*q0**(power-j)*T**j
                   *gamma(j+1)*gammaincc(j+1,w_max) for j in range(power+1))
    return float(pref*kve(1,q0/T+w_max)
                 *(4*ml**2*moment(2)+0.5*moment(4))/mh**4)

def rate_MB(T: float, mi: float, mj: float, ml: float,
            coupling: float=K12, mh: float=MH, method: str="w",
            w_max: float=W_MAX, contact: bool=False) -> RateResult:
    """Per-initial-scalar scattering rate, GeV; both charges and spins.

    gamma = g_l*T/(32*pi^4) int ds lambda*sigma/sqrt(s) K1(sqrt(s)/T).
    Rate=gamma/n_i_eq, normalizing a kinetic MB shape, not assuming
    the actual scalar number density is its equilibrium density.
    """
    _temperature(T); _model(mi,mj,ml,coupling,mh); _positive(w_max)
    if method not in ("w","q-angle","sqrt-w"):
        raise ValueError("method must be w, q-angle, or sqrt-w")
    if contact and method == "q-angle":
        raise ValueError("contact diagnostic supported in w methods only")
    q0,pref=_prefactor(T,mi,mj,ml,coupling,mh)
    if coupling == 0:
        return RateResult(0.,0.,0.,method,w_max)
    def f(w):
        return (math.exp(-w)*kve(1,q0/T+w)
                *t_integral(q0+T*w,mi,mj,ml,mh,contact))
    if method == "w":
        val,err=quad(f,0.,w_max,epsabs=1e-23,epsrel=3e-11,limit=300)
        value,error=pref*val,pref*err
    elif method == "sqrt-w":
        val,err=quad(lambda u:2*u*f(u*u),0.,math.sqrt(w_max),
                     epsabs=1e-23,epsrel=3e-11,limit=300)
        value,error=pref*val,pref*err
    else:
        # Independent invariant-q formulation: ordinary K1/K2 and angle integral.
        # Scaled constant merely keeps QUAD absolute errors under control.
        normal=(G_LEPTON*coupling**2*ml**2
                /(128*math.pi**3*mi**2*kv(2,mi/T)))
        val,err=quad(lambda q:1e30*kv(1,q/T)*t_integral_angular(q,mi,mj,ml,mh),
                     q0,q0+T*w_max,epsabs=1e-19,epsrel=3e-11,limit=300)
        value,error=normal*val/1e30,normal*err/1e30
    return RateResult(float(value),float(error),
                      tail_bound(T,mi,mj,ml,coupling,mh,w_max),method,w_max)

def stationary_threshold(mi: float, mj: float, ml: float) -> float:
    """Minimum total bath-lepton energy in the initial scalar rest frame."""
    _model(mi,mj,ml,1.,MH)
    return max(ml,((mj+ml)**2-mi*mi-ml*ml)/(2*mi))

def stationary_MB_rate(T: float, mi: float, mj: float, ml: float,
                        coupling: float=K12, mh: float=MH) -> float:
    """Diagnostic with the initial scalar at rest, NOT the kinetic MB average."""
    _temperature(T); _model(mi,mj,ml,coupling,mh)
    Emin=stationary_threshold(mi,mj,ml)
    def fun(w):
        E=Emin+T*w
        q=math.sqrt(mi*mi+ml*ml+2*mi*E)
        if q <= max(mi,mj)+ml:
            return 0.
        return math.exp(-w)*t_integral(q,mi,mj,ml,mh)
    value,_=quad(fun,0.,W_MAX,epsabs=1e-23,epsrel=3e-11,limit=300)
    return (G_LEPTON*T*coupling**2*ml**2*math.exp(-Emin/T)
            /(128*math.pi**3*mi**2))*value

def FD_lower_factor(T: float, ml: float) -> float:
    """Bound for zero-chemical-potential FD bath + final Pauli blocking.

    For E,E'>=ml,
      f_FD(E)[1-f_FD(E')]/exp(-E/T)
       =1/[(1+exp(-E/T))(1+exp(-E'/T))]
       lies in [(1+exp(-ml/T))^-2,1].
    Scalar distributions remain dilute kinetic MB; no thermal dispersion changes.
    This is a bracket, NOT an explicit full FD phase-space integral.
    """
    _temperature(T); _positive(ml)
    return (1+math.exp(-ml/T))**-2

def equilibrium_ratio(T: float) -> float:
    _temperature(T)
    return (M2/M1)**2*math.exp(-(M2-M1)/T)*kve(2,M2/T)/kve(2,M1/T)

def hubble(T: float, gstar: float=60.) -> float:
    _temperature(T); _positive(gstar)
    return math.sqrt(8*math.pi**3*gstar/90)*T*T/M_PLANCK

def target_log_slope_over_H(T: float) -> float:
    """|d ln r2_eq/dt|/H for additionally assumed T proportional to a^-1."""
    q=equilibrium_ratio(T)
    x1,x2=M1/T,M2/T
    return (x2*kve(1,x2)/kve(2,x2)-x1*kve(1,x1)/kve(2,x1))/(1+q)

def net_conversion_terms(n1: float,n2: float,down: float,up: float) -> tuple[float,float]:
    if not all(math.isfinite(v) and v>=0 for v in (n1,n2,down,up)):
        raise ValueError("finite nonnegative densities and rates required")
    J=down*n2-up*n1
    return J,-J

def rates_at_temperature(T: float, gstar: float=60.) -> dict:
    q=equilibrium_ratio(T); H=hubble(T,gstar)
    out={}
    for name,ml in LEPTONS.items():
        down=rate_MB(T,M2,M1,ml)
        up=rate_MB(T,M1,M2,ml)
        d,u=down.value_GeV,up.value_GeV
        out[name]={
            "mass_GeV":ml,"down":asdict(down),"up":asdict(up),
            "down_over_H":d/H,"up_over_H":u/H,
            "reaction_density_down_GeV4":d*number_density_MB(T,M2),
            "detailed_balance_relative_residual":u/(q*d)-1,
            "FD_scattering_lower_factor":FD_lower_factor(T,ml),
            "stationary_down_over_kinetic_MB":stationary_MB_rate(T,M2,M1,ml)/d,
            "contact_over_exact":rate_MB(T,M2,M1,ml,contact=True).value_GeV/d,
            "up_stationary_threshold_total_energy_GeV":stationary_threshold(M1,M2,ml)
        }
    down=sum(v["down"]["value_GeV"] for v in out.values())
    up=sum(v["up"]["value_GeV"] for v in out.values())
    low=sum(v["down"]["value_GeV"]*v["FD_scattering_lower_factor"] for v in out.values())
    decay=GAMMA_DECAY_LEPTONIC*kve(1,M2/T)/kve(2,M2/T)
    return {
        "T_GeV":T,"assumed_gstar":gstar,"H_GeV":H,"H_per_second":H/HBAR,
        "q_equilibrium_n2_over_n1":q,"r2_equilibrium":q/(1+q),
        "leptons":out,"scattering_down_total_GeV":down,
        "scattering_up_total_GeV":up,
        "scattering_relaxation_over_H":(down+up)/H,
        "FD_scattering_relaxation_bracket_over_H":[low*(1+q)/H,(down+up)/H],
        "inherited_MB_decay_relaxation_over_H":decay*(1+q)/H,
        "MB_scatter_plus_inherited_decay_relaxation_over_H":(down+up+decay*(1+q))/H,
        "equilibrium_target_log_slope_over_H":target_log_slope_over_H(T),
        "tau_fraction_of_MB_scattering":out["tau"]["down"]["value_GeV"]/down,
        "actual_chemical_equilibrium_established":False,
        "kinetic_equilibrium_demonstrated":False,
        "relic_density_computed":False
    }

def relaxation_crossing_temperature() -> float:
    """Restricted MB scatter+prior-leptonic-decay Lambda/H=1; NOT freeze-out."""
    def f(T):
        down=sum(rate_MB(T,M2,M1,ml).value_GeV for ml in LEPTONS.values())
        decay=GAMMA_DECAY_LEPTONIC*kve(1,M2/T)/kve(2,M2/T)
        return (down+decay)*(1+equilibrium_ratio(T))/hubble(T)-1
    return brentq(f,1/3,.5,xtol=1e-12)

def complete_relic_density(*args,**kwargs):
    raise NotImplementedError("Incomplete collision inventory and kinetic/cosmological inputs")
