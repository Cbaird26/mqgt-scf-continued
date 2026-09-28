"""Note 40 software and approximation checks; NOT physical validation."""
import math
import unittest
from scipy.integrate import solve_ivp
import heavy_quark_thermal as h


class HeavyQuarkThermalTests(unittest.TestCase):
    def test_rg_coefficients(self):
        b0,b1,g0,g1=h.rg_coefficients(5)
        self.assertAlmostEqual(b0,23/12)
        self.assertAlmostEqual(b1,29/12)
        self.assertEqual(g0,1.)
        self.assertAlmostEqual(g1,253/72)

    def test_alpha_boundary(self):
        self.assertAlmostEqual(h.alpha_s(h.MZ),h.ALPHA_MZ,delta=1e-13)

    def test_bottom_mass_boundary(self):
        self.assertAlmostEqual(h.running_mass('b',10.),h.MB_AT_10,delta=1e-12)

    def test_rg_implicit_vs_independent_ode(self):
        b0,b1,_,_=h.rg_coefficients(5)
        sol=solve_ivp(lambda t,y: [-b0*y[0]**2-b1*y[0]**3],
                      (2*math.log(h.MZ),2*math.log(20.)),[h.ALPHA_MZ/math.pi],
                      rtol=2e-12,atol=1e-14,method='DOP853')
        self.assertTrue(sol.success)
        self.assertAlmostEqual(math.pi*sol.y[0,-1]/h.alpha_s(20.),1.,delta=2e-10)

    def test_bottom_running_vs_independent_ode(self):
        b0,b1,g0,g1=h.rg_coefficients(5)
        def f(t,y):
            a=y[0]
            return [-b0*a*a-b1*a**3,-g0*a-g1*a*a]
        sol=solve_ivp(f,(2*math.log(10),2*math.log(40)),
                      [h.alpha_s(10.)/math.pi,math.log(h.MB_AT_10)],
                      rtol=2e-12,atol=1e-14,method='DOP853')
        self.assertTrue(sol.success)
        self.assertAlmostEqual(math.exp(sol.y[1,-1])/h.running_mass('b',40.),1.,delta=2e-10)

    def test_charm_matching_vs_independent_piecewise_ode(self):
        state=[h.alpha_s(3.)/math.pi, math.log(h.MC_AT_3)]
        for lo,hi,nf in ((3.,h.MATCH_B,4),(h.MATCH_B,20.,5)):
            b0,b1,g0,g1=h.rg_coefficients(nf)
            def f(t,y):
                a=y[0]
                return [-b0*a*a-b1*a**3,-g0*a-g1*a*a]
            sol=solve_ivp(f,(2*math.log(lo),2*math.log(hi)),state,
                          rtol=2e-12,atol=1e-14,method='DOP853')
            self.assertTrue(sol.success)
            state=sol.y[:,-1]
        self.assertAlmostEqual(math.exp(state[1])/h.running_mass('c',20.),1.,delta=2e-10)

    def test_running_path_composition(self):
        a,b,c=[h.alpha_s(mu)/math.pi for mu in (10.,20.,40.)]
        self.assertAlmostEqual(h.mass_ratio(c,a,5),h.mass_ratio(c,b,5)*h.mass_ratio(b,a,5),delta=1e-13)

    def test_running_positive_and_decreasing(self):
        mus=(10.,20.,40.,80.,160.)
        for values in ([h.alpha_s(mu) for mu in mus],
                       [h.running_mass('b',mu) for mu in mus],
                       [h.running_mass('c',mu) for mu in mus]):
            self.assertTrue(all(x>0 for x in values))
            self.assertTrue(all(a>b for a,b in zip(values,values[1:])))

    def test_nlo_coefficient_and_log(self):
        self.assertEqual(h.qcd_coefficient(20,20,0.),1.)
        self.assertAlmostEqual(h.qcd_coefficient(20,20,.15),1+17*.15/(3*math.pi))
        self.assertAlmostEqual(h.qcd_coefficient(20,40,.15),1+.15/math.pi*(17/3+4*math.log(2)))

    def test_leading_scale_log_cancellation(self):
        a0=1e-5
        def combined(scale):
            a=h.a_fixed_nf(20*scale,20,a0,5)
            return h.mass_ratio(a,a0,5)**2*h.qcd_coefficient(20,20*scale,math.pi*a)
        slope=(combined(math.exp(1e-3))-combined(math.exp(-1e-3)))/.002
        self.assertLess(abs(slope),1e-7)  # O(a^2), not O(a)

    def test_scalar_current_normalization(self):
        Q=22.; mi,mj,k=h.PAIRS['12']; s=Q*Q
        S=h.current_weight(Q,'b')
        D=(s-h.MH*h.MH)**2+(h.MH*h.GH)**2
        root=math.sqrt((s-(mi+mj)**2)*(s-(mi-mj)**2))
        width=Q*S/(8*math.pi*h.V**2)
        spectral=h.V**2*k*k*Q*width/(D*root)
        direct=k*k*s*S/(8*math.pi*D*root)
        self.assertAlmostEqual(spectral/direct,1.,delta=1e-14)

    def test_lepton_regression_equal_and_unequal(self):
        mf=1.77686
        weight=lambda Q: mf*mf*(1-4*mf*mf/(Q*Q))**1.5
        refs={'11':9.70342862021e-16,'12':9.93179396e-16,'22':1.00691241496e-15}
        for p,value in refs.items():
            self.assertAlmostEqual(h.thermal_from_weight(.5,p,weight)[0],value,delta=8e-25)

    def test_two_variable_quadratures_all_six(self):
        for p in h.PAIRS:
            for q in ('b','c'):
                a=h.thermal_quark(.5,p,q)[0]
                b=h.thermal_quark(.5,p,q,method='Q')[0]
                self.assertAlmostEqual(a/b,1.,delta=2e-9)

    def test_bc_reference_totals(self):
        refs={'11':1.40185320775e-14,'12':1.39989874103e-14,'22':1.38829485425e-14}
        for p,v in refs.items():
            self.assertAlmostEqual(sum(h.thermal_quark(.5,p,q)[0] for q in ('b','c')),v,delta=2e-24)

    def test_lower_temperature_is_numerically_supported(self):
        a=h.thermal_quark(1/3,'12','b')[0]
        b=h.thermal_quark(1/3,'12','b',method='Q')[0]
        self.assertGreater(a,0.)
        self.assertAlmostEqual(a/b,1.,delta=2e-9)

    def test_finite_window_sensitivity(self):
        a=h.thermal_quark(.5,'11','b',cut=90)[0]
        b=h.thermal_quark(.5,'11','b',cut=100)[0]
        self.assertAlmostEqual(a/b,1.,delta=2e-9)

    def test_formal_tail_positive_tiny(self):
        for p in h.PAIRS:
            for q in ('b','c'):
                t=h.formal_tail_bound(.5,p,q)
                self.assertGreater(t,0.)
                self.assertLess(t/h.thermal_quark(.5,p,q)[0],1e-20)

    def test_phase_diagnostic_not_central_result(self):
        for p in h.PAIRS:
            for q in ('b','c'):
                self.assertLess(h.thermal_quark(.5,p,q,born_phase=True)[0],h.thermal_quark(.5,p,q)[0])

    def test_linear_thermal_functional(self):
        w=lambda Q:h.current_weight(Q,'b')
        a=h.thermal_from_weight(.5,'12',w)[0]
        b=h.thermal_from_weight(.5,'12',lambda Q:2*w(Q))[0]
        self.assertAlmostEqual(b/a,2.,delta=1e-12)

    def test_equilibrium_weights_are_conditional(self):
        w=h.equilibrium_weights(.5)
        self.assertAlmostEqual(sum(w.values()),1.,delta=1e-14)
        self.assertAlmostEqual(w['12'],.10788217663518722,delta=1e-14)

    def test_no_low_energy_extrapolation(self):
        with self.assertRaises(ValueError):h.current_weight(1.5,'b')
        with self.assertRaises(ValueError):h.current_weight(19.9,'b')
        with self.assertRaises(ValueError):h.current_weight(81.,'b')

    def test_invalid_inputs(self):
        for f in (lambda:h.alpha_s(2),lambda:h.running_mass('s',20),
                  lambda:h.current_weight(20,'b',scale=3),lambda:h.thermal_quark(1,'11','b'),
                  lambda:h.thermal_quark(.5,'21','b'),lambda:h.thermal_quark(.5,'11','b',cut=0),
                  lambda:h.thermal_quark(.5,'11','b',method='bad'),
                  lambda:h.a_fixed_nf(float('nan'),20,.05,5)):
            with self.assertRaises(ValueError):f()


if __name__=='__main__':
    unittest.main()
