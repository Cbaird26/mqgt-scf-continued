# Manuscript — SPECTRAL EXCLUSIONS (DRAFT v1.5, skeleton + §2/Appendix A prose)

**Working title:** *Where the eighth digit is not: certified exclusions
around the Wyler–Nielsen α⁻¹ candidate on the round Hopf bundle*
(alternative for journal cut, per ChatGPT: *Spectral exclusions for a
proposed correction to a geometric fine-structure-constant candidate* —
decision deferred; both referees accept the current working title.)
**Date:** 2026-09-18 · **Status:** DRAFT v1.5 (per-version log below) — Grok's accept edit
applied to Prop. 2; ChatGPT round-9 reconciliation applied (unified
L/D1 definitions; lock relabeled; σ_need removed from the proposition);
§2 and Appendix A prose written per Grok's accept ("those two units,
then stop"). All other sections remain skeleton.
**v1.1 changes:** (i) Prop. 2 box: L := −ζ′(0) and D1 := (dL/dη)|₀ now
defined from the same generating function and differentiated explicitly
(ChatGPT 1); the lock σ_κ = ±D1 relabeled a high-precision
computational observation, algebraic proof pending (ChatGPT 2);
σ_need = −6.21 removed from the proposition — that number is the
quarantined play chain (Grok + ChatGPT 3); (ii) CODATA value corrected
to the record's 137.035999178(21); (iii) X-table count noted (eight
groups, nine rows); (iv) §2 + Appendix A prose.
**v1.2 changes (round 10, ChatGPT + Grok micro-edits):** (i) CODATA
re-pinned to NIST 137.035999177(21) — the record's …178 tail was
internal rounding; §1 anchor footnote carries both 80-digit comparisons
and the re-anchored pins c₃ = −1.56373700913218, c₄ =
−214.288263496482; record-side re-anchor queued in `LEDGER.md` §5;
(ii) Prop. 2 convention translation printed: the lab's D1_t = ∂_u ζ′(0)
= −D1, so the card's σ_κ = ±D1_t reads σ_κ = ∓D1 here, with per-tower
signs and unchanged magnitudes/ratios; (iii) §2 illustration residuals
recomputed at the 177 anchor (−1500/7: 7.2×10⁻¹², ≈1.4×10³-fold below
the gate; F3: 2.7×10⁻⁹) — replacing the v1.1 "seven hundred-fold" slip
AND its intermediate wrong fix; (iv) §2 constants marked as
identifications (X6 sense), not derived outputs; (v) X2 evidence now
names the exact frozen scan `mqgt_t1_topological_scan.py`
(verification packet v1.0-paper) and states that the continued-line
script does not rerun it.
**v1.3 changes (round 11, ChatGPT T-1 math pass + Grok confirmation):**
(i) §1 carries the exact simplified form α⁻¹_T1 = (8/9)·1920^{1/4}·π^{11/4}
(verified: difference 0.0 at 80 digits) and the Robertson–Gilmore
paragraph stub (radius objection + r = 1 reply, both cited); (ii) §1
anchor footnote adds the experimental framing — ±3.9×10⁻⁴ propagated
uncertainty on c₃, ≈3,965σ gap, no fifteen-digit experimental target;
(iii) Appendix B gains the scaling constraint: S7′ − 2S7 is invariant
under common radius rescaling (theorem on the stated towers, verified
against the ζ(0) theorem); (iv) X7's certificate carries the ChatGPT
round-11 correction — the heat script computed the full Λ^p bundle,
labeled coexact; corrected coexact coefficients verified exactly and
applied to `mqgt_t1_e4_a4_heat.py` + `E4_FINAL_STATUS.md`; the vacuity
verdict is unchanged; Gilmore 1972 added to references.
**v1.4 changes (round 12, ChatGPT two notes; Christopher's
consciousness/Φ_c question routed to play, not this paper):** (i) §5
open gates gain the **EM-normalization bridge** (ChatGPT round 12b;
algebra verified here): the Hopf c₁ fixes the flux integer, not the
1/g² coefficient — Kaluza–Klein illustration on S⁹_R,
1/g₄² = Vol(S⁹_R)/g₁₃² with Vol = π⁵R⁹/12, so α₄ = 3g₁₃²/(π⁶R⁹);
(ii) Appendix B's scaling bullet cross-references the integrated
coexact heat coefficients (ChatGPT round 12a; verified exact:
A₄ᶜᵉ³(S⁷_R) = (49√π/72)R³ and A₄ᶜᵉ²(S⁹_R) = −(7√π/640)R⁵ — both
dimensionful, R^{n−4}, the same radius gate); (iii) record discipline
unchanged: no Φ_c/consciousness content in this manuscript.
**v1.5 changes (round 13, ChatGPT refinements; verified here):** (i)
Appendix B's heat cross-ref gains the ratio caveat — individual heat
coefficients are dimensionful, but scale-independent *ratios* exist
(A_{2k} ~ R^{n−2k}; e.g. A₄⁵/A₂³ on S⁷, A₄⁷/A₂⁵ on S⁹), which would
still need an independently justified connection to the electromagnetic
action, so the normalization concern stands; (ii) heat-script
presentation cleanup recorded — round-2 full-form labels withdrawn at
the source and the correction block retitled as the primary coexact
certificate (rerun clean); (iii) play-side only: Z(Φ_c)F² is *a*
coupling, not the only gauge-invariant one (φF F̃ is the parity-odd
alternative) — noted for the quarantined branch, no manuscript content
changed on that front.
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

