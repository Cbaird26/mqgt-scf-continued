# Lemma 6(d) Computation — Round 15 Result (2026-09-19)

**Authorized:** ChatGPT round-15 authorization + Grok audit charter
(`artifacts/EM_NORMALIZATION_AUDIT_CHARTER_2026-09-19.md`).
**Question:** can TUFT v5's Lemma 6 condition (d) — "a equals the
coupling constant of the n = 0 (massless) sector of the partition
function" — be *derived* from the written U(1) action, rather than
asserted? The EM-normalization audit (`artifacts/
EM_NORMALIZATION_EVIDENCE_MAP_2026-09-19.md`) located the T-1 bridge's
seam at exactly this condition.
**Lab:** `supporting_analysis/mqgt_lemma6d_lab.py` (one command;
output archived at `supporting_analysis/mqgt_lemma6d_lab_out.txt`).
**Answer: no — certified negative, with the boundary of the negative
stated.** The identification stands as an identification.

## What was verified along the way (positive content)

1. **Theorem 48's formula reading.** The PDF text layer garbles the
   fraction structure; the arithmetically consistent reading is
   α = 2 Vol(S²)·(Vol(S⁹)/160)^{1/4} / (Vol(S⁴)²·Vol(RP¹)), which
   matches the record's exact form (8/9)·1920^{1/4}·π^{11/4} with
   difference 0.0 at dps=80.
2. **TUFT's sector machinery is exactly right where it claims to be.**
   ζ′₁(0) = ζ′_R(−2) − ζ′_R(0) = −ζ(3)/(4π²) + ½ ln(2π)
   = 0.8884900761462794710000782 reproduced two independent ways
   (mpmath Hurwitz differentiation vs the closed form; match < 1e-60);
   the sector sum-rule ζ′_n(0) = ζ′₁(0) + Σ_{j<n} j(j+2) ln(j+1)
   reproduced at n = 2, 3 (< 1e-40). The helicity coefficient
   a = 6√2·exp(ζ(3)/(24π²)) = 8.528451441011 matches p60's 8.5284.

## What the computation showed

3. **The n = 0 sector contains no coupling.** In the written ladder
   assembly (TUFT §4.16, eq. 77/83) every n = 0 factor is identically
   1 (multiplicity, helicity, Casimir, ϕ₀ = e^{0·α/6}). α enters
   sectors n ≥ 1 as an *input* (ϕ_n = e^{nα/6}, p61 eq. 75–76), never
   as an output. The lens-space sector map ℓ_min(n) = n degenerates at
   n = 0 (same full spectrum as n = 1): "n = 0" is ladder language, not
   a distinct spectral sector of the written quadratic action.
4. **The Gaussian U(1) partition function on unit S⁹**,
   S = (1/2g²)∫F∧⋆F, Z ∝ [det′(Δ₁ce/g²)]^{−1/2}[det′(Δ₀/g²)]^{+1}:
   via det′(cA) = c^{ζ(0)} det′A and the record's ζ(0) theorem
   (ζ_ce1(0) = +1; ζ₀(0) = 0 conv A / −1 conv B — all three values
   reproduced live at dps=80), **Z₀ ∝ g^{+1} (A) or g^{+3} (B)** — a
   free power of g in either convention. Determinant content at g = 1:
   ln Z₀ = −½L_ce1 + L_scal = 3.81018529220831 (A) /
   0.0153443232731244 (B) — pure geometry, no dimensionless-coupling
   slot. Field redefinition A′ = A/g removes g from the Gaussian
   entirely; g survives only in the charge normalization and the
   measure, neither of which is written. b₁(S⁹) = b₂(S⁹) = 0: no
   harmonic modes, no flux lattice, no θ-sector. The c₁ = 1 flux lives
   on the CP⁴ base and fixes the integer (charge quantization,
   Theorem 47), not the coupling.
5. **The metric/KK route** (Hopf connection as photon): ds² = π*ĝ +
   ρ²η⊗η gives 1/g₄² = 2πρ³/κ₉² (unit-normalized connection; prefactor
   convention-dependent) — needs ρ *and* κ₉, both unfixed by any
   written principle. Same structural hole as the record's round-12b
   illustration.

## Verdict

Lemma 6(d) is **not derivable from the written U(1) action** by any
path examined: (i) the quadratic Beltrami action on S³ carries unit
coefficient — no coupling exists in it; (ii) the S⁵ shell action
carries an explicit free 1/g²_s; (iii) the S⁹ Gaussian Z₀ carries g as
a free power and is g-removable by field redefinition; (iv) the metric
route needs ρ and κ₉; (v) the n = 0 sector is the ladder's
normalization origin. Theorem 48's ratio is nowhere an *output* of the
written partition functions; the uniqueness lemma's condition (d) has
no computed object to attach to. The identification is certified as
**asserted, not derived** — consistent with the source's own header
("Derived, with one physical identification marked below").

**Boundary:** this certifies that the *written* actions contain no
coupling-fixing computation. It does not prove no derivation exists.
One would require a written action whose U(1) kinetic coefficient is a
computed geometric number, or a measure/zero-mode argument on a
manifold with the relevant harmonic structure. Neither exists in the
corpus or TUFT v5 as scanned.

**Consequence for the record:** T-1's status is unchanged but
sharpened — the six-digit conjecture's load-bearing step is now named
and computed against: Lemma 6(d), an identification, X6-category, at
the exact point where the bridge carries weight. Any future claim of
an eight-digit derivation must pass through this point with a
computation, not an identification.

## Reproducibility repair folded into this round

`mqgt_t1_e4_derivation.py` (record script, cited in Appendix A evidence
commands) imported `mqgt_t3_reverse_search`, which was **absent from
the repo** — a fresh clone could not run it (ModuleNotFoundError,
confirmed). The module (the T-3 reverse-search machinery, already the
record's own) was copied in from the workspace verbatim;
`python3 mqgt_t1_e4_derivation.py` now runs clean from a clone, with
E3 sanity checks passing (S7/S7′ to 14 digits, ζ(0) = ±1). Disclosed
per the maintenance rule.
