#!/usr/bin/env python3
"""Explicitly download the pinned offline ZIP and verify its SHA-256."""
import argparse,hashlib,json,os,tempfile,urllib.request
from pathlib import Path
r=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--directory',type=Path,default=Path.cwd())
a=p.parse_args()
entry=next(x for x in json.loads((r/'RELEASE_ASSETS.json').read_text())['assets'] if x['name'].endswith('.zip'))
a.directory.mkdir(parents=True,exist_ok=True)
out=a.directory/entry['name']
if out.exists():
 if hashlib.sha256(out.read_bytes()).hexdigest()!=entry['sha256']:
  raise SystemExit('Existing destination has a different hash; choose another directory.')
 print('Already verified:',out)
 raise SystemExit(0)
fd,tmp=tempfile.mkstemp(prefix='.continuation-download-',dir=a.directory)
try:
 h=hashlib.sha256();size=0
 with os.fdopen(fd,'wb') as f,urllib.request.urlopen(entry['url'],timeout=60) as response:
  while chunk:=response.read(1024*1024):
   f.write(chunk);h.update(chunk);size+=len(chunk)
 if size!=entry['size_bytes'] or h.hexdigest()!=entry['sha256']:
  raise SystemExit('Downloaded asset failed size/SHA-256 verification.')
 os.replace(tmp,out)
 print('Verified:',out)
finally:
 if os.path.exists(tmp):os.unlink(tmp)
