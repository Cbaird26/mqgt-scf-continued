"""Reproduce the loose amplitude-based tail bound for the declared model."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from scipy.special import kv

FERMIONS = [
    ("e", .00051099895, 1), ("mu", .1056583755, 1), ("tau", 1.77686, 1),
    ("u", .002, 3), ("d", .005, 3), ("s", .100, 3),
    ("c", 1.300, 3), ("b", 4.200, 3),
]
MH = 125.
COUPLINGS = ((.001, -.001), (-.001, .001))


def amplitude_maximum(mf, coupling, mh=MH):
    if mh * mh >= 8 * mf * mf:
        return coupling * coupling * mf * mf / (4 * (mh * mh - 4 * mf * mf))
    return 4 * coupling * coupling * mf**4 / mh**4


def calculate(T):
    if not math.isfinite(T) or T <= 0:
        raise ValueError("finite positive temperature required")
    H = math.sqrt(8 * math.pi**3 * 60 / 90) * T * T / 1.2209e19
    rows = []
    B = [0., 0.]
    for name, mf, Nc in FERMIONS:
        integral = mf * T * kv(1, mf / T) / (2 * math.pi**2)
        contributions = [
            sum(4 * Nc * amplitude_maximum(mf, k) * integral / (32 * math.pi)
                for k in couplings)
            for couplings in COUPLINGS
        ]
        for i, term in enumerate(contributions):
            B[i] += term
        rows.append(dict(
            flavor=name, mass_GeV=mf, bath_degeneracy=4*Nc,
            inverse_energy_MB_integral_GeV2=float(integral),
            amplitude_maximum_abs_coupling_0p001=amplitude_maximum(mf, .001),
            B_contribution_by_initial_species_GeV2=contributions,
        ))
    return dict(
        T_GeV=T, H_GeV=H, B_by_initial_species_GeV2=B,
        B_over_H_by_initial_species_GeV=[x/H for x in B],
        bound="nu_i(p) <= B_i(T)/E_i(p)",
        bound_is_not_actual_collision_rate=True,
        theorem_scope="globally extended vacuum-tree fixed ideal MB scattering-only operator",
        uniform_L2_variational_gap_of_scoped_operator=0.,
        physical_UV_completion_claim=False, rows=rows,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--temperature", type=float, default=.4)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("tail_bound_constants.json"))
    args = parser.parse_args()
    result = calculate(args.temperature)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))
