"""Unit checks for illustrative H2 and Gaussian-noise equations.

No experiment is performed; this is not a microscopic scalar-EFT derivation.
Units in the bath toy are natural units, hbar=c=1.
Run: python -m unittest -v h2_audit_checks.py
"""
import math
import unittest


def planning_floor(delta, duration, separation):
    if not (0 <= delta < 1 and duration > 0 and separation > 0):
        raise ValueError("invalid planning inputs")
    return -math.log1p(-delta) / (duration * separation**2)


def bath_zero_frequency(k, damping, temperature, mass):
    if mass <= 0 or damping < 0 or temperature < 0:
        raise ValueError("requires positive mass and nonnegative noise")
    return 2 * damping * temperature / (k*k + mass*mass)**2


def point_path_rate(g, damping, temperature, mass, distance):
    if mass <= 0 or damping < 0 or temperature < 0 or distance < 0:
        raise ValueError("invalid bath parameters")
    return g*g*damping*temperature * (-math.expm1(-mass*distance)) / (4*math.pi*mass)


def radial_integral(mass, separation, kmax=800.0, intervals=40000):
    """Finite-cutoff radial integral of (1-cos(k.d))/(k^2+m^2)^2.

    Returns I = integral d^3k/(2pi)^3 (...) using angular average.
    Cutoff-tail <~1/(2 pi^2 kmax); not an experimental uncertainty.
    """
    if intervals % 2:
        raise ValueError("Simpson intervals must be even")
    h = kmax/intervals
    def fn(k):
        sinc = 1 if k*separation == 0 else math.sin(k*separation)/(k*separation)
        return k*k*(1-sinc)/(2*math.pi**2*(k*k+mass*mass)**2)
    return h/3*(fn(0)+fn(kmax)+4*sum(fn(h*i) for i in range(1, intervals, 2))
                +2*sum(fn(h*i) for i in range(2, intervals, 2)))


class H2AuditChecks(unittest.TestCase):
    def test_planning_floor(self):
        self.assertAlmostEqual(planning_floor(0.00115, 1e-6, 1e-3), 1.150661e9, delta=1e4)

    def test_floor_invalid_inputs(self):
        with self.assertRaises(ValueError):
            planning_floor(1.0, 1e-6, 1e-3)

    def test_noise_at_zero_frequency(self):
        self.assertAlmostEqual(bath_zero_frequency(0.0, 2.0, 3.0, 2.0), 12/16)

    def test_radial_integral(self):
        expected = -math.expm1(-1.0)/(8*math.pi)
        self.assertAlmostEqual(radial_integral(1.0, 1.0), expected, delta=0.00009)

    def test_rate_is_linear_at_short_distance(self):
        r1 = point_path_rate(1.0, 1.0, 1.0, 1.0, 0.001)
        r2 = point_path_rate(1.0, 1.0, 1.0, 1.0, 0.002)
        self.assertAlmostEqual(r2/r1, 2.0, delta=0.002)


if __name__ == '__main__':
    unittest.main(verbosity=2)
