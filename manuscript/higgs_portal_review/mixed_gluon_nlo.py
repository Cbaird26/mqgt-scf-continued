"""Note 44: signed top--bottom/charm O1*O2 gluonic-cut current through a_s^3.

Primary coefficient: Wang/Wang, arXiv:2503.22169v2, Eqs. (5),(6),(8),(10).
Top is integrated out at leading power. Cuts veto real b/c final states.
An explicit loop-mass re-expansion converts the source's hybrid convention
(M_loop on shell, m_Yukawa MSbar) to all-MSbar; RG supplies the scale log.
No NLO O2-square, full hadronic width, relic density, or Omnes input is supplied.
Inherits the unmodified Note-40 thermal kernel and Note-42 mass prescriptions.
"""
from __future__ import annotations
import math
from scipy.special import gamma, gammaincc, kve
import heavy_quark_thermal as h
import gluon_loop_thermal as g
import top_operator_nlo as t

ZETA3 = 1.2020569031595942854
PARTS = ('LO', 'delta_hard', 'delta_wavefunction', 'delta_matching',
         'delta_scale', 'delta_scheme', 'delta_NLO', 'NLO')


def _ratio(r: float) -> None:
    if not math.isfinite(r) or not 0 < r < .25:
        raise ValueError('require 0 < mass^2/Q^2 < 1/4; not threshold physics')


def polylog(n: int, z: float) -> float:
    """Real Li_n(z) power series on the deliberately restricted |z|<0.8."""
    if type(n) is not int or n not in (2, 3, 4):
        raise ValueError('orders 2,3,4 only')
    if not math.isfinite(z) or abs(z) >= .8:
        raise ValueError('polylog implementation requires |z|<0.8')
    terms, power = [], z
    for k in range(1, 1000):
        term = power/k**n
        terms.append(term)
        # Bound absolute remaining series by a geometric majorant.
        if abs(power*z)/((k+1)**n*(1-abs(z))) < 2e-19:
            return math.fsum(terms)
        power *= z
    raise ArithmeticError('polylog series did not converge')


def coordinates(r: float) -> tuple[float, float, float]:
    _ratio(r)
    beta = math.sqrt(1-4*r)
    u = 4*r/(1+beta)**2  # equals (z-2-sqrt(z(z-4)))/2; no cancellation
    if u >= .8:
        raise ValueError('too close to threshold for this implementation')
    return beta, u, -math.log(u)


def lo_shape(r: float) -> float:
    """H(r)=[(1-4r)(ln(u)^2-pi^2)-4]/8, source Eq. (5)."""
    beta, _, L = coordinates(r)
    return beta*beta*(L*L-math.pi**2)/8-.5


def loop_mass_derivative(r: float) -> float:
    """H+2r H': derivative of M_loop H(M_loop^2/Q^2), divided by M_loop.

    Only the loop mass is converted: the source Yukawa mass is already MSbar.
    This expression never divides by H, which has a zero inside the domain.
    """
    beta, _, L = coordinates(r)
    return (1-12*r)*(L*L-math.pi**2)/8-.5-beta*L/2


def hard_shape(r: float) -> float:
    """Source Eq. (6) braces/[12(1+u)^2]; excludes wavefunction log.

    Thus Delta2_q = [4 Q M mY/(pi v^2)] * hard_shape(r) before the
    common heavy-flavor wavefunction term. CA=3, CF=4/3, nl=3, mu=Q.
    """
    _, u, L = coordinates(r)
    l, p2, p4 = -L, math.pi**2, math.pi**4
    li2, lim2 = polylog(2,u), polylog(2,-u)
    li3, lim3 = polylog(3,u), polylog(3,-u)
    pieces = [
        (27*polylog(4,u*u)+72*polylog(4,u)
         -32*(polylog(3,u*u)-ZETA3)*l+(28*lim2+16*li2)*(l*l-p2))
            *(u-1)*(u*u+1)/(2*(u+1)),
        (13*u**4+54*u**3-72*u*u+54*u+5)*l**4/(48*(u+1)**2),
        -(23*u**4+162*u**3-216*u*u+162*u+31)*p2*l*l/(24*(u+1)**2),
        -(94*u**4-540*u**3+720*u*u-540*u-274)*p4/(480*(u+1)**2),
        -4*(u-1)**2*(lim3+8*li3-4*li2*l),
        (51*u*u-110*u+51)*(lim2*l-lim3),
        .5*(53*u*u-114*u+53)*(l*l-p2)*math.log1p(u),
        (31*u*u-70*u+31)*ZETA3,
        -(141*u**3-205*u*u-7*u+39)*l**3/(24*(u+1)),
        (335*u**3-527*u*u+67*u+29)*p2*l/(24*(u+1)),
        -(341*u**4+384*u**3-1588*u*u+384*u+341)*(p2-l*l)/(16*(u+1)**2),
        -12*(u+1)**2*math.log1p(u),
        3*(183*u**3-311*u*u+503*u-119)*l/(16*(u+1)),
        -5285*(u*u+1)/32,
        -3611*u/16,
    ]
    return math.fsum(pieces)/(12*(u+1)**2)


