# Spectral Profile Nonuniqueness at a Common Stationary Vacuum

**Baird / ZoraASI Research Continuation — research note dated 21 October 2026.**
Publication package prepared 22 October 2026, America/New_York.

**Status:** conditional mathematical result within the stipulated shared spectral action. This package preserves an analytic proof, an exact rational seed certificate, and a numerical illustration. It does not determine a physical spectral action or the measured fine-structure constant. Preparation of this package does not itself establish a GitHub publication; see `PREPUBLICATION_RECORD.json` at the archive root.

## Result and inherited action

Within the stipulated shared spectral action and the class of finite positive exponential mixtures, the retained finite local spectral data do not select a unique hypercharge coefficient throughout the class, even when a common stationary vacuum and a common gravitational coefficient are imposed. The result is existential: for every finite order of local data there exist distinct profiles that agree on those data and on the retained vacuum and gravitational quantities, yet differ in the exact hypercharge coefficient. The pair may depend on the chosen order.

The action is the inherited form

\[
S_{\mathrm{sp}}=\frac{\kappa}{2}\sum_i\mathrm{Tr}_{\mathrm{Dirac}}f(D_i^2/\Lambda^2),
\qquad \kappa>0,\qquad R=\Lambda r,
\]

with admissible profiles

\[
f(u)=\sum_{j=1}^{n}w_j e^{-a_j u},
\qquad a_j>0\text{ distinct},\quad w_j>0,\quad \sum_jw_j=1.
\]

The local data of order \(p\) consist of the inverse moments \(m_k=\sum_j w_j a_j^{-k}\), for \(k=1,2,3\), and the derivatives \(f(0),\ldots,f^{(p)}(0)\). These are the profile factors appearing through the corresponding finite order in the six-dimensional local heat expansion. The vacuum prescription is the inherited stationarity condition

\[
F(R)=RP'(R)-2P(R)=0,
\qquad c=P(R)/R^2.
\]

The gravitational coefficient is fixed by \(J(R)\) at fixed \(\kappa\) and \(\Lambda\). The complete definitions of the internal heat sums and kernels are given in the accompanying research note. The exact internal-mode response remains within the inherited low-external-derivative expansion.

## Theorem and proof

