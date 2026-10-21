"""Coupled one-loop SM(top) + Higgs + two-real-singlet baseline.

Deliberate scope: MS-bar, ordinary gY normalization, dominant top Yukawa,
gauge-singlet Phi_c/E, massless quartics. Gravity and higher-dimension FRG
operators are not represented here.
"""
from __future__ import annotations

from typing import Sequence

from higgs_two_singlet_core import beta_scalar_quartics
from sm_gauge_core import beta_gauge, LOOP

NAMES = ("gY", "g2", "g3", "yt", "yb", "ytau", "lambdaH", "lambdaPhi", "lambdaE", "pHPhi", "pHE", "pPhiE")


def beta(c: Sequence[float]) -> tuple[float, ...]:
    g_y, g2, g3, y_t, y_b, y_tau, lh, lp, le, p_hp, p_he, p_pe = map(float, c)
    bg = beta_gauge((g_y, g2, g3))
    by = y_t * (4.5*y_t**2 + 1.5*y_b**2 + y_tau**2 - 17.0/12.0*g_y**2 - 2.25*g2**2 - 8.0*g3**2) / LOOP
    bb = y_b * (4.5*y_b**2 + 1.5*y_t**2 + y_tau**2 - 5.0/12.0*g_y**2 - 2.25*g2**2 - 8.0*g3**2) / LOOP
    bt = y_tau * (2.5*y_tau**2 + 3*y_t**2 + 3*y_b**2 - 15.0/4.0*g_y**2 - 2.25*g2**2) / LOOP
    bs = list(beta_scalar_quartics((lh, lp, le, p_hp, p_he, p_pe)))
    # SM gauge/top contributions to Higgs quartic; scalar contribution above is retained.
    bs[0] += (-6.0*y_t**4 - 6.0*y_b**4 - 2.0*y_tau**4 + 0.375*(2*g2**4 + (g2**2 + g_y**2)**2)
              + lh*(-9*g2**2 - 3*g_y**2 + 12*y_t**2 + 12*y_b**2 + 4*y_tau**2)) / LOOP
    # Gauge/Yukawa wavefunction terms for Higgs-singlet portals.
    portal_factor = 6*y_t**2 + 6*y_b**2 + 2*y_tau**2 - 4.5*g2**2 - 1.5*g_y**2
    bs[3] += p_hp * portal_factor / LOOP
    bs[4] += p_he * portal_factor / LOOP
    return (*bg, by, bb, bt, *bs)


def rk4(couplings: Sequence[float], dt: float, steps: int) -> tuple[float, ...]:
    """Fixed-step baseline RG integrator for t=ln(mu/mu0)."""
    state = tuple(map(float, couplings))
    for _ in range(steps):
        k1 = beta(state)
        k2 = beta(tuple(x + dt*v/2 for x, v in zip(state, k1)))
        k3 = beta(tuple(x + dt*v/2 for x, v in zip(state, k2)))
        k4 = beta(tuple(x + dt*v for x, v in zip(state, k3)))
        state = tuple(x + dt*(a + 2*b + 2*d + e)/6 for x, a, b, d, e in zip(state, k1, k2, k3, k4))
    return state
