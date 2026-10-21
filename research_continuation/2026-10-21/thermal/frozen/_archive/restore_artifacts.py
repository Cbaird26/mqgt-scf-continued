"""Restore the exact frozen collision banks from their ordered binary parts."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent


def safe_path(root: Path, relative: str) -> Path:
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError(f'Unsafe relative path: {relative}')
    target = (root / p).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes destination: {relative}')
    return target


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=HERE,
                        help='Optional separate directory for verifying exact reconstruction.')
    args = parser.parse_args()
    root = args.destination.resolve()
    manifest = json.loads((HERE / 'ARTIFACT_PARTS.json').read_text())
    restored = 0
    for item in manifest['files']:
        target = safe_path(root, item['target'])
        if target.exists():
            if target.stat().st_size != item['bytes'] or digest(target) != item['sha256']:
                raise RuntimeError(f'Refusing to overwrite a changed file: {target}')
            print(f'Already verified: {item["target"]}')
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=target.name + '.', suffix='.partial', dir=target.parent)
        temp = Path(temp_name)
        try:
            complete_hash = hashlib.sha256()
            complete_size = 0
            with os.fdopen(fd, 'wb') as out:
                for part in item['parts']:
                    source = safe_path(HERE, part['path'])
                    part_hash = hashlib.sha256()
                    part_size = 0
                    with source.open('rb') as inp:
                        for block in iter(lambda: inp.read(1024 * 1024), b''):
                            out.write(block)
                            part_hash.update(block)
                            complete_hash.update(block)
                            part_size += len(block)
                            complete_size += len(block)
                    if part_size != part['bytes'] or part_hash.hexdigest() != part['sha256']:
                        raise RuntimeError(f'Part integrity failure: {part["path"]}')
            if complete_size != item['bytes'] or complete_hash.hexdigest() != item['sha256']:
                raise RuntimeError(f'Restored-file integrity failure: {item["target"]}')
            # A hard link installs the verified file atomically without replacing
            # a concurrently created or user-modified destination.
            os.link(temp, target)
            restored += 1
            print(f'Restored and verified: {item["target"]}')
        finally:
            temp.unlink(missing_ok=True)
    print(f'PASS: {len(manifest["files"])} frozen banks verified; {restored} restored.')


if __name__ == '__main__':
    main()
