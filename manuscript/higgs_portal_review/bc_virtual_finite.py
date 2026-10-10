"""Note 46: coherent b/c finite virtual coefficient from hep-ph/0509189.

Implements Harlander/Kant (3.5)-(3.7), with their all-MSbar mass convention.
This is the mass-dependent c_H building block, NOT the full decay NLO
coefficient, NOT a bare virtual probability, and NOT a relic abundance.
The source's universal production pi^2 term, integrated real subtraction,
heavy-flavor-veto completion, and three-gluon remainder are not supplied.
All hard energies GeV; thermal values GeV^-2; inherited parameters unchanged.
"""
from __future__ import annotations
import cmath
import math
from functools import lru_cache
import heavy_quark_thermal as h
import gluon_loop_thermal as g
import coherent_bc_rg as rg

COMPONENTS = ('bb', 'cc', 'bc', 'coherent')
SERIES_TERMS = 48


def _theta_domain(theta: complex) -> complex:
    z=complex(theta)
    if not all(math.isfinite(t) for t in (z.real,z.imag)) or not 0<abs(z)<=0.1:
        raise ValueError('numerical series requires 0<abs(theta)<=0.1')
    return z


def li_series(order: int, z: complex, terms: int = SERIES_TERMS) -> complex:
    """Convergent defining polylog series on |z|<=.1 (not a mass expansion)."""
    z=complex(z)
    if type(order) is not int or order not in (2,3,4):
        raise ValueError('polylogarithm order must be 2,3,4')
    if type(terms) is not int or terms<16 or terms>256:
        raise ValueError('16<=terms<=256 required')
    if not all(math.isfinite(t) for t in (z.real,z.imag)) or abs(z)>.1:
        raise ValueError('polylog series domain |z|<=.1')
    p=z;out=0j
    for n in range(1,terms+1):
        out+=p/n**order
        p*=z
    return out


def hpl_10m10(theta: complex, terms: int = SERIES_TERMS) -> complex:
    """H(1,0,-1,0;theta), standard kernels 1/(1-z),1/z,1/(1+z).

    Derived by expanding the 1D integral of
    [-log(t)*Li2(-t)+2*Li3(-t)]/(1-t). Principal log; theta=-u+i0.
    """
    z=_theta_domain(theta)
    if type(terms) is not int or not 16<=terms<=256:
        raise ValueError('16<=terms<=256 required')
    ell=cmath.log(z);s2=0.;s3=0.;p=z;out=0j
    for j in range(2,terms+1):
        n=j-1;sign=-1. if n%2 else 1.
        s2+=sign/n**2;s3+=sign/n**3
        p*=z
        out+=p/j*((1/j-ell)*s2+2*s3)
    return out


def hk_expression(theta, logtheta, log1m, li, H, zeta2, zeta3, zeta4):
    """Transcription of hep-ph/0509189 Eq.(3.7): F0^H B1^H.

    Arithmetic-agnostic for separate arbitrary-precision testing. The
    source formula is not derived by this function; see note references.
    """
    t=theta;l=logtheta;lm=log1m;d=1-t
    p2,p3,p4=li(2,t),li(3,t),li(4,t)
    n2,n3,n4=li(2,-t),li(3,-t),li(4,-t)
    v=t*(1+t)**2/d**4*(72*H+6*lm*l**3-36*zeta2*p2
        -36*zeta2*lm*l-108*zeta3*lm-64*n3+32*n2*l-8*zeta2*l)
    v-=36*t*(5+5*t+11*t*t+11*t**3)/d**5*n4
    v-=36*t*(5+5*t+7*t*t+7*t**3)/d**5*p4
    v+=4*t*(1+t)*(23+41*t*t)/d**5*(p3+n3)*l
    v-=16*t*(1+t+t*t+t**3)/d**5*n2*l*l
    v-=2*t*(5+5*t+23*t*t+23*t**3)/d**5*p2*l*l
    v+=t*(5+5*t-13*t*t-13*t**3)/(24*d**5)*l**4
    v+=t*(1+t-17*t*t-17*t**3)/d**5*zeta2*l*l
    v+=2*t*(11+11*t-43*t*t-43*t**3)/d**5*zeta3*l
    v+=36*t*(1+t-3*t*t-3*t**3)/d**5*zeta4
    v-=2*t*(55+82*t+55*t*t)/d**4*p3
    v+=2*t*(51+74*t+51*t*t)/d**4*p2*l
    v+=t*(47+66*t+47*t*t)/d**4*lm*l*l
    v+=t*(6+59*t+58*t*t+33*t**3)/(3*d**5)*l**3
    v+=2*t*(31+34*t+31*t*t)/d**4*zeta3
    v+=3*t*(3+22*t+3*t*t)/(2*d**4)*l*l
    v-=24*t*(1+t)/d**3*l
    v-=94*t/d**2
    return v


@lru_cache(maxsize=32768)
def hk_product(r: float) -> complex:
    """F0 B1 for 0<r<=.08, above pair threshold and away from it.

    theta is rationalized to avoid 1-sqrt(1-4r) cancellation.
    The numerical domain covers both declared b/c prescriptions.
    """
    if not math.isfinite(r) or not 0<r<=.08:
        raise ValueError('ratio domain is 0<r<=.08, not threshold kinematics')
    b=math.sqrt(1-4*r)
    t=complex(-4*r/(1+b)**2,0.)
    return hk_expression(t,cmath.log(t),cmath.log(1-t),li_series,
                         hpl_10m10(t),math.pi**2/6,
                         1.2020569031595942854,math.pi**4/90)


