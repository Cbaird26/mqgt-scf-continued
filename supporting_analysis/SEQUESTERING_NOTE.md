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
>
> **ERRATUM 5 (2026-09-18, ChatGPT round 5 — verified and repaired):**
> (viii) erratum 4 mis-stated the no-cancellation criterion as a
> per-channel bound |λ_EX| ≲ C. That is a screening criterion only and
> does NOT bound the combined correction: two portals each at 0.9 C sum
> to 1.8 C. §3(e2) now labels the three distinct statements separately:
> (i) the net bound |Σ_X N_X λ_EX| ≲ C (cancellations allowed);
> (ii) the no-cancellation sufficient condition Σ_X N_X |λ_EX| ≲ C
> (implies (i) by the triangle inequality); (iii) per-channel
> |λ_EX| ≲ C as screening only. N_X = field multiplicity under the §1
> normalization.
>
> **ERRATUM 6 (2026-09-18, SELF-REVIEW — peer-review pass, verified and
> repaired):** (ix) §3(d) kept only the λ_2H triangle (propagators
> S₁,S₂,S₂). Background-field expansion of the same §1 potential
> (M²_S₁S₂ = μ₁₂² + κ_E E) gives BOTH mirror channels: h² attaches to
> the S₁ line (λ_1H; propagators S₁,S₁,S₂) or the S₂ line (λ_2H;
> propagators S₁,S₂,S₂). Full coefficient: δg_H = κ_E μ₁₂²
> [λ_1H|C₀(m₁²,m₁²,m₂²)| + λ_2H|C₀(m₁²,m₂²,m₂²)|]/(16π²) =
> 2.95×10⁻¹⁰·(λ_1H+λ_2H) eV at maximal spurion — same verification
> method as e3b; the qualitative conclusion (bounded, power-counted,
> vanishing as μ₁₂² → 0) is unchanged. (x) at the same spurion order
> there is also an h⁰ linear-E tadpole g_E = μ₁₂²κ_E/(16π²)[ln+B₀]
> (~8.7×10⁻¹⁵ eV³, Λ = 1 eV; induced ⟨E⟩ ~ 8.7×10⁻⁷ eV), now stated
> alongside δg_H; §4's ⟨E⟩ = 0 is the exact-symmetry statement.
>
> **ERRATUM 7 (2026-09-18, ChatGPT round 6 — full-note review, verified
> and repaired):** (xi) §1's potential is A minimal Z₂_h-even closure,
> not the general symmetry-allowed model: ES₁, S₁²S₂, S₂³, ES₁H†H,
> S₂H†H (and higher allowed monomials) are renormalizable and even, are
> set to zero here, and no symmetry excludes them. Lemma 1′ is unaffected
> (all are even; the odd E|H|² still cannot be generated), but the §3
> loop inventory is the minimal-model inventory, and "S₁ couples to the
> SM only through S₁²h²" is a model assumption, not derived. §1 retitled
> and scoped. (xii) The naturalness budget is a low-energy EFT statement;
> naive extrapolation of the induced λ_EH to m_h = 125 GeV gives δm_E² ~
> λ_EH m_h²/(16π²) ~ 5.4×10⁹ eV² vs m_E² = 10⁻⁸ eV² (ratio ~5×10¹⁷).
> This minimal model does NOT establish a natural ultralight scalar
> coupled to the physical Higgs; weak-scale matching, or reading h as a
> light toy scalar, is required — new §3(e4). (xiii) the maximal-spurion
> benchmark sits at exact eigenvalues m_S² ± μ₁₂² = {0, 2m_S²}: the
> single-insertion expansion is uncontrolled at its endpoint. The exact
> background-field resummation is now in the note and script: at
> μ₁₂² = ½m_S² the resummed value is 3.24×10⁻¹⁰ eV (leading insertion
> 2.95×10⁻¹⁰, ratio 1.10); at μ₁₂² → m_S² the exact integrand is
> IR-divergent, so the maximal-mixing number is a leading-insertion
> estimate requiring an IR prescription at the endpoint. (xiv) §5's
> inequality is relabeled: with positive quartics the full potential is
> bounded at large field regardless (t⁴ dominates the cubic); the
> MATH-03 condition governs the E-integrated effective quartic — the
> corpus's own branch — which is the sense in which it is recovered.

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

