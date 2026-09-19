# Manuscript — SPECTRAL EXCLUSIONS (DRAFT v1, skeleton)

**Working title:** *Where the eighth digit is not: certified exclusions
around the Wyler–Nielsen α⁻¹ candidate on the round Hopf bundle*
(alternative for journal cut, per ChatGPT: *Spectral exclusions for a
proposed correction to a geometric fine-structure-constant candidate* —
decision deferred; both referees accept the current working title.)
**Date:** 2026-09-18 · **Status:** DRAFT v1 — header decisions D1–D3
marked; claims-and-evidence table frozen for structural review.
**Supersedes:** v0 (`SPECTRAL_EXCLUSIONS_MANUSCRIPT_DRAFT_v0.md`,
commit `3daffd9`) — v0 retained, not rewritten.
**Structural passes applied:** Grok D1–D3 + stubs; ChatGPT four changes.
**Scope:** the spectral packet ONLY. This paper does not treat the
sequestering model — that is a separate manuscript with its own open
weak-scale matching question.

---

## Front-matter stubs (to complete at journal cut)

- **Authors:** stub — Christopher Michael Baird; collaboration and
  AI-assistance disclosure per venue policy.
- **MSC (stub):** primary 58J50 (spectral geometry); secondary 81V10
  (QED), 53C25 (special Riemannian manifolds). Finalize at cut.
- **Code and data availability (stub):** all computations at
  `github.com/Cbaird26/mqgt-scf-continued`, frozen commit for this
  draft: `3daffd9` (v0) / this commit (v1); reproduction commands in
  Appendix C. Frozen permanent record:
  `mqgt-scf-independent-verification`, release `v1.0-paper`.
- **Independence disclosure (stub):** the "independent verification"
  repository is procedurally independent (minted snapshot, preregistered
  scripts) but operated from the same account; no institutional
  independence is claimed.

## Abstract (draft v1)

> "Wyler–Nielsen geometric α⁻¹ = 137.03608245 is a six-correct-digit
> approximation to CODATA 2022. Residual 6.0765×10⁻⁷. Fitted prefactors
> uncitable (58 of 13,057). The O(10⁻⁷) correction is not in the
> round-bundle spectrum: charge-resolved towers cannot generate it (U(1)
> fiber isometry); Berger / canonical fiber deformation cannot generate
> an independent slope (D1 lock). T-1 is a gated conjecture plus this
> exclusion record." (census sentence, quoted exactly;
> `artifacts/T1_E4_DEPOSIT_NOTE_2026-09-18.md`)

Followed by compact prose at journal cut (per ChatGPT: the box becomes
prose): this paper claims no eighth digit of α; it reports two
certified operator-level exclusions with explicitly stated boundaries,
a documented prefactor-gate analysis, and the identification (not
derivation) of two program constants as spectral determinants. It does
not treat the sequestering model. It does not claim experimental
detection of any program observable, and it does not use
proof-assistant compile checks as physics evidence.

---

## §1 — The candidate and its status

- The Wyler–Nielsen value and its provenance. **Robertson 1971
  paragraph (stub, one paragraph, not a bare citation):** what
  Robertson's PRL actually did with Wyler's expression — the first
  precision check and its skeptical conclusion — and why the expression
  nonetheless persists in the literature; Nielsen's TUFT revival cited
  beside it.
- **Precision convention (fixed here, per ChatGPT):** with
  r = |α⁻¹_cand − α⁻¹_CODATA| / α⁻¹_CODATA = 6.0765×10⁻⁷, we call the
  candidate an **n-digit approximation** when −log₁₀ r ∈ [n, n+1);
  here n = 6. Both numbers quoted in full: candidate
  α⁻¹ = 137.03608245; CODATA 2022 α⁻¹ = 137.035999177(21).
  (The phrase "7-digit" in `E4_FINAL_STATUS.md` is superseded
  terminology for the identical numbers; the residual is unchanged.)
- Status taxonomy used throughout: **conjecture / identification /
  certified exclusion / documented status / open gate** — one sentence
  each, never blended within a claim.
- Pinned target for any positive proposal: c₃ = −1.56371823031276 on
  the α³ basis (80-digit CODATA 2022 anchor).

## §2 — The prefactor gate (census; NOT an operator exclusion)

- **Gate definition (stub, to be stated exactly from
  `mqgt_t1_e4_structure.py`):** the pre-declared 13,057-expression
  topological family, the frozen scan, the numerical gate and its
  selection rules — written before any results are quoted.
