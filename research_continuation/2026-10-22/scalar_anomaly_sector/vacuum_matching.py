"""Coupled scalar/radius/anomaly-sector vacuum, broken-background neutral matrices,
null-space residue, massive spectrum, and the tree-level matching data.

Standard library only (decimal, fractions).  Reads the inherited-input results
and the scalar-sector results; writes vacuum_matching_results.json.

Units: lengths in 1/Lambda (so r = R/Lambda), canonical vevs squared in units
of kappa Lambda^2, neutral kinetic coefficients in units of kappa.  The scalar
sector is the a_4-truncated local heat-kernel action of the specified
Yukawa-fluctuated operator (ASSUMPTIONS.md, A3); the radius potential and the
gauge kinetic coefficients are the inherited exact internal mode sums.
"""
from decimal import Decimal as D, getcontext
from fractions import Fraction as Fr
from pathlib import Path
import json

import heatsums as hs

HERE = Path(__file__).resolve().parent
hs.set_precision(95)
PI = hs.pi()
checks = {}
results = {}


def record(name, ok):
    checks[name] = bool(ok)


def dsqrt(x):
    return x.sqrt()


# ---------------------------------------------------------------------------
# Inherited data
# ---------------------------------------------------------------------------
pair = json.loads((HERE / 'inputs' / 'common_vacuum_pair.json').read_text())
inh = json.loads((HERE / 'inherited_inputs_results.json').read_text())
nodes = [D(x) for x in pair['nodes']]
W = {'minus': [D(x) for x in pair['weights_minus']], 'plus': [D(x) for x in pair['weights_plus']]}
R_star = D(pair['common_R'])
m1 = D(inh['profiles']['minus']['local_data']['m1'])
m2 = D(inh['profiles']['minus']['local_data']['m2'])
zW = {k: D(inh['profiles'][k]['zW_inherited']) for k in W}
zY = {k: D(inh['profiles'][k]['coefficients_60_levels']['zY']) for k in W}
zX = {k: D(inh['profiles'][k]['coefficients_60_levels']['zX']) for k in W}

# ---------------------------------------------------------------------------
# Model parameters (declared fixture): identical copied blocks, 6D Yukawas y_6 = yhat/Lambda
# ---------------------------------------------------------------------------
N_B = 4
yu, yd, ye = D(1), D(1), D(1)
Nd = N_B * (3 * yd ** 2 + ye ** 2)
Nu = N_B * (3 * yu ** 2)
Lam_d = N_B * (3 * yd ** 4 + ye ** 4)
Lam_u = N_B * (3 * yu ** 4)
Lam_A = N_B * 6 * yu ** 2 * yd ** 2
results['fixture'] = {'N_blocks': N_B, 'yu': str(yu), 'yd': str(yd), 'ye': str(ye), 'N_d': str(Nd), 'N_u': str(Nu),
                      'Lam_d': str(Lam_d), 'Lam_u': str(Lam_u), 'Lam_A': str(Lam_A)}

# canonical quartics times kappa R^2 :  ell_i = lambda_i * kappa * R^2  (R-independent)
ell_d = 16 * PI ** 2 * Lam_d / (3 * m1 * Nd ** 2)
ell_u = 16 * PI ** 2 * Lam_u / (3 * m1 * Nu ** 2)
ell_3 = 8 * PI ** 2 * Lam_A / (3 * m1 * Nd * Nu)
record('all_quartics_positive_so_bounded_below', ell_d > 0 and ell_u > 0 and ell_3 > 0)
record('two_vev_stationary_point_is_minimum_4ldlu_gt_l3sq', 4 * ell_d * ell_u - ell_3 ** 2 > 0)
record('ell_u_equals_16pi2_over_9_m1_Nb', abs(ell_u - 16 * PI ** 2 / (9 * m1 * N_B)) < D('1e-85'))
results['canonical_quartics_times_kappa_R2'] = {'ell_d': str(ell_d), 'ell_u': str(ell_u), 'ell_3=ell_A': str(ell_3)}


def mu2hat(R, delta2=D(0)):
    """Doublet mass parameter mu^2/Lambda^2 at radius R: 2 m2/m1 - delta2 - 5/(6 R^2).

    delta2 = 0 is the untuned truncated action; delta2 > 0 parametrises an
    additional a_2-level contribution (assumption A5) that tunes mu^2 small.
    The 1/R^2 term (curvature coupling + lowest-harmonic eigenvalue) is kept at
    full strength in both cases.
    """
    return 2 * m2 / m1 - delta2 - D(5) / (6 * R * R)


def vev_solution(R, mu2):
    """Aligned minimum in units kappa Lambda^2: sigma_i = vhat_i^2/(kappa Lambda^2).

    Stationarity (canonical fields): 2 lam_d vd^2 + lam_3 vu^2 = 2 mu^2 and
    lam_3 vd^2 + 2 lam_u vu^2 = 2 mu^2 with lam_i = ell_i/(kappa R^2), so
    2 ell_d sigma_d + ell_3 sigma_u = 2 mu2 R^2 (and the u-equation).
    """
    rhs = 2 * mu2 * R * R
    det = 4 * ell_d * ell_u - ell_3 ** 2
    sd = (rhs * 2 * ell_u - ell_3 * rhs) / det
    su = (2 * ell_d * rhs - ell_3 * rhs) / det
    return sd, su


