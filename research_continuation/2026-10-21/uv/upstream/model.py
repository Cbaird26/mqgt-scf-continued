"""Declared 41-coordinate FRG reconstruction interface.

No unknown loop coefficient is silently guessed in this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

NAMES = (
    "gN", "lambdaN", "a_R2", "a_C2", "g1", "g2", "g3", "yt", "yb", "ytau",
    "lambdaH", "mH2", "lambdaPhi", "mPhi2", "lambdaE", "mE2", "kappaPhiE",
    "kappaHPhi", "kappaHE", "xiH", "xiPhi", "xiE", "Z_h", "Z_phi", "Z_E",
    "c_H6", "c_Phi6", "c_E6", "c_H4Phi2", "c_H4E2", "c_H2Phi4", "c_H2E4",
    "c_Phi4E2", "c_Phi2E4", "c_H2Phi2E2", "c_HBox", "c_PhiBox", "c_EBox",
    "c_HF2", "c_PhiF2", "c_EF2",
)

assert len(NAMES) == 41
INDEX = {name: i for i, name in enumerate(NAMES)}


class IncompleteFlowError(RuntimeError):
    """Raised when a claimed full calculation lacks its projected quantum flow."""


def required_eta_n(g_n: float) -> float | None:
    """Return eta_N forced by beta_gN=0, or None at the Gaussian point."""
    return -2.0 if g_n != 0.0 else None


def gravity_beta(g_n: float, eta_n: float) -> float:
    return (2.0 + eta_n) * g_n


@dataclass(frozen=True)
class FlowSpecification:
    """A complete flow needs all 41 projected quantum beta contributions."""

    eta_n: Callable[[Sequence[float]], float] | None = None
    quantum_beta: Callable[[Sequence[float]], Sequence[float]] | None = None

    def beta(self, couplings: Sequence[float]) -> tuple[float, ...]:
        if len(couplings) != len(NAMES):
            raise ValueError(f"Expected {len(NAMES)} couplings, got {len(couplings)}")
        if self.eta_n is None or self.quantum_beta is None:
            raise IncompleteFlowError(
                "Full 41-coupling flow unavailable: supply eta_N and all projected quantum terms."
            )
        quantum = tuple(self.quantum_beta(couplings))
        if len(quantum) != len(NAMES):
            raise ValueError("quantum_beta must return 41 entries")
        result = list(quantum)
        result[INDEX["gN"]] = gravity_beta(couplings[INDEX["gN"]], self.eta_n(couplings))
        return tuple(result)
