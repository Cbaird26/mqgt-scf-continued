"""Tree-level portal interface with explicit basis and normalization conventions.

This is a calculation contract for a restricted effective theory, not a UV
completion. Units are GeV with hbar=c=1. The simultaneous Z2 is exact, the
singlet vacuum is zero, and the physical Higgs is unmixed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import math
import numpy as np


def symmetric_matrix(value, name):
    a = np.asarray(value, dtype=float)
    if a.shape != (2, 2) or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be a finite 2x2 matrix")
    if not np.allclose(a, a.T, rtol=0, atol=1e-13):
        raise ValueError(f"{name} must be symmetric")
    return (a + a.T) / 2


def mass_basis(physical_mass_squared, portal_matrix):
    """Return positive masses, portal in their basis, and phi=R*s rotation."""
    m2 = symmetric_matrix(physical_mass_squared, "physical_mass_squared")
    k = symmetric_matrix(portal_matrix, "portal_matrix")
    eigenvalues, r = np.linalg.eigh(m2)
    if np.any(eigenvalues <= 0):
        raise ValueError("Massive symmetric branch requires positive physical masses")
    return np.sqrt(eigenvalues), r.T @ k @ r, r


def pair_widths(masses, k_mass, higgs_mass=125.0, vev=246.0):
    """Widths in GeV for V_portal = phi^T K phi H^dagger H / 2.

    Identical channels carry 1/(32*pi*m_h); the distinct 12 channel has
    1/(16*pi*m_h). Return production widths, with no invisibility assumption.
    """
    masses = np.asarray(masses, dtype=float)
    k = symmetric_matrix(k_mass, "k_mass")
    if (masses.shape != (2,) or not np.all(np.isfinite(masses)) or
            np.any(masses < 0) or not math.isfinite(higgs_mass) or
            not math.isfinite(vev) or higgs_mass <= 0 or vev <= 0):
        raise ValueError("Invalid masses or electroweak inputs")
    out = {}
    for i, j, label in ((0, 0, "11"), (0, 1, "12"), (1, 1, "22")):
        if masses[i] + masses[j] >= higgs_mass:
            out[label] = 0.0
            continue
        phase = math.sqrt(
            (1 - ((masses[i] + masses[j]) / higgs_mass) ** 2)
            * (1 - ((masses[i] - masses[j]) / higgs_mass) ** 2)
        )
        divisor = 32 if i == j else 16
        out[label] = vev**2 * k[i, j]**2 * phase / (divisor * math.pi * higgs_mass)
    out["total_production"] = sum(out.values())
    return out


def matter_coefficient(k_mass, probe_mass, scalar_form_factor=1.0, higgs_mass=125.0):
    """C [GeV^-1] in L_eff = (s^T C s) fbar f; a point fermion/nucleon only.

    A composite apparatus requires its own spatial response and matching.
    """
    if (not all(math.isfinite(v) for v in (probe_mass, higgs_mass, scalar_form_factor))
            or probe_mass <= 0 or higgs_mass <= 0 or scalar_form_factor < 0):
        raise ValueError("Invalid probe or matching inputs")
    return symmetric_matrix(k_mass, "k_mass") * (
        scalar_form_factor * probe_mass / (2 * higgs_mass**2)
    )


def run_checks():
    physical = np.diag([10.0**2, 11.5**2])
    k = np.array([[0.001, -0.001], [-0.001, 0.001]])
    masses, km, _ = mass_basis(physical, k)
    widths = pair_widths(masses, km)
    rotation_errors = []
    matching_errors = []
    # These are basis changes of the SAME physical point, not new mixings.
    for angle in np.linspace(0, 2 * np.pi, 65):
        q = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        mr, kr, r = mass_basis(q.T @ physical @ q, q.T @ k @ q)
        wr = pair_widths(mr, kr)
        rotation_errors.append(abs(wr["total_production"] / widths["total_production"] - 1))
        # Eigenvector sign ambiguities disappear after matching back to the original basis.
        cr = matter_coefficient(kr, 0.939, 0.3)
        restored = q @ r @ cr @ r.T @ q.T
        expected = matter_coefficient(k, 0.939, 0.3)
        matching_errors.append(float(np.max(np.abs(restored - expected))))
    degenerate = pair_widths([10, 10], k)["total_production"]
    beta = math.sqrt(1 - 4 * 10**2 / 125**2)
    trace_identity = 246**2 * beta * np.trace(k @ k) / (32 * np.pi * 125)
    closed = pair_widths([70, 80], k)
    threshold = pair_widths([62.5, 62.5], k)
    # Off-diagonal identical-particle factor at equal masses and equal entries.
    equal_entries = pair_widths([10, 10], np.ones((2, 2)) * 0.001)
    checks = {
        "production_basis_invariance": max(rotation_errors) < 1e-12,
        "matching_basis_covariance": max(matching_errors) < 1e-20,
        "degenerate_trace_identity": abs(degenerate / trace_identity - 1) < 1e-14,
        "closed_channels_zero": all(x == 0 for x in closed.values()),
        "exact_threshold_zero": all(x == 0 for x in threshold.values()),
        "distinct_channel_factor_two": abs(equal_entries["12"] / equal_entries["11"] - 2) < 1e-14,
    }
    # A cross-route identity, algebraic and independent of an assumed bath population.
    kap, probe_mass, form = 0.001, 0.939, 0.3
    gamma_h = 246**2 * kap**2 * beta / (32 * np.pi * 125)
    c2 = (kap * form * probe_mass / (2 * 125**2))**2
    reconstructed_c2 = 8 * np.pi * form**2 * probe_mass**2 / (246**2 * 125**3 * beta) * gamma_h
    checks["collider_to_noise_coefficient_identity"] = abs(c2 / reconstructed_c2 - 1) < 1e-14
    checks = {name: bool(value) for name, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    bare = physical - 246**2 * k / 2
    return {
        "scope": "Tree-level algebra and basis consistency; no vacuum, relic, detector, or UV certification",
        "units": "GeV, hbar=c=1",
        "benchmark_mass_GeV": masses.tolist(),
        "benchmark_portal_matrix_mass_basis": k.tolist(),
        "tree_widths_GeV": widths,
        "total_production_width_keV": widths["total_production"] * 1e6,
        "hypothetical_fraction_if_every_daughter_invisible_and_SM_width_4p1_MeV":
            widths["total_production"] / (0.0041 + widths["total_production"]),
        "bare_mass_squared_matrix_GeV2": bare.tolist(),
        "bare_mass_squared_eigenvalues_GeV2": np.linalg.eigvalsh(bare).tolist(),
        "bare_eigenvalue_caveat": "A positive quadratic Hessian does not establish global stability; quartics are unspecified.",
        "trace_K_squared": float(np.trace(k @ k)),
        "max_relative_total_width_basis_error": max(rotation_errors),
        "max_absolute_matching_covariance_error_GeV_inverse": max(matching_errors),
        "checks": checks,
        "check_count": len(checks),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(Path(__file__).with_name("common_results.json")))
    args = parser.parse_args()
    result = run_checks()
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
