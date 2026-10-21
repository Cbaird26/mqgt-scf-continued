"""Exact Taylor coefficients of the declared scalar Litim LPA trace.

This is a new, bounded scalar-sector calculation. It does not supply any
graviton, gauge, fermion, nonminimal, or derivative-operator trace.
Fields are canonically normalized (Z=1), k=1, and eta_scalar=0 within this
scalar-only LPA block. The potential convention is the upstream convention:
U = sum_i m_i^2 phi_i^2/2 + quartics/4 + sextics/8, with four real Higgs
components and two real singlets. Couplings can be nonzero; coefficients
through field degree six are obtained algebraically, without finite
differences. Canonical scaling is deliberately separate.
"""
from __future__ import annotations

from math import pi
from typing import Iterable

EXP0 = (0, 0, 0)
MAX_DEGREE = 6
Poly = dict[tuple[int, int, int], float]

MASS_NAMES = ("mH2", "mPhi2", "mE2")
QUARTIC_NAMES = ("lambdaH", "lambdaPhi", "lambdaE", "kappaHPhi", "kappaHE", "kappaPhiE")
QUARTIC_POWERS = ((4, 0, 0), (0, 4, 0), (0, 0, 4), (2, 2, 0), (2, 0, 2), (0, 2, 2))
SEXTIC_NAMES = ("c_H6", "c_Phi6", "c_E6", "c_H4Phi2", "c_H4E2", "c_H2Phi4",
                "c_H2E4", "c_Phi4E2", "c_Phi2E4", "c_H2Phi2E2")
SEXTIC_POWERS = ((6, 0, 0), (0, 6, 0), (0, 0, 6), (4, 2, 0), (4, 0, 2),
                  (2, 4, 0), (2, 0, 4), (0, 4, 2), (0, 2, 4), (2, 2, 2))


def add(a: Poly, b: Poly, scale: float = 1.0) -> Poly:
    result = dict(a)
    for p, value in b.items():
        result[p] = result.get(p, 0.0) + scale * value
    return {p: value for p, value in result.items() if value != 0.0}


def multiply(a: Poly, b: Poly) -> Poly:
    result: Poly = {}
    for p, av in a.items():
        for q, bv in b.items():
            exponent = tuple(x + y for x, y in zip(p, q))
            if sum(exponent) <= MAX_DEGREE:
                result[exponent] = result.get(exponent, 0.0) + av * bv
    return {p: value for p, value in result.items() if value != 0.0}


def derivative(a: Poly, axis: int) -> Poly:
    result: Poly = {}
    for p, value in a.items():
        if p[axis]:
            q = list(p)
            q[axis] -= 1
            result[tuple(q)] = value * p[axis]
    return result


def scaled(a: Poly, factor: float) -> Poly:
    return {p: factor * value for p, value in a.items() if factor * value != 0.0}


def matrix_multiply(a: list[list[Poly]], b: list[list[Poly]]) -> list[list[Poly]]:
    result = [[{} for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] = add(result[i][j], multiply(a[i][k], b[k][j]))
    return result


def potential(masses: Iterable[float], quartics: Iterable[float], sextics: Iterable[float]) -> Poly:
    m, q, c = tuple(masses), tuple(quartics), tuple(sextics)
    if (len(m), len(q), len(c)) != (3, 6, 10):
        raise ValueError("expected 3 masses, 6 quartics and 10 sextics")
    result: Poly = {}
    for axis, value in enumerate(m):
        power = [0, 0, 0]
        power[axis] = 2
        result[tuple(power)] = float(value) / 2.0
    for power, value in zip(QUARTIC_POWERS, q):
        result[power] = float(value) / 4.0
    for power, value in zip(SEXTIC_POWERS, c):
        result[power] = float(value) / 8.0
    return {p: value for p, value in result.items() if value != 0.0}


def trace_polynomial(masses: Iterable[float], quartics: Iterable[float],
                     sextics: Iterable[float]) -> Poly:
    """Taylor polynomial of Tr(1 + Hessian(U))^-1 /(32 pi^2).

    On background (h,0,0,0,phi,e), the six-dimensional Hessian splits
    into a 3x3 radial block and three identical Higgs Goldstone entries.
    D is its field-independent 1+m^2 part and E has degree at least two.
    Therefore sum_{n=0}^3 (-D^-1 E)^n D^-1 is exact through degree six.
    Only the Taylor coefficients are asserted exact: the trace at finite
    field contains higher degrees that are not retained.
    """
    masses = tuple(map(float, masses))
    if any(1.0 + value <= 0.0 for value in masses):
        raise ValueError("this regular scalar chart requires 1 + m_i^2 > 0")
    u = potential(masses, quartics, sextics)
    hessian = [[derivative(derivative(u, i), j) for j in range(3)] for i in range(3)]
    inverse_d = tuple(1.0 / (1.0 + value) for value in masses)
    for i in range(3):
        hessian[i][i].pop(EXP0, None)
    # B = D^-1 E; trace(B^n D^-1) has alternating signs.
    b = [[scaled(hessian[i][j], inverse_d[i]) for j in range(3)] for i in range(3)]
    power = [[({EXP0: 1.0} if i == j else {}) for j in range(3)] for i in range(3)]
    result: Poly = {}
    for n in range(4):
        for i in range(3):
            result = add(result, power[i][i], ((-1.0) ** n) * inverse_d[i])
        power = matrix_multiply(power, b)

    # Goldstone Hessian = 2 dU/d(h^2), repeated three times.
    goldstone: Poly = {}
    for exponent, value in u.items():
        if exponent[0]:
            p = (exponent[0] - 2, exponent[1], exponent[2])
            goldstone[p] = exponent[0] * value
    goldstone.pop(EXP0, None)
    power_s: Poly = {EXP0: 1.0}
    for n in range(4):
        result = add(result, power_s, 3.0 * ((-1.0) ** n) * inverse_d[0] ** (n + 1))
        power_s = multiply(power_s, goldstone)
    return scaled(result, 1.0 / (32.0 * pi**2))


def project(masses=(0.0, 0.0, 0.0), quartics=(0.0,) * 6,
            sextics=(0.0,) * 10, canonical: bool = False) -> dict[str, float]:
    masses, quartics, sextics = tuple(masses), tuple(quartics), tuple(sextics)
    flow = trace_polynomial(masses, quartics, sextics)
    result: dict[str, float] = {}
    for i, name in enumerate(MASS_NAMES):
        power = [0, 0, 0]
        power[i] = 2
        result[name] = 2.0 * flow.get(tuple(power), 0.0)
        if canonical:
            result[name] -= 2.0 * masses[i]
    for name, power in zip(QUARTIC_NAMES, QUARTIC_POWERS):
        result[name] = 4.0 * flow.get(power, 0.0)
    for i, (name, power) in enumerate(zip(SEXTIC_NAMES, SEXTIC_POWERS)):
        result[name] = 8.0 * flow.get(power, 0.0)
        if canonical:
            result[name] += 2.0 * sextics[i]
    return result