## 1. Minimal Z₂_h-even model (closing the corpus source)

Fields: E, S₁ (Z₂_h-odd); S₂, H (Z₂_h-even). Hidden bilinear O_h = S₁S₂
(odd); source E·O_h (even). The renormalizable Z₂_h-even potential used
throughout this note:

V = ½m_E²E² + λ_E/4 E⁴ + ½m₁²S₁² + λ₁/4 S₁⁴ + ½m₂²S₂² + λ₂/4 S₂⁴
  + κ_E E S₁S₂
  + ½λ_E1 E²S₁² + ½λ_E2 E²S₂² + ½λ_12 S₁²S₂²
  + (λ_1H/2) S₁²h² + (λ_2H/2) S₂²h² + (λ_EH/2) E²h²

Here and throughout, h denotes a Higgs-like fluctuation that — for every
quantitative statement in this note — is the eV-scale scalar of this
minimal model (m_h ≪ Λ = 1 eV), *not* the physical 125 GeV Higgs. The
SM-Higgs reading is the open weak-scale matching problem, stated and
bounded in §3(e4); nothing quantitative here claims that matching.

**Scope (erratum 7).** This is a *minimal* Z₂_h-even closure, not the
general symmetry-allowed model. Further renormalizable even monomials —
ES₁, S₁²S₂, S₂³, ES₁H†H, S₂H†H, and others from the script's allowed
set — are permitted by the stated parity and are here set to zero; no
symmetry or renormalization condition excludes them. The script's
classification is explicit on this point and was misread in the E7
adjudication: with odd = {E, S₁}, ES₁ carries parity (−1)^(nE+n₁) = +1
— even, hence *allowed* — and the script prints exactly that
(`explicit check: E*S1 parity = 1`); an earlier print line that listed
E·S₁² under "key forbidden" referred to the odd operator E·S₁², not
ES₁, and has been clarified. Allowed-but-absent is a model choice,
not a symmetry. Two consequences, stated plainly: (a) Lemma 1′ is unaffected — every omitted term is even,
so the odd operator E|H|² still cannot be generated at any order;
(b) the §3 loop and naturalness inventory is the inventory of *this*
model, and the statement "S₁ couples to the SM only through S₁²h²" is a
model assumption (the minimal portal), not a derived fact.

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
S₁≡S₂ simplified limit, not in the split model (absent soft Z₂_h
breaking; with a soft spurion it reappears bounded and power-counted —
that is §3(d)).

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
Then at one loop the h² attaches to either hidden line — two mirror
triangles (erratum 6):

  δg_H = κ_E μ₁₂² [ λ_1H|C₀(0; m₁², m₁², m₂²)| + λ_2H|C₀(0; m₁², m₂², m₂²)| ]/(16π²),
  C₀(0; m²,m²,m²) = −1/(2m²)   [script reproduces −500000.0 eV⁻² exactly, both channels]

verified by background-field expansion of the §1 potential
(M²_S₁S₂ = μ₁₂² + κ_E E; coefficient of E h² in V₁ = ½∫ln det(k²+M²)).
Equal-mass benchmark (maximal spurion μ₁₂² = m_S²; **leading-insertion
estimate** — see the resummation below):
**δg_H = 2.95×10⁻¹⁰·(λ_1H+λ_2H) eV** (5.9×10⁻¹⁰ eV at λ_1H=λ_2H=1),
scaling as δg_H ≈ 2.95×10⁻⁴ · (λ_1H+λ_2H) · μ₁₂²[eV²] eV.
At the same spurion order there is also an h⁰ linear-E tadpole
g_E = μ₁₂²κ_E/(16π²)[ln(Λ²/μ²) + B₀] ≈ 8.7×10⁻¹⁵ eV³ (Λ = 1 eV),
inducing ⟨E⟩ ~ g_E/m_E² ~ 8.7×10⁻⁷ eV (erratum 6).
Both effects are bounded, power-counted in the spurion, and vanish in
the symmetry limit μ₁₂² → 0 — the corpus's requirement "power-counted
and bounded" (Ch. 4) is met with explicit coefficients.

