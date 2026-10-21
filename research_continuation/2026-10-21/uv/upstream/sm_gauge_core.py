"""One-loop Standard Model gauge core with two gauge-singlet real scalars.

Convention uses the ordinary hypercharge coupling gY, not GUT-normalized g1:
  d gY/d ln(mu) = (41/6) gY^3/(16 pi^2)
  d g2/d ln(mu) = (-19/6) g2^3/(16 pi^2)
  d g3/d ln(mu) = -7 g3^3/(16 pi^2)

Phi_c and E are treated as SM gauge singlets, as stated in the supplied action.
"""
from __future__ import annotations

from math import pi
from typing import Sequence

LOOP = 16.0 * pi**2
COEFFICIENTS = (41.0 / 6.0, -19.0 / 6.0, -7.0)
NAMES = ("gY", "g2", "g3")


def beta_gauge(couplings: Sequence[float]) -> tuple[float, float, float]:
    return tuple(b * float(g) ** 3 / LOOP for g, b in zip(couplings, COEFFICIENTS))


def one_loop_fixed_point(couplings: Sequence[float], tolerance: float = 1e-12) -> bool:
    """All nonzero one-loop gauge beta functions have fixed sign; only g=0 is a root."""
    return all(abs(float(g)) <= tolerance for g in couplings)


def inverse_squared_at_scale(g0: float, coefficient: float, log_mu_ratio: float) -> float:
    """One-loop analytic flow: 1/g^2(mu)=1/g0^2-b ln(mu/mu0)/(8 pi^2)."""
    return 1.0 / g0**2 - coefficient * log_mu_ratio / (8.0 * pi**2)


def landau_log_scale(g0: float, coefficient: float) -> float | None:
    """Return ln(mu_pole/mu0) for b>0, otherwise None."""
    return 8.0 * pi**2 / (coefficient * g0**2) if coefficient > 0.0 else None
