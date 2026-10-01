"""Note 45: finite collinear-subtracted real light-pair emission from b/c loops.

Calculates only the finite real-emission remainder for h* -> g q qbar,
q=u,d,s massless, induced coherently by bottom/charm loops. Not the full
real width, full bc-square NLO current, total QCD, or a relic abundance.
Source triangle: Spira et al. hep-ph/9504378, Appendix C, Eq. (C.5).
All physical energies GeV. Inherited source modules are unchanged.
"""
from __future__ import annotations
from functools import lru_cache
import math
import numpy as np
from scipy.integrate import quad, quad_vec
from scipy.special import roots_legendre
import heavy_quark_thermal as h
import gluon_loop_thermal as g

COMPONENTS = ('bb', 'cc', 'bc')


def _tau(tau: float) -> None:
    if not math.isfinite(tau) or tau <= 0:
        raise ValueError('positive finite tau required')


def loop_functions(tau: float) -> tuple[complex, complex]:
    """Spira f(tau), g(tau) with the physical timelike boundary value."""
    if not math.isfinite(tau) or tau < 0:
        raise ValueError('finite nonnegative tau required')
    if tau == 0:
        return 0j, 1.+0j
    if tau <= 1:
        angle = math.asin(math.sqrt(tau))
        return complex(angle*angle), complex(math.sqrt((1-tau)/tau)*angle)
    beta = math.sqrt(1-1/tau)
    Z = complex(math.log(tau)+2*math.log1p(beta), -math.pi)
    return -.25*Z*Z, .5*beta*Z


def offshell_triangle(tau: float, z: float) -> complex:
    """Normalized h* -> g g* transverse form factor; z=k^2/Q^2.

    -3/4 times A_qqg in source Eq. (C.5); F(tau,0)=Note42 F(tau).
    For 1-z<1e-3 use the derived endpoint expansion through second order.
    The physical application has tau>1, safely away from tau=1.
    Small-tau general use is not supported except z=0; no heavy-quark
    approximation is substituted into the actual b/c calculation.
    """
    _tau(tau)
    if not math.isfinite(z) or not 0 <= z <= 1:
        raise ValueError('z must be in [0,1]')
    if z == 0:
        return g.form_factor(tau)
    if tau < .01 or abs(tau-1.) < 1e-10:
        raise ValueError('off-shell evaluator requires tau>=.01 away from tau=1')
    f, aux = loop_functions(tau)
    if z > 1-1e-3:
        if tau > 1:
            beta = math.sqrt(1-1/tau)
            Z = complex(math.log(tau)+2*math.log1p(beta), -math.pi)
            fp = -Z/(2*tau*beta)
            fpp = (-1/(2*tau*tau*beta*beta)+Z/(2*tau*tau*beta)
                   +Z/(4*tau**3*beta**3))
            fppp = (1.5/(tau**3*beta**2)+.75/(tau**4*beta**4)
                    -Z/(tau**3*beta)-Z/(tau**4*beta**3)
                    -.375*Z/(tau**5*beta**5))
        else:
            angle = math.asin(math.sqrt(tau))
            den = math.sqrt(tau*(1-tau))
            fp = angle/den
            fpp = 1/(2*tau*(1-tau))-angle*(1-2*tau)/(2*den**3)
            fppp = (-3*(1-2*tau)/(4*den**4)+angle/den**3
                    +3*angle*(1-2*tau)**2/(4*den**5))
        edge = 3/(4*tau)*(1+(2*tau-1)*fp)
        slope = -(1-fp)/(4*tau)+(3*tau-1)*fpp/4
        quadratic = (1-fp)/(8*tau)+fpp/8+(4*tau*tau-tau)*fppp/16
        return edge+(z-1)*slope+(z-1)**2*quadratic
    fz, gz = loop_functions(z*tau)
    delta = z-1
    return -1.5/(tau*delta)*(1-2*z*(gz-aux)/delta
                            -(1+1/(tau*delta))*(fz-f))


def collinear_derivative(tau: float) -> complex:
    """Analytic partial derivative dF(tau,z)/dz at z=0."""
    _tau(tau)
    f, aux = loop_functions(tau)
    return 1.5/tau*(4-tau-2*aux+(1-2/tau)*f)


