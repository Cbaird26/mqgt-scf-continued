"""Note 45: RG-fixed logs and mass-scheme matching for coherent b/c-square gg.

Calculates the LO current, the REQUIRED explicit NLO scale logarithm, and
finite mass-conversion terms. The finite real-plus-virtual NLO hard current
is NOT supplied, fitted, bounded, or replaced by a universal K-factor.
All masses/couplings and the finite-window thermal kernel are inherited.
"""
from __future__ import annotations
import math
from typing import Callable, Mapping
import heavy_quark_thermal as h
import gluon_loop_thermal as g

BETA0 = 23.0 / 12.0  # a=alpha_s/pi, derivative w.r.t. ln(mu^2), nf=5
GAMMA0 = 1.0
COMPONENTS = ('bb', 'cc', 'bc', 'coherent')


def _couplings(kb: float, kc: float) -> None:
    if not all(math.isfinite(v) for v in (kb, kc)):
        raise ValueError('finite real Yukawa multipliers required')


def form_and_mass_derivative(r: float) -> tuple[complex, complex]:
    """Return F(r) and D F=m*dF/dm (equal Yukawa and loop masses).

    Exact above-threshold one-loop formula, r=m^2/Q^2 in (0,1/4).
    The derivative includes BOTH Yukawa and loop dependence.
    No finite-difference differentiation or division by an amplitude is used.
    """
    if not math.isfinite(r) or not 0 < r < .25:
        raise ValueError('0<r<1/4 required; threshold resummation not provided')
    beta = math.sqrt(1 - 4*r)
    ell = -math.log(4*r/(1+beta)**2)
    z = complex(ell, -math.pi)
    f = -.25*z*z
    F = 6*r*(1+(1-4*r)*f)
    DF = 12*r*(1+(1-8*r)*f+beta*z/2)
    return F, DF


def born_data(rb: float, rc: float, kb: float = 1., kc: float = 1.) -> dict:
    """Dimensionless B=|kb*Fb+kc*Fc|^2 and its two log-mass derivatives.

    bc is the entire signed interference 2 Re(kb*Fb (kc*Fc)*).
    Yukawa multipliers are independent probes, NOT changes to mass inputs.
    """
    _couplings(kb, kc)
    Fb, Db = form_and_mass_derivative(rb)
    Fc, Dc = form_and_mass_derivative(rc)
    Fb, Db, Fc, Dc = kb*Fb, kb*Db, kc*Fc, kc*Dc
    values = {'bb':abs(Fb)**2, 'cc':abs(Fc)**2,
              'bc':2*(Fb*Fc.conjugate()).real}
    db = {'bb':2*(Db*Fb.conjugate()).real, 'cc':0.,
          'bc':2*(Db*Fc.conjugate()).real}
    dc = {'bb':0., 'cc':2*(Dc*Fc.conjugate()).real,
          'bc':2*(Fb*Dc.conjugate()).real}
    # Direct coherent expression retains positivity and cancellation accurately.
    A = Fb+Fc
    values['coherent'] = abs(A)**2
    db['coherent'] = 2*(Db*A.conjugate()).real
    dc['coherent'] = 2*(Dc*A.conjugate()).real
    return {'B':values, 'D_b':db, 'D_c':dc}


def required_log_coefficient(rb: float, rc: float, kb: float = 1.,
                             kc: float = 1.) -> dict[str, float]:
    """K=2 beta0 B + gamma0*(D_b+D_c) B in the all-MSbar scheme.

    S=Q^2/9 * {a^2 B + a^3 [C_fin(rb,rc)+L K]} + O(a^4),
    L=ln(mu^2/Q^2). C_fin is unknown. This fixes logs, not that function.
    """
    d = born_data(rb, rc, kb, kc)
    return {c:2*BETA0*d['B'][c]+GAMMA0*(d['D_b'][c]+d['D_c'][c])
            for c in COMPONENTS}


def scheme_shift(rb: float, rc: float, scale: float = 1.,
                 kb: float = 1., kc: float = 1.) -> dict[str, float]:
    """Additive OS->all-MSbar NLO coefficient shift sum d_q D_q B.

    M_q=mbar_q(mu)*(1+a*d_q)+O(a^2), d_q=4/3+ln(mu^2/mbar_q^2).
    Does NOT calculate the unknown OS or MSbar finite hard coefficient.
    """
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError('positive finite scale required')
    d = born_data(rb, rc, kb, kc)
    d_b = 4/3+2*math.log(scale)-math.log(rb)
    d_c = 4/3+2*math.log(scale)-math.log(rc)
    return {c:d_b*d['D_b'][c]+d_c*d['D_c'][c] for c in COMPONENTS}


