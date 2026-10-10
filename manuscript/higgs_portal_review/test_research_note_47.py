"""Note47 source/normalization/analytic-continuation checks, not new-field validation."""
import hashlib,math,itertools,unittest
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.integrate import quad
import three_gluon_remainder as r
from three_gluon_reference import log_box,simplex_box
import gluon_loop_thermal as g
import heavy_quark_thermal as h

class ThreeGluonTests(unittest.TestCase):
    def test_inherited_source_bytes(self):
        for mod,sha in ((h,'40d51657a26fb20851be2bafa0ea6b3efe05ddfb'),
                        (g,'c49c6fab4baa2d9c01c64f9fd8c2fdb7f018d50c')):
            b=Path(mod.__file__).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha)

    def test_triangle_functions_high_precision(self):
        with mp.workdps(55):
            for t in (.001,.2,.9,1.1,4.,100.):
                tm=mp.mpc(t,'1e-24');f=mp.asin(mp.sqrt(tm))**2
                gg=mp.sqrt(1/tm-1)*mp.asin(mp.sqrt(tm))
                a,b=r.fg(complex(tm))
                self.assertLess(abs(a-complex(f)),2e-13)
                self.assertLess(abs(b-complex(gg)),2e-13)

    def test_box_against_three_dimensional_parameters(self):
        for S,T,U in ((.2,.3,.5),(.4,.7,.9)):
            val=r.box_j(*[complex(v,1e-24*v) for v in (S,T,U)])
            self.assertAlmostEqual(val.real,simplex_box(S,T,U),delta=2e-12)
            self.assertLess(abs(val.imag),2e-12)

    def test_box_against_log_integral_above_threshold(self):
        for S,T,U in ((1.,2.,3.),(8.,12.,20.),(80.,120.,200.),(.1,8.,30.)):
            val=r.box_j(*[complex(v,1e-24*v) for v in (S,T,U)])
            self.assertLess(abs(val-log_box(S,T,U)),2e-11)

    def test_box_symmetry(self):
        S,T,U=[complex(v,1e-24*v) for v in (8.,12.,20.)]
        self.assertLess(abs(r.box_j(S,T,U)-r.box_j(U,T,S)),2e-13)

    def test_heavy_limit_source_helicities(self):
        for x,y in ((.2,.3),(.15,.4)):
            z=1-x-y;expected=np.array([x*x,-y*y,z*z,1.])
            got=r.helicities(.004,x,y)
            np.testing.assert_allclose(got,expected,rtol=3e-4,atol=2e-8)

    def test_heavy_norm_not_half(self):
        x,y=.2,.3;z=1-x-y;P=1+x**4+y**4+z**4
        val=float(sum(abs(r.helicities(.004,x,y))**2))
        self.assertAlmostEqual(val/P,1.,delta=6e-4)
        self.assertGreater(abs(val/P-.5),.49)

    def test_all_bose_permutations(self):
        for rho in (.4,40.,400.):
            vals=[sum(abs(r.helicities(rho,x,y))**2) for x,y,z in itertools.permutations([.1,.2,.7])]
            self.assertLess(max(vals)/min(vals)-1,2e-10)

    def test_collinear_limits(self):
        for rho in (40.,400.):
            B=abs(g.form_factor(rho/4))**2
            x=1e-6;y=.3;z=1-x-y;P=1+x**4+y**4+z**4
            self.assertAlmostEqual(sum(abs(r.helicities(rho,x,y))**2)/(B*P),1.,delta=3e-6)

    def test_soft_limits(self):
        for rho in (40.,400.):
            e=1e-4;x=1-e;y=.3*e;z=.7*e;P=1+x**4+y**4+z**4
            B=abs(g.form_factor(rho/4))**2
            self.assertAlmostEqual(sum(abs(r.helicities(rho,x,y))**2)/(B*P),1.,delta=3e-6)

    def test_regulator_variation(self):
        a=r.helicities(40.,.2,.3,1e-18);b=r.helicities(40.,.2,.3,1e-26)
        np.testing.assert_allclose(a,b,rtol=2e-12,atol=2e-13)

    def test_printed_source_leaves_collinear_residue(self):
        for x in (1e-4,1e-6):
            y=.3;z=1-x-y;P=1+x**4+y**4+z**4
            v=r.shape_components(20.,x,y,printed=True)[3]
            B=abs(sum(g.loop_amplitudes(20.)[q] for q in ('b','c')))**2
            matched=r.shape_components(20.,x,y)[3]
            residue=.5*P*B/(y*z)
            self.assertAlmostEqual(v*x-residue,2*x*matched,delta=3e-12)
            if x<=1e-6:self.assertLess(abs(v*x-residue),3e-6)

    def test_reconstructed_difference_is_finite_collinear(self):
        v1=r.shape_components(20.,1e-5,.3)[3];v2=r.shape_components(20.,1e-6,.3)[3]
        self.assertLess(abs(v1-v2),3e-4)

    def test_eikonal_current_normalization(self):
        dot=lambda a,b:a[0]*b[0]-np.dot(a[1:],b[1:])
        p1=np.array([1.,0,0,1.]);p2=np.array([1.,0,0,-1.]);CA=3.
        for theta in (.4,1.2):
            k=.001*np.array([1.,math.sin(theta),0.,math.cos(theta)])
            J=p1/dot(p1,k)-p2/dot(p2,k)
            eikonal=-CA*dot(J,J)
            sij=2*dot(p1,p2);sik=2*dot(p1,k);sjk=2*dot(p2,k)
            self.assertAlmostEqual(eikonal/(4*CA*sij/(sik*sjk)),1.,delta=2e-14)

    def test_identical_pair_and_three_body_phase_space(self):
        # Q=1; Phi2=1/(8pi), Phi3=integral ds/(2pi) Phi2(1;s,0)Phi2(s;0,0)
        p3=quad(lambda s:(1-s)/(128*math.pi**3),0,1)[0]
        self.assertAlmostEqual(p3,1/(256*math.pi**3),delta=1e-18)
        # M3^2/M2^2 coefficient=8pi alpha_s CA/Q^2; 1/3! vs 1/2!.
        coefficient=(1/(128*math.pi**3)/6)/(1/(8*math.pi)/2)*8*math.pi*3
        self.assertAlmostEqual(coefficient,1/(2*math.pi),delta=2e-15)

    def test_production_heavy_limit_independent_coefficient(self):
        # Source (C.4) heavy limit; the integral is -11/6.
        integral=quad(lambda v:-4+6*v-4*v*v+2*v**3,0,1)[0]
        self.assertAlmostEqual(3*integral,-11/2,delta=2e-14)

    def test_component_sum(self):
        for x,y in ((.2,.3),(.01,.4)):
            v=r.shape_components(20.,x,y)
            self.assertAlmostEqual(sum(v[:3]),v[3],delta=1e-13)

    def test_identical_loop_coherence(self):
        a=r.helicities(40.,.2,.3)
        self.assertAlmostEqual(sum(abs(a+a)**2),4*sum(abs(a)**2),delta=1e-14)
        self.assertAlmostEqual(sum(abs(a-a)**2),0.,delta=1e-15)

    def test_vector_vs_scalar(self):
        xs=np.array([.1,.2]);ys=np.array([.2,.3])
        v=r.shape_components(20.,xs,ys)
        for i in range(2):np.testing.assert_allclose(v[:,i],r.shape_components(20.,xs[i],ys[i]),rtol=1e-11,atol=1e-12)

    def test_shape_regression(self):
        v=r.finite_remainder(20.,n=24)
        np.testing.assert_allclose(v,[-.44242092,.02843049,.22882502,-.18516542],rtol=0,atol=2e-8)

    def test_angular_convergence(self):
        a=r.finite_remainder(20.,n=24);b=r.finite_remainder(20.,n=48)
        self.assertLess(max(abs(a-b)),1e-6)

    def test_shape_upper_hard_domain(self):
        a=r.finite_remainder(80.,n=24);b=r.finite_remainder(80.,n=48)
        self.assertLess(max(abs(a-b)),3e-6)

    def test_thermal_two_representations(self):
        a=r.thermal_components(angular_n=12,thermal_n=16)
        b=r.thermal_components(angular_n=12,thermal_n=32,method='Q')
        self.assertLess(max(abs(a-b)),1e-23)

    def test_invalid_kinematics(self):
        for x,y in ((0,.3),(.4,.7),(-.1,.3),(math.nan,.2)):
            with self.assertRaises(ValueError):r.helicities(40,x,y)
        with self.assertRaises(ValueError):r.helicities(0,.2,.3)

    def test_invalid_hard_domains(self):
        for Q in (1.5,19,81,math.inf):
            with self.assertRaises(ValueError):r.finite_remainder(Q,n=8)
        with self.assertRaises(ValueError):r.finite_remainder(20,scheme='unknown')
        with self.assertRaises(ValueError):r.finite_remainder(20,scale=3)

    def test_invalid_quadrature_or_thermal(self):
        for n in (0,7,257,3.1):
            with self.assertRaises(ValueError):r.nodes(n)
        with self.assertRaises(ValueError):r.thermal_components(T=1)
        with self.assertRaises(ValueError):r.thermal_components(pair='21')
        with self.assertRaises(ValueError):r.thermal_components(thermal_n=0)
        with self.assertRaises(ValueError):r.thermal_components(method='unknown')

if __name__=='__main__':unittest.main()
