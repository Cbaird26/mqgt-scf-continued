# Note 52 — Reproduction and scope

The standalone new calculation requires Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0; tests also use mpmath 1.3.0. The inherited chain additionally uses SymPy 1.14.0. These are recorded working versions, not claims that other versions cannot work.

From the extracted package root:

```sh
export PYTHONPATH="baseline/note51:baseline/note51/inherited"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python -m unittest -v test_research_note_52
python reproduce_note52.py
python -m unittest -v test_research_note_40 test_research_note_42 test_research_note_43 test_research_note_44 test_note45_rg_matching test_research_note_46 test_research_note_47 test_research_note_48 test_research_note_49 test_research_note_50 test_research_note_51 test_research_note_52
```

Inside the live repository's `manuscript/higgs_portal_review` folder the new 31-test suite needs no extra PYTHONPATH because Note 51's kernel is adjacent. The 339 count belongs to the supplied local inherited lineage, not the alternative live Note-49 suite. Never equate it with a whole-repository audit. Do not apply obsolete patches preserved in baseline historical files.

`RESULTS_NOTE_52.json` contains all calculated moment matrices, eigenvalues, quantum-statistics brackets and integration comparisons. The repository summary points to that generated output. Numerical digits reflect reproducibility, not physical precision. The code explicitly refuses a full-spectrum kinetic-equilibrium or QCD-response claim.

`NOTE_52_BRANCH_READY.patch` contains only the new files. Its apply check verifies additions to an empty path set; check the current branch before applying to avoid duplicate publication. No license is changed by this package. Existing rights and source attribution are preserved. No external code, laboratory data, Omnes arrays or cosmological solver was acquired or run.

Clean-package and remote-publication receipts are separate from the working execution record. Their presence is not inferred from the manifest.
