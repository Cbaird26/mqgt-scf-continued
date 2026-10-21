"""Reproduce and extend a pinned partial UV reconstruction without claiming closure.

Run: python continue_uv.py
Optional slow upstream finite-difference comparison:
     python continue_uv.py --reference-difference
Outputs are local results.json, nonlinear_flows.csv, projection_contract.json,
and provenance.json. No network access or repository mutation is performed.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import csv
import hashlib
import json
from math import pi, sqrt
from pathlib import Path
import platform
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
UPSTREAM = HERE / "upstream"
sys.path.insert(0, str(UPSTREAM))

import gravity_matter_coupling as dep
import higgs_two_singlet_core as tensor
import joint_fixed_point_stability as joint
import partial_flow_41 as partial
import perturbative_matter_baseline as matter
import r2_gravity_cpr as cpr
from model import INDEX, NAMES
from scalar_tensor_nonminimal_np import beta_xi_matter, GMFP_LAM0_STAR, GMFP_XI0_STAR
from sextic_lpa import litim_potential_flow_sextic

from scalar_polynomial_projection import project, trace_polynomial, QUARTIC_NAMES, SEXTIC_NAMES

COMMIT = "0a644a41eb947509280cbd648996d98bad54bdc5"
BASE_URL = f"https://github.com/Cbaird26/uv-reconstruction-frg/blob/{COMMIT}/"


def native(value):
    if isinstance(value, dict):
        return {str(k): native(v) for k, v in value.items()}
    if isinstance(value, (tuple, list, np.ndarray)):
        return [native(x) for x in value]
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, (complex, np.complexfloating)):
        return {"real": float(value.real), "imag": float(value.imag)}
    return value


def write_json(name, data):
    (HERE / name).write_text(json.dumps(native(data), indent=2, allow_nan=False) + "\n")


@contextmanager
def exact_scalar_projectors():
    """Replace only existing scalar mass/sextic evaluations in memory.

    The assembled vector field's omitted sextic-to-quartic feedback is not
    silently inserted. That incompleteness is measured and reported below.
    Upstream source files are never modified.
    """
    old_mass = partial.project_scalar_potential_flow
    old_sextic = partial.project_sextic_flow
    partial.project_scalar_potential_flow = lambda masses, quartics: project(masses, quartics)
    partial.project_sextic_flow = lambda masses, quartics, sextics: project(masses, quartics, sextics)
    try:
        yield
    finally:
        partial.project_scalar_potential_flow = old_mass
        partial.project_sextic_flow = old_sextic


def scalar_validation():
    checks = []
    # Independent one-field resolvent expansion with nonzero mass/quartic/sextic.
    mass, lam, c = 0.2, 0.03, 0.004
    q = [0.0] * 6
    q[1] = lam
    s = [0.0] * 10
    s[1] = c
    result = project((0.0, mass, 0.0), q, s)
    d, pref = 1.0 + mass, 1.0 / (32.0 * pi**2)
    expected = {
        "mPhi2": -6.0 * lam / d**2 * pref,
        "lambdaPhi": (36.0 * lam**2 / d**3 - 15.0 * c / d**2) * pref,
        "c_Phi6": (180.0 * lam * c / d**3 - 216.0 * lam**3 / d**4) * pref,
    }
    error = max(abs(result[k] - v) for k, v in expected.items())
    assert error < 1e-16, (result, expected)
    checks.append({"name": "independent_single_scalar_resolvent", "max_absolute_error": error})

    # Exact tensor contraction is independent of the polynomial Hessian implementation.
    rng = np.random.default_rng(20261021)
    error = 0.0
    for _ in range(12):
        q = rng.uniform(0.0, 0.15, size=6)
        projected = project(quartics=q)
        target = tensor.beta_scalar_quartics(q)
        error = max(error, max(abs(projected[n] - v) for n, v in zip(QUARTIC_NAMES, target)))
    assert error < 1e-15, error
    checks.append({"name": "twelve_scalar_tensor_quartic_comparisons", "max_absolute_error": error})

    # Direct six-component Hessian trace verifies Goldstone multiplicity and cross terms.
    masses = (0.02, 0.03, 0.04)
    q = (0.08, 0.04, 0.06, 0.01, 0.02, 0.015)
    s = tuple(0.001 * (i + 1) for i in range(10))
    h = (0.02, -0.015, 0.01)
    polynomial = trace_polynomial(masses, q, s)
    value = sum(v * np.prod([h[i] ** p[i] for i in range(3)]) for p, v in polynomial.items())
    direct = litim_potential_flow_sextic((h[0], 0.0, 0.0, 0.0, h[1], h[2]), masses, q, s)
    error = abs(value - direct)
    assert error < 1e-12, error
    checks.append({"name": "six_component_trace_small_field_remainder", "absolute_error": error,
                   "interpretation": "Agreement includes a nonzero O(field^8) truncation remainder."})
    try:
        project(masses=(-1.0, 0.0, 0.0))
        raise AssertionError("regulator pole accepted")
    except ValueError:
        checks.append({"name": "singular_scalar_chart_rejected", "passed": True})
    return checks


def gravity_benchmark(n_s):
    arguments = dict(n_s=float(n_s), n_d=22.5, n_v=12.0, improved=False,
                     ghost_factor=dep.DEP_TABLE_GHOST_FACTOR)
    lam, g = dep.fixed_point(seed=(-2.399, 1.762), **arguments)
    beta_lam, beta_g = dep.beta(lam, g, **arguments)
    etas = dep.eta_system(lam, g, **arguments)
    assert max(abs(beta_lam), abs(beta_g)) < 1e-11
    return {
        "scope": "DEP gravity block only, massless minimally coupled scalar census",
        "matter_census": {"real_scalars": n_s, "dirac_equivalents": 22.5, "vectors": 12},
        "coordinates": {"Lambda_tilde": lam, "gN_equals_G_tilde": g, "lambdaN_equals_2Lambda_tilde": 2.0 * lam},
        "beta_residual": {"beta_Lambda_tilde": beta_lam, "beta_gN": beta_g},
        "critical_exponents": dep.critical_exponents(lam, g, **arguments),
        "eta_N_defined_from_background_newton_beta": beta_g / g - 2.0,
        "fluctuation_etas": dict(zip(("eta_h", "eta_ghost", "eta_scalar", "eta_fermion", "eta_vector"), etas)),
    }


def spectrum_summary(theta, matrix):
    return {
        "coordinate_count": len(theta),
        "sign_counts_tolerance_1e-6": {
            "positive_real_part": int(np.sum(theta.real > 1e-6)),
            "zero_within_tolerance": int(np.sum(np.abs(theta) <= 1e-6)),
            "negative_real_part": int(np.sum(theta.real < -1e-6)),
        },
        "theta_convention": "theta = -eig(d beta / d u)",
        "theta": [complex(z) for z in theta],
        "jacobian_coordinate_order": joint.DERIVED,
        "jacobian_diagonal": {name: matrix[i, i] for i, name in enumerate(joint.DERIVED)},
        "interpretation": "Formal spectrum of the supplied assembled partial vector field; incompatible projection conventions prevent a common physical fixed-point interpretation.",
    }


def rk4_scalar(rhs, start, dt, steps):
    value = float(start)
    for _ in range(steps):
        a = rhs(value)
        b = rhs(value + 0.5 * dt * a)
        c = rhs(value + 0.5 * dt * b)
        d = rhs(value + dt * c)
        value += dt * (a + 2.0 * b + 2.0 * c + d) / 6.0
    return value


def nonlinear_analysis():
    """One-loop matter-subsystem diagnostics, not a full center-manifold solve."""
    rows, analysis = [], []
    times = (0.0, 10.0, 50.0, 100.0, 200.0)
    for name, coefficient in (("gY", 41.0 / 6.0), ("g2", -19.0 / 6.0), ("g3", -7.0)):
        start = 0.2
        pole = 8.0 * pi**2 / (coefficient * start**2) if coefficient > 0 else None
        for time in times:
            exact = start / sqrt(1.0 - coefficient * start**2 * time / (8.0 * pi**2))
            steps = max(1, round(time / 0.025))
            numeric = rk4_scalar(lambda g: coefficient * g**3 / (16.0 * pi**2), start, time / steps, steps)
            assert abs(exact - numeric) < 1e-11
            rows.append(dict(coupling=name, initial=start, t_log_k_over_k0=time,
                             analytic=exact, numerical=numeric, absolute_error=abs(exact - numeric)))
        analysis.append({"coupling": name, "initial": start, "leading_beta": f"({coefficient}) * g^3 / (16*pi^2)",
                         "classification": "marginally UV-repulsive" if coefficient > 0 else "marginally UV-attractive",
                         "formal_one_loop_pole_t": pole,
                         "scope": "Autonomous gauge subsystem; gauge fields source scalar quartics, so a gauge-only axis is not invariant in the full matter system."})
    for name, coefficient in (("lambdaH", 24.0), ("lambdaPhi", 18.0), ("lambdaE", 18.0)):
        start = 0.01
        pole = 16.0 * pi**2 / (coefficient * start)
        for time in times:
            exact = start / (1.0 - coefficient * start * time / (16.0 * pi**2))
            steps = max(1, round(time / 0.025))
            numeric = rk4_scalar(lambda lam: coefficient * lam**2 / (16.0 * pi**2), start, time / steps, steps)
            assert abs(exact - numeric) < 1e-11
            rows.append(dict(coupling=name, initial=start, t_log_k_over_k0=time,
                             analytic=exact, numerical=numeric, absolute_error=abs(exact - numeric)))
        analysis.append({"coupling": name, "initial": start, "leading_beta": f"({coefficient}) * lambda^2 / (16*pi^2)",
                         "classification": "positive quartic ray is marginally UV-repulsive in the scalar matter baseline",
                         "formal_one_loop_pole_t": pole,
                         "scope": "The self-quartic ray with other quartics, portals, gauge and Yukawa couplings zero; not a full gravity-coupled trajectory."})
    with (HERE / "nonlinear_flows.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    names = ("gY", "g2", "g3", "yt", "yb", "ytau", "lambdaH", "lambdaPhi", "lambdaE", "kappaHPhi", "kappaHE", "kappaPhiE")
    examples = []
    for name, magnitude in (("yt", 0.1), ("kappaHPhi", 0.01)):
        point = [0.0] * 12
        point[names.index(name)] = magnitude
        flow = matter.beta(point)
        examples.append({"initial_nonzero_coupling": {name: magnitude},
                         "nonzero_beta_components": {n: value for n, value in zip(names, flow) if value != 0.0},
                         "implication": "This coordinate axis is not invariant; coupled nonlinear analysis is required."})
    return {"scope": "Nonlinear diagnostics of the supplied perturbative matter baseline. No gravitational correction has been invented.",
            "t_definition": "t = ln(k/k0), UV means increasing t", "probes_are_empirical_inputs": False,
            "resolved_subsystem_behavior": analysis, "non_invariant_axis_examples": examples,
            "max_analytic_numerical_error": max(row["absolute_error"] for row in rows),
            "conclusion": "Twelve zero linear exponents do not establish twelve exactly marginal couplings. The full center manifold and gravity-corrected classifications remain uncomputed."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference-difference", action="store_true")
    options = parser.parse_args()
    checks = scalar_validation()
    benchmark4, benchmark6 = gravity_benchmark(4), gravity_benchmark(6)
    point = joint.joint_fixed_point_couplings()
    with exact_scalar_projectors():
        theta, matrix = joint.stability_spectrum(point)
        flows = joint.full_flow(point, canonical=True)
        missing = [NAMES[i] for i, v in enumerate(flows) if not np.isfinite(v)]
        finite_residual = float(max(abs(v) for v in flows if np.isfinite(v)))
        try:
            partial.requires_complete_flow(point)
            raise AssertionError("incomplete 41-dimensional flow was accepted")
        except RuntimeError as error:
            refusal = str(error)
    assert missing == [name for name in NAMES if name in joint.MISSING]
    assert finite_residual < 1e-12
    summary = spectrum_summary(theta, matrix)
    assert summary["sign_counts_tolerance_1e-6"] == {"positive_real_part": 8, "zero_within_tolerance": 12, "negative_real_part": 13}
    diag = summary["jacobian_diagonal"]
    assert all(abs(diag[name] + 2.0) < 1e-12 for name in ("mH2", "mPhi2", "mE2"))
    assert all(abs(diag[name] - 2.0) < 1e-12 for name in SEXTIC_NAMES)
    checks.append({"name": "formal_spectrum_reproduced_and_sector_assignment_checked", "passed": True})

    raw = None
    if not options.reference_difference and (HERE / "results.json").exists():
        previous = json.loads((HERE / "results.json").read_text())
        if previous.get("source_commit") == COMMIT:
            raw = previous.get("formal_partial_fixed_point", {}).get("original_nested_finite_difference_spectrum")
    if options.reference_difference:
        raw_theta, raw_matrix = joint.stability_spectrum(point)
        raw = spectrum_summary(raw_theta, raw_matrix)
        raw["max_sorted_theta_difference_from_polynomial_evaluation"] = float(max(abs(np.sort_complex(raw_theta) - np.sort_complex(theta))))

    # A new scalar feedback term absent from the assembled matter beta.
    feedback = []
    for name, quartic in (("c_H6", "lambdaH"), ("c_Phi6", "lambdaPhi"), ("c_E6", "lambdaE")):
        sextics = [0.0] * 10
        sextics[SEXTIC_NAMES.index(name)] = 1.0
        coefficient = project(sextics=sextics)[quartic]
        feedback.append({"source_sextic": name, "target_quartic": quartic,
                         "derivative_of_scalar_LPA_beta_quartic": coefficient,
                         "assembled_upstream_derivative": 0.0,
                         "interpretation": "Projection within the same scalar trace; the upstream perturbative quartic block has no sextic arguments."})

    shift = {name: (benchmark6["coordinates"][name] / benchmark4["coordinates"][name] - 1.0) * 100.0
             for name in benchmark4["coordinates"]}
    contract = {
        "status": "common_coupled_projection_not_available",
        "authority": "New audit contract, not a claim that upstream implements these requirements.",
        "dimension": 4, "RG_time": "ln(k/k0)",
        "required_scalar_census": {"H_real_components": 4, "Phi_real_components": 1, "E_real_components": 1, "total": 6},
        "coordinate_map": {"gN": "G*k^2 = G_tilde", "lambdaN": "2*Lambda/k^2 = 2*Lambda_tilde",
                           "beta_lambdaN": "2*beta_Lambda_tilde", "g1": "gY in ordinary Standard Model hypercharge normalization"},
        "coordinate_map_scope": "This records the repository DEP branch, not a universal map to the separately implemented Litim branch. A single action convention must replace the conflicting branch labels.",
        "NP_scalar_mass_matching": {"paper_potential": "V contains lambda2*phi^2", "canonical_mass_potential": "V contains m^2*phi^2/2",
                                    "required_identification_at_Z1": "lambda2=m^2/2", "upstream_wiring": "lambda2=m^2",
                                    "status": "factor-of-two mismatch; changing it alone does not reconcile backgrounds, Higgs multiplicity, or nonminimal signs"},
        "field_normalization": {"eta_i": "-d ln(Z_i)/dt", "regular_chart": "Z_i > 0, with canonically normalized fields sqrt(Z_i)*phi_i",
                                "essential_mass_squared": "m_i^2/(Z_i*k^2)", "essential_self_quartic": "lambda_i/Z_i^2",
                                "essential_sextic": "k^2*c_abc/(Z_H^a*Z_Phi^b*Z_E^c), a+b+c=3",
                                "sextic_scaling_term": "(2+a*eta_H+b*eta_Phi+c*eta_E)*c_abc_tilde"},
        "missing_at_reported_point": missing,
        "required_projection_work": [
            {"operators": ["a_R2", "a_C2"], "canonical_weight": 0,
             "required": "Choose regular higher-curvature coordinates and one gravity/matter Hessian; include mixing. Existing inverse coordinates are singular at the selected point; standalone CPR beta_aC2 is nonzero."},
            {"operators": ["c_HBox", "c_PhiBox", "c_EBox"], "canonical_weight": 2,
             "required": "Declare scalar invariant normalization, integration-by-parts/EOM basis and momentum subtraction projector; project the p^2 part of appropriate four-scalar vertices with all selected traces."},
            {"operators": ["c_HF2", "c_PhiF2", "c_EF2"], "canonical_weight": 2,
             "required": "Declare whether F denotes U(1), SU(2), SU(3), or a fixed combination. A general scalar-bilinear gauge-strength set has a separate coefficient for each scalar invariant and each gauge factor; project transverse two-gauge/two-scalar vertices."},
        ],
        "common_flow_acceptance_criteria": [
            "One explicitly defined field content, action, gauge fixing, ghost normalization and regulator prescription, or a derived matching map between schemes.",
            "All retained beta projections finite in a regular field-normalization chart; no missing entries silently replaced by zero.",
            "Gravity, scalar, gauge, Yukawa, nonminimal and higher-derivative mixing included to the declared truncation order, with controlled omission estimates.",
            "Nonzero Newton fixed point satisfies beta_gN=(2+eta_N)*gN and eta_N=-2; distinguish background eta_N from fluctuation eta_h.",
            "Residual, basis/field-normalization checks, derivative-step convergence, regulator sensitivity and truncation enlargement assessed before claiming physical critical exponents.",
            "Nonlinear analysis resolves zero linear exponents before an exact-marginality or UV-critical-surface dimension claim.",
        ],
    }
    blockers = [
        {"id": "mixed_projection_backgrounds", "severity": "blocks_common_flow", "evidence": "DEP running gravity is assembled with NP xi projections frozen at another gravity fixed point; no scheme/background matching is implemented."},
        {"id": "coordinate_normalizations", "severity": "blocks_cross_branch_identification", "evidence": "The NP lambda2=m^2 wiring conflicts with its potential/threshold convention. The separate Litim wrapper divides by c4 when recovering G*k^2 although its primary-paper fixed point requires multiplication. The DEP lambdaN=2*Lambda_tilde convention is explicitly retained only as a repository coordinate."},
        {"id": "scalar_census", "severity": "requires_model_consistent_recomputation", "evidence": "The default gravity census is four real scalars; the declared scalar Hessian contains six."},
        {"id": "kinetic_chart", "severity": "blocks_literal_physical_fixed_point", "evidence": "The reported point has all Z_i=0, while nonzero eta_scalar makes beta_Z=-eta_scalar*Z vanish only there if Z is treated as a fixed coordinate. This is not a regular canonical field chart."},
        {"id": "missing_projections", "severity": "blocks_41_coordinate_solution", "evidence": "Eight coordinates are unavailable at the chosen point; the inherited completion guard correctly refuses a full solve."},
        {"id": "incomplete_scalar_feedback", "severity": "blocks_claim_of_complete_scalar_truncation", "evidence": "The shared scalar trace gives sextic-to-quartic feedback, but the assembled matter quartic block has no sextic dependence."},
        {"id": "nonlinear_marginal_sector", "severity": "blocks_exact_marginality_claim", "evidence": "At least the gauge subsystem and positive pure self-quartic rays run at nonlinear order despite zero linear exponents."},
    ]
    results = {
        "source_commit": COMMIT,
        "research_status": "new bounded calculations complete; common coupled UV completion remains open",
        "validation": checks,
        "formal_partial_fixed_point": {"coordinates": {name: point[INDEX[name]] for name in ("gN", "lambdaN")},
                                       "all_other_retained_coordinates": 0.0, "max_finite_beta_residual": finite_residual,
                                       "missing_coordinates": missing, "full_flow_refusal": refusal,
                                       "spectrum_with_exact_scalar_polynomial_evaluation": summary,
                                       "original_nested_finite_difference_spectrum": raw},
        "corrected_sector_labels": {"mass_squared_exponents": [2.0] * 3,
                                    "nonminimal_xi_exponents": [-diag[name] for name in ("xiH", "xiPhi", "xiE")],
                                    "interpretation": "Documentation label swap; the formal sign counts do not change."},
        "gravity_census_sensitivity": {"four_scalar_source_benchmark": benchmark4, "six_scalar_conditional_benchmark": benchmark6,
                                       "coordinate_relative_change_percent": shift,
                                       "interpretation": "Changes scalar census within the same DEP block only, with no singlet threshold effects or complete mixed-sector recomputation."},
        "nonminimal_background": {"NP_lambda0_star": GMFP_LAM0_STAR, "NP_xi0_star": GMFP_XI0_STAR,
                                  "source_function_uses_running_DEP_coordinates": False},
        "normalization_audit": {
            "DEP_cosmological_map": {"repository_definition": "lambdaN=2*Lambda_tilde", "paper_coordinate_value": benchmark4["coordinates"]["Lambda_tilde"],
                                      "repository_coordinate_value": benchmark4["coordinates"]["lambdaN_equals_2Lambda_tilde"],
                                      "interpretation": "A documented reparameterization explains these two reported numbers. A regular linear reparameterization does not alter critical eigenvalues."},
            "separate_Litim_wrapper": {"c4": 24.0*pi, "equation_level_g_star": 1.0/64.0,
                                        "paper_Gk2_star": 3.0*pi/8.0, "wrapper_claimed_Gk2_star": 1.0/(1536.0*pi),
                                        "required_map": "G*k^2=c4*g_equation", "implemented_map": "g_equation=c4*gN",
                                        "ratio_paper_to_wrapper": (24.0*pi)**2,
                                        "source": "https://arxiv.org/pdf/hep-th/0606044, equations (5), (6), (11)",
                                        "effect_on_DEP_run": "None: the reproduced DEP spectrum does not call this wrapper."},
            "NP_mass_map": {"required_at_canonical_Z": "lambda2=m^2/2", "upstream_map": "lambda2=m^2",
                            "example_mass_squared": 0.2, "scalar_Hessian_threshold": 1.2,
                            "wired_NP_threshold": 1.4, "matched_NP_threshold": 1.2,
                            "source": "https://arxiv.org/pdf/0911.0386, equations (1), (25), (26)",
                            "effect_on_quoted_zero_matter_sign_counts": "This off-diagonal mass-to-xi normalization issue does not change the reproduced zero-mass diagonal exponent labels; it matters away from that point."},
        },
        "scalar_LPA_new_projection": {"scope": "One scalar Wetterich trace, six real scalars, normalized kinetic terms, through field degree six",
                                      "method": "Finite multivariate polynomial expansion of the matrix resolvent; exact Taylor coefficients in this stated truncation",
                                      "sextic_to_quartic_feedback": feedback},
        "nonlinear_matter": nonlinear_analysis(),
        "standalone_CPR_beta_aC2": cpr.a_c2_beta(),
        "common_flow_gate": {"accepted": False, "blockers": blockers},
    }
    write_json("results.json", results)
    write_json("projection_contract.json", contract)
    fetched = json.loads((UPSTREAM / "FETCH_PROVENANCE.json").read_text())
    provenance = {"repository": "Cbaird26/uv-reconstruction-frg", "commit": COMMIT,
                  "python": platform.python_version(), "numpy": np.__version__,
                  "primary_papers_consulted": [
                      {"url": "https://arxiv.org/pdf/hep-th/0606044", "title": "On fixed points of quantum gravity", "locations": "equations (4)-(6), (11)"},
                      {"url": "https://arxiv.org/pdf/0911.0386", "title": "Renormalization Group Flow in Scalar-Tensor Theories. I", "locations": "equations (1), (25), (26), Appendix A"},
                      {"url": "https://arxiv.org/pdf/1311.2898", "title": "Matter matters in asymptotically safe quantum gravity", "locations": "equations (21), (22), (32); source code remains pinned independently"}
                  ],
                  "new_files": [], "upstream_files": []}
    for item in fetched["files"]:
        path = UPSTREAM / item["path"]
        data = path.read_bytes()
        blob_sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        provenance["upstream_files"].append({**item, "sha256": hashlib.sha256(data).hexdigest(),
                                             "local_git_blob_sha": blob_sha,
                                             "matches_fetched_blob_sha": blob_sha == item["sha"]})
    for name in ("continue_uv.py", "scalar_polynomial_projection.py"):
        provenance["new_files"].append({"path": name, "sha256": hashlib.sha256((HERE / name).read_bytes()).hexdigest()})
    assert all(item["matches_fetched_blob_sha"] for item in provenance["upstream_files"]), "download normalization changed a source blob"
    write_json("provenance.json", provenance)
    print(json.dumps(native({"status": results["research_status"], "validation_checks": len(checks),
                             "spectrum_counts": summary["sign_counts_tolerance_1e-6"],
                             "mass_exponents": results["corrected_sector_labels"]["mass_squared_exponents"],
                             "xi_exponents": results["corrected_sector_labels"]["nonminimal_xi_exponents"],
                             "six_scalar_DEP_coordinates": benchmark6["coordinates"],
                             "common_flow_accepted": False}), indent=2))


if __name__ == "__main__":
    main()
