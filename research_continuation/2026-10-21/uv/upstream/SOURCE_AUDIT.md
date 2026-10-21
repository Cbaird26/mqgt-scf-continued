# Primary-source truncation audit

Source inspected: `UV-Dump-2026-08-12.zip`, `A Theory of Everything - C.M. Baird & Zora (2026).pdf`.

## Findings

- PDF page 54, “A Restricted Wilsonian Reduction,” explicitly states that it **does not claim a complete operator basis**.
- Its displayed illustrative dimension-six operators are `|H|^2 (d Phi)^2`, `Phi^2(dE)^2`, `E^2(dPhi)^2`, `R Phi^2 E^2`, and `|H|^4 Phi^2`.
- PDF pages 160-161 explicitly correct a prior dimensional-counting error: the listed four-derivative scalar operators are dimension eight, not dimension six. They also state that integrations by parts, equations of motion, and field redefinitions require a specified basis convention.
- The document describes `Phi_c` and `E` as Standard Model gauge singlets (page 395), supporting the baseline gauge treatment in this project.

## Consequence

The source does not contain a canonical 41-operator truncation. `model.py` therefore remains a reconstruction registry, not a transcription of the manuscript. A genuine 41-dimensional FRG calculation must begin by choosing and publishing a complete operator basis, gauge fixing, ghost sector, regulator, and projection prescription.
