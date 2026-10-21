# Electromagnetic spectral-profile continuation

Run from this directory, or by absolute script path:

```bash
python spectral_profile_analysis.py
```

The script uses Python 3.12, NumPy, SciPy and Matplotlib. The recorded run used Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0. Exact linear algebra uses the Python standard library's `fractions`; independent high-precision evaluations use `decimal`. No network, measured coupling, paid compute or outside write is required. Runtime is approximately several seconds on the available environment.

## Files

| File | Purpose |
|---|---|
| `RESEARCH_NOTE.md` | Derivation, source boundary, numerical findings and limitations |
| `spectral_profile_analysis.py` | Reproducible computation and 38 built-in checks |
| `profile_identifiability_results.json` | Exact identities, selected 70-digit calculations, validation and provenance |
| `profile_family_scan.csv` | 1,001-point scan of the continuous five-node family |
| `spectral_profile_sensitivity.png` | Changes in the gauge coefficient and normalization-independent ratio |

The calculation is deterministic. Running it overwrites only generated results in this directory. The original archive is optional for rerunning the mathematics; if present at the recorded relative location its SHA-256 is recomputed. If absent, that provenance field is null while the documented equations remain executable.

The branch bracket [1.2,1.4] applies to the five- and six-node mixture examples, not to every possible spectral profile. Positivity at a stationary point is a restricted potential-curvature check, not a physical radion-mass result. The extra derivative datum identifies the fixed five-node ansatz; the six-node counterexample demonstrates why that identification cannot be generalized to arbitrary profiles.
