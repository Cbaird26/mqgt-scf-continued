"""Pure math software checks of Note 24's conditional Higgs pair envelope."""
import math
import unittest
from invisible_channel_envelope import (MH, SM_WIDTH, branching_envelope,
                                        conditional_invisible_width, pair_widths)


class EnvelopeTests(unittest.TestCase):
    def test_individual_rates_reproduce_note22(self):
        for got,old in zip(pair_widths(),(4.753669542e-6,9.487199838e-6,4.733488003e-6)):
            self.assertAlmostEqual(got/old,1,delta=3e-10)

    def test_sum_matches_note22(self):
        self.assertAlmostEqual(sum(pair_widths())/1.897435738e-5,1,delta=3e-10)

    def test_branching_matches_note22(self):
        self.assertAlmostEqual(branching_envelope()[1]/0.0046065733,1,delta=3e-8)

    def test_lower_bound_positive_and_below_upper(self):
        lo,hi=branching_envelope()
        self.assertTrue(0<lo<hi<1)

    def test_all_width_zero_returns_no_signal(self):
        self.assertEqual(branching_envelope((0.,0.,0.)),(0.,0.))

    def test_abstract_probability_corners(self):
        w=pair_widths()
        self.assertEqual(conditional_invisible_width(0,0),w[0])
        self.assertEqual(conditional_invisible_width(1,1),sum(w))

    def test_probability_monotonicity(self):
        self.assertLessEqual(conditional_invisible_width(.3,.4),conditional_invisible_width(.4,.4))
        self.assertLessEqual(conditional_invisible_width(.3,.4),conditional_invisible_width(.3,.5))

    def test_thresholds(self):
        self.assertEqual(pair_widths(m1=60,m2=65)[1],0)
        self.assertEqual(pair_widths(m1=63,m2=65)[0],0)
        self.assertEqual(pair_widths(m1=60,m2=65)[2],0)

    def test_zero_portals(self):
        self.assertEqual(pair_widths(k11=0,k12=0,k22=0),(0.,0.,0.))

    def test_portal_sign_invariance(self):
        a=pair_widths()
        b=pair_widths(k11=-.001,k12=.001,k22=-.001)
        self.assertEqual(a,b)

    def test_validation(self):
        for val in (-.1,1.01,math.nan,math.inf):
            with self.assertRaises(ValueError): conditional_invisible_width(val,0)
        with self.assertRaises(ValueError): branching_envelope(sm_width=0)
        with self.assertRaises(ValueError): pair_widths(m1=-1)
        with self.assertRaises(ValueError): branching_envelope(widths=(1,-1,2))

    def test_additional_unmodeled_width_changes_branching_bounds(self):
        widths=pair_widths()
        lo0,hi0=branching_envelope(widths)
        lo1,hi1=branching_envelope(widths,sm_width=SM_WIDTH+.001)
        self.assertLess(lo1,lo0)
        self.assertLess(hi1,hi0)


if __name__=='__main__':
    unittest.main()
