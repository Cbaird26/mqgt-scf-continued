"""Read-only verification of every frozen package member and snapshot checksum."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    manifest = json.loads((HERE / 'CHECKPOINT_MANIFEST.json').read_text())
    total = 0
    for package in manifest['packages']:
        expected = set()
        for item in package['files']:
            relative = Path(item['path'])
            assert not relative.is_absolute() and '..' not in relative.parts
            p = HERE / relative
            assert p.is_file(), f'Missing: {relative}'
            assert p.stat().st_size == item['bytes'], f'Size changed: {relative}'
            assert digest(p) == item['sha256'], f'Hash changed: {relative}'
            expected.add(relative.as_posix())
            total += 1
        actual = {p.relative_to(HERE).as_posix() for p in (HERE / package['package']).rglob('*') if p.is_file()}
        assert actual == expected, f'Extra or missing files in {package["package"]}'
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        expected_hash, relative = line.split('  ', 1)
        assert digest(HERE / relative) == expected_hash, f'Checkpoint checksum changed: {relative}'
    print(f'PASS: {len(manifest["packages"])} packages, {total} byte-identical archived members, and all checkpoint checksums.')


if __name__ == '__main__':
    main()
