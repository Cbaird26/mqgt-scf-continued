"""Regenerate controlled expanding-network comparisons from supplied raw banks."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import time

import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'network'))
from evolve_network import evolve


def main():
    output=HERE/'results';output.mkdir(exist_ok=True)
    shared=dict(scatter_path=HERE/'solver/bank_q48_eta16.npz',
                pair_path=HERE/'network/pair_bank_eta16.npz',
                decay_path=HERE/'network/decay_bank_eta16.npz')
    cases={
        'full_final':{},
        'full_time96':{'steps':96},
        'full_grid96':{'aggregation':2},
        'full_temperature8':{'temperature_stride':2},
        'full_tail40':{'tail_ymax':40.},
        'scattering_and_decay':{'use_annihilation':False},
        'scattering_only':{'use_annihilation':False,'use_decay':False},
        'full_quadrature40_temperature8':{
            'scatter_path':HERE/'solver/bank_q40.npz',
            'pair_path':HERE/'network/pair_bank.npz',
            'decay_path':HERE/'network/decay_bank.npz'},
    }
    results={}
    for name,override in cases.items():
        start=time.perf_counter()
        results[name]=evolve(**(shared|override))
        (output/(name+'.json')).write_text(json.dumps(results[name],indent=2)+'\n')
        end=results[name]['rows'][-1]
        print(name,'seconds',round(time.perf_counter()-start,2),
              'Tkin/T',end['Tkin_over_T'],'heavy',end['heavy_fraction'],
              'numberloss_ppm',1e6*(1-end['comoving_number_relative_to_initial']),flush=True)
    observable_keys=['Tkin_over_T','heavy_fraction','total_variation_to_common_fugacity_MB',
                     'total_variation_to_same_species_MB','mean_kinetic_energy_GeV']
    def comparison(coarse,fine):
        a=results[coarse]['rows'][-1];b=results[fine]['rows'][-1]
        difference={key:{'coarser':a[key],'finer':b[key],
                         'finer_minus_coarser':b[key]-a[key],
                         'relative_change':(b[key]-a[key])/b[key]} for key in observable_keys}
        loss_a=1-a['comoving_number_relative_to_initial'];loss_b=1-b['comoving_number_relative_to_initial']
        difference['annihilation_number_loss_fraction']={
            'coarser':loss_a,'finer':loss_b,'finer_minus_coarser':loss_b-loss_a,
            'relative_change':(loss_b-loss_a)/loss_b}
        return difference
    pairs={
        'time96_to192':('full_time96','full_final'),
        'grid96_to192':('full_grid96','full_final'),
        'temperature8_to16':('full_temperature8','full_final'),
        'tail40_to48':('full_tail40','full_final'),
        'quadrature40_to48_at_temperature8':('full_quadrature40_temperature8','full_temperature8'),
    }
    checks={}
    for name,r in results.items():
        rows=r['rows']
        check={'positive_populations':r['minimum_comoving_cell_mass']>0,
               'max_linear_number_error':r['max_single_linear_step_number_error'],
               'maximum_number_increase':float(np.max(np.diff([x['comoving_number_relative_to_initial'] for x in rows])))}
        if not r['channels']['annihilation_and_inverse']:
            check['conserved_number_error']=max(abs(x['comoving_number_relative_to_initial']-1) for x in rows)
            assert check['conserved_number_error']<1e-12
        assert check['positive_populations']
        assert check['max_linear_number_error']<1e-12
        assert check['maximum_number_increase']<1e-12
        checks[name]=check
    summary={
        'T_initial_GeV':.5,'T_final_GeV':1/3,'model_scope':'leading-portal-order free-fermion network; fixed gstar=gstar_s=60',
        'final_source':'results/full_final.json','all_structural_checks_pass':True,
        'refinement_changes_are_certified_errors':False,
        'refinements':{name:comparison(a,b) for name,(a,b) in pairs.items()},
        'checks':checks,
        'endpoint_cases':{name:{k:v for k,v in r['rows'][-1].items() if k!='comoving_cell_masses'} for name,r in results.items()},
    }
    (output/'convergence_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('All structural checks passed. Refinement changes are sensitivities, not certified error bounds.')


if __name__=='__main__':main()