def _masses(Q: float, scale: float, scheme: str) -> tuple[float,float]:
    g._hard(Q,scale)
    if scheme == 'MSbar':
        return h.running_mass('b',scale*Q), h.running_mass('c',scale*Q)
    if scheme == 'pole1':
        return g.auxiliary_pole_mass('b'), g.auxiliary_pole_mass('c')
    raise ValueError('scheme must be MSbar or pole1')


def _products(Fb: complex, Fc: complex) -> np.ndarray:
    """The bc entry contains twice the real interference, never half."""
    return np.array([abs(Fb)**2,abs(Fc)**2,2*(Fb*Fc.conjugate()).real])


def subtracted_integrand(z: float, tb: float, tc: float) -> np.ndarray:
    """(1-z)^3/z times the difference from the on-shell squared amplitude.

    Entries are bb, cc, and signed bc interference. This subtraction convention
    removes the universal massless final-pair collinear singularity only.
    """
    _tau(tb); _tau(tc)
    if not math.isfinite(z) or not 0 <= z <= 1:
        raise ValueError('z must be in [0,1]')
    Fb0,Fc0 = g.form_factor(tb),g.form_factor(tc)
    if z == 1:
        return np.zeros(3)
    if z < 1e-9:
        Db,Dc = collinear_derivative(tb),collinear_derivative(tc)
        # This branch is the analytic collinear limit; its interval is tiny.
        return np.array([2*(Db*Fb0.conjugate()).real,
                         2*(Dc*Fc0.conjugate()).real,
                         2*(Db*Fc0.conjugate()+Fb0*Dc.conjugate()).real])
    Fb,Fc = offshell_triangle(tb,z),offshell_triangle(tc,z)
    # Difference-of-squares form reduces cancellation as z -> 0.
    db,dc = Fb-Fb0,Fc-Fc0
    difference = np.array([(db*(Fb+Fb0).conjugate()).real,
                           (dc*(Fc+Fc0).conjugate()).real,
                           2*(db*Fc.conjugate()+Fb0*dc.conjugate()).real])
    return ((1-z)**3/z)*difference



@lru_cache(maxsize=8)
def _legendre(n: int) -> tuple[np.ndarray,np.ndarray]:
    if type(n) is not int or not 16<=n<=512:
        raise ValueError('16<=quadrature nodes<=512 required')
    nodes,weights=roots_legendre(n)
    return (nodes+1)/2,weights/2