# gamma: sigma_d + sigma_u = gamma * mu2 * R^2 with (2 ell_d, ell_3; ell_3, 2 ell_u)(gamma_d, gamma_u) = (2, 2)
_det = 4 * ell_d * ell_u - ell_3 ** 2
gamma_d = (4 * ell_u - 2 * ell_3) / _det
gamma_u = (4 * ell_d - 2 * ell_3) / _det
GAMMA = gamma_d + gamma_u
results['gamma_vev_coefficient'] = {'gamma_d': str(gamma_d), 'gamma_u': str(gamma_u), 'gamma': str(GAMMA)}


def V_H_min_over_kappa_Lambda4(R, mu2):
    """-(mu^2 s)/4 at the aligned minimum, in units kappa Lambda^4."""
    sd, su = vev_solution(R, mu2)
    return -(mu2 * (sd + su)) / 4


def G_H(R, delta2=D(0)):
    """(4 pi^2/(kappa Lambda^4)) V_H^min(R) = - pi^2 gamma mu2(R)^2 R^2 : the scalar backreaction added to P_f(R)."""
    return 4 * PI ** 2 * V_H_min_over_kappa_Lambda4(R, mu2hat(R, delta2))


# The closed forms below hold where the doublet is tachyonic (mu2 > 0).  For mu2 <= 0 there is
# no vev, V_H^min = 0, and G_H and all its derivatives vanish.  The threshold radius is
# R_c = sqrt((5/6)/(2 m2/m1 - delta2)).
def _tachyonic(R, delta2):
    return mu2hat(R, delta2) > 0


def G_H_closed(R, delta2=D(0)):
    if not _tachyonic(R, delta2):
        return D(0)
    return -PI ** 2 * GAMMA * mu2hat(R, delta2) ** 2 * R * R


def Gtilde_closed(R, delta2=D(0)):
    """R G_H' - 2 G_H = -2 pi^2 gamma mu2 (mu2)' R^3 = -(10 pi^2/3) gamma mu2(R)  [since (mu2)' = (5/3)/R^3]."""
    if not _tachyonic(R, delta2):
        return D(0)
    return -(10 * PI ** 2 / 3) * GAMMA * mu2hat(R, delta2)


def dGtilde_closed(R, delta2=D(0)):
    if not _tachyonic(R, delta2):
        return D(0)
    return -(10 * PI ** 2 / 3) * GAMMA * (D(5) / 3) / R ** 3


def d2G_H_closed(R, delta2=D(0)):
    # G_H = -pi^2 gamma (A - B/R^2)^2 R^2 = -pi^2 gamma (A^2 R^2 - 2AB + B^2/R^2);  G'' = -pi^2 gamma (2A^2 + 6 B^2/R^4)
    if not _tachyonic(R, delta2):
        return D(0)
    A = 2 * m2 / m1 - delta2
    B = D(5) / 6
    return -PI ** 2 * GAMMA * (2 * A * A + 6 * B * B / R ** 4)


R_c_untuned = (D(5) / 6 / (2 * m2 / m1)).sqrt()
results['tachyon_threshold_radius_untuned'] = str(R_c_untuned)


# closed forms versus numerical differentiation (consistency of the algebra)
_h = D('1e-30')
record('G_H_closed_form_matches_direct', abs(G_H(R_star) - G_H_closed(R_star)) < D('1e-80'))
_num_Gt = R_star * (G_H(R_star + _h) - G_H(R_star - _h)) / (2 * _h) - 2 * G_H(R_star)
record('Gtilde_closed_form_matches_numerical_derivative', abs(_num_Gt - Gtilde_closed(R_star)) < D('1e-25'))


def coupled_stationary_radius(name, delta2, R0, levels=60):
    """Newton on F_tot(R) = F_f(R) + Gtilde(R) = 0 (flat-vacuum prescription applied to P_f + G_H)."""
    R = D(R0)
    for it in range(80):
        co = hs.profile_coefficients(nodes, W[name], R, levels=levels)
        Ft = co['F'] + Gtilde_closed(R, delta2)
        Ftp = R * co['K'] + dGtilde_closed(R, delta2)
        step = Ft / Ftp
        R -= step
        if abs(step) < D('1e-60'):
            break
    co = hs.profile_coefficients(nodes, W[name], R, levels=levels)
    Ptil = co['P'] + G_H_closed(R, delta2)
    ctil = Ptil / (R * R)
    Ktil = co['P_RR'] + d2G_H_closed(R, delta2) - 2 * ctil
    return {'R': R, 'c_tilde': ctil, 'K_tilde': Ktil, 'K_f_at_R': co['K'], 'iterations': it + 1, 'G_H': G_H_closed(R, delta2), 'P_f': co['P'],
            'F_residual': co['F'] + Gtilde_closed(R, delta2)}


# ---------------------------------------------------------------------------
# A. Coupled vacuum: untuned truncated action (no flat stationary radius) and hierarchical tunings
# ---------------------------------------------------------------------------
vac = {}
mu2_star = mu2hat(R_star)
sd0, su0 = vev_solution(R_star, mu2_star)
vac['at_common_radius_untuned'] = {
    'mu2_over_Lambda2': str(mu2_star),
    'sigma_d = vhat_d^2/(kappa Lambda^2)': str(sd0), 'sigma_u': str(su0), 's/(kappa Lambda^2)': str(sd0 + su0),
    'tan_beta^2 = vu^2/vd^2': str(su0 / sd0),
    'V_H_min/(kappa Lambda^4)': str(V_H_min_over_kappa_Lambda4(R_star, mu2_star)),
    'G_H = 4pi^2 V_H_min/(kappa Lambda^4)': str(G_H_closed(R_star)),
    'Gtilde = R G_H\' - 2 G_H': str(Gtilde_closed(R_star)),
    'P_f(R_star)': inh['profiles']['minus']['coefficients_60_levels']['P'],
    'F_f(R_star)': inh['profiles']['minus']['coefficients_60_levels']['F'],
}
record('vevs_positive_untuned', sd0 > 0 and su0 > 0)
Km = D(inh['profiles']['minus']['coefficients_60_levels']['K'])
Kp = D(inh['profiles']['plus']['coefficients_60_levels']['K'])
vac['at_common_radius_untuned']['first_order_delta_R_minus'] = str(-Gtilde_closed(R_star) / (R_star * Km))
vac['at_common_radius_untuned']['first_order_delta_R_plus'] = str(-Gtilde_closed(R_star) / (R_star * Kp))
record('untuned_first_order_shift_not_small', abs(Gtilde_closed(R_star) / (R_star * Km)) > D('0.1') * R_star)

