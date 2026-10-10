# Note-45 numbering and publication crosswalk — 10 October 2026

Two complementary documents independently received number 45. Neither supersedes or replaces the other. Use full titles or the descriptive labels **45-real** and **45-RG** in cross-references; keep the source titles/dates unchanged.

| Record | Exact source / identity | Meaning |
|---|---|---|
| Note 44 | RESEARCH_NOTE_44_MIXED_GLUON_NLO_AND_MASS_SCHEME.md; mixed_gluon_nlo.py blob 0ffc28870c414cc8613d28549511d10bcaf30ee7 | Initially local on 30 September. Already recovered on the live branch by the inspected head 994b7f12af99e228bda0fe0e9dcaa5dae2d8dff4. The old failed-publication statement is historical. |
| 45-real | RESEARCH_NOTE_45_COHERENT_BC_FINITE_REAL_RADIATION.md; bc_real_radiation.py blob 7a1404c8cc99b335b376f943c3a4abc2e1963a15 | Existing live 1 October real-emission calculation. Its test_research_note_45.py, RESULTS_NOTE_45.json and NOTE_45_EXECUTION_RECORD.json are preserved. |
| 45-RG | RESEARCH_NOTE_45_COHERENT_BC_RG_AND_MATCHING.md; coherent_bc_rg.py blob b95d7bdd1cf8a467df9f5df2e54112d073f8579a | Separate local 1 October scale/mass-matching calculation. Its original text and code are recovered without content edits alongside Note 46. |
| 45-RG tests | test_note45_rg_matching.py, blob 181b1c088dbb49d4efa89966adf4b14bfa09deda | Byte-identical to the local archive's test_research_note_45.py; filename changed only to avoid the live real-radiation test. |
| 45-RG results/history | RESULTS_NOTE_45_RG.json; NOTE_45_RG_EXECUTION_RECORD_ARCHIVE.json | Byte-identical original RG results and historical execution record, stored under collision-safe names. Historical paths inside the record identify the original local archive, not the live real-radiation files. |
| Note 46 | RESEARCH_NOTE_46_COHERENT_BC_FINITE_VIRTUAL.md | New mass-dependent finite virtual coefficient. Does not claim completion of real/virtual/subtraction assembly. |

The older local NOTES_44_45_BRANCH_READY.patch and NOTE_45_BRANCH_READY.patch target a branch state before 45-real. They would collide with the now-existing test and result names and **must not be applied as-is** to the current branch. The Note-46 package instead supplies an additions-only patch with the unique names above. No prior note, test, result or main-branch file is replaced.

The 171-test execution for Note 46 includes 30 tests from **45-RG**, not the 29-test **45-real** suite. It also excludes the original standalone Note-41 suite. Count those separately and never equate the combined run with the whole repository.

Publication is evidenced by the commit containing this crosswalk and the associated new files, not by rewriting dated failure statements. The conversation package's publication receipt records the actual resulting commit and branch status. It reports a failed write instead if recovery does not succeed.
