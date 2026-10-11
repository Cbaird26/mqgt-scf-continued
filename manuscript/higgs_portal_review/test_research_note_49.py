"""Note 49: independent source transcription and exact-convention checks.

No experimental/model validation or whole-repository audit is implied.
"""
import ast
import cmath
import math
from pathlib import Path
import unittest
import numpy as np
import abdv_virtual_check as a
import abdv_reference as ref
import bc_virtual_finite as hk
import coherent_bc_rg as rg
import heavy_quark_thermal as h
from prove_note49 import proof

class ABDVTests(unittest.TestCase):
    def test_no_import_of_old_hard_coefficients(self):
        tree=ast.parse(Path(a.__file__).read_text())
        modules=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        modules += [al.name for n in ast.walk(tree) if isinstance(n,ast.Import) for al in n.names]
        self.assertFalse(set(modules)&{'bc_virtual_finite','mixed_gluon_nlo','decay_assembly_audit','coherent_bc_rg'})

    def test_hpl_all_zero_words(self):
        x=complex(-.03,0)
        for n in range(1,5):self.assertLess(abs(a.hpl((0,)*n,x)-cmath.log(x)**n/math.factorial(n)),2e-14)

    def test_hpl_logarithms(self):
        for x in (-.09,-.005,.04):
            z=complex(x,0)
            self.assertLess(abs(a.hpl((1,),z)+cmath.log(1-z)),3e-15)
            self.assertLess(abs(a.hpl((-1,),z)-cmath.log(1+z)),3e-15)

    def test_hpl_reference_all_needed_words(self):
        for x in (-.09,-.003):
            for word,value in ref.hpl_reference_values(x).items():
                self.assertLess(abs(a.hpl(word,complex(x,0))-complex(value)),3e-13,(x,word))

    def test_hpl_series_order(self):
        for word in ((1,0,-1,0),(0,1,0,0),(1,0,0,0)):
            v=a.hpl(word,complex(-.095,0),48)
            self.assertLess(abs(v-a.hpl(word,complex(-.095,0),64)),2e-15)

    def test_hpl_kernel_derivative(self):
        x=complex(-.03,.01);eps=1e-7
        for word in ((1,0,-1,0),(0,-1,0),(-1,0,0)):
            d=(a.hpl(word,x+eps)-a.hpl(word,x-eps))/(2*eps)
            kernel={0:1/x,1:1/(1-x),-1:1/(1+x)}[word[0]]
            expected=kernel*a.hpl(word[1:],x)
            self.assertLess(abs(d-expected),3e-8)

    def test_upper_timelike_boundary(self):
        x=-.02
        self.assertGreater(a.hpl((0,),complex(x,0)).imag,0)
        self.assertLess(abs(a.hpl((0,),complex(x,1e-12))-a.hpl((0,),complex(x,0))),6e-11)

    def test_born_normalization(self):
        for r in (1e-6,.001,.03,.08):
            self.assertLess(abs(a.coefficients(r)['F']-rg.form_and_mass_derivative(r)[0]),1e-14)

    def test_ABDV_mass_log_derivative(self):
        for r in (1e-6,.001,.03,.08):
            self.assertLess(abs(a.coefficients(r)['Fb']-rg.form_and_mass_derivative(r)[1]),2e-14)

    def test_third_source_MS_matches_Note48(self):
        for r in (1e-6,.001,.03,.08):
            F,D=rg.form_and_mass_derivative(r)
            for scale in (.5,1.,2.):
                expected=hk.hk_product(r)+2*(2*math.log(scale)-math.log(r)+4/3)*D
                self.assertLess(abs(a.coefficients(r,scale)['G']-expected),5e-13)

    def test_third_source_OS_matches_G1(self):
        for r in (1e-6,.001,.03,.08):
            self.assertLess(abs(a.coefficients(r,scheme='OS')['G']-hk.hk_product(r)),5e-13)

    def test_literal_old_block_is_not_matched(self):
        r=.03;F,D=rg.form_and_mass_derivative(r)
        old=hk.hk_product(r)-2*math.log(r)*D
        delta=a.coefficients(r)['G']-old
        self.assertGreater(abs(delta),1.)
        self.assertLess(abs(delta-(8/3)*D),5e-13)

    def test_symbolic_mass_derivative(self):
        self.assertTrue(proof()['Fb_minus_mass_derivative_exact_zero'])

    def test_symbolic_OS_identity(self):
        self.assertTrue(proof()['G_ABDV_OS_minus_HK_G1_exact_zero'])

    def test_symbolic_MS_identity(self):
        self.assertTrue(proof()['G_ABDV_MS_minus_HK_G1_minus_2_log_plus_four_thirds_D_exact_zero'])

    def test_arbitrary_precision_coefficient(self):
        for r in (.03,.001):
            for scheme in ('MSbar','OS'):
                out=ref.reference_coefficients(r,1.,scheme)
                self.assertLess(abs(out['G']-a.coefficients(r,1.,scheme)['G']),3e-13)

    def test_coherent_current_decomposition(self):
        for Q in (20.,40.,80.):
            val=sum(a.current(Q,component=c) for c in ('bb','cc','bc'))
            self.assertAlmostEqual(val,a.current(Q),delta=5e-17)

    def test_current_matches_finite_mass_shift(self):
        for Q in (20.,23.,65.):
            for scale in (.5,1.,2.):
                mb,mc=a.masses(Q,scale)
                Fb,Db=rg.form_and_mass_derivative((mb/Q)**2)
                Fc,Dc=rg.form_and_mass_derivative((mc/Q)**2)
                shift=Q*Q/9*(h.alpha_s(scale*Q)/math.pi)**3*(8/3)*((Db+Dc)*(Fb+Fc).conjugate()).real
                literal=hk.current_weight(Q,scale)
                self.assertLess(abs(a.current(Q,scale)-literal-shift),1e-15)

    def test_OS_current_matches_shifted_old_OS(self):
        Q=23.;mb,mc=a.masses(Q,1.,'OS')
        Fb,Db=rg.form_and_mass_derivative((mb/Q)**2);Fc,Dc=rg.form_and_mass_derivative((mc/Q)**2)
        shift=Q*Q/9*(h.alpha_s(Q)/math.pi)**3*(8/3)*((Db+Dc)*(Fb+Fc).conjugate()).real
        self.assertLess(abs(a.current(Q,scheme='OS')-hk.current_weight(Q,scheme='pole1')-shift),2e-15)

    def test_thermal_two_variables_all_pairs(self):
        for pair in h.PAIRS:
            v=a.thermal(.5,pair)[0];q=a.thermal(.5,pair,method='Q')[0]
            self.assertAlmostEqual(v/q,1.,delta=5e-10)

    def test_equilibrium_weighted_virtual_regression(self):
        w=h.equilibrium_weights(.5)
        v=sum(w[p]*a.thermal(.5,p)[0] for p in h.PAIRS)
        self.assertAlmostEqual(v,2.002097222782949e-17,delta=2e-27)

    def test_low_temperature_window(self):
        v=a.thermal(1/3,'12')[0];q=a.thermal(1/3,'12',method='Q')[0]
        self.assertGreater(v,0.)
        self.assertAlmostEqual(v/q,1.,delta=5e-10)

    def test_input_validation(self):
        for fn in (lambda:a.hpl((2,),-.01),lambda:a.hpl((0,),0),lambda:a.hpl((1,),.2),
                   lambda:a.coefficients(0),lambda:a.coefficients(.25),lambda:a.coefficients(.01,scheme='none'),
                   lambda:a.current(19),lambda:a.current(20,scale=.1),lambda:a.thermal(1,'11'),
                   lambda:a.current(20,component='none')):
            with self.assertRaises(ValueError):fn()

    def test_refuse_full_rate_label(self):
        with self.assertRaises(NotImplementedError):a.complete_physical_rate(20.)

if __name__=='__main__':unittest.main()
