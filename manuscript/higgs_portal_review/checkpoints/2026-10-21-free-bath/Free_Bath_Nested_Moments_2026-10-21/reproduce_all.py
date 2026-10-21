"""Recompute all supplied numerical outputs locally; no network access."""
from pathlib import Path
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
env = os.environ.copy()
env["OPENBLAS_NUM_THREADS"] = "1"


def run(script, *arguments):
    subprocess.run([sys.executable, str(HERE / script), *map(str, arguments)],
                   cwd=HERE, env=env, check=True)


run("reproduce_baseline.py")
setups = [
    (.4, 24, 8, 8, 4, 8, "results_q24.json"),
    (.4, 48, 12, 12, 4, 8, "results_q48.json"),
    (.4, 80, 20, 20, 6, 12, "results_q80.json"),
    (1 / 3, 48, 12, 12, 4, 8, "results_Tthird_q48.json"),
    (.5, 48, 12, 12, 4, 8, "results_Thalf_q48.json"),
]
for T, q, boost, scattering, direction, azimuth, output in setups:
    run("numerics/nested_free_bath.py", "--temperature", T, "--q", q,
        "--boost", boost, "--scattering", scattering, "--direction", direction,
        "--azimuth", azimuth, "--output", HERE / "numerics" / output)
run("numerics/verify_nested_results.py")
run("numerics/summarize_temperatures.py")
print("All requested calculations and numerical consistency checks completed.")
