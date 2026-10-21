import sys
import unittest
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model import (INDEX, NAMES, FlowSpecification, IncompleteFlowError,
                   gravity_beta, required_eta_n)
from scalar_core import beta_scalar, bounded_from_below, only_real_one_loop_fixed_point
from higgs_two_singlet_core import beta_scalar_quartics
from sm_gauge_core import beta_gauge, one_loop_fixed_point
from perturbative_matter_baseline import beta as matter_beta, rk4
from scalar_frg_lpa import litim_potential_flow, mass_matrix, project_scalar_potential_flow
from partial_flow_41 import coverage, requires_complete_flow, beta_partial
from canonical_scaling import beta_canonical
from einstein_hilbert_litim_benchmark import beta as litim_beta, d4_fixed_point, eta as litim_eta, critical_exponents as litim_exponents
from lithium_thresholds import Phi, Phi_tilde, Phi_integral, Phi_tilde_integral, Q_n_threshold
from gravity_frg import (fixed_point as frg_fixed_point, beta as frg_beta, eta_n,
                         critical_exponents as frg_exponents, fixed_point_equation_level,
                         fixed_point_paper_coordinates, c_d, g_eq)
from gravity_matter_coupling import (beta as dep_beta, fixed_point as dep_fixed_point,
                                     eta_system, critical_exponents as dep_exponents,
                                     STANDARD_MODEL, DEP_TABLE_GHOST_FACTOR,
                                     beta_perturbative, perturbative_fixed_point)
from r2_gravity_cpr import (omega_fixed_points, theta_star, q_omega,
                            beta_lambda_rsq, beta_xi_rsq, beta_omega_rsq,
                            beta_theta_rsq, beta_g_tilde_rsq,
                            beta_lambda_tilde_rsq, r2_newton_fixed_point,
                            a_r2_beta, a_c2_beta)


