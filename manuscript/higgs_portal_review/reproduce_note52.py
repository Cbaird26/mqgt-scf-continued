"""Reproduce the finite-window Note-52 moment matrices and diagnostics."""
from pathlib import Path
import json
import numpy as np
import kinetic_moment_audit as k

def reproduce():
    rows=[k.evaluate(T) for T in (.5,.4,1/3)]
    comparisons=[]
    for T in (.5,1/3):
        for flavor,ml in k.base.LEPTONS.items():
            for pair in ('11','21','22'):
                a=k.collision_gram(T,ml,pair)
                b=k.collision_gram(T,ml,pair,method='q')
                comparisons.append({'T':T,'flavor':flavor,'pair':pair,
                   'relative_frobenius_difference':float(np.linalg.norm(a-b)/np.linalg.norm(a))})
    o=rows[0];fine=k.evaluate(.5,n=48)
    coarse=k.evaluate(.5,n=16)
    a=np.array(o['D_MB_per_N_GeV']);b=np.array(fine['D_MB_per_N_GeV'])
    tail={str(T):sum(k.omitted_normalized_form_bound(T,ml,pair)/k.base.hubble(T)
                     for ml in k.base.LEPTONS.values() for pair in ('11','21','22')) for T in (.5,.4,1/3)}
    r=np.array(o['fractions']);metric=np.array(o['metric_per_N'])
    elastic=np.zeros((6,6));conv=np.zeros((6,6))
    for row in o['channels']:
        for pair,D in row['channels_gram_per_N_GeV'].items():
            if pair=='21':conv+=np.array(D)
            else:elastic+=np.array(D)
    return {'research_date':'2026-10-12','scope':'near-stationary lepton-scattering moments only',
       'model':{'m1':k.M1,'m2':k.M2,'mh':k.MH,'K11':k.K11,'K12':k.K12,'K22':k.K22},
       'temperatures':rows,'independent_q_w_checks':comparisons,
       'max_q_w_relative_frobenius_difference':max(x['relative_frobenius_difference'] for x in comparisons),
       'refinement_24_48_angular_relative_gram_difference':float(np.linalg.norm(a-b)/np.linalg.norm(b)),
       'central_16_node_scalar_rates_over_H':coarse['MB_projected']['scalar_eigenvalues_over_H'],
       'central_elastic_energy_rates_over_H':[float(elastic[i,i]/metric[i]/o['H_GeV']) for i in (2,3)],
       'central_elastic_drift_rates_over_H':[float(elastic[i,i]/metric[i]/o['H_GeV']) for i in (4,5)],
       'omitted_mathematical_MB_tail_normalized_form_bound_over_H':tail,
       'basis':'density1,density2,centered_energy1,centered_energy2,drift1_z,drift2_z',
       'FD_brackets':'Loewner order for the PROJECTED matrices; not a full-spectrum lower bound',
       'full_kinetic_spectrum_computed':False,'full_FD_integral_computed':False,
       'QCD_response_computed':False,'decay_moment_matrix_included':False,
       'chemical_or_kinetic_equilibrium_established':False,'abundance_computed':False}

if __name__=='__main__':
    result=reproduce()
    out=Path('RESULTS_NOTE_52.json');out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for row in result['temperatures']:
        print(row['T_GeV'],row['MB_projected']['scalar_eigenvalues_over_H'],row['MB_projected']['drift_eigenvalues_over_H'])
    print(out)
