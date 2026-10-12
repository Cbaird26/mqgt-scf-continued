# A Theory of Everything — Research Collection (2026-10-01), public edition

**Status: REVIEW.** Branch `edition/2026-10-01-public`. Not merged, not tagged,
release not published, no Zenodo version minted. The owner authorized review,
corrections and a branch push; the PDF is staged as a draft release. See
`REVIEW.md` for the independent artifact checks and remaining publication work.

This folder holds the *metadata* for the public edition of the 1 October 2026
research collection. The PDF itself is **not committed to the tree** (it is
41 MB and every rebuild would add another 41 MB to every clone forever). It is
distributed as a GitHub Release asset on tag `v2026.10.01` and, once approved,
as a new Zenodo version. The hashes here are how anyone checks that the file
they downloaded is the file described here.

| File | Purpose |
|---|---|
| `SOURCE_MANIFEST.json` | Every source file with SHA-256, page counts, page map, withheld items. Also embedded inside the PDF as an attachment (next to the original manifest of the full collection). |
| `PAGE_MAP.csv` | Component → full-collection pages → public-edition pages. |
| `SHA256SUMS` | SHA-256 of the distributed PDF; provenance hashes for the private inputs are comments and also appear in `SOURCE_MANIFEST.json`. |
| `NOTICE.md` | Per-component rights and license terms. The repository's blanket CC BY 4.0 does **not** extend to third-party material. |
| `DUPLICATES.csv` | Page-level exact-duplicate report (324 groups, 363 redundant pages) — the duplicate report the 2026-09-19 staging plan asked for. |
| `build_public_edition.py` | Fail-closed derivation script (pikepdf + ReportLab). Rebuilds from the exact full-collection and repository-core bytes named in the manifest; aborts if any boundary page differs. |
| `verify_public_edition.py`, `VERIFICATION.json`, `RENDER_VERIFICATION.json`, `REVIEW.md` | Independent comparison procedure, recorded results and repair rationale. |
| `RELEASE_CHECKLIST.md` | What remains before merge / release / Zenodo, mapped to the publish gates defined in `editions/2026-09-19/SOURCE_MANIFEST_DRAFT.json`. |

## What the public edition is

`A_Theory_of_Everything_Research_Collection_2026-10-01_public-edition.pdf`
— 7,399 pages, SHA-256 in `SHA256SUMS`, built 2026-10-12.

| PDF pages | Content | Authorship |
|---|---|---|
| 1–4 | Cover, contents/source map, attribution, public-edition notes (editorial, regenerated) | editorial |
| 5–15 | MQGT-SCF / ToE claim-by-claim change log (research snapshot 19 Sep 2026, checked against this repo at `58d054c`) | C. M. Baird / ZoraASI |
| 16 | ToE research corpus: local inventory and release trail (19 Sep 2026) | C. M. Baird / ZoraASI |
| 17–159 | TOE Corpus Companion Pack: index + 34 working papers (corrected 19 Sep 2026) | C. M. Baird / ZoraASI |
| 160–7,085 | **The 18 Sep 2026 unified edition (6,926 pp)** — restored directly from `A_Theory_of_Everything_UPDATED_2026-09-18.pdf` on `main` (SHA-256 `1e8c1705…`, git blob `b348518`) | C. M. Baird / ZoraASI |
| 7,086–7,197 | Dated research notes, 22 Jan – 27 Mar 2026 (chronological copies of Companion Pack papers) | C. M. Baird / ZoraASI |
| 7,198–7,232 | *A Theory of Everything That Thinks and Chooses?* — article series (19 Sep 2026) | C. M. Baird |
| 7,233–7,236 | Synthetic connectivity–memory ablation preprint (ZoraASI Phase 2.3, 21 Sep 2026) | C. M. Baird |
| 7,237–7,242 | Two-singlet effective theory consistency audit, working paper v0.2 (21 Sep 2026) | C. M. Baird |
| 7,243–7,250 | Separating network telemetry from multimodal representation (22 Sep 2026) | C. M. Baird |
| 7,251–7,282 | Omni-Information Coupling Framework — corpus addendum | C. M. Baird |
| 7,283 | Nielsen B divider (editorial, regenerated) | editorial |
| 7,284–7,399 | **Nielsen B** — *The Complex Hopf Fibration as the Canonical Space for Gauge-Gravity Unification*, Preprints.org v5, 17 Jul 2026, DOI 10.20944/preprints202604.0315.v5, **CC BY 4.0** | Jennifer Lorraine Nielsen (independent author) |

The 6,926 core pages are copied directly from the hash-verified repository PDF
to repair rendering damage found in the full collection. The 468 surrounding
source pages are retained without edits. Five editorial pages and the bookmark
outline were regenerated. `REVIEW.md` records the comparison, repair and checks.

## What is withheld, and why