class ReconstructionTests(unittest.TestCase):
    def test_declared_basis_document_tracks_registry(self):
        document = (Path(__file__).resolve().parents[1] / "DECLARED_TRUNCATION_V0_1.md").read_text()
        for name in NAMES:
            self.assertIn(f"`{name}`", document)

    def test_declares_41_unique_coordinates(self):
        self.assertEqual(len(NAMES), 41)
        self.assertEqual(len(INDEX), 41)

    def test_nonzero_gravity_fixed_point_requires_eta_minus_two(self):
        self.assertEqual(required_eta_n(0.27), -2.0)
        self.assertEqual(gravity_beta(0.27, -2.0), 0.0)
        self.assertNotEqual(gravity_beta(0.27, 0.0), 0.0)

    def test_gaussian_gravity_does_not_fix_eta(self):
        self.assertIsNone(required_eta_n(0.0))

    def test_incomplete_flow_refuses_a_fake_calculation(self):
        with self.assertRaises(IncompleteFlowError):
            FlowSpecification().beta([0.0] * 41)

    def test_scalar_core_has_gaussian_real_fixed_point(self):
        self.assertEqual(beta_scalar((0.0, 0.0, 0.0)), (0.0, 0.0, 0.0))
        self.assertTrue(only_real_one_loop_fixed_point((0.0, 0.0, 0.0)))
        self.assertFalse(only_real_one_loop_fixed_point((0.19, 0.14, 0.05)))

    def test_scalar_core_is_positive_at_reported_like_candidate(self):
        flow = beta_scalar((0.19, 0.14, 0.05))
        self.assertGreater(flow[0], 0.0)
        self.assertGreater(flow[1], 0.0)
        self.assertTrue(bounded_from_below((0.19, 0.14, 0.05)))

    def test_higgs_plus_two_singlet_tensor_reduces_to_known_higgs_coefficient(self):
        # For p=0, O(4) scalar theory gives beta(lambda_H)=24 lambda_H^2/(16 pi^2).
        lambda_h = 0.13
        beta = beta_scalar_quartics((lambda_h, 0.0, 0.0, 0.0, 0.0, 0.0))
        self.assertAlmostEqual(beta[0], 24.0 * lambda_h**2 / (16.0 * 3.141592653589793**2))

    def test_higgs_plus_two_singlet_tensor_vanishes_at_gaussian_point(self):
        self.assertEqual(beta_scalar_quartics((0.0,) * 6), (0.0,) * 6)

    def test_sm_gauge_core_has_only_gaussian_one_loop_fixed_point(self):
        self.assertEqual(beta_gauge((0.0, 0.0, 0.0)), (0.0, 0.0, -0.0))
        self.assertTrue(one_loop_fixed_point((0.0, 0.0, 0.0)))
        self.assertFalse(one_loop_fixed_point((0.357, 0.652, 1.221)))
        beta = beta_gauge((0.357, 0.652, 1.221))
        self.assertGreater(beta[0], 0.0)
        self.assertLess(beta[1], 0.0)
        self.assertLess(beta[2], 0.0)

    def test_coupled_matter_baseline_has_finite_short_rg_step(self):
        seed = (0.357, 0.652, 1.221, 0.936, 0.024, 0.010, 0.13, 0.19, 0.14, 0.01, 0.01, 0.05)
        self.assertEqual(len(matter_beta(seed)), 12)
        result = rk4(seed, 0.01, 10)
        self.assertEqual(len(result), 12)
        self.assertTrue(all(abs(x) < 10 for x in result))

    def test_scalar_lpa_hessian_and_trace_at_origin(self):
        matrix = mass_matrix((0.0,) * 6, (0.1, 0.2, 0.3), (0.13, 0.19, 0.14, 0.01, 0.01, 0.05))
        self.assertEqual(tuple(matrix.diagonal()), (0.1, 0.1, 0.1, 0.1, 0.2, 0.3))
        self.assertGreater(litim_potential_flow((0.0,) * 6, (0.1, 0.2, 0.3), (0.13, 0.19, 0.14, 0.01, 0.01, 0.05)), 0.0)

    def test_scalar_lpa_projection_returns_all_potential_coordinates(self):
        projected = project_scalar_potential_flow((0.1, 0.2, 0.3), (0.13, 0.19, 0.14, 0.01, 0.01, 0.05))
        self.assertEqual(set(projected), {"mH2", "mPhi2", "mE2", "lambdaH", "lambdaPhi", "lambdaE", "pHPhi", "pHE", "pPhiE"})
        self.assertTrue(all(np.isfinite(value) for value in projected.values()))

    def test_partial_41_flow_reports_missing_sectors(self):
        info = coverage([0.0] * 41)
        self.assertEqual(len(info["derived"]), 33)
        self.assertIn("gN", info["derived"])
        self.assertIn("lambdaN", info["derived"])
        self.assertIn("mH2", info["derived"])
        self.assertIn("Z_h", info["derived"])
        self.assertIn("xiH", info["derived"])
        self.assertIn("c_H6", info["derived"])
        self.assertEqual(info["missing"],
                         ("a_R2", "a_C2", "c_HBox", "c_PhiBox", "c_EBox",
                          "c_HF2", "c_PhiF2", "c_EF2"))

    def test_partial_41_joint_solve_gravity_at_dep_sm_fixed_point_matter_gaussian(self):
        from partial_flow_41 import gravity_beta_dep
        lam_dep, g_dep = dep_fixed_point(improved=False,
                                         ghost_factor=DEP_TABLE_GHOST_FACTOR,
                                         seed=(-2.399, 1.762), **STANDARD_MODEL)
        couplings = [0.0] * 41
        couplings[INDEX["lambdaN"]] = 2.0 * lam_dep
        couplings[INDEX["gN"]] = g_dep
        beta_lam, beta_g = gravity_beta_dep(couplings, 4.0, 22.5, 12.0,
                                            improved=False,
                                            ghost_factor=DEP_TABLE_GHOST_FACTOR)
        self.assertAlmostEqual(beta_lam, 0.0, places=10)
        self.assertAlmostEqual(beta_g, 0.0, places=10)
        for name in ("g1", "g2", "g3", "yt", "yb", "ytau", "lambdaH",
                     "lambdaPhi", "lambdaE", "kappaHPhi", "kappaHE", "kappaPhiE"):
            self.assertEqual(0.0, couplings[INDEX[name]])
        self.assertAlmostEqual(2.0 * lam_dep, -4.798, places=3)
        self.assertAlmostEqual(g_dep, 1.762, places=3)
        values = beta_partial(couplings)
        for name in ("mH2", "mPhi2", "mE2", "Z_h", "Z_phi", "Z_E",
                     "xiH", "xiPhi", "xiE"):
            self.assertAlmostEqual(values[INDEX[name]], 0.0, places=12)
        for name in ("c_H6", "c_Phi6", "c_E6", "c_H4Phi2", "c_H4E2",
                     "c_H2Phi4", "c_H2E4", "c_Phi4E2", "c_Phi2E4",
                     "c_H2Phi2E2"):
            self.assertAlmostEqual(values[INDEX[name]], 0.0, places=9)

    def test_partial_41_dep_gravity_block_matches_pure_gravity_fixed_point(self):
        lam_dep, g_dep = 0.01046, 0.7725
        couplings = [0.0] * 41
        couplings[INDEX["lambdaN"]] = 2.0 * lam_dep
        couplings[INDEX["gN"]] = g_dep
        values = beta_partial(couplings, gravity="dep", gravity_counts=(0.0, 0.0, 0.0))
        self.assertAlmostEqual(values[INDEX["gN"]], 0.0, places=4)
        self.assertAlmostEqual(values[INDEX["lambdaN"]], 0.0, places=4)
        beta_lit, beta_lit_g = dep_beta(lam_dep, g_dep, 0.0, 0.0, 0.0, improved=False,
                                        ghost_factor=DEP_TABLE_GHOST_FACTOR)
        self.assertAlmostEqual(values[INDEX["gN"]], beta_lit_g, places=12)
        self.assertAlmostEqual(values[INDEX["lambdaN"]], 2.0 * beta_lit, places=12)

    def test_partial_41_requires_complete_flow_still_refuses_incomplete(self):
        with self.assertRaises(RuntimeError):
            requires_complete_flow([0.0] * 41)

    def test_canonical_scaling_matches_dimensions(self):
        point = [0.0] * 41
        point[INDEX["gN"]], point[INDEX["mH2"]], point[INDEX["c_H6"]] = 0.27, 0.5, 0.1
        beta = beta_canonical(point)
        self.assertAlmostEqual(beta[INDEX["gN"]], 0.54)
        self.assertAlmostEqual(beta[INDEX["mH2"]], -1.0)
        self.assertAlmostEqual(beta[INDEX["c_H6"]], 0.2)

    def test_litim_einstein_hilbert_d4_benchmark_fixed_point(self):
        lam, g = d4_fixed_point()
        beta_lam, beta_g = litim_beta(lam, g)
        self.assertAlmostEqual(beta_lam, 0.0, places=12)
        self.assertAlmostEqual(beta_g, 0.0, places=12)
        self.assertAlmostEqual(litim_eta(lam, g), -2.0, places=12)
        exponents = litim_exponents(lam, g)
        expected = 5.0/3.0
        self.assertTrue(all(abs(value.real - expected) < 1e-5 for value in exponents))
        self.assertTrue(all(abs(abs(value.imag) - (167.0**0.5)/3.0) < 1e-5 for value in exponents))

    def test_litim_threshold_closed_forms_match_defining_integrals(self):
        for n, p, w in [(1, 1, 0.0), (2, 1, 0.0), (2, 2, 0.5), (3, 2, -0.25), (4, 1, 1.0)]:
            self.assertAlmostEqual(Phi(n, p, w), Phi_integral(n, p, w), places=6)
            self.assertAlmostEqual(Phi_tilde(n, p, w), Phi_tilde_integral(n, p, w), places=6)
        self.assertAlmostEqual(Phi(2, 1, 0.0), 0.5)
        self.assertAlmostEqual(Phi_tilde(2, 1, 0.0), 1.0/6.0)
        self.assertEqual(Q_n_threshold(2, "dP/P"), 1.0)

    def test_gravity_frg_reconstruction_coordinates_reproduce_litim_fixed_point(self):
        lam_star, g_star = frg_fixed_point()
        self.assertAlmostEqual(lam_star, 0.25, places=9)
        self.assertAlmostEqual(g_star, 1.0 / (64.0 * c_d()), places=9)
        beta_lam, beta_g = frg_beta(lam_star, g_star)
        self.assertAlmostEqual(beta_lam, 0.0, places=10)
        self.assertAlmostEqual(beta_g, 0.0, places=10)
        self.assertAlmostEqual(eta_n(lam_star, g_star), -2.0, places=9)
        lam_eq, g_eq_val = fixed_point_equation_level()
        self.assertAlmostEqual(lam_eq, 0.25, places=9)
        self.assertAlmostEqual(g_eq_val, 1.0/64.0, places=9)
        lam_p, g_p = fixed_point_paper_coordinates()
        self.assertAlmostEqual(lam_p, 0.25, places=9)
        self.assertAlmostEqual(g_p, 3.0*np.pi/8.0, places=9)
        exponents = frg_exponents(lam_star, g_star)
        self.assertTrue(all(abs(value.real - 5.0/3.0) < 1e-3 for value in exponents))
        self.assertTrue(all(abs(abs(value.imag) - (167.0**0.5)/3.0) < 1e-3 for value in exponents))

    def test_dep_beta_functions_vanish_at_published_fixed_points_with_table_etas(self):
        import math
        import gravity_matter_coupling as gmc

        def beta_with_etas(lam, g, ns, nd, nv, eh, ec, es, ed, ev):
            d = gmc.D
            pre = (4.0 * np.pi) ** (d/2.0) * math.gamma(d/2.0)
            inv = 1.0/(1.0 - 2.0*lam)
            term1 = (d*(d+1.0)*(d+2.0-eh)*inv - 4.0*d*(d+2.0-ec)
                     + 2.0*ns*(2.0+d-es) - 2.0*nd*gmc.SPINOR_WEIGHT*(2.0+d-ed)
                     + 2.0*nv*(d**2-4.0-d*ev))
            term2 = (d*(5.0*d-7.0)*(d-eh)*inv + 4.0*(d+6.0)*(d-ec)
                     - 2.0*ns*(d-es) - nd*gmc.SPINOR_WEIGHT*(d-ed)
                     + 2.0*nv*(d*(8.0-d)-(6.0-d)*ev))
            bl = (-2.0*lam + 8.0*np.pi*g*term1/(pre*d*(d+2.0))
                  - 4.0*np.pi*g*lam*term2/(3.0*d*pre))
            bg = (d-2.0)*g - 4.0*np.pi*g**2*term2/(3.0*d*pre)
            return bl, bg
        cases = [
            (0, 0, 0.7725, 0.01046, 0.2690, -0.8065, -0.3384, -0.5014, -0.1843, 0.0),
            (4, 22.5, 1.762, -2.399, 2.983, -0.139, -0.076, -0.015, -0.133, 12.0),
        ]
        for ns, nd, G, L, eh, ec, es, ed, ev, nv in cases:
            bl, bg = beta_with_etas(L, G, ns, nd, nv, eh, ec, es, ed, ev)
            self.assertLess(abs(bl), 5e-3)
            self.assertLess(abs(bg), 5e-3)

    def test_dep_table_convention_reproduces_published_pure_gravity_benchmark(self):
        lam, g = dep_fixed_point(0, 0, 0, improved=False,
                                 ghost_factor=DEP_TABLE_GHOST_FACTOR,
                                 seed=(0.01046, 0.7725))
        self.assertAlmostEqual(lam, 0.01046, places=4)
        self.assertAlmostEqual(g, 0.7725, places=4)
        eta_h, eta_c, eta_s, eta_d, eta_v = eta_system(lam, g, improved=False,
                                                       ghost_factor=DEP_TABLE_GHOST_FACTOR)
        self.assertAlmostEqual(eta_h, 0.2690, places=4)
        self.assertAlmostEqual(eta_c, -0.8065, places=4)
        exponents = np.sort(dep_exponents(lam, g, improved=False,
                                          ghost_factor=DEP_TABLE_GHOST_FACTOR).real)
        self.assertAlmostEqual(exponents[1], 3.299, places=3)
        self.assertAlmostEqual(exponents[0], 1.951, places=3)

    def test_dep_table_convention_reproduces_published_standard_model_benchmark(self):
        lam, g = dep_fixed_point(improved=False, ghost_factor=DEP_TABLE_GHOST_FACTOR,
                                 seed=(-2.399, 1.762), **STANDARD_MODEL)
        self.assertAlmostEqual(lam, -2.399, places=3)
        self.assertAlmostEqual(g, 1.762, places=3)
        eta = eta_system(lam, g, improved=False, ghost_factor=DEP_TABLE_GHOST_FACTOR,
                         **STANDARD_MODEL)
        for computed, published, atol in zip(eta, (2.983, -0.139, -0.076, -0.015, -0.133),
                                             (1e-2, 1e-2, 1e-3, 1e-3, 1e-3)):
            self.assertAlmostEqual(computed, published, delta=atol)
        exponents = np.sort(dep_exponents(lam, g, improved=False,
                                          ghost_factor=DEP_TABLE_GHOST_FACTOR,
                                          **STANDARD_MODEL).real)
        self.assertAlmostEqual(exponents[1], 3.961, places=3)
        self.assertAlmostEqual(exponents[0], 1.644, places=3)

    def test_dep_printed_eta_c_equation_differs_from_table_benchmark(self):
        eta_printed = eta_system(0.01046, 0.7725, improved=False, ghost_factor=1.0)
        self.assertAlmostEqual(eta_printed[1], -0.1008, places=4)
        self.assertAlmostEqual(eta_printed[1] * DEP_TABLE_GHOST_FACTOR, -0.8065, places=3)

    def test_dep_perturbative_expansion_has_standard_model_fixed_point(self):
        lam, g = perturbative_fixed_point(**STANDARD_MODEL)
        bl, bg = beta_perturbative(lam, g, **STANDARD_MODEL)
        self.assertLess(abs(bl), 1e-12)
        self.assertLess(abs(bg), 1e-12)
        self.assertAlmostEqual(lam, -1.5, places=9)
        self.assertAlmostEqual(g, 12.0*np.pi/45.0, places=9)

    def test_cpr_r2_block_reproduces_published_fixed_points(self):
        rep, attr = omega_fixed_points()
        self.assertAlmostEqual(rep, -5.467, places=3)
        self.assertAlmostEqual(attr, -0.0228, delta=1e-4)
        self.assertAlmostEqual(theta_star(), 0.3275, places=4)
        lam_t, g_t = r2_newton_fixed_point()
        self.assertAlmostEqual(lam_t, 0.221, places=3)
        self.assertAlmostEqual(g_t, 1.389, places=3)
        self.assertAlmostEqual(q_omega(attr), 1.440, places=3)
        self.assertAlmostEqual(beta_g_tilde_rsq(g_t, 0.0, attr), 0.0, places=10)
        self.assertAlmostEqual(beta_lambda_tilde_rsq(lam_t, g_t, 0.0, attr), 0.0, places=10)

    def test_cpr_omega_conversion_matches_chain_rule(self):
        lam, omega = 0.1, omega_fixed_points()[1]
        xi = -3.0 * lam / omega
        printed = beta_omega_rsq(lam, omega)
        chain = -3.0 * (beta_lambda_rsq(lam) / xi - lam * beta_xi_rsq(lam, xi) / xi**2)
        self.assertAlmostEqual(printed, chain, places=12)

    def test_cpr_r2_coordinate_flows_match_chain_rule(self):
        a_r2, a_c2 = 0.05, 0.4
        lam, xi = 1.0 / (2.0 * a_c2), 1.0 / a_r2
        self.assertAlmostEqual(a_c2_beta(), -beta_lambda_rsq(lam) / (2.0 * lam**2), places=12)
        self.assertAlmostEqual(a_r2_beta(a_r2, a_c2), -beta_xi_rsq(lam, xi) / xi**2, places=12)

    def test_partial_41_r2_entries_finite_off_gaussian_singular_at_gaussian(self):
        couplings = [0.0] * 41
        couplings[INDEX["a_R2"]] = 0.05
        couplings[INDEX["a_C2"]] = 0.4
        values = beta_partial(couplings)
        self.assertTrue(np.isfinite(values[INDEX["a_R2"]]))
        self.assertTrue(np.isfinite(values[INDEX["a_C2"]]))
        self.assertAlmostEqual(values[INDEX["a_C2"]], a_c2_beta(), places=12)
        gaussian = beta_partial([0.0] * 41)
        self.assertTrue(np.isnan(gaussian[INDEX["a_R2"]]))
        self.assertTrue(np.isnan(gaussian[INDEX["a_C2"]]))

    def test_np_gmfp_reproduces_published_fixed_point(self):
        from scalar_tensor_nonminimal_np import (beta_gmfp_pair,
                                                 GMFP_LAM0_STAR, GMFP_XI0_STAR)
        beta_lam, beta_xi = beta_gmfp_pair(GMFP_LAM0_STAR, GMFP_XI0_STAR)
        self.assertLess(abs(beta_lam), 1e-6)
        self.assertLess(abs(beta_xi), 1e-6)
        self.assertAlmostEqual(GMFP_LAM0_STAR, 0.00862, places=5)
        self.assertAlmostEqual(GMFP_XI0_STAR, 0.02375, places=4)

    def test_np_critical_exponents_and_eigenvector_reproduce_published(self):
        from scalar_tensor_nonminimal_np import (beta_gmfp_pair,
                                                 GMFP_LAM0_STAR, GMFP_XI0_STAR)
        point = np.array([GMFP_LAM0_STAR, GMFP_XI0_STAR])
        jacobian = np.zeros((2, 2))
        step = 1e-7
        for axis in range(2):
            offset = np.zeros(2)
            offset[axis] = step
            jacobian[:, axis] = (np.array(beta_gmfp_pair(*(point + offset)))
                                 - np.array(beta_gmfp_pair(*(point - offset)))) / (2.0 * step)
        values, vectors = np.linalg.eig(jacobian)
        self.assertEqual(len(values), 2)
        real = [value.real for value in values]
        imag = [value.imag for value in values]
        self.assertEqual(len(real), 2)
        theta_real = [-r for r in real]
        theta_imag = [-i for i in imag]
        self.assertAlmostEqual(theta_real[0], 2.143, places=2)
        self.assertAlmostEqual(abs(theta_imag[0]), 2.879, places=2)
        self.assertAlmostEqual(theta_real[0], theta_real[1], places=9)
        self.assertAlmostEqual(theta_imag[0], -theta_imag[1], places=9)
        for value, vector in zip(values, vectors.T):
            if abs(value.imag) < 1e-6:
                continue
            norm = np.sqrt(abs(vector[0])**2 + abs(vector[1])**2)
            self.assertAlmostEqual(abs(vector[0]) / norm, 0.5199, places=2)
            self.assertAlmostEqual(vector[1] / norm, 0.8549, places=2)

    def test_np_gaussian_matter_is_exact_fixed_point_of_xi_flow(self):
        from scalar_tensor_nonminimal_np import (beta_xi_matter, beta_lam2_tilde,
                                                 beta_xi2_tilde, beta_lam4_tilde,
                                                 solve_eta, GMFP_LAM0_STAR,
                                                 GMFP_XI0_STAR)
        self.assertAlmostEqual(beta_xi_matter(0.0, 0.0, 0.0), 0.0, places=12)
        eta = solve_eta(GMFP_LAM0_STAR, GMFP_XI0_STAR, 0.0, 0.0)
        self.assertAlmostEqual(eta, 2.0, places=9)
        self.assertAlmostEqual(beta_lam2_tilde(GMFP_LAM0_STAR, GMFP_XI0_STAR, 0.0, 0.0, 0.0),
                               0.0, places=12)
        self.assertAlmostEqual(beta_xi2_tilde(GMFP_LAM0_STAR, GMFP_XI0_STAR, 0.0, 0.0, 0.0),
                               0.0, places=12)
        self.assertAlmostEqual(beta_lam4_tilde(GMFP_LAM0_STAR, GMFP_XI0_STAR, 0.0, 0.0, 0.0),
                               0.0, places=12)

    def test_np_xi_entries_finite_off_fixed_point(self):
        couplings = [0.0] * 41
        couplings[INDEX["mH2"]] = 0.1
        couplings[INDEX["lambdaH"]] = 0.05
        couplings[INDEX["xiH"]] = 0.02
        couplings[INDEX["mPhi2"]] = 0.2
        couplings[INDEX["lambdaPhi"]] = 0.07
        couplings[INDEX["xiPhi"]] = -0.03
        values = beta_partial(couplings)
        self.assertTrue(np.isfinite(values[INDEX["xiH"]]))
        self.assertTrue(np.isfinite(values[INDEX["xiPhi"]]))
        self.assertTrue(np.isfinite(values[INDEX["xiE"]]))
        self.assertNotAlmostEqual(values[INDEX["xiH"]], 0.0)

    def test_sextic_tensor_convention_matches_radial_potential(self):
        from sextic_lpa import sextic_tensor, mass_matrix_sextic
        tensor = sextic_tensor((0.1, 0.2, 0.3, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11))
        self.assertAlmostEqual(tensor[0, 0, 0, 0, 0, 0], 90.0 * 0.1)
        self.assertAlmostEqual(tensor[0, 0, 0, 0, 1, 1], 18.0 * 0.1)
        self.assertAlmostEqual(tensor[0, 0, 0, 0, 4, 4], 6.0 * 0.05)
        self.assertAlmostEqual(tensor[0, 0, 4, 4, 5, 5], 0.11)
        radial = 0.07
        hessian = mass_matrix_sextic((radial, 0.0, 0.0, 0.0, 0.0, 0.0),
                                     (0.0, 0.0, 0.0), (0.0,) * 6,
                                     (0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        self.assertAlmostEqual(hessian[0, 0], 3.75 * 0.1 * radial**4)

    def test_sextic_tensor_reproduces_monomials(self):
        from sextic_lpa import sextic_tensor
        from higgs_two_singlet_core import quartic_tensor
        def potential_radial(background, couplings):
            field = np.asarray(background, dtype=float)
            h2 = np.sum(field[:4] ** 2)
            phi2 = field[4] ** 2
            e2 = field[5] ** 2
            quartic = ((couplings[0] / 4.0) * h2 * h2 + (couplings[1] / 4.0) * phi2 * phi2)
            sextic = ((couplings[2] / 8.0) * h2 ** 3 + (couplings[3] / 8.0) * e2 ** 3
                      + (couplings[5] / 8.0) * h2 ** 2 * phi2
                      + (couplings[4] / 8.0) * h2 * phi2 * e2)
            return quartic + sextic
        def tensor_potential(background, couplings):
            field = np.asarray(background, dtype=float)
            lam = quartic_tensor((couplings[0], couplings[1], 0.0, 0.0, 0.0, 0.0))
            cee = sextic_tensor((couplings[2], 0.0, couplings[3], couplings[5], 0.0, 0.0,
                                 0.0, 0.0, 0.0, couplings[4]))
            return (np.einsum("abcd,a,b,c,d->", lam, field, field, field, field) / 24.0
                    + np.einsum("abcdef,a,b,c,d,e,f->", cee, field, field, field, field, field, field) / 720.0)
        couplings = (0.1, 0.05, 0.02, 0.01, 0.001, 0.03)
        for point in ((0.05, 0.0, 0.0, 0.0, 0.0, 0.0),
                      (0.03, 0.04, 0.0, 0.0, 0.0, 0.0),
                      (0.02, 0.01, 0.0, 0.0, 0.05, 0.0),
                      (0.01, 0.02, 0.0, 0.0, 0.03, 0.04)):
            direct = potential_radial(point, couplings)
            tensor = tensor_potential(point, couplings)
            self.assertAlmostEqual(tensor, direct, places=12)

    def test_sextic_projection_matches_analytic_toy_derivatives(self):
        from sextic_lpa import _mixed_derivative
        def toy(point):
            h, phi, e = point
            return (h * h + phi * phi + e * e) ** 3
        step = 0.01
        self.assertAlmostEqual(_mixed_derivative(toy, [(0, 6)], step), 720.0, places=6)
        self.assertAlmostEqual(_mixed_derivative(toy, [(0, 4), (1, 2)], step), 144.0, places=6)
        self.assertAlmostEqual(_mixed_derivative(toy, [(0, 2), (1, 2), (2, 2)], step), 48.0, places=6)

    def test_sextic_flow_matches_quartic_flow_at_zero_sextics(self):
        from sextic_lpa import litim_potential_flow_sextic
        masses = (0.1, 0.2, 0.3)
        quartics = (0.13, 0.19, 0.14, 0.01, 0.01, 0.05)
        for point in ((0.0, 0.0, 0.0), (0.1, 0.2, 0.3), (-0.05, 0.0, 0.15)):
            background = (point[0], 0.0, 0.0, 0.0, point[1], point[2])
            old = litim_potential_flow(background, masses, quartics)
            new = litim_potential_flow_sextic(background, masses, quartics, (0.0,) * 10)
            self.assertEqual(old, new)

    def test_sextic_entries_vanish_at_gaussian_and_are_step_stable(self):
        from sextic_lpa import project_sextic_flow, SEXTIC_NAMES
        gaussian = project_sextic_flow((0.0, 0.0, 0.0), (0.0,) * 6, (0.0,) * 10)
        for name in SEXTIC_NAMES:
            self.assertLess(abs(gaussian[name]), 1e-9)
        masses = (0.1, 0.05, 0.0)
        quartics = (0.1, 0.05, 0.02, 0.01, 0.0, 0.0)
        sextics = (0.02, 0.01, 0.005, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        small = project_sextic_flow(masses, quartics, sextics, step=3e-2)
        large = project_sextic_flow(masses, quartics, sextics, step=7e-2)
        for name in ("c_H6", "c_Phi6", "c_E6", "c_H4Phi2"):
            self.assertLess(abs(small[name] - large[name]) / abs(small[name]), 5e-2)

    def test_partial_41_sextic_entries_finite_off_gaussian(self):
        couplings = [0.0] * 41
        couplings[INDEX["mH2"]] = 0.1
        couplings[INDEX["mPhi2"]] = 0.05
        couplings[INDEX["lambdaH"]] = 0.1
        couplings[INDEX["lambdaPhi"]] = 0.05
        couplings[INDEX["c_H6"]] = 0.02
        couplings[INDEX["c_Phi6"]] = 0.01
        values = beta_partial(couplings)
        for name in ("c_H6", "c_Phi6", "c_E6", "c_H4Phi2", "c_H4E2",
                     "c_H2Phi4", "c_H2E4", "c_Phi4E2", "c_Phi2E4",
                     "c_H2Phi2E2"):
            self.assertTrue(np.isfinite(values[INDEX[name]]))
        self.assertNotAlmostEqual(values[INDEX["c_H6"]], 0.0)

    def test_joint_fixed_point_is_fixed_point_of_full_flow(self):
        from joint_fixed_point_stability import (joint_fixed_point_couplings,
                                                 full_flow, DERIVED, MISSING)
        point = joint_fixed_point_couplings()
        values = full_flow(point, canonical=True)
        for name in DERIVED:
            self.assertTrue(np.isfinite(values[INDEX[name]]))
            self.assertLess(abs(values[INDEX[name]]), 1e-9, name)
        for name in MISSING:
            self.assertTrue(np.isnan(values[INDEX[name]]), name)

    def test_joint_fp_gravity_eigenvalues_match_dep_benchmark(self):
        from joint_fixed_point_stability import stability_spectrum
        thetas, _ = stability_spectrum()
        real = [theta.real for theta in thetas]
        self.assertAlmostEqual(max(real), 3.961, places=2)
        self.assertIn(1.644, [round(value, 3) for value in real])

    def test_joint_fp_spectrum_block_structure(self):
        from joint_fixed_point_stability import stability_spectrum
        thetas, _ = stability_spectrum()
        real = [theta.real for theta in thetas]
        relevant = sum(1 for value in real if value > 1e-3)
        marginal = sum(1 for value in real if abs(value) <= 1e-3)
        irrelevant = sum(1 for value in real if value < -1e-3)
        self.assertEqual(len(thetas), 33)
        self.assertEqual(relevant, 8)
        self.assertEqual(marginal, 12)
        self.assertEqual(irrelevant, 13)
        mass_squared = [value for value in real if abs(value - 2.8554) < 1e-2]
        xi = [value for value in real if abs(value - 2.0) < 1e-2]
        z = [value for value in real if abs(value - (-0.0756)) < 1e-2]
        dim6 = [value for value in real if abs(value - (-2.0)) < 1e-2]
        self.assertEqual(len(mass_squared), 3)
        self.assertEqual(len(xi), 3)
        self.assertEqual(len(z), 3)
        self.assertEqual(len(dim6), 10)

    def test_cpr_ac2_has_no_fixed_point_and_ar2_zero_lines(self):
        from r2_gravity_cpr import a_c2_beta, a_r2_beta
        self.assertGreater(a_c2_beta(), 0.0)
        self.assertAlmostEqual(a_c2_beta(), 133.0 / (320.0 * np.pi**2), places=12)
        discriminant = 25.0 - 4.0 * 10.0 * 5.0 / 36.0
        self.assertGreater(discriminant, 0.0)
        x1 = (5.0 + discriminant**0.5) / 20.0
        x2 = (5.0 - discriminant**0.5) / 20.0
        for x in (x1, x2):
            a_c2 = 0.4
            self.assertAlmostEqual(a_r2_beta(2.0 * x * a_c2, a_c2), 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