- The Wyler–Nielsen value and its provenance. Exact simplified form
  (ChatGPT, round 11; verified here at 80 digits, difference 0.0):
  α⁻¹_T1 = (9/(8π⁴))·(π⁵/1920)^{1/4} = **(8/9)·1920^{1/4}·π^{11/4}**
  = 137.03608244816433744….
  **Robertson–Gilmore paragraph (stub, one paragraph):** Robertson's
  PRL 27:1545–1547 (1971) made the radius objection — Wyler's
  expression "agrees with experiment only if the radius of these
  spaces is arbitrarily chosen to equal 1… no known reason for setting
  the radius equal to one"; Gilmore's PRL 28:462–464 (1972) supplied
  the group-theoretic reason for r = 1. The paragraph must state both,
  and connect them to this paper's spectral form of the same question
  (Appendix B, scaling constraint): for determinant-built corrections
  the radius objection reappears as the ζ′(0) scaling law.
- **Precision convention (fixed here, per ChatGPT):** with
  r = |α⁻¹_cand − α⁻¹_CODATA| / α⁻¹_CODATA = 6.0765×10⁻⁷, we call the
  candidate an **n-digit approximation** when −log₁₀ r ∈ [n, n+1);
  here n = 6. Both numbers quoted in full: candidate
  α⁻¹ = 137.03608245; CODATA 2022 α⁻¹ = 137.035999177(21) (NIST).
  (The phrase "7-digit" in `E4_FINAL_STATUS.md` is superseded
  terminology for the identical numbers; the residual is unchanged.)
- **CODATA anchor footnote (Grok round 10):** the continued-line record
  scripts anchor on 137.035999178 — an internal rounding of the NIST
  value. This paper pins 137.035999177(21). The 80-digit comparisons:
  residual 6.0765175×10⁻⁷ (…178 anchor) vs 6.0765904×10⁻⁷ (…177
  anchor) — both round to the working residual 6.0765×10⁻⁷. The pinned
  coefficients re-anchor as c₃ = −1.56373700913218, c₄ =
  −214.288263496482 (…177) vs the record's c₃ = −1.56371823031276,
  c₄ = −214.285690123763 (…178). A record-side re-anchor is queued in
  `LEDGER.md` §5 as an erratum candidate; the frozen scan's conclusion
  is anchor-insensitive at its gate width. Experimental framing
  (ChatGPT round 11): CODATA's (21) propagates to ±3.9×10⁻⁴ on c₃ —
  so neither anchor's c₃ is a fifteen-digit experimentally fixed
  target; the pin is a theory target relative to the central value,
  and the candidate's gap is ≈3,965 CODATA standard uncertainties.
- Status taxonomy used throughout: **conjecture / identification /
  certified exclusion / documented status / open gate** — one sentence
  each, never blended within a claim.
- Pinned target for any positive proposal: c₃ = −1.56373700913218 on
  the α³ basis (80-digit, NIST 137.035999177 anchor; the record's
  …178-anchored pin is footnoted above).

## §2 — The prefactor gate (census; NOT an operator exclusion)

