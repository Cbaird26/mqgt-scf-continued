"""Audit the directly-contracted H + Phi_c + E scalar core."""
from higgs_two_singlet_core import NAMES, beta_scalar_quartics


def main():
    candidate = (0.038, 0.19, 0.14, 0.0, 0.0, 0.05)
    print("One-loop scalar-only H + Phi_c + E quartic-tensor audit")
    print("candidate:", dict(zip(NAMES, candidate)))
    print("beta:", dict(zip(NAMES, (f"{x:.10e}" for x in beta_scalar_quartics(candidate)))))
    print("No fixed-point conclusion beyond this scalar-only subsystem is implied.")


if __name__ == "__main__":
    main()
