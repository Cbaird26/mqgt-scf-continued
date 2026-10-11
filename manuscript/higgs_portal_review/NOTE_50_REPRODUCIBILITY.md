# Note 50 reproduction and scope

11 October 2026. New source: antenna_normalization_audit.py; new tests: test_research_note_50.py.

On the review branch, run from manuscript/higgs_portal_review:

```
python -m unittest -v test_research_note_50
python antenna_normalization_audit.py > RESULTS_NOTE_50_REGENERATED.json
```

The new suite contains 24 tests. The conversation package also contains the unchanged 253-test LOCAL Note-49 lineage; the combined 277-test execution uses that lineage, not the live branch's alternate 251-test implementation. See NOTE_50_EXECUTION_RECORD.json for commands, hashes, versions, failed invocation history and scope. Do not overwrite live Note-49 files with the package's inherited variants or apply obsolete recovery patches.

This checks the independent local-operator antenna normalization, regulated real integrals, pole cancellation and universal finite coefficient. The published virtual Laurent term is an input, not a newly calculated loop amplitude. It does not independently rederive every massive helicity function, compute a complete annihilation rate, or determine an abundance.

Required libraries: NumPy, SciPy, SymPy; inherited tests additionally use mpmath. No external executable or experimental dataset is run.
