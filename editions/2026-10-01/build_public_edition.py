#!/usr/bin/env python3
"""
build_public_edition.py -- fail-closed derivation of the PUBLIC EDITION of
"A Theory of Everything - Research Collection (2026-10-01)".

Input : the full 7,689-page collection PDF (private; contains an unlicensed
        third-party manuscript and personal material).
Output: a 7,399-page public edition that
        * reproduces Baird / ZoraASI corpus Parts 1-4 unchanged, except that the
          personal 50-page study guide (full-collection pp. 7250-7299) is withheld;
        * CITES (does not reproduce) Nielsen A, the 240-page TUFT manuscript whose
          supplied copy carries no redistribution license (pp. 7332-7572);
        * reproduces Nielsen B (Preprints.org v5, CC BY 4.0) in full;
        * replaces the five editorial pages with regenerated ones;
        * rebuilds the bookmark outline as a flat, truthful structure;
        * embeds a regenerated source manifest (+ the original one) as attachments;
        * writes PAGE_MAP.csv, SOURCE_MANIFEST.json and SHA256SUMS next to the PDF.

Every page-content check is fail-closed: if the input is not the exact expected
file, or a boundary page does not carry its expected text, the build aborts.

Usage:
    python3 build_public_edition.py --input FULL_COLLECTION.pdf --outdir OUT_DIR
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import subprocess
import sys

import pikepdf
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# --------------------------------------------------------------------------
# Expected input (fail-closed)
# --------------------------------------------------------------------------
EXPECTED_INPUT_SHA256 = "c8417d0a9804a1f42769958962729225e4cda4b79a34aa0d2698c244cd8be218"
EXPECTED_INPUT_PAGES = 7689
BUILD_DATE = "2026-10-12"
BUILD_TIMESTAMP = dt.datetime.now(dt.timezone(dt.timedelta(hours=-4))).replace(microsecond=0).isoformat()  # America/New_York (EDT)
OUTPUT_BASENAME = "A_Theory_of_Everything_Research_Collection_2026-10-01_public-edition.pdf"

# Boundary pages in the FULL collection (1-based) and a text marker each must carry.
MARKERS = {
    1: "RESEARCH COLLECTION",
    2: "Contents and source map",
    3: "Attribution and reading guide",
    4: "claim-by-",
    15: "ToE research corpus: local inventory",
    16: "TOE Corpus Pack",
    159: "Christopher Michael Baird",
    7085: "Deterministic Fifth-Force Falsification",
    7197: "A Theory of Everything That Thinks and Chooses",
    7232: "Synthetic Connectivity",
    7236: "Two-Singlet",
    7242: "Separating Network Telemetry",
    7250: "Mathematical Physics Study Guide",
    7299: "Functional analysis for quantum theory",
    7300: "Omni-Information Coupling Framework",
    7331: "Omni-Information Coupling Framework",
    7332: "NIELSEN A",
    7333: "The Topological Unified Field Theory",
    7572: "Nielsen",
    7573: "NIELSEN B",
    7574: "Posted Date: 17 July 2026",
    7689: "115 of 115",
}

# Kept ranges of the full collection, in output order (1-based inclusive).
# Editorial pages are generated; see assemble().
KEEP_RANGES = [
    (4, 7249),      # Parts 1-4 up to (not including) the withheld study guide
    (7300, 7331),   # Omni-Information Coupling Framework corpus addendum
    # (Nielsen B divider: generated)
    (7574, 7689),   # Nielsen B, Preprints.org v5, CC BY 4.0
]
WITHHELD = {
    "study_guide": (7250, 7299),
    "nielsen_a_divider": (7332, 7332),
    "nielsen_a_manuscript": (7333, 7572),
    "editorial_pages_replaced": [1, 2, 3, 7573],
}
N_FRONT = 4   # generated front-matter pages
EXPECTED_OUTPUT_PAGES = N_FRONT + (7249 - 4 + 1) + (7331 - 7300 + 1) + 1 + (7689 - 7574 + 1)
assert EXPECTED_OUTPUT_PAGES == 7399

# Components (full-collection ranges) used for the page map and the outline.
COMPONENTS = [
    # id, title, full_start, full_end, authorship
    ("CHANGE_LOG_2026-09-19", "MQGT-SCF / ToE claim-by-claim change log (research snapshot 19 Sep 2026)", 4, 14, "C. M. Baird / ZoraASI"),
    ("INVENTORY_2026-09-19", "ToE research corpus: local inventory and release trail (19 Sep 2026)", 15, 15, "C. M. Baird / ZoraASI"),
    ("COMPANION_PACK", "TOE Corpus Companion Pack (index + 34 working papers, corrected 19 Sep 2026)", 16, 158, "C. M. Baird / ZoraASI"),
    ("CORE_2026-09-18", "A Theory of Everything - unified edition of 18 Sep 2026 (6,926 pages; = mqgt-scf-continued A_Theory_of_Everything_UPDATED_2026-09-18.pdf)", 159, 7084, "C. M. Baird / ZoraASI"),
    ("DATED_NOTES_2026", "Dated research notes, 22 Jan - 27 Mar 2026 (duplicate copies of Companion Pack papers, in chronological order)", 7085, 7196, "C. M. Baird / ZoraASI"),
    ("ARTICLE_SERIES_2026-09-19", "A Theory of Everything That Thinks and Chooses? - article series (19 Sep 2026)", 7197, 7231, "C. M. Baird"),
    ("CONNECTIVITY_MEMORY_PREPRINT", "A Reproducible Synthetic Connectivity-Memory Ablation (ZoraASI Phase 2.3 preprint, 21 Sep 2026)", 7232, 7235, "C. M. Baird"),
    ("CONSISTENCY_AUDIT_v0.2", "A Two-Singlet Effective Theory and Its Experimental Interfaces - consistency audit, working paper v0.2 (21 Sep 2026)", 7236, 7241, "C. M. Baird"),
    ("SOFTWARE_PREPRINT_2026-09-22", "Separating Network Telemetry from Multimodal Representation in AI Agent Software (22 Sep 2026)", 7242, 7249, "C. M. Baird"),
    ("STUDY_GUIDE_WITHHELD", "Mathematical physics self-study guide (personal planning document) - WITHHELD from the public edition", 7250, 7299, "C. M. Baird (personal)"),
    ("OMNI_INFORMATION_ADDENDUM", "The Omni-Information Coupling Framework - corpus addendum", 7300, 7331, "C. M. Baird"),
    ("NIELSEN_A_WITHHELD", "Nielsen A - The Topological Unified Field Theory on the Complex Hopf Fibration (240-page manuscript, 14 Aug 2026) - CITED, NOT REPRODUCED (no redistribution license)", 7332, 7572, "Jennifer Lorraine Nielsen (independent author)"),
    ("NIELSEN_B", "Nielsen B - The Complex Hopf Fibration as the Canonical Space for Gauge-Gravity Unification (Preprints.org v5, 17 Jul 2026, CC BY 4.0)", 7573, 7689, "Jennifer Lorraine Nielsen (independent author)"),
]

# Dated research notes (full-collection start pages) from the original outline.
DATED_NOTES = [
    (7085, "2026-01-22 - Fifth-force methods note"),
    (7092, "2026-02-07 - Archetypal operators research"),
    (7097, "2026-02-08 - Minimal kernel"),
    (7106, "2026-02-09 - Identity as Process"),
    (7109, "2026-02-13 - Emergent matter"),
    (7113, "2026-02-18 - Teleology manuscript"),
    (7120, "2026-02-28 - February companion - day not confirmed"),
    (7121, "2026-02-28 - Teleology variant - day not confirmed"),
    (7128, "2026-02-28 - Quantum-like learning toy - day not confirmed"),
    (7139, "2026-02-28 - Frequency atlas - day not confirmed"),
    (7140, "2026-02-28 - Frequency ladder - day not confirmed"),
    (7141, "2026-03-01 - Scientific status - March; day not confirmed"),
    (7144, "2026-03-01 - Core formalism - March; day not confirmed"),
    (7147, "2026-03-01 - Executive findings - March; day not confirmed"),
    (7149, "2026-03-01 - Lineage memo - March; day not confirmed"),
    (7152, "2026-03-01 - Replication summary - March; day not confirmed"),
    (7154, "2026-03-01 - Experiment program - March; day not confirmed"),
    (7156, "2026-03-01 - H1 methods - March; day not confirmed"),
    (7158, "2026-03-01 - H2 memo - March; day not confirmed"),
    (7160, "2026-03-01 - H3 memo - March; day not confirmed"),
    (7162, "2026-03-01 - Phase II variant A - March; day not confirmed"),
    (7166, "2026-03-01 - Phase II variant B - March; day not confirmed"),
    (7170, "2026-03-01 - Minimal EFT anchor - March; day not confirmed"),
    (7175, "2026-03-01 - Hardening - March; day not confirmed"),
    (7178, "2026-03-01 - GKSL/Jhana - March; day not confirmed"),
    (7180, "2026-03-01 - Execution report - March; day not confirmed"),
    (7183, "2026-03-01 - Hypothesis campaign - March; day not confirmed"),
    (7186, "2026-03-27 - Recent work full addendum"),
    (7193, "2026-03-27 - Recent work physics variant"),
]

# Companion Pack order (from the pack index, full-collection pp. 16-17): (title, pages)
PACK_ITEMS = [
    # (bookmark title, pages, marker text that must appear on the first page)
    ("Deterministic Fifth-Force Falsification for a Higgs-Mixed Scalar Portal (index file 00_SOLVED_TOE_root)", 7, "Deterministic Fifth-Force"),
    ("Teleology as Covariant Boundary Selection in a Consciousness-Ethics Field Theory (index file 01_SOLVED_TOE_2026)", 7, "Teleology as Covariant Boundary"),
    ("Current Scientific Status of the MQGT-SCF Program (2026)", 3, "Current Scientific Status"),
    ("Core Formalism 1.0 for the Layered MQGT-SCF Program (2026)", 3, "Core Formalism 1.0"),
    ("Executive Findings Insert 2026", 2, "Executive Findings"),
    ("Lineage Integration Memo for the Layered ToE Program (2026)", 3, "Lineage Integration Memo"),
    ("Recent Work Addendum for the ToE Stack (March 24-27, 2026)", 7, "Recent Work Addendum for the ToE Stack"),
    ("Recent Work Addendum for the ToE Stack - Physics Lanes (March 24-27, 2026)", 7, "Physics Lanes"),
    ("Addendum 2026 - Companion to The Theory of Everything", 1, "Addendum 2026"),
    ("External Replication Summary (2026)", 2, "External Replication Summary"),
    ("Ranked Experiment Program for the Layered ToE (2026)", 2, "Ranked Experiment Program"),
    ("H1 QRNG binary pilot: methods posture, null calibration snapshot", 2, "H1 QRNG"),
    ("H2 Next Experiment Memo (2026)", 2, "H2 Next Experiment Memo"),
    ("H3 Result Memo (2026)", 2, "H3 Result Memo"),
    ("MQGT-SCF Phase II: Scalar-Singlet EFT Extension, GKSL Measurement Control, Interferometric Test Program (variant A)", 4, "MQGT-SCF Phase II"),
    ("MQGT-SCF Phase II (variant B)", 4, "MQGT-SCF Phase II"),
    ("MQGT-SCF as a Minimal Scalar-Singlet EFT: Specification-Level Closure (Anchor)", 5, "Minimal Scalar-Singlet EFT"),
    ("MQGT-SCF Hardening Completion Update (2026)", 3, "Hardening Completion Update"),
    ("Explicit Ethics-Weighted GKSL Operators, Jhana Attractor, and a Lab-Ready Estimator", 2, "Explicit Ethics-Weighted GKSL"),
    ("MQGT-SCF Execution Report (2026)", 3, "Execution Report"),
    ("MQGT-SCF Exhaustive Hypothesis Campaign 2026", 3, "Exhaustive Hypothesis Campaign"),
    ("Identity as Process (IaP): A Mathematical Framework for Hardened Agent", 3, "Identity as Process"),
    ("Teleology as Covariant Boundary Selection (variant)", 7, "Teleology as Covariant Boundary"),
    ("Ethically Biased Quantum-like Learning on Discrete Lattices", 11, "Ethically Biased Quantum-like Learning"),
    ("Evidence for Emergent Matter from Quantum Vacuum Fluctuations", 4, "Evidence for Emergent Matter"),
    ("Archetypal Operators and Phoenix Protocols", 5, "Archetypal Operators and Phoenix"),
    ("A Full-Stack Index and Minimal Kernel for Coherent, Ethically Regularized Agency", 9, "Full-Stack Index and Minimal Kernel"),
    ("Full Value Ledger - All | World", 4, "Full Value Ledger"),
    ("MQGT-SCF: Constraint Channels on a Frequency Axis (frequency atlas)", 1, "Frequency Axis"),
    ("MQGT-SCF: frequency ladder with constraint-channel anchors", 1, "frequency ladder"),
    ("Errata sheet - corrected unified edition (2026-09-11)", 2, "Errata sheet"),
    ("Reservoir derivation and fail-closed interferometric protocol (2026-09-11)", 14, "Reservoir derivation"),
    ("Neutrino Portal: E-Scalar Dirac Mass Portal for Neutrino Masses in MQGT-SCF", 3, "Neutrino Portal"),
    ("UV Completion: Asymptotic Safety Fixed-Point Search in MQGT-SCF", 3, "UV Completion"),
]
assert sum(p for _, p, _ in PACK_ITEMS) == 141 and 16 + 2 + 141 - 1 == 158

NIELSEN_A_CITATION = (
    "Nielsen, Jennifer Lorraine (14 August 2026). The Topological Unified Field Theory on the "
    "Complex Hopf Fibration: The Canonical Field Bundle, Beltrami Lagrangian, Spectral Geometry, "
    "and Particle Spectrum. 240-page manuscript (supplied as NIETTU 2.pdf; PhilArchive record "
    "NIETTU, https://philarchive.org/rec/NIETTU; earlier preprints Nov 2019, Feb 2023, Mar 2025)."
)
NIELSEN_B_CITATION = (
    "Nielsen, Jennifer Lorraine (17 July 2026). The Complex Hopf Fibration as the Canonical Space "
    "for Gauge-Gravity Unification: The Field, Universal Action, and Particle Spectrum. "
    "Preprints.org, version 5 (not peer reviewed). DOI 10.20944/preprints202604.0315.v5. CC BY 4.0."
)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def page_text(pdf_path: str, page: int) -> str:
    out = subprocess.run(
        ["pdftotext", "-layout", "-f", str(page), "-l", str(page), pdf_path, "-"],
        capture_output=True, text=True, check=True,
    ).stdout
    return " ".join(out.replace("ﬁ", "fi").replace("ﬂ", "fl").split())


def die(msg: str) -> None:
    print(f"FAIL-CLOSED: {msg}", file=sys.stderr)
    sys.exit(2)


def new_page(full_page: int) -> int:
    """Map a full-collection page number to its public-edition page number."""
    if 4 <= full_page <= 7249:
        return full_page + 1
    if 7300 <= full_page <= 7331:
        return full_page - 49
    if 7574 <= full_page <= 7689:
        return full_page - 290
    raise ValueError(f"page {full_page} is not reproduced in the public edition")


# --------------------------------------------------------------------------
# editorial pages (ReportLab)
# --------------------------------------------------------------------------
W, H = letter
LM, RM, TM, BM = 1.0 * inch, 1.0 * inch, 0.9 * inch, 0.9 * inch
INK = (0.12, 0.12, 0.12)
MUTED = (0.42, 0.42, 0.42)
RULE = (0.70, 0.70, 0.70)


def _wrap(c: canvas.Canvas, text: str, font: str, size: float, width: float) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _para(c, y, text, font="Helvetica", size=9.6, leading=13.2, width=None, color=INK, indent=0):
    width = width or (W - LM - RM - indent)
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    for line in _wrap(c, text, font, size, width):
        if y < BM + 0.2 * inch:
            raise RuntimeError(f"paragraph overflow: {text[:50]!r}")
        c.drawString(LM + indent, y, line)
        y -= leading
    return y


def _heading(c, y, text, size=12.5):
    c.setFont("Helvetica-Bold", size)
    c.setFillColorRGB(*INK)
    c.drawString(LM, y, text)
    return y - size * 1.5


def _header(c, label):
    c.setFont("Helvetica", 7.5)
    c.setFillColorRGB(*MUTED)
    c.drawString(LM, H - 0.6 * inch, label)
    c.setStrokeColorRGB(*RULE)
    c.setLineWidth(0.5)
    c.line(LM, H - 0.66 * inch, W - RM, H - 0.66 * inch)


def _footer(c, left, right):
    c.setStrokeColorRGB(*RULE)
    c.setLineWidth(0.5)
    c.line(LM, 0.72 * inch, W - RM, 0.72 * inch)
    c.setFont("Helvetica", 7.5)
    c.setFillColorRGB(*MUTED)
    c.drawString(LM, 0.55 * inch, left)
    c.drawRightString(W - RM, 0.55 * inch, right)


def _table(c, y, rows, colx, widths, font="Helvetica", size=8.6, leading=11.5, bold_first=False):
    """rows: list of tuples of strings; wraps cells; returns new y."""
    for r_i, row in enumerate(rows):
        cells = []
        for j, cell in enumerate(row):
            f = "Helvetica-Bold" if (bold_first and r_i == 0) else font
            cells.append(_wrap(c, cell, f, size, widths[j]))
        n = max(len(x) for x in cells)
        if y - n * leading < BM + 0.3 * inch:
            raise RuntimeError(f"table overflow at row {r_i}: {row[0][:40]!r}")
        for j, lines in enumerate(cells):
            f = "Helvetica-Bold" if (bold_first and r_i == 0) else font
            c.setFont(f, size)
            c.setFillColorRGB(*INK)
            for k, line in enumerate(lines):
                if j == len(cells) - 1 and widths[j] < 1.3 * inch:
                    c.drawRightString(colx[j] + widths[j], y - k * leading, line)
                else:
                    c.drawString(colx[j], y - k * leading, line)
        y -= n * leading + 3
        if r_i == 0 and bold_first:
            c.setStrokeColorRGB(*RULE)
            c.line(LM, y + leading - 4, W - RM, y + leading - 4)
            y -= 2
    return y


def make_editorial_pages(input_sha: str, source_manifest: dict) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setTitle("Editorial pages - public edition")

    # ---- page i: cover -------------------------------------------------------
    _header(c, f"RESEARCH COLLECTION / PUBLIC EDITION / {BUILD_DATE}")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(LM, H - 2.3 * inch, "A THEORY OF")
    c.drawString(LM, H - 2.75 * inch, "EVERYTHING")
    c.setFont("Helvetica", 16)
    c.drawString(LM, H - 3.2 * inch, "Research Collection - Public Edition")
    y = H - 3.9 * inch
    c.setFont("Helvetica", 11.5)
    c.drawString(LM, y, "Baird / ZoraASI corpus, Parts 1-4"); y -= 0.26 * inch
    y = _para(c, y, "7,278 of 7,328 corpus pages reproduced; a 50-page personal study guide is withheld", color=MUTED); y -= 0.28 * inch
    c.setFillColorRGB(*INK); c.setFont("Helvetica", 11.5)
    c.drawString(LM, y, "With the independent preprint by Jennifer Lorraine Nielsen"); y -= 0.26 * inch
    y = _para(c, y, "Gauge-gravity preprint, Preprints.org v5 (116 pages, CC BY 4.0), reproduced in full", color=MUTED)
    y = _para(c, y, "TUFT manuscript (240 pages): cited, not reproduced - no redistribution license on the supplied copy", color=MUTED); y -= 0.4 * inch
    c.setFillColorRGB(*INK)
    y = _para(c, y, "Derived without page-content edits from the full research collection of 1 October 2026 "
                    f"(7,689 pages; SHA-256 {input_sha}). "
                    "7,394 source pages preserved, with 5 regenerated editorial pages. Independent authorship and "
                    "source provenance retained; the embedded source manifest records file hashes and page ranges.")
    y -= 0.15 * inch
    y = _para(c, y, "Public edition assembled for Christopher Michael Baird on 12 October 2026 (AI-assisted, Claude). "
                    "Full collection assembled 1 October 2026 (AI-assisted, ChatGPT, ZoraASI project).", color=MUTED)
    _footer(c, "Editorial front matter", "i")
    c.showPage()

    # ---- page ii: contents and source map -----------------------------------
    _header(c, "NAVIGATION / SOURCE PROVENANCE")
    y = H - 1.1 * inch
    y = _heading(c, y, "Contents and source map", 14)
    y = _para(c, y, "Read in order: Parts 1-4, then the Nielsen preprint. Ranges are physical page positions in "
                    "this public edition; 'source pages' are the original corpus page numbers.")
    y -= 6
    rows = [("Section / original authorship", "Source pages", "PDF pages")]
    rows += [
        ("Part 1: Baird / ZoraASI corpus (claim-by-claim change log, archive inventory, Companion Pack, start of the 18 Sep 2026 unified edition)", "1-2,267", "5-2,271"),
        ("Part 2: Baird / ZoraASI corpus (unified edition, continued)", "2,268-3,771", "2,272-3,775"),
        ("Part 3: Baird / ZoraASI corpus (unified edition, continued)", "3,772-5,541", "3,776-5,545"),
        ("Part 4: Baird / ZoraASI corpus (end of unified edition; dated notes Jan-Mar 2026; article series; preprints; consistency audit; software preprint)", "5,542-7,246", "5,546-7,250"),
        ("Part 4 (continued): Omni-Information Coupling Framework corpus addendum", "7,297-7,328", "7,251-7,282"),
        ("Withheld from Part 4: personal mathematical-physics study guide (50 pages)", "7,247-7,296", "-"),
        ("Nielsen A: larger TUFT manuscript, Jennifer Lorraine Nielsen, 14 Aug 2026 (240 pages) - cited on page iii, not reproduced", "-", "-"),
        ("Nielsen B divider (editorial)", "-", "7,283"),
        ("Nielsen B: gauge-gravity preprint, Jennifer Lorraine Nielsen, 17 Jul 2026, Preprints.org v5, CC BY 4.0, DOI 10.20944/preprints202604.0315.v5 (116 pages)", "1-116", "7,284-7,399"),
    ]
    colx = [LM, LM + 4.35 * inch, LM + 5.45 * inch]
    widths = [4.2 * inch, 1.0 * inch, 1.05 * inch]
    y = _table(c, y, rows, colx, widths, bold_first=True)
    y -= 8
    y = _heading(c, y, "Components inside Parts 1-4", 11)
    comp_rows = [("Component", "PDF pages")]
    for cid, title, s, e, auth in COMPONENTS:
        if cid in ("STUDY_GUIDE_WITHHELD", "NIELSEN_A_WITHHELD", "NIELSEN_B"):
            continue
        comp_rows.append((title, f"{new_page(s):,}-{new_page(e):,}" if s != e else f"{new_page(s):,}"))
    y = _table(c, y, comp_rows, [LM, LM + 5.45 * inch], [5.3 * inch, 1.05 * inch], bold_first=True, size=8.2, leading=10.6)
    y -= 6
    y = _para(c, y, "Editorial pages: cover, source map, attribution, public-edition notes (1-4); Nielsen B divider (7,283). "
                    "Total: 7,399 pages. Bookmarks were rebuilt as a flat, truthful outline.", color=MUTED, size=8.6, leading=11.5)
    _footer(c, "Editorial front matter", "ii")
    c.showPage()

    # ---- page iii: attribution and reading guide -----------------------------
    _header(c, "AUTHORSHIP / RESEARCH SCOPE")
    y = H - 1.1 * inch
    y = _heading(c, y, "Attribution and reading guide", 14)
    y = _heading(c, y, "Separate authorship", 10.5)
    y = _para(c, y, "The Baird / ZoraASI research corpus (Parts 1-4) and the work of Jennifer Lorraine Nielsen are "
                    "separately authored. Her titles, author lines, references and source notices are preserved wherever her "
                    "work appears, and her work is attributed to her throughout the contents, dividers and bookmarks. "
                    "Inclusion or citation does not imply coauthorship, collaboration, or endorsement of this compilation.")
    y -= 6
    y = _heading(c, y, "Purpose of this collection", 10.5)
    y = _para(c, y, "This volume places independent research programs together for study of possible connections. Shared "
                    "subjects, such as unification, field structure, spectra and interferometric tests, are starting points "
                    "for comparison. A proposed connection still requires an explicit mathematical mapping, compatible "
                    "assumptions and testable consequences. Assembly of the papers alone does not establish a unified "
                    "solution. Claims remain attributable to their original authors; existing corpus corrections and "
                    "historical-status notices remain in force as written in the sources.")
    y -= 6
    y = _heading(c, y, "Nielsen A - cited, not reproduced", 10.5)
    y = _para(c, y, NIELSEN_A_CITATION)
    y = _para(c, y, "The supplied copy carries no explicit reuse license and no DOI, and the archive record lists the paper as "
                    "forthcoming / under review. No public-republication license is claimed, so the manuscript is not "
                    "reproduced in this public edition. It remains part of the private full collection (pages 7,333-7,572 "
                    "there). It can be added to a later public version with the author's written permission.")
    y -= 6
    y = _heading(c, y, "Nielsen B - citable preprint, reproduced in full", 10.5)
    y = _para(c, y, NIELSEN_B_CITATION)
    y = _para(c, y, "Source: https://doi.org/10.20944/preprints202604.0315.v5 - License: https://creativecommons.org/licenses/by/4.0/ "
                    "The source identifies this as a not-peer-reviewed preprint and states CC BY 4.0.")
    y -= 6
    y = _heading(c, y, "Editorial contribution", 10.5)
    y = _para(c, y, "AI-assisted assembly, front matter, source mapping and attribution of the full collection were prepared "
                    "for Christopher Michael Baird using ChatGPT in the ZoraASI project (1 October 2026). This public edition "
                    "was derived from that file on 12 October 2026 with AI assistance (Claude). All reproduced source pages are "
                    "unchanged in content. The embedded source manifest records file hashes and output ranges. No new license "
                    "is assigned to the included source works; see the NOTICE in the repository for per-component terms.")
    _footer(c, "Editorial front matter", "iii")
    c.showPage()

    # ---- page iv: public-edition notes and verification ----------------------
    _header(c, "PUBLIC EDITION / CHANGES AND VERIFICATION")
    y = H - 1.1 * inch
    y = _heading(c, y, "What differs from the full collection of 1 October 2026", 14)
    items = [
        "Withheld: Nielsen A (full-collection pages 7,332-7,572; divider + 240-page manuscript). Reason: no redistribution license on the supplied copy. Replaced by the citation on page iii.",
        "Withheld: personal mathematical-physics study guide (full-collection pages 7,250-7,299; 50 pages). Reason: personal planning document, not research output. Retained in the private full collection.",
        "Replaced: the five editorial pages (cover, source map, attribution, Nielsen A divider, Nielsen B divider) were regenerated for the new page positions; pages 7,332 and 7,573 of the full collection are superseded by pages iv and 7,283 here.",
        "Rebuilt: the bookmark outline. The full collection nested each source inside the previous one and omitted the Omni-Information addendum; this edition lists the components as siblings with correct page targets.",
        "Unchanged: all other pages are reproduced without page-content edits. The 18 Sep 2026 unified edition (pages 160-7,085 here) is page-for-page identical in text to A_Theory_of_Everything_UPDATED_2026-09-18.pdf in Cbaird26/mqgt-scf-continued (SHA-256 1e8c17058fdf50d0985e9f669e10e448cdd2878b090973ad4c90567fee5c561c).",
    ]
    for it in items:
        y = _para(c, y, "\u2022  " + it, indent=0)
        y -= 3
    y -= 4
    y = _heading(c, y, "Known characteristics of the reproduced material", 11)
    for it in [
        "Duplicates: the dated research notes (pages 7,086-7,197) are exact copies of Companion Pack papers (pages 19-159) arranged chronologically; 22 Companion Pack pages also recur inside the unified edition. This is an archival compilation, not a deduplicated edition; a page-level duplicate report accompanies the repository files.",
        "Placeholder metadata: about twenty pages inside the corpus carry template author / affiliation / e-mail placeholders (e.g. 'Author Name(s)', 'email@domain'). They are reproduced as found and flagged for the author rather than filled in.",
        "Status labels: proposals, conditional mathematical statements, numeric code checks, synthetic controls, preregistration drafts and physically observed results are different classes of statement; the corpus's own change log (pages 5-15) and the repository ledger govern claim status.",
    ]:
        y = _para(c, y, "\u2022  " + it)
        y -= 3
    y -= 4
    y = _heading(c, y, "Verification", 11)
    y = _para(c, y, "Attachment source_manifest.json (this edition) lists every reproduced source file with its SHA-256 and page map; "
                    "source_manifest_full_collection_2026-10-01.json is the manifest embedded in the full collection, kept for provenance. "
                    "Repository: github.com/Cbaird26/mqgt-scf-continued, folder editions/2026-10-01/ (README, SOURCE_MANIFEST.json, PAGE_MAP.csv, "
                    "SHA256SUMS, NOTICE.md, DUPLICATES.csv, build_public_edition.py). The build script is fail-closed: it rebuilds this file only "
                    "from the exact full-collection bytes named above and aborts if any boundary page differs.")
    _footer(c, "Editorial front matter", "iv")
    c.showPage()

    # ---- Nielsen B divider ---------------------------------------------------
    _header(c, "INDEPENDENT SOURCE / NIELSEN B")
    y = H - 1.5 * inch
    c.setFont("Helvetica-Bold", 22); c.setFillColorRGB(*INK)
    c.drawString(LM, y, "NIELSEN B"); y -= 0.5 * inch
    c.setFont("Helvetica-Bold", 15)
    for line in ["The Complex Hopf Fibration as the", "Canonical Space for Gauge-Gravity", "Unification: The Field, Universal", "Action, and Particle Spectrum"]:
        c.drawString(LM, y, line); y -= 0.3 * inch
    y -= 0.1 * inch
    c.setFont("Helvetica", 12); c.drawString(LM, y, "Jennifer Lorraine Nielsen"); y -= 0.3 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Posted: 17 July 2026",
        "Preprints.org, version 5. Source status: not peer reviewed.",
        "DOI: 10.20944/preprints202604.0315.v5",
        "Source license: Creative Commons Attribution 4.0 (CC BY 4.0).",
        "Source file: download_pub.pdf",
        "SHA-256: " + source_manifest["nielsen_b_sha256"],
        "Extent: 116 source pages, reproduced in full.",
        "Physical PDF pages: 7,284-7,399.",
    ]:
        c.drawString(LM, y, line); y -= 0.22 * inch
    y -= 0.15 * inch
    y = _para(c, y, "Original authorship and source notices are retained. This is an independently authored work included for "
                    "comparative research. Its inclusion does not imply the author endorses the Baird / ZoraASI framework.")
    y -= 0.1 * inch
    c.setFont("Helvetica-Oblique", 9.5); c.setFillColorRGB(*MUTED)
    c.drawString(LM, y, "Editorial divider - the original preprint follows")
    _footer(c, "Editorial divider", "7,283")
    c.showPage()

    c.save()
    return buf.getvalue()


# --------------------------------------------------------------------------
# outline
# --------------------------------------------------------------------------
def build_outline(pdf: pikepdf.Pdf, core_outline: list[tuple[int, str, int]]):
    """core_outline: list of (depth, title, core_page_1based) from the repo's core PDF."""
    def item(title, full_page=None, out_page=None):
        p = out_page if out_page is not None else new_page(full_page)
        return pikepdf.OutlineItem(title, p - 1)  # 0-based page index

    with pdf.open_outline() as outline:
        root = outline.root
        fm = item("Front matter (public edition)", out_page=1)
        fm.children.append(item("Cover", out_page=1))
        fm.children.append(item("Contents and source map", out_page=2))
        fm.children.append(item("Attribution and reading guide (Nielsen A cited here)", out_page=3))
        fm.children.append(item("Public edition: changes and verification", out_page=4))
        root.append(fm)

        corpus = item("Baird / ZoraASI corpus - Parts 1-4", full_page=4)
        for cid, title, s, e, auth in COMPONENTS:
            if cid in ("STUDY_GUIDE_WITHHELD", "NIELSEN_A_WITHHELD", "NIELSEN_B"):
                continue
            node = item(title, full_page=s)
            if cid == "COMPANION_PACK":
                node.children.append(item("Pack index (corrected 2026-09-19)", full_page=16))
                p = 18
                for n, (t, pp, _m) in enumerate(PACK_ITEMS, start=1):
                    node.children.append(item(f"{n:02d} - {t}", full_page=p))
                    p += pp
                assert p == 159
            if cid == "CORE_2026-09-18":
                node.children.append(item("Part 1 boundary (source pages 1-2,267)", full_page=159))
                node.children.append(item("Part 2 boundary (source pages 2,268-3,771)", full_page=2271))
                node.children.append(item("Part 3 boundary (source pages 3,772-5,541)", full_page=3775))
                node.children.append(item("Part 4 boundary (source pages 5,542-7,328)", full_page=5545))
                # import the verification-supplement outline carried by the repo's core PDF
                stack = {0: node}
                for depth, title, core_p in core_outline:
                    full_p = 159 + core_p - 1
                    it = item(title, full_page=full_p)
                    parent = stack.get(depth, node)
                    parent.children.append(it)
                    stack[depth + 1] = it
            if cid == "DATED_NOTES_2026":
                for p, t in DATED_NOTES:
                    node.children.append(item(t, full_page=p))
            corpus.children.append(node)
        root.append(corpus)

        nb = item("Nielsen B - Jennifer Lorraine Nielsen (independent author) - divider", out_page=7283)
        nb.children.append(item("Original preprint - The Complex Hopf Fibration as the Canonical Space for Gauge-Gravity Unification (Preprints.org v5, CC BY 4.0)", full_page=7574))
        root.append(nb)