The T-1 candidate α⁻¹ = 137.03608244816433744 fails the program's own
admissibility gate — agreement with CODATA 2022 to relative 1×10⁻⁸ —
by a relative margin of 6.07652×10⁻⁷. Before asking whether any
*structural* correction could close that gap, the program asked a prior
question: how often do mere coincidences close it? The instrument is a
frozen, pre-declared family — coefficients c = Aπ^j/B with
j ∈ {−2, −1, 0, 1, 2} and A, B ∈ 1…64: 20,480 expressions, 13,057
distinct values — scanned once against the gate
(`mqgt_t1_topological_scan.py`, verification packet v1.0-paper), with
the family and the gate fixed before any result was quoted. No further
candidate search is performed in the continued line
(`mqgt_t1_e4_structure.py` pins targets and tests hypotheses; it does
not search).

Fifty-eight of the 13,057 expressions pass the gate. Two illustrate
what a gate-passer is (both recomputed at this paper's NIST anchor;
the record's …178-anchored figures differ slightly, see §1 footnote).
The coefficient c₄ = −214.288263496482 lies within 1.2×10⁻⁵ (relative)
of −1500/7, so the correction (1 − (1500/7)α⁴) passes the gate with
residual 7.2×10⁻¹² — ≈1.4×10³-fold below the gate — and −1500/7 has
no derivation from the program's operator content. Conversely, the
known F3 coincidence (1 − (π/2)α³) passes the gate at residual
2.7×10⁻⁹, yet −π/2 = −1.5707963 differs from the needed
c₃ = −1.56373700913218 by 4.5×10⁻³ relative — excluded outright as an
identity, before any multiplicity argument. Gate-passing is necessary,
not sufficient.

The inference rejected here is stated precisely: from "expression X
passes the numerical gate" one cannot infer "X identifies a topological
prefactor of the correction." For this family, 58/13,057 is the
coincidence floor set jointly by the gate width and the family size;
every gate-passer remains coincidence-class until its coefficient is
produced from operator content with every factor identifiable before
comparison to CODATA. This is a documented multiplicity ceiling on
fitting within one pre-declared family. It excludes nothing outside
that family, and it is not an operator-level exclusion — those are
Propositions 1 and 2.

The resolution standard is therefore quantified: a closing derivation
must produce c₃ = −1.56373700913218 on the α³ basis (equivalently
c₄ = −214.288263496482 on α⁴; NIST anchor, §1 footnote) from a trace
anomaly, heat-kernel coefficient, or index density of the operator
content already in the theory — the content underlying the program's
identified constants ζ(3)·13/(24π) = 0.20725607285,
ζ(5)/(4π²) = 0.0262656868757, S7/56 = 0.0312223607937, and
S7′/16 = 0.0258527911369 (identifications in the sense of X6, not
derived operator outputs; `E4_ALPHA_GATE_RESEARCH_NOTE.md`). Any
combination found by fitting remains coincidence-class per the frozen
scan, regardless of how far inside the gate it falls.

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
> *Definitions (unified, ChatGPT round 9).* Both invariants are derived
> from the same generating function, the log-determinant
> L := −ζ′(0): the determinant invariant is D1 := (dL/dη)|₀, with η
> the uniform endomorphism shift (the corpus's E-shift). Under the
> ansatz, differentiating L explicitly gives the round-point responses
> as exact full-tower zeta values:
> dL/dκ = +Σ_x Q2(x)/λ(x) and dD1/dκ = −Σ_x Q2(x)/λ(x)²
> (Q2(k) an exact even polynomial — truncation-free); the response
> slope is σ_κ := (dD1/dκ)/(dL/dκ).
> *Statement.* The ansatz generates no independent slope in the
> (L, D1) plane: in both towers the slope is locked to the tower's own
> determinant response. In this paper's convention (D1 := ∂_η L|₀,
> L := −ζ′(0)) the lock reads σ_κ = −D1 (S⁷ ce3) and σ_κ = +D1
> (S⁹ ce2), with D1(S⁷ ce3) = −4.650979245 and D1(S⁹ ce2) = −0.2375.
> *Certificate vs support (ChatGPT, rounds 8–9).* The responses
> themselves are derivation-level exact (dL/dκ = +1/7 and −1/9;
> dD1/dκ = +0.664425606401 and +19/720 — exact rational). The *lock
> identity* σ_κ = ±D1 is a **high-precision computational observation**
> (deviations 1.5×10⁻¹²⁸ and 1.1×10⁻⁶⁰), algebraic proof pending; it is
> labeled as such, not asserted as a derived identity.
> *Convention translation (ChatGPT round 10, verified against the lab).*
> The Door 2 lab's comparison value is D1_t := ∂_u ζ′(0)|₀ = −D1, so
> the card prints the same lock as σ_κ = ±D1_t (S⁷: +, S⁹: −). The two
> conventions carry identical magnitudes and slope ratios
> (|σ_κ| = 4.650979245 and 0.2375; deviations 1.5×10⁻¹²⁸ and
> 1.1×10⁻⁶⁰); only the signed ± labels interchange. The lab's printed
> κ-responses (dL/dκ = +ΣQ2/λ, dD1/dκ = −ΣQ2/λ²) already use this
> paper's log-determinant convention; no lab numbers change.
> *Boundary.* Not a theorem about every geometric deformation — only
> about the κq² canonical-variation ansatz. No external slope target
> appears in this proposition: the play-branch comparison value
> σ_need = −6.21 belongs to the quarantined interior-observer chain
> (`play_notes/`) and is not a premise, target, or conclusion here.

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
- **EM-normalization bridge (ChatGPT round 12b; algebra verified
  here):** the Hopf c₁ fixes the flux integer (Dirac quantization),
  not the 1/g² coefficient of F². Kaluza–Klein illustration on S⁹_R:
  1/g₄² = Vol(S⁹_R)/g₁₃² with Vol = π⁵R⁹/12, hence
  α₄ = 3g₁₃²/(π⁶R⁹) — the gauge-kinetic coefficient is independent
  data the bundle geometry does not supply. Any T-1 closure must trace
  the F² coefficient, charge normalization, compactification scale, and
  renormalization prescription end-to-end without importing the
  measured α. Recorded as an open gate, not an exclusion.
- **Out of scope (statement, not a claim):** the interior-observer /
  refractive-α chain (R*, σ-weightings) is quarantined play-branch
  material (`play_notes/`) and is not part of this paper.

## Appendix A — Claims and evidence (frozen v1.1)

This appendix is the paper's audit spine: every numbered claim, its
evidence type, and its exact evidence path. Five evidence types are
distinguished, and the type is part of the claim: **documented status**
(a position or value on the record; no command, by design); **analytic
proof** (a derivation closed in the text or its cited record file);
**derivation certificate with numerical support** (responses derived
exactly, with an associated identity observed numerically and labeled
as observed); **computational reproduction** (a script whose output is
the evidence); **identification** (a constant matched to a named
spectral object, with numerical confirmation, without a derivation of
its normalization). A claim's row never promises a stronger type than
it carries.

Numbering (Grok D1): manuscript claims are **X1–X8** — eight numbered
groups in nine table rows, since X3a and X3b are counted separately.
The X-numbers are manuscript-local; they are distinct from the frozen
verification packet's C6a–C9. v0's C1–C9 map: C1→X1, C2→X2,
C3→X3a/X3b, C4→X4, C5→X5, C6→X6, C7→X7, C8→X8, C9→out-of-scope
statement (§5), not a claim.

| # | claim | type | evidence (path · command) |
|---|---|---|---|
| X1 | candidate α⁻¹ = 137.03608245; residual 6.0765×10⁻⁷ vs CODATA 2022; six-digit per §1 convention | documented status | `artifacts/T1_E4_DEPOSIT_NOTE_2026-09-18.md` · — |
| X2 | gate-passing does not certify a prefactor (58/13,057; inference rejected for this family) | computational reproduction (frozen packet) + documented status (continued line) | frozen scan: `mqgt_t1_topological_scan.py`, `mqgt-scf-independent-verification` v1.0-paper — family c = Aπ^j/B, j ∈ {−2,…,2}, A,B ∈ 1…64 → 13,057 distinct values, gate rel. 1×10⁻⁸, 58 pass; the continued-line `mqgt_t1_e4_structure.py` quotes the count and does **not** rerun the scan |
| X3a | the *specific* QED-running route (bare-α running, electron threshold) is excluded: needs q/m_e = 1.00039, no such threshold | documented exclusion (with assumptions) | `E4_FINAL_STATUS.md` · `python3 mqgt_t1_e4_derivation.py` |
| X3b | QED-running closure not advanced without a specified dial-free scale | methodological refusal (documented status) | `E4_FINAL_STATUS.md`; deposit note · — |
| X4 | charge-resolved towers cannot generate c₃ (Prop. 1; scope boundary in §3) | analytic proof + computational certification | `exclusions/DOOR1_TWISTED_TOWERS_CLOSED.md` · `python3 play_notes/play_twisted_towers_lab.py` |
| X5 | Berger κq² ansatz generates no independent slope (Prop. 2; scope boundary in §4) | responses derivation-exact (dL/dκ = +1/7, −1/9; dD1/dκ exact); the lock — σ_κ = ∓D1 in this paper's convention (±D1_t in the lab's, translation printed in Prop. 2) — is a **high-precision computational observation** (1.5e-128 / 1.1e-60), algebraic proof pending | `exclusions/DOOR2_BERGER_CHARGE_CLOSED.md` · `python3 play_notes/play_berger_charge_lab.py` |
| X6 | T-3 constants are spectral determinants on S⁷, S⁹ (S7 = 1.74845220445; S7′ = 0.41364465819) | identification, not derivation; numerically confirmed to 14 digits (E3) | deposit note; verification packet E3 · — |
| X7 | a₄‴(0) = a₄⁗(0) ≡ 0 on the corpus path | analytic proof (exact-integer arithmetic); certificate corrected round 11 — script had computed the full Λ^p bundle labeled coexact; corrected coexact coefficients (S⁷ ce3: A = 94080, B = −40320, C = 3600, mult 20; S⁹ ce2: A = −24192, B = −34560, C = 5040, mult 28) verified exactly; vacuity unchanged | `E4_FINAL_STATUS.md` (correction block) · `python3 mqgt_t1_e4_a4_heat.py` |
| X8 | middle-tower D1 / L / ζ(0) closed forms (exact rational; 65/65 towers) | analytic proof + high-precision certification | `supporting_analysis/MIDDLE_TOWER_*.md`, `ZETA0_THEOREM.md` · three scripts in `supporting_analysis/` |

