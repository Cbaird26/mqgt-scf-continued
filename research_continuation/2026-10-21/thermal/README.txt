THERMAL CONTINUATION DELIVERABLE
21 October 2026

Start with SCIENTIFIC_NOTE.txt for the twelve initial-condition runs and
eos/EOS_NOTE.txt for the entropy-consistent background-EOS sensitivity.

Commands from this directory (Python with NumPy, SciPy and Matplotlib):

  OPENBLAS_NUM_THREADS=1 python run_continuation.py
  python make_report.py
  OPENBLAS_NUM_THREADS=1 python eos_sensitivity.py
  python make_eos_report.py
  python verify_provenance.py

The numerical calculations use supplied raw collision banks, require no network
access, and write results separately from frozen sources. The two numerical
suites took about 28 and 24 seconds in the recorded environment. New runs and
environment versions are documented in results/run_metadata.json and EOS JSON.

Principal machine-readable outputs:
  results/scan_summary.csv and .json
  results/initial_condition_scan.json
  results/validation.json and review_summary.json
  eos/eos_summary.csv
  eos/eos_sensitivity_results.json
  eos/eos_review_summary.json

Figures:
  results/thermal_initial_condition_sensitivity.png and .svg
  eos/eos_sensitivity.png and .svg

The frozen source is pinned to Cbaird26/mqgt-scf-continued commit
48f9dcbd34e7cfb86504167a0483f732a5dd5e8e. Source URLs and hashes are in
source_provenance.json. EOS source URLs and download hashes are in
eos/source_provenance.json; the authors' WB-EoS.dat table is supplied.
The original acquisition provenance is preserved. Current local verification
writes provenance_verification.json as a separate report and explicitly records
any absent redundant binary parts as unverified local files, while checking the
complete reconstructed banks.
The archived source PDFs are research-reading intermediates and can be omitted
from a distribution; the public links identify the exact paper versions.

frozen/ contains the needed scripts, notes, banks and diagnostics, not a complete
mirror of the repository or original release. Run the continuation commands above.
Do not use the original reproduce_all.py as a substitute: it writes inside its
own frozen tree and expects additional original diagnostic files.

Compact bundles may omit frozen/_archive/artifact_parts/ because the exact NPZ
banks reconstructed from those raw parts are supplied. verify_provenance.py
accepts only this specific redundancy, verifies the reconstructed-bank hashes,
and reports any omitted parts. If reacquisition is needed, download_frozen.py
performs read-only pinned public downloads and restore_banks.py validates the
exact concatenation. Network access is needed only for reacquisition.

independent_measurement_review.py is a read-only cross-review of the neighboring
measurement module. Its result is in results/independent_measurement_review.json.
It needs the neighboring measurement source data; it is not required to reproduce
the thermal calculations.

Scientific scope: finite-window, ideal collision-bath benchmarks with imposed
initial preparations. The EOS variants change the homogeneous background and
redshift consistently but do not supply interacting-QCD collision kernels. No
earlier cosmological preparation, physical relic abundance, or completed Theory
of Everything is claimed.
