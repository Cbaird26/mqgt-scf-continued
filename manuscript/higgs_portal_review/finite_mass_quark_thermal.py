"""Note 41: finite-mass O(alpha_s) nonsinglet b/c currents, all-MSbar.

Uses the unmodified Note-40 RG/thermal module. No new mass fits, HDECAY,
Omnes arrays, relic-density calculation, or full hadronic spectrum.
The pole formula is re-expanded in BOTH Yukawa and kinematic mass through
O(alpha_s). This is NOT a threshold-resummed or differential jet calculation.
Primary formulas: hep-ph/0503172 Eqs. (2.13)-(2.15); hep-ph/9704436
Eqs. (3),(4),(6),(7); 1911.11524 Eqs. (2.33)-(2.35),(B.8),(B.9).
All energies GeV. Numerical results integrate a finite thermal window.
"""
from __future__ import annotations
import math
from scipy.special import spence, gamma, gammaincc, kve
import heavy_quark_thermal as h


def _ratio(r: float) -> None:
    if not math.isfinite(r) or not 0. < r < .25:
        raise ValueError('mass-squared ratio must lie strictly between 0 and 1/4')


def pole_coefficient(r: float) -> float:
    """c_OS = (4/3) Delta_H(beta), coefficient of alpha_s/pi.

    r=M_pole^2/Q^2 when used in the on-shell formula. This pure
    mathematical function does not make near-threshold perturbation reliable.
    """
    _ratio(r)
    beta = math.sqrt(1-4*r)
    # Rationalized p avoids cancellation in 1-beta at small r.
    p = 4*r/(1+beta)**2
    L, lb = -math.log(p), math.log(beta)
    A = ((1+beta*beta)*(4*spence(1-p)+2*spence(1+p)
         -3*L*math.log(2/(1+beta))-2*L*lb)
         -3*beta*math.log(1/r)-4*beta*lb)
    delta = (A/beta+(3+34*beta**2-13*beta**4)*L/(16*beta**3)
             +3*(7*beta**2-1)/(8*beta**2))
    return float((4/3)*delta)


def born_log_derivative(r: float) -> float:
    """d log[m^2(1-4m^2/Q^2)^(3/2)] / d log(m)."""
    _ratio(r)
    return 2-12*r/(1-4*r)


def mass_conversion_d(r: float, scale: float = 1.) -> float:
    """M=mbar(mu)[1+a*d]+O(a^2), a=alpha_s/pi, scale=mu/Q."""
    _ratio(r)
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError('positive finite scale required')
    return 4/3+math.log(scale*scale/r)


def msbar_coefficient(r: float, scale: float = 1.) -> float:
    """All-MSbar coefficient after first-order re-expansion of the pole mass.

    Includes the derivative of Born phase space; not just Yukawa conversion.
    """
    return pole_coefficient(r)+mass_conversion_d(r,scale)*born_log_derivative(r)


def expanded_spectral_b1(r: float, scale: float = 1.) -> float:
    """Independent r^4 large-Q series of the spectral O(a) coefficient.

    From imaginary parts of hep-ph/9704436 Eq. (7), not from fitting the
    dilogarithm formula. Normalization: S/(3*mbar^2) = beta^3 + a*B1.
    Used for checks, NOT a replacement for the full-mass expression.
    """
    _ratio(r)
    mass_conversion_d(r,scale)
    lm, L = -math.log(r), -2*math.log(scale)
    return (17/3-2*L+r*(-40+24*L)+r*r*(4-12*lm-36*L)
            +r**3*(2272/27+104*lm/9-32*L)
            +r**4*(1304/9+30*lm-60*L))


def current_weight(Q: float, flavor: str, scale: float = 1.) -> float:
    """Inclusive q qbar(+g) nonsinglet S(Q), all-MSbar through O(alpha_s).

    Exact mass dependence AT THIS ORDER, with inherited two-loop running.
    Hard domain Q=[20,80], mu/Q=[1/2,2]; does not define a physical
    pair threshold at 2*mbar or extend to low-energy hadronic decays.
    """
    if not math.isfinite(Q) or not 20. <= Q <= 80.:
        raise ValueError('hard energy must be in [20,80] GeV')
    if not math.isfinite(scale) or not .5 <= scale <= 2.:
        raise ValueError('scale must be in [0.5,2]')
    mu = scale*Q
    mass = h.running_mass(flavor,mu)
    r = (mass/Q)**2
    coeff = 1+h.alpha_s(mu)/math.pi*msbar_coefficient(r,scale)
    if not math.isfinite(coeff) or coeff <= 0:
        raise ValueError('invalid or nonpositive truncated current')
    return 3*mass*mass*(1-4*r)**1.5*coeff


