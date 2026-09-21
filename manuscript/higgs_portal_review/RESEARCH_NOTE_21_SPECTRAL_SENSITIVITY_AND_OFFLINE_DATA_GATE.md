# Research Note 21 — How strong must the low-mass spectrum be, and what can we safely authenticate?

**21 September 2026 · Public, unreviewed scientific-development draft.** Human author: Christopher Michael Baird. ChatGPT (ZoraASI) assisted with independent algebra, software implementation, synthetic-fixture testing and drafting. The underlying two-singlet model is hypothetical; no physical interpretation as a consciousness or ethics field is experimentally established.

This note continues Notes 15, 19 and 20's restricted symmetric-vacuum, zero-source, common-\(\mathbb Z_2\) collider EFT and **does not add a hadronic-width measurement**. It closes two *procedural/mathematical* gaps without using unavailable third-party numerical grids: (a) quantitatively characterizing the ambiguity of the previous 0.414% kinematic weight, and (b) supplying a fail-closed, offline provenance checker for the four pinned upstream Omnès input files.

## 1. Exact spectral-weight identity, not a QCD prediction

With the **illustrative, unfitted** parameters `m1=10 GeV`, `m2=25 GeV`, `mh=125 GeV`, `Gamma_h=0.0041 GeV`, `v=246 GeV`, `|K12|=0.001`, Note 20 obtains the positive toy kernel `W(s)` on `0<s<(15 GeV)^2`, whose *normalized integrated weight* below `sqrt(s)=2 GeV` is

\[
p\equiv\frac{\int_0^{4\;\mathrm{GeV}^2}W(s)\,ds}{\int_0^{225\;\mathrm{GeV}^2}W(s)\,ds}
=0.004138912\quad(\text{numerical toy-kernel integration}).
\]

For any **specified** nonnegative channel spectrum `rho(s)=Gamma_unit(h*(sqrt(s))->X)` of the same physical final-state set across the entire integration range, let `I_L=integral_[0,4] W`, `I_H=integral_[4,225] W`, and `bar_rho_L=(integral_L W rho)/I_L`, with an analogous high-bin definition. Where both weighted means are defined and `bar_rho_H>0`, set `R=bar_rho_L/bar_rho_H`. The *actual channel-specific low-window width fraction* obeys the **algebraic identity**

\[
 F_L = \frac{I_L\bar\rho_L}{I_L\bar\rho_L+I_H\bar\rho_H}
     = \frac{pR}{pR+1-p},\qquad
 R(F_L)=\frac{F_L(1-p)}{p(1-F_L)}.
\]

It follows that a low-bin contribution of 1%, 10%, 50%, or 90% would respectively require weighted-mean low/high spectral-strength ratios of approximately **2.4304, 26.7344, 240.6094, or 2165.4845**. For synthetic ratios `R=1, 10, 100, 250, 1000`, the corresponding exact-to-rounded-input fractions are **0.41389%, 3.99027%, 29.35914%, 50.95704%, 80.60555%**. These numbers are *hypothetical sensitivity examples*, NOT inferred QCD ratios, calculated pion/kaon fractions, or branching predictions. The ratio can differ across channels; channel fractions cannot be added as though they shared a denominator. If the high-bin strength vanishes but the low bin is nonzero, `F_L=1`; if the full channel strength vanishes, `F_L` is undefined. Consequently no nontrivial hadronic fraction bound follows from `p` alone. The below-2-GeV partial integration also cannot stand in for the channel's full width through 15 GeV.

If future independently validated spectral analysis establishes `R <= R_max`, monotonicity gives `F_L <= p R_max/(p R_max+1-p)`; a certified positive lower bound analogously gives a lower bound. **There is currently no verified numerical `R_max` or `R_min`.** In particular, the ~0.414% kinematic weight cannot be used to argue either that missing low-energy QCD is negligible or that it dominates.

## 2. A reproducible, fail-closed *offline* input-identity gate

