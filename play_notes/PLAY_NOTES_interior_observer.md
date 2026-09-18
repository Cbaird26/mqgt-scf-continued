# Play Notes — The Interior Observer (2026-09-18)

**Status: play, not the scientific record.** Graduation rule agreed before
running: a principle produces R from the theory's own content → u₀ = η(⟨E⟩R)²
→ net slope σ → gate at 1e-8. Product match graduates; everything else stays
play.

## The idea

The α⁻¹ geometric identity (137.03608245) may describe the *empty* geometry.
We measure from inside the E-scalar background (⟨E⟩ = DETAE = 0.1 eV), so the
measured value could be the geometry dressed by the medium — a refractive
index of the scalar ocean. The correction is third-order (α³): the medium
responding to itself responding to itself.

## Established during play (computed, reproducible)

- The dial exists: all spectral determinants respond to the endomorphism
  shift u = ηE. Files: `mqgt_t1_e4_derivation.py` (scientific record),
  `play_interior_observer_round2.py`, `play_15_ideas_lab.py` (play).
- Net u-slopes of the theory's own towers (both Hopf spheres, principled
  combinations): C1 plain = −8.47, C2 de Rham = +37.4, C3 full Hodge = −8.40,
  C4 torsion = +0.98.
- The whisper (−6.0765×10⁻⁷ relative) requires u₀ ≈ 7.2×10⁻⁸ (C1/C3) —
  an intrinsic scale **R ≈ 0.75 nm (M ≈ 264 eV)**.

## The 15-idea lab (2026-09-18)

- **1 IN-WINDOW:** ZM5, midscale √(DETAE·m_e) = 226 eV → R = 0.873 nm
  (17% off the C1/C3 target). **Coincidence-class** — no principle stated
  for geometric means. Becomes interesting only if a principle appears.
- **8 MISS:** G2/Z2 (DETAE shoreline, 1973 nm), G3 (m_E Compton, 1.97 mm),
  Z1 (m_Φ Compton, 197 μm), ZM1 (lowest-mode anchors, ~8–9 μm),
  ZM2 (Hartree, 7.25 nm), ZM3 (electroweak vev, 8×10⁻¹⁰ nm),
  ZM4 (dark-energy density, 86 μm).
- **6 UNDEFINED (need operational form):** G1 (fiber radius is a free
  modulus; ζ gives no extremum — d logdet/d ln R = 2ζ(0) = ±2 ≠ 0),
  G4 (CP⁴ physical radius likewise free), G5 (winding reduces to free R at
  Hopf charge 1), Z3 (tested round 1, gate fails by 15%),
  Z4 (GKSL rate → length needs γ₀ in physical units + a speed),
  Z5 (no definition).

## Lab 2 — the torus harness (2026-09-18, `play_torus_fixed_point_lab.py`)

- **The torus upgrades the free-modulus theorem:** topology alone sets no
  size, but a torus carries self-duality (R ↔ ℓ²/R), which fixes a preferred
  size. Grok's "reciprocal fixed point" is exactly that principle.
- **The fixed point is formulation-invariant** (geometric means are
  inversion-covariant): R* = √(L_coh·λ̄_e) = 0.873 nm ↔ E* = √(DETAE·m_e) =
  226 eV. The only principle of the night producing a nanometer scale from
  stated program content. (An earlier claim of length/energy ambiguity was
  wrong and was corrected by the harness itself.)
- **Remaining gap, quantified:** R* gives u₀ = 9.8×10⁻⁸; the chain then needs
  a combination slope of −6.21; the pre-declared combinations give −8.47
  (C1/C3), +37.4 (C2), +0.98 (C4). Product misses the gate by ~36% on the
  slope. **Candidate, not closed.**
- **Torus constants:** self-dual determinants at τ = i and τ = e^{iπ/3} sit
  32–67% from |c₃|. The torus matters as the *principle* (self-duality fixes
  size), not as the constant.

## What would graduate the idea

