"""Note 42: coherent t/b/c one-loop gg thermal contribution (LO alpha_s^2).

Uses unmodified Note-40 running and thermal integration, Note-41 b/c currents.
Full mass dependence at the leading nonzero gg order; NOT NLO gg, total QCD,
relic abundance, detector response, or low-energy s2 decay. Energies in GeV.
Primary formulas: Djouadi hep-ph/0503172 (2.46)-(2.48),(2.58);
Wang/Wang 2503.22169v2 (4),(5),(7),(12) provide separate LO checks.
"""
from __future__ import annotations
import math
from itertools import combinations
from scipy.special import gamma, gammaincc, kve
import heavy_quark_thermal as h
import finite_mass_quark_thermal as fm

# Additional fixed historical input, Wang/Wang (2025) Eq. (12), not latest fit.
MT = 172.69
FLAVORS = ('t', 'b', 'c')
COMPONENTS = ('tt', 'bb', 'cc', 'tb', 'tc', 'bc')


def form_factor(tau: float) -> complex:
    """F=3*A_1/2/4, tau=Q^2/(4m_loop^2); F(0)=1.

    For mass/Yukawa schemes that differ, multiply F by m_Yukawa/m_loop.
    This function itself uses equal loop and Yukawa masses, no color factor.
    """
    if not math.isfinite(tau) or tau < 0:
        raise ValueError('finite nonnegative tau required')
    if tau < 1e-3:
        # Heavy-mass Taylor series through tau^4; error O(tau^5).
        return complex(1+tau*(7/30+tau*(2/21+tau*(26/525+tau*512/17325))))
    if tau <= 1:
        f = complex(math.asin(math.sqrt(tau))**2)
    else:
        beta = math.sqrt(1-1/tau)
        # Rationalized log avoids subtracting 1-beta for large tau.
        L = math.log(tau)+2*math.log1p(beta)
        f = -.25*complex(L, -math.pi)**2
    return 1.5/tau*(1+(1-1/tau)*f)


def _hard(Q: float, scale: float) -> None:
    if not math.isfinite(Q) or not 20 <= Q <= 80:
        raise ValueError('Q must lie in [20,80] GeV; no low-energy extrapolation')
    if not math.isfinite(scale) or not .5 <= scale <= 2:
        raise ValueError('scale mu/Q must lie in [0.5,2]')


def auxiliary_pole_mass(flavor: str) -> float:
    """One-loop conversion at frozen input anchor; a scheme diagnostic only.

    Not a precision pole-mass determination. No higher-order matching.
    """
    if flavor not in ('b', 'c'):
        raise ValueError('only b,c supported')
    mu, mass = (10., h.MB_AT_10) if flavor == 'b' else (3., h.MC_AT_3)
    return mass*(1+h.alpha_s(mu)/math.pi*(4/3+2*math.log(mu/mass)))


def loop_amplitudes(Q: float, scale: float = 1., scheme: str = 'MSbar',
                    heavy_top: bool = False) -> dict[str, complex]:
    """Top uses fixed MT; b,c use same mass in Yukawa and propagators.

    MSbar uses inherited mbar(mu); pole1 uses auxiliary one-loop pole estimates.
    Their difference starts beyond LO gg formally, but is not an error interval.
    """
    _hard(Q, scale)
    if scheme not in ('MSbar', 'pole1'):
        raise ValueError('scheme must be MSbar or pole1')
    masses = {q: h.running_mass(q,scale*Q) if scheme == 'MSbar'
              else auxiliary_pole_mass(q) for q in ('b','c')}
    amps = {'t': 1.+0j if heavy_top else form_factor((Q/(2*MT))**2)}
    amps.update({q: form_factor((Q/(2*m))**2) for q,m in masses.items()})
    return amps


def components(Q: float, scale: float = 1., scheme: str = 'MSbar',
               heavy_top: bool = False) -> dict[str, float]:
    """S_gg=alpha_s^2 Q^2/(9*pi^2) |F_t+F_b+F_c|^2, GeV^2.

    Signed off-diagonal pieces are interference, NOT distinct partial widths.
    The published width already includes final gluon color/pair counting.
    """
    amps = loop_amplitudes(Q,scale,scheme,heavy_top)
    pref = h.alpha_s(scale*Q)**2*Q*Q/(9*math.pi**2)
    result = {q+q: pref*abs(a)**2 for q,a in amps.items()}
    result.update({q+r: pref*2*(amps[q]*amps[r].conjugate()).real
                   for q,r in combinations(FLAVORS,2)})
    return result


def current_weight(Q: float, scale: float = 1., scheme: str = 'MSbar',
                   component: str = 'coherent') -> float:
    amps = loop_amplitudes(Q,scale,scheme)
    pref = h.alpha_s(scale*Q)**2*Q*Q/(9*math.pi**2)
    if component == 'coherent':
        return pref*abs(sum(amps.values()))**2
    if component == 'incoherent':
        return pref*sum(abs(a)**2 for a in amps.values())
    if component == 'heavy_top_only':
        return pref
    if component == 'heavy_top_coherent':
        return pref*abs(1+amps['b']+amps['c'])**2
    if component not in COMPONENTS:
        raise ValueError('unknown gluon-current component')
    return components(Q,scale,scheme)[component]