# Scan of F_tot = F_f + Gtilde over the radius (30-digit arithmetic, adaptive levels so that a_1 L^2/R^2 >= 60)
import math
getcontext().prec = 30
scan = []
Fmax = D('-1e9')
Kmin_scan = D('1e9')
for Rs_ in [D(x) / 10 for x in range(1, 41)] + [D(x) for x in (5, 6, 7, 8, 10, 12, 15, 20, 30)]:
    L = int(math.ceil(float(Rs_) * 10.7)) + 5
    L = max(L, 40)
    co = hs.profile_coefficients(nodes, W['minus'], Rs_, levels=L)
    Ft = co['F'] + Gtilde_closed(Rs_)
    Fmax = max(Fmax, Ft)
    dF = Rs_ * co['P_RR'] - co['P_R']          # F_f'(R) = R P'' - P'  (equals R K_f only at a stationary point)
    Kmin_scan = min(Kmin_scan, dF)
    scan.append({'R': str(Rs_), 'levels': L, 'tachyonic': bool(_tachyonic(Rs_, D(0))), 'F_f': str(co['F'].quantize(D('1e-8'))),
                 'dF_f_dR': str(dF.quantize(D('1e-8'))),
                 'Gtilde': str(Gtilde_closed(Rs_).quantize(D('1e-8'))), 'F_tot': str(Ft.quantize(D('1e-8')))})
getcontext().prec = 95
F_inf = 56 * m2 / 3                      # large-R limit of F_f (Euler-Maclaurin constant -1/6 per sector: H = 56/u - 28/3 + O(u))
Gt_inf = -(10 * PI ** 2 / 3) * GAMMA * (2 * m2 / m1)
vac['untuned_scan'] = {'points': scan, 'max_F_tot_on_scan': str(Fmax), 'F_f_large_R_limit_(56/3)m2': str(F_inf), 'Gtilde_large_R_limit': str(Gt_inf), 'F_tot_large_R_limit': str(F_inf + Gt_inf)}
vac['untuned_scan']['tachyon_threshold_radius_R_c'] = str(R_c_untuned)
vac['untuned_scan']['min_dF_f_dR_on_scan'] = str(Kmin_scan)
record('untuned_no_flat_stationary_radius_on_scan', Fmax < 0)
record('F_f_increasing_on_scan', Kmin_scan > 0)
record('scan_includes_non_tachyonic_points_below_R_c', any(not p['tachyonic'] for p in scan) and any(p['tachyonic'] for p in scan))
record('untuned_no_flat_stationary_radius_asymptotically', F_inf + Gt_inf < 0)
record('scan_F_f_approaches_asymptote_from_below', D(scan[-1]['F_f']) < F_inf and D(scan[-1]['F_f']) > F_inf - D('0.05'))
vac['untuned_conclusion'] = ('With the untuned a_4-truncated scalar sector, F_f(R) + Gtilde(R) < 0 at every scanned radius 0.1 <= R <= 30 '
                             '(Gtilde = 0 below the tachyon threshold R_c, where there is no vev) and in the R -> infinity limit: the flat-vacuum '
                             'prescription has no solution on the scan. Scan-based, not interval-certified. The inherited common stationary radius is not '
                             'preserved. This is a statement about the declared truncated action evaluated outside its validity domain (A3, A4).')

# Validity of the truncated minimum: largest eigenvalue of M^2 (= of Y^dag Y) over the sphere at the actual vacuum.
# With aligned vevs, Phi_d = H_d Y_{1/2,1}/r peaks at the south pole and Phi_u^* = (i s2 H_u^*) Y_{1/2,0}/r at the north
# pole, each with max |Y|^2 = 1/(2 pi).  Sector eigenvalues (hatted, dimensionless Yukawas; N_hat = N without 1/Lambda^2):
#   d, e:  4 pi^2 yhat^2 sigma_d Lambda^2/(m1 R^2 N_hat_d),   u: 4 pi^2 yu^2 sigma_u Lambda^2/(m1 R^2 N_hat_u);
# the quark (u,d) block is rank one with eigenvalue y_u^2|Phi_u|^2 + y_d^2|Phi_d|^2, whose maximum over the sphere is the
# larger of the two pole values because the two profiles are sin^2(theta/2) and cos^2(theta/2).
def M2_sector_max(sigma, yhat2, Nhat):
    return 4 * PI ** 2 * yhat2 * sigma / (m1 * R_star ** 2 * Nhat)


