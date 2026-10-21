#!/usr/bin/env python3
"""Verify the delivered package or rerun its declared calculations locally."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def verify():
    manifest = ROOT / "PACKAGE_MANIFEST.json"
    if not manifest.is_file():
        raise SystemExit("PACKAGE_MANIFEST.json is created at final packaging time")
    entries = json.loads(manifest.read_text())["files"]
    failures = []
    for item in entries:
        p = ROOT / item["path"]
        if not p.is_file():
            failures.append({"path": item["path"], "reason": "missing"})
            continue
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != item["sha256"]:
            failures.append({"path": item["path"], "reason": "sha256 mismatch"})
    print(json.dumps({"manifest_entries": len(entries), "failures": failures}, indent=2))
    return 1 if failures else 0


def run(name, relative, env, extra=()):
    script = ROOT / relative
    print(f"Running {name}: {relative}", flush=True)
    subprocess.run([sys.executable, str(script), *extra], cwd=script.parent,
                   env=env, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rerun", action="store_true", help="Rerun computations; overwrites generated result files and timestamps")
    parser.add_argument("--include-thermal", action="store_true", help="Also rerun the frozen-bank momentum network and EOS extension when present")
    parser.add_argument("--reference-uv-difference", action="store_true", help="Recompute the slower original finite-difference Jacobian comparison")
    args = parser.parse_args()
    if not args.rerun:
        return verify()
    env = dict(os.environ)
    env["OPENBLAS_NUM_THREADS"] = "1"
    env["OMP_NUM_THREADS"] = "1"
    env.setdefault("MPLCONFIGDIR", "/tmp/toe_continuation_matplotlib")
    run("common portal contract", "common/portal_interface.py", env)
    run("count-level measurement diagnostic", "measurement/poisson_visibility.py", env)
    run("spectral-profile continuation", "electromagnetic/spectral_profile_analysis.py", env)
    run("UV continuation", "uv/continue_uv.py", env,
        ["--reference-difference"] if args.reference_uv_difference else [])
    run("synthetic causal memory", "agency/synthetic_causal_memory.py", env)
    if args.include_thermal:
        run("restore pinned collision banks", "thermal/restore_banks.py", env)
        run("thermal initial-state continuation", "thermal/run_continuation.py", env)
        run("thermal table and figure", "thermal/make_report.py", env)
        eos = ROOT / "thermal/eos_sensitivity.py"
        if eos.is_file():
            run("equation-of-state sensitivity", "thermal/eos_sensitivity.py", env)
            run("equation-of-state summary and figure", "thermal/make_eos_report.py", env)
        run("source provenance verification", "thermal/verify_provenance.py", env)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
