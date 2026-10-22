#!/usr/bin/env python3
"""Rebuild the public reading copy from package-relative PDF components.
Run: python3 06_Rebuild/rebuild_public.py /path/to/rebuilt.pdf
The output must be outside the extracted package. PDF serialization may vary.
"""
from pathlib import Path
import sys,json,hashlib
import pikepdf
root=Path(__file__).resolve().parents[1]
plan=json.loads((root/'06_Rebuild/assembly_plan.json').read_text())
if len(sys.argv)!=2:raise SystemExit(__doc__)
outpath=Path(sys.argv[1]).resolve()
if outpath.is_relative_to(root):raise SystemExit('Choose an output path outside the package.')
if outpath.exists():raise SystemExit('Refusing to overwrite an existing file.')
out=pikepdf.new()
for part in plan['parts']:
 p=root/part['path']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==part['sha256'],p
 with pikepdf.open(p) as src:
  result=out.add_pages_from(src)
  assert not result.dropped_dests,result.dropped_dests
with out.open_outline() as outline:
 for item in plan['bookmarks']:outline.root.append(pikepdf.OutlineItem(item['title'],item['page']))
out.attachments['catalog.json']=(root/'CATALOG.json').read_bytes()
out.docinfo['/Title']=plan['title']
assert len(out.pages)==plan['expected_pages']
out.save(outpath,object_stream_mode=pikepdf.ObjectStreamMode.generate,compress_streams=True)
print(f'Rebuilt {len(out.pages)} pages: {outpath}')
