# Synthetic causal-memory experiment

Everything in this directory is synthetic and reproducible. It is an operational memory experiment, not evidence of consciousness or a physical field.

```bash
python synthetic_causal_memory.py
```

Dependencies are NumPy and Matplotlib plus Python's standard library. The recorded environment uses Python 3.12.14 and NumPy 2.3.5. Runtime is a few seconds. No network, training service or external data is needed.

The program checks the prewritten protocol hash before generating data, then recreates both source conditions from their fixed seeds and overwrites the generated result JSON, trial-score CSV and plot. Mathematical results and data hashes are deterministic for the recorded environment; run timestamps change on reruns. It does not overwrite the protocol or its original lock record.

| File | Purpose |
|---|---|
| `protocol.json` | Design fixed before the first simulation |
| `protocol.sha256` | Byte-exact hash checked by the executable |
| `protocol_lock.json` | Local record made before first data generation |
| `synthetic_causal_memory.py` | Source, interventions, train-only prediction, bootstrap and validation |
| `synthetic_memory_results.json` | Aggregate losses, paired intervals, checks, hashes and scope |
| `held_out_trial_scores.csv` | All 800 held-out trial score records with source, donor and cluster IDs |
| `synthetic_memory_interventions.png` | Paired effect plot |
| `RESEARCH_NOTE.md` | Findings, reasoning, limitations and further bridge requirements |

The confidence intervals preserve whole trajectories and both donor-linked trials. They describe held-out uncertainty conditional on the trained predictor. The local protocol lock is not external preregistration. No human or physical-field observations are included.