def thermal_quark(T: float, pair: str, flavor: str, scale: float = 1.,
                  method: str = 'w', cut: float = h.W_CUT) -> tuple[float,float]:
    """Finite-window thermal current contribution; no infinity-tail claim."""
    return h.thermal_from_weight(T,pair,
        lambda Q:current_weight(Q,flavor,scale),cut,method)


def hard_domain_current_cap() -> float:
    """Conservative absolute S cap ONLY on the inherited hard/scale domain.

    Uses analytic triangle bounds on the dilogarithm formula, not a grid max.
    Quark masses/alpha decrease along the inherited RG flow. The bound's
    displayed floating-point value is not a directed-rounding certificate.
    """
    mmax = h.running_mass('b',10.)
    mmin = h.running_mass('c',160.)
    rmin, rmax = (mmin/80)**2, (mmax/20)**2
    beta0 = math.sqrt(1-4*rmax)
    p0 = 4*rmax/(1+beta0)**2
    Lmax, lbmax = math.log(1/rmin), -math.log(beta0)
    l2max = math.log(2/(1+beta0))
    Acap = (2*(6*p0/(1-p0)+3*Lmax*l2max+2*Lmax*lbmax)
            +3*Lmax+4*lbmax)
    oscap = (4/3)*(Acap/beta0+50*Lmax/(16*beta0**3)+3/beta0**2)
    dcap = 4/3+math.log(4/rmin)
    # g(r) is positive and <=2 across this domain.
    if born_log_derivative(rmax) <= 0:
        raise ValueError('inherited domain no longer supports the cap proof')
    return 3*mmax*mmax*(1+h.alpha_s(10.)/math.pi*(oscap+2*dcap))


def within_domain_remainder_bound(T: float, pair: str, cut: float = h.W_CUT) -> float:
    """Per-flavor bound for omitted interval Q(cut)<Q<=80 ONLY.

    Integrating the bounding envelope to infinity bounds a FINITE interval;
    it does not assert that the physical/current model continues beyond 80.
    """
    mi,mj,k = h._pair_setup(T,pair,cut)
    if mi+mj+T*cut >= 80:
        raise ValueError('cut must end inside the hard domain')
    xi,xj = mi/T,mj/T
    a = xi+xj
    moment = sum(math.comb(4,j)*a**(4-j)*gamma(j+1)*gammaincc(j+1,cut)
                 for j in range(5))
    pref = k*k/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj))
    return float(pref*hard_domain_current_cap()*kve(1,a+cut)*moment/(h.MH*h.GH)**2)


def summary(T: float = .5) -> dict:
    weights = h.equilibrium_weights(T)
    variants = {}
    for label,scale in (('mu_half',.5),('central',1.),('mu_double',2.)):
        channels = {p:{q:thermal_quark(T,p,q,scale)[0] for q in ('b','c')}
                    for p in h.PAIRS}
        totals = {p:sum(channels[p].values()) for p in h.PAIRS}
        variants[label] = {'channels_GeV_minus2':channels,
            'pair_totals_GeV_minus2':totals,
            'conditional_effective_GeV_minus2':sum(weights[p]*totals[p] for p in h.PAIRS)}
    refs = {}
    for label,phase in (('note40_LP_NLO',False),('note40_phase_diagnostic',True)):
        refs[label] = sum(weights[p]*sum(h.thermal_quark(T,p,q,born_phase=phase)[0]
                          for q in ('b','c')) for p in h.PAIRS)
    checks = {p:{q:{'Q_vs_w_relative':abs(thermal_quark(T,p,q,method='Q')[0]/
                         thermal_quark(T,p,q)[0]-1),
                  'cut100_vs90_relative':abs(thermal_quark(T,p,q,cut=100)[0]/
                         thermal_quark(T,p,q)[0]-1)} for q in ('b','c')} for p in h.PAIRS}
    return {'temperature_GeV':T,'window_w':[0,h.W_CUT],
            'scope':'Finite-mass O(alpha_s) b/c nonsinglet currents, all-MSbar re-expansion; NOT full QCD or relic density.',
            'equilibrium_weights_ASSUMED':weights,'variants':variants,
            'historical_comparators':refs,'numerical_checks':checks,
            'hard_domain_current_cap_GeV2':hard_domain_current_cap(),
            'per_flavor_remainder_to_Q80_bounds_GeV_minus2':{
                p:within_domain_remainder_bound(T,p) for p in h.PAIRS},
            'Q_above_80_included':False,'chemical_equilibrium_established':False,
            'Omnes_data_acquired_in_this_step':False,'relic_density_computed':False}


if __name__ == '__main__':
    import json
    print(json.dumps(summary(),indent=2))