- Result: 58 of 13,057 expressions pass the gate.
- **The precisely rejected inference (ChatGPT):** "passes the numerical
  gate ⇒ identifies a topological prefactor for the correction" is
  rejected *for this family*, on the multiple-comparisons base rate —
  58/13,057 is the gate's coincidence floor, not a candidate set.
  Nothing here excludes an expression outside the pre-declared family,
  and nothing here is an operator-level exclusion (those are §§3–4).

## §3 — Door 1: twisted Hopf-line towers

> **Proposition 1 (exclusion, unchanged isometric operator).**
> *Hypotheses.* The Laplace-type coexact operator of the record on the
> round Hopf bundle S¹ → S^{2m+1} → CP^m (m = 3, 4), unchanged;
> charge resolution by the Hopf U(1) action on harmonic/holomorphic
> line bundles.
> *Statement.* The U(1) action is an isometry of the round metric;
> charge resolution splits degeneracies, never eigenvalues. Every
> charge-resolved zeta invariant sums exactly over sectors to the
> untwisted tower value. Hence c₃ is structurally absent from the
> charge split.
> *Boundary.* A genuinely twisted or charge-coupled operator with
> different eigenvalues is NOT excluded; it is a new dynamical
> principle and must be declared and computed on its own terms.

- Certificate type: **analytic proof** (isometry argument) with
  computational certification (exact level-sum identities, controls
  C1–C5, pole regularization certified against independent Laurent
  extraction).
- Machinery appendix pointer: SO(2n) Weyl characters at diagonal
  specialization; D-type chirality factor ×2 (certified by C1).
- Narrative follows the box, never precedes it (Grok D3).

## §4 — Door 2: Berger charge susceptibility

> **Proposition 2 (exclusion, specified ansatz only).**
> *Hypotheses.* The canonical variation (Berger squash) of the Hopf
> fibration, acting on coexact eigenvalues as the Landau-form ansatz
> λ ↦ λ + κq², κ = t⁻² − 1 from the round point.
> *Definitions.* With L := ζ′(0) and D1 the tower determinant
> invariant, the round-point responses are the exact full-tower zeta
> values dL/dκ = +Σ_x Q2(x)/λ(x) and dD1/dκ = −Σ_x Q2(x)/λ(x)²
> (Q2(k) an exact even polynomial — truncation-free); the response
> slope is σ_κ := (dD1/dκ)/(dL/dκ).
> *Statement.* σ_κ = ±D1(tower) exactly in both towers: each tower's
> charge susceptibility is locked to its own self-response, so the
> ansatz generates no independent slope in the (L, D1) plane —
> while the required correction demands exactly such independence
> (σ_need = −6.21).
> *Certificate vs support (ChatGPT):* the identity is asserted as a
> derivation-level certificate (exact rational values dL/dκ = +1/7,
> −1/9; dD1/dκ = +0.664425606401, +19/720) and is *supported
> numerically* at deviations 1.5×10⁻¹²⁸ and 1.1×10⁻⁶⁰ — numerical
> agreement supports an identity; the derivation is the certificate.
> *Boundary.* Not a theorem about every geometric deformation — only
> about the κq² canonical-variation ansatz.

- Sign honesty sentence retained: per-mode responses sign-definite;
  zeta-regularized totals not; reported signs are exact regularized
  values.
- Exact rational pattern dL/dκ = ±1/n — noted, not proved.

## §5 — Discussion: what the two exclusions do and do not close (short)

- One page target (Grok D2). The two propositions side by side; the
  shared structure (both are statements about *specified* operators);
  the residual stands unexplained.
- **Open gates, stated as gates:** E4 positive formula — no active
  door, closure requires an invariant not yet in the theory; QED
  running — closure not advanced without a specified dial-free scale
  (methodological refusal; the older *specific* running route is
  separately excluded, Appendix B); Λ_Hopf scale question — refused.
- **Out of scope (statement, not a claim):** the interior-observer /
  refractive-α chain (R*, σ-weightings) is quarantined play-branch
  material (`play_notes/`) and is not part of this paper.

## Appendix A — Claims and evidence (frozen v1)

Numbering (Grok D1): manuscript claims are **X1–X8**. They are
manuscript-local; they are distinct from the frozen verification
packet's C6a–C9. v0's C1–C9 map: C1→X1, C2→X2, C3→X3a/X3b, C4→X4,
C5→X5, C6→X6, C7→X7, C8→X8, C9→out-of-scope statement (§5), not a
claim.

