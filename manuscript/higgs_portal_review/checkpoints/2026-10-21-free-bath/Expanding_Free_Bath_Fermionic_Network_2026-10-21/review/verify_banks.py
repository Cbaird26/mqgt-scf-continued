"""Check the fixed-temperature count contrast after rebinning into y cells."""
import json
import math
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
SOLVER = HERE.parent / "solver"
sys.path.insert(0, str(SOLVER))
from expanding_free_bath import ScatteringBank, cell_data

reference = 2.97474576498998
rows = []
for path in sorted(SOLVER.glob("bank_*.npz")):
    bank = ScatteringBank(path)
    eta = math.log(.5/.4)
    W = bank.conductance(eta)
    pi = cell_data(.4, bank.edges)[:, :, 0].ravel()
    n = len(pi)//2
    r2 = pi[n:].sum()
    h = np.r_[np.full(n, -r2), np.full(n, 1-r2)]
    D = np.diag(W.sum(axis=1))-W
    Q = -D/pi[None, :]
    value = h@D@h / np.dot(pi, h*h)
    row = {
        "bank": path.name,
        "count_contrast_over_H": float(value),
        "reference": reference,
        "relative_difference": float(value/reference-1),
        "relative_number_null_residual": float(np.linalg.norm(D@np.ones(len(pi)))/np.linalg.norm(D)),
        "stationarity_absolute_max": float(np.max(np.abs(Q@pi))),
    }
    assert abs(row["relative_difference"]) < 1e-8
    assert row["relative_number_null_residual"] < 1e-12
    assert row["stationarity_absolute_max"] < 1e-12
    rows.append(row)

assert rows, "No scattering bank supplied"
(HERE / "bank_normalization_check.json").write_text(json.dumps({
    "T_GeV": .4, "checks": rows, "all_checks_passed": True,
}, indent=2) + "\n")
print(f"Count-contrast, conservation, and stationary-metric checks passed for {len(rows)} banks.")