## Appendix B — Related spectral results (short; companion-note candidates if they grow)

- T-3 identification details (X6) — Dowker–Kirsten coexact towers;
  a name in spectral geometry, not a fitted constant.
- **Scaling constraint (ChatGPT round 11; confirmed by Grok; verified
  here against the record's ζ(0) theorem).** Eigenvalues of the
  Laplace-type towers scale as R⁻², so ζ′_{tR}(0) = ζ′_R(0) +
  2ζ_R(0) ln t. With convention-B values ζ(0) = +1 (S⁷ ce3) and
  ζ(0) = −1 (S⁹ ce2): S7(tR) = S7 + ln t, S7′(tR) = S7′ + 2 ln t.
  Hence **I := S7′ − 2S7 = −3.08325975071 is invariant under common
  rescaling**; the individual determinants are not. Consequence for any
  future repair: a correction built from S7 or S7′ requires a justified
  radius and a dial-free normalization, or a demonstrably
  scale-invariant combination; fitting t to the residual is a dial and
  is refused (same rule as QED running without Λ_Hopf). This is the
  spectral form of Robertson's 1971 radius objection; Gilmore's r = 1
  reply is cited with it in §1. I is uniqueness raw material, not the
  eighth digit. The same radius gate appears in the heat sector: the
  integrated coexact coefficients A₄ᶜᵉ³(S⁷_R) = (49√π/72)R³ and
  A₄ᶜᵉ²(S⁹_R) = −(7√π/640)R⁵ (ChatGPT round 12a; verified exact; X7
  script) are dimensionful — R^{n−4} — so no heat coefficient yields a
  number without the same justified radius prescription. (Refinement,
  ChatGPT round 13: dimensionful is not automatically unusable —
  scale-independent *ratios* exist, since A_{2k} ~ R^{n−2k}; e.g.
  A₄⁵/A₂³ on S⁷ and A₄⁷/A₂⁵ on S⁹ are radius-free. Such a ratio would
  still need an independently justified connection to the
  electromagnetic action, so the central normalization concern stands.)
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
- Gilmore, Phys. Rev. Lett. 28:462–464 (1972) — the r = 1 reply; see §1.
- Nielsen, TUFT v5, Center for Topological Physics
  (github.com/startigerjln/CenterforTopologicalPhysics).
- CODATA 2022 recommended value, α⁻¹ = 137.035999177(21) (NIST).
- Frozen verification record: `mqgt-scf-independent-verification`,
  release v1.0-paper; upstream corpus: `mqgt-scf-science-public`.

---

## Gate status (v1.1)

Grok's accept (2026-09-18) authorized §2 and Appendix A prose after one
box edit; ChatGPT's round-9 conditions were the same edits in longer
form (Prop. 2 definitions unified and differentiated; the lock relabeled
observation-pending-proof; σ_need removed). Those edits are in this
v1.1, and §2 + Appendix A prose is written. **Stop line held:** §§1, 3,
4, 5 and Appendices B–D remain skeleton. Not §§1–6 in one sitting; no
uniqueness lemma; no QED running. Next prose units await the referees'
pass on these two units and Christopher's word.