| # | claim | type | evidence (path · command) |
|---|---|---|---|
| X1 | candidate α⁻¹ = 137.03608245; residual 6.0765×10⁻⁷ vs CODATA 2022; six-digit per §1 convention | documented status | `artifacts/T1_E4_DEPOSIT_NOTE_2026-09-18.md` · — |
| X2 | gate-passing does not certify a prefactor (58/13,057; inference rejected for this family) | computational reproduction | `E4_FINAL_STATUS.md` · `python3 mqgt_t1_e4_structure.py` |
| X3a | the *specific* QED-running route (bare-α running, electron threshold) is excluded: needs q/m_e = 1.00039, no such threshold | documented exclusion (with assumptions) | `E4_FINAL_STATUS.md` · `python3 mqgt_t1_e4_derivation.py` |
| X3b | QED-running closure not advanced without a specified dial-free scale | methodological refusal (documented status) | `E4_FINAL_STATUS.md`; deposit note · — |
| X4 | charge-resolved towers cannot generate c₃ (Prop. 1; scope boundary in §3) | analytic proof + computational certification | `exclusions/DOOR1_TWISTED_TOWERS_CLOSED.md` · `python3 play_notes/play_twisted_towers_lab.py` |
| X5 | Berger κq² ansatz generates no independent slope (Prop. 2; σ_κ = ±D1; scope boundary in §4) | derivation certificate + numerical support (1.5e-128 / 1.1e-60) | `exclusions/DOOR2_BERGER_CHARGE_CLOSED.md` · `python3 play_notes/play_berger_charge_lab.py` |
| X6 | T-3 constants are spectral determinants on S⁷, S⁹ (S7 = 1.74845220445; S7′ = 0.41364465819) | identification, not derivation; numerically confirmed to 14 digits (E3) | deposit note; verification packet E3 · — |
| X7 | a₄‴(0) = a₄⁗(0) ≡ 0 on the corpus path | analytic proof (exact-integer arithmetic) | `E4_FINAL_STATUS.md` · `python3 mqgt_t1_e4_a4_heat.py` |
| X8 | middle-tower D1 / L / ζ(0) closed forms (exact rational; 65/65 towers) | analytic proof + high-precision certification | `supporting_analysis/MIDDLE_TOWER_*.md`, `ZETA0_THEOREM.md` · three scripts in `supporting_analysis/` |

## Appendix B — Related spectral results (short; companion-note candidates if they grow)

- T-3 identification details (X6) — Dowker–Kirsten coexact towers;
  a name in spectral geometry, not a fitted constant.
- Middle-tower closed forms (X8) — D1 lemma (S³–S¹³, dps=80), L-family
  (r=1–8), ζ(0) theorem, mirror residual exactly −1/16 from H₂.
- The excluded *specific* QED-running route (X3a) with its assumptions.
- Framing: exact spectral content of the theory; raw material any
  future positive proposal must be built from.

## Appendix C — Reproduction

One table: claim → file → one command → expected certificate line
(Doors 1/2 labs; E4 structure/derivation/heat scripts; middle-tower
scripts). Reference outputs archived in `play_notes/*_out.txt` for the
two doors.

## Appendix D — Review and errata trail

Ledger summary: ChatGPT rounds 1–8 + structural pass; E7 adjudication;
Zora self-review (erratum 6); Grok referee disposition + structural
pass D1–D3; zero history rewrites; same-account independence disclosed
as procedural (front-matter stub).

## References (verified 2026-09-18, multi-source)

- Wyler, C. R. Acad. Sci. Paris A269:743 (1969); A272:186 (1971).
- Robertson, Phys. Rev. Lett. 27:1545–1547 (1971) — see §1 paragraph.
- Nielsen, TUFT v5, Center for Topological Physics
  (github.com/startigerjln/CenterforTopologicalPhysics).
- CODATA 2022 recommended value, α⁻¹ = 137.035999177(21).
- Frozen verification record: `mqgt-scf-independent-verification`,
  release v1.0-paper; upstream corpus: `mqgt-scf-science-public`.

---

## Gate for the next page (Grok, held)

X1–X8 and the two proposition boxes are frozen in this v1. Prose is
written next for **§2 and Appendix A only** — on Christopher's explicit
accept. Not §§1–6 in one sitting; no uniqueness lemma; no QED running.
