"""Note 50: independent gluon-antenna normalization and subtraction audit.

Primary matrix elements: Gehrmann-De Ridder, Gehrmann, Glover,
hep-ph/0502110 Eqs. (3.2),(3.3),(4.3),(4.9). Their integrated results
(4.6),(4.11),(4.14) are comparison targets, NOT integration inputs.
We integrate the d=4-2*epsilon tree expressions by Dirichlet moments.
Conventions: real/virtual Laurent coefficients multiply alpha_s/(2*pi),
T0 and a common (Q^2)^(-epsilon). QCD numerical currents use GeV^2.
This is not a full independent massive-loop amplitude or relic calculation.
"""
from __future__ import annotations
import math
from functools import lru_cache
import numpy as np
import sympy as sp
from scipy.special import roots_legendre, gamma, gammaln

E = sp.Symbol('epsilon')
R = sp.Rational


def _gamma_ratio(n: int, c: int = 1):
    """Gamma(n-c*e)/Gamma(1-c*e), for nonnegative integer n."""
    if type(n) is not int or n < 0:
        raise ValueError('nonnegative integer Gamma shift required')
    return -1/(c*E) if n == 0 else sp.prod(k-c*E for k in range(1,n))


def dirichlet_rational(a: int, b: int, c: int):
    """Dirichlet moment with common Gamma(1-e)^3/Gamma(1-3e) removed.

    It integrates x^(a-1-e) y^(b-1-e) z^(c-1-e) on x+y+z=1.
    Initially convergent for negative epsilon for the moments used here;
    its meromorphic continuation fixes the Laurent coefficients.
    """
    if any(type(v) is not int or v<0 for v in (a,b,c)) or a+b+c == 0:
        raise ValueError('nonnegative integer shifts and positive sum required')
    return sp.cancel(_gamma_ratio(a)*_gamma_ratio(b)*_gamma_ratio(c)
                     /_gamma_ratio(a+b+c,3))


@lru_cache(maxsize=2)
def integrated_rational(channel: str):
    """Integrate the d-dimensional matrix element by monomial moments."""
    D = dirichlet_rational
    if channel == 'ggg':
        return sp.factor(R(2,3)*(3*D(2,0,0)+3*D(2,2,0)
                       +(6-2/(1-E))*D(1,1,1)))
    if channel == 'gqq':
        return sp.factor(2*D(3,1,0)-2*E/(1-E)*D(2,2,0))
    raise ValueError('channel must be ggg or gqq')


@lru_cache(maxsize=4)
def laurent_coefficients(channel: str, max_power: int = 2):
    """Exact coefficients; no finite published integral is substituted."""
    if type(max_power) is not int or not 0 <= max_power <= 2:
        raise ValueError('max_power must be 0, 1, or 2')
    # MS-bar phase-space factor times the common Dirichlet Gamma ratio:
    # H(e)=exp(gamma_E*e) Gamma(1-e)^2 / Gamma(1-3e).
    n = max_power+2
    logH = sum((2-3**j)*sp.zeta(j)*E**j/j for j in range(2,n+1))
    H = sp.series(sp.exp(logH),E,0,n+1).removeO()
    rat = sp.series(integrated_rational(channel),E,0,max_power+1).removeO()
    expanded = sp.expand(rat*H)
    return {p:sp.simplify(expanded.coeff(E,p)) for p in range(-2,max_power+1)}


def source_virtual_coefficients(N=None,nf=None):
    """Published renormalized EFT virtual term, Eq. (3.3), not rederived.

    Does not include the heavy-top Wilson-coefficient matching correction.
    """
    N=sp.Symbol('N') if N is None else sp.sympify(N)
    nf=sp.Symbol('nf') if nf is None else sp.sympify(nf)
    return {-2:-2*N,-1:-R(11,3)*N+R(2,3)*nf,
             0:R(7,6)*N*sp.pi**2}


