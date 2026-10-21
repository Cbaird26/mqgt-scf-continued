#!/usr/bin/env python3
"""Verify all SHA-256 entries. Python standard library only. Read-only."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[1]
errors=[];count=0
for line in (root/'SHA256SUMS.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 expected,rel=line.split('  ',1)
 p=(root/rel).resolve()
 if not p.is_relative_to(root):errors.append('Unsafe path: '+rel);continue
 if not p.is_file():errors.append('Missing: '+rel);continue
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(2**20),b''):h.update(chunk)
 if h.hexdigest()!=expected:errors.append('Mismatch: '+rel)
 count+=1
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {count} payload files match SHA-256 checksums.')
