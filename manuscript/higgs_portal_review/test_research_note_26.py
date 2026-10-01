"""Restricted kinematic/regression tests; no external optical calculation."""
import math
import unittest
from optical_threshold_gate import (
    EV_TO_GEV, M1, M2, pair_threshold, two_photon_s, photon_pair_open,
    min_equal_head_on_photon_energy, monochromatic_max_s,
    free_vacuum_bilinear_cut, f2_wavespeed)


class KinematicGateTests(unittest.TestCase):
    def test_pair_cut_thresholds(self):
        self.assertEqual(pair_threshold(M1,M1),400.)
        self.assertEqual(pair_threshold(M1,M2),462.25)
        self.assertEqual(pair_threshold(M2,M2),529.)

    def test_unit_conversion(self):
        self.assertEqual(2*EV_TO_GEV,2e-9)
        self.assertEqual(20/EV_TO_GEV,2e10)

    def test_head_on_two_optical_photons(self):
        e=2*EV_TO_GEV
        self.assertAlmostEqual(two_photon_s(e,e,-1),4*e*e)
        self.assertAlmostEqual(math.sqrt(monochromatic_max_s(e)),4e-9)
        self.assertFalse(photon_pair_open(e,e,-1,M1,M1))

    def test_collinear_zero_invariant_s(self):
        self.assertEqual(two_photon_s(2e-9,7e-9,1),0.)
        self.assertFalse(photon_pair_open(2e-9,7e-9,1,M1,M1))

    def test_head_on_threshold_all_three_channels(self):
        for a,b in ((M1,M1),(M1,M2),(M2,M2)):
            e=min_equal_head_on_photon_energy(a,b)
            self.assertTrue(photon_pair_open(e,e,-1,a,b))
            self.assertFalse(photon_pair_open(.99*e,.99*e,-1,a,b))

    def test_angle_dependence(self):
        e=12.
        self.assertTrue(photon_pair_open(e,e,-1,M1,M1))
        self.assertFalse(photon_pair_open(e,e,1,M1,M1))

    def test_asymmetric_photons_threshold(self):
        self.assertTrue(photon_pair_open(5,20,-1,M1,M1))
        self.assertFalse(photon_pair_open(5,19,-1,M1,M1))

    def test_free_bilinear_cuts_match_pair_kinematics(self):
        for a,b in ((M1,M1),(M1,M2),(M2,M2)):
            self.assertEqual(free_vacuum_bilinear_cut(a,b),pair_threshold(a,b))

    def test_contact_vacuum_normalization_not_index(self):
        for z in (0.01,1.,1e8):
            self.assertEqual(f2_wavespeed(z),1.)

    def test_invalid_pair_masses(self):
        for bad in (0,-1,float('nan'),float('inf')):
            with self.assertRaises(ValueError):
                pair_threshold(bad,1)

    def test_invalid_photon_inputs(self):
        for args in ((0,1,-1),(1,-1,-1),(1,1,2),(1,1,-2),(float('nan'),1,0)):
            with self.assertRaises(ValueError):
                two_photon_s(*args)

    def test_invalid_f2_normalization(self):
        for bad in (0,-1,float('inf'),float('nan')):
            with self.assertRaises(ValueError):
                f2_wavespeed(bad)


if __name__=='__main__':
    unittest.main(verbosity=2)