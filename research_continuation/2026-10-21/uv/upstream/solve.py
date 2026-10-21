"""Numerical audit tools for a supplied 41-dimensional beta system."""
from __future__ import annotations

import argparse
import numpy as np

from model import INDEX, NAMES, FlowSpecification, gravity_beta, required_eta_n


def residual(beta, point):
    return float(np.linalg.norm(np.asarray(beta(point), dtype=float), ord=np.inf))


def finite_difference_jacobian(beta, point, step=1e-6):
    point = np.asarray(point, dtype=float)
    if point.shape != (len(NAMES),):
        raise ValueError("point must contain 41 coordinates")
    matrix = np.empty((len(NAMES), len(NAMES)))
    for j in range(len(NAMES)):
        delta = step * max(1.0, abs(point[j]))
        upper, lower = point.copy(), point.copy()
        upper[j], lower[j] = upper[j] + delta, lower[j] - delta
        matrix[:, j] = (np.asarray(beta(upper)) - np.asarray(beta(lower))) / (2.0 * delta)
    return matrix


def critical_exponents(beta, point):
    """Convention: theta = -eigenvalue(d beta / d g) at the fixed point."""
    return -np.linalg.eigvals(finite_difference_jacobian(beta, point))


def check_reported_point():
    point = np.zeros(len(NAMES))
    point[INDEX["gN"]] = 0.27
    point[INDEX["lambdaH"]] = 0.038
    eta = required_eta_n(point[INDEX["gN"]])
    print("reported gN=0.27, lambdaH=0.038")
    print(f"necessary eta_N at a nonzero fixed point: {eta:g}")
    print(f"beta_gN at eta_N={eta:g}: {gravity_beta(point[INDEX['gN']], eta):.3e}")
    print("Full certification: unavailable until all 41 projected beta functions are supplied.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-reported", action="store_true")
    args = parser.parse_args()
    if args.check_reported:
        check_reported_point()
    else:
        parser.error("Use --check-reported; a full solve requires a complete FlowSpecification.")
