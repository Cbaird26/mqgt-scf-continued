#!/usr/bin/env python3
"""Rebuild the 2026-10-21 offline release without changing its reference records.

No publication is performed. Network use is limited to hash-pinned public input
acquisition. Missing large outputs are regenerated, compared to the recorded
results, and identified as regenerated rather than represented as original bytes.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import zipfile

SOURCE_COMMIT = 'b50fb33ea8f82a3897cfef3b8d438b333b1f44c7'
TAG = 'v2026.10.21-research-continuation'
REPO = 'Cbaird26/mqgt-scf-continued'
PDF_NAME = 'Theory_of_Everything_Continuation_2026-10-21.pdf'
ZIP_NAME = 'MQGT_SCF_Research_Continuation_2026-10-21.zip'
REFERENCE_PDF_SHA256 = '9488d93d948e129b45f4073e11f346af783dbac09dab9a5570882d827ba8d325'
REFERENCE_TEXT_SHA256 = 'cf199b6152d50948a0e65b4b3b99b0e9e51aebb94ed4edbd94c188c20bda4f5b'
RESULTS = ['common/common_results.json', 'thermal/results/scan_summary.json',
           'thermal/eos/eos_sensitivity_results.json', 'measurement/measurement_results.json',
           'electromagnetic/profile_identifiability_results.json', 'uv/results.json',
           'agency/synthetic_memory_results.json']


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_path(root: Path, relative: str) -> Path:
    p = root / relative
    if not p.resolve().is_relative_to(root.resolve()):
        raise ValueError('Unsafe relative path: ' + relative)
    return p


def fetch(url: str) -> bytes:
    host = urllib.parse.urlparse(url).hostname
    if host not in {'raw.githubusercontent.com', 'zenodo.org'}:
        raise ValueError('Input download host is not allowed')
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'MQGT-SCF-checkpoint-rebuild/1'})
            with urllib.request.urlopen(req, timeout=120) as res:
                return res.read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError('Unreachable')


def run(script: Path, cwd: Path, log: Path, extra: tuple[str, ...] = ()) -> None:
    env = dict(os.environ)
    env.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MPLBACKEND='Agg',
               PYTHONUNBUFFERED='1')
    for key in ('GH_TOKEN', 'GITHUB_TOKEN', 'ACTIONS_RUNTIME_TOKEN'):
        env.pop(key, None)
    with log.open('ab') as stream:
        stream.write(('\nRUN ' + str(script.relative_to(cwd)) + ' ' + ' '.join(extra) + '\n').encode())
        stream.flush()
        subprocess.run([sys.executable, str(script), *extra], cwd=cwd, env=env,
                       stdout=stream, stderr=subprocess.STDOUT, check=True)


def numbers(value, path=()):
    if isinstance(value, dict):
        for k, v in value.items():
            if k in {'elapsed_seconds', 'environment', 'run_started_utc', 'run_completed_utc'}:
                continue
            yield from numbers(v, path + (k,))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from numbers(v, path + (str(i),))
    elif isinstance(value, (int, float, bool)):
        yield '/'.join(path), value


def compare(reference, actual, filename: str):
    if filename.endswith('eos_sensitivity_results.json'):
        reference = {k: reference[k] for k in ('parameters_2014', 'summary')}
        actual = {k: actual[k] for k in ('parameters_2014', 'summary')}
    a, b = dict(numbers(reference)), dict(numbers(actual))
    errors = []
    for key, expected in a.items():
        if key not in b:
            errors.append({'path': key, 'reason': 'missing'})
            continue
        got = b[key]
        if isinstance(expected, bool):
            ok = isinstance(got, bool) and got == expected
        elif isinstance(expected, int):
            ok = got == expected
        else:
            ok = (math.isnan(expected) and math.isnan(got)) or math.isclose(
                expected, got, rel_tol=1e-6, abs_tol=1e-10)
        if not ok:
            errors.append({'path': key, 'expected': expected, 'actual': got})
    return {'file': filename, 'numeric_or_boolean_values_checked': len(a),
            'relative_tolerance': 1e-6, 'absolute_tolerance': 1e-10,
            'integer_and_boolean_comparison': 'exact', 'failures': errors}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    stage = output.parent / 'offline_stage' / 'toe_continuation_2026-10-21'
    if stage.exists():
        raise RuntimeError('Refuse to reuse an existing staging directory')
    stage.mkdir(parents=True)
    manifest_raw = (source / 'PACKAGE_MANIFEST.json').read_bytes()
    original_manifest = json.loads(manifest_raw)
    preserved = {}
    for row in original_manifest['files']:
        p = safe_path(source, row['path'])
        if p.is_file():
            raw = p.read_bytes()
            if digest(raw) != row['sha256']:
                raise RuntimeError('Recorded compact input differs: ' + row['path'])
            target = safe_path(stage, row['path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            preserved[row['path']] = raw
    references = {n: json.loads((stage / n).read_bytes()) for n in RESULTS}
    acquired = []
    manifest = json.loads((stage / 'thermal/download_manifest.json').read_text())
    if manifest['commit'] != '48f9dcbd34e7cfb86504167a0483f732a5dd5e8e' or manifest['repository'] != REPO:
        raise RuntimeError('Unexpected thermal input provenance')

    def acquire_thermal(row):
        path = row['path']
        relative = (path[len(manifest['base']):] if path.startswith(manifest['base'])
                    else '_archive/' + path[len(manifest['checkpoint']):])
        target = safe_path(stage / 'thermal/frozen', relative)
        if target.exists():
            return None
        url = f"https://raw.githubusercontent.com/{REPO}/{manifest['commit']}/" + urllib.parse.quote(path, safe='/')
        raw = fetch(url)
        git_sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if len(raw) != row['size'] or git_sha != row['sha']:
            raise RuntimeError('Thermal source hash mismatch: ' + path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        return {'path': str(target.relative_to(stage)), 'url': url, 'sha256': digest(raw)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        acquired.extend(x for x in pool.map(acquire_thermal, manifest['files']) if x)
    data = next(x for x in json.loads((stage / 'sources/source_catalog.json').read_text())['sources'] if x['id'] == 'D1')
    data_url = 'https://zenodo.org/records/17502163/files/Na-Cluster-Interference.zip?download=1'
    archive = stage / 'measurement/sources/Na-Cluster-Interference.zip'
    raw = archive.read_bytes() if archive.exists() else fetch(data_url)
    if digest(raw) != data['zip_sha256'] or hashlib.md5(raw).hexdigest() != data['zip_md5']:
        raise RuntimeError('Public count-data ZIP hash mismatch')
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(raw)
    acquired.append({'path': str(archive.relative_to(stage)), 'url': data_url, 'sha256': digest(raw)})
    extracted = stage / 'measurement/sources/pedalino_original'
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            if name.endswith('/'):
                continue
            target = safe_path(extracted, name)
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(name))
    log = output / 'rebuild_execution.log'
    run(stage / 'reproduce.py', stage, log, ('--rerun', '--include-thermal'))
    comparisons = [compare(references[n], json.loads((stage / n).read_text()), n) for n in RESULTS]
    (output / 'result_comparison.json').write_text(json.dumps(comparisons, indent=2) + '\n')
    if any(x['failures'] for x in comparisons):
        raise RuntimeError('Scientific result comparison failed; publication is blocked')
    for name, raw in preserved.items():
        safe_path(stage, name).write_bytes(raw)
    (stage / 'sources/recorded_package_manifest.json').write_bytes(manifest_raw)
    shutil.copy2(log, stage / 'sources/github_rebuild_execution.log')
    run(stage / 'reports/build_report.py', stage, log)
    from pypdf import PdfReader
    pdf = stage / 'reports' / PDF_NAME
    reader = PdfReader(pdf)
    text = ''.join(''.join(p.extract_text().split()) for p in reader.pages)
    text_sha = digest(text.encode())
    if len(reader.pages) != 13:
        raise RuntimeError('Unexpected report page count')
    if text_sha != REFERENCE_TEXT_SHA256:
        raise RuntimeError('Rebuilt report text differs from reviewed report; publication is blocked')
    if (stage / 'thermal/eos/WB-EoS.dat').exists():
        raise RuntimeError('Uncleared optional EOS table must not be redistributed')
    for row in original_manifest['files']:
        if not safe_path(stage, row['path']).is_file():
            raise RuntimeError('Offline package is missing: ' + row['path'])
    provenance = {
        'version': TAG, 'source_commit': SOURCE_COMMIT,
        'build_commit': os.environ.get('GITHUB_SHA'),
        'workflow_run': os.environ.get('GITHUB_RUN_ID'),
        'kind': 'Reconstructed offline publication; not a byte-identical copy of the earlier prepared ZIP',
        'original_reference_manifest_sha256': digest(manifest_raw),
        'preserved_compact_file_count': len(preserved),
        'missing_large_outputs_regenerated': True,
        'reference_pdf_sha256': REFERENCE_PDF_SHA256,
        'rebuilt_pdf_sha256': digest(pdf.read_bytes()),
        'report_page_count': len(reader.pages),
        'report_text_matches_reviewed_reference': text_sha == REFERENCE_TEXT_SHA256,
        'report_normalized_text_sha256': text_sha,
        'source_acquisition': acquired, 'comparisons': comparisons,
        'full_rerun_exit_code': 0,
        'scope': 'Internal software reproduction and packaging, not external scientific validation',
    }
    notice = ('\nPUBLICATION REBUILD\n'
              'This offline distribution was reconstructed from the pinned public source checkpoint.\n'
              'Previously recorded compact sources and results are preserved byte-for-byte. Missing\n'
              'large outputs were regenerated; numeric/boolean reference checks passed, and the\n'
              '13-page report has identical normalized extracted text to the reviewed report.\n'
              'The ZIP and rendering bytes have new hashes. See sources/github_rebuild_validation.json.\n')
    with (stage / 'README.txt').open('a') as f:
        f.write(notice)
    (stage / 'sources/github_rebuild_validation.json').write_text(json.dumps(provenance, indent=2) + '\n')
    run(stage / 'package_delivery.py', stage, log, ('--output', str(output / ZIP_NAME)))
    run(stage / 'reproduce.py', stage, log)
    shutil.copy2(pdf, output / PDF_NAME)
    shutil.copy2(stage / 'PACKAGE_MANIFEST.json', output / 'PACKAGE_MANIFEST.json')
    (output / 'BUILD_PROVENANCE.json').write_text(json.dumps(provenance, indent=2) + '\n')
    assets = []
    for name in (PDF_NAME, ZIP_NAME, 'BUILD_PROVENANCE.json'):
        p = output / name
        assets.append({'name': name, 'size_bytes': p.stat().st_size, 'sha256': digest(p.read_bytes()),
                       'url': f'https://github.com/{REPO}/releases/download/{TAG}/{name}'})
    (output / 'RELEASE_ASSETS.json').write_text(json.dumps({'version': TAG,
        'release_url': f'https://github.com/{REPO}/releases/tag/{TAG}', 'assets': assets}, indent=2) + '\n')
    (output / 'RELEASE_SHA256SUMS.txt').write_text(''.join(x['sha256'] + '  ' + x['name'] + '\n' for x in assets))
    print(json.dumps({'status': 'verified_rebuild', 'assets': assets,
                      'numeric_values_checked': sum(x['numeric_or_boolean_values_checked'] for x in comparisons)}, indent=2))


if __name__ == '__main__':
    main()
