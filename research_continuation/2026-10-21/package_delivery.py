#!/usr/bin/env python3
"""Build the lean offline archive and its SHA-256 inventory."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parent


def selected_files():
    excluded_source_files={"thermal/eos/Borsanyi_2010.pdf","thermal/eos/Borsanyi_2014.pdf",
                           "thermal/eos/WB-EoS.dat"}
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel=p.relative_to(ROOT)
        if any(part.startswith(".") or part=="__pycache__" for part in rel.parts):
            continue
        if str(rel).startswith("thermal/frozen/_archive/artifact_parts/"):
            continue
        if str(rel) in excluded_source_files or p.suffix in {".pyc",".pyo"}:
            continue
        if rel.name=="PACKAGE_MANIFEST.json":
            continue
        yield p


def write_manifest():
    records=[]
    for p in selected_files():
        records.append({"path":str(p.relative_to(ROOT)),"size_bytes":p.stat().st_size,
                        "sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
    payload={"package":"Theory of Everything research continuation","date":"2026-10-21",
             "sha256_scope":"Every delivered regular file except this self-referential manifest",
             "intentional_omissions":["Redundant split collision-bank parts; complete verified banks are present",
                                      "Python caches and source-directory metadata",
                                      "Two EOS reading PDFs and optional ancillary validation table; source URLs, hashes, analytic fit and historical validation results are present",
                                      "The original 9252-page uploaded archive; source hash and page map are present"],
             "files":records}
    (ROOT/"PACKAGE_MANIFEST.json").write_text(json.dumps(payload,indent=2)+"\n")
    return records


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--manifest-only",action="store_true")
    parser.add_argument("--output",type=Path,default=ROOT.parent/"output"/"MQGT_SCF_Research_Continuation_2026-10-21.zip")
    args=parser.parse_args()
    records=write_manifest()
    if args.manifest_only:
        print(json.dumps({"files":len(records),"bytes":sum(x['size_bytes'] for x in records)}))
        return
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.output,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for row in records:
            z.write(ROOT/row["path"],arcname=ROOT.name+"/"+row["path"])
        z.write(ROOT/"PACKAGE_MANIFEST.json",arcname=ROOT.name+"/PACKAGE_MANIFEST.json")
    with zipfile.ZipFile(args.output) as z:
        bad=z.testzip()
        if bad is not None:
            raise RuntimeError("Archive CRC failure: "+bad)
    print(json.dumps({"path":str(args.output),"files":len(records)+1,"size_bytes":args.output.stat().st_size,
                      "sha256":hashlib.sha256(args.output.read_bytes()).hexdigest()},indent=2))


if __name__=="__main__":
    main()
