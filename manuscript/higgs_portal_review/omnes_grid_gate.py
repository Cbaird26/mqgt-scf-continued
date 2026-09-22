"""Authenticated, prefix-only Omnes s-grid inspection; NO amplitude parsing or eval.

Requires four unmodified upstream files in an offline directory. This tool neither
runs hipsofcobra nor computes form factors or decay widths.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import math
import os
from pathlib import Path
import stat

REVISION = '6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7'
EXPECTED = {
    'hips_c1.txt': (2981801, '89cb2c3a7a992653521a9c2e9eb84295a0c45737'),
    'hips_c2.txt': (2981479, 'fa282fc1584322ed1f64902ca023fcdac8e01843'),
    'hips_d1.txt': (3032630, 'e5c0ef428e84e9605777dfa9845cc262e5b0e037'),
    'hips_d2.txt': (2939837, '1ff49406489df0dc90eabcb06acd99083bfcb56e'),
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def authenticated_bytes(path: Path, size: int, blob_sha: str) -> bytes:
    """Check a single bounded regular-file snapshot before inspecting any contents."""
    if not 0 < size <= 5_000_000:
        raise ValueError('unacceptable expected file size')
    if len(blob_sha) != 40 or any(ch not in '0123456789abcdef' for ch in blob_sha):
        raise ValueError('invalid expected Git blob id')
    if path.is_symlink():
        raise ValueError('symlink forbidden')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb') as f:
        before = os.fstat(f.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size != size:
            raise ValueError('nonregular or unexpected size')
        data = f.read(size + 1)
        after = os.fstat(f.fileno())
        if len(data) != size or before.st_size != after.st_size or before.st_mtime_ns != after.st_mtime_ns:
            raise ValueError('file changed or unexpected length')
    if git_blob_sha1(data) != blob_sha:
        raise ValueError('Git blob mismatch')
    return data


def first_grid(data: bytes, *, max_prefix: int = 30000) -> tuple[float, ...]:
    """Parse ONLY first [s0,...,sN] nested list with ast.literal_eval; ignore rest."""
    if not data.startswith(b'[['):
        raise ValueError('unexpected outer-list prefix')
    end = data.find(b']', 2, max_prefix)
    if end == -1 or data[end + 1:end + 2] != b',':
        raise ValueError('first grid missing or unexpectedly long')
    try:
        raw = ast.literal_eval(data[1:end + 1].decode('ascii'))
    except (ValueError, SyntaxError, UnicodeDecodeError, RecursionError, MemoryError) as exc:
        raise ValueError('invalid grid literals') from exc
    if not isinstance(raw, list) or len(raw) != 601:
        raise ValueError('expected 601 scalar s-grid points')
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in raw):
        raise ValueError('grid requires finite plain numbers')
    grid = tuple(float(x) for x in raw)
    if any(not math.isclose(x, i * 0.01, abs_tol=3e-12, rel_tol=0)
           for i, x in enumerate(grid)):
        raise ValueError('unexpected s-grid nodes')
    return grid


def inspect_folder(folder: Path, *, expected=EXPECTED) -> dict[str, tuple[float, ...]]:
    grids = {}
    for name, (size, sha) in expected.items():
        if Path(name).name != name or name in ('.', '..'):
            raise ValueError('unsafe manifest path')
        grids[name] = first_grid(authenticated_bytes(folder / name, size, sha))
    if any(grid != next(iter(grids.values())) for grid in grids.values()):
        raise ValueError('input s-grids disagree')
    return grids


def endpoint_gate(m1: float, m2: float, *, s_max: float = 6.) -> dict[str, float | bool]:
    if not all(map(math.isfinite, (m1, m2, s_max))) or not 0 < m1 < m2 or s_max <= 0:
        raise ValueError('invalid mass inputs')
    s_end = (m2 - m1)**2
    return {'s_endpoint_GeV2': s_end, 'within_grid': s_end <= s_max,
            'within_provisional_2_GeV_window': s_end <= 4.}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('folder', type=Path)
    args = p.parse_args(argv)
    try:
        grids = inspect_folder(args.folder)
    except (OSError, ValueError) as exc:
        print(f'UNVERIFIED: {type(exc).__name__}: {exc}')
        return 1
    print(f'PASS: {len(grids)} authenticated files share 601 s nodes, 0..6 GeV^2 in 0.01 increments')
    print('NOT CHECKED: numerical amplitude arrays, uncertainties, physical applicability, widths or total lifetime')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
