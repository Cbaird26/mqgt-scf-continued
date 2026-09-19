# Manuscript skeleton — SPECTRAL EXCLUSIONS (DRAFT v0)

**Working title:** *Where the eighth digit is not: certified exclusions
around the Wyler–Nielsen α⁻¹ candidate on the round Hopf bundle*
**Date:** 2026-09-18 · **Status:** DRAFT v0 — skeleton for referee review
of structure, not yet a paper. Every claim below traces to the record
(`LEDGER.md`) and a one-command reproduction.
**Scope decision (referees, 2026-09-18):** this manuscript covers the
spectral packet ONLY. The sequestering model is a separate paper with
its open weak-scale matching question. Not both.

---

## Abstract (draft)

> The Wyler–Nielsen geometric value α⁻¹ = 137.03608245 is a
> six-correct-digit approximation to CODATA 2022 (relative residual
> 6.0765×10⁻⁷). We do not claim an eighth digit. We report instead a
> certified exclusion record for the O(10⁻⁷) correction: (i) a frozen,
> pre-declared scan of 13,057 topological-expression candidates yields
> 58 gate-passing coincidences — fitted prefactors are uncitable;
> (ii) charge-resolved (twisted) spectral towers on the Hopf bundle
> cannot generate the correction, because the U(1) fiber action is an
> isometry that splits degeneracies without moving eigenvalues;
> (iii) the canonical (Berger) fiber deformation cannot generate an
> independent slope: each tower's charge susceptibility is locked to
> its own spectral determinant, σ_κ = ±D1(tower), certified at
> 1.5×10⁻¹²⁸ and 1.1×10⁻⁶⁰. We also identify the program's two T-3
> constants as coexact spectral determinants on S⁷ and S⁹
> (identification, not derivation), and record exact closed forms for
> the middle-tower invariants as uniqueness raw material. Each negative
> result states precisely what it does not exclude.

> **This paper does not claim:**
> - an eight-digit (or better) derivation of α from geometry
> - first-principles derivation of the T-3 normalizations
> - exclusion of *every* twisted operator or *every* geometric
>   deformation — only the unchanged-isometric operator (Door 1) and
>   the λ ↦ λ + κq² canonical-variation ansatz (Door 2)
> - experimental detection of any program observable
> - proof-assistant compile checks as physics evidence

---

## Section map

### 1. The candidate and its status
- The Wyler–Nielsen value, its provenance (Wyler 1969/71; Robertson
  1971; Nielsen TUFT), and the pinned corpus target
  c₃ = −1.56371823031276 on the α³ basis (80-digit CODATA 2022 anchor).
- Status taxonomy used throughout: **conjecture / identification /
  certified exclusion / open gate**. One sentence each, no blending.
- Census sentence (verbatim, from `artifacts/T1_E4_DEPOSIT_NOTE_2026-09-18.md`).

### 2. The prefactor census (E4 fits)
- 13,057-expression pre-declared topological family, frozen scan;
  58 gate-passing coincidences; why gate-passing ≠ citation.
- Verdict: fitted prefactors uncitable. (Record: `E4_FINAL_STATUS.md`,
  `mqgt_t1_e4_structure.py`.)

### 3. Door 1 — twisted Hopf-line towers (certified exclusion)
- Declared principle (pre-computation): Hopf-line-valued forms;
  charge-resolved coexact spectra for the S⁷-3 and S⁹-2 towers.
- Machinery: SO(2n) Weyl characters at the diagonal specialization;
  D-type chirality subtlety; pole regularization — controls C1–C5.
- Theorem-shaped result: U(1) fiber isometry ⇒ charge resolution splits
  degeneracies, never eigenvalues; every charge-resolved zeta sums
  exactly to the untwisted tower. c₃ structurally absent.
- **Scope boundary (verbatim from the CLOSED card):** does not exclude
  a genuinely twisted or charge-coupled operator with different
  eigenvalues; that would be a new dynamical principle.
- (Record: `exclusions/DOOR1_TWISTED_TOWERS_CLOSED.md`;
  reproduce `python3 play_notes/play_twisted_towers_lab.py`.)

### 4. Door 2 — Berger charge susceptibility (certified exclusion)
- Declared principle: canonical variation as the dial-free deformation;
  Landau-form ansatz λ ↦ λ + κq².
- Truncation-free argument: Q2(k) exact even polynomial; responses are
  exact full-tower zeta values.
- The D1 lock: σ_κ = ±D1(tower) exactly (deviations 1.5×10⁻¹²⁸,
  1.1×10⁻⁶⁰); no independent slope in the (L, D1) plane; σ_need = −6.21
  requires exactly such independence. Exact rational pattern
  dL/dκ = ±1/n (+1/7, −1/9) — noted, not proved.
