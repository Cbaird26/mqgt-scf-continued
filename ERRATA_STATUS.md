# Errata Disposition — September 2026 Verification (E1–E13)

Source of record: `MQGT_SCF_ERRATA_2026-09-17.md` (v4) in
[`mqgt-scf-independent-verification`](https://github.com/Cbaird26/mqgt-scf-independent-verification).

## Applied in this repository (MQGT-SCF side)

| ID | Claim | Repair applied here |
|---|---|---|
| E1 | UV completion wording | Documentation now states: two non-perturbative NGFPs exist alongside the perturbative result; "matter sector Gaussian at joint FP" retained with that qualifier. |
| E2 | Neutrino portal texture | `neutrino_portal_v2.py`: single-Yukawa texture replaced by the exactly-solvable 3-Yukawa texture. **Variant A is the default** (sum rule Σm_ν = 0.05928 eV preserved; span 104×); Variant B selectable (span 5.8×, Σm_ν = 0.0720 eV). The phrase "exact match" is retired in favor of "reproduces the normal-ordering spectrum with a fitted Yukawa scale and a texture." |
| E3 | T-3 constants | Constants now cited with their correct identifications: S7 = ½ζ′(0) of coexact 3-forms on S⁷ = 1.74845220445; S7′ = −ζ′(0) of coexact 2-forms on S⁹ = 0.41364465819. Confirmed by a third independent method. |
| E5 | (minor) | Cosmetic/wording items folded into documentation. |

## Open (MQGT-SCF side)

| ID | Claim | Status |
|---|---|---|
| E4 | T-1 α⁻¹ gate (residual 6.08×10⁻⁷) | **Open by design.** Fitted corrections are uncertifiable (58 pre-declared gate-passing coincidences); a structural derivation is required. Research run 2026-09-18: target pinned to c₃ = −1.56371823031276 on the α³ basis, QED-running hypothesis excluded numerically, resolution standard set — see `E4_ALPHA_GATE_RESEARCH_NOTE.md` + `mqgt_t1_e4_structure.py`. Derivation attempt round 1 (`mqgt_t1_e4_derivation.py`, `E4_DERIVATION_NOTE.md`): correction is NOT any existing spectral invariant (M1/M3 excluded numerically); Derivation attempt round 2 (`mqgt_t1_e4_a4_heat.py`, `E4_FINAL_STATUS.md`): a₄(E) is degree-2 in the shift, so a₄'''(0) ≡ a₄''''(0) ≡ 0 — the corpus's a₄ path is vacuous. Exclusion record complete: fits, running, existing invariants, heat kernel. T-1 identity stands as a 7-digit approximation; c₃ = −1.56371823031276 remains the pinned target. |

## Notes for the TUFT upstream (Nielsen) — documented, not applied here

These concern TUFT v5 materials and are the upstream author's to adjudicate;
recorded collegially in the errata document:

| ID | Item | Note |
|---|---|---|
| E6 | g−2 α-dependence caveat | All printed values and σ-pulls reproduce under the theory's own α; residual is structural to leading order. |
| E7 | Charged-lepton sector | Public code fits Λ₃ to m_e and misses m_μ at 10.8σ; a one-line normalization repair is proposed in the errata. |
| E9 | Boson sector | Resolved at source: missing factor identified as e^{−α/4π} in the author's own code. |
| E10 | CKM/PMNS | θ₁₂, θ₁₃ (CKM) verified; |Vub| bounded, not predicted (F ≈ 0.40); PMNS ratio Δm²₃₁/Δm²₂₁ = 32.84 ✓, angles not yet predicted. |

## Machine-checked

E13: 6/6 Lean 4.34.0 kernels verify axiom-clean (see verification repo,
`tuft_verify_fixed.lean`). The Lean scope covers the forcing chain, not the
spectral numerics.