def coefficient_components(rb: float, rc: float, scale: float = 1.,
                           scheme: str = 'MSbar', kb: float=1., kc: float=1.) -> dict:
    """Dimensionless finite virtual coefficient Re[G A*], not full C_fin.

    G_MS,q=F0 B1+2 D F0 log(mu^2/mbar^2).
    G_OS,q=F0 B1-(8/3) D F0, derived from pole/MSbar re-expansion.
    A factor 2 is already in the source cross-section B coefficient.
    Universal 2 beta0 log(mu^2/Q^2)*B is returned SEPARATELY.
    """
    if not math.isfinite(scale) or scale<=0 or not all(math.isfinite(x) for x in (kb,kc)):
        raise ValueError('positive finite scale and finite real Yukawa probes required')
    if scheme not in ('MSbar','pole1'):
        raise ValueError('mass convention must be MSbar or pole1')
    f1,d1=rg.form_and_mass_derivative(rb);f2,d2=rg.form_and_mass_derivative(rc)
    if scheme=='MSbar':
        v1=hk_product(rb)+2*d1*(2*math.log(scale)-math.log(rb))
        v2=hk_product(rc)+2*d2*(2*math.log(scale)-math.log(rc))
    else:
        v1=hk_product(rb)-(8/3)*d1
        v2=hk_product(rc)-(8/3)*d2
    f1,d1,v1=kb*f1,kb*d1,kb*v1
    f2,d2,v2=kc*f2,kc*d2,kc*v2
    A=f1+f2;G=v1+v2
    B={'bb':abs(f1)**2,'cc':abs(f2)**2,'bc':2*(f1*f2.conjugate()).real,
       'coherent':abs(A)**2}
    virtual={'bb':(v1*f1.conjugate()).real,'cc':(v2*f2.conjugate()).real,
             'bc':(v1*f2.conjugate()+v2*f1.conjugate()).real,
             'coherent':(G*A.conjugate()).real}
    ulog={c:2*rg.BETA0*2*math.log(scale)*B[c] for c in COMPONENTS}
    return {'B':B,'virtual':virtual,'universal_scale_log':ulog}


def current_weight(Q: float, scale: float = 1., scheme: str = 'MSbar',
                   component: str = 'coherent', part: str = 'virtual',
                   kb: float = 1., kc: float = 1.) -> float:
    """Signed mass-dependent c_H current or explicitly selected companion term.

    'virtual' excludes source production pi^2 and all real pieces.
    'virtual_scale' includes only the universal coupling scale log in addition.
    'LO' is the pure coherent b/c leading current, for comparison.
    No returned option is a complete NLO gluonic decay current.
    """
    g._hard(Q,scale)
    if component not in COMPONENTS or part not in ('virtual','virtual_scale','LO'):
        raise ValueError('select a declared component and partial term')
    if scheme not in ('MSbar','pole1'):
        raise ValueError('mass convention must be MSbar or pole1')
    mb,mc=[h.running_mass(q,scale*Q) if scheme=='MSbar' else g.auxiliary_pole_mass(q)
           for q in ('b','c')]
    co=coefficient_components((mb/Q)**2,(mc/Q)**2,scale,scheme,kb,kc)
    a=h.alpha_s(scale*Q)/math.pi;pref=Q*Q/9
    if part=='LO': return pref*a*a*co['B'][component]
    v=co['virtual'][component]
    if part=='virtual_scale':v+=co['universal_scale_log'][component]
    return pref*a**3*v


def thermal(T: float, pair: str, scale: float=1., scheme: str='MSbar',
            component: str='coherent', part: str='virtual', method: str='w',
            cut: float=h.W_CUT, kb: float=1., kc: float=1.) -> tuple[float,float]:
    return h.thermal_from_weight(T,pair,
          lambda Q: current_weight(Q,scale,scheme,component,part,kb,kc),cut,method)


def complete_nlo_current(*args, **kwargs):
    """Explicitly reject mistaking this building block for a completed rate."""
    raise NotImplementedError('finite virtual c_H only: real/virtual assembly and cut matching incomplete')


def summary(T: float=.5) -> dict:
    weights=h.equilibrium_weights(T)
    pair={p:{c:thermal(T,p,component=c)[0] for c in COMPONENTS} for p in h.PAIRS}
    eff={c:sum(weights[p]*pair[p][c] for p in h.PAIRS) for c in COMPONENTS}
    scales={str(s):sum(weights[p]*thermal(T,p,scale=s,part='virtual_scale')[0]
                       for p in h.PAIRS) for s in (.5,1.,2.)}
    pole=sum(weights[p]*thermal(T,p,scheme='pole1')[0] for p in h.PAIRS)
    lo=sum(weights[p]*thermal(T,p,part='LO')[0] for p in h.PAIRS)
    check={p:{c:abs(thermal(T,p,component=c,method='Q')[0]-pair[p][c]) for c in COMPONENTS}
           for p in h.PAIRS}
    return {'date':'2026-10-10','temperature_GeV':T,'window_w':[0,h.W_CUT],
        'scope':'Mass-dependent infrared-regularized c_H virtual building block; NOT complete decay NLO.',
        'pair_virtual_GeV_minus2':pair,'conditional_effective_virtual_GeV_minus2':eff,
        'conditional_effective_LO_bc_square_GeV_minus2':lo,
        'virtual_plus_universal_scale_log_scan_GeV_minus2':scales,
        'auxiliary_pole1_virtual_GeV_minus2':pole,
        'Q_vs_w_absolute_differences_GeV_minus2':check,
        'chemical_equilibrium_established':False,'complete_coherent_NLO_computed':False,
        'physical_rate_beyond_Q80_computed':False,'relic_density_computed':False,
        'low_energy_Omnes_data_acquired':False,
        'source':'hep-ph/0509189 Eqs.(2.7),(3.4)-(3.7); source mass convention explicitly MSbar'}

if __name__=='__main__':
    import json
    print(json.dumps(summary(),indent=2))