| Withheld | Full-collection pages | Reason | How it can come back |
|---|---|---|---|
| **Nielsen A** — *The Topological Unified Field Theory on the Complex Hopf Fibration*, 240-page manuscript dated 14 Aug 2026 (supplied as `NIETTU 2.pdf`; PhilArchive record [NIETTU](https://philarchive.org/rec/NIETTU)) | 7,332–7,572 | The supplied copy carries no reuse license and no DOI; the archive record lists the paper as forthcoming / under review; the full collection's own attribution page says "confirm its terms before public redistribution". The repository license cannot grant redistribution rights to her manuscript; permission has not been established. It is **cited** on page iii instead. | Written permission from the author → rebuild with the range re-enabled → new version (v2026.10.01.1 or later) and a new Zenodo version. |
| Personal mathematical-physics study guide (50 pp, 26 Sep 2026) | 7,250–7,299 | Personal planning document, not research output; the 2026-09-19 staging rules require explicit release approval for personal material. | Owner's decision; update the selected ranges, mappings, page counts, editorial text and verification together. |

Not withheld, but noted: the unified edition opens with the author's CV
(public-edition pages 160–161). It is already public on `main` as pages 1–2
of the 18 Sep PDF, so this edition changes nothing there; removing it would
be a two-page edit to the core, which this edition deliberately does not touch.

## Known characteristics of the reproduced material

* **Duplicates.** The dated notes (pp. 7,086–7,197) are exact copies of 112
  Companion Pack pages, re-ordered chronologically; 22 Companion Pack pages also
  recur inside the unified edition. 363 redundant pages overall (4.9 % of the
  public edition). This is an *archival compilation*, not a deduplicated
  edition. `DUPLICATES.csv` lists every group.
* **Placeholder metadata.** About twenty pages inside the corpus carry template
  author/affiliation/e-mail placeholders (`Author Name(s)`, `email@domain`;
  e.g. p. 7,086). Reproduced as found and flagged for the author, per the
  staging rule "flag them for author approval rather than silently inventing
  metadata".
* **Claim status.** The corpus's own change log (pp. 5–15), `LEDGER.md` and
  `ERRATA_STATUS.md` govern what is a proposal, a conditional statement, a
  numeric check, a synthetic control or an observed result. A larger page
  count is not verification.
* **Companion Pack index titles.** The pack index (p. 17) labels its first two
  files `00_SOLVED_TOE_root` / `01_SOLVED_TOE_2026`; the documents at those
  positions are the fifth-force falsification note and the teleology
  manuscript. Bookmarks use the documents' printed titles.

## Verify a downloaded copy

```sh
shasum -a 256 -c SHA256SUMS                 # run beside the downloaded PDF
pdfinfo A_Theory_of_Everything_Research_Collection_2026-10-01_public-edition.pdf | grep Pages   # 7399
qpdf --list-attachments A_Theory_of_Everything_Research_Collection_2026-10-01_public-edition.pdf
#   source_manifest.json                              (this edition)
#   source_manifest_full_collection_2026-10-01.json   (provenance: manifest of the private full collection)
```

## Rebuild (requires the private full collection)

```sh
# Requires Python packages pikepdf>=10.17, pypdf and reportlab, plus Poppler pdftotext.
# Run from editions/2026-10-01; --input names the private full collection.
python3 build_public_edition.py \
  --input /path/to/A_Theory_of_Everything_Research_Collection_2026-10-01.pdf \
  --outdir out \
  --core-pdf ../../A_Theory_of_Everything_UPDATED_2026-09-18.pdf
```

The script verifies both input hashes and 22 full-collection boundary markers,
restores the repository core, assembles the surrounding ranges, regenerates five editorial
pages, rebuilds the outline, embeds both manifests, sets metadata, then
re-verifies the output (page count, seam markers, absence of withheld content)
and writes `SOURCE_MANIFEST.json`, `PAGE_MAP.csv` and `SHA256SUMS`. PDF metadata carries the build timestamp, so a rebuild is byte-different.
Use the recorded checksum for the staged artifact and compare rebuilt page text
with `pdftotext`; never replace a release asset without updating its checksum.

## Relationship to the rest of the repository

* `main` keeps the 18 Sep 2026 unified edition in-tree; this edition contains
  it unchanged and adds the September working papers, the dated notes and the
  Nielsen preprint around it.
* [The 2026-09-19 staging plan](https://github.com/Cbaird26/mqgt-scf-continued/tree/zora/toe-edition-2026-09-19-draft/editions/2026-09-19) (chronology-first ToE edition) lives on a separate branch
  and describes the plan this edition partly realizes. Its publish gates are tracked in
  `RELEASE_CHECKLIST.md`.
* `Cbaird26/mqgt-scf-independent-verification` `v1.0-paper` is frozen and
  untouched. Zenodo record 22738328 (v302, 13 Sep 2026) is a historical
  deposit and is not overwritten; a *new version* is minted after approval.
