from sm_gauge_core import COEFFICIENTS, NAMES, beta_gauge, landau_log_scale


def main():
    values = (0.357, 0.652, 1.221)
    print("SM one-loop gauge audit with Phi_c and E as gauge singlets")
    print("beta:", dict(zip(NAMES, (f"{v:.10e}" for v in beta_gauge(values)))))
    print(f"ln(mu_pole/mu0) for hypercharge: {landau_log_scale(values[0], COEFFICIENTS[0]):.6f}")
    print("Only the Gaussian point is a fixed point of this isolated one-loop gauge sector.")


if __name__ == "__main__":
    main()
