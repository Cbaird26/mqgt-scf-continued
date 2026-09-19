# MQGT-SCF / ToE — 2026-09-19 edition staging (DRAFT)

Owner/editor: Christopher Michael Baird. Assembly/research review: ChatGPT/Zora; local source harvesting and builds: Luna; Grok contributions are separately attributed. This staging branch is not an endorsed physics result, not a final PDF, and not a Zenodo release. Do not merge or tag until Christopher approves the exact built artifacts and privacy/licensing review.

## Canonical sources and unresolved version boundary

1. Preserve Zenodo [record 22738328](https://zenodo.org/records/22738328) as a historical deposit. The supplied Grok addendum reports a 6,916-page September 13 PDF; **verify its API metadata, file SHA and page count rather than relying on that statement**.
2. Use this repo's `A_Theory_of_Everything_UPDATED_2026-09-18.pdf` as the intended next working core **only after its actual bytes have been retrieved and checked**. Source metadata observed through main at `58d054cac096832269864d5c43204cd420ea9405`: Git blob SHA-1 `b34851819648f6d1a0b5fab6e8a5269bf2e1682b`, 38,772,609 bytes; README describes 6,926 pages. Git SHA-1 is not the required published-file SHA-256.
3. Append source papers **in their printed chronological order**, preserving full pages, equations, figures, document titles, and duplicate-version annotations. The uploaded 146-page Grok/companion set is a packet, not the thesis. Its first 3 pages concern personal L2/L3 readout and are not automatically public; original pages 4–5 are a dated packet cover, not an authoritative latest-edition claim.
4. Place September 18 verification and September 19 bridge/errata notes *after* the dated papers they update. Preserve `mqgt-scf-independent-verification` `v1.0-paper` unchanged. The current September 19 source head is `58d054c`; fetch latest before assembling.

## Scientific status labels and correction gates

Keep proposals, conditional mathematical statements, numeric code checks, synthetic controls, preregistration drafts, and physically observed results in different classes. T-1 is a geometric candidate with residual ~6.0765e-7, not a derivation of measured alpha. T-3 values are identified spectral determinants, not first-principles gauge normalizations. The `artifacts/LEMMA6D_COMPUTATION_2026-09-19.md` note reports a bounded negative result for the examined written actions; it does not rule out all future constructions. `GATE1_RECONCILIATION.md` reports software-validation only, with production blocked pending real preregistration. Check the September 18 vs September 19 `c3` anchor differences before syncing active tables; historical sources are immutable.

## Boundaries for public distribution

Do **not** add `All + ToE_Part.1.pdf` through `.9.pdf` to a public repository or Zenodo deposit by default: the private compendium includes third-party textbook material and at least one Wiley EULA page. The Grok interface addendum contains personal birth/chart/relationship content; separate it from the scientific publication and seek Christopher's explicit release approval if any portion is proposed for public distribution. Some companion papers include placeholder author/email fields; flag them for author approval rather than silently inventing metadata. Check licenses of every component, no automatic CC-BY declaration for third-party material.

## Delivery sequence

Luna fetches and hashes the actual September 18 core, the Zenodo file list and the requested separate research sources, then produces a read-only source manifest and duplicate report. Zora checks source order, mathematical and claim-status transitions, rights and privacy, and the draft proof PDF. Christopher approves final section order, source selection and publication target. Only then produce final PDF + checksums + citation/metadata, merge reviewed branch and create a deliberate Zenodo new version. No force-push or rewriting frozen records.

See `SOURCE_MANIFEST_DRAFT.json` and `LUNA_LOCAL_HANDOFF.md` in this folder. Both are preparatory and contain unverified slots to be filled by Luna; no code or physical experiment has been rerun by this staging commit.