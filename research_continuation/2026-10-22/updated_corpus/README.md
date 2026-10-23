# Updated research corpus — edition 2026.10.22

The reading edition brings the complete 9,252-page prior public corpus together
with nine recent theory notes (90 pages), 42 distinct computational mathematics/status
PDFs (99 pages), and six new editorial/navigation pages: **9,447 pages total**.

- [Zenodo version DOI](https://doi.org/10.5281/zenodo.23585376) · [record](https://zenodo.org/records/23585376)
- [GitHub research prerelease and seven download assets](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.22-updated-corpus)
- [Six-page update guide](02_Update_Guide_and_Catalogue_2026-10-22.pdf)
- [Current claims and supersession](CLAIM_STATUS.md)
- [New-work catalogue](CATALOG_NEW_WORK.csv) and [physical page map](PAGE_MAP.csv)
- [Rights and attribution](RIGHTS_AND_ATTRIBUTION.txt)
- [Asset identities](RELEASE_ASSETS.json), [checksums](RELEASE_SHA256SUMS.txt),
  [assembly verification](VERIFICATION.json), [fresh ZIP verification](ARCHIVE_VERIFICATION.json)

## Zenodo delivery format

The full corpus PDF remains a normal standalone Zenodo download. Because Zenodo
interrupted long archive transfers, the ZIP is deposited as **39 lossless binary
parts**, with four small reconstruction/checksum files. Download all parts and
the [transport helpers](Zenodo_Transport/ZENODO_READ_FIRST.txt) into one directory;
run `python3 REASSEMBLE_ZENODO.py`. The script verifies every part and reconstructs
the exact original ZIP, SHA-256
`f75ba959ed1686e91889916dbc97d1d1c6fcfd7f7e364a3bc3f39085d7127f7d`.
Local reassembly was verified. Use the original single-file ZIP on GitHub for
immediate access. The original seven assets, research contents and hashes remain
unchanged; the Zenodo representation has 49 files: six standalone original assets,
39 archive parts and four helpers. The six-page guide is the Zenodo preview.

The original release tag preserves the initial source snapshot. This additive
metadata update records the transfer adaptation; publication status is determined
by the live Zenodo record. No new scientific calculations are introduced.

## Read the latest result first

**The minimal retained action has negative-residue tachyonic poles and non-real
poles under its stated direct Lorentzian continuation.** Positive restricted static
curvatures and infrared kinetic matrices do not establish a stable vacuum. These
are conditional classical calculations with unresolved compactification, omitted
modes, quantum continuation, and matching. No measured coupling is fitted; the
measured fine-structure constant remains unexplained. This is not a completed or
experimentally validated Theory of Everything.

## Preservation and scope

The full ZIP preserves the prior public ZIP byte for byte; all 26 original assets
from seven research prereleases through `v2026.10.22-finite-momentum-poles`;
two intervening weak/neutral-Higgs PDF notes; available mathematical sidecars;
original caveats; provenance; page maps; and portable rebuild tools.
Standalone code bundles for the two intervening notes were not located.
This covers documented published and local sources, not every cloud-only draft
or repository. Historical revisions and status repetition are labeled and retained.

The root ZIP and corpus PDF are **release assets**, not Git blobs. This directory
is a compact source index and verification/rebuild apparatus. It is not a complete
working copy of the archive: obtain the ZIP before running package-relative scripts.
`SEALED_PACKAGE_SHA256SUMS.txt` describes paths inside the extracted ZIP, while
`RELEASE_SHA256SUMS.txt` describes downloadable assets.

## Reproduce the archive checks and reading PDF

Download the seven assets from either publication location. In that download directory:

```sh
shasum -a 256 -c RELEASE_SHA256SUMS.txt
unzip PUBLIC_Zenodo_Package_2026-10-22.zip -d extracted
cd extracted/ToE_Zenodo_2026-10-22
python3 08_Rebuild/verify_package.py
python3 -m venv /tmp/toe-corpus-rebuild
/tmp/toe-corpus-rebuild/bin/python -m pip install -r 08_Rebuild/requirements.txt
/tmp/toe-corpus-rebuild/bin/python 08_Rebuild/rebuild_corpus.py /tmp/rebuilt-corpus.pdf
```

Use a fresh output path for the rebuild. PDF serialization may differ; the fidelity
contract is decoded page content, geometry and navigation. Original research bundles
retain their separate calculation instructions and dependencies.

All 208 edition payload files passed SHA-256 verification after fresh ZIP extraction.
The preserved previous ZIP verified 758 payload hashes; 26 original release assets
and 444 active release payload hashes were verified. All 9,447 pages match source
decoded streams and geometry, and an isolated package-only rebuild matches all pages.
PDF syntax, 990 bookmarks and 116 referenced historical named destinations passed
checks. Visual review covered all six new guide pages and selected transitions.
Scientific calculations were **not rerun** for packaging. These checks establish
archive integrity and assembly fidelity, not physical validation or external peer review.

## Citation, dates and rights

Version DOI: `10.5281/zenodo.23585376`. Series concept: `10.5281/zenodo.14019809`.
Previous published version: `10.5281/zenodo.23524358`.
The edition is dated 22 October; the publication metadata uses **23 October 2026 UTC**.
The sealed PDFs/ZIP retain historical preparation statements. They are preserved
records, superseded for publication status by the live release and Zenodo record.
No scientific bytes were changed during publication.

CC BY 4.0 applies to the author-controlled compilation; individual component licenses,
authorship and notices remain authoritative. Nielsen's separately authored licensed
116-page preprint is retained; her private 240-page manuscript and personal study
guide remain excluded. Pedalino et al. public data are separately attributed; the
optional EOS ancillary table is not redistributed. Inclusion implies neither common
coauthorship nor endorsement. AI-assisted curation and assembly are disclosed.

All stage-specific limitations remain in [the claim guide](CLAIM_STATUS.md),
`07_Caveats/`, original release notes and full research bundles.
