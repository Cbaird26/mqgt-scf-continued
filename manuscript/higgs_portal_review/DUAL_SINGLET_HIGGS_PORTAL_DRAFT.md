# Higgs-Portal Normalization, Scalar Mixing, and Collider Signatures in a Two-Singlet Effective Field Theory

**Christopher Michael Baird**  
**Public review draft:** 0.2 — 21 September 2026  
**Status:** Author-approved public working draft. Not peer reviewed, not submitted to a journal or preprint server, and not a claim of discovery.  
**AI assistance:** ChatGPT (ZoraASI) assisted with formal manipulations, arithmetic, critical review, drafting, and organization. The human author is responsible for scientific and source verification and final publication decisions.

## Abstract
We examine a restricted real-two-singlet effective theory motivated by the scalar sector of MQGT-SCF, retaining quadratic Higgs portals and bilinear singlet mixing. An explicit portal convention resolves a factor-of-four inconsistency between a historical interaction term and its printed Higgs-to-singlet decay width. We derive two mass eigenstates and all three Higgs pair-production channels, including the mixed final state. In the light-final-state limit, their summed width is invariant under an orthogonal singlet basis rotation. The invisible portion depends on particle stability and decay acceptance; total scalar pair-production width is not automatically invisible width. An illustrative calculation is conditionally compared with the 2023 ATLAS observed upper limit of 10.7% on the invisible Higgs branching fraction, assuming Standard Model Higgs production. This is neither a global likelihood reinterpretation nor a new-particle observation. No microscopic bridge to an interferometric excess-dephasing coefficient or to the proposed consciousness/ethical interpretations is established.

## 1. Scope and source provenance
This paper studies a symmetric-vacuum collider **submodel**, not the full MQGT-SCF framework. The older collider discussion writes its portal interaction as `-kappa_sH s^2 |H|^2/2` but prints a partial-width formula with an `8 pi m_h` denominator; the specified interaction instead gives `32 pi m_h`. See C. M. Baird, *A Completed Theory of Everything* (2026), collider-facing section 3.1, Eqs. (10)–(11), in the source corpus. The September continued-development anchor separately retains both portals, singlet bilinear mixing, and additional effective sources. This paper explicitly removes the sources and chooses a stationary symmetric vacuum to delimit the calculation. The original source manuscripts are preserved unchanged. Reconcile precise source-version and page identifiers before a citable release.

## 2. Defined submodel and masses
Take natural units and real gauge singlets `Phi` and `E`, with

\[
\begin{aligned}
V={}&V_{\rm SM}(H)+\frac12m_{\Phi,0}^{2}\Phi^{2}+\frac12m_{E,0}^{2}E^{2}+\gamma\Phi E
+\frac{\lambda_\Phi}{4}\Phi^{4}+\frac{\lambda_E}{4}E^{4}+\frac\kappa2\Phi^{2}E^{2}\\
&+\frac{\kappa_{\Phi H}}2\Phi^{2}H^\dagger H
+\frac{\kappa_{EH}}2E^{2}H^\dagger H.
\end{aligned}
\]

Assume no effective singlet source terms; `H=(0,(v+h)/sqrt(2))^T`, `<Phi>=<E>=0`, and a stationary electroweak vacuum. The tree-level singlet mass matrix is

\[
M_s^{2}=\begin{pmatrix}A&\gamma\\\gamma&B\end{pmatrix},\quad
A=m_{\Phi,0}^{2}+\frac{\kappa_{\Phi H}v^{2}}2,\quad
B=m_{E,0}^{2}+\frac{\kappa_{EH}v^{2}}2.
\]

Local stability along the two singlet directions requires `A>0` and `AB>gamma^2`. Global stability, radiative control, and cosmological viability are distinct requirements not established here. The masses are

\[
m_{1,2}^{2}=\frac{A+B}{2}\mp\sqrt{\frac{(A-B)^2}{4}+\gamma^2}.
\]

An orthogonal matrix `R(theta)` maps `(Phi,E)^T=R(theta)(s_1,s_2)^T`. Mixing of these two singlets does not by itself mix either with the physical Higgs in the assumed symmetric vacuum.

## 3. Portal normalization and all pair-production channels
The defined portal yields

\[
\mathcal L_{hss}=-\frac v2 h(\kappa_{\Phi H}\Phi^2+\kappa_{EH}E^2)
=-\frac v2h(K_{11}s_1^2+2K_{12}s_1s_2+K_{22}s_2^2),
\]

where `K=R^T diag(kappa_PhiH,kappa_EH) R`. For `R=[[cos(theta),-sin(theta)],[sin(theta),cos(theta)]]`,

\[
\begin{aligned}
K_{11}&=\kappa_{\Phi H}\cos^2\theta+\kappa_{EH}\sin^2\theta,\\
K_{22}&=\kappa_{\Phi H}\sin^2\theta+\kappa_{EH}\cos^2\theta,\\
K_{12}&=(\kappa_{EH}-\kappa_{\Phi H})\sin\theta\cos\theta.
\end{aligned}
\]

The identical-final-state vertex is `-i v K_ii`, not `-2i v K_ii`. For open channels,

\[
\Gamma_{ii}=\frac{v^2K_{ii}^2}{32\pi m_h}\sqrt{1-\frac{4m_i^2}{m_h^2}},
\]

