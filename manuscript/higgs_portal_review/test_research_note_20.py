"""Research Note 20: toy KINEMATIC kernel checks only.

Does not load third-party Omnes data or predict hadronic widths or detectors.
"""
import math
import unittest

M1, M2, MH, GH, V, K12 = 10.0, 25.0, 125.0, 0.0041, 246.0, 0.001
S_MAX = (M2 - M1) ** 2
MPI, MK = 0.134, 0.497  # upstream code's approximate reference masses


def triangle(a, b, s):
    return (a - b - s) ** 2 - 4 * b * s


def kernel(s):
    if not (0 <= s <= S_MAX):
        raise ValueError('outside physical interval')
    root = math.sqrt(max(0.0, triangle(M2*M2, M1*M1, s)))
    d = (MH*MH - s)**2 + (MH*GH)**2
    return V*V*K12*K12*root*math.sqrt(s)/(16*math.pi**2*M2**3*d)


def simpson(f, a, b, n=32768):
    if not (0 <= a <= b <= S_MAX and n > 0 and n % 2 == 0):
        raise ValueError('invalid integration interval or grid')
    if a == b:
        return 0.0
    h = (b - a)/n
    z = f(a) + f(b)
    z += 4*sum(f(a + (2*j - 1)*h) for j in range(1, n//2 + 1))
    z += 2*sum(f(a + 2*j*h) for j in range(1, n//2))
    return z*h/3


def fraction(a, b):
    return simpson(kernel, a, b)/simpson(kernel, 0.0, S_MAX)


class KernelChecks(unittest.TestCase):
    def test_kinematic_endpoints_and_positive(self):
        self.assertEqual(kernel(0), 0)
        self.assertEqual(kernel(S_MAX), 0)
        self.assertTrue(all(kernel(S_MAX*j/100)>0 for j in range(1, 100)))

    def test_invalid_inputs_rejected(self):
        for x in (-1, S_MAX+1):
            with self.assertRaises(ValueError):
                kernel(x)

    def test_fraction_additivity(self):
        # Composite Simpson has residual error near the sqrt endpoint.
        self.assertAlmostEqual(fraction(0, 4)+fraction(4, S_MAX), 1, delta=1e-7)

    def test_2gev_coverage_not_mass_fraction(self):
        f = fraction(0, 4)
        self.assertTrue(0 < f < 0.05)
        self.assertNotAlmostEqual(f, 2/15, places=3)
        self.assertNotAlmostEqual(f, 4/225, places=3)

    def test_source_threshold_windows(self):
        self.assertTrue(0 < fraction(4*MK**2, 4)
                        < fraction(4*MPI**2, 4) < fraction(0, 4))

    def test_synthetic_spectral_counterexample(self):
        # Arbitrary positive synthetic spectral multiplier 1e8 below 2 GeV;
        # demonstrates why kernel-weight fraction != physical decay fraction.
        low = simpson(kernel, 4*MPI**2, 4)
        high = simpson(kernel, 4, S_MAX)
        self.assertGreater(low*1e8/(low*1e8+high), 0.99)

    def test_analytic_lambda_factorization(self):
        for s in (0, 1, 4, 100, 200, 225):
            want = ((M2+M1)**2 - s)*((M2-M1)**2 - s)
            self.assertAlmostEqual(triangle(M2*M2, M1*M1, s), want, places=6)


if __name__ == '__main__':
    print('f_W(0 <= sqrt(s) <= 2 GeV) =', f'{fraction(0, 4):.10f}')
    print('f_W(pi reference threshold -> 2 GeV) =', f'{fraction(4*MPI**2, 4):.10f}')
    print('f_W(K reference threshold -> 2 GeV) =', f'{fraction(4*MK**2, 4):.10f}')
    unittest.main()
