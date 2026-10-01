"""Internal arithmetic tests for Research Note 16; not a hadronic calculation or experimental validation."""
import math
import unittest

MH, WIDTH_H, V, M1, M2, K12 = 125.0, 0.0041, 246.0, 10.0, 25.0, 0.001
HBARC = 1.973269804e-16 # GeV m
M_TAU, M_MU, M_E = 1.77686, 0.1056583755, 0.00051099895
QMAX = (M2-M1)**2


def kallen(x, y, z):
    return (x-y-z)**2-4*y*z


def denom(q2):
    return (MH*MH-q2)**2+(MH*WIDTH_H)**2


def virtual_lepton_width(q2, mass):
    if q2 <= 4*mass*mass:
        return 0.0
    return mass*mass*math.sqrt(q2)/(8*math.pi*V**2)*(1-4*mass*mass/q2)**1.5


def spectral_kernel(q2, virtual_width, contact=False):
    if q2 <= 0 or q2 >= QMAX:
        return 0.0
    q_lambda = kallen(M2*M2,M1*M1,q2)
    if q_lambda <= 0:
        return 0.0
    d = denom(0) if contact else denom(q2)
    return (V*V*K12*K12*math.sqrt(q_lambda)/(16*math.pi*M2**3)
            *math.sqrt(q2)*virtual_width(q2)/(math.pi*d))


def simpson(func, low=0.0, high=QMAX, n=8192):
    if n <= 0 or n%2:
        raise ValueError('even positive subdivisions required')
    h=(high-low)/n
    return (func(low)+func(high)+sum((4 if i%2 else 2)*func(low+i*h) for i in range(1,n)))*h/3


def leptonic_width():
    return sum(simpson(lambda q2, mass=m: spectral_kernel(q2,lambda x:virtual_lepton_width(x,mass))) for m in (M_E,M_MU,M_TAU))


def survival_from_ratio(r, bg, length=1.0):
    """r=Gamma_nonleptonic/Gamma_leptonic, for model branches with no extra interference."""
    return math.exp(-length*(1+r)*leptonic_width()/(HBARC*bg))


class Note16Checks(unittest.TestCase):
    def test_positive_window_and_propagator_bound(self):
        self.assertGreater(denom(0),denom(QMAX))
        self.assertAlmostEqual(denom(0)/denom(QMAX),1.029434242672748,places=13)

    def test_contact_bound_for_known_tau_spectrum(self):
        vw=lambda s:virtual_lepton_width(s,M_TAU)
        contact=simpson(lambda s:spectral_kernel(s,vw,contact=True))
        full=simpson(lambda s:spectral_kernel(s,vw))
        self.assertLessEqual(contact,full)
        self.assertLessEqual(full,contact*denom(0)/denom(QMAX))
        self.assertAlmostEqual(full,1.151478228e-15,delta=5e-20)

    def test_contact_bound_for_unknown_nonnegative_synthetic_spectra(self):
        for vw in (lambda s:math.sqrt(s),
                   lambda s:math.exp(-((math.sqrt(s)-8.0)/0.8)**2),
                   lambda s:math.sqrt(s)*max(0.,1.-100./s) if s>0 else 0.):
            contact=simpson(lambda s:spectral_kernel(s,vw,contact=True))
            full=simpson(lambda s:spectral_kernel(s,vw))
            self.assertGreater(contact,0)
            self.assertLessEqual(contact,full*(1+1e-12))
            self.assertLessEqual(full,contact*denom(0)/denom(QMAX)*(1+1e-12))

    def test_tau_upper_window_weight(self):
        vw=lambda s:virtual_lepton_width(s,M_TAU)
        full=simpson(lambda s:spectral_kernel(s,vw))
        above=simpson(lambda s:spectral_kernel(s,vw),low=100.,high=QMAX)
        self.assertAlmostEqual(above/full,0.7394097155,delta=2e-5)

    def test_unknown_hadronic_ratio_is_parameter_not_measurement(self):
        floor=leptonic_width()
        self.assertAlmostEqual(floor,1.15649868e-15,delta=5e-20)
        for r in (0,1,5,10):
            self.assertAlmostEqual(HBARC/((1+r)*floor),(HBARC/floor)/(1+r),places=13)

    def test_exponential_probability_not_acceptance(self):
        e2=(MH**2+M2**2-M1**2)/(2*MH)
        bg=math.sqrt(e2**2-M2**2)/M2
        self.assertAlmostEqual(survival_from_ratio(0,bg),0.085453354,delta=2e-6)
        self.assertAlmostEqual(survival_from_ratio(1,bg),survival_from_ratio(0,bg)**2,delta=1e-12)
        self.assertGreater(survival_from_ratio(0,bg),survival_from_ratio(1,bg))

    def test_rank_one_portal_identity(self):
        k11,k22,k12=.001,.001,-.001
        self.assertAlmostEqual(k11*k22-k12*k12,0,places=15)


if __name__=='__main__':
    unittest.main(verbosity=2)
