# MQGT-SCF Research Continuation — 2026-10-21

Version: `v2026.10.21-research-continuation`

This checkpoint makes six research routes reviewable together: a shared low-energy
parameter contract, thermal-history sensitivity, public-count reanalysis,
electromagnetic profile identifiability, an ultraviolet implementation audit,
and a synthetic causal-memory experiment. It records computed results,
assumptions, source provenance, numerical checks, and the physical inputs still
needed to connect these routes.

## New results

- **Common action:** explicit portal normalization, basis covariance, matching,
  and a benchmark total tree-level scalar production width of 18.97436 keV.
- **Thermal history:** the frozen 386-state network reproduces; twelve initial
  preparations retain distinguishable endpoints. Entropy-consistent background
  thermodynamics shifts final Tkin/T from 0.750271 to 0.722201, or 0.705674 with
  the separately declared ideal charm/bottom addition. Collision banks remain
  the inherited ideal-bath ones.
- **Measurement:** 95 public scans, 3,895 bins and 10,772,714 recorded counts are
  reanalyzed. The working model has Pearson statistic/df 3.43938. Common
  attenuation remains confounded with free contrast under the stated model.
- **Electromagnetism:** positive five- and six-component spectral profiles
  preserve the imposed scalar data while changing the gauge coefficient.
- **Ultraviolet reconstruction:** scalar feedback through degree six,
  normalization and field-count diagnostics, corrected exponent labels, and
  nonlinear subsystem checks identify specific completion requirements.
- **Operational memory:** a prespecified, entirely synthetic intervention study
  finds causal predictive value in memory access, with held-out and control
  analyses. It is not an experience measurement.

## Scientific status

These are conditional computational and methodological results. A complete
Theory of Everything, a detected new scalar, a derived measured fine-structure
constant, a complete coupled physical UV fixed point, and a consciousness field
are not established. `sources/claim_status.json` gives the exact scope and next
physical dependency for every workstream. Internal AI-assisted cross-checks are
identified as such; they are not external peer review or experimental replication.

## Files and reproduction

The release PDF provides a 13-page account. The offline ZIP includes source,
recorded outputs, required frozen collision banks, public experimental input,
source hashes, notices, and reproduction instructions. The Git source directory
contains code and compact records; larger outputs and binary inputs are in the
ZIP. Download the ZIP for complete offline execution.

```bash
python -m pip install -r requirements.txt
python reproduce.py
python reproduce.py --rerun --include-thermal
```

The full calculation suite was run successfully from an isolated offline copy.
Its log and receipt are included. The optional authors' EOS ancillary table is
not redistributed: its source, hash, and historical validation are recorded,
and an explicit download helper can restore it for a fresh table comparison.
The analytic EOS, thermodynamic checks, and kinetic evolution run offline
without that optional table. Original numerical results and the report are
preserved; the publication pass adds metadata and optional-validation handling.

## Sources and attribution

The thermal source is pinned at
`Cbaird26/mqgt-scf-continued@48f9dcbd34e7cfb86504167a0483f732a5dd5e8e`.
The audited UV source is pinned at
`Cbaird26/uv-reconstruction-frg@0a644a41eb947509280cbd648996d98bad54bdc5`.
The public count data are Pedalino et al., DOI
[10.5281/zenodo.17502163](https://doi.org/10.5281/zenodo.17502163), CC BY 4.0;
the new reanalysis is separate and is not endorsed by the data authors.
See `THIRD_PARTY_NOTICES.md`, `CITATION.cff`, and `sources/source_catalog.json`.

The previous frozen verification release remains the historical record.
