# Radiative Sequestering of the Hidden Source J[Ψ] = κ_ES²E
## Record-side note — MQGT-SCF verification program, parallel 2 (2026-09-18)

> **ERRATUM (2026-09-18, ChatGPT review — both points verified and repaired):**
> the original §3(e) claimed the κ vertex reaches the E propagator "only at
> two loops" with δm_E² ~ κ_E²Λ²/(16π²)². Wrong twice: (i) two κ vertices
> already make a **one-loop** E self-energy bubble (internal S₁, S₂ lines);
> (ii) κ_E²Λ² has mass dimension 4, not the dim-2 of a mass correction.
> §3(e) is rewritten with the correct one-loop content: the κ bubble
> (log-divergent) and the Z₂_h-allowed E²X² portal tadpoles (quadratic;
> the actual E-mass naturalness constraint). Lemma 1′ (all-orders absence
> of E|H|²), vacuum alignment, and boundedness are untouched. Credit:
> ChatGPT's 2026-09-18 trace, relayed by Christopher (initially
> mis-credited to Grok in commit 1f0dedc; attribution corrected here).
>
> **ERRATUM 2 (2026-09-18, ChatGPT round 2 — verified and repaired):**
> (iii) with the §1 normalization (λ_EX/2)E²X², the tadpole coefficient is
> λ_EXΛ²/(16π²), not /(32π²) — verified by the background-field identity
> δm_E² = ∂²V₁/∂E²|₀ = λ_EX∫d⁴k/(k²+m_X²); the portal cap halves to
> 1.58×10⁻⁶ (eV/Λ)². (iv) "portals multiplicatively renormalized" was
> wrong: vanishing portals are **not** radiatively stable — tree-level
> exchange induces λ_E1 = λ_E2 = −κ_E²/m_S² = −8.7×10⁻⁹ and a one-loop
> box induces λ_EH ~ κ_E²λ_1Hλ_2H/(16π²m_S²). Repaired in §3(e3): the
> induced floor is calculable and sits 2–3 orders below the cap; the cap
> applies to the bare + induced total.
>
> **ERRATUM 3 (2026-09-18, ChatGPT round 3 — verified and repaired):**
> (v) the λ_EH topology is a **triangle** — two κ_EES₁S₂ vertices + ONE
> Higgs-portal vertex (λ_1H or λ_2H) — with coupling κ_E²(λ_1H+λ_2H),
> not the round-2 box with κ_E²λ_1Hλ_2H. Verified by background-field
> expansion of the §1 potential, V₁ = ½∫Tr ln(k²+M²): the E²h² coefficient
> is exactly the stated triangle integral, equal-mass value
> κ_E²(λ_1H+λ_2H)/(32π²m_S²) = 2.76×10⁻¹¹·(λ_1H+λ_2H), confirmed by
> numeric quadrature (script e3b). Decisive control λ_1H=0, λ_2H=1 →
> nonzero; the box formula wrongly gave zero (the λ_1H=λ_2H=1 benchmark
> coincided at 5.5×10⁻¹¹, masking the wrong dependence). (vi) the
> tree-induced −κ_E²/m_S² terms are **alternative EFT matchings**
> (integrate out S₂ → λ_E1, or S₁ → λ_E2), not additive quartics in the
> full theory where both scalars propagate — the full κ-only answer is
> §3(e1), and no quadratic EFT estimate is extrapolated above the
> integrated-out mass.
>
> **ERRATUM 4 (2026-09-18, ChatGPT round 4 — verified and repaired):**
> (vii) the e2 naturalness condition was stated one-sided
> (λ_E1+λ_E2+λ_EH < cap). Because e3a records NEGATIVE induced quartics,
> a one-sided bound silently admits an arbitrarily large negative mass
> correction. Naturalness bounds |δm_E²|, so the condition is two-sided:
> |λ_E1+λ_E2+λ_EH| ≲ 1.58×10⁻⁶ (eV/Λ)², with field-multiplicity factors.
> The net-sum bound tolerates cancellation among unrelated portals; the
> stricter no-cancellation criterion bounds each |λ_EX| separately.
> These are different claims and are no longer conflated.

**Scope.** Corpus Part 0 open problem 1 states: *"the working hidden source
J[Ψ] = κ_ES² requires a symmetry-complete radiative-sequestering model."*
The corpus supplies: Lemma 1 (tree-level sequestering by hidden parity, §7),
the parametric one-loop estimates eqs. (5.14)–(5.15), the coupled potential
V(S,E) (§8, eq. 18), and the MATH-03 weak-branch stability bound
λ_S > 2κ_E²/m_E². It explicitly flags as missing: *a full hidden-sector
model, vacuum alignment, and loop or spurion calculation* (Ch. 4).
This note delivers those three items at one-loop accuracy, with exact
coefficients where the corpus quoted parametric scalings.