1. A principle that produces R ≈ 0.36–2.2 nm from program content
   (e.g. a derived reason for the midscale √(DETAE·m_e), a compactification
   radius, a monitor coherence length).
2. A derived tower→α combination rule fixing which σ (C1–C4) is real.
3. Sign check: C1/C3 want u₀ > 0; C2/C4 want screening sign.

Until then: the ocean stays metaphor — but a metered one.

## Lab 3 — GKSL-weighted combinations (2026-09-18, `play_gksl_weighted_lab.py`)

Proposal: towers couple to α through a GKSL-weighted determinant product,
weights fixed by the corpus rates γ_k(E) = γ₀/(k e^{ηE}), no free parameters.

Findings:
- Structural: the corpus rate weights MODES, and Σ d(k)/k diverges on spheres;
  the weighting is only defined under a bandwidth K. So the honest test was a
  robustness scan over K = 3..800.
- The good news: the combination is genuinely robust — σ(K) plateaus at
  +1.87 → +1.89 across two and a half decades of K, dominated by the S⁹
  high-p towers. The mechanism is well-defined; the plateau means no hidden
  cutoff-tuning.
- The bad news: the plateau sits at **+1.88**, not the needed **−6.21**.
  Wrong value AND wrong sign. MISMATCH — stays play.

Status of the branch: the interior-observer chain now stands as
R* = 0.873 nm (self-dual fixed point, formulation-invariant) → u₀ = 9.8e-8 →
needs σ = −6.21; unweighted sums give −8.47, GKSL-weighted gives +1.88,
single towers give +1.33/+1.35. The combination rule remains the sole open
gate of this play branch. Do NOT iterate weightings ad hoc — that is the
coincidence trap; a new weighting needs its own principle first.

## Lab 4 — self-dual parity projection (2026-09-18, `play_parity_projection_lab.py`)

Proposal (Grok, principle declared first): the interior monitor projects onto
the self-dual eigenspace of B = ⋆d, flipping high-p tower parity; the
combination slope σ = Σw_p D1_p / Σw_p L_p is computed with signs fixed by
the projection, never fitted.

Corpus grounding (full traversal of the 6,916 pp corpus, same day):
- Projection IS corpus-native: the Place-3 monitor coupling is literally a
  projector, H_SR = λ(ΔE)|L⟩⟨L|⊗B (Reservoir Protocol Note, corr. ed., eq. 11).
- Signed channel response IS corpus-legal: γ_k(E) = γ⁰_k e^{η_k E}, η_k ∈ ℝ
  per channel (Part 0 Thm 3.2). η_p < 0 = inhibited channel. The corpus
  assigns NO sign to any tower — the assignment rule is the missing input.
- NOT corpus-native: the S⁷/S⁹ coexact towers themselves (verification-side
  machinery) and any self-duality→sign map.
- Math check: on round Sⁿ (n odd), ⋆² = +1 on all forms; B self-pairs only
  the middle tower (S⁷ p=3, S⁹ p=4); the η-invariant of B vanishes on the
  round metric — the ± splitting is exactly balanced, so a self-dual
  projection selects half the middle tower but breaks no balance by itself.

Harness validation: control P4 (alternating) reproduced +37.42 ✓; baseline
(all +1) reproduced −8.4674 ✓.

Scorecard (four pre-declared projections, no others tried — guardrail held):
| projection | σ | dist to −6.21 | ratio | play window |
|---|---|---|---|---|
| P1 flip p≥2 | −7.729 | 1.52 | 1.245 | YES (closest) |
| P2 flip p≥3 | −11.391 | 5.18 | 1.834 | YES (barely) |
| P3 flip self-paired middle only | −8.475 | 2.27 | 1.365 | YES |
| P4 alternating (control) | +37.42 | 43.6 | −6.03 | no |

Verdict per pre-declared rules: P1 lands in-window with correct sign —
CANDIDATE-class, gated on deriving the sign assignment from monitor dynamics.
No projection converges to −6.21; the best is 24% off in magnitude. The
slope gap narrowed (from −8.47 baseline to −7.73) but is not closed.

