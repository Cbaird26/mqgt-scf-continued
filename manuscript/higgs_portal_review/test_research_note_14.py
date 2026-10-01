"""Internal regression tests for conditional Research Note 14, not an experimental or external validation."""
import math
import unittest


def kallen(x, y, z):
    return (x - y - z)**2 - 4*y*z


def fermion_width(m2, m1, mf, nc, k12, mh=125.0, gammah=0.0041, n=8192):
    """Composite Simpson integral of tree-level s2 -> s1 f fbar via h*."""
    if m2 - m1 <= 2*mf:
        return 0.0
    if n < 2 or n % 2:
        raise ValueError('Simpson n must be even')
    low, high = 4*mf**2, (m2-m1)**2
    factor = nc*k12**2*mf**2/(128*math.pi**3*m2**3)
    def kernel(q):
        phase = max(0., kallen(m2**2, m1**2, q))
        beta2 = max(0., 1 - 4*mf**2/q)
        return factor*q*math.sqrt(phase)*beta2**1.5 / ((q-mh**2)**2+(mh*gammah)**2)
    step = (high-low)/n
    ans = kernel(low)+kernel(high)
    for i in range(1,n):
        ans += (4 if i%2 else 2)*kernel(low+i*step)
    return ans*step/3


class Note14Checks(unittest.TestCase):
    def test_tau_partial_width_against_separately_integrated_value(self):
        w = fermion_width(25.,10.,1.77686,1,.001)
        self.assertAlmostEqual(w/1.151478228056e-15,1.0,delta=.00005)

    def test_numerical_refinement(self):
        w1=fermion_width(25.,10.,1.77686,1,.001,n=4096)
        w2=fermion_width(25.,10.,1.77686,1,.001,n=8192)
        self.assertLess(abs(w1/w2-1),.00005)

    def test_closed_three_s1_threshold(self):
        self.assertLess(25.,3*10.)

    def test_positive_mass_matrix(self):
        a,b,gamma=362.5,362.5,262.5
        self.assertGreater(a*b-gamma**2,0)
        self.assertEqual((a+b)/2-math.sqrt(((a-b)/2)**2+gamma**2),100.)
        self.assertEqual((a+b)/2+math.sqrt(((a-b)/2)**2+gamma**2),625.)

    def test_lifetime_and_boost(self):
        w=fermion_width(25.,10.,1.77686,1,.001)
        ctau=1.973269804e-16/w
        e2=(125.**2+25.**2-10.**2)/(2*125.)
        bg=math.sqrt(e2**2-25.**2)/25.
        self.assertAlmostEqual(ctau,.171368,delta=.00003)
        self.assertAlmostEqual(bg,2.38266,delta=.00003)
        self.assertAlmostEqual(math.exp(-1/(bg*ctau)),.08637,delta=.00003)

    def test_equal_portals_remove_offdiagonal_higgs_channel(self):
        kphi=ke=.002
        theta=math.pi/4
        self.assertAlmostEqual((ke-kphi)*math.sin(theta)*math.cos(theta),0)


if __name__=='__main__':
    unittest.main(verbosity=2)
