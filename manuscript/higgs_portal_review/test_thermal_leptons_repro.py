"""Mathematical regressions for Note 36. Not a physical model validation."""
import math
import unittest
from thermal_leptons_repro import (
    M1,MH,MASS,K11,GH,sigma_v,thermal_quad,thermal_laguerre,
    tail_upper_bound,equilibrium_density,hubble,summarize
)

class ThermalLeptonicRegression(unittest.TestCase):
    def test_threshold_total_matches_note28(self):
        actual=sum(sigma_v(4*M1*M1,mf) for mf in MASS.values())
        self.assertAlmostEqual(actual,1.03679016281e-15,delta=2e-26)
    def test_threshold_tau_matches_note28(self):
        self.assertAlmostEqual(sigma_v(400.,MASS['tau']),1.03295820409e-15,delta=2e-26)
    def test_threshold_and_resonance_values(self):
        m=MASS['tau']
        self.assertGreater(sigma_v(MH*MH,m),sigma_v(400,m))
        self.assertEqual(sigma_v(400.,M1),0.)
    def test_leptonic_cross_sections_nonnegative(self):
        for s in (400.,402.,1000.,MH*MH,20000.):
            for mf in MASS.values():
                self.assertGreaterEqual(sigma_v(s,mf),0.)
    def test_independent_integrators_three_masses(self):
        for mf in MASS.values():
            v,_=thermal_quad(20.,mf)
            gl=thermal_laguerre(20.,mf)
            self.assertAlmostEqual(gl/v,1.,delta=2e-11)
    def test_independent_integrators_three_temperatures(self):
        for x in (10.,20.,30.):
            v,_=thermal_quad(x,MASS['tau'])
            gl=thermal_laguerre(x,MASS['tau'])
            self.assertAlmostEqual(gl/v,1.,delta=2e-11)
    def test_laguerre_quadrature_order(self):
        for x in (10.,20.,30.):
            v=thermal_laguerre(x,MASS['tau'],64)
            self.assertAlmostEqual(thermal_laguerre(x,MASS['tau'],32)/v,1.,delta=1e-8)
    def test_tau_values_note35(self):
        expected={10.:9.19878793e-16,20.:9.70342862e-16,30.:9.89733829e-16}
        for x,value in expected.items():
            self.assertAlmostEqual(thermal_quad(x,MASS['tau'])[0],value,delta=8e-25)
    def test_three_lepton_sum_at_x20(self):
        s=summarize(20.)
        self.assertAlmostEqual(s['leptonic_partial'],9.73929725783516e-16,delta=5e-27)
        self.assertAlmostEqual(sum(s['channels'].values()),s['leptonic_partial'],delta=1e-28)
    def test_old_formal_and_new_thermal_reference(self):
        s=summarize(20.)
        old=equilibrium_density(20.)*s['threshold_partial']/hubble(20.)
        self.assertAlmostEqual(old,6.31276235e-6,delta=2e-14)
        self.assertAlmostEqual(s['formal_equilibrium_ratio'],5.93002048073e-6,delta=3e-17)
    def test_tail_upper_bounds_are_positive_and_tiny(self):
        for x in (10.,20.,30.):
            s=summarize(x)
            self.assertGreater(s['tail_bound'],0.)
            self.assertLess(s['tail_bound']/s['leptonic_partial'],1e-20)
    def test_window_change_within_proven_tail_bound(self):
        for mf in MASS.values():
            v90=thermal_quad(20.,mf,90.)[0]
            v100=thermal_quad(20.,mf,100.)[0]
            self.assertLessEqual(abs(v100-v90),tail_upper_bound(20.,mf,90.)+2e-25)
    def test_reference_density_is_not_actual_density(self):
        self.assertAlmostEqual(equilibrium_density(20.),1.60329212678e-9,delta=7e-21)
        self.assertAlmostEqual(hubble(20.),2.63320146442e-19,delta=3e-31)
    def test_invalid_inputs_fail_closed(self):
        for s,mf in ((399.,MASS['mu']),(400.,-1.),(math.inf,1.)):
            with self.assertRaises(ValueError):sigma_v(s,mf)
        for x in (-1.,0.,math.inf):
            with self.assertRaises(ValueError):thermal_quad(x,MASS['tau'])
        with self.assertRaises(ValueError):thermal_laguerre(20.,MASS['tau'],4)
        with self.assertRaises(ValueError):tail_upper_bound(20.,MASS['tau'],-2.)

if __name__ == '__main__':unittest.main()
