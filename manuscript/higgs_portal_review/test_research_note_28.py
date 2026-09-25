"""Math/regression tests only; not an abundance calculation."""
import math
import unittest
from thermal_population_gate import (
    MASS, M1, M2, K11, MH, GH, CM2_PER_GEV2, C_CM_S,
    LEPTON_FLOOR_S2, HBAR_GEV_S, sigma_v_ff_threshold,
    equilibrium_heavy_fraction, coannihilation_coefficients,
    heavier_lifetime_ceiling_seconds,
)

class ThermalPopulationGateTests(unittest.TestCase):
    def test_zero_for_closed_channel(self):
        self.assertEqual(sigma_v_ff_threshold(mf=M1), 0)
        self.assertEqual(sigma_v_ff_threshold(mf=M1+1), 0)

    def test_zero_portal(self):
        self.assertEqual(sigma_v_ff_threshold(k=0), 0)

    def test_quadratic_portal_scaling(self):
        w=sigma_v_ff_threshold()
        self.assertAlmostEqual(sigma_v_ff_threshold(k=2*K11)/w,4)

    def test_color_multiplicity(self):
        self.assertAlmostEqual(sigma_v_ff_threshold(color=3)/sigma_v_ff_threshold(),3)

    def test_massless_limit_yukawa_suppressed(self):
        self.assertLess(sigma_v_ff_threshold(mf=MASS['electron']),sigma_v_ff_threshold(mf=MASS['muon']))

    def test_tau_threshold_expression(self):
        m=MASS['tau']
        independent=(K11*m)**2/(4*math.pi*((4*M1*M1-MH*MH)**2+(MH*GH)**2))*(1-m*m/M1**2)**1.5
        self.assertAlmostEqual(sigma_v_ff_threshold(),independent,delta=independent*1e-14)

    def test_partial_conversion_regression(self):
        s=sum(sigma_v_ff_threshold(mf=m) for m in MASS.values())
        self.assertAlmostEqual(s*CM2_PER_GEV2*C_CM_S,1.21027614498e-32,delta=1e-42)

    def test_heavy_fraction_reduces_with_x(self):
        self.assertGreater(equilibrium_heavy_fraction(20),equilibrium_heavy_fraction(25))

    def test_degenerate_equilibrium_case(self):
        self.assertAlmostEqual(equilibrium_heavy_fraction(20,m2=M1),0.5)

    def test_weights_sum_to_one(self):
        for x in (1,20,25,100):
            self.assertAlmostEqual(sum(coannihilation_coefficients(equilibrium_heavy_fraction(x))),1)

    def test_cross_weight_double_counts_ordered_pairs_once(self):
        self.assertAlmostEqual(coannihilation_coefficients(0.5)[1],0.5)

    def test_lifetime_ceiling_and_width_scaling(self):
        tau=heavier_lifetime_ceiling_seconds()
        self.assertAlmostEqual(tau,HBAR_GEV_S/LEPTON_FLOOR_S2)
        self.assertAlmostEqual(heavier_lifetime_ceiling_seconds(2*LEPTON_FLOOR_S2),tau/2)

    def test_invalid_inputs(self):
        for inp in (float('nan'),-1,0):
            with self.assertRaises(ValueError): equilibrium_heavy_fraction(inp)
            with self.assertRaises(ValueError): heavier_lifetime_ceiling_seconds(inp)
        for inp in (float('nan'),-1,1.01):
            with self.assertRaises(ValueError): coannihilation_coefficients(inp)
        with self.assertRaises(ValueError): sigma_v_ff_threshold(mchi=0)
        with self.assertRaises(ValueError): sigma_v_ff_threshold(mf=-1)

if __name__ == '__main__': unittest.main(verbosity=2)
