#!/usr/bin/env python3
"""PRIVATE/UNRELEASED ToE chronology builder. Requires PyMuPDF (`pip install pymupdf`).

Luna must test this script and verify output visually. It does not download files,
update git, publish Zenodo, or assert that mathematical claims are proven.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import fitz

# Source page numbers refer to the exact 146-page user-supplied companion packet.
# These 34 complete ranges preserve both variant manuscripts until compared.
# Month-only dates are an editorial ordering, not invented publication days.
CHRONOLOGY = [
    (6, 12, "2026-01-22 Fifth-force note"),
    (105, 109, "2026-02-07 Archetypal operators"),
    (110, 118, "2026-02-08 Minimal kernel"),
    (80, 82, "2026-02-09 Identity as Process"),
    (101, 104, "2026-02-13 Emergent matter"),
    (13, 19, "2026-02-18 Teleology manuscript"),
    (45, 45, "2026-02 (day unknown) Historical companion note"),
    (83, 89, "2026-02 (day unknown) Teleology variant"),
    (90, 100, "2026-02 (day unknown) Quantum-like learning toy"),
    (119, 122, "2026-02 (day unknown) Illustrative valuation - PRIVATE", "private"),
    (123, 123, "2026-02 (day unverified) Frequency atlas"),
    (124, 124, "2026-02 (day unverified) Frequency ladder"),
    (20, 22, "2026-03 (day unknown) Scientific status"),
    (23, 25, "2026-03 (day unknown) Core formalism"),
    (26, 27, "2026-03 (day unknown) Executive findings"),
    (28, 30, "2026-03 (day unknown) Lineage memo"),
    (46, 47, "2026-03 (day unknown) Replication summary"),
    (48, 49, "2026-03 (day unknown) Experiment plan"),
    (50, 51, "2026-03 (day unknown) H1 methods"),
    (52, 53, "2026-03 (day unknown) H2 memo"),
    (54, 55, "2026-03 (day unknown) H3 memo"),
    (56, 59, "2026-03 (day unknown) Phase II variant A"),
    (60, 63, "2026-03 (day unknown) Phase II variant B"),
    (64, 68, "2026-03 (day unknown) Minimal EFT anchor"),
    (69, 71, "2026-03 (day unknown) Hardening update"),
    (72, 73, "2026-03 (day unknown) GKSL/Jhana note"),
    (74, 76, "2026-03 (day unknown) Execution report"),
    (77, 79, "2026-03 (day unknown) Hypothesis campaign"),
    (31, 37, "2026-03-27 Recent work full addendum"),
    (38, 44, "2026-03-27 Recent work physics variant"),
    (125, 126, "2026-09-11 Errata sheet"),
    (127, 140, "2026-09-11 Reservoir protocol note"),
    (141, 143, "2026-09-13 Neutrino note (superseded in part)"),
    (144, 146, "2026-09-13 UV note (superseded in part)"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--core", type=Path, required=True, help="ACTUAL Sep 18 full corpus PDF")
    ap.add_argument("--companion", type=Path, required=True, help="Exact 146-page uploaded packet")
    ap.add_argument("--editorial", type=Path, required=True, help="Dated Sep 18-19 addendum PDF")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--public-candidate", action="store_true", help="Omit personal addendum and valuation; NOT clearance to publish")
    args = ap.parse_args()
    for p in (args.core, args.companion, args.editorial):
        if not p.is_file():
            ap.error(f"Required source PDF absent: {p}")
    if args.output.resolve() in {p.resolve() for p in (args.core, args.companion, args.editorial)}:
        ap.error("Output must not overwrite any source PDF")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with fitz.open(args.core) as core, fitz.open(args.companion) as packet, fitz.open(args.editorial) as editorial:
        if len(core) != 6926:
            ap.error(f"Latest 6926-page core not confirmed: found {len(core)} pages in {args.core}")
        if len(packet) != 146:
            ap.error(f"Unexpected companion packet: found {len(packet)} pages, expected 146")
        if not len(editorial):
            ap.error("Editorial addendum is empty")
        work = fitz.open()
        page = work.new_page(width=612, height=792)
        cover = [
            "THEORY OF EVERYTHING / MQGT-SCF", "CHRONOLOGICAL REVIEW EDITION - 19 SEPTEMBER 2026", "",
            "Christopher Michael Baird", "", "UNRELEASED REVIEW COPY - NOT A ZENODO DEPOSIT", "",
            "Base: Sep 18 full authored corpus (checked at 6,926 pages)",
            "Then: dated original companion papers, ordered by printed date", "Then: Sep 18-19 research corrections / editorial addendum",
            "Personal/symbolic appendix: " + ("excluded" if args.public_candidate else "included - PRIVATE"), "",
            "This document does not establish experimental detection or", "physical derivation of the electromagnetic coupling.",
            "Publication, licenses and privacy require author approval.",
        ]
        page.insert_text((52, 78), "\n".join(cover), fontsize=12, fontname="helv", lineheight=1.65)
        sections = [[1, "Edition notice (unreleased)", 1]]
        maprows = []

        def append(source, first, last, label, source_path):
            start = len(work) + 1
            work.insert_pdf(source, from_page=first, to_page=last)
            stop = len(work)
            sections.append([1, label, start])
            maprows.append({"merged_start": start, "merged_end": stop,
                            "source_path": str(source_path), "source_start": first + 1,
                            "source_end": last + 1, "label": label})

        append(core, 0, len(core)-1, "Sep 18 full corpus", args.core)
        for item in CHRONOLOGY:
            start, end, label = item[:3]
            if args.public_candidate and len(item) > 3 and item[3] == "private":
                continue
            append(packet, start - 1, end - 1, label, args.companion)
        append(editorial, 0, len(editorial)-1, "Sep 18-19 editorial update / claims and limits", args.editorial)
        if not args.public_candidate:
            append(packet, 0, 2, "Sep 19 Grok interface: private interpretive appendix", args.companion)
        work.set_toc(sections)
        work.set_metadata({"title":"ToE - chronological unreleased review edition - 2026-09-19",
                           "author":"Christopher Michael Baird",
                           "subject":"PRIVATE review; not validated or published"})
        tmp = args.output.with_name(args.output.name + ".building.pdf")
        try:
            work.save(str(tmp), garbage=3, deflate=True)
            with fitz.open(tmp) as check:
                if len(check) != len(work) or not check[0].get_text().strip():
                    raise RuntimeError("Post-save page/text verification failed")
            os.replace(tmp, args.output)
        finally:
            if tmp.exists():
                tmp.unlink()
        result = {"status":"UNRELEASED_REVIEW_COPY", "pages":len(work),
                  "pdf":str(args.output), "sha256":sha256(args.output),
                  "sources":{str(p):sha256(p) for p in (args.core, args.companion, args.editorial)},
                  "page_map":maprows}
        manifest_path = args.output.with_suffix(".manifest.json")
        manifest_path.write_text(json.dumps(result,indent=2),encoding="utf-8")
        print(json.dumps({"pdf":str(args.output),"pages":len(work),"sha256":result["sha256"],
                          "manifest":str(manifest_path)}, indent=2))
        work.close()

if __name__ == "__main__":
    main()
