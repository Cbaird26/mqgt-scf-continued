"""Canonical contributions to beta functions of the declared dimensionless basis."""
from __future__ import annotations
import numpy as np
from model import INDEX, NAMES

CANONICAL = np.zeros(41)
CANONICAL[INDEX["gN"]] = 2.0
CANONICAL[INDEX["lambdaN"]] = -2.0
for name in ("mH2", "mPhi2", "mE2"):
    CANONICAL[INDEX[name]] = -2.0
for name in ("c_H6", "c_Phi6", "c_E6", "c_H4Phi2", "c_H4E2", "c_H2Phi4", "c_H2E4", "c_Phi4E2", "c_Phi2E4", "c_H2Phi2E2", "c_HBox", "c_PhiBox", "c_EBox", "c_HF2", "c_PhiF2", "c_EF2"):
    CANONICAL[INDEX[name]] = 2.0

def beta_canonical(couplings):
    values = np.asarray(couplings, dtype=float)
    if values.shape != (41,):
        raise ValueError("expected 41 couplings")
    return tuple(CANONICAL * values)

def dimensions_report():
    return {NAMES[i]: float(CANONICAL[i]) for i in range(41) if CANONICAL[i] != 0.0}
