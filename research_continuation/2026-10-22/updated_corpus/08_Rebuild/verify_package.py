#!/usr/bin/env python3
"""Verify the full edition manifest and every retained ZIP's CRC; no science rerun."""
from pathlib import Path,PurePosixPath
import hashlib,zipfile
root=Path(__file__).resolve().parents[1]
lines=(root/'SHA256SUMS.txt').read_text().splitlines();seen=set()
for line in lines:
 expected,name=line.split('  ',1);p=PurePosixPath(name)
 assert not p.is_absolute() and '..' not in p.parts and name not in seen
 seen.add(name);h=hashlib.sha256()
 with (root/name).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 assert h.hexdigest()==expected,name
for p in root.rglob('*.zip'):
 with zipfile.ZipFile(p) as z:assert z.testzip() is None,p
print(f'PASS: {len(lines)} payload SHA-256 hashes and all nested ZIP CRC checks. Scientific calculations were not rerun.')
