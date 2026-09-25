# Research Note 19 — Source-to-model matching of pion/kaon spectral inputs

**21 September 2026 · Public scientific-development draft; not peer reviewed.** Human author: Christopher Michael Baird; ChatGPT (ZoraASI) assisted with source audit, algebra and drafting. This note treats only the restricted symmetric-vacuum, zero-source, common-Z2 companion two-singlet EFT of Notes 12–18. The hypothetical fields are not established measurements of consciousness or ethics.

## 1. Primary-source current normalization

Blackstone, Tarrús Castellà, Passemar and Zupan, *Hadronic Decays of a Higgs-mixed Scalar*, arXiv:2407.13587v1 (18 July 2024), Sec. 2, Eqs. (2.1)–(2.4), define dimensionless coefficients `c_q`, `c_l` and `c_g` multiplying SM-Higgs-normalized quark, lepton and gluon operators, with `v_W=246 GeV`. Eq. (2.2) specifies `c_q=c_l=c_g=sin(theta_h)` for a Higgs-mixed scalar. In the isospin limit, Eq. (4.8) sets `c_ud=c_u=c_d`. Appendix A identifies the package's `clist=[c_ud,c_s,c_g]`, and Sec. 5/Fig. 8 use `[1,1,1]` as the **unit-strength Higgs-mixed reference current**. This is a current normalization, NOT an assumption that either of our singlets mixes linearly with the physical Higgs.

Paper: https://arxiv.org/pdf/2407.13587v1 (Secs. 2, 4.1, 5.2 and Appendix A). Pinned upstream: https://github.com/blackstonep/hipsofcobra/tree/6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7 (package 0.0.8, GPL-3.0). `clist=[1,1,1]` specifies only the *virtual Higgs decay current*; our off-diagonal portal `K12` appears solely in the `s2-s1-h*` production vertex. The gluonic coefficient and heavy-flavor threshold scheme still require a dedicated EFT matching audit outside the low-energy domain.

## 2. Exact source multiplicities and partial widths

The paper's Eq. (5.1) gives `Gamma(phi -> P P) = A_P sigma_P(M²) |G_P(M²)|² / (16 pi M)`, with `sigma_P=sqrt(1-4 m_P²/M²)`, `A_pi=3` and `A_K=4`. These include the respective charged and neutral **two-body** isospin channels; do not count charge states a second time. At the pinned upstream commit, `classes.py` assigns `prefactor=3/16` to `Pname='pi'`, `prefactor=0.25` to `Pname='K'`, and `G_to_width` multiplies by `sigma_P*abs(G_P)**2/(pi*M)`. The code and Eq. (5.1) therefore agree on multiplicity and normalization for form factors in the paper's convention.

For the *unit Higgs current* and within a justified mass range, the candidate partial spectra are

```
Gamma_unit_pi_pi(M) = 3 * sqrt(1-4*m_pi**2/M**2) * |G_pi(M**2; [1,1,1])|**2 / (16*pi*M)
Gamma_unit_K_K(M)   = 4 * sqrt(1-4*m_K**2/M**2)  * |G_K(M**2; [1,1,1])|**2   / (16*pi*M)
```

Each vanishes below its own two-meson threshold. Upstream uses isospin reference masses `m_pi=0.134 GeV`, `m_K=0.497 GeV`, not an exact charged/neutral threshold treatment. These are **absolute partial widths in GeV**, not branching ratios. Do NOT divide `[1,1,1]` results by a Higgs-mixing angle again, nor multiply them twice by `K12²`. For `[epsilon,epsilon,epsilon]`, a homogeneous amplitude gives an `epsilon²` width only when the matching/input assumptions are held fixed.

## 3. Provisional domain and execution gates

The paper studies two-meson form factors from threshold to **about 2 GeV**, with Fig. 6/8 plotting up to 2 GeV. Sec. 3.2 reports underlying fitted elastic pion-phase data extending to 1.42 GeV and pion-to-kaon input to 2 GeV, with extrapolation beyond data boundaries. Treat `M<=2 GeV` as a **conservative provisional integration window**, NOT an accuracy certification: the actual shipped grid maximum, extrapolated regions and validity must be audited independently. Our illustrative model requires `M<=m2-m1=15 GeV`; no form-factor extrapolation from 2 to 15 GeV is justified.

Upstream supplies two matching schemes (`DGL` and `BTPZ`) and stochastic mean/one-standard-deviation curves. These are not certified pointwise bounds. The pinned `classes.py` reads Omnès input via `eval(file.read().replace('C','c'))` and uses a random generator without a fixed seed. Do not execute untrusted `eval` inputs. Review the input grammar and hashes; use a format-specific safe parser and seeded sampling only after verifying compatibility. In particular, `ast.literal_eval` is **not assumed to be drop-in compatible** with complex encodings. Link/credit upstream and review GPL-3.0 plus data provenance before any redistribution. **No third-party code, source-data grid or form-factor calculations were executed for this note.**

## 4. Conditional interface, not a new lifetime estimate

For the positive off-shell-Higgs kernel `W(s)` from Note 15, and `M_max <= min(2 GeV, m2-m1, independently verified source grid maximum)`, distinct exclusive final states would yield

```
Gamma_partial = integral_[4*m_pi**2, M_max**2] ds W(s) Gamma_unit_pi_pi(sqrt(s))
              + integral_[4*m_K**2, M_max**2] ds W(s) Gamma_unit_K_K(sqrt(s)).
```

Count each physical final state only once; do not add individually squared light-quark/gluon terms or inclusive continuum already containing these modes. Once independently calculated, a positive `Gamma_partial` can *conditionally* tighten the leptons-only upper bound on `c*tau2`; it cannot provide a total width or lower bound on the lifetime. No numerical hadronic width or updated 17.06-cm ceiling is claimed.

**Finding:** The primary paper and code resolve the candidate coupling-vector meaning and pion/kaon multiplicities. **Remaining gates:** safely inspect/version-pin the actual Omnès grid; audit the virtual-current gluon/heavy-flavor convention; run deterministic source computations in a controlled environment; establish domain/uncertainty and exclusive-channel inventory; integrate verified partial widths and obtain independent review. See `test_research_note_19.py` for six standard-library algebra/contract tests using arbitrary synthetic amplitudes only.