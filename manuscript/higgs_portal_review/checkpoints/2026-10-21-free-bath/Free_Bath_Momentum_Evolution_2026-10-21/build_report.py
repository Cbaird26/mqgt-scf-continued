"""Build the compact numerical summary and publication-style comparison figure.

This reads completed calculations. It does not rerun collision integrals.
All paths are relative to this file, so the extracted package is portable.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "free_bath_momentum_mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

ROOT = Path(__file__).resolve().parent


def read_json(relative):
    return json.loads((ROOT / relative).read_text())


def main(output_dir):
    final = read_json("solver/final_evolution.json")
    conv = read_json("solver/convergence_summary.json")
    moment = read_json("comparison/moment_evolution.json")
    tail = read_json("tail/tail_bound_constants.json")
    checks = read_json("review/independent_exponential_check.json")
    ev = final["evolution"]
    initial = ev["initial_conditions"]
    names = {"population": "population", "energy": "temperature"}
    chosen_times = [0.0, 0.25, 0.5, 1.0, 2.0, 5.0]
    curves = {}
    rows = []
    for name, raw_name in names.items():
        raw = initial[raw_name]["rows"]
        times = np.array([r["tau_Ht"] for r in raw])
        values = np.array([r["autocorrelation_relative_to_initial"] for r in raw])
        assert np.allclose(times, moment["times_Ht"], rtol=0, atol=1e-14)
        curves[name] = {"times": times, "grid": values}
        for method, results in moment["cases"][name].items():
            curves[name][method] = np.array(results["autocorrelation"])
    for t in chosen_times:
        k = int(np.flatnonzero(np.isclose(curves["energy"]["times"], t, atol=1e-14, rtol=0))[0])
        record = {"tau_Href_t": t}
        for name, raw_name in names.items():
            raw = initial[raw_name]["rows"][k]
            values = curves[name]
            entry = {
                "radial_grid_own_initial_normalization": float(values["grid"][k]),
                "radial_grid_continuum_initial_normalization": raw["autocorrelation_divided_by_continuum_variance"],
                "radial_grid_L2_norm_ratio": float(np.sqrt(raw["chi2_relative_to_initial"])),
                "original_scalar_moment": float(values["original_scalar"][k]),
                "enlarged_scalar_moment": float(values["enlarged_scalar"][k]),
                "original_minus_grid_relative_percent": float(100 * (values["original_scalar"][k] / values["grid"][k] - 1)),
                "enlarged_minus_grid_relative_percent": float(100 * (values["enlarged_scalar"][k] / values["grid"][k] - 1)),
            }
            if name == "population":
                entry["count_only_exponential"] = float(values["count_only"][k])
            record[name] = entry
        rows.append(record)

    refinements = {}
    for label, data in conv["refinement_changes"].items():
        refinements[label] = {}
        for name, raw_name in names.items():
            v = data[raw_name]
            refinements[label][name] = {
                "tau_Href_t": v["tau_Ht"],
                "finer_minus_coarser_relative_percent": [100 * x for x in v["relative_change"]],
                "absolute_change": v["absolute_change"],
            }
    summary = {
        "title": "Fixed-temperature momentum-resolved free-bath evolution",
        "date": "2026-10-21",
        "T_GeV": final["T_GeV"],
        "H_reference_GeV": tail["H_GeV"],
        "time_coordinate": "tau = H_reference * t; T and H_reference held fixed",
        "equilibrium_species_fractions": ev["equilibrium_species_fractions"],
        "equilibrium_mean_energy_GeV": moment["equilibrium_mean_energy_GeV"],
        "initial_conditions": {
            "population": "h_P(i,E) = 1_(i=2) - r2",
            "energy": "h_E(i,E) = (E - equilibrium_mean_energy)/T",
            "distribution": "f(0) = f_eq * (1 + 0.05*h); two separate initial-value problems",
            "energy_projection_retains_continuum_variance_fraction": initial["temperature"]["initial_variance_retained_fraction"],
        },
        "observable_definition": "C_h(tau) = <h, exp(-L*tau/H_reference) h>_pi / <h,h>_pi",
        "normalization_caveat": "Radial-grid headline curves use each represented initial excess. Polynomial energy profiles retain the exact continuum variance; the grid retains 99.935897%. Both radial normalizations are provided.",
        "numerical_discretization": {
            "finite_energy_cells_per_species": final["finite_bins_per_species"],
            "cell_coordinate": "x_i=(E_i-m_i)/T",
            "cell_width": 0.125,
            "last_cell": "[16,infinity) for each species; tail mass and event weights retained",
            "quadrature": final["resolution"],
            "raw_source_graph": final["source_graph"],
        },
        "selected_times": rows,
        "refinement_sensitivity": refinements,
        "refinement_changes_are_certified_error_bounds": False,
        "structural_checks": {
            "all_invariants_passed": conv["all_invariants_passed"],
            "number_null_relative_residual": ev["number_null_relative_residual"],
            "max_absolute_number_error": max(abs(r["total_number_relative_error"]) for item in initial.values() for r in item["rows"]),
            "minimum_relative_occupation_by_initial_condition": {
                name: min(r["minimum_relative_occupation"] for r in initial[raw_name]["rows"])
                for name, raw_name in names.items()
            },
            "independent_forward_matrix_exponential": checks,
        },
        "finite_graph_lowest_positive_rate_over_H": min(ev["positive_eigenvalues_over_H"]),
        "numerical_calculation_certifies_continuum_gap": False,
        "separate_conditional_analytic_theorem": {
            "uniform_L2_variational_gap": 0.0,
            "scope": tail["theorem_scope"] + "; unbounded momentum domain and retained massive propagator",
            "proof_file": "tail/CONDITIONAL_ZERO_GAP_THEOREM.txt",
            "frequency_upper_bound": tail["bound"],
            "B_by_initial_species_GeV2": tail["B_by_initial_species_GeV2"],
            "is_claim_about_physical_UV_completion": False,
            "does_not_imply_absence_of_bulk_relaxation": True,
        },
        "expanding_cosmological_history_computed": False,
        "interacting_QCD_response_computed": False,
        "apparatus_response_computed": False,
        "result_scope": "isotropic, fixed ideal Maxwell-Boltzmann lepton plus free-quark bath, dilute scalar scattering-only benchmark",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "comparison_summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11.5,
        "axes.titlesize": 13.5, "axes.labelsize": 12,
        "axes.spines.top": False, "axes.spines.right": False,
        "savefig.facecolor": "white", "figure.facecolor": "white",
    })
    fig, (left, right) = plt.subplots(1, 2, figsize=(13.6, 6.6))
    fig.subplots_adjust(left=.075, right=.975, bottom=.23, top=.78, wspace=.27)
    fig.text(.075, .94, "Momentum-resolved free-bath relaxation", fontsize=22, weight="bold", color="#14243b")
    fig.text(.075, .885, r"Fixed $T=0.4$ GeV  |  Separate isotropic initial perturbations  |  $\tau=H_{\rm ref}t$", fontsize=13, color="#4c5e72")
    fig.text(.075, .845, "The bath is held fixed; these curves do not include cosmological expansion.", fontsize=11, color="#4c5e72")

    times = curves["energy"]["times"]
    left.plot(times, 100 * curves["energy"]["grid"], color="#c55c16", lw=2.6, label="Mean-energy excess: resolved")
    left.plot(times, 100 * curves["population"]["grid"], color="#1764a3", lw=2.6, label="Species-population excess: resolved")
    left.plot(times, 100 * curves["population"]["count_only"], color="#75818c", lw=1.9, ls="--", label="Count-only population prediction")
    left.set_yscale("log")
    left.set_ylim(1e-5, 150)
    left.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100])
    left.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}"))
    left.set_ylabel("Initial excess remaining (%)")
    left.set_title("A  Bulk observables relax at different rates", loc="left", pad=12)
    left.legend(loc="lower left", fontsize=9.5, frameon=False)

    grid = curves["energy"]["grid"]
    right.axhline(0, color="#aab3bd", lw=1)
    right.plot(times, 100 * (curves["energy"]["original_scalar"] / grid - 1), color="#75818c", lw=2.3, label="Original scalar moments")
    right.plot(times, 100 * (curves["energy"]["enlarged_scalar"] / grid - 1), color="#138576", lw=2.6, label="Enlarged scalar moments")
    coarse = conv["quadrature_and_grid"]["80"]["64"]["initial_conditions"]["temperature"]
    ct = np.array(coarse["tau_Ht"])
    fine_selected = np.interp(ct, times, grid)
    coarse_diff = 100 * (np.array(coarse["correlation"]) / fine_selected - 1)
    right.plot(ct, coarse_diff, color="#7964ad", lw=1.6, ls=":", marker="o", ms=5,
               label="64-cell grid (resolution comparison)")
    right.set_ylim(-14, 1.5)
    right.set_ylabel("Difference from 128-cell energy curve (%)")
    right.set_title("B  Energy evolution: moment comparison", loc="left", pad=12)
    right.legend(loc="lower left", fontsize=9.5, frameon=False)
    for ax in (left, right):
        ax.set_xlim(0, 5)
        ax.set_xlabel(r"Elapsed time $\tau=H_{\rm ref}t$")
        ax.grid(axis="y", which="major", color="#dfe4ea", linewidth=.75)
        ax.set_axisbelow(True)

    fig.text(.075, .13, r"Initial shapes: $h_P=\mathbf{1}_{i=2}-r_2$,  $h_E=(E-\langle E\rangle_\pi)/T$;  $f(0)=f_{\rm eq}(1+0.05h)$.", fontsize=11, color="#24394f")
    fig.text(.075, .087, "Each curve is normalized to its represented initial excess. The energy grid retains 99.9359% of the continuum initial variance.", fontsize=10.5, color="#4c5e72")
    fig.text(.075, .049, "128 finite cells plus one semi-infinite tail cell per species. Refinement differences measure sensitivity; they are not certified error bounds.", fontsize=10.2, color="#4c5e72")
    png = output_dir / "Free_Bath_Momentum_Evolution_T0p4_GeV.png"
    fig.savefig(png, dpi=190)
    plt.close(fig)
    print(f"Wrote {png.name} and comparison_summary.json")
    for row in rows:
        if row["tau_Href_t"] in (1.0, 2.0, 5.0):
            print(json.dumps(row))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "report")
    main(parser.parse_args().output_dir)
