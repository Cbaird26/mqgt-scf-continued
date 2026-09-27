"""Regression tests for Research Note 39; not physical-model validation."""
import math
import unittest
from coannihilation_leptons import (
    M1,M2,K11,K12,K22,MASS,sigma_s,thermal_pair_quad,thermal_pair_direct,
    tail_upper_bound,equilibrium_fractions,leptonic_pair_partial,
    conditional_leptonic_sigma_eff
)

class CoannihilationLeptonTests(unittest.TestCase):
    def test_11_reproduces_note36(self):
        self.assertAlmostEqual(leptonic_pair_partial(.5,"11"),9.73929725783516e-16,delta=6e-27)

    def test_pair_partial_reference_values(self):
        expected={"11":9.73929725783517e-16,"12":9.96829268711261e-16,"22":1.01059518369794e-15}
        for pair,val in expected.items():
            self.assertAlmostEqual(leptonic_pair_partial(.5,pair),val,delta=7e-27)

    def test_transformed_vs_direct_tau_all_pairs(self):
        for mi,mj,k in ((M1,M1,K11),(M1,M2,K12),(M2,M2,K22)):
            a=thermal_pair_quad(.5,mi,mj,k,MASS["tau"])[0]
            b=thermal_pair_direct(.5,mi,mj,k,MASS["tau"])
            self.assertAlmostEqual(a/b,1.0,delta=3e-11)

    def test_transformed_vs_direct_all_leptons_mixed(self):
        for mf in MASS.values():
            a=thermal_pair_quad(.5,M1,M2,K12,mf)[0]
            b=thermal_pair_direct(.5,M1,M2,K12,mf)
            self.assertAlmostEqual(a/b,1.0,delta=5e-8)

    def test_full_mb_equilibrium_fraction(self):
        r1,r2=equilibrium_fractions(.5)
        self.assertAlmostEqual(r2,0.0572145986119163,delta=2e-15)
        self.assertAlmostEqual(r1+r2,1.0,places=15)

    def test_exact_mb_weights(self):
        o=conditional_leptonic_sigma_eff(.5)
        self.assertAlmostEqual(o["weights"]["11"],0.88884431307049,delta=2e-14)
        self.assertAlmostEqual(o["weights"]["12"],0.107882176635187,delta=2e-14)
        self.assertAlmostEqual(o["weights"]["22"],0.0032735102943227,delta=2e-15)
        self.assertAlmostEqual(sum(o["weights"].values()),1.0,places=14)

    def test_conditional_effective_partial(self):
        o=conditional_leptonic_sigma_eff(.5)
        self.assertAlmostEqual(o["sigma_eff"],9.76520203072442e-16,delta=8e-27)
        self.assertAlmostEqual(o["sigma_eff"]/o["rates"]["11"],1.002659819512995,delta=2e-14)

    def test_effective_is_weighted_sum(self):
        o=conditional_leptonic_sigma_eff(.5)
        self.assertAlmostEqual(o["sigma_eff"],sum(o["pieces"].values()),delta=1e-29)

    def test_portal_sign_does_not_change_rate(self):
        for mf in MASS.values():
            a=thermal_pair_quad(.5,M1,M2,K12,mf)[0]
            b=thermal_pair_quad(.5,M1,M2,-K12,mf)[0]
            self.assertEqual(a,b)

    def test_tail_bounds_positive_tiny(self):
        for mi,mj,k in ((M1,M1,K11),(M1,M2,K12),(M2,M2,K22)):
            for mf in MASS.values():
                v=thermal_pair_quad(.5,mi,mj,k,mf)[0]
                t=tail_upper_bound(.5,mi,mj,k,mf)
                self.assertGreater(t,0.0)
                self.assertLess(t/v,1e-20)

    def test_cross_section_positive_above_threshold(self):
        for mi,mj,k in ((M1,M1,K11),(M1,M2,K12),(M2,M2,K22)):
            s=(mi+mj+1.0)**2
            self.assertGreater(sigma_s(s,mi,mj,k,MASS["tau"]),0.0)

    def test_zero_coupling_zero_cross_section(self):
        s=(M1+M2+1)**2
        self.assertEqual(sigma_s(s,M1,M2,0.0,MASS["tau"]),0.0)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):thermal_pair_quad(0,M1,M2,K12,MASS["tau"])
        with self.assertRaises(ValueError):thermal_pair_quad(.5,M1,M2,K12,-1)
        with self.assertRaises(ValueError):leptonic_pair_partial(.5,"21")
        with self.assertRaises(ValueError):sigma_s((M1+M2)**2-1,M1,M2,K12,MASS["tau"])

if __name__ == "__main__":unittest.main()