def unit_higgs_width(Q: float, scale: float = 1., scheme: str = 'MSbar') -> float:
    """Gamma(h*(Q)->gg); auxiliary unit Higgs current, not a new on-shell Higgs."""
    return Q*current_weight(Q,scale,scheme)/(8*math.pi*h.V**2)


def thermal_gg(T: float, pair: str, scale: float = 1., scheme: str = 'MSbar',
               component: str = 'coherent', method: str = 'w',
               cut: float = h.W_CUT) -> tuple[float,float]:
    """Finite-window MB contribution in GeV^-2, with quadrature error estimate."""
    return h.thermal_from_weight(T,pair,
        lambda Q: current_weight(Q,scale,scheme,component),cut,method)


def domain_cap() -> float:
    """Analytic absolute cap on coherent/incoherent current ONLY for Q<=80.

    Top: positive Feynman parameter integrand gives F<=3/2 for tau<=1.
    b,c: |F| <= 3/(2*tau_min)*(1+(log(4*tau_max)^2+pi^2)/4).
    Covers MSbar and auxiliary pole1 over declared scales; not a sampled max.
    """
    amp_cap = 1.5
    for q in ('b','c'):
        lo = min(h.running_mass(q,160.), auxiliary_pole_mass(q))
        hi = max(h.running_mass(q,10.), auxiliary_pole_mass(q))
        tmin, tmax = (20/(2*hi))**2, (80/(2*lo))**2
        if tmin <= 1 or 80 >= 2*MT:
            raise ValueError('masses no longer support this cap proof')
        amp_cap += 1.5/tmin*(1+(math.log(4*tmax)**2+math.pi**2)/4)
    return h.alpha_s(10.)**2*80**2/(9*math.pi**2)*amp_cap**2


def remainder_to_80(T: float, pair: str, cut: float = h.W_CUT) -> float:
    """Bounds only Q(cut)<Q<=80, not unknown Q>80 or missing channels."""
    mi,mj,k = h._pair_setup(T,pair,cut)
    if mi+mj+T*cut >= 80:
        raise ValueError('window must end below 80')
    xi,xj = mi/T,mj/T
    a = xi+xj
    moment = sum(math.comb(4,j)*a**(4-j)*gamma(j+1)*gammaincc(j+1,cut)
                 for j in range(5))
    return float(k*k*domain_cap()*kve(1,a+cut)*moment/
        (32*math.pi*xi**2*xj**2*kve(2,xi)*kve(2,xj)*(h.MH*h.GH)**2))


def summary(T: float = .5) -> dict:
    weights = h.equilibrium_weights(T)
    variants = {}
    for label,scale,scheme,component in (
        ('central',1.,'MSbar','coherent'),('mu_half',.5,'MSbar','coherent'),
        ('mu_double',2.,'MSbar','coherent'),('pole1_diagnostic',1.,'pole1','coherent'),
        ('incoherent_diagnostic',1.,'MSbar','incoherent'),
        ('top_only',1.,'MSbar','tt'),('heavy_top_only',1.,'MSbar','heavy_top_only'),
        ('heavy_top_coherent',1.,'MSbar','heavy_top_coherent')):
        rates = {p:thermal_gg(T,p,scale,scheme,component)[0] for p in h.PAIRS}
        variants[label] = {'pair_rates_GeV_minus2':rates,
            'conditional_effective_GeV_minus2':sum(weights[p]*rates[p] for p in h.PAIRS)}
    decomposition = {p:{c:thermal_gg(T,p,component=c)[0] for c in COMPONENTS} for p in h.PAIRS}
    eff_components = {c:sum(weights[p]*decomposition[p][c] for p in h.PAIRS) for c in COMPONENTS}
    bc = sum(weights[p]*sum(fm.thermal_quark(T,p,q)[0] for q in ('b','c')) for p in h.PAIRS)
    numerical_checks = {p:{'Q_vs_w_relative':abs(thermal_gg(T,p,method='Q')[0]/thermal_gg(T,p)[0]-1),
        'cut100_vs90_relative':abs(thermal_gg(T,p,cut=100)[0]/thermal_gg(T,p)[0]-1)} for p in h.PAIRS}
    return {'temperature_GeV':T,'top_mass_input_GeV':MT,
        'auxiliary_pole1_masses_GeV':{q:auxiliary_pole_mass(q) for q in ('b','c')},
        'equilibrium_weights_ASSUMED':weights,'variants':variants,
        'signed_loop_components_GeV_minus2':decomposition,
        'conditional_effective_signed_components_GeV_minus2':eff_components,
        'inherited_note41_bc_GeV_minus2':bc,'numerical_checks':numerical_checks,
        'current_cap_GeV2':domain_cap(),
        'remainder_only_to_Q80_GeV_minus2':{p:remainder_to_80(T,p) for p in h.PAIRS},
        'scope':'LO alpha_s^2 gg from coherent t/b/c loops only; finite window; not total QCD.',
        'NLO_gg_computed':False,'light_quark_loops_included':False,
        'Q_above_80_included':False,'chemical_equilibrium_established':False,
        'relic_density_computed':False,'Omnes_data_acquired_in_this_step':False}


if __name__ == '__main__':
    import json
    print(json.dumps(summary(),indent=2))
