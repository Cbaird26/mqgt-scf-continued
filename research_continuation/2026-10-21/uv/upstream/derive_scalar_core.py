"""Run an explicit audit of the two-scalar one-loop core."""
from scalar_core import LOOP, beta_scalar


def main():
    candidate = (0.19, 0.14, 0.05)
    print("Potential: lambda_phi*phi^4/4 + lambda_e*e^4/4 + kappa*phi^2*e^2/2")
    print(f"16 pi^2 = {LOOP:.12f}")
    print("beta(lambda_phi), beta(lambda_e), beta(kappa) at (0.19, 0.14, 0.05):")
    print(" ", tuple(f"{value:.10e}" for value in beta_scalar(candidate)))
    print("Conclusion: in the isolated real one-loop scalar core, the only fixed point is Gaussian.")
    print("A non-Gaussian point requires specified additional contributions (gravity, gauge, Yukawa, or higher operators).")


if __name__ == "__main__":
    main()
