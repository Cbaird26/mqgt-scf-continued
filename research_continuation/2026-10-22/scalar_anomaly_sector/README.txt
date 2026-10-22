A Microscopic Scalar and Anomaly-Complete Sector for the Shared Spectral Action
Baird / ZoraASI research continuation, 22 October 2026
Prepared for Christopher Michael Baird with Claude.

Reproduction (from this directory):

    python3 run_all.py              # stdlib scripts, then independent_check.py if numpy+scipy import
    python3 run_all.py --no-float   # skip independent_check.py; core scripts need only the
                                    # standard library (6 NumPy checks run if NumPy is present)

Order and dependencies:
    inherited_inputs.py  -> inherited_inputs_results.json   (reads inputs/*.json)
    scalar_sector.py     -> scalar_sector_results.json      (reads inherited_inputs_results.json)
    anomaly_sector.py    -> anomaly_sector_results.json
    vacuum_matching.py   -> vacuum_matching_results.json    (reads the three above)
    independent_check.py -> independent_check_results.json  (reads all; needs numpy, scipy)

Each script asserts its own checks and exits non-zero on failure; the result
files record every check.  Expected totals: 28 + 26 + 16 + 125 + 33 = 228
(189 standard library only, 39 need NumPy/SciPy).  Review record: REVIEW_RESPONSE.md.

Manuscript: research_note.tex (pdflatex, run twice).  Compiled copy:
Scalar_Anomaly_Sector_Coupled_Vacuum_2026-10-22.pdf.

Assumptions: ASSUMPTIONS.md.  Provenance and hashes: provenance.json, SHA256SUMS.txt.
License: CC BY 4.0 (LICENSE).  No network or publication actions are performed by any script.
