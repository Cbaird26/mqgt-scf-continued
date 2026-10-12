# Artifact review and repair — 12 October 2026

The reviewed edition is suitable for a GitHub review branch and draft release.
It contains 7,399 pages (41,013,847 bytes). The PDF is a release asset; only
metadata, build/verification scripts and reports belong in the repository.
Public release and a Zenodo deposit remain follow-up steps.

## Repair made during review

The received PDF had SHA-256
`3427baabf8585f8948b69d4990fdb6295f63618b44c6616c4f38f523feef2ce3`.
Its 7,394 retained pages matched the supplied full collection in normalized
text, but the claim that its core was fully identical to the repository PDF
was too strong. All 6,926 core pages were compared: 80 differed in extracted
text after whitespace and fi/fl normalization. Rendering those 80 pages at a
maximum dimension of 1,200 pixels found nine pixel differences; visual review
showed text collisions, notably on core pages 6,384 and 6,924.
The nine affected core page numbers were 6,384, 6,386, 6,391, 6,918, 6,919,
6,921, 6,922, 6,923 and 6,924. These differences were inherited from the supplied
collection, rather than introduced by Claude's selection of public pages.
`RECEIVED_ARTIFACT_REVIEW.json` records that comparison.

The repaired build copies the complete canonical core directly from
`A_Theory_of_Everything_UPDATED_2026-09-18.pdf` at `main@58d054c`, requiring
SHA-256 `1e8c17058fdf50d0985e9f669e10e448cdd2878b090973ad4c90567fee5c561c`.
It preserves the core's linked named destinations, retains 468 surrounding
source pages, and regenerates the five editorial pages. The page count and
component boundaries are unchanged. Both embedded and external manifests
explicitly identify the restored core.

**Reviewed artifact SHA-256:**
`ac0d62ae361a796bea3bbab3062112a4c872c2aec71bf4aeacfb72741398bb7c`.

## Verification

- All 6,926 core pages match the repository source in normalized extracted
  text and decoded page-content streams: zero mismatches.
- All 468 surrounding source pages match the supplied full collection in
  normalized text and decoded page-content streams: zero mismatches.
- All 80 previously flagged core pages now render pixel-for-pixel identically
  to the repository source at the tested resolution. This raster comparison
  is limited to those 80 pages; it is not an all-page visual certification.
- Both embedded manifests match their intended source bytes; all 107 bookmark
  destinations are valid; all 19 named destinations referenced by core links
  retain their correct page targets.
- All 324 listed duplicate groups still match (363 redundant pages retained
  as archival copies).
- `qpdf --check` reports no syntax or stream-encoding errors. The standalone
  `shasum -a 256 -c SHA256SUMS` check passes. `CITATION.cff` validates against
  CFF 1.2.0. The builder rejects missing or altered core inputs.
- Rendered editorial pages and repaired samples were visually inspected for
  layout and legibility. Verification results are in `VERIFICATION.json`
  and `RENDER_VERIFICATION.json`.

This review concerns source fidelity, provenance, navigation and packaging.
Scientific claims retain the statuses in the repository ledger and errata;
this review does not establish their empirical or theoretical validity.

## Publication and metadata decisions

Nielsen's 240-page manuscript and the 50-page personal study guide remain
withheld. The included 116-page preprint's first page explicitly identifies
CC BY 4.0, with attribution retained. The already-public CV remains in the
canonical core. No new permission is inferred for other third-party material.

The checksum file now has one active entry for the distributed PDF; private
input hashes are comments and remain in the manifest. This avoids treating
inline provenance comments as parts of filenames. The rebuild command,
separate-branch links and wording about licensing and filename changes were
corrected. The Zenodo template credits Nielsen as the author of an included
work through its description and relation, without presenting her as a
contributor to this compilation. An unverified `isNewVersionOf` relation was
replaced with a provenance relation.

Zenodo's record and API returned HTTP 403 during this review. Its latest
version and concept lineage remain unverified; no Zenodo write was attempted.
The metadata template must be checked before an eventual deposit. The owner
has authorized review and pushing suitable work; the chosen delivery is the
review branch and a draft GitHub release. Main, the frozen verification
repository and existing releases are outside this change.

## Reproduce the source checks

From this edition directory, with Python packages `pikepdf>=10.17`, `pypdf`,
`reportlab`, and Poppler available:

```sh
python3 verify_public_edition.py \
  --pdf /path/to/A_Theory_of_Everything_Research_Collection_2026-10-01_public-edition.pdf \
  --input /path/to/A_Theory_of_Everything_Research_Collection_2026-10-01.pdf \
  --core-pdf ../../A_Theory_of_Everything_UPDATED_2026-09-18.pdf \
  --report /tmp/toe-public-edition-verification.json
```

The private input is needed only for local provenance checks; it is not a
release asset. For the raster check, render each core page listed in
`RENDER_VERIFICATION.json` and the output page 159 positions later using
`pdftoppm -f PAGE -l PAGE -singlefile -scale-to 1200 -png FILE`. Compare the
RGB pixels; all recorded pairs were identical after repair.
