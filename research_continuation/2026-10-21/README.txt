THEORY OF EVERYTHING RESEARCH CONTINUATION - 21 OCTOBER 2026
=========================================================

Checkpoint version: v2026.10.21-research-continuation
Human author and project maintainer: Christopher Michael Baird
Canonical development repository: https://github.com/Cbaird26/mqgt-scf-continued

This package carries forward six recommended research workstreams from the
uploaded Baird archive and pinned Cbaird26 repositories. It contains executed
calculations, public-data reanalysis, a prespecified synthetic experiment,
source provenance, and explicit scientific completion criteria.

The calculations are conditional on declared models. The package establishes
neither a complete Theory of Everything nor a discovery of a new field. It
records actual progress while preventing missing physical input from silently
becoming a numerical assumption.

START HERE
  reports/Theory_of_Everything_Continuation_2026-10-21.pdf
  common/action_parameter_contract.json
  CITATION.cff
  THIRD_PARTY_NOTICES.md

WORKSTREAMS
  common/          Action conventions, parameter dependencies, tree widths,
                   basis covariance and cross-route matching identities.
  thermal/         Frozen-bank momentum evolution, initial fugacity and
                   preparation sensitivity, entropy-consistent published-EOS
                   sensitivity, provenance and numerical checks.
  measurement/     All 95 public sodium-cluster power scans independently fit
                   at count level; residual checks and contrast/attenuation
                   identifiability; apparatus completion protocol.
  electromagnetic/ Exact finite-family spectral-profile constraints,
                   stationary-radius scans and a six-node counterexample.
  uv/              Pinned partial-flow reproduction, exact scalar-potential
                   Taylor projection, convention audit and nonlinear probes.
  agency/          Entirely synthetic causal-memory intervention experiment,
                   frozen train/test protocol, controls and uncertainty.
  sources/         Cross-workstream source and claim-status records.

REPRODUCIBILITY
Python 3.12 was used. Required packages for the calculation scripts are NumPy,
SciPy, pandas, openpyxl and matplotlib. Creating the report additionally needs
reportlab. The recorded dependency versions are in sources/environment.json.
No network access is required to recompute the analytic EOS, kinetic evolution
and other delivered calculations using the included frozen collision banks and
public experimental inputs. The separate optional fit-to-source-table check
requires WB-EoS.dat, which is not redistributed; when absent, that check is
explicitly skipped and its maxima are null, while other validation continues.

Verify all delivered bytes (default; does not modify outputs):
  python reproduce.py

Rerun the common, measurement, electromagnetic, UV and synthetic-memory work:
  python reproduce.py --rerun

Also rerun the thermal momentum network and EOS sensitivity:
  python reproduce.py --rerun --include-thermal

The optional --reference-uv-difference flag recomputes the slower upstream
nested finite-difference comparison. The normal UV run still recomputes the
new scalar projections and audits; it preserves the recorded comparison if
the pinned source commit matches.

Rerunning changes generated timestamps and may change last-bit floats across
library versions. The delivery manifest is a record of the original package,
not an assertion that new execution timestamps should have identical hashes.
Original source files and frozen banks must remain unchanged.

The source PDF is identified by name, page numbers and SHA256 in the source
catalog; its 9252 pages are not duplicated in this code package. Every formula
needed to run the new computations is in the supplied scripts and notes.
The complete restored collision banks are included. Redundant split copies of
those same bytes and research-reading EOS PDFs are omitted. Source acquisition
hashes remain recorded; verification distinguishes present files from omitted
redundant copies. The EOS fit coefficients and the historical table-comparison
record are included. The authors' raw WB-EoS.dat ancillary table is excluded
from public distribution because its separate redistribution terms were not
explicitly identified. To retrieve and verify that optional input, run:
  python thermal/fetch_eos_validation_table.py
The helper is never invoked automatically. After retrieval, rerun the thermal
suite to repeat the table comparison. See THIRD_PARTY_NOTICES.md for details.

The full notes record inherited versus new results, normalization conventions,
assumptions, checks, interpretation limits and the next concrete scientific
dependency. Pinned upstream snapshots retain their original contents. This
dated continuation is published as a new checkpoint rather than a revision
of an earlier frozen verification record.

LICENSE, CITATION AND ASSISTANCE
New continuation material is distributed under Creative Commons Attribution
4.0 International, consistent with the destination development repository.
See LICENSE and https://creativecommons.org/licenses/by/4.0/. This designation
does not replace the licenses or rights of third-party material identified
in THIRD_PARTY_NOTICES.md. Cite this checkpoint using CITATION.cff, and retain
the source-specific acknowledgments when reusing inherited material or data.

Christopher Michael Baird is the human project author and maintainer. ChatGPT
assisted with analysis, code, documentation and internal cross-checks for this
continuation. Those checks are internal AI-assisted checks, not external peer
review or independent experimental replication. No cited-source author is
represented as endorsing or coauthoring the new continuation.

OFFLINE-RUN EVIDENCE
The preserved raw log is sources/offline_reproduction_stdout.txt. Its SHA-256
and the original run status are recorded in
sources/offline_reproduction_validation.json. The original run verified 281
files before its receipt was added; the initial delivered package therefore
had 282 manifest-listed files. Publication notices and the preserved log are
later additions. Use PACKAGE_MANIFEST.json for the current release inventory.

ATTRIBUTION
Public sodium-cluster data and author code: Pedalino, Ramirez Galindo, Ferstl,
Hornberger, Arndt and Gerlich, DOI 10.5281/zenodo.17502163, CC BY 4.0. The original
zip is preserved with verified MD5/SHA256. The new reanalysis is separate and
is not endorsed by those authors. Their associated article is DOI
10.1038/s41586-025-09917-9. Keep this attribution with any redistribution.

Pinned upstream repository files retain their original author notices and
licenses. The new calculations do not transfer authorship of the cited work.

SCIENTIFIC STATUS
The common UV/low-energy action is not yet fully matched; QCD collision rates,
earlier population history, laboratory scalar state, composite detector
response, physical spectral-profile selection and a field-to-experience
bridge remain explicit dependencies. See sources/claim_status.json and the
report for the exact completion requirements.

PUBLICATION REBUILD
This offline distribution was reconstructed from the pinned public source checkpoint.
Previously recorded compact sources and results are preserved byte-for-byte. Missing
large outputs were regenerated; numeric/boolean reference checks passed, and the
13-page report has identical normalized extracted text to the reviewed report.
The ZIP and rendering bytes have new hashes. See sources/github_rebuild_validation.json.

CHECKSUM INVENTORIES
thermal/SHA256SUMS_CONTINUATION describes the thermal files in this rebuilt ZIP.
Its earlier reference list is preserved in sources/historical_continuation_SHA256SUMS.txt.
The pinned upstream thermal/frozen/SHA256SUMS remains its original archival inventory;
that upstream inventory also lists diagnostics outside this package's documented scope.
