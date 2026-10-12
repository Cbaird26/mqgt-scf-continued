"""Reproduce Note 51 numbers; no external data or network access."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import leptonic_conversion_scattering as c

def results():
    comparisons=[]
    for T in (0.5,0.4,1/3):
        for flavor,m in c.LEPTONS.items():
            for mi,mj,direction in ((c.M2,c.M1,"down"),(c.M1,c.M2,"up")):
                a=c.rate_MB(T,mi,mj,m)
                b=c.rate_MB(T,mi,mj,m,method="q-angle")
                comparisons.append({"T_GeV":T,"flavor":flavor,"direction":direction,
                    "w_GeV":a.value_GeV,"q_angle_GeV":b.value_GeV,
                    "relative_difference":b.value_GeV/a.value_GeV-1})
    return {
        "scope":"Vacuum-tree lepton scattering with kinetic MB scalars and an ideal bath",
        "parameters":{"m1_GeV":c.M1,"m2_GeV":c.M2,"mh_GeV":c.MH,"K12":c.K12,
                      "lepton_masses_GeV":c.LEPTONS,"bath_degeneracy_per_flavor":4,
                      "assumed_gstar":60.0,"w_max":c.W_MAX},
        "temperature_results":[c.rates_at_temperature(T) for T in (0.5,0.4,1/3)],
        "independent_thermal_comparisons":comparisons,
        "maximum_relative_thermal_difference":max(abs(v["relative_difference"]) for v in comparisons),
        "restricted_MB_relaxation_H_crossing_T_GeV":c.relaxation_crossing_temperature(),
        "crossing_is_freeze_out_prediction":False,
        "FD_integral_explicitly_evaluated":False,
        "FD_scattering_bracket_derived":True,
        "full_conversion_network_computed":False,
        "chemical_equilibrium_established":False,
        "kinetic_equilibrium_established":False,
        "relic_density_computed":False
    }

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default="RESULTS_NOTE_51.json")
    args=parser.parse_args()
    Path(args.output).write_text(json.dumps(results(),indent=2,allow_nan=False)+"\n")
    print("Saved",args.output)