M2_d = M2_sector_max(sd0, yd ** 2, Nd)
M2_e = M2_sector_max(sd0, ye ** 2, Nd)
M2_u = M2_sector_max(su0, yu ** 2, Nu)
M2_max = max(M2_d, M2_e, M2_u)
vac['validity'] = {
    'M2_max_over_Lambda2_d_sector': str(M2_d), 'M2_max_over_Lambda2_e_sector': str(M2_e), 'M2_max_over_Lambda2_u_sector': str(M2_u),
    'M2_max_over_Lambda2': str(M2_max),
    'a_j_times_M2max_over_Lambda2_range': [str((nodes[0] * M2_max).quantize(D('1e-10'))), str((nodes[-1] * M2_max).quantize(D('1e-10')))],
    'special_case_ye_0_M2max_over_Lambda2 = mu2/2': str(mu2_star / 2),
    'statement': ('The truncated local minimum sits at a Yukawa-weighted vev of order Lambda (largest M^2 eigenvalue 0.86 Lambda^2 for the fixture); '
                  'the a_4 truncation is not controlled there. Untuned numbers are fixtures of the declared truncated action, not controlled predictions.'),
}
record('truncated_minimum_outside_local_validity', nodes[-1] * M2_max > 1)
# special case y_e = 0: all quartics equal, gamma_d = gamma_u = 3 m1 Nb/(8 pi^2), M2_max = mu2/2 exactly
_gd0 = 3 * m1 * N_B / (8 * PI ** 2)
record('ye0_special_case_M2max_is_mu2_over_2', abs(4 * PI ** 2 * _gd0 * mu2_star * R_star ** 2 / (m1 * R_star ** 2 * 3 * N_B) - mu2_star / 2) < D('1e-85'))

# gamma as a function of the Yukawas: depends only on t = y_e^2/y_d^2 (and on m1, Nb):
#   gamma = (3 m1 Nb/(16 pi^2)) g(t),  g = (16 s^2 - 84 s + 144)/(4 s^2 - 24 s + 45),  s = 3 + t,
#   g(0) = g(inf) = 4, g(1) = 64/13 (fixture), max g = 5 at t = 3/2.
def g_exact(t):
    s_ = 3 + t
    return (16 * s_ * s_ - 84 * s_ + 144) / (4 * s_ * s_ - 24 * s_ + 45)


def dg_num(s_):   # numerator of dg/ds
    return (32 * s_ - 84) * (4 * s_ * s_ - 24 * s_ + 45) - (16 * s_ * s_ - 84 * s_ + 144) * (8 * s_ - 24)


gamma_pref = 3 * m1 * N_B / (16 * PI ** 2)
record('gamma_fixture_equals_prefactor_times_g1_64_13', abs(GAMMA - gamma_pref * D(64) / 13) < D('1e-85'))
record('g_exact_values_0_1_three_halves', g_exact(Fr(0)) == 4 and g_exact(Fr(1)) == Fr(64, 13) and g_exact(Fr(3, 2)) == 5)
record('g_stationary_at_t_three_halves', dg_num(Fr(9, 2)) == 0)
_grid = [Fr(k, 100) for k in range(0, 5001)]
record('g_max_on_grid_0_to_50_is_5', max(g_exact(t) for t in _grid) == 5 and g_exact(Fr(50)) > 4)
gamma_min, gamma_max = 4 * gamma_pref, 5 * gamma_pref
# Both gamma and K_f scale with Nb (every D_n counts copies), so the stability condition is Nb independent:
#   K_tilde > 0  <=>  gamma/K_f < R^4/(8 pi^2 B^2)   (eps -> 0 limit)
ratio_bound = R_star ** 4 / (8 * PI ** 2 * (D(5) / 6) ** 2)
vac['gamma_range_over_yukawas'] = {
    'gamma_prefactor_3m1Nb_over_16pi2': str(gamma_pref), 'gamma_min (t=0 or inf)': str(gamma_min),
    'gamma_fixture (t=1)': str(GAMMA), 'gamma_max (t=3/2)': str(gamma_max),
    'stability_ratio_bound R^4/(8 pi^2 B^2)': str(ratio_bound),
    'gamma_max_over_K_f_minus': str(gamma_max / Km), 'gamma_max_over_K_f_plus': str(gamma_max / Kp),
    'statement': 'gamma/K_f is independent of Nb; for the published profiles even the maximum over Yukawa ratios stays below the bound.',
}
record('restricted_stability_survives_all_yukawa_ratios', gamma_max / Km < ratio_bound and gamma_max / Kp < ratio_bound)

# Hierarchical regime (A5): delta2 chosen so that mu2(R_*) = eps; full Newton solve and first-order formula.
# Linearisation of F_tot = F_f + Gtilde about R_*:  delta R = -Gtilde(R_*)/(R_* K_f + Gtilde'(R_*)),
# Gtilde'(R_*) = -(50 pi^2/9) gamma / R_*^3 is O(1) even for eps -> 0 (slope of the KK-type mass term).
# Induced curvature shift of the restricted radius potential (same R):
#   K_tilde - K_f = G_H'' - 2 G_H/R^2 = -(4 pi^2 gamma B / R^2)(mu2 + 2B/R^2),  B = 5/6.
B_KK = D(5) / 6
vac['hierarchical_regime'] = {}
induced = -(4 * PI ** 2 * GAMMA * B_KK / R_star ** 2) * (2 * B_KK / R_star ** 2)
vac['induced_curvature_shift_hierarchical_limit'] = {'Delta_K': str(induced), 'K_f_minus': str(Km), 'K_f_plus': str(Kp),
                                                     'K_tilde_minus_approx': str(Km + induced), 'K_tilde_plus_approx': str(Kp + induced),
                                                     'stability_condition': 'gamma/K_f < R^4/(8 pi^2 B^2) (Nb independent)',
                                                     'gamma_fixture_over_K_f_minus': str(GAMMA / Km),
                                                     'gamma_fixture': str(GAMMA)}
