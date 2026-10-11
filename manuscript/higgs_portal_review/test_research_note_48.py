"""Note48: finite-convention closure checks, not independent QCD validation.

The literal inherited assembly is kept as a discrepancy diagnostic.  No test
silently changes the old source files or interprets the candidate as data.
"""
import hashlib
import math
from pathlib import Path
import unittest
import numpy as np
from scipy.integrate import quad
import decay_assembly_audit as a
import heavy_quark_thermal as h
import gluon_loop_thermal as g
import coherent_bc_rg as rg
import bc_virtual_finite as v
import three_gluon_remainder as r3
import top_operator_nlo as top
import mixed_gluon_nlo as mixed


class AssemblyAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Q=20.
        cls.c=a.candidate_terms(cls.Q,n=24)
        cls.hardcases={}
        for Q,s,scheme in ((20.,1.,'MSbar'),(23.,1.,'MSbar'),(40.,1.,'MSbar'),
                           (65.,1.,'MSbar'),(20.,.5,'MSbar'),(20.,2.,'MSbar'),
                           (23.,1.,'pole1')):
            cls.hardcases[Q,s,scheme]=a.diagnostic(Q,s,scheme,n=32)
        cls.th=a.thermal_candidate(angular_n=12,thermal_n=12)

    def test_01_inherited_source_bytes_unchanged(self):
        expected={h:'40d51657a26fb20851be2bafa0ea6b3efe05ddfb',
                  v:'fd2af360cc4eae7a838f2d93a16c003627b533a5',
                  r3:'e0fb6fd3964b67324289b3de86f38e7afc85e789',
                  mixed:'0ffc28870c414cc8613d28549511d10bcaf30ee7'}
        for module,digest in expected.items():
            b=Path(module.__file__).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),digest)

    def test_02_products_sum_is_coherent_square(self):
        fs=np.array([1+2j,.3-.4j,-.7+.2j])
        self.assertAlmostEqual(float(a.products(fs).sum()),abs(fs.sum())**2,places=14)

    def test_03_products_retain_signed_interference(self):
        terms=a.products(np.array([1.,-2.,3.]))
        np.testing.assert_allclose(terms,[1,4,9,-4,6,-12],rtol=0,atol=0)

    def test_04_heavy_top_universal_recovery(self):
        # Note43 independently builds its top-sector virtual+real coefficient.
        for Q,s,scheme in self.hardcases:
            terms=a.candidate_terms(Q,s,scheme,n=24)
            target=top.current_components(Q,s,scheme)['delta_veto']
            self.assertAlmostEqual(terms['literal_increment'][0]/target,1.,delta=3e-12)

    def test_05_literal_mixed_mismatch_is_not_hidden(self):
        d=self.hardcases[20.,1.,'MSbar']['flavors']
        self.assertGreater(abs(d['b']['literal_minus_reference_GeV2']),.009)
        self.assertGreater(abs(d['c']['literal_minus_reference_GeV2']),.0009)

    def test_06_residual_follows_mass_derivative(self):
        Q=20.;pref=(h.alpha_s(Q)/math.pi)**3*Q*Q/9
        for q in ('b','c'):
            df=rg.form_and_mass_derivative((h.running_mass(q,Q)/Q)**2)[1]
            residual=self.hardcases[Q,1.,'MSbar']['flavors'][q]['literal_minus_reference_GeV2']
            self.assertAlmostEqual(residual/(pref*df.real),-8/3,delta=8e-8)

    def test_07_matched_bottom_current_closes_all_checkpoints(self):
        for d in self.hardcases.values():
            x=d['flavors']['b']
            self.assertAlmostEqual(x['matched_increment_GeV2']/x['reference_increment_GeV2'],1.,delta=2e-8)

    def test_08_matched_charm_current_closes_all_checkpoints(self):
        for d in self.hardcases.values():
            x=d['flavors']['c']
            self.assertAlmostEqual(x['matched_increment_GeV2']/x['reference_increment_GeV2'],1.,delta=2e-8)

    def test_09_shift_is_born_derivative_not_independent_channel(self):
        Q=20.;ms=a.masses(Q);pref=(h.alpha_s(Q)/math.pi)**3*Q*Q/9
        F=np.array([1,g.form_factor((Q/2/ms['b'])**2),g.form_factor((Q/2/ms['c'])**2)])
        eps=1e-5
        derivative=np.zeros(6)
        for j,q in [(1,'b'),(2,'c')]:
            fp=F.copy();fm=F.copy()
            fp[j]=g.form_factor((Q/(2*ms[q]*math.exp(eps)))**2)
            fm[j]=g.form_factor((Q/(2*ms[q]*math.exp(-eps)))**2)
            derivative+=(a.products(fp)-a.products(fm))/(2*eps)
        np.testing.assert_allclose(a.finite_shift(Q),pref*(4/3)*derivative,rtol=3e-8,atol=1e-15)

    def test_10_zero_shift_for_top_square(self):
        self.assertEqual(a.finite_shift(20.)[0],0.)

    def test_11_matched_virtual_coefficient_direction(self):
        Q=20.;ms=a.masses(Q);pref=(h.alpha_s(Q)/math.pi)**3*Q*Q/9
        for q,j in [('b',1),('c',2)]:
            r=(ms[q]/Q)**2;f,df=rg.form_and_mass_derivative(r)
            corrected=v.hk_product(r)+2*(math.log(1/r)+4/3)*df
            literal=a.born_virtual(Q)[1][j]
            self.assertAlmostEqual(literal+a.finite_shift(Q)[j]/pref,
                                   (corrected*f.conjugate()).real,delta=3e-13)

    def test_12_pole_convention_restores_unshifted_G1(self):
        Q=23.;ms=a.masses(Q,scheme='pole1');pref=(h.alpha_s(Q)/math.pi)**3*Q*Q/9
        b,virt=a.born_virtual(Q,scheme='pole1')
        for q,j in [('b',1),('c',2)]:
            r=(ms[q]/Q)**2;f=rg.form_and_mass_derivative(r)[0]
            self.assertAlmostEqual(virt[j]+a.finite_shift(Q,scheme='pole1')[j]/pref,
                     (v.hk_product(r)*f.conjugate()).real,delta=4e-13)

    def test_13_finite_boundary_reexpansion_order(self):
        rb,rc=.027,.0013
        def B(shift):
            return abs(rg.form_and_mass_derivative(rb*math.exp(2*shift))[0]+
                       rg.form_and_mass_derivative(rc*math.exp(2*shift))[0])**2
        fs=[rg.form_and_mass_derivative(r) for r in (rb,rc)]
        D=2*((fs[0][1]+fs[1][1])*(fs[0][0]+fs[1][0]).conjugate()).real
        errors=[]
        for alpha in (2e-5,1e-5):
            # finite mass shift m -> m exp[(4/3)*a]; width a^2 yields a^4 error
            full=alpha**2*B((4/3)*alpha)
            expanded=alpha**2*B(0)+alpha**3*(4/3)*D
            errors.append(abs(full-expanded))
        self.assertAlmostEqual(errors[0]/errors[1],16.,delta=.02)

    def test_14_nlo_bookkeeping_identity(self):
        np.testing.assert_allclose(self.c['matched_NLO'],self.c['LO']+self.c['matched_increment'],rtol=0,atol=0)
        np.testing.assert_allclose(self.c['matched_increment'],self.c['literal_increment']+self.c['finite_shift'],rtol=0,atol=0)

    def test_15_universal_massless_flavor_difference(self):
        Q=20.;ms=a.masses(Q);logs=sum(math.log(Q*Q/m**2) for m in ms.values())
        U5=73/4-7*5/6
        self.assertAlmostEqual(a.universal(Q)-U5,7/3-logs/3,places=13)

    def test_16_finite_subtraction_relocation_keeps_sum(self):
        terms=self.c;B=a.born_virtual(20.)[0]
        pref=(h.alpha_s(20.)/math.pi)**3*20**2/9
        # Explicitly synthetic finite subtraction change, not a new QCD input.
        shift=0.7*pref*B
        total=(terms['virtual_literal']+terms['universal']+shift+
               terms['three_gluon']-shift+terms['light_pair'])
        np.testing.assert_allclose(total,terms['literal_increment'],rtol=4e-15,atol=2e-17)

    def test_17_pair_remainder_note45_real_checkpoint(self):
        p=a.pair_remainder(20.)
        self.assertAlmostEqual(float(p[1]+p[2]+p[5]),-.0773301160,delta=7e-10)

    def test_18_pair_quadrature_refinement(self):
        p=a.pair_remainder(20.,n=128);q=a.pair_remainder(20.,n=64)
        np.testing.assert_allclose(p,q,rtol=1e-7,atol=2e-9)

    def test_19_offshell_collinear_normalization(self):
        for t in (10.,200.):
            ref=g.form_factor(t);actual=a.offshell(t,np.array([1e-9]))[0]
            self.assertLess(abs(actual-ref),2e-8)

    def test_20_offshell_endpoint_is_finite(self):
        for t in (10.,200.):
            value=a.offshell(t,np.array([1-1e-9,1-1e-7]))
            self.assertTrue(np.all(np.isfinite(value)))
            self.assertLess(abs(value[0]-value[1]),1e-6)

    def test_21_three_gluon_bc_recovery(self):
        six=a.three_remainder(20.,n=24)
        old=r3.finite_remainder(20.,n=24)
        np.testing.assert_allclose(six[[1,2,5]],old[:3],rtol=2e-10,atol=3e-12)

    def test_22_top_real_remainders_vanish(self):
        self.assertEqual(a.pair_remainder(20.)[0],0.)
        self.assertLess(abs(a.three_remainder(20.,n=24)[0]),1e-12)

    def test_23_bose_symmetry_with_top_probe(self):
        x,y,z=.15,.32,.53
        np.testing.assert_allclose(a.shape(20.,x,y),a.shape(20.,z,y),rtol=2e-9,atol=2e-10)

    def test_24_cross_sector_refinement(self):
        d=a.diagnostic(20.,n=32)
        old=self.hardcases[20.,1.,'MSbar']
        for q in ('b','c'):
            self.assertLess(abs(d['flavors'][q]['matched_increment_GeV2']-
                       old['flavors'][q]['matched_increment_GeV2']),2e-9)

    def test_25_thermal_lo_reference(self):
        # Initial pair 11 only; the actual numerical check is recomputed here.
        lo=self.th[a.PARTS.index('LO')]
        self.assertAlmostEqual(float(lo[1]+lo[2]+lo[5])/2.67595e-17,1.,delta=3e-6)

    def test_26_thermal_virtual_reference(self):
        val=self.th[a.PARTS.index('virtual_literal')]
        inherited=v.thermal(.5,'11')[0]
        self.assertAlmostEqual(float(val[1]+val[2]+val[5])/inherited,1.,delta=2e-9)

    def test_27_thermal_sum_is_componentwise(self):
        np.testing.assert_allclose(self.th[8],self.th[0]+self.th[7],rtol=2e-15,atol=2e-30)

    def test_28_invalid_hard_inputs_fail(self):
        for Q in (1.5,19.,81.,math.nan):
            with self.assertRaises(ValueError):a.born_virtual(Q)
        with self.assertRaises(ValueError):a.pair_remainder(20.,scheme='unknown')
        with self.assertRaises(ValueError):a.pair_remainder(20.,n=8)
        with self.assertRaises(ValueError):a.offshell(.5,np.array([.2]))
        with self.assertRaises(ValueError):a.offshell(10.,np.array([0.]))

    def test_29_invalid_thermal_inputs_fail(self):
        for args in ({'T':1.},{'pair':'21'},{'angular_n':2},{'thermal_n':True},{'method':'unknown'}):
            with self.assertRaises(ValueError):a.thermal_candidate(**args)

    def test_30_full_physical_claim_is_blocked(self):
        with self.assertRaises(NotImplementedError):a.complete_physical_rate(20.)
        d=self.hardcases[20.,1.,'MSbar']
        self.assertFalse(d['source_erratum_confirmed'])
        self.assertFalse(d['complete_physical_NLO_claimed'])

if __name__=='__main__':unittest.main()
