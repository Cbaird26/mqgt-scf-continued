# Two-singlet EFT and experimental interfaces — public technical review

**Status:** Author-approved public *draft* on a review branch; NOT peer reviewed, not journal-submitted, not a GitHub release, not a DOI mint, and not an experimental finding. The PR is unmerged; frozen independent-verification release and original corpus are unchanged.

This package develops a restricted symmetric-vacuum, two-real-singlet effective theory motivated by the MQGT-SCF source archive, plus conditional open-system and H2 interfaces. It does not verify MQGT-SCF as a Theory of Everything or establish any consciousness/ethical scalar interpretation.

- `COMPREHENSIVE_WORKING_PAPER_2026-09-21.md`: broad working-paper synthesis of Research Notes 01–13; derived and illustrative results are distinguished from unresolved links.
- `DUAL_SINGLET_HIGGS_PORTAL_DRAFT.md`: narrower standalone collider working paper.
- `RESEARCH_NOTE_14_DECAY_AUDIT.md`: subsequent *development addendum*, not silently incorporated into the already dated working paper. It internally rechecks the illustrative leptonic partial-width arithmetic and derives the conditional quartic `s2 -> 3s1` threshold. Full heavy-state lifetime remains unverified.
- `CLAIMS_AND_RELEASE_GATE.md`: evidence/assumption ledger and outstanding release gates; its original 01–13 status snapshot should be read alongside the Note 14 addendum.
- `higgs_portal_checks.py`, `h2_audit_checks.py` and `test_research_note_14.py`: 17 local tests in aggregate (6 + 5 + 6); checks of toy equations and numerical examples only, not validation of experimental physics or the complete theory.

**Provenance:** Initial draft assembled 2026-09-21 against the original source corpus and continued-development repository. Exact edition/page/equation mapping, current literature and independent referee review remain required before a released preprint or journal submission.

**Authorship / AI assistance:** Christopher Michael Baird is the human author. ChatGPT (ZoraASI) assisted with research-note drafting, algebra, code and consistency checking. No independent coauthor, referee, experiment, or machine sentience claim is made. Existing repository licensing terms apply subject to owner's final publication metadata decision. No third-party copyrighted compilations are redistributed here.

## Subsequent development (Notes 15–21; not silently backported into dated papers)

Notes 15–17 audit model-conditional spectral/fermion formulas and threshold problems; Notes 18–20 map a possible partial pion/kaon form-factor source and its as-yet-unretrieved numerical Omnès inputs. **Note 21** (`RESEARCH_NOTE_21_SPECTRAL_SENSITIVITY_AND_OFFLINE_DATA_GATE.md`) gives an exact weighted-mean spectral-ratio identity: the 0.414% toy kinematic weight below 2 GeV cannot determine any QCD decay fraction, and a hypothetical 50% low-window contribution would require a low/high weighted-mean spectral-strength ratio ~240.61. This is a sensitivity exercise, not a QCD prediction.

`safe_omnes_manifest.py` is an original offline size/Git blob-digest verifier for four pinned upstream Omnès files; its separate raw SHA-256 receipt and escaped byte sample require actual local files. `test_research_note_21.py` has 15 passing local tests using **synthetic file fixtures and algebra only**. The original numerical Omnès files remain unavailable/unparsed; no hadronic central width or tighter lifetime has been computed. Once all four files have been independently obtained, run `python3 safe_omnes_manifest.py /absolute/path/to/hipsofcobra/input`. All prior physics, review, licensing and publication gates remain open, and the conditional toy-model leptonic-only `c*tau_2 <= ~17.06 cm` is unchanged.