SPARK (structural, possibly record-side): the two self-paired middle towers
nearly cancel each other — S⁷ce3 (L=+3.4969, D1=+4.651) vs S⁹ce4
(L=−3.4859, D1=−4.7135): magnitudes match to 0.3% (L) and 1.3% (D1) with
opposite signs. That is why P3 barely moves σ. If exact, this mirror
identity is a property of the theory itself, not of any play weighting —
worth a record-side check with the full zeta machinery.

## Mirror settlement (record-side, 2026-09-18, `mqgt_mirror_check.py`)

Grok's call: exact zeta check before any new weightings. Result at dps=80:
the S⁷ce3/S⁹ce4 mirror is **NOT exact** (L residual 3.1e-3, D1 residual
1.3e-2 = exactly −1/16). Coincidence-class near-relation; the weighting
hold discharges with a negative. Bonus, exact: the whole middle-tower family
obeys D1 = (−1)^x0·(π²/3 + H₂(x0−1)) at dps=80 across S³..S¹³ — see
E4_MIRROR_CHECK_2026-09-18.md (record-side, 07_Supporting_Analysis).

## Lab 5 — the Lagrangian package (2026-09-18, `play_lagrangian_package.py`)

Question (Grok's (a), ordered): can a Lagrangian produce NATIVE η-signs —
signs derived from an E-coupling rather than assigned?

The standard scalar–form coupling menu, analyzed before running:
- Axionic E·(topological density): zero on round Sⁿ (no harmonic p-forms).
  EXCLUDED structurally.
- Mass portal E²|A|²: quadratic — no linear response at the background.
  EXCLUDED structurally.
- Dilatonic S_p = ∫ e^{γE} dA_p∧⋆dA_p (E as internal-geometry modulus):
  by det(cA) = c^{ζ(0)} det A, sector p's response weight is ζ_p(0); γ is
  common and cancels in the σ ratio. Signs = the towers' own ζ(0) signs.

Controls: p=0 towers identified as SCALAR towers (archive match exact);
baseline reproduced −8.4674 ✓.

Findings (all at dps=80):
- **ζ(0) of scalar towers = 0 exactly** (1e-73 / 1e-82) — scalar sectors do
  not respond to a uniform modulus at all; they decouple.
- **ζ_ce_p(0) = (−1)^{p+1} exactly** on both spheres, all p (1e-40) — the
  dilaton weights ARE the alternating pattern; the first native sign source
  found. (Plausibly a known sphere fact; provable by the same trivial-zeros
  mechanism as the middle-tower forms; not yet promoted record-side.)
- **σ_dil = +0.7973** (Σ ζ(0)D1 / Σ ζ(0)L, one shot, pre-declared).
  Misses the window: wrong sign, wrong magnitude. EXCLUDED as stated.
  Verdict per pre-declared rules; the standard menu is now exhausted.

Diagnostic (recorded, NOT adopted — coincidence-trap guard):
- Uniform-sign family: σ(t) runs −3.01 (scalars off) → −8.47 (full);
  crosses −6.21 at scalar share t* = 0.01952 (~1.95%). Reachable but no
  principle produces that fraction.
- Alternating family: σ(t) runs +0.80 → −3.35; never reaches −6.21.

Branch status: the interior-observer chain's combination rule now has a
complete exclusion record across every principled weighting tried:
uniform −8.47, full-Hodge −8.40, de Rham +37.4, torsion +0.98, GKSL +1.88,
parity P1/P2/P3 −7.73/−11.39/−8.47, dilaton +0.80. −6.21 has not been
produced by any principle. Next move needs a NEW principle (not a new
weighting) or goes record-side: derive f_p(E) per sector from an actual
E–form Lagrangian beyond the standard menu — or accept E4 open.

---

## 2026-09-18 ~04:40 — ζ(0) results promoted record-side (Selection 3)

The two dilaton-lab micro-results are now CERTIFIED as middle-tower family
extensions (script `mqgt_zeta0_theorem.py`, note `ZETA0_THEOREM.md`,
archived in 07_Supporting_Analysis):

- **ζ_ce_p(0) = (−1)^{p+1} exactly** for ALL 65 coexact p-form towers,
  n=3..21 odd, every p — exact rational arithmetic (fractions.Fraction),
  via ζ(0) = −c₀/2 − Σ_{q=1}^{x0−1} d(q) from the trivial zeros at
  s = −1,…,−(x0−1). The alternating pattern is a theorem, not a numerics
  coincidence.
- **Scalar towers**: ζ(0) = 0 under convention A (constant mode formally
  included), ζ(0) = −1 under convention B (det′ = coexact-0 determinant).
  Exact for S³..S²¹. dps=80 machinery cross-check: worst |Δ| = 1.07e-60.

**Convention discovery (play-relevant):** the lab-5 claim "scalar sectors
do not respond to a uniform modulus" is a CONVENTION-A artifact of the
zero mode. Under det′ (convention B) the scalar rows DO respond:
  S⁷ scal det′: L = −0.200915319509,  D1 = +0.408333
  S⁹ scal det′: L = +0.0547377225888, D1 = +0.339732
(vs convention A: L = 4.169/3.850, D1 = −43.9/−24.6).
Uniform-play baseline shifts: A = −8.4674 → B = −12.677.
All play scorecard numbers so far are convention-A. A full convention-B
rebuild of labs 1–5 is an OPEN recheck item — not done, queued. σ_need =
−6.21 is convention-independent (it is rel-gap/u₀), so the gate itself
does not move; only the scorecard's bookkeeping convention is in question.

---

## 2026-09-18 ~15:00 — Convention-B rebuild DONE (open recheck item closed)

Script `play_conventionB_rebuild.py`. Controls all pass: A-side reproduces
every archived scorecard value; B-side p=0 rows match the ζ(0) certification
to 1e-9; torsion is convention-invariant as predicted (p=0 weight is 0).
GKSL note: Γ₀ weights are convention-independent (nonzero scalar spectrum
= coexact-0 spectrum — proven by build(n,0) reproducing the det′ values;
the standalone deg_coexact(·,0,·) helper is a p≥1 formula and does NOT
degenerate to the scalar spectrum — measured, noted, not used).

Scorecard (σ by weighting, A → B):

| weighting | σ_A | σ_B |
|---|---|---|
| uniform | −8.467 | −12.677 |
| de Rham | +37.42 | +0.713 |
| full Hodge | −8.395 | +1.694 |
| torsion | +0.980 | +0.980 (invariant) |
| parity P1 | −7.729 | −0.099 |
| parity P2 | −11.391 | −0.451 |
| parity P3 | −8.475 | −9.832 |
| dilaton ζ(0) | +0.797 | +0.713 |
| GKSL plateau | +1.88 | +1.726 |

Structural findings:
1. **dilaton-B ≡ de Rham-B exactly** (0.71259342 both): under B the ζ(0)
   weights are (−1)^{p+1} on every row including the scalar (−1), i.e.
   −(−1)^p uniformly — the two labs cross-validate.
2. **The t* = 0.0195 crossing was a convention-A artifact.** Under B the
   uniform family runs σ(0) = −3.01 → σ(1) = −12.68 and crosses −6.21 at
   t* = 2.29, OUTSIDE [0,1]. The one "reachable in principle" diagnostic
   of the A scorecard evaporates under det′.
3. **P3 lands at −9.832 under B** — inside the loose factor-2 window
   (ratio 1.58). Same class as the A-side window hits (uniform −8.47,
   Hodge −8.40, P1 −7.73): a lead, not an approach to the 1e-8 gate.
   Nothing in either convention comes near the gate.
4. **New metadata for the branch:** σ is CONVENTION-SENSITIVE for every
   weighting that touches p=0. Any future candidate principle must arrive
   with its zero-mode prescription attached, or it is not well-defined.

Verdict: the combination-rule exclusion record now stands under BOTH
zero-mode conventions. Convention-robust values: torsion +0.98, GKSL
+1.7–1.9 — both far from −6.21. The freeze on new weightings stands;
Option 1 (E–form Lagrangian beyond the standard menu) remains the only
open play route, deferred per directive.

---

## 2026-09-18 ~15:20 — OPTION 1 EXECUTED AND CLOSED (operator-basis pass)

Done as a corpus-grade (MATH-01) operator-basis enumeration, not as
another weighting: the COMPLETE basis of linear-in-E, gauge-consistent,
parity-even couplings of E to a free p-form sector on round Sⁿ, each
class given exactly one disposition. Script `play_option1_operator_basis.py`.

| class | coupling | disposition |
|---|---|---|
| B1 uniform dilaton | e^{γE} on whole operator | computed (lab 5): σ = +0.797 — excluded |
| B2 non-minimal endomorphism | E·A∧⋆(E₀A), w_p = p(n−p) | computed here: **σ_nm = +1.84155187751** — excluded (wrong sign) |
| B3 Chern–Simons | E·A∧dA (middle forms only) | structurally zero: round Sⁿ has an orientation-reversing isometry conjugating ⋆d → −⋆d, so the ⋆d spectrum is ±-symmetric mode by mode and the linear response cancels identically; first effect O(E²) |
| B4 BF mixing | E·A_p∧⋆dA_{p−1} | structurally zero within the coexact set (d maps coexact → exact, outside the operator content) |
| B5 higher-derivative | E·A∧⋆(Δ^q A) | q = 1 collapses to B1; q ≥ 2 power-divergent, EFT-unnatural (MATH-01 kill condition) |
| B6 portal / axionic | E²\|A\|², E·top. density | quadratic / zero on round Sⁿ (prior) |

Properties of B2 worth recording: it is the first CONVENTION-INDEPENDENT
principle (scalar endomorphism is exactly zero on any space, so the
zero-mode question never arises), and its value +1.84 lands inside the
positive-side cluster {torsion +0.98, GKSL +1.73–1.89, dilaton/de Rham-B
+0.71} — structure noted, not a hit.

**Option 1 verdict: CLOSED.** Every linear-response class is structurally
zero, EFT-unnatural, or numerically excluded. The interior-observer branch
has no remaining play route to σ = −6.21 expressible with the declared
operator content. Per the branch's own rules, this is the stopping point:
the refractive/interior-observer idea remains play, its scorecard now
complete under both zero-mode conventions and under the full operator
basis. Record-side, E4 stands with the pinned target
c₃ = −1.56371823031276 and a total exclusion record (fits, QED running,
existing invariants, heat kernel, middle towers, ζ(0) families, and now
the complete linear-response E×form basis).

---

## DOOR 1 — TWISTED TOWERS: Hopf-charge-resolved spectra (2026-09-18, PLAY)

**Principle (Christopher, declared before computation):** twisted towers are
the geometry's native missing content — Hopf-line-valued forms on the actual
bundle, not plain free ringing. Compute the charged coexact spectra for the
S⁷-3 and S⁹-2 sectors; any structural shift that produces c₃ closes the
residual without dials. One shot, distances reported, never graded.

Script `play_twisted_towers_lab.py`, output `play_twisted_towers_lab_out.txt`.

### Machinery (new, built for this door)

- **Charge engine:** SO(2n) Weyl character formula at the diagonal Hopf
  specialization x_j = t, via the confluent-determinant limit,
  ch_λ(t₀) = [s^N]det M^λ / [s^N]det M^ρ, N = n(n−1)/2, solved for integer
  charge multiplicities d_q at t₀ = 2..A+2 (t₀ = 1 singular).
- **D-type chirality subtlety (discovered in controls):** for λ_n ≠ 0 the
  +det ratio returns the O(2n) average (ch₊ + ch₋)/2 at the diagonal
  specialization — diagnosed from a raw q=±4 coefficient of exactly 0.5 on
  [1,1,1,1], sums to half the full tower. The physical middle-form tower
  carries both chiralities ⇒ scale by 2. Certified by C1 at every level.
- **Pole regularization (derived in-file):** sector degeneracy polys contain
  ALL powers of x (record towers are even-only), so the binomial expansion
  of (x²−a2)^{−s} hits the Hurwitz pole at 2j−m = 1 for odd m. The finite
  constant term: ζ(0) gains c·a2^j/(2j), ζ′(0) gains
  (c·a2^j/j)·(H_{j−1}/2 − ψ(x0)). Certificate C5 below.

### Controls — ALL PASS

- **C1** Σ_q d(level,q) = deg_coexact/deg_scalar total, every level, both
  towers, k = 0..16 (S⁷: 70…3432198; S⁹: 120…49480200, all exact).
- **C2/C3** palindrome, nonneg integers, clean rounding margins.
- **C4** scalar sectors vs independent SU(m+1) Weyl-product closed form,
  S⁷/S⁹, k = 0..4, q = 0..3: all match.
- **C5** spectral certificate: sector ζ′(0), ζ(0), D1 vs an INDEPENDENT
  Laurent extraction from the exact binomial expansion at s = ±10⁻³
  (never touches the pole; two-level Richardson) plus finite-difference D1.
  Four scalar sectors (S⁷/S⁹ × q = 0,2): agreement to ~1e-10 on every
  quantity. The pole algebra is certified, not assumed.
- **Void control (recorded):** a truncated sector-SUM control is void —
  sector zeta values carry pole terms cancelling only across ALL sectors
  (verified numerically: partial sums ~392 vs full 4.17). No such control
  used or claimed.

### Resolved sector spectra (per-sector ζ′(0) = L_q, D1_q, ζ_q(0))

**S⁷ coexact 3-forms** (a2 = 0, so no pole terms at all — these are pure
tails): q = 0: L = −0.540917949086; q = 1: +83.27; q = 2: +16.05;
q = 3: +106.16; q = 4: +149.45; q = 5: +776.65; q = 6: +2554.41;
q = 7: +10184.23; q = 8: +11362.19. High-q sectors have large tails;
only the full all-sector sum telescopes to the archived tower value.

**S⁹ coexact 2-forms** (a2 = 4): q = 1: L = −1.58421491374,
D1 = +0.2202812508, ζ(0) = −0.09558; q = 3: L = +10.905540999,
D1 = −0.3458115882, ζ(0) = +0.1773. (Later-onset sectors lack the
degp+1 levels needed for stable polys inside KMAX = 16; tables exact and
archived in the output file.)

### Probes and verdict

Pre-declared truncated second-charge-moment probes:
S⁷ M2_L = 2682152.6, M2_D1 = 3685940.3; S⁹ M2_L = 193.13, M2_D1 = −5.78;
σ_M2(trunc) = +1.374 — distance 7.58 to σ_need = −6.21, 2.94 to c₃.
**Dominated by the highest-q resolved tails (q = 7,8 carry ~91% of M2_L);
truncation artifact dwarfs any signal — indicative only, by design never
graded.**

**Door-1 verdict: CLOSED, negative, with a structural reason.**
The Hopf U(1) acts by isometry, so charge resolution splits ONLY
degeneracies, never eigenvalues; every zeta invariant of the twisted tower
sums back over sectors to the identical untwisted value (exact identity,
certified). c₃ does not live in the charge split. The naive charge moments
produce nothing near c₃ or σ_need, and the split introduces no new
spectral scale at all.

**Where a twist could still bite (hypothesis, not computed):** only an
operator that couples charge to EIGENVALUE — e.g. a charged/ Landau-type
Laplacian λ → (x² − a2) + κq² from a nontrivial Hopf-connection curvature
background — changes the spectra themselves rather than their resolution.
That is a different door (dynamical background field, not the round
sphere), to be declared with its own principle before any computation.

### Engineering notes (for future labs)

- Record modules RESET mpmath dps on import (mqgt_t1 sets 80); set dps
  AFTER imports. Symptom was precision-independent rounding margins.
- int(mpf) TRUNCATES — int(round(...)) for control targets.
- q = 0 scalar sector: skip the j = 0 constant zero mode (onset k = 1).
- det denominator cached per rank; dps 140 suffices for KMAX = 16
  (conditioning eats ~41 digits).

---

## DOOR 2 — BERGER CHARGE SUSCEPTIBILITY (2026-09-18, PLAY)

**Declared principle (before computation):** the dial-free geometric source
of charge-to-eigenvalue coupling is the canonical variation (Berger squash)
of the Hopf fibration — the unique metric deformation holding the CP^m base
fixed and scaling the S¹ fiber. On scalars it provably shifts every
charge-q eigenvalue by exactly κq², κ = t⁻² − 1 from the round point
(κ = 0 is the record, already excluded). Applied as the Landau-form ansatz
λ → λ + κq² to the two coexact α towers. One shot, distances reported,
never graded.

Script `play_berger_charge_lab.py`, output `play_berger_charge_lab_out.txt`.

### Why this door is truncation-free

Door 1's failure mode (per-sector tails dominate, sums don't converge in
window) is structurally absent: the total charge moment
Q2(k) = Σ_q d_q(k)q² is a closed-form EVEN polynomial in x
(Dynkin-index polynomiality), so the round-point linear responses

  dL/dκ|₀  = + Σ_x Q2(x)/λ(x),   dD1/dκ|₀ = − Σ_x Q2(x)/λ(x)²

