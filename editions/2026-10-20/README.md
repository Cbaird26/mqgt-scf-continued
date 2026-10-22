# Expanded research collection — 20 October 2026

The public reading edition combines the reviewed 7,399-page public baseline with 551 supplemental PDFs and four new editorial pages, for **9,252 pages**. The supplement contains 550 byte-distinct existing research PDFs dated 19 September–20 October 2026 and a verbatim rendering of the latest free-bath reference report. The archive supplies the original supplemental PDFs, available Markdown sources, the current report's supporting code/results, catalogue, page maps, checksums and rebuild tools.

The binary files are assets of the draft release tagged `v2026.10.20-research-collection`. Open the repository's [releases page](https://github.com/Cbaird26/mqgt-scf-continued/releases) while signed in to view the draft. This directory records the public release materials; PDFs and ZIPs are not committed into this edition's Git history.

| Asset | Purpose |
|---|---|
| `PUBLIC_Zenodo_Package_2026-10-20.zip` | Complete prepared public upload package, 412,794,731 bytes |
| `01_Combined_Research_Collection_PUBLIC_2026-10-20.pdf` | 9,252-page reading copy with 666 bookmarks |
| `02_Collection_Catalogue.pdf` | Document IDs, titles, original filenames and page ranges |
| `RELEASE_SHA256SUMS.txt` | Checksums for the three binary release assets |

## Verify or rebuild

1. Download the assets and check them with `shasum -a 256 -c RELEASE_SHA256SUMS.txt` from their download directory.
2. Extract the ZIP. Inside its `PUBLIC_ZENODO_UPLOAD` folder, run `python3 06_Rebuild/verify_package.py`. This checks 758 payload files using Python's standard library. The copy of `SHA256SUMS.txt` in this repository describes the extracted package, not this smaller metadata directory.
3. To rebuild the reading copy, install `06_Rebuild/requirements.txt` in a fresh environment and run `python3 06_Rebuild/rebuild_public.py /path/outside/the/package/rebuilt.pdf` from the extracted package. The script uses the included baseline, editorial PDFs and supplement. It preserves page content and rebuilds navigation; PDF serialization and outline hierarchy need not be byte-identical.

`VERIFICATION.json` records successful checks of every copied page's decoded content streams and geometry, PDF syntax, bookmark destinations and the 19 retained named-link targets. The shipped rebuild was run and its 9,252 page signatures matched the public reading copy. Visual review covered the editorial pages, catalogue/report samples and selected transitions, not every historical page. Scientific calculations were not rerun as part of packaging.

## Scope and attribution

The inventory inspected 5,361 local PDF paths. Selection was bounded to the identified baseline and recent research PDFs in the documented research/download folders. Of 743 selected existing source paths, 550 unique PDF byte streams were retained and 193 byte-identical copies were recorded as aliases. Historical repeated papers, near duplicates and distinct revisions remain. This is not a claim that all cloud-only drafts or all repository work are included.

Jennifer Lorraine Nielsen's **independently authored 116-page preprint** remains reproduced with its CC BY 4.0 notice and citation: *The Complex Hopf Fibration as the Canonical Space for Gauge-Gravity Unification: The Field, Universal Action, and Particle Spectrum*, Preprints.org v5, 17 July 2026, DOI [10.20944/preprints202604.0315.v5](https://doi.org/10.20944/preprints202604.0315.v5). Inclusion does not assert joint authorship of the Baird corpus or her endorsement of the compilation.

The owner selected inclusion of only Nielsen's publicly licensed preprint. The 240-page Nielsen manuscript without a stated republication license, the personal study guide, the original private full collection, and the 9,542-page full local review edition are **not release assets and are not committed here**. Catalogue columns describing full-edition page positions are reference metadata only. See `RIGHTS_AND_ATTRIBUTION.txt` and `baseline_review/NOTICE.md` for component-specific rights.

This is an archival research compilation. Existing assumptions, corrections and research-status distinctions remain in force. Packaging does not establish a completed or experimentally validated Theory of Everything.

## Zenodo

`ZENODO_DESCRIPTION.txt` and `ZENODO_METADATA_DRAFT.json` prepare a manual deposit. A JSON file does not populate Zenodo's browser form. Use the actual publication date, preserve source-specific rights, and confirm the intended record lineage before choosing New version. No Zenodo upload, new DOI, or new-version relation is claimed here.

The draft release is staged for owner review. GitHub release publication and Zenodo publication are separate actions.
