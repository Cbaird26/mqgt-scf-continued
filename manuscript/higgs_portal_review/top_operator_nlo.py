"""Note 43: top-operator-square NLO current and massive real heavy-flavor cuts.

Heavy-top EFT through alpha_s^3 in the O1^2 sector ONLY. Does not upgrade
O1*O2 or O2^2 to NLO, and is not complete gg, total QCD, or relic abundance.
Source: Wang/Wang 2503.22169v2 Eq. (4); Spira et al. hep-ph/9504378
Eqs. (26),(31). The finite-mass real-splitting integral is derived in Note 43.
Inherits Note-40 running/thermal kernel and Note-42 mass prescriptions.
All energies GeV; S weights GeV^2; thermal contributions GeV^-2.
"""
from __future__ import annotations
import math
from scipy.integrate import quad
from scipy.special import gamma, gammaincc, kve
import heavy_quark_thermal as h
import gluon_loop_thermal as g

NL = 3  # massless u,d,s for real gluon splitting; NOT their Yukawa currents
NF = 5  # alpha_s running includes b,c; top is integrated out
PARTS = ('LO', 'delta_veto', 'real_b', 'real_c', 'NLO_veto', 'NLO_inclusive')


def _r(r: float) -> None:
    if not math.isfinite(r) or not 0 < r < .25:
        raise ValueError('0 < m^2/Q^2 < 1/4 required; no physical threshold claim')


def real_integral_beta(r: float) -> float:
    """I(r) in beta=B*t, with a nonsingular fixed integration interval."""
    _r(r)
    B = math.sqrt(1-4*r)
    def integrand(t: float) -> float:
        b = B*t
        return B*b*b*(3-b*b)*(B*B-b*b)**3/(1-b*b)**4
    value, _ = quad(integrand, 0., 1., epsabs=1e-30, epsrel=3e-12, limit=300)
    return value


def real_integral(r: float) -> float:
    """Exact tree-level O1-induced g q qbar phase integral.

    I=integral_(4r)^1 dz/z (1-z)^3 sqrt(1-4r/z) (1+2r/z).
    A near-threshold beta-variable integration avoids closed-form cancellation.
    Domain here is mathematical. Hard-current entry points impose Q>=20 GeV.
    """
    _r(r)
    B = math.sqrt(1-4*r)
    if B < .2:
        return real_integral_beta(r)
    L = -math.log(r)+2*math.log((1+B)/2)
    return (1-18*r*r+8*r**3)*L-(3.5+r)*B**3


def real_integral_z(r: float) -> float:
    """Separate logarithmic-invariant-mass quadrature: z=4r exp(u)."""
    _r(r)
    umax = math.log(1/(4*r))
    def integrand(u: float) -> float:
        z = 4*r*math.exp(u)
        x = math.exp(-u)
        return (1-z)**3*math.sqrt(-math.expm1(-u))*(1+x/2)
    value, _ = quad(integrand, 0., umax, epsabs=1e-30, epsrel=3e-12, limit=300)
    return value


def real_minus_collinear_log(r: float) -> float:
    """Stable I(r)-ln(1/r), tending to -7/2 as r->0."""
    _r(r)
    B = math.sqrt(1-4*r)
    if B < .2:
        return real_integral_beta(r)+math.log(r)
    A = 1-18*r*r+8*r**3
    return (-18*r*r+8*r**3)*(-math.log(r))+2*A*math.log((1+B)/2)-(3.5+r)*B**3


def masses(Q: float, scale: float = 1., scheme: str = 'MSbar') -> dict[str, float]:
    g._hard(Q, scale)
    if scheme not in ('MSbar', 'pole1'):
        raise ValueError('scheme must be MSbar or pole1')
    return {q:h.running_mass(q,scale*Q) if scheme == 'MSbar'
            else g.auxiliary_pole_mass(q) for q in ('b','c')}


def coefficient_veto(Q: float, mb: float, mc: float, scale: float = 1.) -> float:
    """Coefficient of a=alpha_s/pi, after including squared Wilson matching.

    Keeps gg, ggg, and g uubar/ddbar/ssbar; excludes g bbar and g cbar.
    This is a partonic final-state convention, not a simulated detector veto.
    Massive b,c virtual loops are retained, hence the uncancelled mass logs.
    """
    g._hard(Q, scale)
    if not all(math.isfinite(m) and m > 0 for m in (mb, mc)):
        raise ValueError('positive finite masses required')
    _r((mb/Q)**2); _r((mc/Q)**2)
    lb, lc = 2*math.log(Q/mb), 2*math.log(Q/mc)
    L = 2*math.log(scale)
    return 95/4-7*NL/6-(lb+lc)/3+(33-2*NF)*L/6


def coefficient_inclusive(Q: float, mb: float, mc: float, scale: float = 1.) -> float:
    """O1-square coefficient including massive real g bbar and g cbar cuts.

    In the small-mass limit this recovers 95/4-7*NF/6+(33-2*NF)L/6.
    Does not include the direct b/c Yukawa amplitudes or their interference.
    """
    coefficient_veto(Q,mb,mc,scale)  # validates arguments
    return (95/4-7*NL/6+(33-2*NF)*math.log(scale)/3
            +sum(real_minus_collinear_log((m/Q)**2)/3 for m in (mb,mc)))


