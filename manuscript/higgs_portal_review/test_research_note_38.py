"""Algebraic regression tests for Research Note 38; not physics validation."""
import unittest
from reaction_network_gate import (
    odd_number_delta,forward_event_rates,forward_total_number_loss,
    species_annihilation_terms,conversion_terms,sigma_eff,
    reduced_total_collision,full_total_collision,equilibrium_weights
)

class CollisionBookkeepingTests(unittest.TestCase):
    def test_conversion_stoichiometry_conserves_odd_number(self):
        self.assertEqual(odd_number_delta((0,1),(1,0)),0)
        self.assertEqual(odd_number_delta((1,0),(0,1)),0)

    def test_annihilation_stoichiometry_changes_by_two(self):
        for initial in ((2,0),(1,1),(0,2)):
            self.assertEqual(odd_number_delta(initial,(0,0)),-2)

    def test_identical_pair_event_factor(self):
        r=forward_event_rates(3.0,0.0,5.0,0.0,0.0)
        self.assertEqual(r["11"],22.5)
        self.assertEqual(forward_total_number_loss(3.0,0.0,5.0,0.0,0.0),-45.0)

    def test_mixed_pair_has_no_half_event_factor(self):
        r=forward_event_rates(2.0,3.0,0.0,7.0,0.0)
        self.assertEqual(r["12"],42.0)
        self.assertEqual(forward_total_number_loss(2.0,3.0,0.0,7.0,0.0),-84.0)

    def test_conversion_terms_cancel_in_total(self):
        for j in (-9.0,0.0,4.25):
            c1,c2=conversion_terms(j)
            self.assertEqual(c1+c2,0.0)

    def test_species_sum_matches_expanded_total(self):
        args=(2.0,3.0,1.0,1.5,5.0,7.0,11.0)
        c1,c2=species_annihilation_terms(*args)
        n1,n2,n1e,n2e,a,b,c=args
        expected=-(a*(n1*n1-n1e*n1e)+2*b*(n1*n2-n1e*n2e)+c*(n2*n2-n2e*n2e))
        self.assertAlmostEqual(c1+c2,expected)

    def test_effective_weights_sum_to_one(self):
        for r2 in (0.0,0.05784749058,0.5,1.0):
            self.assertAlmostEqual(sum(equilibrium_weights(r2)),1.0,places=15)

    def test_note28_weight_regression(self):
        w=equilibrium_weights(0.05784749058)
        self.assertAlmostEqual(w[0],0.8876513510,delta=2e-10)
        self.assertAlmostEqual(w[1],0.1090023168,delta=2e-10)
        self.assertAlmostEqual(w[2],0.00334633217,delta=2e-11)

    def test_equal_cross_sections_give_same_effective_cross_section(self):
        for r2 in (0.1,0.3,0.9):
            self.assertAlmostEqual(sigma_eff(r2,4.0,4.0,4.0),4.0,places=14)

    def test_chemical_equilibrium_reduction_identity(self):
        for r2 in (0.05,0.2,0.7):
            r1=1-r2
            N,Neq=12.0,3.0
            sv=(2.0,5.0,11.0)
            full=full_total_collision(r1*N,r2*N,r1*Neq,r2*Neq,*sv)
            red=reduced_total_collision(N,Neq,r2,*sv)
            self.assertAlmostEqual(full,red,places=12)

    def test_equilibrium_is_fixed_point_of_annihilation_terms(self):
        self.assertAlmostEqual(full_total_collision(2,3,2,3,5,7,11),0.0,places=15)

    def test_nonnegative_rates_deplete_above_equilibrium(self):
        self.assertLess(reduced_total_collision(10,2,.1,1,2,3),0.0)

    def test_invalid_inputs_fail(self):
        with self.assertRaises(ValueError): odd_number_delta((1,-1),(0,0))
        with self.assertRaises(ValueError): sigma_eff(1.2,1,1,1)
        with self.assertRaises(ValueError): forward_event_rates(-1,1,1,1,1)
        with self.assertRaises(ValueError): conversion_terms(float("nan"))

if __name__=="__main__":
    unittest.main()
