"""Independent antenna and subtraction tests. Not a massive-QCD certification."""
import itertools
import math
import unittest
import numpy as np
import sympy as sp
import antenna_normalization_audit as a

class AntennaAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit=a.symbolic_audit()
        cls.gg=a.laurent_coefficients('ggg')
        cls.qq=a.laurent_coefficients('gqq')

    def test_01_exact_symbolic_identities(self):
        self.assertTrue(self.audit['all_exact_zero'])
        self.assertTrue(all(v=='0' for v in self.audit['identities'].values()))

    def test_02_dirichlet_moment_against_gamma(self):
        for shifts in ((2,0,0),(2,2,0),(1,1,1),(3,1,0)):
            for e in (-1.,-2.):
                base=math.gamma(1-e)**3/math.gamma(1-3*e)
                derived=float(a.dirichlet_rational(*shifts).subs(a.E,e))*base
                reference=math.prod(math.gamma(v-e) for v in shifts)/math.gamma(sum(shifts)-3*e)
                self.assertAlmostEqual(derived/reference,1.,delta=2e-14)

    def test_03_ggg_differential_normalization(self):
        # Independent color-summed, already-symmetrized matrix elements:
        # T0=lambda^2(N^2-1)Q^4/4; T3=lambda^2 gs^2(N^2-1)N Q^2 P/(6xyz).
        Q=37.;gs2=4*math.pi*.17;N=3
        for x,y in ((.2,.3),(.05,.1),(.42,.23)):
            z=1-x-y;P=1+x**4+y**4+z**4
            T0=(N*N-1)*Q**4/4
            T3=gs2*(N*N-1)*N*Q*Q*P/(6*x*y*z)
            phase_ratio=Q*Q/(16*math.pi**2)
            measured=T3/T0*phase_ratio
            expected=.17/math.pi/2*P/(x*y*z)
            self.assertAlmostEqual(measured/expected,1.,delta=1e-14)

    def test_04_full_source_ggg_shape(self):
        for x,y in ((.2,.3),(.01,.1),(.32,.31)):
            z=1-x-y;P=1+x**4+y**4+z**4
            # a/2 * N * source density becomes a/2 * P/(xyz) at N=3.
            self.assertAlmostEqual(3*a.real_density(x,y,0.,'ggg')/(P/(x*y*z)),1.,delta=2e-14)

    def test_05_light_pair_phase_and_color_normalization(self):
        z=.37;u,w=np.polynomial.legendre.leggauss(12);u=(u+1)/2;w=w/2
        x=(1-z)*u;y=(1-z)*(1-u)
        val=.5*(1-z)*np.sum(w*a.real_density(x,y,0.,'gqq'))
        self.assertAlmostEqual(val/((1-z)**3/(3*z)),1.,delta=2e-14)

    def test_06_ggg_poles(self):
        self.assertEqual(self.gg[-2],2);self.assertEqual(self.gg[-1],sp.Rational(11,3))

    def test_07_ggg_finite_and_higher_orders(self):
        # Separately transcribed Eq. (4.6) comparison targets.
        e0=sp.Rational(73,6)-7*sp.pi**2/6
        e1=sp.Rational(451,12)-77*sp.pi**2/36-50*sp.zeta(3)/3
        e2=sp.Rational(2729,24)-511*sp.pi**2/72-275*sp.zeta(3)/9-71*sp.pi**4/720
        for p,r in enumerate((e0,e1,e2)):self.assertEqual(sp.simplify(self.gg[p]-r),0)

    def test_08_light_pair_poles(self):
        self.assertEqual(self.qq[-2],0);self.assertEqual(self.qq[-1],-sp.Rational(2,3))

    def test_09_light_pair_finite_and_higher_orders(self):
        e0=-sp.Rational(7,3)
        e1=-sp.Rational(15,2)+7*sp.pi**2/18
        e2=-sp.Rational(93,4)+49*sp.pi**2/36+50*sp.zeta(3)/9
        for p,r in enumerate((e0,e1,e2)):self.assertEqual(sp.simplify(self.qq[p]-r),0)

    def test_10_pole_cancellation_for_arbitrary_colors_flavors(self):
        for N,nf in ((2,0),(3,3),(3,5),(5,7)):
            V=a.source_virtual_coefficients(N,nf)
            for p in (-2,-1):self.assertEqual(sp.simplify(N*self.gg[p]+nf*self.qq[p]+V[p]),0)

    def test_11_integrated_finite_no_pi_squared(self):
        N,nf=sp.symbols('N nf');V=a.source_virtual_coefficients(N,nf)
        total=sp.simplify(N*self.gg[0]+nf*self.qq[0]+V[0])
        self.assertEqual(total,sp.Rational(73,6)*N-sp.Rational(7,3)*nf)
        self.assertFalse(total.has(sp.pi))

    def test_12_wrong_double_real_normalization_leaves_poles(self):
        V=a.source_virtual_coefficients(3,3)
        self.assertEqual(2*3*self.gg[-2]+V[-2],6)
        self.assertNotEqual(2*3*self.gg[-1]+3*self.qq[-1]+V[-1],0)

    def test_13_evanescent_quark_term_is_finite(self):
        wrong=2*a.dirichlet_rational(3,1,0)
        correction=sp.limit(a.integrated_rational('gqq')-wrong,a.E,0)
        self.assertEqual(correction,sp.Rational(1,3))
        self.assertEqual(self.qq[0]-correction,-sp.Rational(8,3))

    def test_14_direct_2d_vs_analytic_regulator_integrals(self):
        for e in (-1.,-2.,-3.):
            for channel in ('ggg','gqq'):
                d=a.direct_regulated_integral(e,channel)
                g=a.gamma_regulated_integral(e,channel)
                self.assertAlmostEqual(d/g,1.,delta=2e-13)

    def test_15_direct_quadrature_node_refinement(self):
        for channel in ('ggg','gqq'):
            low=a.direct_regulated_integral(-2.,channel,16)
            high=a.direct_regulated_integral(-2.,channel,48)
            self.assertAlmostEqual(low/high,1.,delta=3e-13)

    def test_16_bose_symmetry_of_independent_tree(self):
        xyz=(.12,.23,.65)
        reference=a.real_density(xyz[0],xyz[1],0.,'ggg')
        for x,y,z in itertools.permutations(xyz):
            self.assertAlmostEqual(a.real_density(x,y,0.,'ggg')/reference,1.,delta=2e-14)

    def test_17_resolved_real_probabilities_positive(self):
        for channel in ('ggg','gqq'):
            for x,y in ((.1,.2),(.32,.31),(.001,.6)):
                self.assertGreater(a.real_density(x,y,0.,channel),0.)

    def test_18_three_to_five_flavor_bookkeeping(self):
        Q,mu,mb,mc=23.,46.,3.1,.75
        L=math.log(mu*mu/(Q*Q));ell=math.log(Q*Q/(mb*mb))+math.log(Q*Q/(mc*mc))
        expected=73/4-7*3/6-ell/3+23/6*L
        self.assertAlmostEqual(a.universal_veto(Q,mu,mb,mc),expected,delta=1e-13)

    def test_19_universal_matches_archived_assembly(self):
        import decay_assembly_audit as old
        import heavy_quark_thermal as h
        for Q in (20.,23.,40.,65.,80.):
            for scale in (.5,1.,2.):
                mu=Q*scale
                result=a.universal_veto(Q,mu,h.running_mass('b',mu),h.running_mass('c',mu))
                self.assertAlmostEqual(result,old.universal(Q,scale),delta=1e-13)

    def test_20_thermal_universal_reproduces_existing_piece(self):
        import heavy_quark_thermal as h
        w=h.equilibrium_weights(.5)
        effective=sum(w[p]*a.thermal_universal(.5,p) for p in w)
        self.assertAlmostEqual(effective,1.46447344241e-17,delta=8e-29)

    def test_21_thermal_variables_and_lower_temperature(self):
        for T in (.5,1/3):
            for p in ('11','12','22'):
                w=a.thermal_universal(T,p);Q=a.thermal_universal(T,p,method='Q')
                self.assertAlmostEqual(w/Q,1.,delta=2e-11)

    def test_22_heavy_top_matching_added_once(self):
        for nf in (0,3,5):
            universal=sp.Rational(73,4)-sp.Rational(7,6)*nf
            self.assertEqual(universal+sp.Rational(11,2),sp.Rational(95,4)-sp.Rational(7,6)*nf)

    def test_23_invalid_arguments_rejected(self):
        for f in (lambda:a.dirichlet_rational(-1,0,1),lambda:a.dirichlet_rational(True,1,1),
                  lambda:a.laurent_coefficients('wrong'),lambda:a.laurent_coefficients('ggg',3),
                  lambda:a.real_density(.8,.4,0.,'ggg'),lambda:a.gamma_regulated_integral(0.,'ggg'),
                  lambda:a.direct_regulated_integral(-.5,'gqq'),lambda:a.universal_veto(0,1,1,1),
                  lambda:a.universal_veto(20,float('nan'),1,1)):
            with self.assertRaises(ValueError):f()

    def test_24_no_full_massive_rate_claim(self):
        with self.assertRaises(NotImplementedError):a.complete_massive_NLO_rate()

if __name__=='__main__':unittest.main()
