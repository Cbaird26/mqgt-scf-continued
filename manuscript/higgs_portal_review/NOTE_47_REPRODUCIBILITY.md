# Note 47 — Reproduction and scope

Run from this directory with Python, NumPy, SciPy and mpmath. The recorded environment is Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0 and mpmath 1.3.0. These are the executed versions, not a claim of compatibility with every environment.

```sh
python -m unittest -v test_research_note_40.py test_research_note_42.py test_research_note_43.py test_research_note_44.py test_note45_rg_matching.py test_research_note_46.py test_research_note_47.py
python reproduce_note47.py central
python reproduce_note47.py
```

The first command runs 197 tests, including 26 new tests. It excludes the separate live 45-real and standalone 41 suites; this is not the entire repository. The second command regenerates only three central pair results. The third regenerates all six numerical prescriptions and writes RESULTS_NOTE_47_REGENERATED.json incrementally. It does not read the historical result file. Full reproduction took several minutes in the recorded environment; no timing guarantee is made.

Compare the `runs` object of regenerated output against RESULTS_NOTE_47.json. The `fine` prescription is the central numerical result quoted in the note. Quadrature refinements are diagnostics, not physical uncertainty estimates.

Read the source-normalization audit before using these numbers. The helicity amplitudes are source-derived, while the decay prefactor is separately reconstructed from soft radiation and identical-particle phase space. The literal printed subtraction fails the recorded limiting checks. This is not an author-confirmed erratum. A signed finite real remainder is not a positive standalone decay channel or complete NLO rate. No abundance, lifetime or empirical validation follows.

Publication status is in the commit/ref receipt supplied with the conversation package. The local package also preserves the failed initial test, successful hash-matched run, numerical output and an additions-only patch. No earlier source file is replaced by that patch.
