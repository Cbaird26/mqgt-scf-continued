"""Reprocess supplied scattering banks and report independent sensitivities."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from expanding_free_bath import ScatteringBank, evolve, cell_data, T0, TF

HERE=Path(__file__).resolve().parent
OBSERVABLES=['heavy_fraction','Tkin_over_T','mean_kinetic_energy_GeV',
             'total_variation_to_common_fugacity_MB','total_variation_to_same_species_MB']


def select(result,T):
    return min(result['rows'],key=lambda r:abs(r['T_GeV']-T))


def compare(coarse,fine):
    rows=[]
    for T in [.4,TF]:
        a,b=select(coarse,T),select(fine,T)
        rows.append(dict(T_GeV=T,absolute_change={k:b[k]-a[k] for k in OBSERVABLES},
                         relative_change={k:(b[k]-a[k])/b[k] for k in OBSERVABLES}))
    return rows


def main(final_q=48, final_bank=None):
    finalpath=Path(final_bank) if final_bank else HERE/f'bank_q{final_q}_eta16.npz'
    if not finalpath.exists():finalpath=HERE/f'bank_q{final_q}.npz'
    finebank=ScatteringBank(finalpath)
    fine_intervals=finebank.metadata['eta_intervals']
    configs={
        'fine':(finalpath,1,1,None,192),
        'grid96':(finalpath,2,1,None,192),
        'grid48':(finalpath,4,1,None,192),
        'temperature_half':(finalpath,1,2,None,192),
        'time96':(finalpath,1,1,None,96),
        'time48':(finalpath,1,1,None,48),
        'tail36':(finalpath,1,1,36.,192),
    }
    for q in [24,40]:
        if q<final_q and (HERE/f'bank_q{q}.npz').exists():
            configs[f'q{q}']=(HERE/f'bank_q{q}.npz',1,1,None,192)
    results={}
    for label,(path,ag,ts,tail,steps) in configs.items():
        bank=ScatteringBank(path,ag,ts,tail)
        results[label]=evolve(bank,steps)
        print(label,{k:results[label]['rows'][-1][k] for k in ['heavy_fraction','Tkin_over_T']},flush=True)
    fine=results['fine']
    changes={
        'grid_48_to_96':compare(results['grid48'],results['grid96']),
        'grid_96_to_192':compare(results['grid96'],fine),
        f'temperature_{fine_intervals//2}_to_{fine_intervals}_intervals':compare(results['temperature_half'],fine),
        'time_48_to_96_steps':compare(results['time48'],results['time96']),
        'time_96_to_192_steps':compare(results['time96'],fine),
        'tail_start_36_to_48':compare(results['tail36'],fine),
    }
    # Quadrature comparisons must use the same temperature nodes.
    reference8=fine if fine_intervals==8 else results['temperature_half']
    if 'q24' in results:
        changes['quadrature_24_to_40']=compare(results['q24'],results.get('q40',reference8))
    if 'q40' in results:
        changes[f'quadrature_40_to_{final_q}']=compare(results['q40'],reference8)
    result=dict(final_quadrature=final_q,final_bank=finalpath.name,model='expanding ideal free-bath scattering only',
                final_result=fine,refinement_changes=changes,
                refinement_changes_are_certified_error_bounds=False,
                controls={label:{'final':{k:v for k,v in run['rows'][-1].items() if k!='comoving_cell_masses'},
                                  'at_T0p4':{k:v for k,v in select(run,.4).items() if k!='comoving_cell_masses'}}
                          for label,run in results.items()},
                max_number_error=max(abs(row['comoving_number_relative_to_initial']-1)
                                     for run in results.values() for row in run['rows']),
                minimum_cell_mass=min(row['minimum_cell_mass'] for run in results.values() for row in run['rows']))
    (HERE/'scattering_convergence.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'scattering_final.json').write_text(json.dumps(fine,indent=2)+'\n')
    print('Wrote scattering_final.json and scattering_convergence.json')


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--final-q',type=int,default=48)
    p.add_argument('--final-bank')
    args=p.parse_args()
    main(args.final_q,args.final_bank)
