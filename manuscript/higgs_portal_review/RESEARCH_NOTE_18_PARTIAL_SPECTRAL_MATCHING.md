# Research Note 18 — A source-audited partial hadronic bound, without an invented total width

**21 September 2026 | Scientific development draft, not peer reviewed.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with literature identification, methodological audit, algebra and writing. This note extends the *restricted*, symmetric-vacuum, zero-source, common-Z2 two-singlet companion EFT and preserves the distinction from the full MQGT-SCF action. The labels Phi_c and E are hypothetical field names, not established measurements of consciousness or ethics.

## 1. Concrete candidate for part of the missing QCD input

Blackstone, Tarrús Castellà, Passemar and Zupan, *Hadronic Decays of a Higgs-mixed Scalar* (arXiv:2407.13587, 2024), describe dispersive light-hadron scalar form factors with uncertainty estimates and provide the public **hipsofcobra** code. Its repository is https://github.com/blackstonep/hipsofcobra, fixed here at commit `6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7` (package `0.0.8`, GPL-3.0). Its `setup.py` describes pion and kaon final states; `HipsofCobra` in `hipsofcobra/classes.py` accepts `Pname='pi'` or `Pname='K'`, generates form factors and reports widths through `G_to_width`. These facts make the package **a candidate for exclusive pion-pair and kaon-pair partial widths**, not a verified absolute inclusive hadronic width throughout the 0–15 GeV virtual-Higgs mass range. The implementation uses external Omnès input files and stochastic samples. No third-party code or data are copied here.

Other methodological sources for review are HDECAY (Djouadi et al., *HDECAY: Twenty++ years after*, Comput. Phys. Commun. 238, 214–231 (2019), https://doi.org/10.1016/j.cpc.2018.12.010) and Winkler, *Decay and detection of a light scalar boson mixing with the Higgs boson*, Phys. Rev. D 99, 015018 (2019), https://doi.org/10.1103/PhysRevD.99.015018. Neither HDECAY nor a hadronic form-factor table has been run, imported, or validated for this benchmark. The candidate code does **not** by itself close our total-width calculation.

## 2. The normalization/exclusivity gate

The required source-normalized spectrum is the **absolute** partial width of a virtual scalar of mass M=sqrt(s) with *unit Standard Model Higgs-current strength*. If a reference computes a Higgs-mixed scalar whose entire relevant amplitude scales linearly with epsilon, the unit-normalized width equals Gamma(S->X;epsilon)/epsilon². First verify the convention, full amplitude, valid mass domain, and that the parameter is indeed epsilon. A branching fraction alone lacks absolute normalization.

For one exclusive final state X, Gamma_X is proportional to |A_light,X + A_gluonic,X + A_heavy,X|². Do **not** add individually squared light-quark, gluon and heavy-quark width labels for the same X; matched amplitudes may interfere. After matching, *distinct physical final states* (e.g. pi pi, K K-bar, and charged leptons) have nonnegative widths and can be summed. Do not also add exclusive channels to an inclusive continuum that already includes them, or count a quarkonium resonance both as a separate final state and among the hadrons into which it decays.

## 3. New conditional result: partial coverage can tighten the decay-length ceiling

For the illustrative masses m1=10 GeV, m2=25 GeV, |K12|=0.001, the virtuality spans 0 <= s <= 225 GeV². With lambda(a,b,c)=(a-b-c)²-4bc define the nonnegative kernel

W(s) = v² K12² sqrt[lambda(m2²,m1²,s)] sqrt(s) / {16 pi² m2³ [(mh²-s)² + mh² Gammah²]}.

For any independently justified set C of disjoint hadronic final states and valid mass domains I_X, define

Gamma_C = sum_(X in C) integral_(I_X) ds W(s) Gamma_unit(h*->X;sqrt(s)) >= 0.

If additional amplitudes do not alter the stated partial widths and remaining *physical-final-state* widths are nonnegative, then

**Gamma_total >= Gamma_leptons + Gamma_C, and c*tau_total <= hbar*c/(Gamma_leptons + Gamma_C).**

This works even without an inclusive 0–15 GeV QCD spectrum. A verified pi-pi and K-Kbar calculation could thus tighten the preceding leptons-only conditional c*tau <= approximately 17.06 cm. **We have not run or normalized the upstream code: no Gamma_C, improved numerical lifetime, or full lifetime is claimed.** A lower bound on c*tau also needs an upper bound for *all* significant channels or an independently justified inclusive upper envelope. A mean +/- one-sigma uncertainty band is not automatically a rigorous pointwise bound; the inspected upstream implementation transforms the sampled absolute-form-factor mean +/- standard deviation into width curves, which must be statistically calibrated before any certification claim.

## 4. Reproducible, security-conscious acquisition and publication gate

Pin source commit and input hashes; review upstream license and data provenance; verify mass-grid coverage and exclusive/inclusive channels; map its coupling vector `clist` to the unit-SM-Higgs-current convention; fix a random seed and record convergence when sampling; propagate physical and numerical uncertainty; record uncovered s-intervals. Inspected upstream `classes.py` loads external text through `eval(file.read())`: **do not run this on untrusted/modified inputs** without a safe audited parser. Keep the upstream GPL attribution and do not vendor its sources into this manuscript.

`test_research_note_18.py` checks kernel positivity and partial-spectrum inequalities using **synthetic spectra only**. It does not execute hipsofcobra/HDECAY, compute QCD, assess a real detector or verify the fields.

**Stop condition:** No numerical hadronic central width, total lifetime, displaced fraction, exclusion, or consciousness/ethics interpretation until amplitude normalization, final-state inventory, valid mass range, uncertainties and detector response have been independently checked.

Primary references: https://arxiv.org/abs/2407.13587 ; https://github.com/blackstonep/hipsofcobra/tree/6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7 ; https://doi.org/10.1016/j.cpc.2018.12.010 ; https://doi.org/10.1103/PhysRevD.99.015018.