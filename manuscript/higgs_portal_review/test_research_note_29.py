"""Mathematical regression only; no real cosmological computation."""
import math
import unittest
from thermal_conversion_gate import (HBAR, M1, M2, GAMMA_LEP,
                                     M_PLANCK, hubble_radiation,
                                     equilibrium_heavy_to_light, rates)


class ConversionGateTests(unittest.TestCase):
    def test_hubble_matches_166(self):
        self.assertAlmostEqual(hubble_radiation(.5, 60) /
                               (1.66*math.sqrt(60)*.5**2/M_PLANCK), 1, delta=.0008)

    def test_hubble_scales_quadratically(self):
        self.assertAlmostEqual(hubble_radiation(1)/hubble_radiation(.5),4)

    def test_hubble_scales_sqrt_g(self):
        self.assertAlmostEqual(hubble_radiation(.5,100)/hubble_radiation(.5,25),2)

    def test_equilibrium_ratio_matches_prior(self):
        r=equilibrium_heavy_to_light(.5)
        self.assertAlmostEqual(r/(1+r),.05784749058,delta=3e-11)

    def test_colder_less_heavy(self):
        self.assertLess(equilibrium_heavy_to_light(.4),equilibrium_heavy_to_light(.5))

    def test_partial_gamma_nonzero(self):
        self.assertLess(rates(.5)['gamma_lep_H_upper'],.002)
        self.assertGreater(rates(.5)['gamma_lep_H_upper'],.001)

    def test_inverse_per_light_detailed_balance(self):
        r = rates(.5)
        self.assertAlmostEqual(r['inverse_per_light_H_upper']/r['gamma_lep_H_upper'],r['q_nr'])

    def test_lower_thermal_rate_than_rest_frame(self):
        r = rates(.5)
        self.assertLess(r['inverse_per_light_H_upper'],r['gamma_lep_H_upper'])

    def test_hubble_seconds(self):
        r=rates(.5)
        self.assertAlmostEqual(r['H_time_s']*r['H_per_s'],1)
        self.assertAlmostEqual(r['gamma_lep_s']*(HBAR/GAMMA_LEP),1)

    def test_zero_leptonic_rate(self):
        r=rates(.5,gamma_lep=0)
        self.assertEqual(r['inverse_per_light_H_upper'],0)
        self.assertEqual(r['gamma_lep_H_upper'],0)

    def test_invalid_inputs(self):
        for T,g in [(0,60),(-1,60),(.5,0),(.5,float('nan'))]:
            with self.subTest(T=T,g=g), self.assertRaises(ValueError): hubble_radiation(T,g)
        with self.assertRaises(ValueError): rates(.5,gamma_lep=-1)
        with self.assertRaises(ValueError): equilibrium_heavy_to_light(.5,m2=M1)

    def test_independent_radiation_friedmann(self):
        # Natural units G=1/Mpl²; rho=pi²/30 g T^4; H²=8pi G rho/3
        T=.5; g=60
        independent=math.sqrt((8*math.pi/(3*M_PLANCK*M_PLANCK)) * (math.pi**2/30*g*T**4))
        self.assertAlmostEqual(hubble_radiation(T,g)/independent,1,places=14)


class ExactMBTests(unittest.TestCase):
    def test_positive_integral_and_time_dilation(self):
        from thermal_conversion_gate import _scaled_besselk_nu
        for z in (20,23,25,28.75):
            self.assertGreater(_scaled_besselk_nu(2,z),_scaled_besselk_nu(1,z))

    def test_exact_mb_half_gev(self):
        from thermal_conversion_gate import exact_mb_metrics
        r=exact_mb_metrics(.5)
        self.assertAlmostEqual(r['mb_q'], .0606867676649,delta=1e-10)
        self.assertAlmostEqual(r['time_dilation'],.938176870693,delta=1e-10)
        self.assertAlmostEqual(r['mb_heavy_fraction'], .0572145986119,delta=1e-10)

    def test_exact_mb_04_gev(self):
        from thermal_conversion_gate import exact_mb_metrics
        r=exact_mb_metrics(.4)
        self.assertAlmostEqual(r['mb_inverse_per_light_H'],4.95651158833e-05,delta=2e-12)

    def test_massive_mb_occupancy_is_not_nr_exact(self):
        from thermal_conversion_gate import exact_mb_metrics
        r=exact_mb_metrics(.5)
        self.assertLess(r['mb_heavy_fraction'],r['heavy_fraction'])
        self.assertLess(r['mb_inverse_per_light_H'],r['inverse_per_light_H_upper'])


if __name__=='__main__':
    unittest.main(verbosity=2)
