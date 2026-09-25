"""Note 15: standard-library reproducibility only; not empirical evidence."""
import math
import unittest

MH, V, GAMMA_H = 125.0, 246.0, 0.0041
M1, M2, K11, K22, K12 = 10.0, 25.0, 0.001, 0.001, -0.001
HBARC = 1.973269804e-16  # GeV m


def kallen(x, y, z):
    return (x-y-z)**2-4*y*z


def virtual_h_fermion_width(q, mf, nc=1):
    if q <= 4*mf**2: return 0.0
    return nc*mf**2*math.sqrt(q)/(8*math.pi*V**2)*(1-4*mf**2/q)**1.5


def differential_width(q, mf, nc=1):
    if not 4*mf**2 < q < (M2-M1)**2: return 0.0
    phase=math.sqrt(max(0.0,kallen(M2**2,M1**2,q)))
    propagator=(MH**2-q)**2+(MH*GAMMA_H)**2
    two_body=V**2*K12**2*phase/(16*math.pi*M2**3)
    return two_body*math.sqrt(q)*virtual_h_fermion_width(q,mf,nc)/(math.pi*propagator)


def simpson(f,a,b,n=8192):
    if n<2 or n%2: raise ValueError('n must be a positive even integer')
    d=(b-a)/n
    return (f(a)+f(b)+sum((4 if i%2 else 2)*f(a+i*d) for i in range(1,n)))*d/3


def leptonic_width(mf):
    if M2-M1 <=2*mf:return 0.0
    return simpson(lambda q:differential_width(q,mf),4*mf**2,(M2-M1)**2)


def pair_width(a,b):
    m={1:M1,2:M2}; k={(1,1):K11,(1,2):K12,(2,2):K22}[(a,b)]
    return V**2*k**2/(32*math.pi*MH)*math.sqrt(max(0.0,kallen(MH**2,m[a]**2,m[b]**2)))/MH**2*(2 if a!=b else 1)


def survival(distance,beta_gamma,partial_width_floor):
    return math.exp(-distance*partial_width_floor/(HBARC*beta_gamma))


class Note15Checks(unittest.TestCase):
    def test_spectral_factorization_matches_direct_matrix_element(self):
        mf=1.77686
        for q in (20.,40.,100.,180.):
            direct=K12**2*mf**2*q*math.sqrt(kallen(M2**2,M1**2,q))*(1-4*mf**2/q)**1.5/(128*math.pi**3*M2**3*((q-MH**2)**2+(MH*GAMMA_H)**2))
            self.assertAlmostEqual(differential_width(q,mf)/direct,1,places=12)
    def test_tau_reproduces_prior_note(self):
        self.assertAlmostEqual(leptonic_width(1.77686)/1.151478228056e-15,1,delta=0.00005)
    def test_lepton_floor(self):
        tau=leptonic_width(1.77686)
        floor=sum(leptonic_width(m) for m in (1.77686,0.1056583755,0.00051099895))
        self.assertGreater(floor,tau)
        self.assertAlmostEqual(HBARC/floor,0.1706244,delta=0.00005)
    def test_pair_decay_arithmetic(self):
        total=sum(pair_width(a,b) for a,b in ((1,1),(1,2),(2,2)))
        self.assertAlmostEqual(total,1.83466908415845e-05,delta=1e-13)
    def test_idealized_one_metre_survival_bounds(self):
        floor=sum(leptonic_width(m) for m in (1.77686,0.1056583755,0.00051099895))
        e12=(MH**2+M2**2-M1**2)/(2*MH)
        bg12=math.sqrt(e12**2-M2**2)/M2
        bg22=math.sqrt((MH/2)**2-M2**2)/M2
        self.assertAlmostEqual(survival(1,bg12,floor),0.085453267,delta=0.00005)
        self.assertAlmostEqual(survival(1,bg22,floor),0.07746924,delta=0.00005)

if __name__=='__main__':
    unittest.main(verbosity=2)
