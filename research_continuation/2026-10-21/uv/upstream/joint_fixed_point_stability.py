"""Joint fixed point and stability spectrum of the derived 33 coordinates.

The joint fixed point of the currently derived flow is the DEP SM fixed
point with the matter sector at its Gaussian point:
  (lambdaN, gN) = (2 Lambda_tilde*, G_tilde*) = (-4.7975095, 1.7621271)
  all other 31 coordinates zero.
At this point every derived entry of `beta_partial` vanishes: gravity
exactly, matter entries exactly, the xi entries to ~1e-16, and the
dimension-six entries to the finite-difference noise floor (~1e-11).

The stability matrix is the numerical Jacobian of the derived 33
coordinates at the fixed point.  Two conventions are reported:

  - quantum-only: Jacobian of `partial_flow_41.beta_partial` restricted
    to the 33 derived coordinates (the mass-squared and dimension-six
    entries of that function are quantum trace contributions only);
  - quantum+canonical: the same, with the canonical terms
    (-2 m^2 for the mass-squared entries, +2 c for the dimension-six
    entries) added.  The DEP gravity block already contains its own
    canonical terms, so no canonical terms are added there, and all
    other matter couplings are dimensionless (canonical weight 0).

Critical exponents are theta = -eigenvalue (positive real part =
relevant), the convention stated in `DECLARED_TRUNCATION_V0_1.md`.

Quantum+canonical spectrum at the joint fixed point (33 entries):
  8 relevant:    +3.9609  (Lambda_tilde direction)
                 +2.8554  x3  (mH2, mPhi2, mE2: canonical 2 + quantum shift)
                 +2.0000  x3  (xiH, xiPhi, xiE: pure quantum, GMFP shift)
                 +1.6436  (G_tilde direction)
   12 marginal:   0.0000  x12 (g1, g2, g3, yt, yb, ytau, and the six
                  quartic entries: lambdaH, lambdaPhi, lambdaE, kappaHPhi,
                  kappaHE, kappaPhiE; all Gaussian in the one-loop matter
                  blocks at this point)
   13 irrelevant: -0.0756  x3  (Z_h, Z_phi, Z_E: beta_Z = -eta_s Z with
                  eta_s = -0.076, so theta = +eta_s)
                  -2.0000  x10 (the dimension-six entries: canonical,
                  quantum part vanishes at Gaussian matter)

The two gravity eigenvalues reproduce the DEP table-convention exponents
(3.961, 1.644) (improved=False, ghost factor 2*2^{[d/2]}).

Excluded from the spectrum: a_R2/a_C2 are NaN at the Gaussian point
(singular 1/(2 lambda) parametrization), and the derivative/portal
entries c_HBox, c_PhiBox, c_EBox, c_HF2, c_PhiF2, c_EF2 have no
projected flow (pending, recorded in DECLARED_TRUNCATION_V0_1.md).
"""
from __future__ import annotations

import numpy as np

from model import INDEX, NAMES
from partial_flow_41 import beta_partial
from canonical_scaling import CANONICAL
from gravity_matter_coupling import (fixed_point as dep_fixed_point,
                                     DEP_TABLE_GHOST_FACTOR, STANDARD_MODEL)

MISSING = ("a_R2", "a_C2", "c_HBox", "c_PhiBox", "c_EBox",
           "c_HF2", "c_PhiF2", "c_EF2")
DERIVED = tuple(name for name in NAMES if name not in MISSING)
DERIVED_INDICES = tuple(INDEX[name] for name in DERIVED)


def joint_fixed_point_couplings() -> list[float]:
    """The 41-vector of the joint fixed point of the derived flow."""
    lam_dep, g_dep = dep_fixed_point(improved=False,
                                     ghost_factor=DEP_TABLE_GHOST_FACTOR,
                                     seed=(-2.399, 1.762), **STANDARD_MODEL)
    point = [0.0] * 41
    point[INDEX["lambdaN"]] = 2.0 * lam_dep
    point[INDEX["gN"]] = g_dep
    return point


def full_flow(couplings, canonical: bool = False):
    """beta_partial, optionally with canonical terms for mass^2 and dim-6."""
    values = np.asarray(beta_partial(couplings), dtype=float)
    if canonical:
        for name in ("mH2", "mPhi2", "mE2"):
            values[INDEX[name]] += CANONICAL[INDEX[name]] * couplings[INDEX[name]]
        for name in NAMES:
            if name.startswith("c_"):
                values[INDEX[name]] += CANONICAL[INDEX[name]] * couplings[INDEX[name]]
    return values


def jacobian(flow, point: list[float], step: float = 1e-6) -> np.ndarray:
    """Central-difference Jacobian of `flow` at `point` (41 x 41)."""
    base = np.asarray(point, dtype=float)
    matrix = np.empty((41, 41))
    for column in range(41):
        delta = step * max(1.0, abs(base[column]))
        upper, lower = base.copy(), base.copy()
        upper[column] += delta
        lower[column] -= delta
        matrix[:, column] = (flow(upper) - flow(lower)) / (2.0 * delta)
    return matrix


def stability_spectrum(point=None, canonical: bool = True,
                       step: float = 1e-6) -> tuple[np.ndarray, np.ndarray]:
    """(thetas sorted by real part descending, derived 33x33 Jacobian)."""
    if point is None:
        point = joint_fixed_point_couplings()
    matrix = jacobian(lambda c: full_flow(c, canonical=canonical), point, step)
    block = matrix[np.ix_(DERIVED_INDICES, DERIVED_INDICES)]
    eigenvalues = -np.linalg.eigvals(block)
    order = np.argsort(eigenvalues.real)[::-1]
    return eigenvalues[order], block
