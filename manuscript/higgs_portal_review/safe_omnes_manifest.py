"""Offline provenance gate for the *four* pinned hipsofcobra Omnes input files.

This verifies size and Git blob SHA-1 only. It does not execute upstream code,
parse source data, certify grid units/coverage, or produce physical spectra.

Source revision: blackstonep/hipsofcobra@6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7
Input directory: hipsofcobra/input/
Expected metadata was transcribed from the pinned GitHub contents API.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import stat
import sys

REVISION = '6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7'
# (file length in bytes, Git *blob* ID, not SHA-1 of the raw file)
EXPECTED = {
    'hips_c1.txt': (2981801, '89cb2c3a7a992653521a9c2e9eb84295a0c45737'),
    'hips_c2.txt': (2981479, 'fa282fc1584322ed1f64902ca023fcdac8e01843'),
    'hips_d1.txt': (3032630, 'e5c0ef428e84e9605777dfa9845cc262e5b0e037'),
    'hips_d2.txt': (2939837, '1ff49406489df0dc90eabcb06acd99083bfcb56e'),
}


def git_blob_sha1(data: bytes) -> str:
    """Reference test helper for Git's blob hashing convention."""
    h = hashlib.sha1()
    h.update(b'blob ' + str(len(data)).encode('ascii') + b'\0')
    h.update(data)
    return h.hexdigest()


def verify_file(path: Path, *, expected_size: int, expected_blob: str,
                max_bytes: int = 5_000_000, sample_bytes: int = 96) -> tuple[bytes, str]:
    """Fail closed on unexpected bytes; return short sample + raw SHA-256.

    No data is evaluated, parsed, imported, or run. Never use a user-supplied
    path as a substitute for the manifest-controlled filenames in check_folder.
    """
    if not (0 <= sample_bytes <= 256):
        raise ValueError('sample_bytes must be between 0 and 256')
    if not (0 < expected_size <= max_bytes):
        raise ValueError('expected size exceeds configured file-size cap')
    if len(expected_blob) != 40 or any(x not in '0123456789abcdef' for x in expected_blob):
        raise ValueError('expected Git blob ID must be 40 lowercase hex digits')
    if path.is_symlink():
        raise ValueError('refusing symlink')
    flags = os.O_RDONLY
    if hasattr(os, 'O_NOFOLLOW'):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb') as stream:
        initial = os.fstat(stream.fileno())
        if not stat.S_ISREG(initial.st_mode):
            raise ValueError('refusing non-regular input')
        if initial.st_size != expected_size:
            raise ValueError(f'byte count mismatch: got {initial.st_size}, expected {expected_size}')
        h = hashlib.sha1()
        sha256 = hashlib.sha256()
        h.update(b'blob ' + str(initial.st_size).encode('ascii') + b'\0')
        count = 0
        sample = b''
        while True:
            chunk = stream.read(65536)
            if not chunk:
                break
            count += len(chunk)
            if count > max_bytes or count > expected_size:
                raise ValueError('input grew beyond permitted size')
            h.update(chunk)
            sha256.update(chunk)
            if len(sample) < sample_bytes:
                sample += chunk[:sample_bytes-len(sample)]
        final = os.fstat(stream.fileno())
        if (count != expected_size or final.st_size != expected_size
                or initial.st_mtime_ns != final.st_mtime_ns):
            raise ValueError('input changed during read or has unexpected length')
        if h.hexdigest() != expected_blob:
            raise ValueError('Git blob SHA-1 mismatch')
        return sample, sha256.hexdigest()


def check_folder(folder: Path, *, expected=EXPECTED, max_bytes: int = 5_000_000,
                 sample_bytes: int = 96) -> dict[str, tuple[bytes, str]]:
    """Only fixed manifest basenames are opened; fail on *any* missing/bad file."""
    output = {}
    for name, (size, blob_id) in expected.items():
        if Path(name).name != name or name in ('.', '..'):
            raise ValueError('manifest contains unsafe filename')
        output[name] = verify_file(folder / name, expected_size=size,
                                   expected_blob=blob_id, max_bytes=max_bytes,
                                   sample_bytes=sample_bytes)
    return output


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path, help='local directory with all four pinned Omnes inputs')
    parser.add_argument('--sample-bytes', type=int, default=96, help='show up to 256 literal, escaped bytes per file')
    args = parser.parse_args(argv)
    try:
        samples = check_folder(args.folder, sample_bytes=args.sample_bytes)
    except (OSError, ValueError) as exc:
        print(f'UNVERIFIED: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 1
    print(f'PASS: all {len(samples)} files match pinned size + Git blob SHA-1 at {REVISION}')
    for name, (sample, raw_sha256) in samples.items():
        print(f'{name}: raw SHA-256={raw_sha256}; escaped byte sample={sample!r}')
    print('NOT VERIFIED: grammar, grid extent/units, amplitudes, uncertainties, widths, or physics.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
