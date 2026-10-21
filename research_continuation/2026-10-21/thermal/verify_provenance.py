"""Validate all acquired sources plus exact reconstructed numerical banks."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'download_manifest.json').read_text())
base=manifest['base'];checkpoint=manifest['checkpoint'];commit=manifest['commit'];repo=manifest['repository']
archive=json.loads((ROOT/'frozen'/'_archive'/'ARTIFACT_PARTS.json').read_text())
part_hashes={part['path']:part['sha256'] for item in archive['files'] for part in item['parts']}
rows=[];omitted=[]
for f in manifest['files']:
    path=f['path'];rel=path[len(base):] if path.startswith(base) else '_archive/'+path[len(checkpoint):]
    local=ROOT/'frozen'/rel
    if not local.exists() and rel.startswith('_archive/artifact_parts/'):
        # Compact distributions may omit redundant raw parts once their exact
        # reconstructed NPZ banks are present and verified below.
        part=rel[len('_archive/'):]
        assert part in part_hashes
        omitted.append(dict(path=path,git_blob_sha1=f['sha'],sha256=part_hashes[part],bytes=f['size'],
                            url=f'https://github.com/{repo}/blob/{commit}/{path}',status='Redundant split part omitted; exact reconstructed bank verified'))
        continue
    raw=local.read_bytes()
    sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert len(raw)==f['size'] and sha==f['sha'],path
    rows.append(dict(path=path,local=str(local.relative_to(ROOT)),url=f'https://github.com/{repo}/blob/{commit}/{path}',
                     git_blob_sha1=sha,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)))
checksum_matches=[]
for line in (ROOT/'frozen'/'SHA256SUMS').read_text().splitlines():
    expected,relative=line.split('  ',1);local=ROOT/'frozen'/relative
    if local.is_file():
        actual=hashlib.sha256(local.read_bytes()).hexdigest();assert actual==expected,relative
        checksum_matches.append(dict(path=relative,sha256=actual))
restored=[]
for f in archive['files']:
    rel=Path(f['target']).relative_to('Expanding_Free_Bath_Fermionic_Network_2026-10-21')
    raw=(ROOT/'frozen'/rel).read_bytes();actual=hashlib.sha256(raw).hexdigest()
    assert len(raw)==f['bytes'] and actual==f['sha256'],str(rel)
    restored.append(dict(path=str(rel),sha256=actual,bytes=len(raw)))
result=dict(repository=repo,commit=commit,verified_source_file_count=len(rows),files=rows,
            omitted_redundant_split_parts=omitted,
            source_checksum_matches=checksum_matches,exact_restored_banks=restored,
            missing_archived_diagnostics='Only the files used for this continuation and its review were acquired; this is not a complete repository mirror.')
(ROOT/'provenance_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(verified_git_blobs=len(rows),omitted_redundant_parts=len(omitted),verified_archived_sha256=len(checksum_matches),verified_restored_banks=len(restored))))