Verification script: `mqgt_sequestering_loops.py` (mpmath, dps = 50).
Nothing here is play-side; all formulas are standard scalar EFT and all
numbers below are reproduced by the script.

---

## 1. Symmetry-complete model

Fields: E, S₁ (Z₂_h-odd); S₂, H (Z₂_h-even). Hidden bilinear O_h = S₁S₂
(odd); source E·O_h (even). Renormalizable Z₂_h-even potential:

V = ½m_E²E² + λ_E/4 E⁴ + ½m₁²S₁² + λ₁/4 S₁⁴ + ½m₂²S₂² + λ₂/4 S₂⁴
  + κ_E E S₁S₂
  + ½λ_E1 E²S₁² + ½λ_E2 E²S₂² + ½λ_12 S₁²S₂²
  + (λ_1H/2) S₁²h² + (λ_2H/2) S₂²h² + (λ_EH/2) E²h²      (h = Higgs fluctuation)

Operator classification (script §a): of the 69 scalar monomials of
dimension ≤ 4 over {E, S₁, S₂, h}, 37 are even (allowed) and 32 odd
(forbidden). **E|H|² is in the forbidden set; E S₁S₂ is allowed.** The
corpus's single-field source κ_ES²E is recovered as the S₁→S₂-aligned
(spurion-maximal) simplification: a literal S²E term is itself Z₂_h-odd,
which is exactly the corpus's own observation that "a literal S2E source
does not by itself explain why |H|²E is absent" (§7). The S₁/S₂ field
split — listed in corpus §5.4 as one of the three sequestering options —
is here realized explicitly.

## 2. Lemma 1′ — all-orders selection rule (upgrade of corpus Lemma 1)

**Statement.** With the Lagrangian of §1 (every vertex Z₂_h-even) and a
parity-preserving regulator/counterterm scheme, the operator E|H|² is not
generated at any order of perturbation theory.

**Proof sketch.** Every propagator connects fields of equal parity and
every vertex is even, so every 1PI amplitude carries even total parity.
E|H|² is odd. Hence its 1PI Green function vanishes to all orders; no
counterterm for it is ever required. ∎

This discharges the corpus's radiative-stability caveat ("every
interaction ... respects the same selection rule", §7) for the full
renormalizable Lagrangian of §1, including the Higgs portals λ_1H, λ_2H,
λ_EH: the regeneration channel of corpus eq. (5.15) exists only in the
S₁≡S₂ simplified limit, not in the split model.

## 3. One-loop coefficients (explicit)

**(c) Hidden-mass correction** (corpus eq. 5.14 made exact). The κ vertex
enters the S₂ self-energy at one loop (E–S₁ bubble), logarithmically
divergent only:

  δm_S² = κ_E²/(16π²) · [ ln(Λ²/μ²) + B0_fin(m_S²; m_E², m_S²; μ²) ]

At benchmark (κ_E = κ_cap = 9.33×10⁻⁸ eV; B0_fin = +1.7193):
δm_S²/m_S² = 8.6×10⁻¹⁰ (Λ = 1 eV) — hidden-mass naturalness is satisfied
by nine orders of magnitude.

**(d) Spurion-broken induced portal** (corpus eq. 5.15 made exact in the
split model). Let Z₂_h be broken only by the soft spurion μ₁₂²S₁S₂.
Then at one loop (triangle with propagators S₁, S₂, S₂):

  δg_H = κ_E λ_2H μ₁₂² · |C₀(0; m₁², m₂², m₂²)| /(16π²),
  C₀(0; m²,m²,m²) = −1/(2m²)   [script reproduces −500000.0 eV⁻² exactly]

Benchmark (maximal spurion μ₁₂² = m_S², λ_2H = 1):
**δg_H = 2.95×10⁻¹⁰ eV**, scaling as δg_H ≈ 2.95×10⁻⁴ · λ_2H · μ₁₂²[eV²] eV.
The induced direct source is bounded, power-counted in the spurion, and
vanishes in the symmetry limit μ₁₂² → 0 — the corpus's requirement
"power-counted and bounded" (Ch. 4) is met with an explicit coefficient.

**(e) E-mass naturalness (corrected — see erratum above).** Two distinct
one-loop channels:

