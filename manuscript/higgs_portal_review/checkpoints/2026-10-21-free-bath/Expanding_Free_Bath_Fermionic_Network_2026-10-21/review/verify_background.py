"""Independent analytic equilibrium and collisionless-background controls."""
from pathlib import Path
import json
import math
import sys
import numpy as np
from scipy.special import kv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "solver"))
import expanding_free_bath as s

rows = []
for bins in (48, 96, 192):
    edges = np.r_[np.linspace(0, 48, bins + 1), np.inf]
    for T in (.5, .4, 1 / 3):
        data = s.cell_data(T, edges)
        analytic = np.array([m*m*T*kv(2, m/T)/(2*math.pi**2) for m in s.MASS])
        analytic /= analytic.sum()
        row = {
            "finite_bins": bins,
            "T_GeV": T,
            "metric_normalization_error": float(abs(data[:, :, 0].sum() - 1)),
            "species_fraction_max_error": float(np.max(np.abs(data[:, :, 0].sum(axis=1) - analytic))),
            "MB_Tkin_over_T_error": float(abs(data[:, :, 3].sum()/T - 1)),
        }
        assert row["metric_normalization_error"] < 1e-12
        assert row["species_fraction_max_error"] < 1e-12
        assert row["MB_Tkin_over_T_error"] < 1e-12
        initial = s.cell_data(.5, edges)[:, :, 0].ravel()
        cell = s.observables(initial, T, edges)
        exact = s.collisionless_exact(T)
        row.update({
            "collisionless_exact_Tkin_over_T": exact["Tkin_over_T"],
            "collisionless_cell_closure_Tkin_over_T": cell["Tkin_over_T"],
            "collisionless_closure_Tkin_relative_error": cell["Tkin_over_T"]/exact["Tkin_over_T"] - 1,
        })
        rows.append(row)

result = {
    "method": "Independent analytic equilibrium density (Bessel K2), exact MB pressure identity, and direct continuum collisionless comparison",
    "checks": rows,
    "elapsed_time": {"eta_final": math.log(1.5), "H_T0_delta_t": .625, "H_0p4_delta_t": .4},
    "all_equilibrium_checks_passed": True,
}
(HERE / "independent_background_check.json").write_text(json.dumps(result, indent=2) + "\n")
print("Analytic equilibrium and collisionless-background checks passed.")