record('induced_curvature_shift_negative', induced < 0)
record('restricted_stability_survives_fixture', Km + induced > 0 and Kp + induced > 0)
for eps_str in ('1e-2', '1e-4', '1e-8'):
    eps = D(eps_str)
    delta2 = 2 * m2 / m1 - D(5) / (6 * R_star * R_star) - eps
    sd_e, su_e = vev_solution(R_star, eps)
    Gt0 = Gtilde_closed(R_star, delta2)
    Gtp = dGtilde_closed(R_star, delta2)
    entry = {'mu2_over_Lambda2_at_R_star': eps_str, 'delta2': str(delta2), 'sigma_d': str(sd_e), 'sigma_u': str(su_e),
             's/(kappa Lambda^2)': str(sd_e + su_e), 'G_H(R_star)': str(G_H_closed(R_star, delta2)), 'Gtilde(R_star)': str(Gt0), "Gtilde'(R_star)": str(Gtp)}
    sols = {}
    dR1s = {}
    for name in ('minus', 'plus'):
        K = D(inh['profiles'][name]['coefficients_60_levels']['K'])
        dR1 = -Gt0 / (R_star * K + Gtp)
        dR1s[name] = dR1
        sol = coupled_stationary_radius(name, delta2, R_star + dR1)
        sols[name] = sol
        entry[name] = {'delta_R_first_order': str(dR1), 'R_tilde': str(sol['R']), 'delta_R_exact': str(sol['R'] - R_star),
                       'c_tilde': str(sol['c_tilde']), 'K_tilde': str(sol['K_tilde']), 'K_tilde_minus_K_f': str(sol['K_tilde'] - K),
                       'F_tot_residual': str(sol['F_residual']),
                       'newton_iterations': sol['iterations'], 'mu2_at_R_tilde': str(mu2hat(sol['R'], delta2))}
        record('hier_%s_converged_%s' % (eps_str, name), abs(sol['F_residual']) < D('1e-50'))
        record('hier_%s_curvature_positive_%s' % (eps_str, name), sol['K_tilde'] > 0)
        record('hier_%s_first_order_accurate_1pct_%s' % (eps_str, name), abs((sol['R'] - R_star) - dR1) < D('0.01') * abs(dR1))
        induced_full = -(4 * PI ** 2 * GAMMA * B_KK / sol['R'] ** 2) * (mu2hat(sol['R'], delta2) + 2 * B_KK / sol['R'] ** 2)
        entry[name]['induced_curvature_formula_at_R_tilde'] = str(induced_full)
        entry[name]['K_f_at_R_tilde'] = str(sol['K_f_at_R'])
        entry[name]['K_tilde_minus_K_f_at_R_tilde'] = str(sol['K_tilde'] - sol['K_f_at_R'])
        record('hier_%s_induced_curvature_formula_1pct_%s' % (eps_str, name), abs((sol['K_tilde'] - sol['K_f_at_R']) - induced_full) < D('0.01') * abs(induced_full))
    split = sols['plus']['R'] - sols['minus']['R']
    pred = dR1s['plus'] - dR1s['minus']
    entry['pair_radius_splitting'] = str(split)
    entry['pair_radius_splitting_first_order'] = str(pred)
    entry['pair_c_tilde_splitting'] = str(sols['plus']['c_tilde'] - sols['minus']['c_tilde'])
    record('hier_%s_splitting_matches_first_order' % eps_str, abs(split - pred) < (5 * eps + D('1e-3')) * abs(pred))
    vac['hierarchical_regime'][eps_str] = entry
co_m = hs.profile_coefficients(nodes, W['minus'], R_star, levels=60)
co_p = hs.profile_coefficients(nodes, W['plus'], R_star, levels=60)
_h = D('1e-30')
_num = (hs.profile_coefficients(nodes, W['minus'], R_star + _h, levels=60)['zY'] - hs.profile_coefficients(nodes, W['minus'], R_star - _h, levels=60)['zY']) / (2 * _h)
record('zY_R_derivative_matches_numerical', abs(_num - co_m['zY_R']) < D('1e-25'))
vac['coupling_radius_derivatives_at_R_star'] = {'dzY_dR_minus': str(co_m['zY_R']), 'dzY_dR_plus': str(co_p['zY_R']),
                                                'dzX_dR_minus': str(co_m['zX_R']), 'dzX_dR_plus': str(co_p['zX_R']),
                                                'dzW_dR': 'not available: requires the predecessor weak kernel away from R_*'}
for eps_str, entry in vac['hierarchical_regime'].items():
    split = D(entry['pair_radius_splitting'])
    dR_common = D(entry['minus']['delta_R_exact'])
    corr_Y = co_m['zY_R'] * split + (co_p['zY_R'] - co_m['zY_R']) * dR_common
    dzY_star = co_p['zY'] - co_m['zY']
    entry['pair_delta_zY_at_coupled_vacua_minus_at_R_star'] = str(corr_Y)
    entry['relative_to_delta_zgamma_at_R_star'] = str(corr_Y / (D(inh['delta_zgamma_tree'])))
    # direct evaluation at the two coupled radii (Y part only)
    zYm = hs.profile_coefficients(nodes, W['minus'], D(entry['minus']['R_tilde']), levels=60)['zY']
    zYp = hs.profile_coefficients(nodes, W['plus'], D(entry['plus']['R_tilde']), levels=60)['zY']
    entry['pair_delta_zY_at_coupled_vacua_direct'] = str(zYp - zYm)
    record('hier_%s_zY_correction_first_order_matches_direct' % eps_str, abs((zYp - zYm) - (dzY_star + corr_Y)) < (5 * D(eps_str) + D('1e-3')) * abs(corr_Y))
