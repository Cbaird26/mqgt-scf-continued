"""Summarize the three temperatures and validate their inherited subspaces."""
from pathlib import Path
import json
import numpy as np
from nested_free_bath import metric_data

HERE = Path(__file__).resolve().parent
baseline = json.loads((HERE.parent / "baseline_six_moment.json").read_text())
rows = []
for name in ["results_Tthird_q48.json", "results_q80.json", "results_Thalf_q48.json"]:
    result = json.loads((HERE / name).read_text())
    T = result["T_GeV"]
    old = next(row for row in baseline["rows"] if row["T_GeV"] == T)
    new = result["leptons_plus_free_quarks"]
    GS, GV, _ = metric_data(T)
    S = np.array(new["gram_scalar_per_N_GeV"])
    V = np.array(new["gram_drift_per_N_GeV"])
    transform = np.eye(4)
    transform[0, 2] = -GS[0, 2] / GS[0, 0]
    transform[1, 3] = -GS[1, 3] / GS[1, 1]
    D = np.zeros((6, 6))
    D[:4, :4] = transform.T @ S[:4, :4] @ transform
    D[4:, 4:] = V[:2, :2]
    oldD = np.array(old["D_per_N_GeV"])
    relative_error = np.linalg.norm(D - oldD) / np.linalg.norm(oldD)
    assert relative_error < 1e-8
    for oldkey, newkey in [
        ("scalar_degree1_over_H", "scalar_degree2_over_H"),
        ("drift_degree0_over_H", "drift_degree1_over_H"),
    ]:
        a, b = np.array(new[oldkey]), np.array(new[newkey])
        assert np.all(b > 0)
        assert np.all(b[:len(a)] <= a + 1e-12)
        assert np.all(a <= b[len(b)-len(a):] + 1e-12)
    rows.append(dict(
        T_GeV=T, resolution=result["resolution"],
        full_baseline_matrix_relative_Frobenius_error=float(relative_error),
        counts_over_H=new["counts_over_H"],
        old_scalar_over_H=new["scalar_degree1_over_H"][0],
        new_scalar_over_H=new["scalar_degree2_over_H"][0],
        old_drift_over_H=new["drift_degree0_over_H"][0],
        new_drift_over_H=new["drift_degree1_over_H"][0],
        new_quadrupole_over_H=new["quadrupole_degree0_over_H"][0],
    ))
summary = dict(
    model="ideal MB leptons plus five free Dirac-quark species; tree Higgs exchange; gstar60",
    baseline_commit="994e51cb28b51ade500bb0e1902f3b082ef8e594",
    basis="12 symmetry-reduced representatives: scalar6, vector4, tensor2 (full angular degeneracies not counted)",
    rows=rows, full_spectral_gap_lower_bound=None, QCD_medium_calculated=False,
    all_baseline_and_interlacing_checks_passed=True,
)
(HERE / "three_temperature_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
