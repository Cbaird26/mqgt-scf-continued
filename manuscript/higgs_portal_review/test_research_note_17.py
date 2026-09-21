"""Research Note 17: certified spectral-envelope arithmetic; NO hadronic model/data."""
import math
import unittest

MH, GH, V, M1, M2, K12 = 125.0, .0041, 246.0, 10.0, 25.0, -.001
HBARC = 1.973269804e-16  # GeV m
LEPTON_WIDTH = 1.15649868e-15  # GeV; internally crosschecked in Note 16
S_MAX = (M2-M1)**2


def kallen(a, b, c):
    return (a-b-c)**2-4*b*c


def weight(s):
    """Gamma_X = integral weight(s)*Gamma*_X(sqrt(s)) ds; GeV^-2."""
    if not (0 < s < S_MAX): return 0.
    disc = kallen(M2*M2, M1*M1, s)
    if disc <= 0: return 0.
    den = (MH*MH-s)**2+(MH*GH)**2
    return (V*V*K12*K12*math.sqrt(disc)*math.sqrt(s)
            /(16*math.pi**2*M2**3*den))


def simpson(fun, start, stop, steps=2048):
    if steps <= 0 or steps % 2: raise ValueError('even positive steps')
    h=(stop-start)/steps
    return (fun(start)+fun(stop)+sum((4 if i%2 else 2)*fun(start+h*i)
              for i in range(1, steps)))*h/3


def envelope_widths(bins):
    """Each (slo,shi,lower,upper) gives pointwise bounds on virtual width [GeV].
    Entire [0,S_MAX] must be covered with disjoint adjacent bins. Missing interval: reject.
    """
    if not bins: raise ValueError('no bins')
    prev=0.
    lower_total=upper_total=0.
    for slo,shi,lower,upper in bins:
        if not math.isclose(slo,prev,abs_tol=1e-11,rel_tol=0):
            raise ValueError('gap or overlap')
        if not (slo < shi <= S_MAX+1e-11 and 0 <= lower <= upper
                and all(math.isfinite(x) for x in (slo,shi,lower,upper))):
            raise ValueError('invalid interval or spectral bound')
        w=simpson(weight,slo,shi)
        lower_total += w*lower
        upper_total += w*upper
        prev=shi
    if not math.isclose(prev,S_MAX,abs_tol=1e-11,rel_tol=0):
        raise ValueError('incomplete spectral coverage')
    return lower_total,upper_total


def length_bracket(hadronic_lower,hadronic_upper):
    assert 0 <= hadronic_lower <= hadronic_upper
    return (HBARC/(LEPTON_WIDTH+hadronic_upper),
            HBARC/(LEPTON_WIDTH+hadronic_lower))


class SpectralContractChecks(unittest.TestCase):
    def test_physical_thresholds_and_scalar_quarkonia_in_window(self):
        mD,mB,mChiC0,mChiB0=1.86484,5.27965,3.41471,9.85944
        self.assertLess(mChiC0,2*mD)
        self.assertLess(mChiB0,2*mB)
        self.assertLess(2*mB,math.sqrt(S_MAX))

    def test_weight_nonnegative_and_vanish_at_boundaries(self):
        self.assertEqual(weight(0),0)
        self.assertEqual(weight(S_MAX),0)
        self.assertTrue(all(weight(j*S_MAX/100) >= 0 for j in range(101)))

    def test_constant_spectral_bounds_are_integrated(self):
        bins=[(0.,25.,.1,.2),(25.,100.,.2,.5),(100.,S_MAX,.25,.75)]
        # Completely SYNTHETIC GeV widths, not QCD estimates.
        lo,hi=envelope_widths(bins)
        synthetic=simpson(lambda s:weight(s)*.15,0,25)
        synthetic+=simpson(lambda s:weight(s)*.3,25,100)
        synthetic+=simpson(lambda s:weight(s)*.5,100,S_MAX)
        self.assertTrue(lo<synthetic<hi)

    def test_equal_bounds_reproduce_constant_spectrum(self):
        c=.001  # SYNTHETIC, not a hadronic prediction
        lo,hi=envelope_widths([(0.,S_MAX,c,c)])
        self.assertAlmostEqual(lo,hi,places=24)
        self.assertAlmostEqual(lo,c*simpson(weight,0,S_MAX),delta=abs(lo)*1e-12)

    def test_fails_open_for_gaps_overlap_negative_or_unknown(self):
        for bad in ([(0.,S_MAX-1,0,1)],
                    [(0.,10,0,1),(11,S_MAX,0,1)],
                    [(0.,100,0,1),(99,S_MAX,0,1)],
                    [(0.,S_MAX,-.01,1)],
                    [(0.,S_MAX,0,float('inf'))]):
            with self.assertRaises(ValueError): envelope_widths(bad)

    def test_lifetime_interval_is_reverse_order(self):
        low,high=length_bracket(LEPTON_WIDTH,10*LEPTON_WIDTH)
        self.assertAlmostEqual(low,HBARC/(11*LEPTON_WIDTH),places=12)
        self.assertAlmostEqual(high,HBARC/(2*LEPTON_WIDTH),places=12)
        self.assertLess(low,high)

    def test_zero_hadronic_information_retains_only_upper_length(self):
        lo,hi=length_bracket(0,1e-12)  # finite illustrative upper, not physical
        self.assertAlmostEqual(hi,HBARC/LEPTON_WIDTH,places=10)
        self.assertLess(lo,hi)


if __name__=='__main__': unittest.main(verbosity=2)
