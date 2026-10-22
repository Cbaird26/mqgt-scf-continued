"""Cross-representation validation of the nested free-bath calculation.

Uses the separately rerun upstream six-moment matrix and two quadratures.
Checks numerical consistency; no physical-error/full-spectrum certificate.
"""
import json
from pathlib import Path
import numpy as np
from scipy.special import roots_genlaguerre,kve
from nested_free_bath import metric_data,eigenvalues

HERE=Path(__file__).resolve().parent
high=json.loads((HERE/'results_q80.json').read_text())
low=json.loads((HERE/'results_q48.json').read_text())
coarse=json.loads((HERE/'results_q24.json').read_text())
base=json.loads((HERE.parent/'baseline_six_moment.json').read_text())
old=next(x for x in base['rows'] if x['T_GeV']==high['T_GeV'])
T=high['T_GeV']; GS,GV,GQ=metric_data(T)
new=high['leptons_plus_free_quarks']
S=np.array(new['gram_scalar_per_N_GeV']);V=np.array(new['gram_drift_per_N_GeV'])
A=np.eye(4);A[0,2]=-GS[0,2]/GS[0,0];A[1,3]=-GS[1,3]/GS[1,1]
D=np.zeros((6,6));D[:4,:4]=A.T@S[:4,:4]@A;D[4:,4:]=V[:2,:2]
oldD=np.array(old['D_per_N_GeV'])
relative_frobenius=np.linalg.norm(D-oldD)/np.linalg.norm(oldD)
Gcenter=np.zeros((6,6));Gcenter[:4,:4]=A.T@GS[:4,:4]@A;Gcenter[4:,4:]=GV[:2,:2]
metric_error=np.linalg.norm(Gcenter-np.diag(old['metric']))/np.linalg.norm(old['metric'])
assert relative_frobenius<1e-8
assert metric_error<1e-10
result={'T_GeV':T,'independent_baseline_matrix_relative_Frobenius_error':float(relative_frobenius),
        'direct_metric_vs_upstream_relative_Frobenius_error':float(metric_error),
        'quadrature_refinement':{},'interlacing':{},'boost_normalization_max_error':0.,
        'certified_physical_uncertainty':False,'certified_full_spectral_gap':False}
for name in ['scalar_degree1_over_H','scalar_degree2_over_H','drift_degree0_over_H','drift_degree1_over_H','quadrupole_degree0_over_H']:
    hi=np.array(new[name]);lo=np.array(low['leptons_plus_free_quarks'][name]);c=np.array(coarse['leptons_plus_free_quarks'][name])
    err=float(np.max(np.abs((hi-lo)/hi)));errc=float(np.max(np.abs((hi-c)/hi)))
    assert err<1e-8
    assert np.all(hi>0)
    result['quadrature_refinement'][name]={'q48_to_q80_max_relative_change':err,'q24_to_q80_max_relative_change':errc}
for sector,oldname,newname in [('scalar','scalar_degree1_over_H','scalar_degree2_over_H'),('drift','drift_degree0_over_H','drift_degree1_over_H')]:
    a=np.array(new[oldname]);b=np.array(new[newname]);gap=len(b)-len(a)
    assert np.all(b[:len(a)]<=a+1e-12)
    assert np.all(a<=b[gap:]+1e-12)
    result['interlacing'][sector]=True
    result[sector+'_slow_rate_fractional_decrease']=float(1-b[0]/a[0])
for n in [8,12,20]:
    v,w=roots_genlaguerre(n,.5)
    for z in [20.,25.,100.,400.]:
        err=abs(float(np.sum(w*np.sqrt(2*z+v)/(z*kve(1,z))))-1)
        result['boost_normalization_max_error']=max(result['boost_normalization_max_error'],err)
assert result['boost_normalization_max_error']<1e-12
assert new['number_null_relative_residual']<1e-14
result['number_null_relative_residual']=new['number_null_relative_residual']
result['metric_condition_numbers']={'scalar_degree2':float(np.linalg.cond(GS)),
                                   'drift_degree1':float(np.linalg.cond(GV)),
                                   'quadrupole_degree0':float(np.linalg.cond(GQ))}
result['all_assertions_passed']=True
(HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