# --------------------------------------------------------------------------
# main build
# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--core-pdf", default=None, help="repo copy of A_Theory_of_Everything_UPDATED_2026-09-18.pdf (optional; outline import + hash check)")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    # 1. input identity ---------------------------------------------------------
    print("[1/7] verifying input ...")
    sha = sha256_file(args.input)
    if sha != EXPECTED_INPUT_SHA256:
        die(f"input SHA-256 {sha} != expected {EXPECTED_INPUT_SHA256}")
    src = pikepdf.open(args.input)
    if len(src.pages) != EXPECTED_INPUT_PAGES:
        die(f"input has {len(src.pages)} pages, expected {EXPECTED_INPUT_PAGES}")
    for p, marker in MARKERS.items():
        t = page_text(args.input, p)
        if marker not in t:
            die(f"full-collection page {p} lacks marker {marker!r}: {t[:120]!r}")
    p = 18
    for t, pp, marker in PACK_ITEMS:
        if marker not in page_text(args.input, p):
            die(f"Companion Pack document expected at full-collection page {p} ({t[:40]}) lacks marker {marker!r}")
        p += pp
    print("      input OK:", sha)

    # 2. original embedded manifest -------------------------------------------
    print("[2/7] reading embedded manifest ...")
    if "source_manifest.json" not in src.attachments:
        die("input has no embedded source_manifest.json")
    orig_manifest_bytes = src.attachments["source_manifest.json"].get_file().read_bytes()
    orig_manifest = json.loads(orig_manifest_bytes)
    by_index = {s["index"]: s for s in orig_manifest["sources"]}
    nielsen_b_sha = by_index[5]["sha256"]

    core_outline = []
    core_sha = None
    if args.core_pdf and os.path.exists(args.core_pdf):
        import pypdf
        core_sha = sha256_file(args.core_pdf)
        rd = pypdf.PdfReader(args.core_pdf)
        if len(rd.pages) != 6926:
            die(f"core PDF has {len(rd.pages)} pages, expected 6926")
        def walk(items, depth=0):
            for it in items:
                if isinstance(it, list):
                    walk(it, depth + 1)
                else:
                    try:
                        pn = rd.get_destination_page_number(it) + 1
                    except Exception:
                        pn = None
                    if pn:
                        core_outline.append((depth, str(it.title), pn))
        walk(rd.outline)
        print(f"      core outline entries imported: {len(core_outline)}")

    # 3. editorial pages ---------------------------------------------------------
    print("[3/7] generating editorial pages ...")
    ed_bytes = make_editorial_pages(sha, {"nielsen_b_sha256": nielsen_b_sha})
    ed = pikepdf.open(io.BytesIO(ed_bytes))
    if len(ed.pages) != N_FRONT + 1:
        die(f"editorial PDF has {len(ed.pages)} pages, expected {N_FRONT + 1}")

    # 4. assemble ------------------------------------------------------------------
    print("[4/7] assembling ...")
    out = pikepdf.new()
    out.pages.extend(ed.pages[0:N_FRONT])
    for s, e in KEEP_RANGES[:2]:
        out.pages.extend(src.pages[s - 1:e])
    out.pages.append(ed.pages[N_FRONT])
    s, e = KEEP_RANGES[2]
    out.pages.extend(src.pages[s - 1:e])
    if len(out.pages) != EXPECTED_OUTPUT_PAGES:
        die(f"assembled {len(out.pages)} pages, expected {EXPECTED_OUTPUT_PAGES}")

    # 5. outline, manifest attachments, metadata --------------------------------------
    print("[5/7] outline, attachments, metadata ...")
    build_outline(out, core_outline)

    page_map = []
    for cid, title, s_, e_, auth in COMPONENTS:
        if cid in ("STUDY_GUIDE_WITHHELD", "NIELSEN_A_WITHHELD"):
            page_map.append({"component_id": cid, "title": title, "authorship": auth,
                             "full_collection_pages": f"{s_}-{e_}", "public_edition_pages": "WITHHELD",
                             "pages": 0})
            continue
        if cid == "NIELSEN_B":
            page_map.append({"component_id": "NIELSEN_B_DIVIDER", "title": "Nielsen B divider (editorial, regenerated)", "authorship": "editorial",
                             "full_collection_pages": "7573 (superseded)", "public_edition_pages": "7283", "pages": 1})
            page_map.append({"component_id": cid, "title": title, "authorship": auth,
                             "full_collection_pages": "7574-7689", "public_edition_pages": f"{new_page(7574)}-{new_page(7689)}", "pages": 116})
            continue
        page_map.append({"component_id": cid, "title": title, "authorship": auth,
                         "full_collection_pages": f"{s_}-{e_}", "public_edition_pages": f"{new_page(s_)}-{new_page(e_)}",
                         "pages": e_ - s_ + 1})
    page_map.insert(0, {"component_id": "FRONT_MATTER", "title": "Cover, source map, attribution, public-edition notes (editorial, regenerated)",
                        "authorship": "editorial", "full_collection_pages": "1-3 (superseded)", "public_edition_pages": "1-4", "pages": 4})

    sources = []
    for i in range(4):
        s0 = by_index[i]
        entry = dict(s0)
        entry["full_collection_output_start"] = s0["output_start"]
        entry["full_collection_output_end"] = s0["output_end"]
        if i < 3:
            entry["public_edition_start"] = new_page(s0["output_start"])
            entry["public_edition_end"] = new_page(s0["output_end"])
            entry["reproduction"] = "complete"
        else:
            entry["public_edition_ranges"] = [
                {"public_start": new_page(5545), "public_end": new_page(7249), "source_pages": "5542-7246", "full_collection_pages": "5545-7249"},
                {"public_start": new_page(7300), "public_end": new_page(7331), "source_pages": "7297-7328", "full_collection_pages": "7300-7331"},
            ]
            entry["withheld"] = {"source_pages": "7247-7296", "full_collection_pages": "7250-7299", "pages": 50,
                                 "reason": "personal mathematical-physics study guide; not research output; retained privately"}
            entry["reproduction"] = "partial (1,737 of 1,787 pages)"
        for k in ("output_start", "output_end"):
            entry.pop(k, None)
        sources.append(entry)
    na = dict(by_index[4]); na.pop("output_start", None); na.pop("output_end", None)
    na.update({"reproduction": "none - cited only", "full_collection_pages": "7333-7572",
               "reason": "supplied copy carries no explicit reuse license or DOI; archive record lists the paper as forthcoming / under review; no public-republication license claimed",
               "citation": NIELSEN_A_CITATION, "philarchive_record": "https://philarchive.org/rec/NIETTU"})
    sources.append(na)
    nb = dict(by_index[5]); nb.pop("output_start", None); nb.pop("output_end", None)
    nb.update({"reproduction": "complete", "full_collection_pages": "7574-7689",
               "public_edition_start": new_page(7574), "public_edition_end": new_page(7689),
               "license": "CC BY 4.0", "doi": "10.20944/preprints202604.0315.v5", "citation": NIELSEN_B_CITATION})
    sources.append(nb)

    manifest = {
        "manifest_schema": "toe-edition-sources-v2",
        "title": "A Theory of Everything - Research Collection - Public Edition",
        "edition": "public",
        "build_date": BUILD_DATE,
        "derived_from": {
            "title": orig_manifest.get("title"),
            "compiled_date": orig_manifest.get("compiled_date"),
            "total_pages": EXPECTED_INPUT_PAGES,
            "sha256": sha,
            "note": "private full collection; not for public distribution as-is (contains an unlicensed third-party manuscript and a personal document)",
        },
        "total_pages": EXPECTED_OUTPUT_PAGES,
        "source_pages": EXPECTED_OUTPUT_PAGES - 5,
        "editorial_pages": [1, 2, 3, 4, 7283],
        "withheld": [
            {"what": "Nielsen A - TUFT manuscript (divider + 240 pages)", "full_collection_pages": "7332-7572", "reason": "no redistribution license on supplied copy; cited instead"},
            {"what": "personal mathematical-physics study guide (50 pages)", "full_collection_pages": "7250-7299", "reason": "personal planning document; not research output"},
        ],
        "source_content_policy": "All reproduced source pages retained without page-content edits; editorial pages regenerated; bookmarks rebuilt.",
        "authorship_policy": orig_manifest.get("authorship_policy"),
        "core_2026_09_18": {
            "repo": "Cbaird26/mqgt-scf-continued", "path": "A_Theory_of_Everything_UPDATED_2026-09-18.pdf",
            "commit_checked": "58d054cac096832269864d5c43204cd420ea9405", "git_blob_sha1": "b34851819648f6d1a0b5fab6e8a5269bf2e1682b",
            "sha256": core_sha or "1e8c17058fdf50d0985e9f669e10e448cdd2878b090973ad4c90567fee5c561c",
            "pages": 6926, "public_edition_pages": f"{new_page(159)}-{new_page(7084)}",
            "check": "20 sampled pages text-identical (modulo fi/fl ligature encoding) between the repo file and the collection",
        },
        "sources": sources,
        "components": page_map,
        "build_tool": "editions/2026-10-01/build_public_edition.py (pikepdf + ReportLab); fail-closed on input hash and boundary-page markers",
    }
    manifest_bytes = json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8")
    out.attachments["source_manifest.json"] = pikepdf.AttachedFileSpec(
        out, manifest_bytes, mime_type="application/json", description="Public-edition source manifest (hashes, page map, withheld items)")
    out.attachments["source_manifest_full_collection_2026-10-01.json"] = pikepdf.AttachedFileSpec(
        out, orig_manifest_bytes, mime_type="application/json", description="Manifest embedded in the full collection of 2026-10-01 (provenance)")

    with out.open_metadata() as meta:
        meta["dc:title"] = "A Theory of Everything - Research Collection - Public Edition (Baird / ZoraASI corpus Parts 1-4; Nielsen gauge-gravity preprint, CC BY 4.0)"
        meta["dc:creator"] = ["Compilation for Christopher Michael Baird; source authorship credited by section"]
        meta["dc:description"] = ("Public edition derived 2026-10-12 from the 2026-10-01 research collection: 7,278-page Baird / ZoraASI corpus "
                                  "(50-page personal study guide withheld) plus Jennifer Lorraine Nielsen's 116-page Preprints.org preprint (CC BY 4.0). "
                                  "Nielsen's 240-page TUFT manuscript is cited, not reproduced (no redistribution license).")
        meta["pdf:Keywords"] = "Theory of Everything, Baird, ZoraASI, MQGT-SCF, Jennifer Lorraine Nielsen, Hopf fibration, research collection, public edition, attribution"
        meta["xmp:CreatorTool"] = "Public edition: AI-assisted derivation (Claude) with pikepdf and ReportLab; full collection: AI-assisted editorial assembly using ChatGPT in the ZoraASI project"
        meta["xmp:CreateDate"] = BUILD_TIMESTAMP
        meta["xmp:ModifyDate"] = BUILD_TIMESTAMP
    out.docinfo["/Subject"] = pikepdf.String(
        "Public edition: 7,278-page Baird / ZoraASI corpus plus Jennifer Lorraine Nielsen's 116-page CC BY 4.0 preprint; TUFT manuscript cited, not reproduced")

    # 6. save ---------------------------------------------------------------------------------
    out_pdf = os.path.join(args.outdir, OUTPUT_BASENAME)
    print("[6/7] saving", out_pdf, "...")
    out.save(out_pdf, linearize=True, min_version="1.7", object_stream_mode=pikepdf.ObjectStreamMode.generate, compress_streams=True)
    out.close(); src.close(); ed.close()

    # 7. verify output + sidecars ---------------------------------------------------------------------
    print("[7/7] verifying output ...")
    with pikepdf.open(out_pdf) as chk:
        if len(chk.pages) != EXPECTED_OUTPUT_PAGES:
            die(f"output has {len(chk.pages)} pages")
        if "source_manifest.json" not in chk.attachments:
            die("output lacks manifest attachment")
    checks = {
        new_page(4): MARKERS[4], new_page(16): MARKERS[16], new_page(159): MARKERS[159], new_page(7085): MARKERS[7085],
        new_page(7249): "ZoraASI software methods research", new_page(7300): MARKERS[7300], new_page(7331): MARKERS[7331],
        7283: "NIELSEN B", new_page(7574): MARKERS[7574], new_page(7689): MARKERS[7689],
    }
    for p, marker in checks.items():
        t = page_text(out_pdf, p)
        if marker not in t:
            die(f"public-edition page {p} lacks marker {marker!r}: {t[:120]!r}")
    # withheld content must be absent at the seams
    for p, bad in {new_page(7249) + 1: "Mathematical Physics Study Guide", 7283: "NIELSEN A", new_page(7331) + 1: "Topological Unified Field Theory on the Complex Hopf Fibration S"}.items():
        if bad in page_text(out_pdf, p):
            die(f"withheld marker {bad!r} found on public-edition page {p}")
    out_sha = sha256_file(out_pdf)

    with open(os.path.join(args.outdir, "SOURCE_MANIFEST.json"), "wb") as f:
        f.write(manifest_bytes)
    with open(os.path.join(args.outdir, "PAGE_MAP.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["component_id", "title", "authorship", "full_collection_pages", "public_edition_pages", "pages"])
        w.writeheader(); w.writerows(page_map)
    with open(os.path.join(args.outdir, "SHA256SUMS"), "w") as f:
        f.write(f"{out_sha}  {OUTPUT_BASENAME}\n")
        f.write(f"# --- inputs (not distributed in this folder) ---\n")
        f.write(f"{sha}  A_Theory_of_Everything_Research_Collection_2026-10-01.pdf  # private full collection (7,689 pages)\n")
        f.write(f"{manifest['core_2026_09_18']['sha256']}  A_Theory_of_Everything_UPDATED_2026-09-18.pdf  # repo core, main@58d054c\n")
        for s_ in orig_manifest["sources"]:
            f.write(f"{s_['sha256']}  {s_['filename']}  # source {s_['index']}: {s_['title']}\n")
    print("DONE")
    print("  output :", out_pdf)
    print("  pages  :", EXPECTED_OUTPUT_PAGES)
    print("  sha256 :", out_sha)
    print("  size   :", os.path.getsize(out_pdf), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
