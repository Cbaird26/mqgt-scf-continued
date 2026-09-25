"""Pure algebra/regression checks, not experimental or astrophysical validation."""
import math
import unittest
from stable_singlet_direct_detection import (
    M_H, M_N, V, GEV_MINUS2_TO_CM2, crossing_ratio_cm2_per_gev,
    density_rescaled_cross_section, higgs_to_light_pair_width,
    inelastic_target_kinetic_threshold, nucleon_cross_section,
)


class StableSingletNucleonTests(unittest.TestCase):
    def test_numerical_benchmark(self):
        self.assertAlmostEqual(nucleon_cross_section()/7.39917378137e-47, 1., places=11)

    def test_higgs_width_agrees_with_note22(self):
        self.assertAlmostEqual(higgs_to_light_pair_width()/4.75366954175e-6, 1., places=10)

    def test_crossing_identity(self):
        sigma=nucleon_cross_section()
        gamma=higgs_to_light_pair_width()
        self.assertAlmostEqual(sigma/(gamma*crossing_ratio_cm2_per_gev()),1.,places=13)

    def test_alternate_benchmark_crossing(self):
        for m,k in ((4,.003),(15,.0002),(50,.009)):
            sigma=nucleon_cross_section(m,k)
            gamma=higgs_to_light_pair_width(m,k)
            self.assertAlmostEqual(sigma/(gamma*crossing_ratio_cm2_per_gev(m)),1.,places=12)

    def test_portal_quadratic_scaling(self):
        self.assertAlmostEqual(nucleon_cross_section(k11=.002)/nucleon_cross_section(),4)

    def test_form_factor_scaling(self):
        self.assertAlmostEqual(nucleon_cross_section(f_n=.35)/nucleon_cross_section(),(.35/.30)**2)

    def test_zero_portal(self):
        self.assertEqual(nucleon_cross_section(k11=0),0)
        self.assertEqual(higgs_to_light_pair_width(k11=0),0)

    def test_closed_pair_threshold_and_crossing_gate(self):
        self.assertEqual(higgs_to_light_pair_width(m1=62.5),0)
        with self.assertRaises(ValueError):
            crossing_ratio_cm2_per_gev(m1=62.5)

    def test_density_fraction_is_rate_factor(self):
        sigma=nucleon_cross_section()
        self.assertEqual(density_rescaled_cross_section(sigma,0.0),0.)
        self.assertAlmostEqual(density_rescaled_cross_section(sigma,.1)/sigma,.1)
        self.assertEqual(density_rescaled_cross_section(sigma,1.),sigma)

    def test_inelastic_lab_threshold(self):
        expected=(11.5**2-10**2)/(2*M_N)+(11.5-10)
        self.assertAlmostEqual(inelastic_target_kinetic_threshold(),expected)
        self.assertGreater(expected,18.)

    def test_invalid_mass_and_portal(self):
        for kw in ({'m1':0},{'f_n':-1},{'mh':float('nan')},{'k11':float('inf')}):
            with self.assertRaises(ValueError):
                nucleon_cross_section(**kw)

    def test_invalid_fraction(self):
        for xi in (-.01,1.1,float('nan')):
            with self.assertRaises(ValueError):
                density_rescaled_cross_section(1.,xi)


if __name__ == '__main__':
    unittest.main(verbosity=2)
