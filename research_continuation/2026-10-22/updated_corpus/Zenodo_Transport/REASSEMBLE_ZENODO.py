#!/usr/bin/env python3
"""Reassemble the exact sealed research assets, checking every part and output.
Usage: python3 REASSEMBLE_ZENODO.py [download-directory] [output-directory]
Defaults: script directory; its reconstructed/ subdirectory. No dependencies.
Keep all downloaded files together. Existing correct outputs are left untouched.
"""
from pathlib import Path
import hashlib,json,os,shutil,sys,tempfile
base=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
out=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else base/'reconstructed'
out.mkdir(parents=True,exist_ok=True)
meta=json.loads((base/'ZENODO_TRANSPORT_MANIFEST.json').read_text())
def verify(path,item):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 if path.stat().st_size!=item['bytes'] or h.hexdigest()!=item['sha256']:
  raise ValueError('Checksum or size mismatch: '+str(path))
for item in meta['split_files']:
 target=out/item['name']
 if target.exists():verify(target,item);print('Already verified:',target.name);continue
 for part in item['parts']:
  if Path(part['name']).name!=part['name']:raise ValueError('Unsafe part name')
  verify(base/part['name'],part)
 fd,tmp=tempfile.mkstemp(prefix='.reassemble-',dir=out)
 try:
  with os.fdopen(fd,'wb') as dst:
   for part in item['parts']:
    with (base/part['name']).open('rb') as src:shutil.copyfileobj(src,dst)
  verify(Path(tmp),item)
  if target.exists():raise FileExistsError(target)
  Path(tmp).rename(target)
 finally:
  if Path(tmp).exists():Path(tmp).unlink()
 print('Reassembled and verified:',target.name)
for item in meta['original_assets']:
 target=out/item['name']
 if target.exists():verify(target,item);continue
 source=base/item['name']
 if source.is_file():
  verify(source,item);shutil.copy2(source,target);print('Verified:',target.name)
 else:print('Not downloaded:',item['name'])
print('Exact sealed originals are in',out)
print('These are archive integrity checks; scientific calculations were not rerun.')