def symbolic_audit():
    x,y,t,z,NN,nf,L,lb,lc = sp.symbols('x y t z N nf L ell_b ell_c')
    zz=1-x-y
    P=1+x**4+y**4+zz**4
    red=(x/(y*zz)+y/(x*zz)+zz/(x*y)+x*y/zz+x*zz/y+y*zz/x+4)/3
    gg=laurent_coefficients('ggg');qq=laurent_coefficients('gqq')
    virt=source_virtual_coefficients(NN,nf)
    total={p:sp.simplify(NN*gg[p]+nf*qq[p]+virt[p]) for p in (-2,-1,0)}
    U3=R(73,4)-R(7,6)*3+R(9,2)*L
    U5=sp.expand(U3-R(1,3)*(lb+lc+2*L))
    naive=2*dirichlet_rational(3,1,0)
    checks={
      'four_dimensional_ggg_shape':sp.factor(red-P/(6*x*y*zz)),
      'light_pair_angular_normalization':sp.integrate(t*t+(1-t)**2,(t,0,1))-R(2,3),
      'double_pole_cancellation':total[-2],
      'single_pole_cancellation':total[-1],
      'integrated_finite_coefficient':sp.simplify(total[0]-(R(73,6)*NN-R(7,3)*nf)),
      'SU3_universal_coefficient':sp.simplify(total[0].subs(NN,3)/2-(R(73,4)-R(7,6)*nf)),
      'heavy_top_with_Wilson_matching':sp.simplify(total[0].subs(NN,3)/2+R(11,2)-(R(95,4)-R(7,6)*nf)),
      'five_flavor_veto_translation':sp.expand(U5-(R(73,4)-R(7,6)*3-(lb+lc)/3+R(23,6)*L)),
      'evanescent_light_pair_finite_shift':sp.limit(integrated_rational('gqq')-naive,E,0)-R(1,3),
    }
    if any(v.has(sp.Float) for v in checks.values()):
        raise ArithmeticError('floating coefficients entered exact audit')
    return {'identities':{k:str(sp.simplify(v)) for k,v in checks.items()},
            'all_exact_zero':all(sp.simplify(v)==0 for v in checks.values()),
            'ggg_rational':str(integrated_rational('ggg')),
            'gqq_rational':str(integrated_rational('gqq')),
            'ggg_laurent':{str(p):str(v) for p,v in gg.items()},
            'gqq_laurent':{str(p):str(v) for p,v in qq.items()},
            'finite_in_alpha_over_pi':str(sp.simplify(total[0]/2)),
            'U_veto_in_alpha5':str(U5)}


def real_density(x, y, epsilon: float, channel: str):
    """d-dimensional source density in alpha_s/(2pi)*N or *nf units.

    Source spin sums divided by the d-dimensional Born normalization.
    The phase-space weight (x*y*z)^(-epsilon) is not included here.
    """
    x,y=np.broadcast_arrays(np.asarray(x,float),np.asarray(y,float));z=1-x-y
    if not math.isfinite(epsilon) or epsilon>=1 or np.any((x<=0)|(y<=0)|(z<=0)):
        raise ValueError('interior triangle and finite epsilon<1 required')
    if channel=='ggg':
        return (2/3)*(x/(y*z)+y/(x*z)+z/(x*y)+x*y/z+x*z/y+y*z/x+6-2/(1-epsilon))
    if channel=='gqq':
        return (x+y)**2/z-2*x*y/((1-epsilon)*z)
    raise ValueError('channel must be ggg or gqq')


def direct_regulated_integral(epsilon: float, channel: str, n: int = 32):
    """Independent two-dimensional Gaussian check at epsilon<=-1.

    Negative regulator values make these integrals nonsingular. This is
    a mathematical continuation check, not a physical cutoff prescription.
    """
    if not math.isfinite(epsilon) or not -3<=epsilon<=-1:
        raise ValueError('audited quadrature regulator interval is [-3,-1]')
    if type(n) is not int or not 8<=n<=128:raise ValueError('8..128 nodes required')
    u,w=roots_legendre(n);u=(u+1)/2;w=w/2
    x=u[:,None];y=(1-x)*u[None,:];z=1-x-y
    kernel=real_density(x,y,epsilon,channel)*(x*y*z)**(-epsilon)*(1-x)
    factor=math.exp(float(sp.EulerGamma)*epsilon)/gamma(1-epsilon)
    return float(factor*np.sum(w[:,None]*w[None,:]*kernel))


