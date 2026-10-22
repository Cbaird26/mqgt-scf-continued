# Spectral Profile Nonuniqueness at a Common Stationary Vacuum

Baird / ZoraASI Research Continuation. Research note dated 21 October 2026; publication package prepared 22 October 2026.

This continuation extends the earlier five- and six-component profile calculations to an arbitrary-order existence theorem. For every finite local order, suitable positive exponential profiles exist with identical retained local data, a common stationary radius, the same subtraction coefficient, and the same gravitational coefficient at fixed normalization and scale, but different exact hypercharge coefficients. Both profiles have positive restricted radius-potential curvature.

The package includes:

- The complete analytic proof, with its existential quantifier boundary.
- An exact rational certificate for the simple pure-exponential stationary seed.
- A ten-component numerical illustration preserving local data through a10, with a hypercharge-coefficient difference of 9.31197879865... x 10^-8 and relative difference of approximately 4.64564 x 10^-7.
- Standard-library reproduction scripts, a separate NumPy/SciPy check, recorded results, source provenance, the repository license, and checksums.

## Scientific status

This is a conditional mathematical result within the stipulated shared spectral action and profile class. The pair may depend on the finite order; uniqueness can still hold for particular prescribed data. The theorem does not claim that every dataset is ambiguous or that p+8 is a minimal component count.

The profiles represent different actions. The result does not select a physical action, derive the measured fine-structure constant, establish complete compactification stability, or provide a quantum and electroweak completion. The size of the numerical example is chosen by the weight displacement and is not a predicted correction to the archived T-1 residual.

The general theorem is analytic, its starting seed is rationally certified, and the specific ten-node illustration is numerical. Internal AI-assisted review and reproduction are disclosed; external peer review is not claimed.

## Relation to the previous checkpoint

This is an additive continuation of `v2026.10.21-research-continuation`. That checkpoint's five- and six-component profile examples selected their stationary vacua separately. The present theorem and example preserve a common radius, subtraction, and gravitational coefficient. The October 21 release remains the historical predecessor.

## Reproduction

The full publication summary and instructions are in `research_continuation/2026-10-22/electromagnetic/README.md`. From that directory run:

```bash
python3 stationary_profiles.py
python3 certify_seed.py
# Optional independent numerical check; requires NumPy and SciPy:
python3 independent_check.py
```

The next physical target is an independently justified restriction on the profile or action, or a completed matching calculation establishing insensitivity of the electromagnetic observable to the surviving deformations.
