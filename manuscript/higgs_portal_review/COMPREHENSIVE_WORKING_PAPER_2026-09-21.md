# A Two-Singlet Effective Theory and Its Experimental Interfaces: A Conditional Consistency Audit of the MQGT-SCF Program

**Christopher Michael Baird**  
**Working paper v0.2 — 21 September 2026**  
**Status:** Public technical-review draft; not peer reviewed, journal-submitted, a new DOI, or an experimental discovery.  
**AI-assistance disclosure:** ChatGPT in the ZoraASI project persona assisted with derivations, drafting, critical checks, and implementation. The human author is responsible for the claims, references and eventual submission. AI assistance is not independent replication.

## Abstract

We audit a restricted two-real-singlet effective field theory drawn from the MQGT-SCF research corpus and distinguish its collider, photon, open-system and H2 interferometric interfaces. Fixing the quadratic Higgs-portal convention, we calculate the singlet mass eigenstates and all three Higgs pair-production channels, including a mixed channel. We identify a factor-of-four normalization issue in a historical decay-width expression and derive a mixing-invariant total-width identity in the light-mass limit. Illustrative collider branching fractions are compared conditionally with a dated 2023 ATLAS result, not a contemporary global exclusion. We explain why a symmetric-vacuum quadratic portal does not provide a single-scalar photon coupling, why a gapped stationary free-field model does not automatically yield persistent Markovian pure dephasing, and which additional assumptions create a conditional classical noisy-bath rate. The H2 visibility law is presently an instrument-level estimand without a complete microscopic map from the specified portal couplings. No observation of new scalar fields, quantum collapse, or operational consciousness or ethics fields is claimed.

## 1. Scope and source hierarchy

This working paper synthesizes the focused September 2026 Research Notes 01–13 and selected earlier anchor passages, not every equation in the much larger Theory of Everything archive. The archival March anchor describes hypothetical scalar fields conventionally named Φ_c and E, open-system dynamics, optional measure tilts, and an H2 optical protocol. For the physical calculations here, Φ_c and E are simply two hypothetical **real Standard-Model gauge singlets**. Their interpretation as consciousness or ethics has not been operationally established. Distinguish (i) the source's proposed action, (ii) calculations derived after declaring additional assumptions, (iii) illustrative numerical parameters, and (iv) actual external measurements. The source snapshot is [the development repository at commit 58d054c](https://github.com/Cbaird26/mqgt-scf-continued/commit/58d054cac096832269864d5c43204cd420ea9405); the historical verification release remains unchanged.

## 2. A single declared calculation branch

Write Φ = Φ_c and, in natural units, choose

$$
\begin{aligned}
V={}&V_{\rm SM}(H)+\frac12m_{\Phi,0}^2\Phi^2+\frac12m_{E,0}^2E^2+\gamma\Phi E\\
&+\frac{\lambda_\Phi}{4}\Phi^4+\frac{\lambda_E}{4}E^4+\frac\kappa2\Phi^2E^2\\
&+\frac{\kappa_{\Phi H}}2\Phi^2H^\dagger H+\frac{\kappa_{EH}}2E^2H^\dagger H.
\end{aligned}
$$

For collider calculations only, **set effective sources to zero** and select the stationary symmetric singlet vacuum ⟨Φ⟩ = ⟨E⟩ = 0, with H = (0,(v+h)/√2)^T. The scalar bilinear γΦE remains. This branch has a simultaneous reflection (Φ,E) → (−Φ,−E), not generally independent reflections. This is not a statement that all versions of the larger MQGT-SCF program select this vacuum. Singlet-only quartic boundedness is ensured by λ_Φ>0, λ_E>0, κ>−√(λ_Φλ_E); these conditions alone do not settle global three-field vacuum stability.

## 3. Mixing and correctly normalized Higgs widths

The tree-level singlet squared-mass matrix and eigenvalues are

$$
M_s^2=\begin{pmatrix}A&\gamma\\\gamma&B\end{pmatrix},\quad
A=m_{\Phi,0}^2+\frac{\kappa_{\Phi H}v^2}{2},\quad
B=m_{E,0}^2+\frac{\kappa_{EH}v^2}{2},
$$

$$
m_{1,2}^2=\frac{A+B}{2}\mp\sqrt{\frac{(A-B)^2}{4}+\gamma^2}.
$$

A>0 and AB>γ² establish positivity in singlet directions at the chosen stationary vacuum, not full global or radiative stability. With (Φ,E)^T = R(θ)(s₁,s₂)^T, define K = R^T diag(κ_ΦH,κ_EH) R. Using c = cosθ and s = sinθ,

$$
K_{11}=\kappa_{\Phi H}c^2+\kappa_{EH}s^2,\quad
K_{22}=\kappa_{\Phi H}s^2+\kappa_{EH}c^2,\quad
K_{12}=(\kappa_{EH}-\kappa_{\Phi H})sc.
$$

The mass-basis trilinear is

$$
\mathcal L_{hss}=-\frac v2h(K_{11}s_1^2+2K_{12}s_1s_2+K_{22}s_2^2).
$$

