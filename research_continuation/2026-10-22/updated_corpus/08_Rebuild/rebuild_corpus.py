#!/usr/bin/env python3
"""Rebuild the reading corpus from its package-relative original components.
Usage: python3 08_Rebuild/rebuild_corpus.py /outside/package/rebuilt.pdf
PDF serialization may vary. The contract is decoded page content and geometry.
"""
from pathlib import Path
import hashlib,json,sys,tempfile,zipfile
import pikepdf
ROOT=Path(__file__).resolve().parents[1]
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def outlines(pdf):
 indexes={page.obj.objgen:i for i,page in enumerate(pdf.pages)}
 def target(dest):
  if isinstance(dest,(str,pikepdf.String,pikepdf.Name)):
   name=str(dest)
   tree=pdf.Root.get('/Names',{}).get('/Dests')
   obj=pikepdf.NameTree(tree).get(name) if tree is not None else None
   if obj is None:obj=pdf.Root.get('/Dests',{}).get('/'+name.lstrip('/'))
   dest=obj
  if isinstance(dest,pikepdf.Dictionary):dest=dest.get('/D')
  if isinstance(dest,pikepdf.Array) and len(dest):return indexes.get(dest[0].objgen)
  return None
 def walk(items):
  result=[]
  for item in items:
   d=item.destination
   if d is None and item.action is not None and item.action.get('/S')==pikepdf.Name('/GoTo'):d=item.action.get('/D')
   n=target(d)
   assert n is not None,('Unresolved bookmark',item.title)
   result.append({'title':item.title,'page':n,'children':walk(item.children)})
  return result
 with pdf.open_outline() as o:return walk(o.root)
def append_outline(items,offset):
 result=[]
 for i in items:
  o=pikepdf.OutlineItem(i['title'],i['page']+offset)
  o.children=append_outline(i['children'],offset);o.is_closed=True;result.append(o)
 return result
def build(output):
 output=Path(output).resolve()
 if output.is_relative_to(ROOT) and output.name!='A_Theory_of_Everything_UPDATED_CORPUS_2026-10-22.pdf':raise ValueError('Use an output outside the package.')
 if output.exists():raise FileExistsError(output)
 plan=json.loads((ROOT/'08_Rebuild/assembly_plan.json').read_text())
 pdf=pikepdf.new();groups=[];records=[]
 with tempfile.TemporaryDirectory(prefix='toe-corpus-') as temp:
  for part in plan['parts']:
   if 'archive' in part:
    path=Path(temp)/'baseline.pdf'
    with zipfile.ZipFile(ROOT/part['archive']) as z:
     with z.open(part['member']) as src,path.open('wb') as dest:
      import shutil;shutil.copyfileobj(src,dest)
   else:path=ROOT/part['path']
   assert digest(path)==part['sha256'],path
   start=len(pdf.pages)
   assert start+1==part['start']
   with pikepdf.open(path) as src:
    assert len(src.pages)==part['pages']
    children=outlines(src)
    result=pdf.add_pages_from(src)
    assert not result.dropped_dests,result.dropped_dests
    group=pikepdf.OutlineItem(part['title'],start);group.children=append_outline(children,start);group.is_closed=True;groups.append(group)
    records.append({'title':part['title'],'start':start+1,'pages':part['pages'],'dropped_destinations':list(result.dropped_dests),'renamed_destinations':dict(result.renamed_dests)})
  assert len(pdf.pages)==plan['expected_pages']
  with pdf.open_outline() as outline:outline.root=groups
  for name in ['CATALOG_NEW_WORK.json','PAGE_MAP.csv','CLAIM_STATUS.md']:pdf.attachments[name]=(ROOT/name).read_bytes()
  pdf.docinfo['/Title']=plan['title'];pdf.docinfo['/Author']='Christopher Michael Baird; source authors as attributed'
  pdf.docinfo['/Subject']='Archival research update; conditional results and finite-momentum stability obstructions'
  pdf.save(output,object_stream_mode=pikepdf.ObjectStreamMode.generate,compress_streams=True)
 return {'pages':len(pdf.pages),'parts':records}
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit(__doc__)
 r=build(sys.argv[1]);print(json.dumps(r,indent=2))
