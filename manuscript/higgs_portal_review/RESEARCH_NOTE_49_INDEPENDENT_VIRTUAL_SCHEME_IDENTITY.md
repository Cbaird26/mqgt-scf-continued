# Research Note 49 — Third-source virtual coefficient and an exact finite-scheme identity

**10 October 2026 research continuation | Scientific-development draft; not peer reviewed.** Prepared for Christopher Michael Baird with ChatGPT (ZoraASI) assistance in source comparison, algebra, implementation and numerical verification. This is a conditional Higgs-portal calculation, not an established Theory of Everything or empirical detection. Execution timestamps are recorded in UTC separately.

## 1. The question tested

Note 48 assembled a candidate bottom/charm-square NLO contribution and found that a finite shift of the virtual numerator, `Delta G=(8/3) D F`, was needed to agree with the separately implemented top–bottom/charm coefficient. That was a meaningful cross-sector check, but it did not independently fix the interpretation of the virtual mass convention. This note tests that interpretation against a **third published calculation**, not another numerical representation of the old coefficient.

The third source is Aglietti, Bonciani, Degrassi and Vicini (ABDV), *Analytic Results for Virtual QCD Corrections to Higgs Production and Decay*, hep-ph/0611266v3 [1]. They explicitly calculated the relevant virtual Feynman diagrams, whereas the Harlander–Kant (HK) representation [2] reorganized an earlier integral result. We implement the ABDV fermion formulas independently of the inherited HK rational expression and the Note-44 mixed coefficient. We do not claim to have recomputed the underlying Feynman diagrams ourselves.

**Result:** the independently transcribed ABDV mass-dependent virtual numerator agrees with Note 48's **matched** numerator, not Note 46's unchanged literal interpretation. More strongly, the two published transcriptions reduce to an exact symbolic identity after standard HPL reductions. This resolves the specific finite shift within those conventions; it does not certify the real-emission normalization or the full decay assembly.

## 2. Source conventions and normalization

For one quark, let `r=m^2/Q^2`, `x=(sqrt(1-4r)-1)/(sqrt(1-4r)+1)+i0`. The implementation uses the rationalized expression `x=-4r/(1+sqrt(1-4r))^2+i0`. The production numerical domain is `0<r<=0.08` and `|x|<=0.1`, above quark-pair threshold and separated from it.

ABDV Eq. (6) supplies the one-loop function `F_ABDV^(1)`. Its relation to the inherited heavy-loop-normalized form factor is

```
F = -(3/4) F_ABDV^(1).
```

Let `f_a`, `f_b` be their Eqs. (12),(13), and `g_A` their Eq. (28), with the HPL combinations of Eqs. (14),(30). Here the subscript on `f_b` labels a coefficient in the source, not the bottom quark. Equations (11),(15),(27) give

```
G_ABDV,MS = -(3/2) { C_F [f_a + f_b ln(m^2/mu^2)] + C_A g_A },
G_ABDV,OS = -(3/2) { C_F [f_a + (4/3) f_b] + C_A g_A },
C_F=4/3, C_A=3.
```

The `-3/2` combines the `-3/4` normalization and the conjugate interference term in source Eq. (27). `G` is the cross-section-level numerator used in `Re(G F*)`; an additional factor of two would double count that convention. Neither formula includes the source's universal production `C_A*pi^2/3` contribution, real emission, or the full decay correction.

The source labels its MSbar and on-shell prescriptions explicitly. The comparison uses the same numerical mass argument when testing algebraic scheme identities. A numerical prescription change for a physical prediction would also have to change the Born masses and accompanying terms consistently.

## 3. Exact identity, not a fitted finite coefficient

Write `D=m*d/dm` at fixed Q, and let `G1` be the inherited transcription of HK Eq. (3.7), their product `F0^H B1^H`. Expressing the ABDV HPLs in the same logarithm/polylogarithm basis gives

```
f_b = D F,
G_ABDV,OS = G1,
G_ABDV,MS = G1 + 2[ln(mu^2/m^2)+4/3] D F.
```

Therefore, relative to the literal Note-46 choice `G46=G1+2 ln(mu^2/m^2) D F`,

```
G_ABDV,MS - G46 = (8/3) D F.
```

