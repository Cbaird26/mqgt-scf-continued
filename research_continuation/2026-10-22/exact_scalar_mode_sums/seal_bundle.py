"""Seal the already-compiled note and recorded calculations (standard library).

Run after run_all.py, build_figures.py and two pdflatex passes. The delivery
verification record describes the preparation run; update it if revalidating.
"""
from pathlib import Path
import argparse,hashlib,shutil,zipfile

ROOT=Path(__file__).resolve().parent
PDF='Exact_Scalar_Mode_Sums_and_Higgs_Kinetics_2026-10-22.pdf'
ARCHIVE='Exact_Scalar_Mode_Sums_Reproducibility_2026-10-22.zip'
PREFIX='Exact_Scalar_Mode_Sums_2026-10-22'
FILES=['README.md','ASSUMPTIONS.md','REVIEW.md','LICENSE','main.tex','tables.tex',
       'mode_sums.py','independent_checks.py','run_all.py','build_figures.py',
       'seal_bundle.py','requirements.txt','requirements-tested.txt',
       'results.json','checks.json','provenance.json','DELIVERY_VERIFICATION.json',
       'inputs/common_vacuum_pair.json','inputs/inherited_weak_coefficients.json',
       'images/scalar_response.pdf','images/scalar_response.png',PDF]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=ROOT.parent/'output')
    args=p.parse_args();out=args.output_dir.resolve();(out/'pdf').mkdir(parents=True,exist_ok=True)
    if (ROOT/'main.pdf').exists():shutil.copy2(ROOT/'main.pdf',ROOT/PDF)
    for f in FILES:
        if not (ROOT/f).is_file():raise FileNotFoundError(f)
    manifest=''.join(digest(ROOT/f)+'  '+f+'\n' for f in sorted(FILES))
    (ROOT/'SHA256SUMS.txt').write_text(manifest)
    with zipfile.ZipFile(out/ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted(FILES+['SHA256SUMS.txt']):
            info=zipfile.ZipInfo(PREFIX+'/'+f,date_time=(2026,10,22,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,(ROOT/f).read_bytes())
    shutil.copy2(ROOT/PDF,out/'pdf'/PDF)
    (out/'EXACT_MODE_SUMS_SHA256SUMS.txt').write_text(
        digest(out/'pdf'/PDF)+'  pdf/'+PDF+'\n'+digest(out/ARCHIVE)+'  '+ARCHIVE+'\n')
    print(out/'pdf'/PDF);print(out/ARCHIVE)

if __name__=='__main__':main()
