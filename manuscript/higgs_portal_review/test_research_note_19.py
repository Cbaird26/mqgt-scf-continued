"""Internal algebra/contract checks only. Does not execute third-party hadronic code or QCD."""
import math
import unittest

PI = math.pi
MPI, MK = 0.134, 0.497  # Reference-isospin masses from audited upstream code
MAX_PROVISIONAL_MASS = 2.0
M2, M1 = 25.0, 10.0


def pair_width(mass, daughter_mass, form_factor, multiplicity):
    """Paper Eq. (5.1): reference form-factor amplitude [GeV]."""
    if not (math.isfinite(mass) and mass > 0 and math.isfinite(daughter_mass)
            and daughter_mass > 0 and math.isfinite(form_factor)
            and multiplicity in (3, 4)):
        raise ValueError("Invalid input")
    if mass <= 2 * daughter_mass:
        return 0.0
    return multiplicity * math.sqrt(1 - 4 * daughter_mass**2 / mass**2) * (form_factor**2) / (16 * PI * mass)


def covered_mass_max(grid_max, model_splitting=M2-M1):
    if not (math.isfinite(grid_max) and grid_max > 0 and
            math.isfinite(model_splitting) and model_splitting > 0):
        raise ValueError("Unverified upstream grid / model splitting")
    return min(grid_max, MAX_PROVISIONAL_MASS, model_splitting)


class ContractTests(unittest.TestCase):
    def test_pi_prefactor_matches_upstream(self):
        mass, form = 1.5, .1
        upstream = (3/16) * math.sqrt(1-4*MPI**2/mass**2) * form**2/(PI*mass)
        self.assertAlmostEqual(pair_width(mass, MPI, form, 3), upstream, places=16)

    def test_kaon_prefactor_matches_upstream(self):
        mass, form = 1.5, .1
        upstream = .25 * math.sqrt(1-4*MK**2/mass**2) * form**2/(PI*mass)
        self.assertAlmostEqual(pair_width(mass, MK, form, 4), upstream, places=16)

    def test_both_pair_thresholds(self):
        for daughter, a in ((MPI,3),(MK,4)):
            self.assertEqual(pair_width(2*daughter, daughter, 1.0, a), 0)
            self.assertEqual(pair_width(2*daughter-.01, daughter, 1.0, a), 0)
            self.assertGreater(pair_width(2*daughter+.01, daughter, 1.0, a), 0)

    def test_homogeneous_current_scaling(self):
        self.assertAlmostEqual(pair_width(1.2, MPI, .13, 3)/pair_width(1.2, MPI, .13*.5, 3), 4)

    def test_no_paper_extrapolation_to_fifteen_gev(self):
        self.assertEqual(covered_mass_max(15.0), 2.0)
        self.assertEqual(covered_mass_max(1.7), 1.7)
        self.assertEqual(covered_mass_max(30, .9), .9)

    def test_invalid_grid_and_width_inputs_fail(self):
        for bad in (float('nan'), float('inf'), -1.0, 0.0):
            with self.assertRaises(ValueError):
                covered_mass_max(bad)
        with self.assertRaises(ValueError):
            pair_width(1.4, MPI, float('nan'), 3)
        with self.assertRaises(ValueError):
            pair_width(1.4, MPI, 1., 6)


if __name__ == '__main__':
    unittest.main(verbosity=2)