This is exactly the shift tested numerically in Note 48. There is no fitted constant, coupling, mass, or target cross section in the identity. For the coherent amplitude `A=k_b F_b+k_c F_c` with fixed real Yukawa multipliers, the corresponding finite change is

```
Delta V = Re[(8/3)(k_b D_b F_b+k_c D_c F_c) A*]
        = (4/3)(D_b+D_c)|A|^2.
```

The derivative retains bottom–charm interference. The additive expression remains finite at cancellations; it never divides by a small leading amplitude.

`prove_note49.py` verifies the identities with exact rational SymPy arithmetic. The HPL reductions follow integration by parts/shuffle relations from the standard kernels. For example,

```
H(0,1,0;x) = log(x) Li2(x)-2 Li3(x),
H(1,0,0;x) = -log(x)^2 log(1-x)/2-log(x) Li2(x)+Li3(x),
H(0,0,-1,0;x) = -log(x) Li3(-x)+3 Li4(-x).
```

The single nonclassical HPL `H(1,0,-1,0;x)` is kept as an independent symbolic basis element and cancels in the difference. The zeta identity `zeta4=(2/5)zeta2^2` is applied. The resulting rational coefficients vanish exactly, not just below a floating-point tolerance. This proves an identity of the specified **transcribed expressions in a common branch convention**, not a new QCD theorem or a certification of every earlier source transcription.

The independently published one-loop mass relation in RunDec [3] explains the finite `4/3` boundary term. ABDV's separate on-shell and MSbar expressions now determine which numerator to use in our implementation. We do not assign an author-confirmed erratum to HK or Spira; no author contact or confirmation was obtained. Note 46's historical block is preserved, with this addendum documenting the corrected use.

## 4. Independent numerical implementation and results

The new `abdv_virtual_check.py` does not import `bc_virtual_finite`, `mixed_gluon_nlo`, `decay_assembly_audit`, or `coherent_bc_rg`. Its hard coefficient is a separate transcription of the ABDV color structures. HPLs are evaluated by a generic, recursively constructed power/log series with exact rational coefficients before numerical evaluation. The convergent 48-term special-function series is not a truncation of physical quark-mass dependence.

A separate 65-digit evaluator uses ordinary polylogarithm identities and the defining one-dimensional integral for `H(1,0,-1,0)`. It shares the new ABDV rational color decomposition, so that check is an independent numerical special-function evaluation, not a second transcription of the ABDV rational coefficients. The cross-source comparison against HK uses different rational formulas as well as different special-function evaluators.

The scan covers Q=20,21.5,23,40,65,80 GeV, scales mu/Q=1/2,1,2, running and auxiliary-pole prescriptions, and both quark flavors: **72 complex-numerator comparisons**. The largest matched absolute difference is `9.57e-15` in the dimensionless numerator; the largest relative difference is `7.04e-15` after rounding upward. These are numerical checks, not physical uncertainties. The exact symbolic identity is the stronger statement.

All benchmark inputs remain unchanged: m1=10 GeV, m2=11.5 GeV, mh=125 GeV, fixed Gamma_h=0.0041 GeV, K11=K22=0.001 and K12=-0.001; alpha_s(MZ)=0.1189, MZ=91.1876 GeV, mb(10)=3.610 GeV and mc(3)=0.986 GeV. They are frozen historical comparison inputs, not newly derived parameters. The inherited running and thermal kernel are shared, not independently rederived in this note.

The newly evaluated **matched finite-virtual component**, at assumed T=0.5 GeV and mu=Q, is:

| Incoming pair | Matched mass-dependent virtual contribution [GeV^-2] |
|---|---:|
| 11 | 2.01239116329e-17 |
| 12 | 1.92270952260e-17 |
| 22 | 1.82333114817e-17 |

These are finite-window contributions over w in [0,90], with hard energies restricted to [20,80] GeV and temperatures to [1/3,0.5] GeV. They are not standalone event probabilities or physical infinity-domain integrals. Only under the still-unestablished chemical-equilibrium weighting does the combination become

```
matched finite-virtual effective contribution = 2.00209722278e-17 GeV^-2.
```

It reproduces Note 48's literal virtual component plus its finite matching shift. The bb, cc and interference pieces, respectively, are approximately `1.54177e-17`, `4.23680e-19`, and `4.17956e-18 GeV^-2`. The largest Q-versus-w integration difference for the coherent pair values is `3.09e-32 GeV^-2` after rounding upward. Agreement of two thermal variables checks the integrator, not the QCD accuracy.