def small_mass_shape(r: float, spectator_log: float = 0.) -> float:
    """Independent leading-power Eq. (10), nl=3, including heavy wavefunction.

    spectator_log=0 is the printed single-heavy-flavor limit; it is not
    a massless-charm extrapolation of the physical vetoed two-flavor rate.
    """
    _ratio(r)
    if not math.isfinite(spectator_log):
        raise ValueError('finite spectator logarithm required')
    l, p2, p4 = -math.log(r), math.pi**2, math.pi**4
    ca = (l**4/192+13*l**3/288-(p2/32-349/576)*l*l
          -(13*p2/96-115/192)*l+p4/192+11*ZETA3/12-349*p2/576-5321/1152)
    cf = (-l**4/192+l**3/32-(p2/96-1/8)*l*l
          +(ZETA3+13*p2/96+3/8)*l+23*p4/960+ZETA3/4-p2/8-7/4)
    nl = (-l**3/72-5*l*l/72+(p2/24-7/48)*l-ZETA3/6+5*p2/72+233/288)
    return 3*ca+(4/3)*cf+3*nl-(l+spectator_log)*(l*l-p2-4)/24


def coefficient_parts(r: float, sum_mass_logs: float, scale: float = 1.,
                      scheme: str = 'MSbar') -> dict[str, float]:
    """Coefficients multiplying -(8/3) a^3 mass^2, not multiplicative K-factors.

    Eq. (6)'s final term acts on FULL Delta1 (b+c), and the explicit
    b<->c symmetrization doubles its -1/6 to -1/3. Eq. (10) independently
    checks the per-heavy-flavor wavefunction normalization.
    Scale log in the hybrid scheme is (2 beta0+gamma_m0)*L H=(29/6)L H.
    MSbar: convert loop mass only, +d*(H+2r H').
    pole1: convert Yukawa mass only, -d*H (auxiliary fixed-pole diagnostic).
    """
    if scheme not in ('MSbar','pole1','hybrid'):
        raise ValueError('unknown mass scheme')
    if not math.isfinite(scale) or scale <= 0 or not math.isfinite(sum_mass_logs):
        raise ValueError('finite log and positive scale required')
    H = lo_shape(r)
    d = 4/3+2*math.log(scale)-math.log(r)
    conversion = (d*loop_mass_derivative(r) if scheme == 'MSbar'
                  else -d*H if scheme == 'pole1' else 0.)
    return {'hard':hard_shape(r), 'wavefunction':-sum_mass_logs*H/3,
            'matching':11*H/4, 'scale':(29/6)*2*math.log(scale)*H,
            'scheme':conversion}


def current_components(Q: float, flavor: str, scale: float = 1.,
                       scheme: str = 'MSbar') -> dict[str, float]:
    """SIGNED O1*O2 current weights, GeV^2; no positivity clipping.

    Physical entry points allow all-MSbar or auxiliary all-pole1 only.
    Heavy-top approximation, real b/c cuts vetoed, nl=3; not full gg.
    """
    masses = t.masses(Q,scale,scheme)
    if flavor not in masses:
        raise ValueError('only b and c interference supported')
    m = masses[flavor]
    r, a = (m/Q)**2, h.alpha_s(scale*Q)/math.pi
    logs = sum(2*math.log(Q/mass) for mass in masses.values())
    coeff = coefficient_parts(r,logs,scale,scheme)
    pref = -(8/3)*a*a*m*m
    result = {'LO':pref*lo_shape(r)}
    result.update({'delta_'+key:pref*a*value for key,value in coeff.items()})
    result['delta_NLO'] = math.fsum(result[k] for k in result if k.startswith('delta_'))
    result['NLO'] = result['LO']+result['delta_NLO']
    return result


def thermal(T: float, pair: str, flavor: str, part: str = 'NLO',
            scale: float = 1., scheme: str = 'MSbar', method: str = 'w',
            cut: float = h.W_CUT) -> tuple[float,float]:
    """Finite-window, signed, common-temperature MB interference contribution."""
    if part not in PARTS:
        raise ValueError('unknown interference part')
    return h.thermal_from_weight(T,pair,
        lambda Q:current_components(Q,flavor,scale,scheme)[part],cut,method)


