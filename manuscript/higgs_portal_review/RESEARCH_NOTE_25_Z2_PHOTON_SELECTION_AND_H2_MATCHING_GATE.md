# Research Note 25 — Exact common-Z₂ photon selection rule and the H2 matching gate

**21 September 2026 | Author-approved public *development* draft, not peer reviewed.** Christopher Michael Baird is the human author. ChatGPT (ZoraASI) assisted with the conditional symmetry argument, source-level matching, algebra tests and drafting. These are mathematical statements about the restricted symmetric-vacuum, zero-source two-singlet EFT of the dated working paper, **not** observations of consciousness, ethics, a new particle, an H2 signal or an established theory of everything.

## 1. A separate route while the four hadronic files are missing

Notes 19–24 cannot obtain the heavier singlet's complete width without authenticated Omnès inputs and a nonoverlapping inclusive/exclusive channel inventory. The H2/photon interface is a logically different question that can be clarified without those files. The comprehensive working paper, Secs. 2, 6, 8–9, states that the minimal quadratic Higgs portals at the exact symmetric singlet vacuum do not supply a single-scalar photon mixing term or a microscopic H2 visibility coefficient. Here we strengthen the **selection-rule** portion, under an explicitly exact common Z₂.

The restricted potential is invariant under `(Phi,E)->(-Phi,-E)`, with the SM Higgs, photons, and a prescribed electromagnetic background even. After orthogonal mass rotation both `s1` and `s2` are odd. With an unbroken symmetry and an even vacuum, the S matrix commutes with the parity operator `P`. If `|i>` and `|f>` have opposite common-Z₂ parities,

`<f|S|i> = <f|P^{-1} S P|i> = (P_f P_i)<f|S|i> = -<f|S|i> = 0`.

Consequently **a photon or any photon-only, even initial state cannot produce exactly one odd singlet in the final state in this restricted theory**, to any order in interactions that preserve the symmetry. Adding an ordinary classical magnetic/electric background does not by itself break the singlet parity. Specifically, an operator `s_i F_{mu nu}F^{mu nu}` and an `h s_i` bilinear are odd and forbidden in the symmetric branch. The mixed mass term `gamma Phi E`, the `h s1 s2` vertex, and `s_i s_j F²` are even and allowed. This *does not* forbid producing two odd singlets, transitions between odd singlets in an odd-sector initial state, or every possible effect on photon propagation.

**Scope caveat:** This is a conditional selection theorem, not a universal no-go for the larger archive. A nonzero odd singlet condensate, an odd external source, a new parity-violating interaction, or a different chosen vacuum can invalidate the premise; each requires a declared action and rederived stationary background. An electromagnetic field is even under this **internal** common-Z₂ and is not enough on its own.

## 2. An allowed photon–two-singlet operator, with its normalization exposed

The mass-basis Higgs portal in the existing notes is

`L ⊃ -(v/2) h (K11 s1² + 2 K12 s1 s2 + K22 s2²)`.

**Conditionally** introduce the SM loop-induced virtual-Higgs two-photon interaction in the convention

`L ⊃ [C_gamma(q²)/(4v)] h F_{mu nu}F^{mu nu}`.

`C_gamma` is a dimensionless, unspecified matching coefficient that includes the relevant electroweak/charged-state dynamics. This note **does not** calculate it, treat it as a universal constant, or assert source-form-factor precision. At low momentum relative to the Higgs mass, let `B=(K11 s1²+2K12 s1 s2+K22 s2²)/2`. To leading order in derivatives, the h-dependent terms are

`L_h ≃ -(mh²/2)h² + h J`, `J = C_gamma F²/(4v) - v B`.

The classical stationary solution `h=J/mh²` yields `L_eff ⊃ J²/(2mh²)`, with the photon–singlet cross term

`L_eff ⊃ -[C_gamma/(8 mh²)](K11 s1²+2 K12 s1 s2+K22 s2²)F_{mu nu}F^{mu nu}`.

In particular the mixed coefficient in the stated convention is `-C_gamma K12/(4 mh²)`, **not** `-C_gamma K12/(8 mh²)`. There is no linear `s1 F²` or `s2 F²` term. This is formal low-energy matching of the specified vertices, not a complete one-loop EFT calculation: momentum dependence, form factors, further operators, and any off-shell propagator effects require a dedicated computation. The coefficient is **not an H2 dephasing rate**.

The allowed mixed coupling suggests the *symmetry-allowed* decay `s2 -> s1 + gamma gamma` when `m2>m1` and an off-shell Higgs to two photons is correctly matched. This channel is **not calculated**, need not dominate, and belongs in the still-open nonoverlapping total-width inventory of Notes 22–24. A gamma-only initial state could in principle produce an *even* pair of odd singlets when energy/kinematics and actual amplitudes allow it; this is categorically different from a single-scalar conversion claim.

## 3. Consequence for the H2 optical interpretation

The archived H2 regression `V/V0=exp[-Gamma_H2 T (Delta x)²]` is currently an **instrument-level model**. Neither the pair operator above nor the known production widths determines `Gamma_H2`: doing so needs a specified interferometer system coupling, quantum/thermal state of the singlet sector, applicable spectral/influence-functional correlator, momentum transfer, physical path geometry, acquisition and nuisance model. An even vacuum need not supply accessible on-shell pair production at arbitrary optical frequency; virtual and finite-time effects, matter interactions, noise and boundaries require separate accounting. The working paper's earlier stationary free-gapped-bath caveat also remains.

For the compressed benchmark (`m1=10 GeV`, `m2=11.5 GeV`), single-photon **single-singlet** conversion is forbidden under the exact common-Z₂, while an even-sector two-singlet amplitude is not symmetry-forbidden. **No optical cross section, phase shift, coherence loss, photon decay, total heavy-state lifetime, or portal exclusion has been deduced here.** The illustrative Higgs pair branching fractions and the previous leptonic-only `c*tau2 <= ~645 km` bound remain conditional and unchanged; the missing hadronic input remains missing.

## 4. Reproducibility and a falsifiable model-choice gate

`photon_selection_rules.py` implements only parity classification and algebraic source elimination, using rational arithmetic in its tests. `test_research_note_25.py` checks the forbidden odd monomials and allowed even pairs, the exact stationary h substitution, the mixed-vertex factor of two, and input failures. **Eleven local algebra/regression tests passed; they are not an independent quantum-field-theory calculation or empirical test.** `C_gamma` and every experimental response remain symbolic.

**Before assigning an H2 photon signal to these fields:** (1) choose and document whether the exact common-Z₂ symmetric branch is actually used; (2) if proposing *single*-scalar photon mixing, identify the precise parity-breaking source/background/operator and rederive the vacuum and interaction; (3) if staying symmetric, derive the applicable **even-sector** photon–pair/matter amplitude and its environmental spectrum, including thresholds; (4) propagate it into the actual interferometer visibility estimator and controls; (5) separately evaluate laboratory/collider constraints with dated primary sources. This logic is independent of, and does not remove, the four missing hadronic-grid files.

**Lineage:** `COMPREHENSIVE_WORKING_PAPER_2026-09-21.md` (Secs. 2, 6, 8, 9), `DUAL_SINGLET_HIGGS_PORTAL_DRAFT.md`, Notes 15 and 22–24 in the same review branch. No external papers' physics results are newly asserted, and no third-party source data or code are redistributed.