#!/usr/bin/env python3
"""Publish only the approved, checked continuation artifact. Never force a ref."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile

REPO = 'Cbaird26/mqgt-scf-continued'
BASE = 'b50fb33ea8f82a3897cfef3b8d438b333b1f44c7'
TAG = 'v2026.10.21-research-continuation'
PREFIX = 'research_continuation/2026-10-21/'
ROOT = Path(__file__).resolve().parents[2]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def enc(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def api(method, suffix, data=None, optional=False):
    request = urllib.request.Request('https://api.github.com/repos/' + REPO + '/' + suffix,
        data=None if data is None else json.dumps(data).encode(), method=method,
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json',
                 'User-Agent': 'MQGT-SCF-verified-publication/1'})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if optional and error.code == 404:
            return None
        raise RuntimeError(f'GitHub {method} {suffix} returned HTTP {error.code}') from None


def main():
    approval = json.loads((ROOT / '.github/toe-release-approval.json').read_text())
    if approval['source_commit'] != BASE or approval['tag'] != TAG:
        raise RuntimeError('Unexpected approved source or tag')
    build = api('GET', 'actions/runs/' + str(approval['build_run_id']))
    if build['status'] != 'completed' or build['conclusion'] != 'success' or build['head_sha'] != approval['build_commit']:
        raise RuntimeError('Approved build did not succeed at the expected commit')
    info = api('GET', 'actions/artifacts/' + str(approval['artifact_id']))
    if info['digest'] != 'sha256:' + approval['artifact_sha256'] or info['expired']:
        raise RuntimeError('Approved artifact identity does not match')
    main_ref = api('GET', 'git/ref/heads/main')
    if main_ref['object']['sha'] != BASE:
        raise RuntimeError('Main advanced; reconcile before publishing, never overwrite it')
    if api('GET', 'git/ref/tags/' + TAG, optional=True) is not None:
        raise RuntimeError('Tag already exists; no replacement is permitted')
    for release in api('GET', 'releases?per_page=100'):
        if release['tag_name'] == TAG:
            raise RuntimeError('Release already exists; inspect it rather than overwrite')
    work = Path(os.environ['RUNNER_TEMP']) / 'toe-publish'
    work.mkdir(parents=True, exist_ok=True)
    assets = work / 'assets'
    subprocess.run(['gh', 'run', 'download', str(approval['build_run_id']), '--repo', REPO,
                    '--name', 'toe-continuation-release-build', '--dir', str(assets)], check=True)
    if sha((assets / 'RELEASE_ASSETS.json').read_bytes()) != approval['input_asset_manifest_sha256']:
        raise RuntimeError('Downloaded artifact metadata does not match the reviewed artifact')
    subprocess.run([sys.executable, str(ROOT / '.github/scripts/finalize_toe_release_assets.py'),
                    '--assets', str(assets)], check=True)
    meta = json.loads((assets / 'RELEASE_ASSETS.json').read_text())
    provenance = json.loads((assets / 'BUILD_PROVENANCE.json').read_text())
    finalization = json.loads((assets / 'FINALIZATION_VERIFICATION.json').read_text())
    if not provenance['report_text_matches_reviewed_reference'] or provenance['full_rerun_exit_code'] != 0:
        raise RuntimeError('The report or execution gate failed')
    if any(row['failures'] for row in provenance['comparisons']):
        raise RuntimeError('The numerical comparison gate failed')
    if not finalization['all_final_payload_hashes_passed'] or not finalization['all_active_thermal_inventory_hashes_passed']:
        raise RuntimeError('Final package integrity gate failed')
    expected = {}
    for record in meta['assets']:
        p = assets / record['name']
        if p.name != record['name'] or sha(p.read_bytes()) != record['sha256'] or p.stat().st_size != record['size_bytes']:
            raise RuntimeError('Final release asset does not match metadata')
        expected[p.name] = record['sha256']
    for name in ['RELEASE_ASSETS.json', 'RELEASE_SHA256SUMS.txt', 'FINALIZATION_VERIFICATION.json', 'PACKAGE_MANIFEST.json']:
        expected[name] = sha((assets / name).read_bytes())
    source = ROOT / PREFIX
    mirror = work / 'metadata'
    shutil.copytree(source, mirror)
    updates = {}
    def put(relative, raw):
        p = mirror / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)
        updates[PREFIX + relative] = raw.decode()
    put('sources/prepublication_RELEASE_ASSETS.json', (source / 'RELEASE_ASSETS.json').read_bytes())
    for name in ['RELEASE_ASSETS.json', 'RELEASE_SHA256SUMS.txt', 'PACKAGE_MANIFEST.json']:
        put(name, (assets / name).read_bytes())
    zipname = next(r['name'] for r in meta['assets'] if r['name'].endswith('.zip'))
    with zipfile.ZipFile(assets / zipname) as z:
        for name in ['README.txt', 'thermal/SHA256SUMS_CONTINUATION',
                     'sources/recorded_package_manifest.json', 'sources/github_rebuild_validation.json',
                     'sources/github_rebuild_execution.log', 'sources/historical_continuation_SHA256SUMS.txt',
                     'sources/finalization_verification.json']:
            put(name, z.read('toe_continuation_2026-10-21/' + name))
    put('sources/final_publication_verification.json', (assets / 'FINALIZATION_VERIFICATION.json').read_bytes())
    url = 'https://github.com/' + REPO + '/releases/tag/' + TAG
    notes = (source / 'RELEASE_NOTES.md').read_text()
    notes = notes.replace('Original numerical results and the report are\npreserved; the publication pass adds metadata and optional-validation handling.',
        'Original compact scientific records and normalized report text are preserved.\nMissing large outputs and rendering bytes were regenerated during publication;\nthe release carries new checksums and explicit build provenance.')
    checked = sum(row['numeric_or_boolean_values_checked'] for row in provenance['comparisons'])
    notes += ('\n## Publication rebuild and integrity\n\n'
        f'Clean build: https://github.com/{REPO}/actions/runs/{approval["build_run_id"]}.\n'
        f'{checked} numeric/Boolean reference comparisons passed; the 13-page report\n'
        'retains identical normalized extracted text. The distribution is a rebuilt\n'
        'artifact, not a byte-identical copy of the previously prepared ZIP.\n\n'
        f'The final payload manifest verifies {finalization["final_manifest_entries"]} files.\n'
        f'The active thermal checksum list verifies {finalization["active_thermal_inventory_entries"]} files;\n'
        'its earlier inventory is preserved with a historical label. The optional\n'
        'unlicensed EOS ancillary table is not redistributed. The frozen verification\n'
        'repository and older collection drafts are unchanged.\n\n'
        'This is an AI-assisted internal reproduction and publication checkpoint,\n'
        'not external peer review or confirmation of a complete Theory of Everything.\n')
    put('RELEASE_NOTES.md', notes.encode())
    readme = (source / 'README.md').read_text().replace('[Planned release]', '[Release]')
    start = readme.index('**Publication status')
    end = readme.index('\n## What is here', start)
    readme = readme[:start] + (
        '**Release checkpoint:** `' + TAG + '`. The dated release provides the report,\n'
        'complete offline ZIP, checksums, and build provenance. The download helper\n'
        'uses the final release hashes. The source snapshot preserves the scientific\n'
        'reference records; the offline manifest describes the rebuilt distribution.\n') + readme[end:]
    put('README.md', readme.encode())
    rootreadme = (ROOT / 'README.md').read_text()
    start = rootreadme.index('**Publication status (21 October 2026):**')
    end = rootreadme.index('\n\nThese are conditional', start)
    rootreadme = rootreadme[:start] + (
        '**Release checkpoint:** [' + TAG + '](' + url + ').\n'
        'The release contains the report, complete offline package, SHA-256\n'
        'checksums, and an explicit clean-build and packaging record. The\n'
        'scientific status below remains unchanged.') + rootreadme[end:]
    updates['README.md'] = rootreadme
    snapshot = {'version': TAG,
        'scope': 'Compact scientific reference source; rebuilt offline assets have their own package manifest',
        'source_files': [], 'offline_only_files': [],
        'release_zip_sha256': next(r['sha256'] for r in meta['assets'] if r['name'] == zipname)}
    for p in sorted(mirror.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts or p.suffix in {'.pyc', '.pyo'} or p.name == 'SOURCE_SNAPSHOT_MANIFEST.json':
            continue
        raw = p.read_bytes()
        snapshot['source_files'].append({'path': str(p.relative_to(mirror)), 'size_bytes': len(raw), 'sha256': sha(raw)})
    package_manifest = json.loads((mirror / 'PACKAGE_MANIFEST.json').read_text())
    snapshot['offline_only_files'] = [r for r in package_manifest['files'] if not (mirror / r['path']).is_file()]
    put('SOURCE_SNAPSHOT_MANIFEST.json', enc(snapshot))
    subprocess.run([sys.executable, str(mirror / 'verify_source_snapshot.py')], cwd=mirror, check=True)
    base = api('GET', 'git/commits/' + BASE)
    tree = api('POST', 'git/trees', {'base_tree': base['tree']['sha'], 'tree': [
        {'path': name, 'mode': '100644', 'type': 'blob', 'content': text} for name, text in sorted(updates.items())]})
    commit = api('POST', 'git/commits', {'message': 'release: finalize verified 2026-10-21 continuation assets and provenance',
        'tree': tree['sha'], 'parents': [BASE]})
    refname = 'refs/heads/checkpoint/2026-10-21-published'
    api('POST', 'git/refs', {'ref': refname, 'sha': commit['sha']})
    release = api('POST', 'releases', {'tag_name': TAG, 'target_commitish': commit['sha'],
        'name': 'MQGT-SCF Research Continuation — 2026-10-21', 'body': notes,
        'draft': True, 'prerelease': True, 'make_latest': 'false'})
    subprocess.run(['gh', 'release', 'upload', TAG, '--repo', REPO,
                    *[str(assets / name) for name in expected]], check=True)
    observed = api('GET', 'releases/' + str(release['id']))
    remote_assets = {a['name']: a for a in observed['assets']}
    for name, h in expected.items():
        a = remote_assets[name]
        if a['state'] != 'uploaded' or a['size'] != (assets / name).stat().st_size or a.get('digest') != 'sha256:' + h:
            raise RuntimeError('Uploaded release asset readback failed: ' + name)
    published = api('PATCH', 'releases/' + str(release['id']), {'draft': False, 'prerelease': True, 'make_latest': 'false'})
    if published['draft'] or not published.get('published_at'):
        raise RuntimeError('Release did not become public')
    tag = api('GET', 'git/ref/tags/' + TAG)['object']
    if tag['type'] == 'tag':
        tag = api('GET', 'git/tags/' + tag['sha'])['object']
    if tag['sha'] != commit['sha']:
        raise RuntimeError('Release tag does not point to the recorded source commit')
    main_updated = False
    if api('GET', 'git/ref/heads/main')['object']['sha'] == BASE:
        api('PATCH', 'git/refs/heads/main', {'sha': commit['sha'], 'force': False})
        main_updated = True
    receipt = {'release_url': published['html_url'], 'release_id': published['id'],
        'tag': TAG, 'source_commit': commit['sha'], 'published_at': published['published_at'],
        'draft': published['draft'], 'prerelease': published['prerelease'], 'main_fast_forwarded': main_updated,
        'assets_verified': [{'name': name, 'sha256': h} for name, h in expected.items()],
        'scientific_status': 'Conditional research checkpoint; no complete ToE or new-field detection claimed'}
    (work / 'publication_receipt.json').write_bytes(enc(receipt))
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