*e1 — κ bubble (log-divergent only).* Two κ_EES₁S₂ vertices close into a
one-loop E self-energy bubble (internal S₁, S₂):

  δm_E² = κ_E²/(16π²) · [ ln(Λ²/μ²) + B0_fin(m_E²; m₁², m₂²; μ²) ]

At benchmark (B0_fin = +0.00167): δm_E²/m_E² = 7.6×10⁻⁸ (Λ = 1 eV),
1.5×10⁻⁷ (Λ = 1 keV), 2.3×10⁻⁷ (Λ = 1 MeV). The κ channel alone is
natural to cutoffs far above 1 MeV — only a logarithm, never a power.

*e2 — portal tadpoles (quadratic; the actual constraint).* The Z₂_h-allowed
E²X² quartics of §1 (λ_E1, λ_E2, λ_EH) give one-loop tadpoles

  δm_E² = (λ_E1 + λ_E2 + λ_EH) · Λ²/(16π²)

[coefficient 16π², erratum 2 above], so E-mass naturalness
(|δm_E²| ≲ m_E² — a large negative correction is equally unnatural,
erratum 4) requires the two-sided condition

  |λ_E1 + λ_E2 + λ_EH|  ≲  1.58×10⁻⁶ · (eV/Λ)²

(1.58×10⁻⁶ at Λ = 1 eV; 1.58×10⁻¹² at 1 keV; 1.58×10⁻¹⁸ at 1 MeV).
This net-sum bound tolerates cancellation among unrelated portals; the
stricter no-cancellation criterion bounds each magnitude separately,
|λ_EX| ≲ the same cap. The two claims are not conflated here (erratum 4).
These portals are Z₂_h-even, so sequestering cannot forbid them — but
they are *not* the forbidden operator: E²|H|²-type terms correct the E
mass, they do **not** regenerate a linear E|H|² source (Lemma 1′ stands).

*e3 — radiative stability of the portal floor (errata 2–3).* Setting the
portals to zero is **not** radiatively stable; they are induced at
calculable values:

- **e3a — tree-level exchange, as EFT matching (not full-theory
  quartics).** Integrating out S₂ induces λ_E1 = −κ_E²/m₂²; integrating
  out S₁ induces λ_E2 = −κ_E²/m₁². These are **alternative** low-energy
  descriptions of the same theory — magnitude κ_E²/m_S² = **8.7×10⁻⁹**
  at benchmark (negative) — not additive quartics in the full theory,
  where both scalars propagate and the complete κ-only one-loop answer
  is the e1 bubble. No quadratic EFT estimate is extrapolated above the
  integrated-out mass.
- **e3b — one-loop triangle for λ_EH (closed form at one loop, erratum 3).**
  Two κ vertices + ONE Higgs-portal vertex:

  λ_EH^ind = κ_E²∫d⁴k/(2π)⁴ [ λ_1H/((k²+m₁²)²(k²+m₂²))
                              + λ_2H/((k²+m₁²)(k²+m₂²)²) ]

  verified by background-field expansion of the §1 potential. Equal
  masses: λ_EH^ind = κ_E²(λ_1H+λ_2H)/(32π²m_S²) =
  **2.76×10⁻¹¹·(λ_1H+λ_2H)** — no O(1) Passarino–Veltman estimate
  remains. "Closed form" applies to this one-loop integral under the
  stated equal-mass, zero-external-momentum assumptions; general
  momenta, unequal masses, and higher loops are separate computations
  (ChatGPT round-3 acceptance precision). Decisive control λ_1H=0,
  λ_2H=1 → nonzero 2.76×10⁻¹¹ (the
  round-2 box formula wrongly gave zero; the λ=1,1 benchmark coincided
  at 5.5×10⁻¹¹ and masked the wrong coupling dependence).

All induced pieces sit orders of magnitude below the 1.58×10⁻⁶ cap, and
their tadpole contributions saturate at ~κ_E²/(16π²) ≪ m_E² once Λ
exceeds m_S (above m_S the partner scalar propagates and the κ bubble of
e1 is the full answer — only logarithmic). The cap therefore applies to
the bare + induced **total**; with N degenerate portal species it divides
by N (h counts one real fluctuation as written; a full SU(2) doublet
would count 4). This is the standard ultralight-scalar portal tuning —
a condition on couplings, not a sequestering failure.

## 4. Vacuum alignment (flagged missing in corpus Ch. 4)

Unbroken Z₂_h forces ⟨E⟩ = ⟨S₁⟩ = 0 identically (no E tadpole exists at
any loop order — the operator E itself is odd). A nonzero ⟨S₂⟩ = v₂ is
allowed and induces E–S₁ mixing κ_E v₂ E S₁. The 2×2 mass matrix is
tachyon-free iff κ_E²v₂² < m_E²m₁², i.e.

  v₂ < v₂_crit = m_E m₁/κ_E = 1.07 eV   (at κ_E = κ_cap)

