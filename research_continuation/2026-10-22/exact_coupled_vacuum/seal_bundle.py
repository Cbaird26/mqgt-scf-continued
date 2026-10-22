"""Seal the note and complete reproducibility payload; no network access.

Run after numerical reproduction, figure generation, source compilation,
visual inspection and updating DELIVERY_VERIFICATION.json. PDF compilation
can contain creation timestamps; a regenerated PDF need not be byte-identical.
"""
from pathlib import Path
import hashlib,json,shutil,zipfile

HERE=Path(__file__).resolve().parent
OUTPUT=HERE.parent/'output';(OUTPUT/'pdf').mkdir(parents=True,exist_ok=True)
PDF='Exact_Coupled_Scalar_Radius_Vacuum_2026-10-22.pdf'
ZIP='Exact_Coupled_Vacuum_Reproducibility_2026-10-22.zip'
ROOT='Exact_Coupled_Vacuum_2026-10-22'
FILES=['README.md','ASSUMPTIONS.md','REVIEW.md','LICENSE','main.tex','tables.tex',
       'vacuum.py','mode_sums.py','independent_checks.py','run_all.py','build_figures.py','seal_bundle.py',
       'requirements.txt','requirements-tested.txt','results.json','checks.json','provenance.json',
       'DELIVERY_VERIFICATION.json','inputs/common_vacuum_pair.json','inputs/previous_scalar_results.json',
       'images/untuned_action.pdf','images/untuned_action.png',PDF]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

if __name__=='__main__':
    if (HERE/'main.pdf').exists():shutil.copyfile(HERE/'main.pdf',HERE/PDF)
    report=json.loads((HERE/'checks.json').read_text())
    assert report['passed']==report['total'] and all(c['passed'] for c in report['checks'].values())
    for file in FILES:assert (HERE/file).is_file(),file
    manifest=''.join(digest(HERE/f)+'  '+f+'\n' for f in FILES)
    (HERE/'SHA256SUMS.txt').write_text(manifest)
    with zipfile.ZipFile(OUTPUT/ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in FILES+['SHA256SUMS.txt']:
            info=zipfile.ZipInfo(ROOT+'/'+name,date_time=(2026,10,22,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,(HERE/name).read_bytes())
    shutil.copyfile(HERE/PDF,OUTPUT/'pdf'/PDF)
    (OUTPUT/'EXACT_COUPLED_VACUUM_SHA256SUMS.txt').write_text(
        digest(OUTPUT/'pdf'/PDF)+'  pdf/'+PDF+'\n'+digest(OUTPUT/ZIP)+'  '+ZIP+'\n')
    print(json.dumps({'pdf':str(OUTPUT/'pdf'/PDF),'zip':str(OUTPUT/ZIP),
                      'payload_files':len(FILES),'checks':report['total'],
                      'pdf_sha256':digest(OUTPUT/'pdf'/PDF),'zip_sha256':digest(OUTPUT/ZIP)},indent=2))