record('hierarchical_shift_linear_in_eps',
       abs(D(vac['hierarchical_regime']['1e-4']['minus']['delta_R_exact']) / D(vac['hierarchical_regime']['1e-2']['minus']['delta_R_exact']) - D('1e-2')) < D('1e-3'))
results['vacuum'] = vac

# ---------------------------------------------------------------------------
# B. Broken-background neutral matrices, null space, residue, spectrum
# ---------------------------------------------------------------------------
HD = [D(-1) / 2, D(1) / 2, D(1)]
HU = [D(-1) / 2, D(1) / 2, D(-1)]


def mass_matrix(vd2, vu2, mst2):
    sig = [D(0), D(0), mst2.sqrt() if mst2 > 0 else D(0)]
    return [[vd2 * HD[i] * HD[j] + vu2 * HU[i] * HU[j] + sig[i] * sig[j] for j in range(3)] for i in range(3)]


def matvec(M, v):
    return [sum(M[i][j] * v[j] for j in range(3)) for i in range(3)]


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def neutral_sector(name, vd2, vu2, mst2, chi=D(0), dK=None):
    """Kinetic K = diag(zW, zY, zX) + chi(Y-X) + dK (all in units of kappa); M^2 in units of kappa Lambda^2 (vevs canonical)."""
    K = [[zW[name], D(0), D(0)], [D(0), zY[name], chi], [D(0), chi, zX[name]]]
    if dK is not None:
        K = [[K[i][j] + dK[i][j] for j in range(3)] for i in range(3)]
    M2 = mass_matrix(vd2, vu2, mst2)
    N = [D(1), D(1), D(0)]
    MN = matvec(M2, N)
    NKN = sum(N[i] * sum(K[i][j] * N[j] for j in range(3)) for i in range(3))
    e_inv2 = NKN
    residue = [[N[i] * N[j] / NKN for j in range(3)] for i in range(3)]
    # characteristic polynomial det(M^2 - x K) = -x (x^2 - T x + P) * det K  (one zero root); extract T, P numerically
    # det(M^2 - xK) is cubic in x: c3 x^3 + c2 x^2 + c1 x + c0 with c0 = det M^2 = 0 (kernel).  Evaluate at 3 points and solve.
    xs = [D(1), D(2), D(3)]
    vals = [det3([[M2[i][j] - x * K[i][j] for j in range(3)] for i in range(3)]) for x in xs]
    # c3 x^3 + c2 x^2 + c1 x = val  => solve 3x3 linear system in (c3, c2, c1)
    A = [[x ** 3, x ** 2, x] for x in xs]
    dA = det3(A)
    c3 = det3([[vals[i], A[i][1], A[i][2]] for i in range(3)]) / dA
    c2 = det3([[A[i][0], vals[i], A[i][2]] for i in range(3)]) / dA
    c1 = det3([[A[i][0], A[i][1], vals[i]] for i in range(3)]) / dA
    T = -c2 / c3
    Pc = c1 / c3
    disc = T * T - 4 * Pc
    m_plus = (T + disc.sqrt()) / 2
    m_minus = (T - disc.sqrt()) / 2
    detM2 = det3(M2)
    return {'K': K, 'M2': M2, 'M2_N': MN, 'e_inv2_over_kappa': e_inv2, 'residue': residue, 'T': T, 'P': Pc,
            'm2_heavy': m_plus, 'm2_light': m_minus, 'detM2': detM2,
            'mW2': (vd2 + vu2) / (4 * zW[name]),
            'sin2_thetaW_tree': zW[name] / (zW[name] + zY[name])}


