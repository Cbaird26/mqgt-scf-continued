"""Read-only, pinned public source acquisition; verify Git blob hashes."""
from pathlib import Path
import concurrent.futures,hashlib,json,urllib.request,time
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'download_manifest.json').read_text())
commit=manifest['commit'];repo=manifest['repository'];base=manifest['base'];checkpoint=manifest['checkpoint']
def one(f):
    path=f['path'];rel=path[len(base):] if path.startswith(base) else '_archive/'+path[len(checkpoint):]
    out=ROOT/'frozen'/rel;out.parent.mkdir(parents=True,exist_ok=True)
    url=f'https://raw.githubusercontent.com/{repo}/{commit}/{path}'
    for attempt in range(4):
        try:
            raw=urllib.request.urlopen(url,timeout=90).read()
            assert len(raw)==f['size'],(path,len(raw),f['size'])
            blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            assert blob==f['sha'],(path,blob,f['sha'])
            out.write_bytes(raw)
            return dict(path=path,local=str(out.relative_to(ROOT)),url=url,bytes=len(raw),git_blob_sha1=blob,sha256=hashlib.sha256(raw).hexdigest())
        except Exception:
            if attempt==3:raise
            time.sleep(attempt+1)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    rows=list(pool.map(one,manifest['files']))
(ROOT/'source_provenance.json').write_text(json.dumps(dict(repository=repo,commit=commit,files=rows),indent=2)+'\n')
print(json.dumps({'downloaded':len(rows),'verified_bytes':sum(x['bytes'] for x in rows)}))
