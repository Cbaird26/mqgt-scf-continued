"""Note45: algebra/numerical checks of a finite real-emission subpiece only."""
import hashlib
import math
from pathlib import Path
import unittest
import mpmath as mp
import numpy as np
from scipy.integrate import quad
from scipy.special import roots_genlaguerre,kve
import bc_real_radiation as b
import heavy_quark_thermal as h
import gluon_loop_thermal as g


def mp_off(t,z):
    with mp.workdps(65):
        t,z=mp.mpf(str(t)),mp.mpf(str(z))
        def fg(v):
            if v==0:return mp.mpc(0),mp.mpc(1)
            if v<=1:
                a=mp.asin(mp.sqrt(v));return a*a,mp.sqrt((1-v)/v)*a
            beta=mp.sqrt(1-1/v);Z=mp.log((1+beta)/(1-beta))-mp.j*mp.pi
            return -Z*Z/4,beta*Z/2
        f,aux=fg(t)
        if z==0:
            return complex(mp.mpf(3)/(2*t)*(1+(1-1/t)*f))
        if z==1:
            fp=mp.diff(lambda v:fg(v)[0],t)
            return complex(3/(4*t)*(1+(2*t-1)*fp))
        fz,gz=fg(z*t)
        return complex(-mp.mpf(3)/(2*t*(z-1))*(1-2*z*(gz-aux)/(z-1)
                    -(1+1/(t*(z-1)))*(fz-f)))


def log_parameter_off(t,z):
    # Independent one-dimensional log-integral representation of f and g.
    roots=[]
    for v in (t,z*t):
        if v>=1:
            beta=math.sqrt(1-1/v);roots.extend([(1-beta)/2,(1+beta)/2])
    points=sorted(set(roots))
    def integrand(x):
        A=4*z*t*(x-.5)**2+(1-z*t);B=4*t*(x-.5)**2+(1-t)
        logdiff=complex(math.log(abs(A))-math.log(abs(B)),
                        -math.pi*((A<0)-(B<0)))
        return (-z/(z-1)+.5*(1+1/(t*(z-1)))/x)*logdiff
    re=quad(lambda x:integrand(x).real,0,1,points=points,
             epsabs=2e-10,epsrel=2e-10,limit=500)[0]
    im=quad(lambda x:integrand(x).imag,0,1,points=points,
             epsabs=2e-10,epsrel=2e-10,limit=500)[0]
    return -1.5/(t*(z-1))*(1+complex(re,im))


def thermal_laguerre(T,pair,n=64):
    mi,mj,k=h.PAIRS[pair];xi,xj=mi/T,mj/T;a=xi+xj;d=xi-xj
    nodes,weights=roots_genlaguerre(n,.5)
    total=0.
    for w,weight in zip(nodes,weights):
        if w>90:continue
        y=a+w;Q=T*y
        total+=weight*y*y*math.sqrt((2*a+w)*(y*y-d*d))*b.finite_real_current(Q)*kve(1,y)/((Q*Q-h.MH*h.MH)**2+(h.MH*h.GH)**2)
    return float(k*k*total/(32*math.pi*xi**2*xj**2*kve(2,xi)*kve(2,xj)))


