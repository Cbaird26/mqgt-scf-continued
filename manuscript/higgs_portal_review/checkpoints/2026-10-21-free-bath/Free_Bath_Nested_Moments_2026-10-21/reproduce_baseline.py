"""Reproduce the inherited six-moment free-bath benchmark without source edits."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "upstream"))
import kinetic_moment_audit as km
from leptonic_conversion_scattering import LEPTONS, hubble


def reproduce():
    flavors = [(name, mass, 1) for name, mass in LEPTONS.items()]
    flavors += [("u", .002, 3), ("d", .005, 3), ("s", .100, 3),
                ("c", 1.300, 3), ("b", 4.200, 3)]
    rows = []
    for T in [1 / 3, .4, .5]:
        _, metric = km.equilibrium_metric(T)
        D = np.zeros((6, 6))
        channels = []
        for name, mass, colors in flavors:
            block = colors * sum(
                (km.collision_gram(T, mass, pair) for pair in ("11", "21", "22")),
                start=np.zeros((6, 6)),
            )
            D += block
            channels.append(dict(name=name, mass_GeV=mass, colors=colors,
                                 D_per_N_GeV=block.tolist()))
        rates = km.projected_rates(D, metric)
        H = hubble(T)
        rows.append(dict(
            T_GeV=T,
            counts_over_H=rates["counts_only_relaxation_GeV"] / H,
            density_energy_over_H=(np.array(rates["scalar_eigenvalues_GeV"]) / H).tolist(),
            drift_over_H=(np.array(rates["drift_eigenvalues_GeV"]) / H).tolist(),
            metric=metric.tolist(), D_per_N_GeV=D.tolist(), channels=channels,
        ))
    return dict(
        model="declared free MB bath, tree Higgs propagator, source commit994e51cb28b51ade500bb0e1902f3b082ef8e594",
        rows=rows,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "baseline_six_moment.json")
    args = parser.parse_args()
    result = reproduce()
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(args.output)
    for row in result["rows"]:
        print(row["T_GeV"], row["counts_over_H"],
              row["density_energy_over_H"][0], row["drift_over_H"][0])
