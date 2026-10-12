"""Executed tests for Note 51; algebra/numerics, not empirical validation."""
import math
import unittest
import numpy as np
import mpmath as mp
from scipy.integrate import quad
import leptonic_conversion_scattering as c

class LeptonicConversionTests(unittest.TestCase):
    def test_01_spin_trace_normalization_and_charge(self):
        # Independent Dirac-matrix spin contraction in metric (+---).
        I=np.eye(2); Z=np.zeros((2,2))
        pauli=(np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),
               np.array([[1,0],[0,-1]]))
        gamma=[np.block([[I,Z],[Z,-I]])]
        gamma.extend(np.block([[Z,s],[-s,Z]]) for s in pauli)
        slash=lambda p:p[0]*gamma[0]-sum(p[i]*gamma[i] for i in (1,2,3))
        q,mi,mj,m=18.,c.M2,c.M1,c.LEPTONS["tau"]
        Ei=(q*q+m*m-mi*mi)/(2*q); Ef=(q*q+m*m-mj*mj)/(2*q)
        pi=math.sqrt(Ei*Ei-m*m); pf=math.sqrt(Ef*Ef-m*m)
        for cosine in (-.7,.1,.8):
            k=np.array([Ei,0,0,pi]);kp=np.array([Ef,pf*math.sqrt(1-cosine**2),0,pf*cosine])
            t=2*m*m-2*(Ei*Ef-pi*pf*cosine)
            for sign in (-1,1):  # particle and antiparticle spin sums
                trace=np.trace((slash(kp)+sign*m*np.eye(4))@(slash(k)+sign*m*np.eye(4)))/2
                self.assertAlmostEqual(trace.real,4*m*m-t,delta=5e-13)
                self.assertAlmostEqual(trace.imag,0.,delta=1e-13)

    def test_02_t_endpoints_independent_high_precision(self):
        with mp.workdps(60):
            for m in c.LEPTONS.values():
                for q in (c.M2+m+.01,20.,40.):
                    mi,mj,mm,qq=map(mp.mpf,(c.M2,c.M1,m,q))
                    Ei=(qq**2+mm**2-mi**2)/(2*qq)
                    Ef=(qq**2+mm**2-mj**2)/(2*qq)
                    pi=mp.sqrt(Ei**2-mm**2);pf=mp.sqrt(Ef**2-mm**2)
                    reference=(2*mm**2-2*Ei*Ef-2*pi*pf,2*mm**2-2*Ei*Ef+2*pi*pf)
                    got=c.t_limits(q,c.M2,c.M1,m)
                    for a,b in zip(got,reference):
                        self.assertAlmostEqual(a/float(b),1.,delta=2e-11)

    def test_03_physical_momentum_transfer_domain(self):
        for m in c.LEPTONS.values():
            for q in (c.M2+m+.0001,15.,25.,70.):
                lo,hi=c.t_limits(q,c.M2,c.M1,m)
                self.assertLessEqual(lo,hi)
                self.assertLessEqual(hi,0.)
                self.assertGreaterEqual(lo,-q*q)

    def test_04_forward_reverse_identical_t_limits(self):
        for m in c.LEPTONS.values():
            a=c.t_limits(20.,c.M2,c.M1,m);b=c.t_limits(20.,c.M1,c.M2,m)
            np.testing.assert_allclose(a,b,rtol=2e-14,atol=0.)

    def test_05_integrated_propagator_vs_60_digit_quadrature(self):
        with mp.workdps(60):
            for m in c.LEPTONS.values():
                for q in (14.,20.,50.):
                    lo,hi=c.t_limits(q,c.M2,c.M1,m)
                    mh,ml=mp.mpf(c.MH),mp.mpf(m)
                    ref=mp.quad(lambda t:(4*ml**2-t)/(mh**2-t)**2,[mp.mpf(lo),mp.mpf(hi)])
                    val=c.t_integral(q,c.M2,c.M1,m)
                    self.assertAlmostEqual(val/float(ref),1.,delta=1e-13)

    def test_06_t_primitive_vs_CM_angle(self):
        for m in c.LEPTONS.values():
            for q in (14.,20.,50.):
                a=c.t_integral(q,c.M2,c.M1,m)
                b=c.t_integral_angular(q,c.M2,c.M1,m)
                self.assertAlmostEqual(a/b,1.,delta=2e-12)

    def test_07_contact_propagator_is_upper_bound(self):
        for m in c.LEPTONS.values():
            for q in (14.,20.,50.,100.):
                exact=c.t_integral(q,c.M2,c.M1,m)
                contact=c.t_integral(q,c.M2,c.M1,m,contact=True)
                self.assertLess(exact,contact)
                self.assertGreater(exact,0.)

    def test_08_contact_limit_large_mediator(self):
        m=c.LEPTONS["tau"]
        exact=c.t_integral(20.,c.M2,c.M1,m,mh=1e6)
        contact=c.t_integral(20.,c.M2,c.M1,m,mh=1e6,contact=True)
        self.assertAlmostEqual(exact/contact,1.,delta=1e-9)

    def test_09_reduced_kernel_detailed_balance(self):
        for m in c.LEPTONS.values():
            for q in (14.,20.,40.):
                a=c.kallen_initial(q*q,c.M2,m)*c.cross_section(q,c.M2,c.M1,m)
                b=c.kallen_initial(q*q,c.M1,m)*c.cross_section(q,c.M1,c.M2,m)
                self.assertAlmostEqual(a/b,1.,delta=5e-14)

    def test_10_initial_threshold_integrable(self):
        m=c.LEPTONS["tau"];q0=c.M2+m
        self.assertEqual(c.reduced_kernel(q0,c.M2,c.M1,m),0.)
        with self.assertRaises(ValueError):
            c.cross_section(q0,c.M2,c.M1,m)
        a=c.reduced_kernel(q0+1e-6,c.M2,c.M1,m)
        b=c.reduced_kernel(q0+1e-7,c.M2,c.M1,m)
        self.assertAlmostEqual(a/b,math.sqrt(10),delta=2e-5)
        self.assertGreater(c.cross_section(q0+1e-7,c.M2,c.M1,m),
                           c.cross_section(q0+1e-6,c.M2,c.M1,m))

    def test_11_endothermic_threshold(self):
        m=c.LEPTONS["mu"]
        self.assertEqual(c.cross_section(c.M2+m-.001,c.M1,c.M2,m),0.)
        E=c.stationary_threshold(c.M1,c.M2,m)
        self.assertAlmostEqual(E,1.6125+1.15*m,delta=2e-15)

    def test_12_tau_decay_closed_scattering_open(self):
        m=c.LEPTONS["tau"]
        self.assertLess(c.M2-c.M1,2*m)
        self.assertGreater(c.cross_section(15.,c.M2,c.M1,m),0.)

    def test_13_massless_yukawa_and_zero_coupling(self):
        self.assertEqual(c.matrix_element_sq(-2.,0.),0.)
        self.assertEqual(c.matrix_element_sq(-2.,.1,coupling=0.),0.)
        self.assertEqual(c.rate_MB(.5,c.M2,c.M1,.1,coupling=0.).value_GeV,0.)

    def test_14_coupling_sign_and_quadratic_scaling(self):
        a=c.rate_MB(.5,c.M2,c.M1,c.LEPTONS["tau"]).value_GeV
        b=c.rate_MB(.5,c.M2,c.M1,c.LEPTONS["tau"],coupling=-2*c.K12).value_GeV
        self.assertAlmostEqual(b/a,4.,delta=2e-13)

    def test_15_independent_thermal_q_angle_vs_w(self):
        for T in (.5,1/3):
            for m in c.LEPTONS.values():
                for mi,mj in ((c.M2,c.M1),(c.M1,c.M2)):
                    a=c.rate_MB(T,mi,mj,m).value_GeV
                    b=c.rate_MB(T,mi,mj,m,method="q-angle").value_GeV
                    self.assertAlmostEqual(a/b,1.,delta=5e-10)

    def test_16_sqrt_w_quadrature(self):
        for m in c.LEPTONS.values():
            a=c.rate_MB(.5,c.M2,c.M1,m).value_GeV
            b=c.rate_MB(.5,c.M2,c.M1,m,method="sqrt-w").value_GeV
            self.assertAlmostEqual(a/b,1.,delta=3e-11)

    def test_17_reaction_density_balance(self):
        for T in (.5,.4,1/3):
            for m in c.LEPTONS.values():
                d=c.rate_MB(T,c.M2,c.M1,m).value_GeV
                u=c.rate_MB(T,c.M1,c.M2,m).value_GeV
                n1,n2=c.number_density_MB(T,c.M1),c.number_density_MB(T,c.M2)
                self.assertAlmostEqual(n2*d/(n1*u),1.,delta=5e-13)

    def test_18_degeneracy_and_density_normalization(self):
        T=.5;m=c.LEPTONS["mu"]
        n=c.number_density_MB(T,m,4)
        direct=4/(2*math.pi**2)*quad(lambda p:p*p*math.exp(-math.hypot(p,m)/T),0.,30.)[0]
        self.assertAlmostEqual(n/direct,1.,delta=1e-10)
        self.assertEqual(c.G_LEPTON,4)

    def test_19_tail_bound_exceeds_observed_positive_tail(self):
        for m in c.LEPTONS.values():
            short=c.rate_MB(.5,c.M2,c.M1,m,w_max=12.)
            long=c.rate_MB(.5,c.M2,c.M1,m)
            diff=long.value_GeV-short.value_GeV
            self.assertGreater(diff,0.)
            self.assertLess(diff,short.omitted_tree_MB_tail_bound_GeV)
            self.assertLess(long.omitted_tree_MB_tail_bound_GeV/long.value_GeV,1e-30)

    def test_20_long_window_stability(self):
        for m in c.LEPTONS.values():
            a=c.rate_MB(.5,c.M2,c.M1,m,w_max=60.).value_GeV
            b=c.rate_MB(.5,c.M2,c.M1,m,w_max=90.).value_GeV
            self.assertAlmostEqual(a/b,1.,delta=1e-11)

    def test_21_FD_pointwise_bound(self):
        for T in (.5,1/3):
            for m in c.LEPTONS.values():
                low=c.FD_lower_factor(T,m)
                for E,E2 in ((m,m),(m+.1,m+2),(m+3,m+.2)):
                    ratio=1/((1+math.exp(-E/T))*(1+math.exp(-E2/T)))
                    self.assertGreaterEqual(ratio+1e-15,low)
                    self.assertLessEqual(ratio,1.)

    def test_22_FD_microscopic_reversibility(self):
        # Same CM energy conservation, full equilibrium FD and dilute scalar MB.
        q=16.;T=.5;m=c.LEPTONS["tau"]
        Es2=(q*q+c.M2**2-m*m)/(2*q)
        Es1=(q*q+c.M1**2-m*m)/(2*q)
        Ein,Eout=q-Es2,q-Es1
        f=lambda E:1/(math.exp(E/T)+1)
        forward=math.exp(-Es2/T)*f(Ein)*(1-f(Eout))
        reverse=math.exp(-Es1/T)*f(Eout)*(1-f(Ein))
        self.assertAlmostEqual(forward/reverse,1.,delta=5e-14)

    def test_23_conversion_conserves_total_number(self):
        terms=c.net_conversion_terms(3.,2.,5.,7.)
        self.assertEqual(sum(terms),0.)
        self.assertEqual(terms,(-11.,11.))

    def test_24_population_relaxation_eigenvalue(self):
        down,up=3.,.2
        matrix=np.array([[-up,down],[up,-down]])
        eig=sorted(np.linalg.eigvals(matrix))
        np.testing.assert_allclose(eig,[-3.2,0.],atol=1e-14,rtol=0.)

    def test_25_equilibrium_fixed_point(self):
        T=.5;down=3.;q=c.equilibrium_ratio(T)
        terms=c.net_conversion_terms(1.,q,down,q*down)
        self.assertEqual(terms,(0.,-0.))

    def test_26_moving_target_derivative(self):
        for T in (.4,.45):
            e=1e-5
            def r(t):q=c.equilibrium_ratio(t);return q/(1+q)
            deriv=(math.log(r(T*(1+e)))-math.log(r(T*(1-e))))/(2*e)
            self.assertAlmostEqual(deriv,c.target_log_slope_over_H(T),delta=1e-9)

    def test_27_inherited_decay_timescale_recovery(self):
        result=c.rates_at_temperature(.5)
        self.assertAlmostEqual(result["inherited_MB_decay_relaxation_over_H"],
                               .00115650416636,delta=1e-14)
        self.assertAlmostEqual(result["r2_equilibrium"],.0572145986119163,delta=3e-15)

    def test_28_rate_regressions_and_tau_dominance(self):
        expected=(1.7627736145388546,.703796890043111,.29186241695244924)
        for T,val in zip((.5,.4,1/3),expected):
            r=c.rates_at_temperature(T)
            self.assertAlmostEqual(r["scattering_relaxation_over_H"],val,delta=1e-10)
            self.assertGreater(r["tau_fraction_of_MB_scattering"],.97)
        r=c.rates_at_temperature(.5)
        self.assertLess(r["scattering_relaxation_over_H"],r["equilibrium_target_log_slope_over_H"])

    def test_29_stationary_diagnostic_not_kinetic_replacement(self):
        a=c.rate_MB(.5,c.M2,c.M1,c.LEPTONS["tau"]).value_GeV
        b=c.stationary_MB_rate(.5,c.M2,c.M1,c.LEPTONS["tau"])
        self.assertAlmostEqual(b/a,.9712959888874582,delta=3e-11)
        self.assertGreater(abs(a-b)/a,.01)

    def test_30_timescale_crossing_not_abundance(self):
        T=c.relaxation_crossing_temperature()
        self.assertAlmostEqual(T,.4335683445768584,delta=1e-10)
        r=c.rates_at_temperature(T)
        self.assertAlmostEqual(r["MB_scatter_plus_inherited_decay_relaxation_over_H"],1.,delta=1e-9)
        with self.assertRaises(NotImplementedError):
            c.complete_relic_density()

    def test_31_input_domains_fail_explicitly(self):
        for args in ((.2,c.M2,c.M1,.1),(.5,c.M2,c.M1,-.1),
                     (.5,c.M2,c.M1,100.),(float("nan"),c.M2,c.M1,.1)):
            with self.assertRaises(ValueError):c.rate_MB(*args)
        with self.assertRaises(ValueError):c.matrix_element_sq(1.,.1)
        with self.assertRaises(ValueError):c.rate_MB(.5,c.M2,c.M1,.1,method="FD")
        with self.assertRaises(ValueError):c.net_conversion_terms(-1,1,1,1)
        with self.assertRaises(ValueError):c.number_density_MB(.5,.1,0)

if __name__=="__main__":
    unittest.main()
