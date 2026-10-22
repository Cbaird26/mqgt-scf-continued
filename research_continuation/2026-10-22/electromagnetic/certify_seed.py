#!/usr/bin/env python3
"""Exact-rational seed certificate for the stipulated spectral radius potential.

No external dependencies. All assertions use fractions.Fraction, including
rigorous exponential enclosures. Decimal is used solely to display bounds.

Definitions (n = 0,1,2; multiplicities = 12,28,16):
  H(R) = 30 + sum_n mult_n sum_{ell>=1} (2 ell+n) exp(-ell(ell+n)/R^2)
  F(R) = R H'(R) - 2 H(R)
       = -60 + sum 2 C_lambda (lambda/R^2 - 1) exp(-lambda/R^2)
  F'(R) = sum 4 C_lambda lambda R^-5 (lambda-2R^2) exp(-lambda/R^2).

At a root, c = H(R)/R^2 makes V = H-c R^2 flat and stationary,
and V'' = F'/R > 0. This is restricted radius-potential curvature;
it is neither a radion kinetic analysis nor a full stability theorem.

Tail proof for ell>N, uniform R in [rmin,rmax]:
  0 <= F_tail <= 224/rmin^2 * sum_{ell>N} (ell+1)^3 exp(-ell^2/rmax^2).
The inequalities use sum multiplicities=56, (2ell+n)<=2(ell+1),
ell(ell+n)<=(ell+1)^2, and omit the -1 in lambda/R^2-1.
With L=N+1, the successive ratio is bounded by
  rho=((L+2)/(L+1))^3 exp(-(2L+1)/rmax^2) < 1.
Thus the series is bounded by its first term divided by 1-rho.
All omitted terms in F' are positive when L^2 > 2 rmax^2.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from functools import lru_cache
from pathlib import Path


Q = Fraction
GRID_DIGITS = 80
GRID = 10**GRID_DIGITS
EVEN_TAYLOR_DEGREE = 40
N = 10
RMIN = Q("1.30078")
RMAX = Q("1.30079")
MULTIPLICITIES = ((0, 12), (1, 28), (2, 16))


@lru_cache(maxsize=None)
def exp_negative_interval(x: Fraction) -> tuple[Fraction, Fraction]:
    """Enclose exp(-x) by rationals, without calling exp or using floats.

    Scale x to y in [0,1]. Alternating Taylor partial sums of even degree
    40 and odd degree 41 enclose exp(-y). Round outwards onto a rational
    grid, then square the enclosure outwards once for every scaling step.
    """
    if x < 0:
        raise ValueError("x must be nonnegative")
    y = x
    squarings = 0
    while y > 1:
        y /= 2
        squarings += 1
    term = Q(1)
    partial = Q(1)
    upper = Q(1)
    for degree in range(1, EVEN_TAYLOR_DEGREE + 2):
        term *= -y / degree
        partial += term
        if degree == EVEN_TAYLOR_DEGREE:
            upper = partial
    lower = partial
    assert Q(0) < lower <= upper <= Q(1)
    low_int = lower.numerator * GRID // lower.denominator
    high_int = (
        upper.numerator * GRID + upper.denominator - 1
    ) // upper.denominator
    for _ in range(squarings):
        low_int = low_int * low_int // GRID
        high_int = (high_int * high_int + GRID - 1) // GRID
    return Q(low_int, GRID), Q(high_int, GRID)


def scaled_interval(
    coefficient: Fraction, interval: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    low, high = interval
    if coefficient >= 0:
        return coefficient * low, coefficient * high
    return coefficient * high, coefficient * low


def modes():
    for n, multiplicity in MULTIPLICITIES:
        for ell in range(1, N + 1):
            yield Q(ell * (ell + n)), Q(multiplicity * (2 * ell + n))


def f_prefix_interval(radius: Fraction) -> tuple[Fraction, Fraction]:
    low = high = -Q(60)
    for eigenvalue, coefficient in modes():
        x = eigenvalue / radius**2
        a, b = scaled_interval(
            2 * coefficient * (x - 1), exp_negative_interval(x)
        )
        low += a
        high += b
    return low, high


def f_tail_upper() -> tuple[Fraction, Fraction]:
    first = Q(N + 1)
    assert first**2 > 2 * RMAX**2
    rho_upper = (
        ((first + 2) / (first + 1)) ** 3
        * exp_negative_interval((2 * first + 1) / RMAX**2)[1]
    )
    assert 0 <= rho_upper < 1
    first_term_upper = (
        Q(224) / RMIN**2 * (first + 1) ** 3
        * exp_negative_interval(first**2 / RMAX**2)[1]
    )
    return first_term_upper / (1 - rho_upper), rho_upper


def derivative_uniform_lower() -> Fraction:
    """Termwise lower bound on F' over the entire closed radius interval."""
    lower = Q(0)
    for eigenvalue, coefficient in modes():
        if eigenvalue > 2 * RMAX**2:
            lower += (
                4 * coefficient * eigenvalue / RMAX**5
                * (eigenvalue - 2 * RMAX**2)
                * exp_negative_interval(eigenvalue / RMIN**2)[0]
            )
        elif eigenvalue < 2 * RMIN**2:
            lower -= (
                4 * coefficient * eigenvalue / RMIN**5
                * (2 * RMAX**2 - eigenvalue)
                * exp_negative_interval(eigenvalue / RMAX**2)[1]
            )
        else:
            raise AssertionError("An eigenmode crosses the sign threshold")
    # Omitted modes have eigenvalue >= (N+1)^2 > 2 RMAX^2;
    # all omitted derivative contributions are nonnegative.
    return lower


