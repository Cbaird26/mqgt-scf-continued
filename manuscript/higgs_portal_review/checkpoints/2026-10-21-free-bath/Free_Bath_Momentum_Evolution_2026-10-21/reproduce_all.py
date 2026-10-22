"""Portable reproduction of the fixed-temperature free-bath benchmark.

Default: reprocess the supplied collision graphs and rerun all comparisons
and checks. --full first reconstructs all four expensive collision graphs.
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
                        help="Recompute the four raw collision graphs before postprocessing.")
    parser.add_argument("--skip-report", action="store_true",
                        help="Skip the optional build_report.py step.")
    args = parser.parse_args()
    env = os.environ.copy()
    env["OPENBLAS_NUM_THREADS"] = "1"
    env.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "free_bath_matplotlib_cache"))

    def run(relative_script, *arguments):
        script = HERE / relative_script
        if not script.is_file():
            raise FileNotFoundError(f"Required reproduction script is missing: {script}")
        print(f"Running {relative_script}", flush=True)
        subprocess.run([sys.executable, str(script), *map(str, arguments)],
                       cwd=script.parent, env=env, check=True)

    if args.full:
        setups = [
            (128, 16, 32, 24, 16, 16, 24, "res32_bins128.json"),
            (128, 16, 48, 32, 24, 24, 32, "res48_bins128.json"),
            (128, 16, 64, 48, 32, 32, 48, "res64_bins128.json"),
            (192, 24, 80, 64, 40, 40, 48, "res80_bins192_tail24.json"),
        ]
        for bins, tail, q, boost, scattering, direction, azimuth, output in setups:
            run("solver/radial_free_bath.py", "--temperature", .4,
                "--bins", bins, "--tail-start", tail, "--q", q,
                "--boost", boost, "--scattering", scattering,
                "--direction", direction, "--azimuth", azimuth,
                "--output", HERE / "solver" / output)
    else:
        print("Using the four supplied raw collision graphs; pass --full to regenerate them.",
              flush=True)

    run("solver/analyze_convergence.py")
    run("comparison/moment_evolution.py", "--output",
        HERE / "comparison" / "moment_evolution.json")
    run("tail/tail_bound_constants.py", "--temperature", .4,
        "--output", HERE / "tail" / "tail_bound_constants.json")
    run("review/verify_final.py")

    report = HERE / "build_report.py"
    if report.is_file() and not args.skip_report:
        run("build_report.py")
    elif not args.skip_report:
        print("Optional build_report.py is absent; numerical reproduction is complete.", flush=True)
    print("Reproduction completed successfully. This is a fixed-temperature benchmark.", flush=True)


if __name__ == "__main__":
    main()