For kinematically open channels,

$$
\Gamma(h\to s_is_i)=\frac{v^2K_{ii}^2}{32\pi m_h}\sqrt{1-4m_i^2/m_h^2},
$$

$$
\Gamma(h\to s_1s_2)=\frac{v^2K_{12}^2}{16\pi m_h}
\sqrt{[1-(m_1+m_2)^2/m_h^2][1-(m_1-m_2)^2/m_h^2]}.
$$

The mixed final state has no identical-particle factor. For both masses small compared with m_h and all three channels open,

$$
\Gamma_{11}+\Gamma_{12}+\Gamma_{22}\simeq\frac{v^2}{32\pi m_h}\mathrm{tr}(K^2)
=\frac{v^2(\kappa_{\Phi H}^2+\kappa_{EH}^2)}{32\pi m_h}.
$$

**Archival erratum:** A historical equation using an 8πm_h denominator next to a κ_sH/2 portal differs by a factor of four from the width implied by that interaction. The 8π convention instead belongs to V ⊃ λ_sH s²H†H, with κ_sH=2λ_sH. This paper records the correction and does not overwrite the earlier document.

## 4. Dated collider illustration—not an exclusion scan

With v=246 GeV, m_h=125 GeV, m_s=10 GeV, illustrative SM Higgs width 4.1 MeV, and κ_sH=0.01 **in the convention above**, one stable invisible singlet gives Γ(h→ss)≈0.475 MeV and BR_inv≈10.4%. Two equal invisible channels yield about 18.8% if the corresponding decay chains really escape detection. The [ATLAS 2023 combination, Phys. Lett. B 842, 137963](https://doi.org/10.1016/j.physletb.2023.137963) reports a 95% CL observed invisible-Higgs branching-ratio bound of 10.7%, assuming SM Higgs production. The one-channel illustration lies just below that **particular dated** limit; the two-channel illustration exceeds it under the stated assumptions. This is neither a current comprehensive exclusion nor an allowed parameter region. In the mixed theory s₂ can decay through s₂→s₁h*→s₁f f̄ when the off-diagonal portal and phase space allow it; its invisibility depends on total decay width, branching fractions, boost and detector selection. The numerical three-body lifetime proposed in exploratory Note 13 remains **unverified and excluded** from the certified result set.

## 5. Ultralight mass sensitivity

At the exact symmetric vacuum the tree-level Higgs contribution is Δm_s²=κ_sH v²/2. A separately chosen no-large-cancellation naturalness criterion therefore asks |κ_sH|≲2m_s²/v². The original archive also proposes an approximate cutoff loop estimate |δm_s²|~|κ_sH|Λ²/(16π²), up to scheme- and model-dependent factors. For planning values Λ=1 TeV and m_s=10⁻³ eV, these give illustrative portal ceilings of about 3.3×10⁻²⁹ (tree-level preference) and 1.6×10⁻²⁸ (loop estimate). These **do not mathematically exclude** fine-tuned or symmetry-protected extensions. The ultralight and GeV-scale entries are distinct scenarios, not a jointly fitted benchmark.

## 6. Photon bridge and a symmetry obstruction

Quadratic Higgs portals at the exact symmetric singlet vacuum do not create an h–single-singlet mixing term. A nonzero singlet vacuum value w generates a mass-mixing term of order κ_sH v w, and a mixed eigenstate may then inherit the SM Higgs's loop-induced interaction with photons. That is an **additional vacuum branch** requiring its own stationary solution, scalar mass matrix, loop matching and external constraints. A standalone effective term −g_sγ sF_{μν}F^{μν}/4 yields ∂_μ[(1+g_sγ s)F^{μν}]=0 in vacuum: a constant scalar background by itself does not establish an excess vacuum refractive-index phase. Photon conversion with an external magnetic field is a different proposed observable, not a derivation of the H2 visibility coefficient from the quadratic portal.

## 7. GKSL toy measurement channel

For an independently postulated dephasing toy generator L_j=√r |j⟩⟨j| with r≥0, the Lindblad dissipator preserves trace and complete positivity and gives (dρ_jk/dt)_diss=−rρ_jk for j≠k. Choosing r=r₀exp(ηE) is a **hypothesis**, not a consequence of the scalar action. Complete positivity by itself does not prove relativistic locality or no-signalling for arbitrary nonlocal or state-dependent rules; the archive's no-signalling discussions require their own stated locality assumptions. The unconditioned dephasing toy does not change one-shot Born probabilities. An independent outcome tilt needs its own physical instrument definition and signalling audit.

## 8. Noise spectrum, dephasing and a conditional bath

Assume additionally a localized particle's interaction H_int=g s(x̂,t) and stationary Gaussian field noise. Its long-time Markovian *pure-dephasing* rate samples the zero-frequency **differential** field spectrum. An ideal stationary free massive scalar field has a frequency gap, so it cannot provide the assumed persistent white-noise rate through that linear coupling. This statement does not exclude finite-time, interacting, driven or otherwise non-Markovian effects.

A **different, classical dissipative model** is the postulated mode equation s̈_k+ζṡ_k+(k²+m²)s_k=ξ_k with white bath noise covariance 2ζΘ δ(t−t′). Its specified zero-frequency spectrum is S_s(k,0)=2ζΘ/(k²+m²)². A pointlike two-path coupling yields, in the long-time Gaussian Markov approximation,

$$
\Gamma_{\rm path}(d)=2g^2\zeta\Theta\int\frac{d^3k}{(2\pi)^3}
\frac{1-\cos(\mathbf k\cdot\mathbf d)}{(k^2+m^2)^2}
=\frac{g^2\zeta\Theta}{4\pi m}(1-e^{-md}).
$$

The small-d result is **linear**, not H2's quadratic separation law. A smearing form factor F(k) with convergent ultraviolet moment can instead give a quadratic limit,

$$
\Gamma_{\rm path}(d)=d^2\frac{g^2\zeta\Theta}{3}
\int\frac{d^3k}{(2\pi)^3}\frac{k^2|F(k)|^2}{(k^2+m^2)^2}+O(d^4).
$$

All of these rates are **conditional on an added physical bath and particle coupling**. Neither the classical white bath nor a direct photon coupling is derived from the minimal quadratic-portal action.

## 9. H2 is currently an instrument estimand

The archive proposes V/V₀=exp(−Γ T Δx²), with Q=T Δx² and nuisance-adjusted regression −ln V_jr=a_session+ΓQ_j+X_jr^Tβ+ε_jr. Its illustrative exclusion floor is |ln(1−δ_tot)|/(T Δx²). With T=10⁻⁶ s, Δx=10⁻³ m and δ_tot=1.15×10⁻³, the planning floor is approximately 1.15×10⁹ s⁻¹m⁻². **This is not an achieved hardware sensitivity.** Changes in Q must be disentangled from path length, phase-scanning, temperature, polarization and mechanical nuisance effects; labelled synthetic tests cannot be relabelled experiments. A unique microscopic relation Γ(κ_ΦH,κ_EH,γ,…) has not been established, so an H2 floor cannot yet be converted into a portal exclusion. An optical pilot can characterize the instrument without establishing the proposed scalar fields.

## 10. Status and nonclaims

The conditional tree-level collider widths, rotation identity, and illustrative arithmetic can be reproduced with the accompanying `higgs_portal_checks.py` in this review branch. The broader H2/noisy-bath checks use a separate script and are mathematical unit checks, not data. The three-body lifetime estimate, complete decay inventory, full collider likelihood, fifth-force reinterpretation, cosmological fit and identification of any field with consciousness, ethics or AI qualia remain outside the validated result set. The 13 conversation notes are a **research-development trail**, not 13 separately validated publications. We do not claim a completed theory of everything, a new observed particle or empirical collapse effect.

## 11. Source provenance, authorship, and release gate

The March 2026 anchor is reproduced in the author's uploaded *All + ToE, Part 9* compilation; precise original page/equation and edition mapping remains to be pinned for journal submission. This document supplements, rather than edits, that archive. The source commit is [58d054c](https://github.com/Cbaird26/mqgt-scf-continued/commit/58d054cac096832269864d5c43204cd420ea9405); the related focused collider draft and release-gate ledger are alongside this note. Before promoting this working paper to a citable preprint or journal submission: independently rederive the widths and bath convention, audit the original action and errata, verify stationary/global vacua and complete decays, check updated experimental literature and likelihoods, supply exact archival citations, and obtain human approval of the submitted version. No PDF, DOI or journal acceptance is asserted by this GitHub working-paper commit. OpenAI ChatGPT/ZoraASI contributed drafting and mathematical assistance and is not a human coauthor.

### References

1. C. M. Baird, *MQGT-SCF as a Minimal Scalar-Singlet EFT: Specification-Level Closure, Local GKSL Measurement Dynamics, and an H2 Interferometric Exclusion Observable* (March 2026), within the author's uploaded *All + ToE, Part 9* compilation; original page and publication metadata pending.
2. C. M. Baird, [MQGT-SCF continued development line, source snapshot `58d054c`](https://github.com/Cbaird26/mqgt-scf-continued/commit/58d054cac096832269864d5c43204cd420ea9405) (19 September 2026), development ledger and errata.
3. C. M. Baird, historical collider formulation in the author's compiled archive; normalization discrepancy identified in the companion focused draft, original citation coordinates pending.
4. ATLAS Collaboration, *Combination of searches for invisible decays of the Higgs boson using 139 fb⁻¹ of proton-proton collision data at √s=13 TeV collected with the ATLAS experiment*, **Physics Letters B 842** (2023) 137963, [DOI 10.1016/j.physletb.2023.137963](https://doi.org/10.1016/j.physletb.2023.137963), [arXiv:2301.10731](https://arxiv.org/abs/2301.10731).
5. C. M. Baird, H2 Phase-0 optical protocol and exclusion observable, within *All + ToE, Part 9*; instrument specifications are planning benchmarks.