- **Scope boundary (verbatim):** certificates of the lock for the
  specified ansatz; not a theorem about every geometric deformation.
- (Record: `exclusions/DOOR2_BERGER_CHARGE_CLOSED.md`;
  reproduce `python3 play_notes/play_berger_charge_lab.py`.)

### 5. T-3 identification and middle-tower closed forms (uniqueness raw material)
- S7 = ½ζ′(0) coexact 3-forms on unit S⁷ = 1.74845220445;
  S7′ = −ζ′(0) coexact 2-forms on unit S⁹ = 0.41364465819.
  Dowker–Kirsten towers; a name in spectral geometry, not a fit.
  **Identification, not derivation.**
- Heat-kernel route vacuous: a₄‴(0) = a₄⁗(0) ≡ 0 (exact-integer
  certificate, `mqgt_t1_e4_a4_heat.py`).
- Middle towers: D1 closed form (exact, dps=80, S³–S¹³); L-family
  closed forms (r=1–8); ζ(0) theorem (65/65 coexact towers, scalar
  conventions A/B); mirror residual exactly −1/16 from the H₂
  increment. (Record: `supporting_analysis/MIDDLE_TOWER_*.md`,
  `ZETA0_THEOREM.md`, `E4_MIRROR_CHECK_2026-09-18.md`.)
- Framing: these are the theory's exact spectral content — the raw
  material any future positive proposal must be built from.

### 6. What remains open — gates, not promises
- E4 positive formula: no active door; the exclusion record is the
  current honest shape of close. Any closure must introduce an
  invariant not yet in the theory.
- QED running of the residual: REFUSED without a dial-free Λ_Hopf.
- Scale question: refused until a principle fixes Λ with no free dial.
- The interior-observer chain (R*, σ = −6.21 weightings) is play-branch
  material (`play_notes/`) and is explicitly NOT part of this paper.

### Appendix A — Reproduction
One table: claim → file → one command → expected certificate line.
(Doors 1/2, E4 scripts, middle towers, ζ(0).)

### Appendix B — Review and errata trail
Summary of the ledger: ChatGPT rounds 1–8, E7 adjudication, Zora
self-review, Grok disposition; zero history rewrites; same-account
"independence" disclosed as procedural.

---

## Claims table (claim → status → evidence → ledger)

| # | claim | status | evidence (file · command) | ledger |
|---|---|---|---|---|
| C1 | α⁻¹ = 137.03608245 is six-digit accurate, residual 6.0765×10⁻⁷ | gated conjecture | `artifacts/T1_E4_DEPOSIT_NOTE_2026-09-18.md` | §2 |
| C2 | fitted prefactors uncitable (58 / 13,057) | certified exclusion (fits) | `E4_FINAL_STATUS.md` · `python3 mqgt_t1_e4_structure.py` | §2, §4 |
| C3 | QED running excluded without dial-free Λ | refusal/gate | `E4_FINAL_STATUS.md` | §5 |
| C4 | twisted towers cannot generate c₃ (U(1) isometry) | certified exclusion + scope boundary | `exclusions/DOOR1_*` · `python3 play_notes/play_twisted_towers_lab.py` | §2, §4 |
| C5 | Berger ansatz cannot generate independent slope (D1 lock) | certified exclusion + scope boundary | `exclusions/DOOR2_*` · `python3 play_notes/play_berger_charge_lab.py` | §2, §4 |
| C6 | T-3 constants are spectral determinants on S⁷, S⁹ | identification (not derivation) | deposit note pins | §2 |
| C7 | a₄‴(0) = a₄⁗(0) ≡ 0 on the corpus path | certified (exact integer) | `E4_FINAL_STATUS.md` · `python3 mqgt_t1_e4_a4_heat.py` | §2 |
| C8 | middle-tower D1 / L / ζ(0) closed forms | certified exact | `supporting_analysis/` · three scripts | §2 |
| C9 | σ = −6.21 slope, R*, interior-observer chain | play-branch, open, NOT claimed | `play_notes/` (quarantined) | §3, §5 |

## References (verified 2026-09-18, multi-source)
- Wyler, C. R. Acad. Sci. Paris A269:743 (1969); A272:186 (1971).
- Robertson, Phys. Rev. Lett. 27:1545–1547 (1971).
- Nielsen, TUFT v5, Center for Topological Physics
  (github.com/startigerjln/CenterforTopologicalPhysics).
- CODATA 2022 recommended value of α⁻¹.
- Frozen verification record: `mqgt-scf-independent-verification`,
  release v1.0-paper; upstream corpus: `mqgt-scf-science-public`.

---

## Next actions to full draft (not done here)
1. Christopher reviews this skeleton (section order, claims table).
2. Referee pass on the skeleton (ChatGPT / Grok) before prose.
3. LaTeX cut at journal-cut, per `LEDGER.md` §6 gate.
