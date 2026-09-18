# MQGT-SCF — Continued Development Line

This repository is the **forward development line** of the MQGT-SCF
(Multi-Quantum Geometric Theory / Self-Consistent Field) program, carrying the
corpus forward with the September 2026 independent-verification repairs
**applied**.

It is deliberately separate from the frozen record:

- **Frozen verification record (do not modify):**
  [`Cbaird26/mqgt-scf-independent-verification`](https://github.com/Cbaird26/mqgt-scf-independent-verification),
  release `v1.0-paper` — the paper, errata E1–E13, and verification code,
  minted as a permanent snapshot.
- **Canonical upstream corpus:**
  [`Cbaird26/mqgt-scf-science-public`](https://github.com/Cbaird26/mqgt-scf-science-public).

This repo is where the errata stop being annotations and become the text.

## What's in here

| Path | What it is |
|---|---|
| `ERRATA_STATUS.md` | E1–E13 disposition: which repairs are applied here, which remain open, which belong to the TUFT upstream |
| `neutrino_portal_v2.py` | E2 repair, applied: the neutrino portal with the 3-Yukawa texture (Variant A default, Variant B selectable), both oscillation splittings fit exactly |
| `A_Theory_of_Everything_UPDATED_2026-09-18.pdf` | The 6,926-page unified edition: corpus + verification supplement + verification paper |

## Conventions

- Every repaired claim keeps a pointer to the erratum that motivated the
  change (E-number) and to the verification-repo commit that froze the
  original claim.
- Nothing here rewrites history: the minted verification release remains the
  citable record of what was claimed and when.
- TUFT-side findings (E6, E7, E9, E10) are documented here as **notes for the
  upstream author**, not applied by us — her repo, her call.

License: CC BY 4.0 (matching the verification packet).
