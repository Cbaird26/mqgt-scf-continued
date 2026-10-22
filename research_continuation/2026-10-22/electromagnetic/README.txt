SPECTRAL PROFILE NONUNIQUENESS AT A COMMON VACUUM
Research continuation prepared for Christopher Michael Baird with ChatGPT
User-facing date: 21 October 2026 (America/New_York)

RESULT
For every finite local order in the stipulated positive-exponential spectral
action class, profiles exist with the same local data, stationary radius,
flat-vacuum subtraction, and gravitational coefficient but different
hypercharge coefficients. See the PDF and research_note.tex for the proof.

This is a noninjectivity result for the declared class. It does not say that
every prescribed data vector has multiple solutions, and does not derive the
measured fine-structure constant. Positive restricted potential curvature
does not establish full radion or compactification stability.

FILES
- research_note.tex: complete manuscript source.
- Spectral_Profile_Common_Vacuum_2026-10-21.pdf: compiled research note.
- stationary_profiles.py: high-precision ten-component example (standard library).
- stationary_profiles_results.json: recorded profile weights and results.
- certify_seed.py: exact-rational seed existence and simplicity certificate.
- stationary_seed_certificate.json: complete rational bounds and comparisons.
- independent_check.py: separate float64 sums and bracketed radius checks.
- independent_check_results.json: independent numerical results.
- provenance.json: source references, environment and verification scope.
- SHA256SUMS.txt: hashes of the package files, excluding this manifest itself.

REPRODUCE
With Python 3.10 or newer:

  python3 stationary_profiles.py
  python3 certify_seed.py

The core calculations use only the Python standard library. Each command
overwrites only its own result JSON beside the script. No network calls occur.

For the optional independent floating-point check, install NumPy and SciPy,
then run:

  python3 independent_check.py

Recorded runtime versions are in provenance.json. The independent script
reads stationary_profiles_results.json. Its numerical rank and root results
are diagnostics, not interval-certified results for that ten-node support.

The seed certificate uses exact Fraction arithmetic for every assertion.
Decimal is used there only for displaying outward-rounded bounds. The main
ten-node example uses 95-digit Decimal arithmetic with 40 internal levels,
checked against 60 levels. It is separate from the exact seed certificate.

Compile the manuscript with a standard LaTeX installation:

  pdflatex -interaction=nonstopmode research_note.tex
  pdflatex -interaction=nonstopmode research_note.tex

ATTRIBUTION AND STATUS
The action and coefficient definitions are inherited from the pinned
2026-10-21 electromagnetic continuation listed in provenance.json.
The proof extension, common-vacuum numerical example, and seed certificate
were produced in this conversation using AI-assisted reasoning and mutually
checked calculations. They have not undergone external peer review.
No repository or publication record was changed in preparing this package.