def current_components(Q: float, scale: float = 1., scheme: str = 'MSbar') -> dict[str, float]:
    m = masses(Q,scale,scheme)
    a = h.alpha_s(scale*Q)/math.pi
    S0 = a*a*Q*Q/9  # heavy-top leading current; no finite-top Born reweighting
    E = coefficient_veto(Q,m['b'],m['c'],scale)
    real = {q:S0*a*real_integral((m[q]/Q)**2)/3 for q in ('b','c')}
    return {'LO':S0,'delta_veto':S0*a*E,'real_b':real['b'],'real_c':real['c'],
            'NLO_veto':S0*(1+a*E),
            'NLO_inclusive':S0*(1+a*coefficient_inclusive(Q,m['b'],m['c'],scale))}


def current_weight(Q: float, part: str = 'NLO_inclusive', scale: float = 1.,
                   scheme: str = 'MSbar') -> float:
    if part not in PARTS:
        raise ValueError('unknown top-operator contribution')
    return current_components(Q,scale,scheme)[part]


def thermal(T: float, pair: str, part: str = 'NLO_inclusive', scale: float = 1.,
            scheme: str = 'MSbar', method: str = 'w', cut: float = h.W_CUT) -> tuple[float,float]:
    return h.thermal_from_weight(T,pair,lambda Q:current_weight(Q,part,scale,scheme),cut,method)


def current_cap() -> float:
    """Analytic absolute cap across Q=[20,80], scales=[.5,2], both schemes.

    I(r)<=ln(1/(4r))<ln(1/r) follows from beta*(1+2r/z)<=1.
    Used ONLY to bound the finite omitted interval ending at Q=80.
    """
    small = [min(h.running_mass(q,160.),g.auxiliary_pole_mass(q)) for q in ('b','c')]
    logs = sum(2*math.log(80/m) for m in small)
    Ecap = 95/4+7*NL/6+logs/3+(33-2*NF)*math.log(4)/6
    amax = h.alpha_s(10.)/math.pi
    return amax**2*80**2/9*(1+amax*(Ecap+logs/3))


def remainder_to_80(T: float, pair: str, cut: float = h.W_CUT) -> float:
    mi,mj,k = h._pair_setup(T,pair,cut)
    if mi+mj+T*cut >= 80:
        raise ValueError('window must end below Q=80')
    xi,xj = mi/T,mj/T
    a = xi+xj
    moment = sum(math.comb(4,j)*a**(4-j)*gamma(j+1)*gammaincc(j+1,cut) for j in range(5))
    return float(k*k*current_cap()*kve(1,a+cut)*moment/
        (32*math.pi*xi**2*xj**2*kve(2,xi)*kve(2,xj)*(h.MH*h.GH)**2))


def summary(T: float = .5) -> dict:
    weights = h.equilibrium_weights(T)
    variants = {}
    for label,scale,scheme in (('central',1.,'MSbar'),('mu_half',.5,'MSbar'),
                              ('mu_double',2.,'MSbar'),('pole1_diagnostic',1.,'pole1')):
        rates = {p:{c:thermal(T,p,c,scale,scheme)[0] for c in PARTS} for p in h.PAIRS}
        eff = {c:sum(weights[p]*rates[p][c] for p in h.PAIRS) for c in PARTS}
        variants[label] = {'pair_contributions_GeV_minus2':rates,
                          'conditional_effective_GeV_minus2':eff}
    # Retain amplitude grouping, not incoherent probabilities.
    grouped = {}
    for label,comps in (('O1_square',('tt',)),('O1_O2_interference',('tb','tc')),
                       ('O2_square',('bb','cc','bc'))):
        grouped[label] = sum(weights[p]*sum(g.thermal_gg(T,p,component=c)[0]
                                           for c in comps) for p in h.PAIRS)
    coherent = sum(grouped.values())
    delta = variants['central']['conditional_effective_GeV_minus2']['delta_veto']
    return {'date':'2026-09-30','temperature_GeV':T,'window_w':[0,h.W_CUT],
        'scope':'NLO O1^2 sector in the heavy-top EFT, with massive real b/c cuts. NOT complete coherent NLO gg or total QCD.',
        'equilibrium_weights_ASSUMED':weights,'variants':variants,
        'note42_LO_amplitude_groups_GeV_minus2':grouped,
        'note42_O2_square_fraction_of_LO_gg':grouped['O2_square']/coherent,
        'PARTIAL_UPGRADE_NOT_FULL_NLO':{'coherent_LO_plus_delta_top_veto_GeV_minus2':coherent+delta},
        'domain_current_cap_GeV2':current_cap(),
        'remainder_ONLY_to_Q80_GeV_minus2':{p:remainder_to_80(T,p) for p in h.PAIRS},
        'full_coherent_NLO_gg_computed':False,'NLO_O1_O2_computed':False,
        'NLO_O2_square_computed':False,'finite_top_NLO_computed':False,
        'light_quark_Yukawa_currents_computed':False,'Q_above_80_included':False,
        'chemical_equilibrium_established':False,'relic_density_computed':False,
        'Omnes_data_acquired_in_this_step':False}


if __name__ == '__main__':
    import json
    print(json.dumps(summary(),indent=2))
