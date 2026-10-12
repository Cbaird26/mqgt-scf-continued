# Release checklist — public edition of the 2026-10-01 research collection

Publish gates come from the [2026-09-19 draft source manifest](https://github.com/Cbaird26/mqgt-scf-continued/blob/zora/toe-edition-2026-09-19-draft/editions/2026-09-19/SOURCE_MANIFEST_DRAFT.json) on the separate staging branch.
Status as of the reviewed rebuild on 2026-10-12. This checklist covers public publication; the branch and draft release are review artifacts.

| Gate | Status | Evidence / what remains |
|---|---|---|
| `actual_corpus_bytes_and_sha256` | **met** | Repo core `A_Theory_of_Everything_UPDATED_2026-09-18.pdf`: SHA-256 `1e8c17058fdf50d0985e9f669e10e448cdd2878b090973ad4c90567fee5c561c`, git blob `b34851819648f6d1a0b5fab6e8a5269bf2e1682b`, 6,926 pages, copied directly into the repaired public edition. The received artifact matched the full collection but had core extraction/rendering discrepancies; see `REVIEW.md` for repair and full-source verification. |
| `verified_zenodo_version_comparison` | **open** | The handoff reports that Zenodo 22738328 (v302, 13 Sep 2026) has a newer version. Direct record/API access returned HTTP 403 during this review; current metadata and lineage remain unverified. Fetch the record's version list and confirm which deposit is latest *before* minting, so the public edition becomes a new version of the right concept record and does not fork a parallel lineage. |
| `reviewed_chronological_order` | partly met | Archival order preserved; dated notes carry printed dates with "day not confirmed" labels where the source gives month only. Duplicates documented (`DUPLICATES.csv`) rather than removed. |
| `no_uncleared_third_party_or_personal_material` | **met for the public edition** | Nielsen A withheld (no license); study guide withheld (personal); CV pages already public on `main`; placeholder author fields flagged (not filled). Nielsen B is CC BY 4.0 with attribution. |
| `explicit_author_approval` | **branch/draft staging authorized** | The owner requested review and push of suitable material on 2026-10-12. See `REVIEW.md` for checks. Public release, merge and Zenodo remain separate follow-up steps. |
| `release_pdf_sha256` | **met** | `SHA256SUMS` (first line). Re-compute on the exact file uploaded to the release and to Zenodo; re-saving can change the bytes and hash; renaming a file or adding a `(1)` suffix alone does not. Re-check the actual uploaded bytes. |
| `matching_github_commit_and_zenodo_metadata` | **open** | After merge: tag `v2026.10.01` on the merge commit, publish the draft release, upload the same bytes to Zenodo, then add the Zenodo DOI to `README.md`, `CITATION.cff` and `.zenodo.json` in a follow-up commit. |

## Steps, in order

1. **Review** this branch (`edition/2026-10-01-public`) and the PDF attached to the draft release `v2026.10.01`.
2. **Merge** by normal process (PR → merge). No force-push; `main`'s history and the frozen verification repo are untouched.
3. **Tag + publish release.** `gh release edit v2026.10.01 --draft=false --target main` (or create the tag on the merge commit first; the draft was created against the branch tip so it carries no tag until published). Release assets: the PDF, `SHA256SUMS`, `SOURCE_MANIFEST.json`.
4. **Zenodo new version** of the collection record (not an overwrite of v302): upload the same three files, set license CC BY 4.0 for the deposit *with the NOTICE text in the description* so the Nielsen B attribution and the Nielsen A exclusion are visible on the record. Use the `.zenodo.json` at the repository root as the metadata template.
5. **Back-link the DOI** in `README.md`, `CITATION.cff` (`doi:` and `date-released:`) and `.zenodo.json`.
6. **Optional later versions.** Nielsen A with written permission → rebuild → `v2026.10.01.1`; study guide if the owner decides to publish it; a deduplicated edition if wanted (keep this archival one as the record of what was compiled).

## Commands to stage the draft release (run from a machine with push access)

```sh
# from the repository root, on branch edition/2026-10-01-public
gh release create v2026.10.01 --draft --target edition/2026-10-01-public \
  --title "v2026.10.01 — Research Collection (2026-10-01), public edition" \
  --notes-file editions/2026-10-01/RELEASE_NOTES.md \
  editions/2026-10-01/out/A_Theory_of_Everything_Research_Collection_2026-10-01_public-edition.pdf \
  editions/2026-10-01/SHA256SUMS editions/2026-10-01/SOURCE_MANIFEST.json
```
