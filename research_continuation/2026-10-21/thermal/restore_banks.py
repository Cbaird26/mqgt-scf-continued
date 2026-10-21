"""Restore exact pinned raw banks, verifying archival SHA-256 checksums."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
source=ROOT/'frozen'/'_archive'
manifest=json.loads((source/'ARTIFACT_PARTS.json').read_text())
for item in manifest['files']:
    rel=Path(item['target']).relative_to('Expanding_Free_Bath_Fermionic_Network_2026-10-21')
    target=ROOT/'frozen'/rel
    if target.exists():
        raw=target.read_bytes()
        assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],'Refuse to overwrite changed frozen file'
        print(f'Verified existing {rel}: {len(raw)} bytes')
        continue
    blocks=[]
    for part in item['parts']:
        raw=(source/part['path']).read_bytes()
        assert len(raw)==part['bytes'] and hashlib.sha256(raw).hexdigest()==part['sha256']
        blocks.append(raw)
    raw=b''.join(blocks)
    assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    if target.exists():assert target.read_bytes()==raw,'Refuse to overwrite changed frozen file'
    else:target.write_bytes(raw)
    print(f'Verified {rel}: {len(raw)} bytes')
