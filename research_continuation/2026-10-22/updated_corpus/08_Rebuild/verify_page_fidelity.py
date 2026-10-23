#!/usr/bin/env python3
"""Compare every delivered page with its exact assembly input, including geometry.
Run from any directory with pikepdf installed. No scientific calculations are run.
"""
from pathlib import Path
import hashlib,json,tempfile,zipfile,shutil
import pikepdf
root=Path(__file__).resolve().parents[1]
plan=json.loads((root/'08_Rebuild/assembly_plan.json').read_text())
def signatures(path):
 result=[]
 with pikepdf.open(path) as pdf:
  for p in pdf.pages:
   v=p.obj.get('/Contents');raw=b'' if v is None else v.read_bytes() if isinstance(v,pikepdf.Stream) else b'\n'.join(x.read_bytes() for x in v)
   result.append((hashlib.sha256(raw).hexdigest(),tuple(map(str,p.mediabox)),tuple(map(str,p.cropbox)),int(p.obj.get('/Rotate',0))))
 return result
actual=signatures(root/'A_Theory_of_Everything_UPDATED_CORPUS_2026-10-22.pdf');expected=[]
with tempfile.TemporaryDirectory(prefix='toe-page-check-') as t:
 for part in plan['parts']:
  if 'archive' in part:
   p=Path(t)/'baseline.pdf'
   with zipfile.ZipFile(root/part['archive']) as z,z.open(part['member']) as source,p.open('wb') as destination:shutil.copyfileobj(source,destination)
  else:p=root/part['path']
  expected.extend(signatures(p))
assert len(actual)==plan['expected_pages'] and actual==expected
print(f'PASS: all {len(actual)} page content streams and page geometries match their assembly sources.')
