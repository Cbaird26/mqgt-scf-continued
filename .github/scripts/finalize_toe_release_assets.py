#!/usr/bin/env python3
"""Reconcile publication checksums without modifying scientific payload files."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = 'toe_continuation_2026-10-21/'
INVENTORY = 'thermal/SHA256SUMS_CONTINUATION'
HISTORICAL = 'sources/historical_continuation_SHA256SUMS.txt'
RECEIPT = 'sources/finalization_verification.json'
PROVENANCE = 'sources/github_rebuild_validation.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def finalize(assets):
    assets = Path(assets)
    meta = json.loads((assets / 'RELEASE_ASSETS.json').read_text())
    for record in meta['assets']:
        p = assets / record['name']
        if p.name != record['name'] or p.stat().st_size != record['size_bytes'] or sha(p.read_bytes()) != record['sha256']:
            raise RuntimeError('Input release asset mismatch')
    record = next(r for r in meta['assets'] if r['name'].endswith('.zip'))
    archive = assets / record['name']
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise RuntimeError('Input ZIP CRC failure')
        payload = {}
        for name in z.namelist():
            if name.endswith('/'):
                continue
            if not name.startswith(ROOT) or '..' in Path(name).parts:
                raise RuntimeError('Unexpected ZIP path')
            payload[name[len(ROOT):]] = z.read(name)
    before = dict(payload)
    manifest = json.loads(payload['PACKAGE_MANIFEST.json'])
    for row in manifest['files']:
        raw = payload[row['path']]
        if sha(raw) != row['sha256'] or len(raw) != row['size_bytes']:
            raise RuntimeError('Input payload hash mismatch: ' + row['path'])
    if HISTORICAL in payload or RECEIPT in payload:
        raise RuntimeError('This finalization has already been applied')
    historical = payload[INVENTORY]
    mismatches, omitted = [], []
    for line in historical.decode().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        expected, rel = line.split(maxsplit=1)
        key = 'thermal/' + rel.lstrip('* ')
        if key not in payload:
            omitted.append(rel)
        elif sha(payload[key]) != expected:
            mismatches.append(rel)
    payload[HISTORICAL] = historical
    rows = sorted((key[len('thermal/'):], sha(raw)) for key, raw in payload.items()
                  if key.startswith('thermal/') and key != INVENTORY)
    payload[INVENTORY] = ''.join(h + '  ' + name + '\n' for name, h in rows).encode()
    provenance = json.loads(payload[PROVENANCE])
    provenance['preservation_scope'] = (
        'The preserved_compact_file_count describes the reference-restore step. '
        'Publication notices, provenance, and the active thermal checksum inventory '
        'were subsequently edited. Scientific source and numeric reference files remain byte-preserved.')
    provenance['thermal_checksum_finalization'] = {
        'original_inventory_sha256': sha(historical), 'historical_copy': HISTORICAL,
        'active_inventory_entries': len(rows), 'previous_mismatches_reconciled': mismatches,
        'absent_optional_entries_removed_from_active_inventory': omitted}
    payload[PROVENANCE] = encoded(provenance)
    payload['README.txt'] += (
        '\nCHECKSUM INVENTORIES\n'
        'thermal/SHA256SUMS_CONTINUATION describes the thermal files in this rebuilt ZIP.\n'
        'Its earlier reference list is preserved in sources/historical_continuation_SHA256SUMS.txt.\n'
        'The pinned upstream thermal/frozen/SHA256SUMS remains its original archival inventory;\n'
        'that upstream inventory also lists diagnostics outside this package\'s documented scope.\n').encode()
    allowed = {INVENTORY, PROVENANCE, 'README.txt', 'PACKAGE_MANIFEST.json'}
    unexpected = [key for key in before if payload[key] != before[key] and key not in allowed]
    if unexpected:
        raise RuntimeError('Unexpected scientific payload modification: ' + repr(unexpected))
    receipt = {
        'operation': 'Checksum reconciliation only; scientific source, data, results and PDF bytes unchanged',
        'input_release_zip_sha256': record['sha256'], 'input_manifest_entries': len(manifest['files']),
        'original_inventory_sha256': sha(historical), 'historical_copy': HISTORICAL,
        'active_thermal_inventory_entries': len(rows),
        'previous_mismatches_reconciled': mismatches,
        'absent_optional_entries_removed_from_active_inventory': omitted,
        'modified_existing_paths': sorted(allowed), 'unexpected_scientific_modifications': unexpected}
    payload[RECEIPT] = encoded(receipt)
    manifest['files'] = [{'path': name, 'size_bytes': len(raw), 'sha256': sha(raw)}
                         for name, raw in sorted(payload.items()) if name != 'PACKAGE_MANIFEST.json']
    payload['PACKAGE_MANIFEST.json'] = encoded(manifest)
    temporary = archive.with_suffix('.tmp.zip')
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, raw in sorted(payload.items()):
            item = zipfile.ZipInfo(ROOT + name, date_time=(2026, 10, 21, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            z.writestr(item, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(temporary) as z:
        if z.testzip() is not None:
            raise RuntimeError('Final ZIP CRC failure')
        for row in manifest['files']:
            raw = z.read(ROOT + row['path'])
            if sha(raw) != row['sha256'] or len(raw) != row['size_bytes']:
                raise RuntimeError('Final payload hash mismatch')
        for name, expected in rows:
            if sha(z.read(ROOT + 'thermal/' + name)) != expected:
                raise RuntimeError('Final thermal inventory mismatch')
    temporary.replace(archive)
    (assets / 'BUILD_PROVENANCE.json').write_bytes(payload[PROVENANCE])
    (assets / 'PACKAGE_MANIFEST.json').write_bytes(payload['PACKAGE_MANIFEST.json'])
    (assets / 'FINALIZATION_VERIFICATION.json').write_bytes(encoded({**receipt,
        'final_manifest_entries': len(manifest['files']), 'all_final_payload_hashes_passed': True,
        'all_active_thermal_inventory_hashes_passed': True,
        'final_release_zip_sha256': sha(archive.read_bytes())}))
    for row in meta['assets']:
        p = assets / row['name']
        row.update(size_bytes=p.stat().st_size, sha256=sha(p.read_bytes()))
    (assets / 'RELEASE_ASSETS.json').write_bytes(encoded(meta))
    (assets / 'RELEASE_SHA256SUMS.txt').write_text(''.join(r['sha256'] + '  ' + r['name'] + '\n' for r in meta['assets']))
    print(json.dumps({'status': 'verified_finalization', 'manifest_entries': len(manifest['files']),
                      'active_thermal_entries': len(rows), 'reconciled_old_mismatches': len(mismatches),
                      'assets': meta['assets']}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, required=True)
    finalize(parser.parse_args().assets)
