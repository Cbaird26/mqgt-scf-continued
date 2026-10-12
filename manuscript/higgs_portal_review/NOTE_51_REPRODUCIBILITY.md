# Note 51 — Reproduction

This is a tree-level charged-lepton scattering partial, not an abundance prediction.

For the new calculation alone, in this directory with NumPy, SciPy and mpmath installed:

```
python -m unittest -v test_research_note_51
python reproduce_note51.py --output RESULTS_NOTE_51.json
```

The first command runs 31 new tests. The second regenerates all three temperatures and eighteen forward/reverse numerical comparisons. NOTE_51_RESULTS_SUMMARY.json contains selected results and the SHA-256 of the full JSON retained in the conversation archive.

The 308-test result uses the conversation package's unchanged inherited Note-50 archive (277 tests), including its LOCAL Note-49 lineage. It is not a claim that the alternate live-repository lineage was run. For that exact combined run, use the package README and inherited/ sources. The original standalone Note-41 and 45-real test suites are excluded.

The package also supplies full results, execution logs, source hashes, an additions-only patch and separate publication/clean-extraction receipts. No old patch, historical note, or main-branch file should be overwritten.
