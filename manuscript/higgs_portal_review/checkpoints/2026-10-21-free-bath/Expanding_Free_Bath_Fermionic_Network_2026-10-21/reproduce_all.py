"""Portable reproduction of the expanding free-fermion benchmark.

Default reuses the six supplied scattering/reaction banks. --full first
reconstructs those six required banks. Independent archived diagnostic
files are preserved; see REPRODUCING.txt for their separate scripts.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help="Recompute the six required raw scattering and reaction banks.")
    parser.add_argument("--skip-report", action="store_true",
                        help="Skip the optional build_report.py step.")
    args = parser.parse_args()

    env = os.environ.copy()
    env["OPENBLAS_NUM_THREADS"] = "1"
    env.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "expanding_free_bath_matplotlib_cache"))

    def run(relative_script, *arguments):
        script = HERE / relative_script
        if not script.is_file():
            raise FileNotFoundError(f"Required reproduction script is missing: {script}")
        print(f"Running {relative_script}", flush=True)
        subprocess.run([sys.executable, str(script), *map(str, arguments)],
                       cwd=script.parent, env=env, check=True)

    scatter_coarse = HERE / "solver" / "bank_q40.npz"
    scatter_fine = HERE / "solver" / "bank_q48_eta16.npz"
    pair_coarse = HERE / "network" / "pair_bank.npz"
    pair_fine = HERE / "network" / "pair_bank_eta16.npz"
    decay_coarse = HERE / "network" / "decay_bank.npz"
    decay_fine = HERE / "network" / "decay_bank_eta16.npz"

    if args.full:
        # The final 16-interval graph is built directly. It contains all q48
        # 8-interval nodes, so a separate q48 coarse raw file is unnecessary.
        for output, intervals, q, boost, scattering, direction, azimuth in [
            (scatter_coarse, 8, 40, 28, 20, 20, 32),
            (scatter_fine, 16, 48, 32, 24, 24, 32),
        ]:
            run("solver/expanding_free_bath.py", "bank", "--output", output,
                "--bins", 192, "--ymax", 48, "--intervals", intervals,
                "--q", q, "--boost", boost, "--scattering", scattering,
                "--direction", direction, "--azimuth", azimuth)

        run("network/evolve_network.py", "make-pair-bank",
            "--scattering-bank", scatter_fine, "--output", pair_fine,
            "--intervals", 16, "--radial-order", 4, "--angular-order", 24)
        run("network/evolve_network.py", "make-pair-bank",
            "--scattering-bank", scatter_coarse, "--output", pair_coarse,
            "--intervals", 8, "--radial-order", 4, "--angular-order", 24,
            "--reuse-bank", pair_fine)

        for source, output in [(scatter_fine, decay_fine), (scatter_coarse, decay_coarse)]:
            run("network/build_decay_bank.py", "--source-bank", source,
                "--output", output, "--parent-order", 8,
                "--spectral-order", 64, "--tail-order", 64)
    else:
        required = [scatter_coarse, scatter_fine, pair_coarse, pair_fine,
                    decay_coarse, decay_fine]
        missing = [str(path.relative_to(HERE)) for path in required if not path.is_file()]
        if missing:
            raise FileNotFoundError("Required supplied banks are missing: " + ", ".join(missing)
                                    + ". Use --full to regenerate them.")
        print("Using the six supplied raw banks; pass --full to recompute them.", flush=True)

    run("analyze_network.py")
    run("network/reaction_rates.py", "--output", HERE / "network" / "reaction_rates.json",
        "--temperatures", 1/3, .4, .5, .6, .8, 1.)
    run("review/verify_background.py")
    run("review/verify_banks.py")

    report = HERE / "build_report.py"
    if report.is_file() and not args.skip_report:
        run("build_report.py")
    elif not args.skip_report:
        print("Optional build_report.py is absent; numerical reproduction is complete.", flush=True)
    print("Reproduction completed successfully for the declared expanding free-bath benchmark.", flush=True)


if __name__ == "__main__":
    main()
