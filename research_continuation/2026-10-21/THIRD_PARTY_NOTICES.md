# Third-party notices and attribution

Checkpoint: `v2026.10.21-research-continuation` (21 October 2026).

## Scope of the root license

The root `LICENSE` contains Creative Commons Attribution 4.0 International
([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)), matching the
existing MQGT-SCF continued-development repository. It applies to new
continuation material to the extent the project can license that material.
It does not replace source-specific licenses, claim ownership of upstream
work, or grant rights over the separately supplied research archive.

Christopher Michael Baird is the human project author and maintainer.
ChatGPT assisted with calculations, code, documentation and internal
cross-checks. AI assistance does not imply external peer review, empirical
replication, or endorsement by any cited researcher. Use `CITATION.cff`
for this checkpoint and cite the original sources for their contributions.

## Inherited thermal checkpoint

- Source: [Cbaird26/mqgt-scf-continued](https://github.com/Cbaird26/mqgt-scf-continued).
- Pinned source revision: `48f9dcbd34e7cfb86504167a0483f732a5dd5e8e`.
- Source path: `manuscript/higgs_portal_review/checkpoints/2026-10-21-free-bath/`.
- Source license: [CC BY 4.0](https://github.com/Cbaird26/mqgt-scf-continued/blob/48f9dcbd34e7cfb86504167a0483f732a5dd5e8e/LICENSE).
- Delivered inherited files: `thermal/frozen/`; file acquisition hashes and
  archive reconstruction details are retained in `thermal/source_provenance.json`.
- The frozen source and restored numerical banks remain attributed to the
  upstream project. New preparation and EOS sensitivity calculations are
  documented separately and are not retroactively attributed to the old run.

## Inherited ultraviolet source

- Source: [Cbaird26/uv-reconstruction-frg](https://github.com/Cbaird26/uv-reconstruction-frg).
- Pinned revision: `0a644a41eb947509280cbd648996d98bad54bdc5`.
- Source license: CC BY 4.0, preserved verbatim as `uv/upstream/LICENSE`.
- Delivered original files: `uv/upstream/`; hashes are recorded in
  `uv/provenance.json`.
- New projection and convention diagnostics are separate continuation work.
  The underlying papers retain their named authorship in the source catalog.

## Public sodium-cluster data and author code

Sebastian Pedalino, Bruno Eduardo Ramirez Galindo, Richard Ferstl,
Klaus Hornberger, Markus Arndt, and Stefan Gerlich,
*Probing quantum mechanics with nanoparticle matter-wave interferometry —
Dataset and code*, [DOI 10.5281/zenodo.17502163](https://doi.org/10.5281/zenodo.17502163).

- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as
  identified by the source record; metadata are preserved in
  `measurement/sources/zenodo_metadata.json`.
- The original ZIP and extracted source files are preserved under
  `measurement/sources/`. Its verified MD5 is
  `7917961b27676f4e9df3af6d3b01c374`; SHA-256 is
  `b92355d06e06f16b3c746020ef7bc6c6eac6a629d36d739aff79e6a894003b9a`.
- The new count-level fits, diagnostics and inference protocol are separately
  authored analyses. They do not imply endorsement by the dataset authors.
- Associated article: [DOI 10.1038/s41586-025-09917-9](https://doi.org/10.1038/s41586-025-09917-9).

Keep the original authors, source link, license link and modification statement
with any redistribution of these data or code.

## QCD equation of state and optional ancillary table

Szabolcs Borsányi, Zoltán Fodor, Christian Hoelbling, Sándor D. Katz,
Stefan Krieg and Kálmán K. Szabó, *Full result for the QCD equation of state
with 2+1 flavors*, Physics Letters B **730** (2014), 99–104,
[DOI 10.1016/j.physletb.2014.01.007](https://doi.org/10.1016/j.physletb.2014.01.007),
[arXiv:1309.5258v2](https://arxiv.org/abs/1309.5258v2).

The [SCOAP3 publisher record](https://repo.scoap3.org/records/975) identifies
The Authors as copyright holders and the published article as
[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). The present EOS
implementation cites its analytic central fit and the pressure prescription
in Borsányi et al., *The QCD equation of state with dynamical quarks*,
[arXiv:1007.2580v2](https://arxiv.org/abs/1007.2580v2).

The separately linked `WB-EoS.dat` ancillary file has no embedded license;
the arXiv submission points to the
[arXiv non-exclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/).
No separate general redistribution grant was located for that ancillary file.
The published article's CC BY 3.0 label is therefore not asserted to relicense
the separate data file. The raw table is excluded from the public package.

- Original source URL: <https://arxiv.org/src/1309.5258v2/anc/WB-EoS.dat>.
- SHA-256: `5f39782b65fcadf36a84c84afc57855cf7d20bc1f0b96f9d28c51737916b9550`.
- Optional explicit retrieval: `python thermal/fetch_eos_validation_table.py`.
- The helper verifies the pinned hash and is never called automatically.
- The kinetic evolution uses the analytic fit; it does not require this table.
- Without the table, reruns explicitly skip only the source-table comparison.
  Analytic EOS, derivative, quadrature and kinetic checks continue normally.
- `thermal/eos/historical_table_validation.json` records the previously executed
  comparison, identifies the source hash, and labels the results as historical.
  It is not evidence that an absent-table rerun repeated that comparison.

The two research-reading source PDFs are also excluded. Source URLs and hashes
remain in `thermal/eos/source_provenance.json`. No new lattice simulation or
endorsement by the EOS authors is claimed.

## Uploaded archive and other references

The supplied 9,252-page Baird research archive is identified by filename,
SHA-256 and physical page ranges in `sources/source_catalog.json`. The archive
itself is not redistributed with this continuation. Original books, unrelated
uploads and the personal image are not part of the package.

The source catalog records the theoretical papers used for normalization and
projection comparisons. Their authors retain credit. Mathematical formulas
are implemented and discussed with their assumptions stated; citing a source
does not imply its authors endorse the continuation's hypotheses.
