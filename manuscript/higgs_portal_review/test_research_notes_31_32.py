"""Notes 31-32: algebra and toy-trajectory regression; NOT physical validation.

Run from this directory with: python -m unittest test_research_notes_31_32 -v
These tests were staged while local execution was unavailable; do not claim
that this uploaded file passed until it has actually been executed.
"""
import math
import unittest
from conversion_history import GAMMA_LEP, mb_rates, evolve, rhs, kve_integral

class ConversionHistoryChecks(unittest.TestCase):
    def test_known_note31_q(self):
        self.assertAlmostEqual(mb_rates(20)['q'], .0606867676649, delta=2e-10)
    def test_known_note31_dilation(self):
        self.assertAlmostEqual(mb_rates(20)['d2'], .938176870693, delta=2e-10)
    def test_known_note31_eigenvalue(self):
        m=mb_rates(20)
        self.assertAlmostEqual(m['Lambda_H'], .00115650416636, delta=3e-12)
        self.assertAlmostEqual(m['Lambda'], m['A']+m['B'], delta=1e-35)
    def test_event_count_is_not_eigenvalue(self):
        m=mb_rates(20)
        self.assertAlmostEqual(m['B']/m['H'], 6.616892167e-5, delta=3e-12)
        self.assertGreater(m['Lambda'],m['B'])
    def test_detailed_balance_and_fixed_point(self):
        m=mb_rates(20)
        self.assertAlmostEqual(m['A']*m['r'],m['B']*(1-m['r']), delta=1e-35)
        self.assertAlmostEqual(rhs(20,m['r']),0.0,delta=1e-16)
    def test_exact_fixed_temperature_relaxation(self):
        m=mb_rates(20)
        y0=.2
        t=2/m['Lambda']
        solution=m['r']+(y0-m['r'])*math.exp(-m['Lambda']*t)
        self.assertAlmostEqual((solution-m['r'])/(y0-m['r']),math.exp(-2),places=12)
    def test_zero_width_freezes_fraction(self):
        history=evolve(width=0)
        self.assertTrue(all(y==history[0][1] for _,y in history))
    def test_deliberate_initial_equilibrium(self):
        self.assertAlmostEqual(evolve()[0][1],.2120425359054555,delta=2e-10)
    def test_note32_x20_trajectory(self):
        self.assertAlmostEqual(evolve()[200][1],.211998004152,delta=2e-10)
    def test_note32_x30_trajectory(self):
        self.assertAlmostEqual(evolve()[-1][1],.211868008080,delta=2e-10)
        self.assertAlmostEqual(mb_rates(30)['r'],.0134099205463,delta=2e-10)
    def test_two_integration_methods(self):
        self.assertAlmostEqual(evolve()[-1][1],evolve(method='exp-mid')[-1][1],delta=3e-10)
    def test_convergence_by_halving_step(self):
        self.assertAlmostEqual(evolve(steps=200)[-1][1],evolve(steps=400)[-1][1],delta=2e-10)
    def test_initial_conditions_matter(self):
        self.assertAlmostEqual(evolve(y0=0)[-1][1],7.18481159653e-5,delta=2e-10)
        self.assertAlmostEqual(evolve(y0=.5)[-1][1],.499490889347,delta=2e-10)
    def test_large_rate_midpoint_remains_a_fraction(self):
        hist=evolve(steps=200,method='exp-mid',width=GAMMA_LEP*1e6)
        self.assertTrue(all(0<=y<=1 for _,y in hist))
    def test_bad_parameters_fail_closed(self):
        for kwargs in ({'y0':1.1},{'x0':9},{'x1':31},{'steps':0},
                       {'width':-1},{'gstar':0},{'method':'bogus'}):
            with self.assertRaises(ValueError):
                evolve(**kwargs)
    def test_bessel_outside_domain_rejected(self):
        with self.assertRaises(ValueError):
            kve_integral(3,20)
        with self.assertRaises(ValueError):
            kve_integral(1,5)

if __name__ == '__main__':
    unittest.main()
