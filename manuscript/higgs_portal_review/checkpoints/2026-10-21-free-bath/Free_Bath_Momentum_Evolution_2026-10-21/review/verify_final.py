"""Independent forward-mass exponential check of the final radial output."""
from pathlib import Path
import json
import math
import numpy as np
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
source = json.loads((HERE.parent / 'solver/final_evolution.json').read_text())
D = np.array(source['D_per_N_GeV'])
cell = np.array(source['cell_moments'])
pi = cell[:, :, 0].ravel()
T = source['T_GeV']
H = math.sqrt(8 * math.pi**3 * 60 / 90) * T*T / 1.2209e19
Q = -D / pi[None, :] / H
P = expm(Q)
ev = source['evolution']
result = {
    'T_GeV': T,
    'comparison_time_Ht': 1.,
    'method': 'Direct scipy.linalg.expm of forward mass generator, compared with stored whitened-eigenbasis evolution',
    'minimum_transition_probability': float(P.min()),
    'maximum_transition_column_sum_error': float(np.max(np.abs(P.sum(axis=0)-1))),
    'stationary_mass_maximum_absolute_error': float(np.max(np.abs(P@pi-pi))),
    'cases': {},
}
assert P.min() > -1e-14
assert result['maximum_transition_column_sum_error'] < 1e-12
assert result['stationary_mass_maximum_absolute_error'] < 1e-12
for name, case in ev['initial_conditions'].items():
    g0 = np.array(case['initial_g']).ravel()
    expected = next(row for row in case['rows'] if row['tau_Ht'] == 1.)
    stored_g = np.array(expected['g_by_species']).ravel()
    actual_mass = P @ (pi*g0)
    error = float(np.max(np.abs(actual_mass - pi*stored_g)))
    h = g0-1
    correlation = float(np.dot(h, actual_mass-pi) / np.sum(pi*h*h))
    correlation_error = abs(correlation-expected['autocorrelation_relative_to_initial'])
    result['cases'][name] = {
        'maximum_absolute_cell_mass_error': error,
        'autocorrelation_absolute_error': correlation_error,
        'minimum_evolved_cell_mass': float(actual_mass.min()),
    }
    assert error < 1e-12
    assert correlation_error < 1e-10
result['all_checks_passed'] = True
(HERE / 'independent_exponential_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
