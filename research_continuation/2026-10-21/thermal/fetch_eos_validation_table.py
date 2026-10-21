#!/usr/bin/env python3
"""Explicitly retrieve the pinned optional EOS validation table.

The kinetic calculation uses the analytic published fit, not this table.
This helper is never called automatically by reproduce.py or eos_sensitivity.py.
See THIRD_PARTY_NOTICES.md for the source's separate distribution status.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import urllib.request

URL = "https://arxiv.org/src/1309.5258v2/anc/WB-EoS.dat"
SHA256 = "5f39782b65fcadf36a84c84afc57855cf7d20bc1f0b96f9d28c51737916b9550"
DEFAULT_PATH = Path(__file__).resolve().parent / "eos" / "WB-EoS.dat"


def verify(data: bytes) -> None:
    actual = hashlib.sha256(data).hexdigest()
    if actual != SHA256:
        raise ValueError(f"EOS table SHA-256 mismatch: expected {SHA256}, obtained {actual}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--verify-only", action="store_true", help="Check an existing file without network access.")
    args = parser.parse_args()
    target = args.output
    if target.is_file():
        verify(target.read_bytes())
        print(json.dumps({"status": "existing_file_verified", "path": str(target), "sha256": SHA256}))
        return
    if args.verify_only:
        raise FileNotFoundError(f"Optional EOS table is absent: {target}")
    request = urllib.request.Request(URL, headers={"User-Agent": "MQGT-SCF-research-continuation/2026.10.21"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(1024 * 1024 + 1)
    if len(data) > 1024 * 1024:
        raise ValueError("Unexpectedly large EOS validation response")
    verify(data)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix="eos-table-", delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(data)
    try:
        if target.exists():
            verify(target.read_bytes())
        else:
            temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps({"status": "downloaded_and_verified", "url": URL, "path": str(target), "sha256": SHA256}))


if __name__ == "__main__":
    main()
