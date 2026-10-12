#!/usr/bin/env python3
"""Verify the reviewed edition against both input PDFs and its sidecars.

Requires pikepdf, pypdf and Poppler. The private collection stays local.
The report contains hashes and page numbers, not extracted source text.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
import json
from pathlib import Path
import subprocess

import pikepdf
from pypdf import PdfReader


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def texts(path):
    result = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                            capture_output=True, check=True)
    pages = result.stdout.decode("utf-8").split("\f")
    if not pages[-1].strip():
        pages.pop()
    return [" ".join(t.replace("ﬁ", "fi").replace("ﬂ", "fl").split()) for t in pages]


def content(page):
    value = page.obj.get("/Contents")
    if value is None:
        return b""
    if isinstance(value, pikepdf.Stream):
        return value.read_bytes()
    return b"\n".join(stream.read_bytes() for stream in value)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for key in ("pdf", "input", "core-pdf", "report"):
        ap.add_argument("--" + key, type=Path, required=True)
    ap.add_argument("--metadata-dir", type=Path, default=Path(__file__).parent)
    args = ap.parse_args()
    manifest_bytes = (args.metadata_dir / "SOURCE_MANIFEST.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    assert digest(args.input) == manifest["derived_from"]["sha256"], "wrong collection"
    assert digest(args.core_pdf) == manifest["core_2026_09_18"]["sha256"], "wrong core"
    assert digest(args.pdf) == (args.metadata_dir / "SHA256SUMS").read_text().split()[0], "wrong output"
    # Output positions 160-7085 are canonical core pages. Every other retained
    # source position is checked against the full collection.
    surrounding = ([(n, n + 1) for n in range(4, 159)]
                   + [(n, n + 1) for n in range(7085, 7250)]
                   + [(n, n - 49) for n in range(7300, 7332)]
                   + [(n, n - 290) for n in range(7574, 7690)])
    with ThreadPoolExecutor(max_workers=3) as pool:
        public, full, core = list(pool.map(texts, [args.pdf, args.input, args.core_pdf]))
    assert [len(public), len(full), len(core)] == [7399, 7689, 6926]
    report = {
        "public_pdf_sha256": digest(args.pdf),
        "page_counts": {"public": len(public), "full": len(full), "core": len(core)},
        "core_pages_checked": 6926,
        "surrounding_source_pages_checked": len(surrounding),
        "core_text_mismatches": [n for n in range(1, 6927) if core[n-1] != public[n+158]],
        "surrounding_text_mismatches": [(s, p) for s, p in surrounding if full[s-1] != public[p-1]],
        "comparison_method": "pdftotext -layout; per-page whitespace and fi/fl ligature normalization",
    }
    with pikepdf.open(args.pdf) as out, pikepdf.open(args.input) as src, pikepdf.open(args.core_pdf) as cp:
        assert out.attachments["source_manifest.json"].get_file().read_bytes() == manifest_bytes
        assert out.attachments["source_manifest_full_collection_2026-10-01.json"].get_file().read_bytes() == src.attachments["source_manifest.json"].get_file().read_bytes()
        report["embedded_manifests_match"] = True
        report["core_content_stream_mismatches"] = [n for n in range(1, 6927) if content(cp.pages[n-1]) != content(out.pages[n+158])]
        report["surrounding_content_stream_mismatches"] = [(s, p) for s, p in surrounding if content(src.pages[s-1]) != content(out.pages[p-1])]
    reader, original = PdfReader(args.pdf), PdfReader(args.core_pdf)
    count = 0
    def walk(items):
        nonlocal count
        for item in items:
            if isinstance(item, list):
                walk(item)
            else:
                target = reader.get_destination_page_number(item)
                assert target is not None and 0 <= target < 7399
                count += 1
    walk(reader.outline)
    report["valid_outline_entries"] = count
    # add_pages_from preserves annotation-referenced destinations; unused labels
    # such as Doc-Start need not be imported into the new document.
    referenced = set()
    for page in original.pages:
        for ref in page.get("/Annots", []):
            annotation = ref.get_object()
            dest = annotation.get("/Dest")
            action = annotation.get("/A")
            if action and action.get("/S") == "/GoTo":
                dest = action.get("/D")
            if isinstance(dest, str):
                referenced.add(dest)
    dests = reader.named_destinations
    original_dests = original.named_destinations
    for name in referenced:
        dest = original_dests[name]
        assert name in dests, ("missing named destination", name)
        assert reader.get_destination_page_number(dests[name]) == original.get_destination_page_number(dest) + 159
    report["core_linked_named_destinations_preserved"] = len(referenced)
    rows = list(csv.DictReader((args.metadata_dir / "DUPLICATES.csv").open()))
    errors = []
    for row in rows:
        nums = [int(row["first_page"])] + [int(n) for n in row["duplicate_pages"].split(";")]
        if int(row["copies"]) != len(nums) or any(public[n-1] != public[nums[0]-1] for n in nums):
            errors.append(row["group"])
    report["duplicate_groups_checked"] = len(rows)
    report["duplicate_group_errors"] = errors
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    assert not any(v for k, v in report.items() if k.endswith("mismatches") or k.endswith("errors")), "verification failed"


if __name__ == "__main__":
    main()
