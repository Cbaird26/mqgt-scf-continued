# Research Note 20 — Quantifying the two-meson window and auditing an unresolved data-access gate

**21 September 2026 · Public scientific-development draft, not peer reviewed.** Author: Christopher Michael Baird; AI-assisted derivation, source audit, numerical cross-check, and writing: ChatGPT (ZoraASI). This note studies only the restricted symmetric-vacuum, zero-source, common-Z2 two-singlet collider EFT of Notes 12–19. The fields are hypothetical; their consciousness/ethics interpretations are not physical measurements.

## 1. Source-backed status: upstream input identity, not its contents

The pinned `blackstonep/hipsofcobra` revision `6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7` contains four Omnès text inputs. GitHub's pinned directory API lists the following **Git blob IDs and byte sizes**, which specify files to obtain and authenticate later (these are *not* local content checks):

| Path under `hipsofcobra/input/` | Bytes | Git blob SHA-1 |
|---|---:|---|
| `hips_c1.txt` | 2,981,801 | `89cb2c3a7a992653521a9c2e9eb84295a0c45737` |
| `hips_c2.txt` | 2,981,479 | `fa282fc1584322ed1f64902ca023fcdac8e01843` |
| `hips_d1.txt` | 3,032,630 | `e5c0ef428e84e9605777dfa9845cc262e5b0e037` |
| `hips_d2.txt` | 2,939,837 | `1ff49406489df0dc90eabcb06acd99083bfcb56e` |

Pinned source directory: https://github.com/blackstonep/hipsofcobra/tree/6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7/hipsofcobra/input . Pinned implementation: https://github.com/blackstonep/hipsofcobra/blob/6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7/hipsofcobra/classes.py . Its constructor applies `eval(file.read().replace('C','c'))` to each file and initializes a random generator without a fixed seed. **Do not execute that input loading on untrusted bytes.**

This environment retrieved the directory *metadata* and inspected the relevant Python source, but its GitHub connector returned empty content for the oversized `hips_c1.txt` file; the direct raw-file route was unavailable. Accordingly **none of the four data files was downloaded or parsed, and the actual grid endpoints, syntax, source-data uncertainty and physical coverage remain unverified**. The roughly 2 GeV provisional method window in Note 19 comes from the cited paper, *not* a demonstrated grid maximum. Do not present an inferred grid range as a measured one.

## 2. A new calculation independent of the missing hadronic input

Use the Note 15 tree-level, fixed-width kernel with the illustrative, *unfitted* values `(m1,m2,mh,Gamma_h,v,|K12|)=(10,25,125,0.0041,246,0.001)` in GeV where applicable:

\[W(s)=\frac{v^2K_{12}^2\sqrt{[(m_2+m_1)^2-s][(m_2-m_1)^2-s]}\sqrt{s}}{16\pi^2m_2^3[(m_h^2-s)^2+m_h^2\Gamma_h^2]},\qquad 0\leq s\leq225\;\mathrm{GeV}^2.\]

Define the **kinematic-kernel fraction** `f_W(a,b)=integral_a^b W(s) ds / integral_0^225 W(s) ds`. It is independent of unknown hadronic form factors, but is *not* a branching fraction or a fraction of actual hadronic decays. Numerical quadrature yields:

| `s` interval (GeV²) | Interpretation of the mathematical window | `f_W` |
|---|---|---:|
| `[0,4]` | virtual mass at most 2 GeV | `0.004138912` (0.413891%) |
| `[4 m_pi²,4]`, `m_pi=0.134 GeV` | above the **reference-mass** pion threshold, at most 2 GeV | `0.004128894` (0.412889%) |
| `[4 m_K²,4]`, `m_K=0.497 GeV` | above the **reference-mass** kaon threshold, at most 2 GeV | `0.003628486` (0.362849%) |

The latter two fractions concern **overlapping portions of the same kinematic kernel** and cannot be added. These use the upstream implementation's approximate isospin-symmetric reference masses, not exact charged/neutral thresholds. A standard-library composite-Simpson calculation and a separate SciPy adaptive integration agree to roughly `3e-10` in each quoted dimensionless fraction; the seven standard-library regression tests pass locally. See `test_research_note_20.py`. This is numerical validation of a *chosen toy kernel*, not of QCD or the proposed physical fields.

## 3. A crucial non-inference: 0.414% does not bound a decay fraction

The physical contribution is instead `Gamma_X(window) = integral_window W(s) Gamma_unit(h*(sqrt(s))->X) ds`. Because `Gamma_unit` varies with virtual mass and can peak near thresholds or resonances, **the 0.413891% kernel fraction places neither an upper nor a lower nontrivial bound on the *fraction* of a physical hadronic partial width inside that window**. Even a nonnegative, sharply concentrated *synthetic* spectrum can make the window contribute more than 99% of its constructed total. The code includes this counterexample solely to prevent misuse of `f_W` as a hadronic branching-ratio estimate. Conversely, the source's pion/kaon amplitudes remain physically open above 2 GeV; truncating an integral at the provisional methodological boundary can supply a nonnegative *partial-window contribution*, never automatically the full `pi pi` or `K K-bar` partial width.

The familiar leptonic-only conditional ceiling `c tau_2 <= ~17.06 cm` therefore **has not changed**. No hadronic central width, total lifetime, 2-GeV branching fraction, detector signature or experimental constraint was calculated.

## 4. Read-only reproducibility handoff

Obtain the four exact upstream files by a permitted direct download or user-supplied local checkout. Match **both** byte lengths and Git blob hashes (Git's blob ID is SHA-1 of `b'blob '+length+b'\\0'+file_bytes`; it is not ordinary SHA-1 of the raw file). Inspect only short literal byte samples to establish the real grammar; implement a fail-closed format-specific parser that never invokes `eval`, `exec` or arbitrary imports. Validate monotone `s` grid, first/last values and units, finite complex form factors, equal array shapes and sample counts across all four files; seed and document stochastic evaluation; independently compare one trusted source example. Then evaluate the unit-current `[1,1,1]` pion and kaon **absolute, exclusive** widths in a justified domain, propagate source uncertainty, and integrate them separately with the kernel.

**Stop condition:** metadata alone cannot certify source-grid coverage. Keep numerical hadronic contributions and tighter decay-length numbers out of the manuscript until authenticated bytes, safe parsing, valid domain, source normalization and independent review are actually available. The draft PR is public, unmerged; no journal submission, DOI or experimental validation is implied.

Sources: arXiv:2407.13587v1 https://arxiv.org/pdf/2407.13587v1 ; pinned external code and data https://github.com/blackstonep/hipsofcobra/tree/6a6dcfccf903317ea2104e27bb1dbbc7ad1d9fc7 ; previous audit `RESEARCH_NOTE_19_SOURCE_TO_MODEL_MATCHING.md`.