ns = {}
fixtures = {
    'A_predecessor_s1_equal_vevs_noSt': (D('0.5'), D('0.5'), D(0)),
    'B_model_untuned_vevs_noSt': (sd0, su0, D(0)),
    'C_model_untuned_vevs_St_equal_s': (sd0, su0, sd0 + su0),
    'D_model_untuned_vevs_St_100s': (sd0, su0, 100 * (sd0 + su0)),
    'E_equal_vevs_s1_St_1': (D('0.5'), D('0.5'), D(1)),
}
for fx, (vd2, vu2, mst2) in fixtures.items():
    ns[fx] = {}
    for name in ('minus', 'plus'):
        out = neutral_sector(name, vd2, vu2, mst2)
        # closed forms for T and P (derived in the note), chi = 0
        s = vd2 + vu2
        T_closed = (s / 4) * (1 / zW[name] + 1 / zY[name]) + (s + mst2) / zX[name]
        P_closed = (4 * vd2 * vu2 + s * mst2) * (zW[name] + zY[name]) / (4 * zW[name] * zY[name] * zX[name])
        record('kernel_vector_annihilated_%s_%s' % (fx, name), max(abs(x) for x in out['M2_N']) == 0)
        record('e_inv2_equals_zW_plus_zY_%s_%s' % (fx, name), abs(out['e_inv2_over_kappa'] - (zW[name] + zY[name])) < D('1e-80'))
        record('detM2_zero_%s_%s' % (fx, name), abs(out['detM2']) < D('1e-85'))
        record('trace_closed_form_%s_%s' % (fx, name), abs(out['T'] - T_closed) < D('1e-70'))
        record('product_closed_form_%s_%s' % (fx, name), abs(out['P'] - P_closed) < D('1e-70'))
        record('massive_eigenvalues_positive_%s_%s' % (fx, name), out['m2_light'] > 0 and out['m2_heavy'] > 0)
        # rho-like ratio for the state continuously connected to Z: use the eigenvalue closest to (s/4)(1/zW+1/zY)
        mZ_naive = (s / 4) * (1 / zW[name] + 1 / zY[name])
        mZ2 = out['m2_light'] if abs(out['m2_light'] - mZ_naive) < abs(out['m2_heavy'] - mZ_naive) else out['m2_heavy']
        cos2 = zY[name] / (zW[name] + zY[name])
        rho = out['mW2'] / (mZ2 * cos2)
        ns[fx][name] = {
            'vd2': str(vd2), 'vu2': str(vu2), 'M_St2': str(mst2),
            'e_inv2_over_kappa': str(out['e_inv2_over_kappa']),
            'residue_matrix_times_e_inv2': [[str((out['residue'][i][j] * out['e_inv2_over_kappa']).quantize(D('1e-30'))) for j in range(3)] for i in range(3)],
            'm2_massive_light': str(out['m2_light']), 'm2_massive_heavy': str(out['m2_heavy']),
            'mZ2_naive': str(mZ_naive), 'mX2_naive_s_plus_MSt2_over_zX': str((s + mst2) / zX[name]),
            'mW2': str(out['mW2']), 'sin2_thetaW_tree': str(out['sin2_thetaW_tree']), 'rho_tree_for_Z_like_state': str(rho),
            'T': str(out['T']), 'P': str(out['P']),
        }
    ns[fx]['delta_e_inv2_over_kappa'] = str(D(ns[fx]['plus']['e_inv2_over_kappa']) - D(ns[fx]['minus']['e_inv2_over_kappa']))
# predecessor fixture reproduction (A, minus): mZ2 = 2.500072505697618, mX2 = 0.542537313842138
record('predecessor_fixture_A_mZ2', abs(D(ns['A_predecessor_s1_equal_vevs_noSt']['minus']['m2_massive_heavy']) - D('2.500072505697618')) < D('1e-14'))
record('predecessor_fixture_A_mX2', abs(D(ns['A_predecessor_s1_equal_vevs_noSt']['minus']['m2_massive_light']) - D('0.542537313842138')) < D('1e-14'))
record('rho_equals_one_at_equal_vevs_noSt', abs(D(ns['A_predecessor_s1_equal_vevs_noSt']['minus']['rho_tree_for_Z_like_state']) - 1) < D('1e-80'))
record('rho_deviates_from_one_with_unequal_vevs_noSt', abs(D(ns['B_model_untuned_vevs_noSt']['minus']['rho_tree_for_Z_like_state']) - 1) > D('1e-6'))
record('stueckelberg_mass_drives_rho_towards_one', abs(D(ns['D_model_untuned_vevs_St_100s']['minus']['rho_tree_for_Z_like_state']) - 1) < abs(D(ns['C_model_untuned_vevs_St_equal_s']['minus']['rho_tree_for_Z_like_state']) - 1))
results['neutral_sector'] = ns

# kinetic-mixing control chi != 0 (positivity preserved): photon normalisation unchanged
out_chi = neutral_sector('minus', sd0, su0, sd0 + su0, chi=D('0.1'))
record('chi_control_e_inv2_unchanged', abs(out_chi['e_inv2_over_kappa'] - (zW['minus'] + zY['minus'])) < D('1e-80'))
record('chi_control_massive_positive', out_chi['m2_light'] > 0 and out_chi['m2_heavy'] > 0)
# one-vev boundary: rank drops to one (two massless neutral fields): det of the 2x2 (W3,B) block and nullity
M2_one = mass_matrix(sd0, D(0), D(0))
record('one_vev_boundary_rank_one_without_stueckelberg', det3(M2_one) == 0 and (M2_one[0][0] * M2_one[2][2] - M2_one[0][2] ** 2) == 0)
M2_one_St = mass_matrix(sd0, D(0), sd0)
_minor = M2_one_St[0][0] * M2_one_St[2][2] - M2_one_St[0][2] ** 2
record('one_vev_boundary_with_stueckelberg_rank_two_photon_only',
       abs(det3(M2_one_St)) < D('1e-85') and _minor > 0 and max(abs(x) for x in matvec(M2_one_St, [D(1), D(1), D(0)])) == 0)
# Higgs-induced kinetic shifts: projection drops X mixing entries (structural check with symbolic placeholders)
dK = [[D('0.01'), D('0.002'), D('0.5')], [D('0.002'), D('-0.003'), D('0.7')], [D('0.5'), D('0.7'), D('0.1')]]
out_dK = neutral_sector('minus', sd0, su0, D(0), dK=dK)
record('photon_projection_independent_of_X_column_shifts', abs(out_dK['e_inv2_over_kappa'] - (zW['minus'] + zY['minus'] + dK[0][0] + dK[1][1] + 2 * dK[0][1])) < D('1e-80'))

