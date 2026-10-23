# Validation and self-audit

This record describes checks by the same assistant session using independent computational paths. No separate agent review or external peer review was performed.

## Checks performed

- Recovered the full geometric weak operator, including the Pauli term, from the supplied predecessor PDF; recorded its SHA-256 in provenance.json.
- Built the monopole spinor and scalar multiplication matrices from Clebsch-Gordan coefficients and checked 106 entries against independent Wigner-function sphere quadratures.
- Reproduced the n=0,1,2 heat traces, zero-mode overlap and all three inherited unbroken neutral normalizations.
- Compared scalar quadratic coefficients from the two-insertion formula and a block-triangular matrix exponential; compared quartics against a complex Cauchy-contour evaluation.
- Verified the exact parallel-flavour rotation identity and quark quadratic additivity.
- Derived the full neutral transverse response, retaining the seagull and noncommuting scalar terms. Checked it against full external Clifford matrices at finite momentum, using independent quadrature.
- Checked scalar wave-function/gauge-mass Ward identities and the exact photon commutator and null direction.
- Compared angular cutoffs 8, 10 and 12, two Cauchy contours, real-background Richardson extraction, and radius-derivative step sizes.
- Checked the zero-mode small-radius limits and the large-radius local limits, including the geometric a4 weak correction.

The recorded 126 checks include separate sector/magnetic-block identities; the number is not a count of independent physical predictions. Detailed metrics and tolerances are in checks.json. The convergence comparisons do not certify rounding errors or a universal infinite-tail bound. The exact zero-mode and flavour-rotation statements in the note are analytic identities; their implementation checks are numerical.

## Corrections and distinctions

1. The geometric WW Higgs correction has an a4 curvature contribution. The predecessor's A9 order-counting was incomplete; its shared-local-moment conclusion is unaffected.
2. Equality of the two mixed quartic coefficients belongs to the local a2-a4 truncation. At the inherited radius, the exact coefficients C0 and C1 differ.
3. The kinetic coefficient is defined by the transverse low-momentum response at fixed background. It is not equated to the coefficient of a single dimension-six Wilson operator.
4. Profile comparisons use identical noncanonical scalar amplitudes and a common prescribed radius. Canonical normalization differs slightly, and the physical coupled vacuum is not supplied by this comparison.
5. Internal heat sums are classical spectral-action data. Calling them exact does not promote them to quantum threshold or running corrections.
6. The canonical scalar quadratic parameter is not a physical pole mass. Because it is of order the cutoff, locating the pole requires the momentum kernel beyond its quadratic expansion.

PDF rendering, source compilation and a fresh-extraction rerun are recorded in DELIVERY_VERIFICATION.json when the bundle is sealed.
