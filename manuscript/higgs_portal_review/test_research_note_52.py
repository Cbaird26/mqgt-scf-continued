"""Note 52 algebra/numerical regressions; no full-spectrum or empirical claim."""
import math
import unittest
import numpy as np
import mpmath as mp
from scipy.linalg import eigh
import kinetic_moment_audit as k
import kinetic_moment_reference as ref

class KineticMomentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs={T:k.evaluate(T) for T in (.5,.4,1/3)}

    def test_scalar_stats_against_density_integrals(self):
        for T in (.5,.4,1/3):
            for m in (k.M1,k.M2):
                np.testing.assert_allclose(k.thermal_stats(T,m),ref.scalar_stats(T,m),rtol=2e-12,atol=1e-12)

    def test_variance_is_temperature_derivative(self):
        T=.45;delta=1e-5
        m=k.M1
        numerical=(k.thermal_stats(T+delta,m)[0]-k.thermal_stats(T-delta,m)[0])/(2*delta)
        self.assertAlmostEqual(numerical/k.thermal_stats(T,m)[1],1,delta=2e-9)

    def test_metric_positive_and_normalized(self):
        for o in self.outputs.values():
            d=np.array(o['metric_per_N'])
            self.assertTrue(np.all(d>0));self.assertAlmostEqual(sum(d[:2]),1)

    def test_boost_integrals(self):
        for z in (10.,25.,60.,150.):
            np.testing.assert_allclose(k.boost_moments(z),ref.boost_stats(z),rtol=2e-13,atol=1e-13)

    def test_boost_mass_shell(self):
        for z in (20.,50.,100.):
            _,g2,u2=k.boost_moments(z)
            self.assertAlmostEqual(g2-u2,1,places=14)

    def test_reduced_rate_matches_note51(self):
        for ml in k.base.LEPTONS.values():
            for q in (k.M2+ml+.01,15.,30.):
                got=k.transfer_moments(q,k.M2,k.M1,ml,k.K12)[0]
                target=k.base.reduced_kernel(q,k.M2,k.M1,ml)
                self.assertAlmostEqual(got/target,1,delta=1e-11)

    def test_transfer_moment_high_precision(self):
        with mp.workdps(60):
            for ml in k.base.LEPTONS.values():
                q=15.;tm,tp=k.base.t_limits(q,k.M2,k.M1,ml)
                fun=lambda t:mp.mpf(k.K12)**2*mp.mpf(ml)**2*(4*mp.mpf(ml)**2-t)/(mp.mpf(k.MH)**2-t)**2/(16*mp.pi)
                w0=mp.quad(fun,[mp.mpf(tm),mp.mpf(tp)])
                wu=mp.quad(lambda t:-t*fun(t),[mp.mpf(tm),mp.mpf(tp)])
                got=k.transfer_moments(q,k.M2,k.M1,ml,k.K12)
                np.testing.assert_allclose(got,[float(w0),float(wu)],rtol=3e-13,atol=0)

    def test_reciprocity_of_weighted_transfer(self):
        for ml in k.base.LEPTONS.values():
            a=k.transfer_moments(15,k.M2,k.M1,ml,k.K12)
            b=k.transfer_moments(15,k.M1,k.M2,ml,k.K12)
            np.testing.assert_allclose(a,b,rtol=1e-14,atol=0)

    def test_sign_and_squared_coupling(self):
        args=(15,k.M2,k.M1,k.base.LEPTONS['tau'])
        a=np.array(k.transfer_moments(*args,k.K12))
        np.testing.assert_array_equal(a,k.transfer_moments(*args,-k.K12))
        np.testing.assert_array_equal(4*a,k.transfer_moments(*args,2*k.K12))

    def test_exact_threshold_is_zero(self):
        ml=k.base.LEPTONS['tau']
        self.assertEqual(k.transfer_moments(k.M2+ml,k.M2,k.M1,ml,k.K12),(0.,0.))

    def test_independent_explicit_lorentz_boosts(self):
        for pair in ('11','21','22'):
            a=k.weighted_jump_gram(15.,.5,k.base.LEPTONS['tau'],pair)
            b=ref.direct_jump_gram(15.,.5,k.base.LEPTONS['tau'],pair,k.Model())
            np.testing.assert_allclose(a,b,rtol=2e-11,atol=np.max(abs(a))*1e-12)

    def test_fixed_q_forms_positive(self):
        for ml in k.base.LEPTONS.values():
            for pair in ('11','21','22'):
                a=k.weighted_jump_gram(15.,.5,ml,pair)
                self.assertGreaterEqual(np.linalg.eigvalsh(a).min(),-np.max(abs(a))*2e-13)

    def test_exact_number_null_direction(self):
        null=np.array([1,1,0,0,0,0])
        for o in self.outputs.values():
            np.testing.assert_array_equal(np.array(o['D_MB_per_N_GeV'])@null,np.zeros(6))

    def test_parity_blocks_vanish(self):
        for o in self.outputs.values():
            np.testing.assert_array_equal(np.array(o['D_MB_per_N_GeV'])[:4,4:],np.zeros((4,2)))

    def test_elastic_keeps_counts_separate(self):
        for pair in ('11','22'):
            d=k.collision_gram(.5,k.base.LEPTONS['tau'],pair)
            self.assertEqual(np.count_nonzero(d),2)
            self.assertTrue(np.all(np.diag(d)[np.diag(d)!=0]>0))

    def test_count_block_recovers_note51(self):
        expected={.5:1.7627736145388546,.4:.703796890043111,1/3:.29186241695244924}
        for T,o in self.outputs.items():
            self.assertAlmostEqual(o['MB_projected']['counts_only_relaxation_over_H']/expected[T],1,delta=3e-11)

    def test_projected_central_regression(self):
        o=self.outputs[.5]['MB_projected']
        np.testing.assert_allclose(o['scalar_eigenvalues_over_H'],[.6044446951976372,1.7839910391502363,2.1413347926332227],rtol=3e-10)
        np.testing.assert_allclose(o['drift_eigenvalues_over_H'],[.4180960088250115,1.9877098861313303],rtol=3e-10)

    def test_nonzero_mode_count_and_positive(self):
        for o in self.outputs.values():
            r=o['MB_projected']
            self.assertEqual(len(r['scalar_eigenvalues_GeV']),3)
            self.assertEqual(len(r['drift_eigenvalues_GeV']),2)
            self.assertGreater(min(r['scalar_eigenvalues_GeV']+r['drift_eigenvalues_GeV']),0)

    def test_projected_values_match_full_generalized_eigenproblem(self):
        o=self.outputs[.5];d=np.array(o['D_MB_per_N_GeV']);g=np.diag(o['metric_per_N'])
        allvals=eigh(d,g,eigvals_only=True)
        known=sorted(o['MB_projected']['scalar_eigenvalues_GeV']+o['MB_projected']['drift_eigenvalues_GeV'])
        self.assertLess(abs(allvals[0]),max(known)*1e-12)
        np.testing.assert_allclose(allvals[1:],known,rtol=2e-12,atol=1e-31)

    def test_fd_matrix_loewner_order(self):
        for o in self.outputs.values():
            up=np.array(o['D_MB_per_N_GeV']);lo=np.array(o['D_FD_lower_per_N_GeV'])
            for a in (lo,up-lo):
                self.assertGreaterEqual(np.linalg.eigvalsh(a).min(),-np.max(abs(up))*2e-13)

    def test_fd_projected_eigenvalue_order(self):
        for o in self.outputs.values():
            for key in ('scalar_eigenvalues_GeV','drift_eigenvalues_GeV'):
                lo=np.array(o['FD_lower_projected'][key]);up=np.array(o['MB_projected'][key])
                self.assertTrue(np.all((lo>0)&(lo<=up)))

    def test_thermal_q_and_w_representations(self):
        for T in (.5,1/3):
            for ml in k.base.LEPTONS.values():
                for pair in ('11','21','22'):
                    a=k.collision_gram(T,ml,pair,method='w')
                    b=k.collision_gram(T,ml,pair,method='q')
                    np.testing.assert_allclose(a,b,rtol=1e-8,atol=np.max(abs(a))*1e-10)

    def test_transfer_quadrature_refinement(self):
        for pair in ('11','21','22'):
            a=k.collision_gram(.5,k.base.LEPTONS['tau'],pair,n=16)
            b=k.collision_gram(.5,k.base.LEPTONS['tau'],pair,n=48)
            np.testing.assert_allclose(a,b,rtol=2e-10,atol=np.max(abs(a))*1e-12)

    def test_analytic_tail_upper_bound_is_small(self):
        bound=sum(k.omitted_normalized_form_bound(.5,ml,p)/k.base.hubble(.5) for ml in k.base.LEPTONS.values() for p in ('11','21','22'))
        self.assertGreater(bound,0);self.assertLess(bound,1e-24)

    def test_cut_refinement_with_roundoff_allowance(self):
        ml=k.base.LEPTONS['tau']
        a=k.collision_gram(.5,ml,'21',cut=60)
        b=k.collision_gram(.5,ml,'21',cut=90)
        _,g=k.equilibrium_metric(.5)
        diff=np.linalg.norm(k.normalized_operator(a-b,g),2)
        bound=k.omitted_normalized_form_bound(.5,ml,'21',cut=60)
        rounding=2e-11*np.linalg.norm(k.normalized_operator(b,g),2)
        self.assertLess(diff,bound+rounding)

    def test_no_conversion_adds_second_number_zero(self):
        o=k.evaluate(.5,k.Model(k12=0))
        self.assertEqual(o['MB_projected']['counts_only_relaxation_GeV'],0)
        self.assertEqual(o['MB_projected']['scalar_eigenvalues_GeV'][0],0)

    def test_all_portals_off(self):
        o=k.evaluate(.5,k.Model(k11=0,k12=0,k22=0))
        np.testing.assert_array_equal(o['D_MB_per_N_GeV'],np.zeros((6,6)))

    def test_variational_subspace_order(self):
        for o in self.outputs.values():
            r=o['MB_projected'];d=np.array(o['D_MB_per_N_GeV']);g=np.array(o['metric_per_N'])
            self.assertLessEqual(r['scalar_eigenvalues_GeV'][0],r['counts_only_relaxation_GeV'])
            self.assertLessEqual(r['scalar_eigenvalues_GeV'][0],min(d[2,2]/g[2],d[3,3]/g[3]))

    def test_arbitrary_fugacity_cancels(self):
        o=self.outputs[.5];d=np.array(o['D_MB_per_N_GeV']);g=np.array(o['metric_per_N'])
        np.testing.assert_allclose(k.normalized_operator(7*d,7*g),k.normalized_operator(d,g),rtol=2e-15,atol=1e-33)

    def test_invalid_inputs_rejected(self):
        for T in (0.,.6,float('nan')):
            with self.assertRaises(ValueError):k.evaluate(T)
        with self.assertRaises(ValueError):k.Model(m1=-1).validate()
        with self.assertRaises(ValueError):k.transfer_moments(10,11.5,10,1,k.K12)
        with self.assertRaises(ValueError):k.collision_gram(.5,1,'12')
        with self.assertRaises(ValueError):k.collision_gram(.5,1,'21',method='bad')
        with self.assertRaises(ValueError):k.boost_moments(0)

    def test_no_complete_rate_or_qcd_fabrication(self):
        with self.assertRaises(NotImplementedError):k.complete_kinetic_equilibrium()
        with self.assertRaises(NotImplementedError):k.full_qcd_response()

if __name__=='__main__':unittest.main()