**No new full real-plus-virtual rate was generated in this step.** Note 48's assembled candidate is not promoted to a certified physical rate by this virtual-only check. Its separate real-emission and integrated-subtraction review remains necessary.

## 5. Executed verification, failure record and publication

All 33 entries of the attached Note-48 manifest were verified before using the archived source. The first new suite passed **24 tests**. The combined local suite passed **251 tests: 24 new and the 227-test inherited chain**, zero failures/errors. The original standalone Note-41 and 45-real suites are not included. This is not a whole-repository audit or empirical validation.

An exploratory symbolic diagnostic initially tested `f_b + D F=0` instead of the correctly signed `f_b - D F=0`. Its false result was preserved in `INITIAL_SYMBOLIC_DIAGNOSTIC.json`. The diagnostic sign and comment were corrected after examining the exact coefficient identity; the independently transcribed physics formulas, numeric outputs and test tolerances were not changed. The subsequent three exact identities and all tests passed. A terminal streaming-session launch was unavailable; the completed local subprocess run and its exit status are recorded, not inferred from that launch attempt.

The runtime was Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0 and SymPy 1.14.0. Commands:

```
python -m unittest -v test_research_note_40.py test_research_note_42.py test_research_note_43.py test_research_note_44.py test_note45_rg_matching.py test_research_note_46.py test_research_note_47.py test_research_note_48.py test_research_note_49.py
python reproduce_note49.py
python prove_note49.py
```

The package contains executable dependencies, source hashes, the complete scan, exact-identity output, logs and a separate publication receipt. The earlier Note-48 outage statement remains historical; any recovered publication is recorded in the new receipt without editing that earlier statement. Source objects alone are not evidence of a branch update. No old source, archived paper or main-branch file is to be overwritten by this additive recovery.

The ABDV formula text and explicit schemes were checked in both parsed PDF and HTML. A rendered PDF page containing Eqs. (27)–(30) was successfully inspected. Attempts to render the earlier formula pages and to download PDFs into the container failed; no full-page visual audit or external executable run is claimed. The source does not contain real-emission terms in its virtual result, and we do not silently supply them.

## 6. What is now resolved, and what remains

The specific Note-48 finite-virtual matching shift has an independent published derivation, a separate numerical implementation, and an exact symbolic identity. It is no longer supported only by the mixed-sector numerical comparison. This is a concrete closed check within the declared formalism.

Still open: the independently reviewed three-gluon normalization reconstruction, full compatible real/virtual/subtraction assembly, omitted heavy-final-state cuts and their interference, direct light-quark/electroweak contributions, conversion scatterings, kinetic conditions, cosmological history and initial conditions. No Omnes arrays, heavier-singlet hadronic width/lifetime, H2 observable, detector exclusion, cosmological abundance, DOI or experimental confirmation was produced here.

## Primary references

[1] U. Aglietti, R. Bonciani, G. Degrassi and A. Vicini, *Analytic Results for Virtual QCD Corrections to Higgs Production and Decay*, JHEP 01 (2007) 021, arXiv:hep-ph/0611266v3. Eqs. (6),(11)–(15),(27)–(30). https://arxiv.org/html/hep-ph/0611266 . Third-source virtual diagram result; not a full decay calculation reproduced here.

[2] R. Harlander and P. Kant, *Higgs production and decay: Analytic results at next-to-leading order QCD*, JHEP 12 (2005) 015, arXiv:hep-ph/0509189v1. Eq. (3.7), inherited transcription compared symbolically. https://arxiv.org/pdf/hep-ph/0509189 . The identity determines the relation of coefficient conventions in our implementation; no author-confirmed erratum is asserted.

[3] K. G. Chetyrkin, J. H. Kuhn and M. Steinhauser, *RunDec*, arXiv:hep-ph/0004189. One-loop mass relation and QCD conventions. https://arxiv.org/abs/hep-ph/0004189 . No RunDec executable is run.

Internal lineage: Note-48 conversation package; live review branch initially at 94093121a33a3486a8c5e74c0a1fbcf496654d74. Source authors supply established QCD ingredients, not support for the hypothetical singlets or consciousness/ethics interpretations.
