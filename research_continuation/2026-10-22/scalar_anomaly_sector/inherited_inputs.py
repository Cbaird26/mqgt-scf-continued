"""Reload and re-verify the inherited common-vacuum profile pair; recompute Z_Y, Z_X.

Standard library only.  Reads inputs/common_vacuum_pair.json (byte-identical
copy of the published stationary_profiles_results.json) and
inputs/inherited_weak_coefficients.json (transcript-printed Z_W values).

Writes inherited_inputs_results.json.  Every check is an assertion; the run
fails loudly if an inherited number cannot be reproduced.
"""
from decimal import Decimal as D, getcontext
from fractions import Fraction as Fr
from pathlib import Path
import json
import hashlib

import heatsums as hs

HERE = Path(__file__).resolve().parent
hs.set_precision(95)
PREC_TOL = D('1e-88')


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    pair_path = HERE / 'inputs' / 'common_vacuum_pair.json'
    weak_path = HERE / 'inputs' / 'inherited_weak_coefficients.json'
    pair = json.loads(pair_path.read_text())
    weak = json.loads(weak_path.read_text())

    checks = {}
    nodes = [D(x) for x in pair['nodes']]
    v = [D(x) for x in pair['null_vector']]
    w_minus = [D(x) for x in pair['weights_minus']]
    w_plus = [D(x) for x in pair['weights_plus']]
    R = D(pair['common_R'])

    # 1. node structure a_j = (178939/338184) j
    scale = Fr(178939, 338184)
    scale_dec = hs.frac_to_dec(scale)
    node_err = max(abs(a - scale_dec * j) for j, a in enumerate(nodes, 1))
    checks['nodes_are_rational_scale_times_j'] = node_err < D('1e-92')
    checks['node_scale_matches_file'] = abs(D(pair['node_scale']) - scale_dec) < D('1e-92')

    # 2. weights = 1/10 -/+ v/20
    wm_err = max(abs(wm - (D(1) / 10 - vj / 20)) for wm, vj in zip(w_minus, v))
    wp_err = max(abs(wp - (D(1) / 10 + vj / 20)) for wp, vj in zip(w_plus, v))
    checks['weights_are_tenth_plus_minus_v_over_20'] = max(wm_err, wp_err) < D('1e-92')
    checks['all_weights_positive'] = min(w_minus + w_plus) > 0
    checks['null_vector_max_norm_one'] = max(abs(x) for x in v) == 1

    # 3. recompute coefficients at the common radius (40 levels, then 60)
    results = {'precision': getcontext().prec, 'common_R': str(R), 'profiles': {}}
    recorded = pair['metrics']
    for name, w in (('minus', w_minus), ('plus', w_plus)):
        co40 = hs.profile_coefficients(nodes, w, R, levels=40)
        co60 = hs.profile_coefficients(nodes, w, R, levels=60)
        level_change = max(abs(co40[k] - co60[k]) for k in ('P', 'P_R', 'P_RR', 'J', 'zY', 'zX'))
        rec = recorded[name]
        diffs = {
            'P': abs(co60['P'] - D(rec['P'])),
            'P_R': abs(co60['P_R'] - D(rec['P_R'])),
            'J': abs(co60['J'] - D(rec['J'])),
            'c': abs(co60['c'] - D(rec['c'])),
            'K': abs(co60['K'] - D(rec['potential_curvature_factor'])),
            'zY': abs(co60['zY'] - D(rec['gY_inverse_squared_per_kappa'])),
            'u_grav': abs(co60['u_grav'] - D(rec['M4r_squared_per_kappa'])),
        }
        checks['recomputed_matches_recorded_' + name] = max(diffs.values()) < PREC_TOL
        checks['stationarity_residual_small_' + name] = abs(co60['F']) < D('1e-88')
        checks['positive_curvature_' + name] = co60['K'] > 0
        checks['levels_40_vs_60_' + name] = level_change < D('1e-90')
        loc = hs.local_data(nodes, w)
        results['profiles'][name] = {
            'weights': [str(x) for x in w],
            'coefficients_60_levels': {k: str(co60[k]) for k in ('P', 'P_R', 'P_RR', 'J', 'F', 'c', 'K', 'u_grav', 'zY', 'zX')},
            'local_data': {k: str(val) for k, val in loc.items()},
            'max_abs_difference_to_recorded': str(max(diffs.values())),
            'levels_40_vs_60_max_change': str(level_change),
        }

    # 4. pair differences of retained constraints vanish; z_Y and z_X differ
    pm = results['profiles']['minus']
    pp = results['profiles']['plus']
    constraint_keys = ['m1', 'm2', 'm3', 'f0', 'minus_fprime0', 'fsecond0']
    pair_diff = {k: abs(D(pm['local_data'][k]) - D(pp['local_data'][k])) for k in constraint_keys}
    for k in ('P', 'P_R', 'J'):
        pair_diff[k] = abs(D(pm['coefficients_60_levels'][k]) - D(pp['coefficients_60_levels'][k]))
    checks['nine_retained_constraints_common'] = max(pair_diff.values()) < D('1e-90')
    dzY = D(pp['coefficients_60_levels']['zY']) - D(pm['coefficients_60_levels']['zY'])
    dzX = D(pp['coefficients_60_levels']['zX']) - D(pm['coefficients_60_levels']['zX'])
    checks['delta_zY_matches_recorded'] = abs(dzY - D(pair['delta_gY_inverse_squared_per_kappa'])) < D('1e-88')
    results['pair_constraint_differences'] = {k: str(val) for k, val in pair_diff.items()}
    results['delta_zY'] = str(dzY)
    results['delta_zX'] = str(dzX)

    # 5. inherited Z_W (transcript, 18 digits) and transcript-printed Z_X, Z_Y
    zW = {'minus': D(weak['zW_minus']), 'plus': D(weak['zW_plus'])}
    checks['transcript_delta_zW_consistent'] = abs((zW['plus'] - zW['minus']) - D(weak['delta_zW'])) < D('2e-18')  # inputs printed to 18 digits
    for name in ('minus', 'plus'):
        zY = D(results['profiles'][name]['coefficients_60_levels']['zY'])
        zX = D(results['profiles'][name]['coefficients_60_levels']['zX'])
        checks['zY_matches_transcript_18_digits_' + name] = abs(zY - D(weak['predecessor_printed_zY_' + name])) < D('1e-17')
        checks['zX_matches_transcript_16_digits_' + name] = abs(zX - D(weak['predecessor_printed_zX_' + name])) < D('1e-14')
        results['profiles'][name]['zW_inherited'] = str(zW[name])
        results['profiles'][name]['zgamma_tree'] = str(zW[name] + zY)
    dzg = (zW['plus'] + D(pp['coefficients_60_levels']['zY'])) - (zW['minus'] + D(pm['coefficients_60_levels']['zY']))
    checks['delta_zgamma_matches_transcript'] = abs(dzg - D(weak['predecessor_printed_delta_zgamma'])) < D('2e-18')  # limited by 18-digit Z_W
    results['delta_zgamma_tree'] = str(dzg)
    results['relative_delta_zgamma_to_minus'] = str(dzg / (zW['minus'] + D(pm['coefficients_60_levels']['zY'])))
    checks['relative_delta_zgamma_matches_transcript'] = abs(D(results['relative_delta_zgamma_to_minus']) - D(weak['predecessor_printed_relative_delta_zgamma'])) < D('1e-17')
    checks['zX_positive_both'] = min(D(pm['coefficients_60_levels']['zX']), D(pp['coefficients_60_levels']['zX'])) > 0

    # 6. predecessor fixture masses (s = kappa = 1, minus profile, chi = 0, equal vevs, no Stueckelberg)
    zYm = D(pm['coefficients_60_levels']['zY'])
    zXm = D(pm['coefficients_60_levels']['zX'])
    mX2 = 1 / zXm
    mZ2 = (D(1) / 4) * (1 / zW['minus'] + 1 / zYm)
    checks['fixture_mX2_matches_transcript'] = abs(mX2 - D(weak['predecessor_printed_fixture_mX2_minus_s1_kappa1'])) < D('1e-14')
    checks['fixture_mZ2_matches_transcript'] = abs(mZ2 - D(weak['predecessor_printed_fixture_mZ2_minus_s1_kappa1'])) < D('1e-14')
    results['predecessor_fixture_reproduction'] = {'mX2_minus_s1_kappa1': str(mX2), 'mZ2_minus_s1_kappa1': str(mZ2)}

    # 7. pure-exponential control (October 21 note): R_e = 1.3007832832273603, zY = 0.3303631229653509
    Re, iters = hs.newton_stationary_radius([D(1)], [D(1)], D('1.3008'), levels=60)
    coe = hs.profile_coefficients([D(1)], [D(1)], Re, levels=60)
    checks['pure_exponential_radius_control'] = abs(Re - D('1.3007832832273603')) < D('1e-15')
    checks['pure_exponential_zY_control'] = abs(coe['zY'] - D('0.3303631229653509')) < D('1e-15')
    checks['pure_exponential_root_in_certified_interval'] = D('1.30078') < Re < D('1.30079')
    results['pure_exponential_control'] = {'R_e': str(Re), 'zY': str(coe['zY']), 'zX': str(coe['zX']), 'K': str(coe['K']), 'newton_iterations': iters}

    # 8. input file identities
    results['inputs'] = {
        'common_vacuum_pair.json': {'sha256': sha256(pair_path), 'origin': 'byte-identical copy of research_continuation/2026-10-22/electromagnetic/stationary_profiles_results.json at commit 3a8a1b029e2923ce3fde3335fbc710ebf618a38b (git blob b5c6ec3ab0ef7a42419ef9e612acaa7f5fe7b931)'},
        'inherited_weak_coefficients.json': {'sha256': sha256(weak_path), 'origin': 'transcript-printed predecessor values; see file'},
    }
    results['checks'] = checks
    results['caveat'] = ('High-precision numerical reproduction of the inherited pair, not an interval certificate. '
                         'Z_W is inherited from the predecessor note and is not recomputed here.')
    failed = [k for k, ok in checks.items() if not ok]
    (HERE / 'inherited_inputs_results.json').write_text(json.dumps(results, indent=2))
    print('inherited_inputs: %d checks, %d failed' % (len(checks), len(failed)))
    for k in failed:
        print('  FAILED', k)
    if failed:
        raise SystemExit(1)
    for name in ('minus', 'plus'):
        p = results['profiles'][name]
        print(' %s: zW=%s zY=%s zX=%s' % (name, p['zW_inherited'], p['coefficients_60_levels']['zY'][:22], p['coefficients_60_levels']['zX'][:22]))
    print(' delta zY =', results['delta_zY'][:30], ' delta zX =', results['delta_zX'][:30], ' delta zgamma =', results['delta_zgamma_tree'][:30])


if __name__ == '__main__':
    main()
