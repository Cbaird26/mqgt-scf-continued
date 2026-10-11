# Note 49 reproduction and evidence scope

Run from `manuscript/higgs_portal_review/` in the review branch or the extracted package directory. Use Python with NumPy, SciPy, mpmath and SymPy. The execution record gives exact versions used; installing dependencies is not itself a validation.

```sh
python -m unittest -v test_research_note_40.py test_research_note_42.py test_research_note_43.py test_research_note_44.py test_note45_rg_matching.py test_research_note_46.py test_research_note_47.py test_research_note_48.py test_research_note_49.py
python prove_note49.py
python reproduce_note49.py > RESULTS_NOTE_49_REGENERATED.json
```

Expected scope: 251 tests, including 24 new tests. The new reproducer evaluates 72 complex virtual-coefficient comparisons and the three central pair virtual contributions. It does not rerun the full six-prescription Note-48 decay assembly. Original Note-41 and 45-real standalone test suites are excluded from this count. This is not a whole-repository audit.

`abdv_virtual_check.py` independently transcribes hep-ph/0611266v3. It imports no old virtual/mixed/assembly/RG hard coefficient; it shares the inherited QCD-running and thermal-kernel module. `abdv_reference.py` checks special functions at high precision while sharing the new ABDV rational expressions. `prove_note49.py` compares the two transcribed coefficient expressions symbolically in a common HPL branch convention. This distinction is essential to what is independent.

The recovered Note-48 files preserve their earlier dates and publication-failure text. The new recovery memo and package publication receipt record their later publication. No completed physical NLO rate, new field, empirical observation, Omnes input or relic abundance is claimed. The independently reviewed real-emission normalization remains an outstanding calculation.
