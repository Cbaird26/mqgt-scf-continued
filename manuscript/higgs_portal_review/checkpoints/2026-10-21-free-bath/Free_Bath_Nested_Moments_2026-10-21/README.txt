FREE-BATH NESTED-MOMENT CONTINUATION
Prepared 2026-10-21 UTC

Purpose
-------
This package advances the original six-moment ideal-bath calculation by
enlarging its scalar and drift spaces and adding a quadrupole sector.
It also records dependencies among the ten next steps supplied in the
Grok post. This is an AI-assisted research continuation for Christopher
Michael Baird. It has received internal computational review, not external
peer review. It does not promote an experimental or theoretical gate.

Main result
-----------
At T=0.4 GeV, in the declared ideal Maxwell-Boltzmann bath of charged
leptons and five free quark species:

  scalar slow rate/H:  0.788181031 -> 0.747848884  (5.117117% decrease)
  drift slow rate/H:   0.521608084 -> 0.510586637  (2.112975% decrease)
  new quadrupole/H:                     0.920803280
  restricted count-only rate/H:         2.974745765

The enlarged spaces also lower their slow rates at T=1/3 and T=0.5 GeV.
See RESEARCH_NOTE.txt and numerics/three_temperature_summary.json.

These are finite-space diagnostics and numerical estimates of variational
upper bounds. They are not lower bounds on the full spectral gap, a
physical QCD calculation, a time-dependent cosmological solution, or an
abundance prediction. The complete task "beyond finite-moment limits"
remains open.

Reproduction
------------
Extract the archive, enter this directory, and use Python with NumPy and
SciPy. Supplied outputs were produced using Python 3.12.14, NumPy 2.3.5,
and SciPy 1.17.0. Exact package versions are in requirements.txt.

  python -m pip install -r requirements.txt
  python reproduce_all.py

The second command overwrites the bundled numerical output files. It
reproduces the independent upstream baseline, all five extended runs,
central-temperature validation, and the three-temperature summary.
Runtime here was approximately a minute in total; hardware may differ.
Reported elapsed-time fields and floating-point last digits need not
match byte-for-byte.

To validate the supplied results without repeating the collision integrals:

  python numerics/verify_nested_results.py
  python numerics/summarize_temperatures.py

To reproduce only the central high-resolution result:

  OPENBLAS_NUM_THREADS=1 python numerics/nested_free_bath.py --temperature 0.4 --q 80 --boost 20 --scattering 20 --direction 6 --azimuth 12 --output numerics/results_q80.json

Contents
--------
RESEARCH_NOTE.txt: physical assumptions, method, results, interpretation.
NEXT_STEPS.txt: dependency map and acceptance conditions for all ten items.
provenance.json: pinned upstream sources and targeted collection pages.
requirements.txt: computational package versions used.
reproduce_all.py: local full reproduction entry point.
reproduce_baseline.py: reruns the original analytic/Bessel six-moment code.
baseline_six_moment.json: original independently rerun benchmark matrices.
numerics/nested_free_bath.py: self-contained explicit-boost implementation.
numerics/verify_nested_results.py: central matrix/refinement checks.
numerics/summarize_temperatures.py: three-temperature matrix/nesting checks.
numerics/results_*.json: complete per-flavor matrices and all retained rates.
numerics/verification.json: detailed central verification results.
numerics/three_temperature_summary.json: compact final numerical comparison.
upstream/: five unchanged, byte-verified inherited source files.
SHA256SUMS.txt: digests of all other package files at delivery.

Attribution and source handling
------------------------------
Inherited files are from Cbaird26/mqgt-scf-continued, commit
994e51cb28b51ade500bb0e1902f3b082ef8e594, under
manuscript/higgs_portal_review/. Original attribution and applicable
upstream terms remain with those files. This package does not relicense
the inherited material. New implementation, checks, and explanatory text
were prepared with ChatGPT assistance during this continuation.

The source collection was inspected at the page ranges recorded in
provenance.json; the entire 9,252-page collection was not audited. That
collection is not duplicated inside this archive.