*Exact-mixing resummation (erratum 7).* At μ₁₂² = m_S² the exact
S₁–S₂ mass-squared eigenvalues are m_S² ± μ₁₂² = {0, 2m_S²}: the
single-insertion expansion is uncontrolled at its advertised endpoint.
The background-field determinant is exact in μ₁₂² and gives the
resummed coefficient

  g_Eh² = κ_E μ₁₂² ∫ d⁴k/(2π)⁴ (λ_1H D₂ + λ_2H D₁)/(D₁D₂ − μ₁₂⁴)²,
  Dᵢ = k² + mᵢ²,

which recovers the leading-insertion result for μ₁₂² ≪ m_S². At
μ₁₂² = ½m_S² (λ = 1,1): resummed 3.24×10⁻¹⁰ eV vs leading-insertion
2.95×10⁻¹⁰ eV (ratio 1.10). As μ₁₂² → m_S² the lighter eigenvalue
vanishes and the exact integrand behaves as 1/k⁴ — IR-divergent; the
maximal-mixing number is therefore a leading-insertion estimate, and an
IR prescription is required at the endpoint (script d-resum).

*Closed form (ChatGPT, round 8 — verified here by hand integration and
against the script's quadrature).* For equal hidden masses, writing
u = μ₁₂², the integral evaluates exactly:

  g_Eh² = κ_E(λ_1H+λ_2H)/(64π²) · ln((m_S²+u)/(m_S²−u)),   0 ≤ u < m_S²,

which displays all three regimes at once: small-u, ln((1+x)/(1−x)) ≈ 2x
recovers the insertion 2.95×10⁻¹⁰·(λ_1H+λ_2H) eV; at u = m_S²/2 the
ratio to the insertion is exactly ln 3 = 1.0986 (the reported 1.10);
and the u → m_S² divergence is logarithmic in the vanishing eigenvalue.
Script d-resum prints the closed form beside the numerical quadrature
(agreement at mpmath precision).

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

  |λ_E1 + λ_E2 + λ_EH|  ≲  1.58×10⁻⁶ · (eV/Λ)²   (= C, net, N_X = 1 as written)

(1.58×10⁻⁶ at Λ = 1 eV; 1.58×10⁻¹² at 1 keV; 1.58×10⁻¹⁸ at 1 MeV).
Three distinct statements live here (erratum 5); they are not
conflated:

  (i)  net correction — cancellations allowed:
       |Σ_X N_X λ_EX| ≲ C
  (ii) no-cancellation sufficient condition — implies (i) by the
       triangle inequality:
       Σ_X N_X |λ_EX| ≲ C
  (iii) per-channel screening only — does NOT bound the sum:
       |λ_EX| ≲ C
       (two portals each at 0.9 C already sum to 1.8 C)

N_X is the field multiplicity under the §1 normalization (h = 1 real
fluctuation as written; a full SU(2) doublet would count 4).
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

*e4 — the physical-Higgs scale check (erratum 7).* The benchmarks above
are **low-energy EFT statements** (cutoffs at the eV scale, where the
model's parameters are defined). The note identifies h as the Higgs
fluctuation, so the honest scale question is: what happens at
m_h = 125 GeV? Naive extrapolation of the induced λ_EH to the weak
scale — outside the EFT domain, shown for scale only, *not* a matched
result — gives

  δm_E² ~ λ_EH m_h²/(16π²) ~ 5.4×10⁹ eV²   vs  m_E² = 10⁻⁸ eV²
  (ratio ~ 5×10¹⁷; script e4).

Read correctly, this says: **this minimal model does not establish a
natural ultralight scalar coupled to the physical Higgs.** Either the
E-sector description must be matched at the weak scale (a genuine
multiscale loop calculation, in which the low-energy induced couplings
cannot simply be extrapolated upward without double-counting), or h
must be read as a light toy scalar and the Standard-Model claim
narrowed accordingly. **Named standing interpretation (referee
requirement: toy scalar or matching, no third option):** for every
quantitative statement in this note, h is the eV-scale scalar of the
minimal model; the SM-Higgs reading is the open weak-scale matching
problem, not a standing claim. The e1/e2/e3 naturalness conclusions
stand — at their stated eV-scale cutoff.

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

## 5. Boundedness — MATH-03 recovered and generalized (as an EFT-branch condition)

**Labeling (erratum 7).** With positive stabilizing quartics, the full
potential of §1 is bounded at large field values regardless of the
inequality below: quartics grow as t⁴ and the cubic κ_EES₁S₂ only as
t³, so the quartics dominate every ray. The MATH-03 inequality is
therefore **not** a full-potential boundedness condition. It is the
condition on the **E-integrated effective quartic** — the branch where E
sits at the minimum of its quadratic form — which is the corpus's own
derivation setting, and in that sense it is recovered exactly.

Minimizing E (E* = −κ_E S₁S₂/m_E²; the sign enters the induced quartic
only squared) gives the induced negative quartic
−κ_E² S₁²S₂²/(2m_E²). Boundedness of that effective quartic along all
ray directions requires

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
| δg_H (max spurion, λ_1H=λ_2H=1, **leading-insertion**) | 5.9×10⁻¹⁰ eV = 2.95×10⁻¹⁰(λ_1H+λ_2H) | parametric (eq. 5.15) | dual-channel (r6); endpoint uncontrolled, IR prescription needed (r7) |
| δg_H resummed (μ₁₂² = ½m_S², λ=1,1) | 3.24×10⁻¹⁰ eV | — | exact in μ₁₂²; ratio 1.10 vs insertion (r7) |
| g_E linear-E tadpole (max spurion, Λ=1 eV) | 8.7×10⁻¹⁵ eV³ | — | new (self-review r6) |
| naive weak-scale extrapolation of λ_EH (NOT matched) | δm_E² ~ 5.4×10⁹ eV², ratio ~5×10¹⁷ | — | minimal model fails physical-Higgs naturalness (r7) |
| δm_E²/m_E² (κ bubble, Λ=1 eV) | 7.6×10⁻⁸ | — | corrected 2026-09-18 |
| \|λ_E1+λ_E2+λ_EH\| naturalness cap (Λ=1 eV) | 1.58×10⁻⁶ | — | corrected ×2 (r2); two-sided (r4) |
| Σ_X N_X\|λ_EX\| no-cancellation sufficient bound | ≲ same C | — | new (ChatGPT r5) |
| induced tree exchange −κ_E²/m_S² (EFT matching, alternative) | −8.7×10⁻⁹ | — | ChatGPT r2; relabeled r3 |
| induced λ_EH (one-loop triangle) | 2.76×10⁻¹¹·(λ_1H+λ_2H) | — | corrected (ChatGPT r3) |

The corpus's eq. (5.13) pair (κ_E ≲ 10⁻⁶ eV, Ē_S ≲ 2 eV) does not saturate
½m_E²Ē² = ρ_loc; the recomputed saturation values are given above. Both
corpus numbers sit safely inside the window.

## 7. What this closes / what stays open

**Closed here (record-side):**
1. Explicit minimal Z₂_h-even renormalizable closure (§1, scoped by
   erratum 7 — not the general symmetry-allowed model) — the "full
   hidden-sector model" item of Ch. 4, at minimal-model level.
2. All-orders selection rule against E|H|² (Lemma 1′, §2; robust to the
   omitted even terms).
3. Explicit one-loop coefficients for δm_S², the spurion-induced portal
   (dual-channel, leading-insertion at maximal mixing with exact
   resummation away from the endpoint), and the corrected E-mass
   naturalness analysis (§3e: κ bubble log-only; E²X² portal tadpoles
   λΛ²/16π² as the quadratic constraint, three labeled statements;
   induced tree-exchange floor −κ_E²/m_S² (EFT matching) and the
   closed-form one-loop λ_EH triangle, all orders below the cap; §3e4:
   no naturalness claim at the physical Higgs scale) — the "loop or
   spurion calculation" item.
4. Vacuum-alignment analysis with the v₂ critical value (§4) — the
   "vacuum alignment" item.
5. MATH-03 recovered exactly (as the E-integrated effective-quartic
   condition, erratum 7) and generalized to the three-field system (§5).

**Still open (unchanged, corpus-stated):**
- The global nonlinear retarded source PDE (□ + m_E²)E + λ_EE³ =
  κ_EO_h[S_a] with realistic profiles and S-sector feedback (Ch. 4): local
  control only.
- Nonperturbative vacuum structure of the full three-field potential.
- GKSL-side bare-rate naturalness prior (corpus eq. 5.7) — out of scope here.

*Prepared as part of the MQGT-SCF verification program. Record-side;
no play-side content. All numbers reproduce via `mqgt_sequestering_loops.py`.*
