from perturbative_matter_baseline import NAMES, beta, rk4


def main():
    # Illustrative weak-scale-like seed; portals are declared test inputs, not measurements.
    seed = (0.357, 0.652, 1.221, 0.936, 0.024, 0.010, 0.13, 0.19, 0.14, 0.01, 0.01, 0.05)
    print("initial beta:", dict(zip(NAMES, (f"{x:.6e}" for x in beta(seed)))))
    result = rk4(seed, dt=0.01, steps=100)
    print("one e-fold baseline flow:", dict(zip(NAMES, (f"{x:.6e}" for x in result))))


if __name__ == "__main__":
    main()
