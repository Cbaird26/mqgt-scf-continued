# Research continuation — 21 October 2026

**Status:** executed, conditional research checkpoint. A complete Theory of
Everything and experimental confirmation of new fields are not established.

[Planned release](https://github.com/Cbaird26/mqgt-scf-continued/releases/tag/v2026.10.21-research-continuation) · [Release notes](RELEASE_NOTES.md) ·
[Claim status](sources/claim_status.json) · [Citation](CITATION.cff)

**Publication status (21 October 2026):** the source files are public. The
GitHub Release and downloadable assets are pending publication. The download
helper and URLs in `RELEASE_ASSETS.json` become usable after that release is
published; local source verification works now.

## What is here

The six workstreams are `common/`, `thermal/`, `measurement/`,
`electromagnetic/`, `uv/`, and `agency/`. This Git directory contains their
source code and compact records. The prepared complete offline ZIP contains
larger trajectories, plots, numerical banks, and binary experimental inputs.
`SOURCE_SNAPSHOT_MANIFEST.json` identifies every included source file and all
offline-only files. `PACKAGE_MANIFEST.json` records the complete offline package.

## Reproduce the checkpoint

Verify this compact source directory:

```bash
python verify_source_snapshot.py
```

Once the release is published, download the complete offline package with
its recorded SHA-256:

```bash
python download_offline_package.py
```

Extract that downloaded ZIP into a separate directory. In the extracted
`toe_continuation_2026-10-21` directory, use Python 3.12 and run:

```bash
python -m pip install -r requirements.txt
python reproduce.py
python reproduce.py --rerun --include-thermal
```

The offline ZIP supplies the inputs absent from this compact Git directory.
The optional EOS ancillary table is fetched only on explicit request; its
historical comparison is preserved and the analytic EOS calculation works
offline without it. See the package README and third-party notices.

## Reading order

1. The 13-page PDF prepared for the release for the scientific narrative.
2. `sources/claim_status.json` for completed and unresolved claims.
3. `common/action_parameter_contract.json` for conventions and missing inputs.
4. Each workstream's technical note, results, and executable scripts.
5. `sources/` for source hashes, environment, and verification records.

The source revisions audited by this checkpoint remain pinned in the source
catalog. Internal AI-assisted checks are described as internal verification.
Measured public count data and synthetic memory trials are explicitly labeled.

## Attribution

See [LICENSE](LICENSE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), and
[CITATION.cff](CITATION.cff). The public count data are Pedalino et al., DOI
[10.5281/zenodo.17502163](https://doi.org/10.5281/zenodo.17502163).
