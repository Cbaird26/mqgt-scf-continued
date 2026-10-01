"""Internal synthetic inequalities only: not a QCD result, detector simulation, or experimental test."""
import math
import unittest

M1, M2, MH, GH, V, K12 = 10.0, 25.0, 125.0, 0.0041, 246.0, 0.001
HBARC = 1.973269804e-16
LEPTONS = 1.15650e-15

def lam(a, b, c):
    return (a - b - c)**2 - 4*b*c

def weight(s):
    if not 0.0 <= s <= (M2-M1)**2:
        raise ValueError('out of kinematic range')
    val = max(lam(M2*M2, M1*M1, s), 0.0)
    return V*V*K12*K12*math.sqrt(val)*math.sqrt(s) / (
        16*math.pi**2*M2**3*((MH*MH-s)**2 + MH*MH*GH*GH))

def simpson(fun, left, right, n=2000):
    if n < 2 or n % 2:
        raise ValueError('even integration step count required')
    h = (right-left)/n
    return h/3 * (fun(left)+fun(right) +
                   4*sum(fun(left+i*h) for i in range(1,n,2)) +
                   2*sum(fun(left+i*h) for i in range(2,n,2)))

def partial_width(channel_intervals):
    """Each entry is (lower_s, upper_s, nonnegative SYNTHETIC unit-normalized width)."""
    total=0.0
    for lo,hi,rate in channel_intervals:
        if not (0 <= lo < hi <= (M2-M1)**2) or not math.isfinite(rate) or rate < 0:
            raise ValueError('invalid synthetic interval or rate')
        total += simpson(weight,lo,hi)*rate
    return total

class Note18Tests(unittest.TestCase):
    def test_kinematic_nonnegative(self):
        for i in range(101):
            self.assertGreaterEqual(weight(225*i/100),0)
    def test_partial_channel_tightens_length_ceiling(self):
        synthetic=partial_width([(1,9,1e-8),(9,16,2e-8)])
        self.assertGreater(synthetic,0)
        self.assertLess(HBARC/(LEPTONS+synthetic), HBARC/LEPTONS)
    def test_missing_channels_do_not_form_lower_lifetime_bound(self):
        synthetic=partial_width([(1,9,1e-8)])
        assert synthetic>=0
        for extra in [0, 1e-15, 1e-12]:
            self.assertLessEqual(HBARC/(LEPTONS+synthetic+extra),HBARC/(LEPTONS+synthetic))
    def test_missing_mass_bins_disallow_full_inclusive_claim(self):
        low=partial_width([(1,16,1e-8)])
        high=partial_width([(16,225,1e-8)])
        both=partial_width([(1,225,1e-8)])
        self.assertAlmostEqual(low+high,both,delta=1e-5*both)
        self.assertLess(low,both)
    def test_invalid_synthetic_data_rejected(self):
        for bad in [[(0,226,1)],[(4,2,1)],[(1,2,-1)],[(1,2,float('nan'))]]:
            with self.assertRaises(ValueError): partial_width(bad)

if __name__=='__main__':
    unittest.main(verbosity=2)