Theorem 1 states that for every finite integer \(p\geq0\) there exist two distinct normalized profiles on a common set of \(n=p+8\) distinct positive rates, with every weight strictly positive, and a common radius \(R_*>0\), such that the profiles agree on the local data of order \(p\), share the same values of \(P\), \(P'\), and \(J\) at \(R_*\), both satisfy stationarity with the same numerical \(c\), both have positive restricted radius-potential curvature, and produce different values of \(Z_Y/\kappa\). The construction shows that \(p+8\) components suffice; minimality is not claimed.

For any fixed \(R>0\), the \(p+8\) functions consisting of the Laurent monomials \(a^{-3},\ldots,a^p\), the three vacuum and gravitational kernels \(\mathsf p_R,\mathsf d_R,\mathsf j_R\), and the gauge kernel \(b_R\) are linearly independent on \(a>0\). Independence follows from the distinct exponential asymptotics of the first two nonzero levels of the internal heat sums and from the leading nonconstant exponential contribution to \(b_R\), which cannot be reproduced by a linear combination of the Laurent monomials and the remaining kernels.

Consequently, nodes can be chosen so that the evaluation matrix of these functions is nonsingular. Its first \(p+7\) rows have a one-dimensional kernel. Nonsingularity after appending the gauge row implies that every nonzero vector in that kernel changes the hypercharge coefficient.

Existence of a suitable base point starts from the pure exponential \(f(u)=e^{-u}\). An exact rational certificate establishes a simple stationary root inside \((1.30078,1.30079)\), with \(F'>32\) throughout the interval and restricted curvature \(K>24\) at the root. After fixing the additional distinct positive nodes, assigning them sufficiently small positive weights supplies, by the implicit-function theorem, a nearby stationary root that remains simple with positive curvature. The evaluation matrix remains nonsingular by continuity. Perturbing the weights along its constraint-kernel vector then produces the two profiles while preserving all retained constraints and the common vacuum data.

## Ten-component numerical illustration

A concrete realization for \(p=2\), preserving local data through \(a_{10}\), was computed at 95-digit precision. At the common stationary radius \(R_*\approx1.278472412\), the two profiles share the subtraction and gravitational coefficients. Both have positive restricted curvature; their curvatures are not equal. The hypercharge coefficients differ by

\[
\frac{Z_{Y,+}-Z_{Y,-}}{\kappa}
=9.31197879865\ldots\times10^{-8},
\]

a relative difference of approximately \(4.64564\times10^{-7}\), measured relative to the minus profile. This magnitude is set by the chosen weight displacement and is not a predicted correction to the archived T-1 residual. No measured fine-structure constant was used as an input.

An independent floating-point implementation reproduces the radii and coefficients to ordinary precision. The general existence argument is analytic and uses the rational seed certificate. The ten-node example is a numerical illustration; its specific matrix rank and root are not separately interval-certified. Long displayed decimal strings and small numerical residuals do not change that distinction.

## Quantifiers and physical scope

The theorem establishes noninjectivity of the finite-data map on the stated class. It does not claim ambiguity for every prescribed moment vector, nor does it produce one fixed pair agreeing at every local order simultaneously. Normalized data satisfying \(m_2=m_1^2\), for example, force zero variance of \(1/a\), hence support at a single rate fixed by \(m_1\). An extra local heat coefficient can identify a specified finite ansatz. These possibilities do not supply a general physical selection principle for the unrestricted family.

Positive restricted curvature under the inherited radius-potential prescription does not establish a radion kinetic term, a physical radion mass, or complete compactification stability.

The constructions concern different profiles, hence different actions inside the proposed family. They do not assert that one fully specified action yields contradictory predictions, and they do not select which action is physical. The measured fine-structure constant remains unexplained.

## Open physical problem

A proposed completion must derive a restriction on the admissible profile or action that removes the relevant freedom, or demonstrate that the completed electromagnetic observable is insensitive to the remaining admissible deformations. Independent normalization of \(\kappa\), a consistent vacuum and radiative definition, and electroweak embedding, thresholds, and running remain necessary parts of that calculation. The present result supplies explicit deformations against which such a proposal can be tested.

## Files and reproduction

| File | Purpose |
|---|---|
| `Spectral_Profile_Common_Vacuum_2026-10-21.pdf` | Complete seven-page research note |
| `research_note.tex` | Manuscript source |
| `stationary_profiles.py` | High-precision ten-component construction |
| `stationary_profiles_results.json` | Recorded weights, coefficients, and diagnostics |
| `certify_seed.py` | Exact rational stationary-seed certificate |
| `stationary_seed_certificate.json` | Recorded certificate bounds |
| `independent_check.py` | Independent floating-point implementation |
| `independent_check_results.json` | Recorded independent results |
| `provenance.json` | Original research preparation record and source references |
| `README.txt` | Original reproduction instructions and attribution |
| `PREPARATION_SHA256SUMS.txt` | Original ten-file research manifest |
| `SHA256SUMS.txt` | Complete manifest for this publication subdirectory |
| `LICENSE` | Destination repository's CC BY 4.0 license |

From this directory:

```bash
python3 stationary_profiles.py
python3 certify_seed.py
```

Those two programs use the Python standard library. The optional independent check requires NumPy and SciPy:

```bash
python3 independent_check.py
```

The programs overwrite only their own recorded result files. Verify the supplied checksum manifest before rerunning if checking the archived bytes. No additional mathematical calculation was performed during publication packaging.

## Attribution and source record

Prepared for Christopher Michael Baird with ChatGPT assistance. The proof extension, numerical example, and seed certificate were internally cross-checked using AI-assisted reasoning and calculations. External peer review is not claimed.

The inherited definitions and predecessor calculation are pinned to [the October 21 electromagnetic note](https://github.com/Cbaird26/mqgt-scf-continued/blob/7a36e0d741cb8ddb16056d39640ada43e28ad951/research_continuation/2026-10-21/electromagnetic/RESEARCH_NOTE.md). The source archive's page range and SHA-256 hash are recorded in `provenance.json`. The original proof, PDF, scripts, and numerical results are preserved byte-for-byte from the reviewed research bundle.

This continuation is prepared for distribution under the destination repository's Creative Commons Attribution 4.0 International license, included as `LICENSE`. Third-party source materials are referenced rather than redistributed in this package.
