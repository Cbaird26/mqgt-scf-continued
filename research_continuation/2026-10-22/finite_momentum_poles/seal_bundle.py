"""Seal an explicit allowlist; do not include environments or scratch work."""
from pathlib import Path
import argparse,hashlib,json,shutil,zipfile
HERE=Path(__file__).resolve().parent
PDF='Finite_Momentum_Metric_Radion_Scalar_Poles_2026-10-22.pdf'
ZIP='Finite_Momentum_Poles_Reproducibility_2026-10-22.zip'
ROOT='Finite_Momentum_Poles_2026-10-22'
FILES=['README.md','ASSUMPTIONS.md','REVIEW.md','LICENSE','main.tex','tables.tex',
       'sections/operator.tex','sections/poles.tex','sections/limits.tex',
       'two_point.py','direct_vertices.py','poles.py','run_all.py','build_figures.py','seal_bundle.py',
       'mode_sums.py','vacuum.py','all_scalars.py','dynamics.py','requirements.txt','requirements-tested.txt',
       'results.json','checks.json','provenance.json','DELIVERY_VERIFICATION.json',
       'inputs/common_vacuum_pair.json','inputs/previous_radion_results.json','inputs/previous_radion_checks.json',
       'inputs/previous_vacuum_results.json','inputs/previous_radion_assumptions.md',
       'images/finite_momentum_poles.pdf','images/finite_momentum_poles.png','references/SOURCES.md',PDF]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def seal(out):
    out.mkdir(parents=True,exist_ok=True);(out/'pdf').mkdir(exist_ok=True)
    source=HERE/'main.pdf'
    if source.exists():shutil.copyfile(source,HERE/PDF)
    assert (HERE/PDF).exists()
    checks=json.loads((HERE/'checks.json').read_text())
    assert checks['passed']==checks['total']==194
    assert all(q['passed'] for q in checks['checks'].values())
    provenance=json.loads((HERE/'provenance.json').read_text())
    for name,sha in provenance['inherited_files_sha256'].items():assert digest(HERE/name)==sha,name
    for name in FILES:
        p=HERE/name;assert p.is_file() and not p.is_symlink(),name
        if p.suffix=='.tex':assert not any(ord(c)<32 and c!='\n' for c in p.read_text()),name
    manifest=''.join(digest(HERE/n)+'  '+n+'\n' for n in sorted(FILES))
    (HERE/'SHA256SUMS.txt').write_text(manifest)
    archive=out/ZIP
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(FILES+['SHA256SUMS.txt']):
            info=zipfile.ZipInfo(ROOT+'/'+name,date_time=(2026,10,22,12,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,(HERE/name).read_bytes())
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    shutil.copyfile(HERE/PDF,out/'pdf'/PDF)
    outer=digest(out/'pdf'/PDF)+'  pdf/'+PDF+'\n'+digest(archive)+'  '+ZIP+'\n'
    (out/'FINITE_MOMENTUM_POLES_SHA256SUMS.txt').write_text(outer)
    print(json.dumps({'payload_files':len(FILES),'zip':str(archive),'checksums':outer},indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=HERE.parent/'output')
    seal(parser.parse_args().output_dir)