def bound_record(value: Fraction, direction: str) -> dict[str, str]:
    with localcontext() as context:
        context.prec = 70
        context.rounding = direction
        displayed = Decimal(value.numerator) / Decimal(value.denominator)
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "outward_decimal": str(displayed),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path,
        default=Path(__file__).with_name("stationary_seed_certificate.json"),
    )
    args = parser.parse_args()
    tail_upper, rho_upper = f_tail_upper()
    left_low, left_high = f_prefix_interval(RMIN)
    right_low, right_high = f_prefix_interval(RMAX)
    left_high += tail_upper
    right_high += tail_upper
    derivative_lower = derivative_uniform_lower()
    curvature_lower = derivative_lower / RMAX

    # Every comparison is an exact rational comparison.
    assert left_high < -Q(1, 10000)
    assert right_low > Q(2, 10000)
    assert derivative_lower > Q(32)
    assert curvature_lower > Q(24)
    assert tail_upper < Q(21, 10**27)

    result = {
        "status": "PASS",
        "scope": "Pure exponential profile f(u)=exp(-u), stipulated radius potential",
        "arithmetic": "Exact rational bounds and comparisons; no floating-point exp",
        "exp_method": {
            "even_taylor_degree": EVEN_TAYLOR_DEGREE,
            "odd_taylor_degree": EVEN_TAYLOR_DEGREE + 1,
            "argument_scaled_to": "[0,1]",
            "outward_rational_grid_digits": GRID_DIGITS,
        },
        "radial_levels_per_n_retained": N,
        "n_and_multiplicity": MULTIPLICITIES,
        "radius_bracket": [str(RMIN), str(RMAX)],
        "radius_bracket_decimal": ["1.30078", "1.30079"],
        "F_left": {
            "lower": bound_record(left_low, ROUND_FLOOR),
            "upper": bound_record(left_high, ROUND_CEILING),
        },
        "F_right": {
            "lower": bound_record(right_low, ROUND_FLOOR),
            "upper": bound_record(right_high, ROUND_CEILING),
        },
        "F_uniform_tail": {
            "lower": "0",
            "upper": bound_record(tail_upper, ROUND_CEILING),
            "geometric_ratio_upper": bound_record(rho_upper, ROUND_CEILING),
        },
        "Fprime_uniform_lower": bound_record(derivative_lower, ROUND_FLOOR),
        "restricted_curvature_at_root_lower": bound_record(curvature_lower, ROUND_FLOOR),
        "exact_comparison_checks": {
            "F_left_upper_below_minus_0.0001": True,
            "F_right_lower_above_0.0002": True,
            "Fprime_uniform_lower_above_32": True,
            "restricted_curvature_at_root_above_24": True,
            "F_tail_upper_below_2.1e-26": True,
        },
        "conclusions": [
            "A root exists strictly between 1.30078 and 1.30079.",
            "The root is unique within this bracket because Fprime is positive throughout.",
            "At the root, c=H/R^2 gives V=0 and Vprime=0 for V=H-c R^2.",
            "The restricted radius-potential curvature Vsecond=Fprime/R exceeds 24.",
        ],
        "limitations": [
            "No assertion of global uniqueness outside this interval.",
            "No assertion of global minimality of the radius potential.",
            "No radion kinetic normalization or full physical stability result.",
            "No prediction of measured electromagnetic coupling.",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "certificate": str(args.out.resolve()),
        "F_left_upper": result["F_left"]["upper"]["outward_decimal"],
        "F_right_lower": result["F_right"]["lower"]["outward_decimal"],
        "Fprime_uniform_lower": result["Fprime_uniform_lower"]["outward_decimal"],
        "restricted_curvature_lower": result["restricted_curvature_at_root_lower"]["outward_decimal"],
        "tail_upper": result["F_uniform_tail"]["upper"]["outward_decimal"],
    }, indent=2))


if __name__ == "__main__":
    main()