are exact full-tower zeta values — no sectors, no cutoff.

### Controls — ALL PASS

- **C1** charge-table sums vs deg_coexact at all 15 levels (both towers).
- **C2** Q2 polynomiality holdout-certified (fit k = 0..11, exact on
  k = 12..14, rel dev ≤ 1.5e-134); Q2 exactly even in x (odd part 0.0 —
  this is what keeps the Hurwitz pole out of the λ² sums).
- **C3** window-shift consistency of both responses to ≤ 1e-140.
- **C4** THE LOCK (discovered in-run, then promoted to a control):

### Results

| tower | dL/dκ | dD1/dκ | σ_κ | distance to −6.21 |
|---|---|---|---|---|
| S⁷ ce3 | +1/7 (exact) | +0.664425606401 | **+4.650979245** | 10.861 |
| S⁹ ce2 | −1/9 (exact) | +19/720 (exact) | **−0.2375** | 5.9725 |
| combined | | | **+21.7606566** | 27.971 |

**Door-2 verdict: CLOSED, excluded** — but with the sharpest structural
statement of the play branch so far:

**σ_κ = ±D1(tower) EXACTLY in both towers** (deviations 1.5e-128 and
1.1e-60): each tower's charge susceptibility is locked to its own
self-response. The canonical-variation route cannot generate an
independent slope in the (L, D1) plane — and σ_need = −6.21 would require
exactly such independence. Note also dL/dκ = ±1/n (+1/7, −1/9), an exact
rational pattern ((−1)^{(n+1)/2}/n, pattern noted not proved).

Sign honesty: per-mode responses are sign-definite, but zeta-regularized
tower totals are not (regularized sums of positive series can go
negative); the signs reported are the exact regularized values, same
convention as the record scorecards.

**Play-branch status after two doors:** Door 1 — isometry splits only
degeneracies, c₃ structurally absent from the charge split. Door 2 — when
charge IS coupled into eigenvalues via the geometry's own deformation, the
response is locked to ±D1, not free. Two doors, two structural locks. The
c₃ slope requires content outside {charge resolution, canonical fiber
deformation} — e.g. base (CP^m) metric deformation, torsionful
connections, or genuinely dynamical E-field content. Any next door gets
its own declared principle first.