For v₂ ≲ 1 eV the lightest eigenvalue stays positive and the mixing angle
θ ≤ 0.09 (script §g). Because S₁ itself couples to the SM only through the
even portal λ_1H S₁²h², this mixing does **not** reintroduce a linear
E–Higgs coupling.

## 5. Boundedness — MATH-03 recovered and generalized

Minimizing E (E* = κ_E S₁S₂/m_E²) gives the induced negative quartic
−κ_E² S₁²S₂²/(2m_E²). Boundedness along all ray directions requires

  κ_E²/m_E²  <  λ_12 + √(λ₁λ₂)

In the single-field reduction (S₁ = S₂ = S, λ_S = λ₁ + λ₂ + 2λ_12) this is
**exactly the corpus MATH-03 bound λ_S > 2κ_E²/m_E²** (corpus's V = λ_S/4
S⁴ convention). Numerically at benchmark with λ₁ = λ₂ = λ_12 = 0.1:
κ_E²/m_E² = 8.7×10⁻⁷ vs allowed 0.2 — margin factor 2.3×10⁵; direct grid
minimization of V/t⁴ over x = S₁/S₂ ∈ [10⁻², 10²] gives min = +0.025 > 0.

## 6. Benchmark window (recomputed)

| quantity | value | corpus quote | status |
|---|---|---|---|
| ⟨S²⟩ | 2.3 eV² | 2.3 eV² (eq. 5.11) | matches |
| κ_E cap (½m_E²Ē² = ρ_loc) | 9.3×10⁻⁸ eV | ≲10⁻⁶ eV (eq. 5.13) | corpus conservative ~10× |
| Ē cap | 21.4 eV | ≲ 2 eV (eq. 5.13) | corpus conservative ~10× |
| δm_S²/m_S² (1 loop) | 8.6×10⁻¹⁰ | parametric (eq. 5.14) | coefficient now explicit |
| δg_H (max spurion, λ_2H=1) | 3.0×10⁻¹⁰ eV | parametric (eq. 5.15) | coefficient now explicit |
| δm_E²/m_E² (κ bubble, Λ=1 eV) | 7.6×10⁻⁸ | — | corrected 2026-09-18 |
| \|λ_E1+λ_E2+λ_EH\| naturalness cap (Λ=1 eV) | 1.58×10⁻⁶ | — | corrected ×2 (r2); two-sided (r4) |
| induced tree exchange −κ_E²/m_S² (EFT matching, alternative) | −8.7×10⁻⁹ | — | ChatGPT r2; relabeled r3 |
| induced λ_EH (one-loop triangle) | 2.76×10⁻¹¹·(λ_1H+λ_2H) | — | corrected (ChatGPT r3) |

The corpus's eq. (5.13) pair (κ_E ≲ 10⁻⁶ eV, Ē_S ≲ 2 eV) does not saturate
½m_E²Ē² = ρ_loc; the recomputed saturation values are given above. Both
corpus numbers sit safely inside the window.

## 7. What this closes / what stays open

**Closed here (record-side):**
1. Explicit symmetry-complete renormalizable model (§1) — the "full
   hidden-sector model" item of Ch. 4.
2. All-orders selection rule against E|H|² (Lemma 1′, §2).
3. Explicit one-loop coefficients for δm_S², the spurion-induced portal,
   and the corrected E-mass naturalness analysis (§3e: κ bubble
   log-only; E²X² portal tadpoles λΛ²/16π² as the quadratic constraint;
   induced tree-exchange floor −κ_E²/m_S² (EFT matching) and the
   closed-form one-loop λ_EH triangle, all orders below the cap) — the
   "loop or spurion calculation" item.
4. Vacuum-alignment analysis with the v₂ critical value (§4) — the
   "vacuum alignment" item.
5. MATH-03 recovered exactly and generalized to the three-field system (§5).

**Still open (unchanged, corpus-stated):**
- The global nonlinear retarded source PDE (□ + m_E²)E + λ_EE³ =
  κ_EO_h[S_a] with realistic profiles and S-sector feedback (Ch. 4): local
  control only.
- Nonperturbative vacuum structure of the full three-field potential.
- GKSL-side bare-rate naturalness prior (corpus eq. 5.7) — out of scope here.

*Prepared as part of the MQGT-SCF verification program. Record-side;
no play-side content. All numbers reproduce via `mqgt_sequestering_loops.py`.*