def current_terms(Q: float, scale: float = 1., kb: float = 1.,
                  kc: float = 1.) -> dict:
    """LO, coefficient of L at NLO, and finite OS->MSbar conversion, GeV^2.

    The conversion is a convention change, NOT a missing physical rate.
    The log slope is evaluated at masses/alpha_s(mu); finite C is unknown.
    """
    g._hard(Q, scale)
    _couplings(kb, kc)
    mb, mc = (h.running_mass(q,scale*Q) for q in ('b', 'c'))
    rb, rc = (mb/Q)**2, (mc/Q)**2
    a = h.alpha_s(scale*Q)/math.pi
    d = born_data(rb, rc, kb, kc)
    logs = required_log_coefficient(rb, rc, kb, kc)
    finite_shift = scheme_shift(rb, rc, 1., kb, kc)
    pref = Q*Q/9
    return {c:{'LO':pref*a*a*d['B'][c],
               'required_NLO_log_slope':pref*a**3*logs[c],
               'OS_to_MSbar_finite_shift':pref*a**3*finite_shift[c]}
            for c in COMPONENTS}


def thermal(T: float, pair: str, part: str = 'LO',
            component: str = 'coherent', scale: float = 1.,
            kb: float = 1., kc: float = 1., method: str = 'w',
            cut: float = h.W_CUT) -> tuple[float, float]:
    """Finite-window thermal integrals of known terms, NOT full NLO rates."""
    if part not in ('LO', 'required_NLO_log_slope', 'OS_to_MSbar_finite_shift'):
        raise ValueError('only known terms supported; finite NLO hard term is missing')
    if component not in COMPONENTS:
        raise ValueError('unknown b/c-square component')
    return h.thermal_from_weight(T, pair,
        lambda Q:current_terms(Q,scale,kb,kc)[component][part], cut, method)


def finite_nlo_current(Q: float, finite_coeff: Callable[[float,float],float] | None,
                       scale: float = 1.) -> float:
    """Evaluate ONLY when an independently supplied finite coefficient exists.

    Callback returns dimensionless C_fin(rb,rc) in the declared all-MSbar,
    real-b/c-vetoed convention. This contract does not certify the callback.
    """
    if finite_coeff is None:
        raise ValueError('finite real-plus-virtual C_fin is absent; NLO is not closed')
    g._hard(Q, scale)
    rb, rc = [(h.running_mass(q,scale*Q)/Q)**2 for q in ('b','c')]
    C = float(finite_coeff(rb,rc))
    if not math.isfinite(C):
        raise ValueError('finite hard coefficient required')
    terms=current_terms(Q,scale)['coherent']
    a=h.alpha_s(scale*Q)/math.pi
    return terms['LO']+2*math.log(scale)*terms['required_NLO_log_slope']+Q*Q/9*a**3*C


def polarize(values: Mapping[str, float]) -> dict[str, float]:
    """Recover bb,cc,full bc interference from independently supplied rates.

    All calls MUST hold masses, alpha_s, active flavors, cuts and spectators
    fixed, and vary ONLY real Yukawa multipliers with top Yukawa set to zero.
    Keys: '10','01','11','1-1','00'. Works also on signed NLO increments.
    Synthetic-fixture tests are not an external NLO computation.
    """
    if set(values) != {'10','01','11','1-1','00'}:
        raise ValueError('five fixed-physics probe values required')
    if not all(math.isfinite(v) for v in values.values()):
        raise ValueError('finite probe values required')
    scale = max(abs(v) for v in values.values())
    tol=5e-11*max(scale,1e-300)
    if abs(values['00'])>tol:
        raise ValueError('zero-Yukawa baseline is nonzero: unwanted sectors remain')
    bc=values['11']-values['10']-values['01']
    cross_pm=.5*(values['11']-values['1-1'])
    if abs(bc-cross_pm)>tol:
        raise ValueError('probe data are not a consistent homogeneous quadratic form')
    return {'bb':values['10'],'cc':values['01'],'bc':bc}


def summary(T: float = .5) -> dict:
    weights=h.equilibrium_weights(T)
    names=('LO','required_NLO_log_slope','OS_to_MSbar_finite_shift')
    pairs={p:{c:{k:thermal(T,p,k,c)[0] for k in names} for c in COMPONENTS}
           for p in h.PAIRS}
    eff={c:{k:sum(weights[p]*pairs[p][c][k] for p in h.PAIRS) for k in names}
         for c in COMPONENTS}
    checks={p:{c:{k:abs(thermal(T,p,k,c,method='Q')[0]-pairs[p][c][k])
                  for k in names} for c in COMPONENTS} for p in h.PAIRS}
    return {'date':'2026-10-01','temperature_GeV':T,'window_w':[0,h.W_CUT],
        'scope':'RG-required NLO log and mass-scheme transformation for coherent b/c-square only; finite NLO hard current NOT calculated.',
        'pair_integrals_GeV_minus2':pairs,'equilibrium_weights_ASSUMED':weights,
        'conditional_effective':eff,'two_variable_absolute_differences':checks,
        'log_slope_to_LO_ratio':eff['coherent']['required_NLO_log_slope']/eff['coherent']['LO'],
        'finite_shift_to_LO_ratio':eff['coherent']['OS_to_MSbar_finite_shift']/eff['coherent']['LO'],
        'finite_NLO_hard_current_computed':False,'full_coherent_NLO_gg_computed':False,
        'external_NLO_probe_data_obtained':False,'chemical_equilibrium_established':False,
        'Omnes_data_acquired':False,'relic_density_computed':False,'Q_above_80_included':False}


if __name__=='__main__':
    import json
    print(json.dumps(summary(),indent=2))
