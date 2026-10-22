"""Seal explicit payload files; exclude environments, caches and scratch work.

Run after compilation and delivery verification. An optional output directory
may be supplied. ZIP metadata are fixed; rebuilding the PDF may change bytes.
"""
from pathlib import Path
import hashlib,json,shutil,sys,zipfile

HERE=Path(__file__).resolve().parent
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE.parent/'output'
PDF='Radion_Kinetics_and_Scalar_Mixing_2026-10-22.pdf'
ZIP='Radion_Dynamics_Reproducibility_2026-10-22.zip'
ROOT='Radion_Dynamics_2026-10-22'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

if (HERE/'main.pdf').exists():shutil.copyfile(HERE/'main.pdf',HERE/PDF)
assert (HERE/PDF).is_file()
names=['README.md','ASSUMPTIONS.md','REVIEW.md','LICENSE','main.tex','tables.tex',
       'dynamics.py','all_scalars.py','independent_checks.py','mode_sums.py','vacuum.py',
       'run_all.py','build_figures.py','seal_bundle.py','requirements.txt','requirements-tested.txt',
       'results.json','checks.json','provenance.json','DELIVERY_VERIFICATION.json',PDF]
for sub in ['sections','inputs','images','references']:
    names += [p.relative_to(HERE).as_posix() for p in sorted((HERE/sub).iterdir()) if p.is_file()]
names=sorted(names)
assert len(names)==len(set(names))==30
checks=json.loads((HERE/'checks.json').read_text())
assert checks['passed']==checks['total']==109
assert all(c['passed'] for c in checks['checks'].values())
manifest=''.join(f'{digest(HERE/name)}  {name}\n' for name in names)
(HERE/'SHA256SUMS.txt').write_text(manifest)
OUT.mkdir(parents=True,exist_ok=True);(OUT/'pdf').mkdir(exist_ok=True)
shutil.copyfile(HERE/PDF,OUT/'pdf'/PDF)
with zipfile.ZipFile(OUT/ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in names+['SHA256SUMS.txt']:
        info=zipfile.ZipInfo(ROOT+'/'+name,date_time=(2026,10,22,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
        z.writestr(info,(HERE/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
outer=f'{digest(OUT/"pdf"/PDF)}  pdf/{PDF}\n{digest(OUT/ZIP)}  {ZIP}\n'
(OUT/'RADION_DYNAMICS_SHA256SUMS.txt').write_text(outer)
print(json.dumps({'payload_files':len(names),'pdf':str(OUT/'pdf'/PDF),'zip':str(OUT/ZIP),
                 'sha256':{PDF:digest(OUT/'pdf'/PDF),ZIP:digest(OUT/ZIP)}},indent=2))
