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

**Census (2026-09-18).** Wyler–Nielsen geometric α⁻¹ = 137.03608245 is a
six-correct-digit approximation to CODATA 2022 (residual 6.0765×10⁻⁷);
the O(10⁻⁷) correction is not in the round-bundle spectrum (two
certified exclusions, `exclusions/`); T-3 constants are identified as
spectral determinants on S⁷ and S⁹, not derived.

> **This record does NOT claim:**
> - an eight-digit (or better) derivation of α from geometry
> - first-principles derivation of the T-3 normalizations (identification only)
> - experimental detection of any MQGT-SCF observable — all experimental
>   work is software-validation / protocol-development stage
> - tested confirmations of the corpus's Φ_c / E-sector observables
> - a natural ultralight scalar coupled to the physical Higgs (the
>   sequestering note's minimal model fails that scale check, erratum 7)
> - the general symmetry-allowed hidden model (the note's §1 is minimal)
> - institutional independence of the frozen verification repo — the
>   independence is procedural (minted snapshot, preregistered scripts),
>   same account
> - Lean-4 compile checks as physics evidence (they are proof-assistant
>   checks of stated theorems, where used)

## What's in here

| Path | What it is |
|---|---|
| `ERRATA_STATUS.md` | E1–E13 disposition: which repairs are applied here, which remain open, which belong to the TUFT upstream |
| `LEDGER.md` | **Cross-repository research ledger**: claim → assumptions → derivation → code → controls → status → provenance, with the full review trail (ChatGPT rounds 1–8, Zora self-review, Grok referee disposition and directives) and open gates/refusals |
| `exclusions/` | Certified negative results: Door 1 (twisted Hopf-line towers — U(1) fiber isometry) and Door 2 (Berger/canonical deformation — D1 susceptibility lock), both CLOSED with lab certificates |
| `artifacts/T1_E4_DEPOSIT_NOTE_2026-09-18.md` | The T-1/E4 census: gated six-digit conjecture, residual 6.0765×10⁻⁷, uncitable prefactors, exclusion record |
| `neutrino_portal_v2.py` | E2 repair, applied: the neutrino portal with the 3-Yukawa texture. **Record claim = Variant A**; Variant B retained in-file as a robustness cross-check, not a menu option (referee requirement, Grok disposition) — both oscillation splittings fit exactly |
| `A_Theory_of_Everything_UPDATED_2026-09-18.pdf` | The 6,926-page unified edition: corpus + verification supplement + verification paper |
| `E4_ALPHA_GATE_RESEARCH_NOTE.md`, `E4_DERIVATION_NOTE.md`, `E4_FINAL_STATUS.md` + `mqgt_t1_e4_*.py` | E4 (T-1 α⁻¹ gate) research record: pinned target c₃ = −1.56371823031276, exclusion record across fits, QED running, existing invariants, heat kernel |
| `supporting_analysis/` | 2026-09-18 record-side theorems: middle-tower D₁ lemma and L closed forms (exact rational), mirror-check residual −1/16 closed, ζ(0) theorem (65/65 coexact towers, scalar conventions A/B), and the Part-0 open-problem-1 closure: one-loop radiative sequestering of J = κ_ES² in an explicit minimal Z₂_h-even model (Lemma 1′: E\|H\|² absent to all loop orders *in that model*; errata 1–7 on record) |
| `play_notes/` | Clearly labeled exploration branch (interior-observer / refractive α idea): pre-declared combination-rule exclusion record across eight principled weightings; kept separate from the record side per program discipline |

## Conventions

- Every repaired claim keeps a pointer to the erratum that motivated the
  change (E-number) and to the verification-repo commit that froze the
  original claim.
- Nothing here rewrites history: the minted verification release remains the
  citable record of what was claimed and when.
- TUFT-side findings (E6, E7, E9, E10) are documented here as **notes for the
  upstream author**, not applied by us — her repo, her call.

License: CC BY 4.0 (matching the verification packet).
