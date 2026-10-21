"""Reproduce the validated pure-gravity benchmark in one command."""
from einstein_hilbert_litim_benchmark import beta, critical_exponents, d4_fixed_point, eta


def main():
    lam, g = d4_fixed_point()
    print(f"lambda* = {lam:.12g}")
    print(f"g*_equation_normalization = {g:.12g}")
    print("beta* =", tuple(f"{value:.3e}" for value in beta(lam, g)))
    print(f"eta* = {eta(lam, g):.12g}")
    print("theta* =", tuple(f"{value.real:.12g}{value.imag:+.12g}i" for value in critical_exponents(lam, g)))


if __name__ == "__main__":
    main()