class RealEmissionTests(unittest.TestCase):
    def test_inherited_hashes(self):
        refs={'heavy_quark_thermal.py':'40d51657a26fb20851be2bafa0ea6b3efe05ddfb',
              'gluon_loop_thermal.py':'c49c6fab4baa2d9c01c64f9fd8c2fdb7f018d50c',
              'finite_mass_quark_thermal.py':'117fd5d3abb650f05334d8bff6f88115c63e09da',
              'top_operator_nlo.py':'cf2c5f0fa09802330dfdf401e15ed1c1d78b9ab3',
              'mixed_gluon_nlo.py':'0ffc28870c414cc8613d28549511d10bcaf30ee7'}
        for name,sha in refs.items():
            raw=Path(__file__).with_name(name).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),sha)

    def test_on_shell_recovers_note42(self):
        for t in (.01,.1,.9,2.,10.,100.,4000.):
            self.assertEqual(b.offshell_triangle(t,0),g.form_factor(t))

    def test_offshell_65_digit_formula(self):
        for t in (.03,.4,2.,10.,200.,4000.):
            for z in (1e-6,.01,.3,.8,.99):
                self.assertLess(abs(b.offshell_triangle(t,z)-mp_off(t,z)),3e-9)

    def test_soft_endpoint_and_transition(self):
        for t in (.4,2.,10.,200.):
            for z in (1.,.9999999,.999995,.999989,.999001,.998999):
                self.assertLess(abs(b.offshell_triangle(t,z)-mp_off(t,z)),2e-8)

    def test_internal_branch_points(self):
        for t in (10.,100.):
            for z in (1/t-1e-8,1/t,1/t+1e-8):
                self.assertLess(abs(b.offshell_triangle(t,z)-mp_off(t,z)),3e-10)

    def test_collinear_derivative(self):
        for t in (10.,200.,4000.):
            dz=1e-7/t
            numeric=(mp_off(t,dz)-mp_off(t,0))/dz
            self.assertLess(abs(numeric-b.collinear_derivative(t)),2e-5)

    def test_parameter_log_integral(self):
        for t,z in ((2.,.2),(10.,.1),(10.,.6),(200.,.3)):
            self.assertLess(abs(log_parameter_off(t,z)-b.offshell_triangle(t,z)),3e-8)

    def test_heavy_loop_limit(self):
        # Derived expansion: 1+(7+11z)t/30+(10+16z+22z^2)t^2/105.
        # Tests the actual asymptotic law, rather than an arbitrary closeness.
        for z in (.1,.5,.9):
            for t in (.01,.02):
                series=1+(7+11*z)*t/30+(10+16*z+22*z*z)*t*t/105
                self.assertLess(abs(b.offshell_triangle(t,z)-series),t**3)

    def test_vectorized_triangles_match_scalar(self):
        zs=np.array([1e-8,.001,.01,.05,.2,.5,.9,.999999])
        for t in (10.,200.):
            self.assertLess(max(abs(b._off_vector(t,zs)-np.array([b.offshell_triangle(t,z) for z in zs]))),2e-10)

    def test_coherent_products_include_cross_term(self):
        for z in (.001,.03,.2,.8):
            Fb,Fc=b.offshell_triangle(10.,z),b.offshell_triangle(200.,z)
            self.assertAlmostEqual(sum(b._products(Fb,Fc)),abs(Fb+Fc)**2,delta=3e-15)

    def test_subtracted_collinear_endpoint_is_finite(self):
        exact=b.subtracted_integrand(0,10.,200.)
        self.assertTrue(np.all(np.isfinite(exact)))
        self.assertLess(max(abs(b.subtracted_integrand(1e-8,10.,200.)-exact)),1e-5)
        self.assertTrue(np.all(b.subtracted_integrand(1,10.,200.)==0))

    def test_three_inner_representations(self):
        for Q in (20.,23.,50.,80.):
            refs=b.real_remainder(Q)[:3]
            for method in ('z','root'):
                v=b.real_remainder(Q,method=method)[:3]
                self.assertLess(max(abs(x-y) for x,y in zip(refs,v)),2e-10)

    def test_gaussian_order_convergence(self):
        for Q in (20.,40.,80.):
            mb,mc=b._masses(Q,1.,'MSbar');tb,tc=(Q/(2*mb))**2,(Q/(2*mc))**2
            v=b.gaussian_remainder(tb,tc,128)
            self.assertLess(max(abs(v-b.gaussian_remainder(tb,tc,256))),2e-11)

    def test_gaussian_swap_symmetry(self):
        direct=b.gaussian_remainder(10,200)
        swap=b.gaussian_remainder(200,10)
        self.assertLess(max(abs(direct-swap[[1,0,2]])),2e-12)

    def test_q20_reference(self):
        v=b.real_remainder(20)
        refs=(.09066254160250937,-.012759957015088322,-.1552327005879538)
        self.assertLess(max(abs(x-y) for x,y in zip(v[:3],refs)),1e-11)

    def test_real_phase_space_normalization(self):
        # Explicit two-body tensor contraction, color trace and phase space.
        metric=np.diag([1.,-1.,-1.,-1.]);Q=3.4;alpha=.18;TR=.5
        for z in (.1,.4,.8):
            E=Q*(1-z)/2;p=np.array([E,0,0,E]);k=np.array([Q-E,0,0,-E])
            pk=p@metric@k
            V=pk*metric-np.outer(k,p)
            polsum=sum(metric[i,i]*metric[j,j]*V[i,j]**2 for i in range(4) for j in range(4))
            self.assertAlmostEqual(polsum,2*pk*pk,places=11)
            born=(1/(2*Q))*.5*(1/(8*math.pi))*(Q**4/2)
            spectral=(4*math.pi*alpha)*TR/(6*math.pi)
            real=(1/(2*Q))*(Q*Q/(2*math.pi))*((1-z)/(8*math.pi))*spectral/(z*Q*Q)*polsum
            self.assertAlmostEqual(real/born,(alpha/math.pi)/3*(1-z)**3/z,delta=3e-14)

    def test_counterterm_analytic_integral(self):
        for eps in (.001,.1,.5):
            numerical=quad(lambda z:(1-z)**3/z,eps,1,epsabs=1e-12)[0]
            self.assertAlmostEqual(b.counterterm_integral(eps),numerical,delta=2e-12)

    def test_resolution_subtraction_converges(self):
        J=sum(b.real_remainder(20)[:3]);errors=[]
        for e in (1e-3,1e-5,1e-7):
            result=b.resolved_real_and_counterterm(20,e)
            self.assertGreater(result['resolved_real_integral'],0)
            self.assertGreater(result['counterterm'],0)
            errors.append(abs(result['difference']-J))
        self.assertLess(errors[1],errors[0]/80)
        self.assertLess(errors[2],errors[1]/80)
        self.assertLess(errors[2],3e-7)

    def test_nlight_scaling(self):
        one=b.finite_real_current(20,n_light=1)
        self.assertAlmostEqual(b.finite_real_current(20,n_light=3),3*one,delta=1e-16)
        self.assertEqual(b.finite_real_current(20,n_light=0),0)

    def test_thermal_pair_references(self):
        refs={'11':-1.6525606062989504e-19,'12':-2.2201231653333243e-19,'22':-2.6555937545406168e-19}
        for pair,ref in refs.items():
            self.assertAlmostEqual(b.thermal_finite_real(.5,pair)[0]/ref,1,delta=2e-8)

    def test_thermal_Q_vs_w(self):
        for pair in h.PAIRS:
            v=b.thermal_finite_real(.5,pair)[0]
            q=b.thermal_finite_real(.5,pair,method='Q')[0]
            self.assertAlmostEqual(q/v,1,delta=2e-8)

    def test_thermal_independent_laguerre(self):
        for pair in h.PAIRS:
            self.assertAlmostEqual(thermal_laguerre(.5,pair)/b.thermal_finite_real(.5,pair)[0],1,delta=2e-8)

    def test_window_and_lower_temperature(self):
        v=b.thermal_finite_real(.5,'12')[0]
        for cut in (60.,100.):
            self.assertAlmostEqual(b.thermal_finite_real(.5,'12',cut=cut)[0]/v,1,delta=2e-8)
        v=b.thermal_finite_real(1/3,'11')[0]
        self.assertAlmostEqual(b.thermal_finite_real(1/3,'11',method='Q')[0]/v,1,delta=2e-8)

    def test_signed_thermal_decomposition(self):
        for p in h.PAIRS:
            total=sum(b.thermal_finite_real(.5,p,component=c)[0] for c in b.COMPONENTS)
            self.assertAlmostEqual(total,b.thermal_finite_real(.5,p)[0],delta=1e-28)

    def test_conditional_weighted_result(self):
        weights=h.equilibrium_weights(.5)
        v=sum(weights[p]*b.thermal_finite_real(.5,p)[0] for p in h.PAIRS)
        self.assertAlmostEqual(v/-1.7170739298805313e-19,1,delta=2e-8)

    def test_scheme_diagnostic_is_not_fixed_sign(self):
        weights=h.equilibrium_weights(.5)
        central=sum(weights[p]*b.thermal_finite_real(.5,p)[0] for p in h.PAIRS)
        pole=sum(weights[p]*b.thermal_finite_real(.5,p,scheme='pole1')[0] for p in h.PAIRS)
        self.assertLess(central,0);self.assertGreater(pole,0)

    def test_refuse_complete_NLO(self):
        with self.assertRaises(NotImplementedError):b.complete_bc_nlo_current(20)

    def test_invalid_arguments(self):
        for fn in (lambda:b.finite_real_current(19.),lambda:b.finite_real_current(81.),
                   lambda:b.finite_real_current(20,scale=3),lambda:b.finite_real_current(20,scheme='guess'),
                   lambda:b.finite_real_current(20,component='tt'),lambda:b.finite_real_current(20,n_light=5),
                   lambda:b.offshell_triangle(0,.2),lambda:b.offshell_triangle(10,-.1),
                   lambda:b.counterterm_integral(0),lambda:b.thermal_finite_real(1,'11'),
                   lambda:b._legendre(10),lambda:b.gaussian_remainder(.5,2)):
            with self.assertRaises(ValueError):fn()

    def test_summary_scope_flags(self):
        result=b.summary()
        for field in ('full_bc_square_NLO_computed','standalone_physical_partial_width',
                      'full_coherent_NLO_gg_computed','relic_density_computed',
                      'chemical_equilibrium_established','Q_above_80_included','Omnes_data_acquired'):
            self.assertFalse(result[field])


if __name__=='__main__':unittest.main()
