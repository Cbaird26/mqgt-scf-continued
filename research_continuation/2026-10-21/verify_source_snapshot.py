#!/usr/bin/env python3
"""Verify files in this compact Git source snapshot."""
import hashlib,json
from pathlib import Path
r=Path(__file__).resolve().parent
m=json.loads((r/'SOURCE_SNAPSHOT_MANIFEST.json').read_text())
bad=[]
for item in m['source_files']:
 p=r/item['path']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
  bad.append(item['path'])
print(json.dumps({'verified_files':len(m['source_files']),'failures':bad},indent=2))
raise SystemExit(bool(bad))