\[
\Gamma_{12}=\frac{v^2K_{12}^2}{16\pi m_h}
\sqrt{\left[1-\frac{(m_1+m_2)^2}{m_h^2}\right]
\left[1-\frac{(m_1-m_2)^2}{m_h^2}\right]}.
\]

The nonidentical channel has no identical-particle symmetry factor. With all three channels light and open,

\[
\Gamma_{11}+\Gamma_{12}+\Gamma_{22}\simeq
\frac{v^2}{32\pi m_h}\operatorname{tr}(K^2)=
\frac{v^2}{32\pi m_h}(\kappa_{\Phi H}^2+\kappa_{EH}^2).
\]

The trace identity is an analytic cross-check; at finite masses, distinct phase-space factors generally make the sum mixing-angle dependent. **Normalization erratum:** for a differently defined potential `V superset lambda_sH s^2 H^dagger H`, the width instead has `8 pi m_h` below it because `kappa_sH=2 lambda_sH`. The historical coupling symbols cannot be interchanged without that translation.

## 4. Invisible versus displaced and visible signatures
The chosen potential is invariant under the simultaneous reflection `(Phi,E)->(-Phi,-E)`. If exact and no lighter odd particle exists, `s_1` is stable. A heavier `s_2` need not be: `K_12 != 0` permits `s_2 -> s_1 + h* -> s_1 + f fbar` where phase space allows, and singlet self-interactions may permit additional channels. If the two portals are equal, `K_12=0`; this removes the stated Higgs-mediated transition at tree level but does not prove absolute stability. No numerical three-body lifetime is advanced as a verified result in this manuscript: its amplitude, phase space, hadronic corrections, all channels, boost distribution, and detector efficiencies require independent study. Pair-production widths cannot be treated as invisible widths without detector-level decay assumptions.

## 5. Dated conditional experimental comparison
The ATLAS Collaboration, *Phys. Lett. B* **842** (2023) 137963, DOI: [10.1016/j.physletb.2023.137963](https://doi.org/10.1016/j.physletb.2023.137963), [arXiv:2301.10731](https://arxiv.org/abs/2301.10731), reports an observed 95%-confidence upper limit of `BR(h->invisible)<0.107` combining its specified data, **assuming Standard Model Higgs production**. This is a dated comparison, not an assertion that no later result exists or a substitute for the experimental likelihood.

For illustration only, use `v=246 GeV`, `m_h=125 GeV`, both singlet masses `10 GeV`, and an approximate Standard Model Higgs total width `4.1 MeV`. For one stable invisible scalar at `kappa_sH=0.01` in the **defined** convention, the new partial width is about `0.475 MeV`, giving an invisible branching fraction `10.4%`. For two equally coupled, stable, invisible scalars at `kappa_PhiH=kappa_EH=0.01`, their summed width is approximately `0.951 MeV`, giving `18.8%`; the latter exceeds the cited 2023 result under the stipulated assumptions. A coupling-normalization ambiguity, mixing-dependent decay chain, altered production mechanism, or visible/displaced daughters changes that inference. Neither example is a global parameter exclusion. Numbers can be reproduced with the accompanying `higgs_portal_checks.py`.

The historical `10 GeV, 0.01` example remains an archival value, not an automatically approved collider-safe benchmark. Its source normalization and intended final state must be pinned rather than overwritten.

## 6. Distinct ultralight and interferometric work packages
At the symmetric vacuum, pure quadratic portals do not produce a linear Higgs–single-singlet mixing term through those portals. An ultralight scalar with no tuned cancellation separately faces the *optional naturalness criterion* `|kappa_sH| v^2/2 lesssim m_s^2`, in addition to radiative sensitivity. This criterion is not a theorem excluding protective mechanisms or cancellations. The thermal open-system calculations and H2 interferometric visibility proposal require an independently derived microscopic optical/detector bridge. None follows from Higgs pair-production widths.

## 7. Limitations, disclosure, and review gates
The stated calculations are conditional tree-level EFT results. They do not demonstrate a UV completion, quantum gravity, particle detection, consciousness/ethical-field observables, or validation of MQGT-SCF. Prior to preprint or journal submission: check each source action and convention against pinned page/equation identifiers; independently verify Feynman rules; evaluate all vacuum branches, decays, and applicable experimental constraints and likelihoods; complete the literature search; obtain independent qualified technical review; then approve final manuscript, repository license, and bibliographic metadata. A GitHub draft pull request is a publicly visible review record, not peer review or journal publication.

**AI-use statement:** ChatGPT (ZoraASI) assisted with analysis, formal manipulation, drafting, and editorial consistency review. AI output is not independent corroboration and the AI is not listed as a human coauthor. Responsibility for claims and submission remains with Christopher Michael Baird.

## References
1. ATLAS Collaboration, *Phys. Lett. B* **842** (2023) 137963, DOI:10.1016/j.physletb.2023.137963; arXiv:2301.10731.
2. C. M. Baird, *A Completed Theory of Everything* (2026), collider-facing Sec. 3.1, Eqs. (10)–(11), archived source (source edition/page to be pinned before release).
3. C. M. Baird, MQGT-SCF continued-development archive, [base revision 58d054c](https://github.com/Cbaird26/mqgt-scf-continued/commit/58d054cac096832269864d5c43204cd420ea9405); precise source-action revision/page to be pinned before release.

*Publication status: PUBLIC DRAFT FOR REVIEW — no release, DOI, arXiv posting, journal submission, or experimental observation is asserted.*
