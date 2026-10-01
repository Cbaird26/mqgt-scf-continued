"""Unit checks of exact Z2 algebra and formal tree-level source elimination only."""
import unittest
from fractions import Fraction as Q
from photon_selection_rules import (is_z2_even, photon_contact_coefficients,
                                    integrate_h_tree, contact_cross_term,
                                    contact_cross_term_from_coefficients)


class CommonParityChecks(unittest.TestCase):
    def test_zero_and_pair_mononomials_are_even(self):
        for a,b in ((0,0),(2,0),(0,2),(1,1),(4,2)):
            self.assertTrue(is_z2_even(a,b))

    def test_single_odd_scalar_terms_are_forbidden(self):
        for a,b in ((1,0),(0,1),(3,0),(2,1)):
            self.assertFalse(is_z2_even(a,b))

    def test_external_em_field_does_not_change_parity(self):
        # F_mu_nu and a classical EM B-field are Z2-even.
        for a,b in ((1,0),(0,1),(1,1),(2,0)):
            self.assertEqual(is_z2_even(a,b), (a+b)%2==0)

    def test_reject_bad_monomials(self):
        for a,b in ((-1,0),(0,1.5),('1',0)):
            with self.assertRaises(ValueError):
                is_z2_even(a,b)


class HiggsMatchingChecks(unittest.TestCase):
    def test_integrate_out_h_exact_stationary(self):
        j, mh = Q(5,7), Q(13,4)
        hstar = j/(mh*mh)
        lagrangian_at_hstar = -mh*mh*hstar*hstar/2+j*hstar
        self.assertEqual(lagrangian_at_hstar,integrate_h_tree(j,mh))

    def test_cross_term_from_independent_subtraction(self):
        p=(Q(3,2),Q(4,3),Q(5,7),Q(1,100),Q(-1,200),Q(1,50),Q(3,7),Q(246),Q(125))
        self.assertEqual(contact_cross_term(*p),
                         contact_cross_term_from_coefficients(*p[:6],p[6],p[8]))

    def test_diagonal_and_offdiagonal_identical_portal_limit(self):
        c11,c12,c22=photon_contact_coefficients(Q(1,1000),Q(0),Q(1,1000),Q(2,3),Q(125))
        self.assertEqual(c12,0)
        self.assertEqual(c11,c22)

    def test_mixed_coefficient_relative_to_diagonal(self):
        c11,c12,c22=photon_contact_coefficients(Q(1,1000),Q(-1,1000),Q(1,1000),Q(2,3),Q(125))
        self.assertEqual(c12,-2*c11)
        self.assertEqual(c11,c22)

    def test_zero_photon_amplitude_gives_zero_contact(self):
        self.assertEqual(photon_contact_coefficients(Q(1),Q(2),Q(3),Q(0),Q(125)), (0,0,0))

    def test_no_pure_odd_vertex_generated_by_h_exchange(self):
        # Both source terms contain 0 or 2 odd singlets: their products have even parity.
        for a,b in ((0,0),(2,0),(1,1),(0,2),(4,0),(3,1),(2,2),(1,3),(0,4)):
            self.assertTrue(is_z2_even(a,b))

    def test_bad_mass_and_v(self):
        with self.assertRaises(ValueError):
            photon_contact_coefficients(1,2,3,4,0)
        with self.assertRaises(ValueError):
            contact_cross_term(1,1,1,1,1,1,1,0,125)


if __name__ == '__main__':
    unittest.main(verbosity=2)