def current_cap() -> float:
    """Coarse analytic absolute cap for each flavor on Q=[20,80], scales [.5,2].

    Triangle inequalities on Eq. (6), bounded polylogs/logs and monotone
    inherited RG running. Not a sampled maximum; not directed-rounding.
    It bounds signed LO and NLO magnitudes, not the missing physical spectrum.
    """
    mlo = min(h.running_mass('c',160.),g.auxiliary_pole_mass('c'))
    mhi = max(h.running_mass('b',10.),g.auxiliary_pole_mass('b'))
    rlo,rhi = (mlo/80)**2,(mhi/20)**2
    _, U, _ = coordinates(rhi)
    L = -math.log(rlo);P2=math.pi**2;P4=math.pi**4
    li = U/(1-U);li_sq=U*U/(1-U*U);lp=math.log1p(U)
    poly = lambda cs:sum(abs(c)*U**k for k,c in enumerate(cs))
    # All denominators 1+u >=1, |u-1|<=1; divide entire brace by >=12.
    Bcap=((27*li_sq+72*li+32*(li_sq+ZETA3)*L+44*li*(L*L+P2))*(1+U*U)/2
          +poly([5,54,-72,54,13])*L**4/48
          +poly([31,162,-216,162,23])*P2*L*L/24
          +poly([-274,-540,720,-540,94])*P4/480
          +4*li*(9+4*L)+poly([51,-110,51])*li*(L+1)
          +poly([53,-114,53])*(L*L+P2)*lp/2+poly([31,-70,31])*ZETA3
          +poly([39,-7,-205,141])*L**3/24
          +poly([29,67,-527,335])*P2*L/24
          +poly([341,384,-1588,384,341])*(P2+L*L)/16
          +12*(1+U)**2*lp+3*poly([-119,503,-311,183])*L/16
          +5285*(U*U+1)/32+3611*U/16)/12
    Hcap=(L*L+P2)/8+.5
    derivative_cap=Hcap+rhi*(L*L+P2)+L/2
    dcap=4/3+math.log(4)+L
    Ccap=Bcap+(2*L/3+11/4+(29/6)*math.log(4))*Hcap+dcap*derivative_cap
    amax=h.alpha_s(10.)/math.pi
    return (8/3)*amax**2*mhi**2*(Hcap+amax*Ccap)


def remainder_to_80(T: float, pair: str, cut: float = h.W_CUT) -> float:
    """Absolute per-flavor remainder bound ONLY up to Q=80, not to infinity."""
    mi,mj,k=h._pair_setup(T,pair,cut)
    if mi+mj+T*cut >=80:
        raise ValueError('window endpoint must be below 80')
    xi,xj=mi/T,mj/T;a=xi+xj
    moment=sum(math.comb(4,j)*a**(4-j)*gamma(j+1)*gammaincc(j+1,cut) for j in range(5))
    return float(k*k*current_cap()*kve(1,a+cut)*moment/
        (32*math.pi*xi**2*xj**2*kve(2,xi)*kve(2,xj)*(h.MH*h.GH)**2))


def summary(T: float = .5) -> dict:
    weights=h.equilibrium_weights(T);variants={}
    for label,scale,scheme in (('central',1.,'MSbar'),('mu_half',.5,'MSbar'),
                              ('mu_double',2.,'MSbar'),('pole1_diagnostic',1.,'pole1')):
        rates={p:{q:{s:thermal(T,p,q,s,scale,scheme)[0] for s in ('LO','delta_NLO','NLO')}
                  for q in ('b','c')} for p in h.PAIRS}
        eff={q:{s:sum(weights[p]*rates[p][q][s] for p in h.PAIRS)
                for s in ('LO','delta_NLO','NLO')} for q in ('b','c')}
        eff['b+c']={s:sum(eff[q][s] for q in ('b','c')) for s in ('LO','delta_NLO','NLO')}
        variants[label]={'pair_contributions_GeV_minus2':rates,'conditional_effective':eff}
    inc=variants['central']['conditional_effective']['b+c']['delta_NLO']
    old=sum(weights[p]*g.thermal_gg(T,p)[0] for p in h.PAIRS)
    top_inc=sum(weights[p]*t.thermal(T,p,'delta_veto')[0] for p in h.PAIRS)
    checks={p:{q:{'Q_vs_w_absolute':abs(thermal(T,p,q,method='Q')[0]-thermal(T,p,q)[0]),
                  'cut100_vs90_absolute':abs(thermal(T,p,q,cut=100)[0]-thermal(T,p,q)[0])}
              for q in ('b','c')} for p in h.PAIRS}
    return {'date':'2026-09-30','temperature_GeV':T,'window_w':[0,h.W_CUT],
        'scope':'O1*O2 gluonic-cut interference through alpha_s^3, heavy-top, all-MSbar central. Signed, finite-window; NOT full coherent NLO gg.',
        'equilibrium_weights_ASSUMED':weights,'variants':variants,'numerical_checks':checks,
        'PARTIAL_UPGRADE_NOT_FULL_NLO':{'coherent_LO_note42':old,'top_NLO_veto_increment_note43':top_inc,
           'mixed_NLO_increment':inc,'sum_GeV_minus2':old+top_inc+inc},
        'per_flavor_absolute_current_cap_GeV2':current_cap(),
        'per_flavor_remainder_ONLY_to_Q80_GeV_minus2':{p:remainder_to_80(T,p) for p in h.PAIRS},
        'coherent_bc_square_NLO_computed':False,'full_coherent_NLO_gg_computed':False,
        'mixed_real_heavy_cuts_included':False,'finite_top_NLO_computed':False,
        'chemical_equilibrium_established':False,'relic_density_computed':False,
        'Q_above_80_included':False,'Omnes_data_acquired_in_this_step':False}


if __name__=='__main__':
    import json
    print(json.dumps(summary(),indent=2))
