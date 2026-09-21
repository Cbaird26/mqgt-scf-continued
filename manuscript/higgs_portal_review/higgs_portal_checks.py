"""Reproducibility checks for a conditional two-real-singlet Higgs portal.

The potential convention is V ⊃ (kappa_iH / 2) s_i^2 H†H.
These unit tests check tree-level algebra and illustrative numbers, NOT data.
Run: python -m unittest -v higgs_portal_checks.py
"""
import math
import unittest

V = 246.0  # GeV; illustrative
MH = 125.0  # GeV; illustrative
SM_WIDTH = 0.0041  # GeV; illustrative Standard Model prediction
ATLAS_2023_OBSERVED = 0.107  # 95% CL under published assumptions


def portal_matrix(kappa_phi, kappa_e, angle):
    c, s = math.cos(angle), math.sin(angle)
    return (kappa_phi * c*c + kappa_e * s*s,
            (kappa_e - kappa_phi) * s*c,
            kappa_phi * s*s + kappa_e * c*c)


def identical_width(kappa, mass, mh=MH, v=V):
    if mass < 0 or mh <= 0 or v <= 0:
        raise ValueError("Nonphysical mass or scale")
    if 2 * mass >= mh:
        return 0.0
    return v*v*kappa*kappa/(32*math.pi*mh) * math.sqrt(1 - 4*mass*mass/(mh*mh))


def mixed_width(k12, m1, m2, mh=MH, v=V):
    if m1 < 0 or m2 < 0 or mh <= 0 or v <= 0:
        raise ValueError("Nonphysical mass or scale")
    if m1 + m2 >= mh:
        return 0.0
    phase = (1-(m1+m2)**2/mh**2)*(1-(m1-m2)**2/mh**2)
    return v*v*k12*k12/(16*math.pi*mh)*math.sqrt(max(0.0, phase))


def invisible_fraction(new_width, sm_width=SM_WIDTH):
    if new_width < 0 or sm_width <= 0:
        raise ValueError("Widths must be physical")
    return new_width/(sm_width+new_width)


class PortalChecks(unittest.TestCase):
    def test_portal_trace_invariance(self):
        for angle in (0, 0.17, 0.4, math.pi/4, 1.2):
            k1, k12, k2 = portal_matrix(.01, -.003, angle)
            self.assertAlmostEqual(k1*k1 + 2*k12*k12 + k2*k2,
                                   .01**2 + (-.003)**2, places=15)

    def test_massless_width_invariant(self):
        kphi, ke = .01, .002
        for angle in (0, .23, .7):
            k1, k12, k2 = portal_matrix(kphi, ke, angle)
            total = (identical_width(k1, 0) + mixed_width(k12, 0, 0)
                     + identical_width(k2, 0))
            expected = V*V*(kphi*kphi+ke*ke)/(32*math.pi*MH)
            self.assertAlmostEqual(total, expected, places=15)

    def test_equal_portals_no_transition(self):
        for angle in (0, .5, 1):
            self.assertAlmostEqual(portal_matrix(.01, .01, angle)[1], 0)

    def test_example_single_and_double(self):
        per = identical_width(.01, 10)
        self.assertAlmostEqual(1000*per, .475366954, delta=0.000001)
        self.assertAlmostEqual(invisible_fraction(per), .103897012, delta=0.000001)
        self.assertAlmostEqual(invisible_fraction(2*per), .188236784, delta=0.000001)
        self.assertLess(invisible_fraction(per), ATLAS_2023_OBSERVED)
        self.assertGreater(invisible_fraction(2*per), ATLAS_2023_OBSERVED)

    def test_illustrative_joint_contour(self):
        factor = identical_width(1, 10)
        cap = math.sqrt(ATLAS_2023_OBSERVED / (1-ATLAS_2023_OBSERVED)
                        * SM_WIDTH / factor)
        self.assertAlmostEqual(cap, .01016585, delta=1e-7)

    def test_thresholds(self):
        self.assertEqual(identical_width(.01, 62.5), 0)
        self.assertEqual(mixed_width(.01, 60, 65), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
