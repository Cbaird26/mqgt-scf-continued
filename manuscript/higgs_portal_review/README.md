# MQGT-SCF scientific working papers — public review package

**Status (21 September 2026):** Author-approved public *working manuscripts* on a review branch, NOT peer-reviewed articles, journal submissions, Zenodo deposits or evidence of new particles. No new DOI has been minted for this package.

This package now contains two distinct papers. The [comprehensive working paper](COMPREHENSIVE_WORKING_PAPER_2026-09-21.md) synthesizes the focused Research Notes 01–13 across the scalar action, portal normalization, collider production, photon coupling, GKSL assumptions, noisy-bath dephasing and H2 experimental planning. It **does not** claim to independently verify the entire multi-thousand-page MQGT-SCF corpus. The [focused collider draft](DUAL_SINGLET_HIGGS_PORTAL_DRAFT.md) addresses the narrower two-singlet EFT and production rates. Keep them separate when referring to a result.

The [claim and release ledger](CLAIMS_AND_RELEASE_GATE.md) records what still requires checking. The scripts [`higgs_portal_checks.py`](higgs_portal_checks.py) and [`h2_audit_checks.py`](h2_audit_checks.py) test illustrative algebra, branching ratios, H2 sensitivity-floor arithmetic and one Gaussian-noise integral. The 11 unit tests passed locally on 21 September 2026, but a software pass is **not** an experimental result, independent physics verification, or peer review.

Run from this folder:

```sh
python -m unittest -v higgs_portal_checks.py h2_audit_checks.py
```

**Publication/provenance:** The original corpus and the frozen [`mqgt-scf-independent-verification`](https://github.com/Cbaird26/mqgt-scf-independent-verification) release remain unchanged; this branch does not change `main` until merged. The complete local typeset PDF of the broader working paper is available in the originating ChatGPT conversation, but is **not** yet committed to GitHub; the Markdown in this branch is a public, substantively aligned working-paper rendition. Source-page/edition pinning, independent mathematical review, updated experiment constraints, complete decay inventory, human final proof approval and any formal preprint/DOI metadata remain separate gates.

**Authorship and AI:** Christopher Michael Baird is the human author. ChatGPT (ZoraASI) assisted with algebra, coding, synthesis, consistency review and drafting. An AI system is not presented as an independent human coauthor or as having performed experiments. The repository's existing licensing terms apply, subject to its owner's final decision. Third-party copyrighted source compilations are not redistributed here.