# Scalar spectrum at the untuned fixture (canonical, units kappa Lambda^2 for masses^2 ... note lambda_i = ell_i/(kappa R^2))
def scalar_spectrum(R, mu2):
    sd, su = vev_solution(R, mu2)
    lam_d, lam_u, lam_3 = ell_d / (R * R), ell_u / (R * R), ell_3 / (R * R)   # times 1/kappa
    # masses^2 in units Lambda^2: lambda * vhat^2 = (ell/(kappa R^2)) * kappa Lambda^2 sigma = ell sigma Lambda^2 / R^2
    H = [[2 * lam_d * sd, lam_3 * dsqrt(sd * su)], [lam_3 * dsqrt(sd * su), 2 * lam_u * su]]
    tr = H[0][0] + H[1][1]
    det = H[0][0] * H[1][1] - H[0][1] ** 2
    disc = (tr * tr - 4 * det).sqrt()
    return {'m2_h_light_over_Lambda2': str((tr - disc) / 2), 'm2_h_heavy_over_Lambda2': str((tr + disc) / 2),
            'm2_Hpm_over_Lambda2': str(lam_3 * (sd + su) / 2), 'm2_axion_tree': '0',
            'goldstones_eaten': 4}


results['scalar_spectrum_untuned_fixture'] = scalar_spectrum(R_star, mu2_star)
record('cp_even_masses_positive', D(results['scalar_spectrum_untuned_fixture']['m2_h_light_over_Lambda2']) > 0)

# ---------------------------------------------------------------------------
# C. Tree-level matching data (no measured alpha used)
# ---------------------------------------------------------------------------
match = {}
for name in ('minus', 'plus'):
    zg = zW[name] + zY[name]
    J = D(inh['profiles'][name]['coefficients_60_levels']['J'])
    match[name] = {
        'zgamma = e^-2/kappa': str(zg),
        'alpha_inverse_tree_over_kappa = 4 pi zgamma': str(4 * PI * zg),
        'kappa_required_per_unit_alpha_inverse = 1/(4 pi zgamma)': str(1 / (4 * PI * zg)),
        'alpha_inverse_tree_per_(M4/Lambda)^2 = 96 pi^3 zgamma / J': str(96 * PI ** 3 * zg / J),
        'sin2_thetaW_tree = zW/(zW+zY)': str(zW[name] / zg),
        'J_f(R_star)': str(J),
    }
match['delta_alpha_inverse_tree_over_kappa'] = str(4 * PI * ((zW['plus'] + zY['plus']) - (zW['minus'] + zY['minus'])))
match['delta_sin2_thetaW_tree'] = str(zW['plus'] / (zW['plus'] + zY['plus']) - zW['minus'] / (zW['minus'] + zY['minus']))
anom = json.loads((HERE / 'anomaly_sector_results.json').read_text())
match['one_loop_coefficients'] = anom['one_loop_coefficients_model']
match['running_formula'] = 'Z_i(mu) = Z_i(mu_0) - (b_i/(8 pi^2)) ln(mu/mu_0) for each unbroken factor above the weak scale; e^-2 = Z_W + Z_Y projects with (1,1,0) only in the broken phase at the pole.'
# thresholds in units of Lambda (fixture; no measured input)
thr = {'KK_fermion_n_sector_sqrt(l(l+n))/R_star': {str(n): [str((D(l * (l + n)).sqrt() / R_star).quantize(D('1e-12'))) for l in (1, 2, 3)] for n in (0, 1, 2)},
       'scalar_KK_j=3/2_mass_over_Lambda': str((D(inh['profiles']['minus']['coefficients_60_levels']['P']) * 0 + (-2 * m2 / m1 + 1 / (3 * R_star ** 2) + D(7) / (2 * R_star ** 2))).sqrt()),
       'untuned_fixture_mW_over_Lambda_kappa_free': str((D(ns['B_model_untuned_vevs_noSt']['minus']['mW2'])).sqrt()),
       'note': 'In the untuned truncated action all electroweak-scale states sit at O(Lambda): no hierarchy is generated at tree level.'}
match['thresholds_units_Lambda'] = thr
results['matching'] = match
record('sin2_thetaW_tree_near_one_half', abs(zW['minus'] / (zW['minus'] + zY['minus']) - D('0.5')) < D('0.01'))

results['checks'] = checks
failed = [k for k, ok in checks.items() if not ok]
(HERE / 'vacuum_matching_results.json').write_text(json.dumps(results, indent=2))
print('vacuum_matching: %d checks, %d failed' % (len(checks), len(failed)))
for k in failed:
    print('  FAILED', k)
print(' mu2/L2 =', str(mu2_star)[:18], ' sigma_d,u =', str(sd0)[:12], str(su0)[:12], ' G_H =', str(G_H_closed(R_star))[:14], ' Gtilde =', str(Gtilde_closed(R_star))[:12])
print(' untuned: max F_tot on scan =', vac['untuned_scan']['max_F_tot_on_scan'][:10], ' asymptote =', vac['untuned_scan']['F_tot_large_R_limit'][:10])
for eps_str, e in vac['hierarchical_regime'].items():
    print(' eps=%s: dR_minus=%.6e dR_plus=%.6e split=%.6e (pred %.6e) K~=%.6f' % (eps_str, D(e['minus']['delta_R_exact']), D(e['plus']['delta_R_exact']), D(e['pair_radius_splitting']), D(e['pair_radius_splitting_first_order']), D(e['minus']['K_tilde'])))
print(' fixture A minus: mZ2=%s mX2=%s' % (ns['A_predecessor_s1_equal_vevs_noSt']['minus']['m2_massive_heavy'][:20], ns['A_predecessor_s1_equal_vevs_noSt']['minus']['m2_massive_light'][:20]))
print(' sin2thetaW tree:', match['minus']['sin2_thetaW_tree = zW/(zW+zY)'][:14], ' 4pi zgamma:', match['minus']['alpha_inverse_tree_over_kappa = 4 pi zgamma'][:14])
if failed:
    raise SystemExit(1)