The pinned external source `blackstonep/hipsofcobra@6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7` reports the following four input identities, as independently listed by GitHub's contents metadata in Note 20. These are *expected values*, not evidence that their content has been retrieved in our environment:

| Input file | Expected length, bytes | Expected Git blob SHA-1 |
|---|---:|---|
| `hips_c1.txt` | 2,981,801 | `89cb2c3a7a992653521a9c2e9eb84295a0c45737` |
| `hips_c2.txt` | 2,981,479 | `fa282fc1584322ed1f64902ca023fcdac8e01843` |
| `hips_d1.txt` | 3,032,630 | `e5c0ef428e84e9605777dfa9845cc262e5b0e037` |
| `hips_d2.txt` | 2,939,837 | `1ff49406489df0dc90eabcb06acd99083bfcb56e` |

The new **original, standard-library-only** `safe_omnes_manifest.py` accepts a user-supplied local directory and reads *only those fixed basenames*. It rejects symlinks, non-regular files, wrong lengths, exceeding a size cap, modified bytes and hash mismatches; it computes the correct Git blob digest using `SHA1(b'blob '+ASCII_decimal_byte_count+b'\0'+raw_bytes)`. On **all four successful matches**, it reports a separately computed raw-byte SHA-256 and a bounded `repr`-escaped literal byte sample for later grammar review. Raw SHA-256 values are not yet known because the source files have not been acquired. This identity check does not by itself authenticate the trustworthiness of GitHub, establish spectral correctness or neutralize theoretical SHA-1 collision risks; retain commit/path provenance and the new independent SHA-256 receipts.

**No `eval`, `exec`, third-party source-code execution, numerical-form-factor evaluation, or data-content parsing occurs** in this program. Do not replace this tool with the upstream loader's `eval(file.read().replace('C','c'))`. The candidate grammar of these four files remains unknown; do not assume `ast.literal_eval` accepts it. After the source bytes pass identity verification, inspect escaped text samples, design a grammar-specific parser without general expression evaluation, and separately validate scalar-current normalization, sample/grid dimensions, `s` units, endpoints, finite entries and independent reference results.

Local reproduction, once the exact four files have been **independently obtained**:

```bash
python3 safe_omnes_manifest.py /absolute/path/to/hipsofcobra/input
python3 -m unittest -v test_research_note_21.py
```

Until then, running the validator against a directory with missing files correctly exits with `UNVERIFIED`, rather than inventing successful checks. The 15 synthetic-fixture and algebraic regression tests pass locally; these tests verify **our validation code and algebra**, not external data, QCD, or the research model. Neither third-party code nor input data are redistributed here. The upstream project's license/provenance still needs review before incorporation into any manuscript or artifact.

## 3. Unchanged physical-claim boundary and next stop condition

Note 15's conditional tree-level leptonic floor for this model remains `Gamma_leptons=1.156499157e-15 GeV`, hence `c tau_2 <= approximately 17.06 cm`. Neither a weighted-mean thought experiment nor a successful *future* file-identity check tightens that limit: a numerical lower bound on an **additional, physically matched** hadronic partial width is required, after checking that all final states are nonoverlapping. We still have no verified pion/kaon partial width, total width, hadronic branching ratio, detector efficiency, or new experimental constraint.

**Next gate:** obtain all four byte-exact upstream input files; run the offline identity check and record raw SHA-256 receipts; inspect their grammar without executing it; then certify the form-factor grid and low-energy domain and perform an independently normalized exclusive pion/kaon calculation. Stop at the identity check if any file fails. Keep the draft pull request open and unmerged pending external physics review.

Sources: Notes 15, 19, 20 in this public draft branch; primary hadronic-scalar-current paper https://arxiv.org/pdf/2407.13587v1 ; version-pinned upstream repository https://github.com/blackstonep/hipsofcobra/tree/6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7 . The new `R` sensitivity and validation program are original derived work based on those sources, not statements made in the external hadronic paper.