def _fg_vector(t: np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    f=np.empty(t.shape,dtype=complex);aux=np.empty(t.shape,dtype=complex)
    below=t<=1
    angle=np.arcsin(np.sqrt(t[below]))
    f[below]=angle*angle
    aux[below]=np.sqrt((1-t[below])/t[below])*angle
    beta=np.sqrt(1-1/t[~below])
    Z=np.log(t[~below])+2*np.log1p(beta)-1j*math.pi
    f[~below]=-.25*Z*Z;aux[~below]=.5*beta*Z
    return f,aux


def _off_vector(t: float,z: np.ndarray) -> np.ndarray:
    f,aux=loop_functions(t);fz,gz=_fg_vector(z*t);delta=z-1
    out=-1.5/(t*delta)*(1-2*z*(gz-aux)/delta-(1+1/(t*delta))*(fz-f))
    near=z>1-1e-3
    if np.any(near):
        beta=math.sqrt(1-1/t)
        Z=complex(math.log(t)+2*math.log1p(beta),-math.pi)
        fp=-Z/(2*t*beta)
        fpp=-1/(2*t*t*beta*beta)+Z/(2*t*t*beta)+Z/(4*t**3*beta**3)
        fppp=1.5/(t**3*beta**2)+.75/(t**4*beta**4)-Z/(t**3*beta)-Z/(t**4*beta**3)-.375*Z/(t**5*beta**5)
        quadratic=(1-fp)/(8*t)+fpp/8+(4*t*t-t)*fppp/16
        out[near]=3/(4*t)*(1+(2*t-1)*fp)+delta[near]*(-(1-fp)/(4*t)+(3*t-1)*fpp/4)+delta[near]**2*quadratic
    return out


def gaussian_remainder(tb: float,tc: float,n: int = 128) -> np.ndarray:
    """Fixed-order independent quadrature with threshold-smoothing maps.

    Only used for tb,tc>1, as in the audited b/c domain. The comparison
    between orders is a convergence diagnostic, not a rigorous error bound.
    """
    if not all(math.isfinite(t) and t>1 for t in (tb,tc)):
        raise ValueError('physical timelike b/c domain requires both tau>1')
    nodes,weights=_legendre(n)
    edges=sorted((0.,1/tb,1/tc,1.))
    lo=np.array(edges[:-1])[:,None];width=np.diff(edges)[:,None]
    theta=math.pi*nodes[None,:]/2
    zs=lo+width*np.sin(theta)**2
    jac=width*math.pi*np.sin(theta)*np.cos(theta)
    z=zs.ravel()
    Fb,Fc=_off_vector(tb,z),_off_vector(tc,z)
    Fb0,Fc0=g.form_factor(tb),g.form_factor(tc)
    db,dc=Fb-Fb0,Fc-Fc0
    differences=np.array([(db*(Fb+Fb0).conjugate()).real,
                          (dc*(Fc+Fc0).conjugate()).real,
                          2*(db*Fc.conjugate()+Fb0*dc.conjugate()).real])
    integrand=((1-z)**3/z)*differences
    near=z<1e-9
    if np.any(near):
        integrand[:,near]=subtracted_integrand(0.,tb,tc)[:,None]
    return np.sum(integrand.reshape(3,3,n)*jac[None,:,:]*weights[None,None,:],axis=(1,2))


@lru_cache(maxsize=16384)
def real_remainder(Q: float, scale: float = 1., scheme: str = 'MSbar',
                   method: str = 'gauss') -> tuple[float,float,float,float]:
    """Dimensionless finite J_bb,J_cc,J_bc and quadrature error-norm estimate.

    Branch points z=4m_q^2/Q^2 are split explicitly. Default 'gauss' uses
    vectorized Gaussian rules with sine-squared maps. The reported error is
    an order-comparison diagnostic, not a certificate. 'root' uses adaptive
    integration on those maps; 'z' is direct adaptive integration.
    """
    mb,mc = _masses(Q,scale,scheme)
    tb,tc = (Q/(2*mb))**2,(Q/(2*mc))**2
    edges = sorted((0.,1/tb,1/tc,1.))
    fun = lambda z:subtracted_integrand(z,tb,tc)
    if method == 'gauss':
        val = gaussian_remainder(tb,tc,128)
        err = float(np.linalg.norm(val-gaussian_remainder(tb,tc,64)))
    elif method == 'z':
        val,err = quad_vec(fun,0.,1.,points=edges[1:-1],epsabs=2e-13,
                           epsrel=2e-11,limit=500)
    elif method == 'root':
        val,err = np.zeros(3),0.
        for lo,hi in zip(edges[:-1],edges[1:]):
            def transformed(u):
                theta=math.pi*u/2
                z=lo+(hi-lo)*math.sin(theta)**2
                return fun(z)*(hi-lo)*math.pi*math.sin(theta)*math.cos(theta)
            v,e=quad_vec(transformed,0.,1.,epsabs=1e-13,epsrel=2e-11,limit=300)
            val+=v;err+=e
    else:
        raise ValueError('method must be gauss, z, or root')
    return float(val[0]),float(val[1]),float(val[2]),float(err)


def finite_real_current(Q: float, scale: float = 1., scheme: str = 'MSbar',
                        component: str = 'coherent', n_light: int = 3,
                        inner_method: str = 'gauss') -> float:
    """Delta S_real,finite = n_light*a^3 Q^2 J/27, GeV^2.

    Signed, subtraction-dependent finite remainder, NOT a positive channel.
    q=u,d,s are massless EMITTED flavors, not internal loop flavors.
    """
    if type(n_light) is not int or not 0<=n_light<=3:
        raise ValueError('n_light must be 0..3 for the declared veto convention')
    vals=real_remainder(Q,scale,scheme,inner_method)[:3]
    if component == 'coherent':
        J=sum(vals)
    elif component in COMPONENTS:
        J=vals[COMPONENTS.index(component)]
    else:
        raise ValueError('unknown component')
    a=h.alpha_s(scale*Q)/math.pi
    return n_light*a**3*Q*Q*J/27


def thermal_finite_real(T: float, pair: str, scale: float = 1.,
                        scheme: str = 'MSbar', component: str = 'coherent',
                        method: str = 'w', cut: float = h.W_CUT) -> tuple[float,float]:
    """Finite thermal window for the finite real remainder, in GeV^-2."""
    return h.thermal_from_weight(T,pair,
        lambda Q:finite_real_current(Q,scale,scheme,component),cut,method)


def counterterm_integral(epsilon: float) -> float:
    """Integral_epsilon^1 (1-z)^3/z dz. Diverges as -log(epsilon)."""
    if not math.isfinite(epsilon) or not 0<epsilon<1:
        raise ValueError('epsilon must be in (0,1)')
    return -math.log(epsilon)-11/6+3*epsilon-1.5*epsilon**2+epsilon**3/3


def resolved_real_and_counterterm(Q: float, epsilon: float,
                                  scale: float = 1.) -> dict[str,float]:
    """Diagnostic with an arbitrary invariant-pair-mass resolution cut.

    Both terms depend on epsilon. Their difference approaches J, not a total
    NLO width. The resolution is not a detector model or fitted cut.
    """
    ct=counterterm_integral(epsilon)
    mb,mc=_masses(Q,scale,'MSbar')
    tb,tc=(Q/(2*mb))**2,(Q/(2*mc))**2
    B=abs(g.form_factor(tb)+g.form_factor(tc))**2
    def integrand(z):
        return (1-z)**3/z*abs(offshell_triangle(tb,z)+offshell_triangle(tc,z))**2
    points=[z for z in (1/tb,1/tc) if epsilon<z<1]
    value,error=quad(integrand,epsilon,1.,points=points,epsabs=2e-12,
                     epsrel=1e-10,limit=400)
    return {'resolved_real_integral':value,'counterterm':B*ct,
            'difference':value-B*ct,'quadrature_error':error}


def complete_bc_nlo_current(*args, **kwargs):
    """Deliberately refuse to turn a finite real subpiece into complete NLO."""
    raise NotImplementedError('finite virtual, ggg, and compatible subtraction terms missing')


def summary(T: float = .5) -> dict:
    weights=h.equilibrium_weights(T)
    variants={}
    for label,scale,scheme in (('central',1.,'MSbar'),('mu_half',.5,'MSbar'),
                               ('mu_double',2.,'MSbar'),('pole1_diagnostic',1.,'pole1')):
        pairs={p:thermal_finite_real(T,p,scale,scheme)[0] for p in h.PAIRS}
        variants[label]={'pair_signed_remainders_GeV_minus2':pairs,
            'conditional_effective_GeV_minus2':sum(weights[p]*pairs[p] for p in h.PAIRS)}
    components={p:{c:thermal_finite_real(T,p,component=c)[0] for c in COMPONENTS}
                for p in h.PAIRS}
    comp_eff={c:sum(weights[p]*components[p][c] for p in h.PAIRS) for c in COMPONENTS}
    inherited_bc=sum(weights[p]*sum(g.thermal_gg(T,p,component=c)[0]
                     for c in ('bb','cc','bc')) for p in h.PAIRS)
    return {'temperature_GeV':T,'window_w':[0,h.W_CUT],
            'scope':'Finite collinear-subtracted massless u/d/s real-emission remainder from coherent b/c loops only.',
            'variants':variants,'pair_components_GeV_minus2':components,
            'conditional_effective_components_GeV_minus2':comp_eff,
            'inherited_LO_bc_square_GeV_minus2':inherited_bc,
            'signed_remainder_over_LO_bc_square':variants['central']['conditional_effective_GeV_minus2']/inherited_bc,
            'hard_Q20_J':dict(zip(COMPONENTS,real_remainder(20)[:3])),
            'real_resolution_checks_Q20':{str(e):resolved_real_and_counterterm(20,e) for e in (1e-3,1e-5,1e-7)},
            'full_bc_square_NLO_computed':False,'standalone_physical_partial_width':False,
            'full_coherent_NLO_gg_computed':False,'relic_density_computed':False,
            'chemical_equilibrium_established':False,'Q_above_80_included':False,
            'Omnes_data_acquired':False}


if __name__=='__main__':
    import json
    print(json.dumps(summary(),indent=2))