def gamma_regulated_integral(epsilon: float, channel: str):
    """Gamma-function evaluation of the analytic Dirichlet result."""
    if not math.isfinite(epsilon) or not -3<=epsilon<0:
        raise ValueError('negative regulator in [-3,0) required')
    H=math.exp(float(sp.EulerGamma)*epsilon+2*gammaln(1-epsilon)-gammaln(1-3*epsilon))
    return H*float(integrated_rational(channel).subs(E,epsilon))


def universal_veto(Q: float, mu: float, mb: float, mc: float):
    """Universal coefficient via 3->5 flavor coupling re-expression.

    Starts with the independently integrated three-massless-flavor antenna
    constant and a3 running logarithm. At one loop a3=a5[1-a5/6 sum ln(mu2/m2)].
    This is spectator/coupling scheme bookkeeping. It does not replace the
    hard b/c-loop form factors by a heavy-mass effective approximation.
    """
    if not all(math.isfinite(v) and v>0 for v in (Q,mu,mb,mc)):
        raise ValueError('positive finite energies and masses required')
    L=2*math.log(mu/Q)
    u3=73/4-7*3/6+(9/2)*L
    spectator=-(math.log(mu*mu/(mb*mb))+math.log(mu*mu/(mc*mc)))/3
    return u3+spectator


def thermal_universal(T=.5,pair='11',scale=1.,method='w'):
    """Finite-window verification of Note48's universal term only.

    Inherits historical alpha_s, running masses, Born form factors and the
    thermal kernel. Does NOT call Note48's universal function or its integral.
    """
    import heavy_quark_thermal as h
    import gluon_loop_thermal as g
    def weight(Q):
        mu=scale*Q;mb=h.running_mass('b',mu);mc=h.running_mass('c',mu)
        B=abs(g.form_factor((Q/(2*mb))**2)+g.form_factor((Q/(2*mc))**2))**2
        return (h.alpha_s(mu)/math.pi)**3*Q*Q/9*B*universal_veto(Q,mu,mb,mc)
    return h.thermal_from_weight(T,pair,weight,h.W_CUT,method)[0]


def complete_massive_NLO_rate(*args,**kwargs):
    raise NotImplementedError('This audit supplies normalization and universal subtraction checks, not a new full massive real-amplitude calculation.')


def results():
    import heavy_quark_thermal as h
    numerical=[]
    for e in (-1.,-2.,-3.):
        for channel in ('ggg','gqq'):
            q=direct_regulated_integral(e,channel);a=gamma_regulated_integral(e,channel)
            numerical.append({'epsilon':e,'channel':channel,'two_dimensional_integral':q,
                              'gamma_integral':a,'relative_difference':abs(q/a-1)})
    weights=h.equilibrium_weights(.5)
    thermal={}
    for scale in (.5,1.,2.):
        rates={p:thermal_universal(.5,p,scale) for p in h.PAIRS}
        thermal[str(scale)]={'pair_universal_GeV_minus2':rates,
                'conditional_effective_GeV_minus2':sum(weights[p]*rates[p] for p in rates)}
    cross={p:abs(thermal_universal(.5,p,1.,'Q')/thermal[str(1.)]['pair_universal_GeV_minus2'][p]-1) for p in h.PAIRS}
    return {'date':'2026-10-11','scope':'Independent antenna normalization and universal subtraction; not independent full massive QCD',
            'symbolic':symbolic_audit(),'regulated_numerical_checks':numerical,
            'temperature_GeV_ASSUMED':.5,'weights_ASSUMED':weights,
            'thermal_universal':thermal,'Q_vs_w_relative':cross,
            'baseline_candidate_recomputed':False,'complete_massive_real_amplitudes_rederived':False,
            'abundance_calculated':False,'new_Omnes_data':False}

if __name__=='__main__':
    import json
    print(json.dumps(results(),indent=2,sort_keys=True))
