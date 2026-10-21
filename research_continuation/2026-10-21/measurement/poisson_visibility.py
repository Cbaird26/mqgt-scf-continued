"""Independent count-level diagnostic of the public sodium-cluster scans.

The independent-Poisson sinusoid is an explicitly tested working model, not
an asserted complete account of this apparatus. No new-field exclusion is
computed. Upstream experimental files remain unchanged.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import math
import os
import numpy as np
import pandas as pd
from scipy.special import xlogy
os.environ.setdefault("MPLCONFIGDIR", "/tmp/toe_continuation_mpl")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = HERE / "sources/pedalino_original/Na-Cluster-Interference/Na-Cluster/Data_April2025/22042025"
PERIOD_NM = 133.0


def half_deviance(y, mu):
    if np.any(mu <= 0):
        return math.inf
    return float(np.sum(mu - y + xlogy(y, y / mu)))


def diagnostic_extended_fit(xs_nm, counts, include_order_trend):
    """Check omitted second harmonic and a scan-order trend; no physics claim."""
    y = np.asarray(counts, float)
    angle = 2 * np.pi * np.asarray(xs_nm) / PERIOD_NM
    columns = [np.ones(len(y)), np.cos(angle), np.sin(angle), np.cos(2*angle), np.sin(2*angle)]
    if include_order_trend:
        columns.append(np.linspace(-1, 1, len(y)))
    design = y.mean() * np.column_stack(columns)
    theta = np.linalg.lstsq(design, y, rcond=None)[0]
    if np.any(design @ theta <= 0):
        theta = np.zeros(len(columns))
        theta[0] = 1
    converged = False
    for _ in range(100):
        mu = design @ theta
        grad = design.T @ (1-y/mu)
        hess = design.T @ ((y/mu**2)[:,None] * design)
        step = np.linalg.solve(hess, grad)
        decrement = float(grad @ step)
        if decrement < 1e-17:
            converged = True
            break
        fraction = 1.0
        old = half_deviance(y, mu)
        while fraction > 2**-35:
            proposal = theta - fraction*step
            val = half_deviance(y, design @ proposal)
            if val <= old - 1e-4*fraction*decrement + 1e-10:
                theta = proposal
                break
            fraction /= 2
        else:
            converged = decrement < 1e-10
            break
    if not converged:
        raise RuntimeError("Extended diagnostic did not converge")
    mu = design @ theta
    return {"deviance": 2*half_deviance(y,mu),
            "pearson": float(np.sum((y-mu)**2/mu)), "dof": len(y)-len(columns)}


def fit_scan(xs_nm, counts):
    y = np.asarray(counts, float)
    angle = 2 * np.pi * np.asarray(xs_nm) / PERIOD_NM
    x = np.column_stack([np.ones(len(y)), np.cos(angle), np.sin(angle)])
    scale = y.mean()
    design = scale * x
    theta_ls = np.linalg.lstsq(design, y, rcond=None)[0]
    theta = theta_ls.copy()
    if theta[0] <= np.linalg.norm(theta[1:]):
        theta = np.array([1.0, 0.0, 0.0])
    converged = False
    for iteration in range(100):
        mu = design @ theta
        grad = design.T @ (1 - y / mu)
        hess = design.T @ ((y / mu**2)[:, None] * design)
        step = np.linalg.solve(hess, grad)
        decrement = float(grad @ step)
        if decrement < 1e-17:
            converged = True
            break
        fraction = 1.0
        objective = half_deviance(y, mu)
        while fraction > 2**-35:
            candidate = theta - fraction * step
            if candidate[0] > np.linalg.norm(candidate[1:]) + 1e-10:
                val = half_deviance(y, design @ candidate)
                if val <= objective - 1e-4 * fraction * decrement + 1e-10:
                    theta = candidate
                    break
            fraction /= 2
        else:
            if decrement < 1e-10:
                converged = True
                break
            raise RuntimeError("Newton line search failed")
    if not converged:
        raise RuntimeError("Poisson count fit did not converge")
    mu = design @ theta
    fisher = design.T @ (design / mu[:, None])
    covariance = np.linalg.inv(fisher)
    radial = np.linalg.norm(theta[1:])
    visibility = radial / theta[0]
    dv = np.array([-radial / theta[0]**2,
                   theta[1] / (radial * theta[0]),
                   theta[2] / (radial * theta[0])])
    var_v = float(dv @ covariance @ dv)
    dof = len(y) - 3
    pearson = float(np.sum((y - mu)**2 / mu))
    residual = (y - mu) / np.sqrt(mu)
    lag1 = float(np.corrcoef(residual[:-1], residual[1:])[0, 1])
    return {
        "mean_counts": float(scale * theta[0]),
        "visibility_poisson": float(visibility),
        "visibility_fisher_se_conditional": math.sqrt(var_v),
        "phase_radians": float(np.arctan2(-theta[2], theta[1])),
        "visibility_ordinary_least_squares": float(np.linalg.norm(theta_ls[1:]) / theta_ls[0]),
        "deviance": 2 * half_deviance(y, mu),
        "pearson_chi_squared": pearson,
        "dof": dof,
        "pearson_dispersion": pearson / dof,
        "lag1_pearson_residual_correlation": lag1,
        "newton_iterations": iteration + 1,
        "newton_decrement": decrement,
    }, mu, theta, x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    table = pd.read_excel(DATA / "Powerscan_85kTh_22042025.xlsx")
    rows, fits, source_hashes = [], [], {}
    for _, source in table.iterrows():
        name = source["name"]
        path = DATA / "Interference Scans" / (name + "_s1.dat")
        raw = np.loadtxt(path, delimiter="\t")
        if len(raw) != int(source["# scan steps"]):
            raise ValueError("Metadata count differs from scan length")
        record, mu, theta, x = fit_scan(raw[:, 0], raw[:, 1])
        higher = diagnostic_extended_fit(raw[:,0], raw[:,1], False)
        higher_drift = diagnostic_extended_fit(raw[:,0], raw[:,1], True)
        for key, value in higher.items():
            record["second_harmonic_"+key] = value
        for key, value in higher_drift.items():
            record["second_harmonic_and_order_trend_"+key] = value
        record.update({"name": name, "bins": len(raw), "total_counts": int(raw[:, 1].sum()),
                       "G1_power_mW": float(source.iloc[5]),
                       "G2_power_mW": float(source.iloc[6]),
                       "G3_power_mW": float(source.iloc[7]),
                       "integration_time_seconds": float(source["integration time (s)"])})
        rows.append(record)
        fits.append((raw, mu, theta, x))
        source_hashes[str(path.relative_to(HERE))] = hashlib.sha256(path.read_bytes()).hexdigest()
    with (out / "scan_poisson_fits.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # Exact likelihood ridge: data determine A*exp(-chi), not A and chi separately.
    # Use the fitted per-scan amplitudes as effective contrasts. This proves the
    # invariance without substituting an uncalibrated quantum baseline curve.
    chi_values = np.linspace(0, 0.4, 21)
    ridge = []
    baseline_dev = sum(r["deviance"] for r in rows)
    biggest = max(r["visibility_poisson"] for r in rows)
    maximum_mean_change = 0.0
    for chi in chi_values:
        total_dev = 0.0
        for row, (raw, mu, theta, x) in zip(rows, fits):
            instrumental_contrast = row["visibility_poisson"] * math.exp(chi)
            effective_contrast = instrumental_contrast * math.exp(-chi)
            phase = row["phase_radians"]
            pred = row["mean_counts"] * (1 + effective_contrast *
                np.cos(2 * np.pi * raw[:, 0] / PERIOD_NM + phase))
            total_dev += 2 * half_deviance(raw[:, 1], pred)
            maximum_mean_change = max(maximum_mean_change, float(np.max(np.abs(pred - mu))))
        ridge.append({"chi": float(chi), "max_instrument_contrast": biggest * math.exp(chi),
                      "joint_deviance": total_dev, "delta_deviance": total_dev - baseline_dev})
    with (out / "attenuation_contrast_ridge.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ridge[0]))
        writer.writeheader()
        writer.writerows(ridge)

    pearson = sum(r["pearson_chi_squared"] for r in rows)
    dof = sum(r["dof"] for r in rows)
    max_v_difference = max(abs(r["visibility_poisson"]-r["visibility_ordinary_least_squares"]) for r in rows)
    variances = np.array([r["pearson_dispersion"] for r in rows])
    total_counts = sum(r["total_counts"] for r in rows)
    checks = {
        "95_scans_3895_bins": len(rows) == 95 and sum(r["bins"] for r in rows) == 3895,
        "all_optimized_means_positive": all(np.all(f[1] > 0) for f in fits),
        "all_contrasts_interior": all(0 < r["visibility_poisson"] < 1 for r in rows),
        "stationarity_newton_decrement": all(r["newton_decrement"] < 1e-10 for r in rows),
        "ridge_means_unchanged": maximum_mean_change < 1e-9,
        "ridge_instrument_contrast_below_one": max(x["max_instrument_contrast"] for x in ridge) < 1,
        "original_archive_md5": hashlib.md5((HERE / "sources/Na-Cluster-Interference.zip").read_bytes()).hexdigest() == "7917961b27676f4e9df3af6d3b01c374",
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    result = {
        "analysis": "Independent count-level sinusoidal Poisson diagnostic and structural attenuation-identifiability analysis",
        "dataset": "Pedalino et al., Na-Cluster-Interference, Zenodo 17502163, April 22 2025 scans",
        "dataset_url": "https://zenodo.org/records/17502163",
        "data_status": "Real public experimental counts; this reanalysis is not a new experiment",
        "statistical_model": "Independent Poisson counts with a separate offset, cosine coefficient and sine coefficient for every scan; fixed 133 nm period",
        "n_scans": len(rows), "n_bins": sum(r["bins"] for r in rows),
        "total_counts": total_counts, "total_residual_dof": dof,
        "joint_deviance": baseline_dev,
        "joint_pearson_dispersion": pearson / dof,
        "per_scan_dispersion_min_median_max": [float(variances.min()), float(np.median(variances)), float(variances.max())],
        "scans_with_dispersion_gt_2": int(np.sum(variances > 2)),
        "max_abs_poisson_minus_LS_visibility": max_v_difference,
        "median_abs_poisson_minus_LS_visibility": float(np.median([abs(r["visibility_poisson"] - r["visibility_ordinary_least_squares"]) for r in rows])),
        "fisher_errors_status": "Conditional independent-Poisson Fisher errors only; residual dispersion must be modeled before coverage or a physics exclusion is claimed",
        "extended_model_diagnostics": {
            "second_harmonic_joint_dispersion": sum(r["second_harmonic_pearson"] for r in rows) / sum(r["second_harmonic_dof"] for r in rows),
            "second_harmonic_and_order_trend_joint_dispersion": sum(r["second_harmonic_and_order_trend_pearson"] for r in rows) / sum(r["second_harmonic_and_order_trend_dof"] for r in rows),
            "second_harmonic_joint_deviance": sum(r["second_harmonic_deviance"] for r in rows),
            "second_harmonic_and_order_trend_joint_deviance": sum(r["second_harmonic_and_order_trend_deviance"] for r in rows),
            "interpretation": "An omitted harmonic or scan-order variation can contribute to residuals. These extensions diagnose model dependence, not a new noise mechanism; no multiple-testing discovery or calibrated exclusion is claimed."
        },
        "identifiability": {
            "equation": "V_observed(P)=A V_Q(P) exp(-chi) for power-independent chi",
            "invariance": "log A -> log A + delta; chi -> chi + delta",
            "jacobian": "dmu/d(log A) = - dmu/dchi; the two-column Fisher block is rank one where contrast is nonzero",
            "scope": "Exact only for multiplicative attenuation common to the scan variable; a distinguishable predicted shape with calibrated nuisance parameters can break it",
            "data_ridge_chi_range": [float(chi_values[0]), float(chi_values[-1])],
            "max_ridge_expected_count_difference": maximum_mean_change,
            "max_abs_ridge_delta_deviance": max(abs(r["delta_deviance"]) for r in ridge),
            "physical_bounds": "A<=1 can truncate a ridge if the baseline is known; it does not identify a unique attenuation or its mechanism",
            "new_field_constraint": None
        },
        "checks": {k: bool(v) for k,v in checks.items()},
        "source_file_sha256": source_hashes,
    }
    (out / "measurement_results.json").write_text(json.dumps(result, indent=2) + "\n")

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), layout="constrained")
    power = np.array([r["G2_power_mW"] for r in rows])
    vis = np.array([r["visibility_poisson"] for r in rows])
    axes[0].scatter(power, vis, s=15, c="#146b8c", alpha=.8)
    axes[0].set(xlabel="Second grating power (mW)", ylabel="Fitted first-harmonic visibility", title="Real public count data · 95 scans")
    axes[1].scatter(np.arange(1,len(rows)+1), variances, s=15, c="#a45a21")
    axes[1].axhline(1, color="black", lw=1, ls="--")
    axes[1].set(xlabel="Scan index", ylabel="Pearson statistic / residual df", title="Working-model residual check")
    axes[2].plot(chi_values, [r["max_instrument_contrast"] for r in ridge], color="#605099", lw=2)
    axes[2].set(xlabel="Proposed attenuation exponent chi", ylabel="Required instrumental contrast", title="Same predicted counts along ridge")
    axes[2].text(.04,.92, "A exp(-chi) is unchanged", transform=axes[2].transAxes, va="top", fontsize=9)
    fig.savefig(out / "measurement_diagnostics.png", dpi=180)
    plt.close(fig)
    print(json.dumps({k:v for k,v in result.items() if k != "source_file_sha256"}, indent=2))


if __name__ == "__main__":
    main()
