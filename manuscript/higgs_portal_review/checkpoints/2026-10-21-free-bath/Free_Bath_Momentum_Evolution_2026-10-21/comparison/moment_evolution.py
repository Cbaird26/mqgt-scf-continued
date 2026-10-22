"""Fixed-bath scalar evolution in the inherited polynomial trial spaces.

Compare normalized population and total-energy autocorrelations at tau=H*t.
These are trial-space predictions, not expanding-universe trajectories.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import cholesky, null_space, solve_triangular

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / "baseline"
sys.path.insert(0, str(BASELINE))
from nested_free_bath import MASS, hubble, metric_data


def evolve(T, D, G, initial, times):
    L = cholesky(G, lower=True)
    A = solve_triangular(L, D, lower=True)
    A = solve_triangular(L, A.T, lower=True).T
    number = np.zeros(len(initial))
    number[:2] = 1.
    Q = null_space((L.T @ number)[None, :])
    B = Q.T @ ((A + A.T) / (2 * hubble(T))) @ Q
    eigenvalues, eigenvectors = np.linalg.eigh(B)
    a0 = eigenvectors.T @ Q.T @ L.T @ initial
    weights = a0 * a0
    initial_norm2 = float(weights.sum())
    assert np.max(np.abs(number @ G @ initial)) < 1e-12
    assert eigenvalues.min() > 0
    correlation = np.exp(-np.outer(times, eigenvalues)) @ weights / initial_norm2
    norm_ratio = np.sqrt(np.exp(-2 * np.outer(times, eigenvalues)) @ weights / initial_norm2)
    return dict(eigenvalues_over_H=eigenvalues.tolist(),
                spectral_weights_normalized=(weights / initial_norm2).tolist(),
                initial_norm_squared=initial_norm2,
                autocorrelation=correlation.tolist(), L2_norm_ratio=norm_ratio.tolist())


def run():
    data = json.loads((BASELINE / "results_q80.json").read_text())
    T = data["T_GeV"]
    D = np.array(data["leptons_plus_free_quarks"]["gram_scalar_per_N_GeV"])
    G, _, _ = metric_data(T)
    species_fraction = np.diag(G)[:2]
    total_number = np.array([1., 1., 0., 0., 0., 0.])
    energy_over_T = np.array([MASS[0] / T, MASS[1] / T, 1., 1., 0., 0.])
    mean_energy_over_T = float(total_number @ G @ energy_over_T)
    population = np.array([-species_fraction[1], species_fraction[0], 0., 0., 0., 0.])
    energy = energy_over_T - mean_energy_over_T * total_number
    times = np.unique(np.r_[np.linspace(0, 5, 101), [0., .25, .5, 1., 2., 5.]])
    cases = {}
    for name, initial in [("population", population), ("energy", energy)]:
        cases[name] = {}
        for dimension, label in [(4, "original_scalar"), (6, "enlarged_scalar")]:
            cases[name][label] = evolve(T, D[:dimension, :dimension],
                                       G[:dimension, :dimension], initial[:dimension], times)
    count_rate = float(data["leptons_plus_free_quarks"]["counts_over_H"])
    cases["population"]["count_only"] = dict(
        eigenvalues_over_H=[count_rate],
        autocorrelation=np.exp(-count_rate * times).tolist(),
        L2_norm_ratio=np.exp(-count_rate * times).tolist())
    return dict(T_GeV=T, times_Ht=times.tolist(), species_fractions=species_fraction.tolist(),
                equilibrium_mean_energy_GeV=mean_energy_over_T * T,
                initial_conditions={
                    "population": "h_P(i,E)=1_(i=2)-r2",
                    "energy": "h_E(i,E)=(E-<E>_pi)/T",
                    "distribution": "f=f_eq*(1+epsilon*h), epsilon=0.05",
                },
                cases=cases,
                fixed_temperature=True, cosmological_redshift_included=False,
                number_changing_channels_included=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "moment_evolution.json")
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    for t in [0., .25, .5, 1., 2., 5.]:
        index = result["times_Ht"].index(t)
        print(t, {case: {method: values["autocorrelation"][index]
                        for method, values in methods.items()}
                  for case, methods in result["cases"].items()})
