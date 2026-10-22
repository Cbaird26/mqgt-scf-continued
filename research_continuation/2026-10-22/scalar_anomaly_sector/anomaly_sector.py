"""Anomaly bookkeeping of the retained zero-mode content and the specified
Stueckelberg / Green-Schwarz axion sector.  Exact rational arithmetic only.

Writes anomaly_sector_results.json.
"""
from fractions import Fraction as Fr
from pathlib import Path
from random import Random
import json

HERE = Path(__file__).resolve().parent
checks = {}
results = {}


def record(name, ok):
    checks[name] = bool(ok)


# Left-handed Weyl zero modes of one copied block (n = x; physical right-handed
# singlets with x = +1 appear as left-handed conjugates with x = -1).
# (label, SU(3) rep dim with sign for antitriplet, SU(2) dim, qY, x)
LH_WEYL = [
    ('Q',   3, 2, Fr(1, 6),  Fr(2)),
    ('L',   1, 2, Fr(-1, 2), Fr(2)),
    ('u^c', -3, 1, Fr(-2, 3), Fr(-1)),
    ('d^c', -3, 1, Fr(1, 3),  Fr(-1)),
    ('e^c', 1, 1, Fr(1),     Fr(-1)),
]
N_BLOCKS = 4
T_FUND = Fr(1, 2)   # Dynkin index of the fundamental of SU(N), tr(T^a T^b) = (1/2) delta^{ab}
C_A = {2: Fr(2), 3: Fr(3)}


def anomaly_coefficients(fields):
    A = {k: Fr(0) for k in ('SU3^2 Y', 'SU3^2 X', 'SU2^2 Y', 'SU2^2 X', 'Y^3', 'Y^2 X', 'Y X^2', 'X^3', 'grav^2 Y', 'grav^2 X', 'SU3^3')}
    for _, c3, d2, qY, x in fields:
        dim_c = abs(c3)
        if dim_c == 3:
            A['SU3^2 Y'] += T_FUND * d2 * qY
            A['SU3^2 X'] += T_FUND * d2 * x
            A['SU3^3'] += (1 if c3 > 0 else -1) * d2      # cubic index of 3 is +1, of 3bar is -1
        if d2 == 2:
            A['SU2^2 Y'] += T_FUND * dim_c * qY
            A['SU2^2 X'] += T_FUND * dim_c * x
        mult = dim_c * d2
        A['Y^3'] += mult * qY ** 3
        A['Y^2 X'] += mult * qY ** 2 * x
        A['Y X^2'] += mult * qY * x ** 2
        A['X^3'] += mult * x ** 3
        A['grav^2 Y'] += mult * qY
        A['grav^2 X'] += mult * x
    return A


A1 = anomaly_coefficients(LH_WEYL)
A4 = {k: N_BLOCKS * v for k, v in A1.items()}
results['anomaly_coefficients_one_block'] = {k: str(v) for k, v in A1.items()}
results['anomaly_coefficients_four_blocks'] = {k: str(v) for k, v in A4.items()}

sm_like = ['SU3^2 Y', 'SU2^2 Y', 'Y^3', 'grav^2 Y', 'SU3^3']
x_like = ['SU3^2 X', 'SU2^2 X', 'Y^2 X', 'Y X^2', 'X^3', 'grav^2 X']
record('all_Y_and_nonabelian_anomalies_vanish', all(A1[k] == 0 for k in sm_like))
record('X_anomalies_match_predecessor_1_4_m4_3_0_57_9', [A1[k] for k in x_like] == [Fr(1), Fr(4), Fr(-4, 3), Fr(0), Fr(57), Fr(9)])
record('YX2_anomaly_vanishes_so_Y_leg_needs_no_axion_shift_from_it', A1['Y X^2'] == 0)
record('Y2X_anomaly_nonzero_requires_Bardeen_counterterm_to_protect_Y', A1['Y^2 X'] != 0)
n_doublets = N_BLOCKS * sum(abs(c3) for _, c3, d2, _, _ in LH_WEYL if d2 == 2)
record('witten_su2_anomaly_free_even_doublets', n_doublets % 2 == 0)
results['su2_doublet_count'] = n_doublets

# Scalars do not contribute to chiral anomalies; the n=0 spectator has no zero modes.
results['non_contributors'] = ['Phi_d, Phi_u (scalars): no chiral anomaly', 'n=0 spectator block: no chiral zero modes']

# ---------------------------------------------------------------------------
# Green-Schwarz / Stueckelberg axion sector (specified mechanism)
# ---------------------------------------------------------------------------
# L_anom = (M_St^2/2)(d theta - X)^2 + theta * sum_i (c_i / normalisation_i) O_i + Bardeen counterterm E_{YYX},
#   O_i in { tr G Gdual, tr W Wdual, B Bdual, X Xdual, R Rdual },  theta -> theta + lambda_X.
# With every mixed anomaly moved onto the X leg by the Bardeen (generalized Chern-Simons) counterterm,
# cancellation requires c_i = - k_i A_i where k_i is the standard consistent-anomaly normalisation of
# the i-th structure (k_X = 1/3 relative to the mixed ones for the cubic X^3 term in the symmetric scheme).
# The rational content is the vector A_i; we record the required couplings.  Solvability with one axion
# is a property of the mechanism (every remaining anomaly sits on an X leg), not a computed check.
# The computed condition is that U(1)_Y is non-anomalous once the Bardeen term moves Y^2 X onto X:
GS = {
    'c_3  (theta tr G Gdual)': -A4['SU3^2 X'],
    'c_2  (theta tr W Wdual)': -A4['SU2^2 X'],
    'c_Y  (theta B Bdual)   ': -A4['Y^2 X'],
    'c_X  (theta X Xdual)   ': -A4['X^3'] / 3,
    'c_g  (theta R Rdual)   ': -A4['grav^2 X'],
    'E_YYX (Bardeen term)   ': 'fixed by moving the Y^2 X consistent anomaly from the B legs to the X leg; required because the photon contains B',
    'no theta shift under Y ': 'A_{Y X^2} = 0 and the Bardeen choice leave U(1)_Y exactly non-anomalous',
}
results['green_schwarz_couplings_in_anomaly_units'] = {k: (str(v) if isinstance(v, Fr) else v) for k, v in GS.items()}
y_variations = {k: A4[k] for k in ('Y^3', 'grav^2 Y', 'SU3^2 Y', 'SU2^2 Y', 'Y X^2')}
record('Y_non_anomalous_after_bardeen_term', all(v == 0 for v in y_variations.values()))
results['Y_variation_coefficients_after_bardeen'] = {k: str(v) for k, v in y_variations.items()}

# Stueckelberg charge vector in the (W3, B, X) basis: sigma = (0, 0, M_St).  Predecessor identity:
# det(M^2 + sigma sigma^T) = v_d^2 v_u^2 mu_Y^2 for sigma = (0, mu_Y, mu_X)  => pure-X mass keeps the photon.
rng = Random(20261022)


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def mass_matrix(vd2, vu2, muY, muX):
    hd = [Fr(-1, 2), Fr(1, 2), Fr(1)]
    hu = [Fr(-1, 2), Fr(1, 2), Fr(-1)]
    sig = [Fr(0), muY, muX]
    return [[vd2 * hd[i] * hd[j] + vu2 * hu[i] * hu[j] + sig[i] * sig[j] for j in range(3)] for i in range(3)]


ok_det = True
ok_kernel = True
for _ in range(200):
    vd2, vu2, muY, muX = (Fr(rng.randint(1, 50), rng.randint(1, 50)) for _ in range(4))
    M = mass_matrix(vd2, vu2, muY, muX)
    ok_det &= det3(M) == vd2 * vu2 * muY ** 2
    M0 = mass_matrix(vd2, vu2, Fr(0), muX)
    q = [Fr(1), Fr(1), Fr(0)]
    ok_kernel &= all(sum(M0[i][j] * q[j] for j in range(3)) == 0 for i in range(3))
record('stueckelberg_determinant_identity_random_rationals', ok_det)
record('pure_X_stueckelberg_mass_keeps_photon_direction_1_1_0', ok_kernel)

# ---------------------------------------------------------------------------
# One-loop running coefficients of the light (zero-mode) sector, exact
#   d(1/g^2)/d ln mu = - b/(8 pi^2),  b = -(11/3) C_A + (2/3) sum_Weyl T(R) + (1/3) sum_complex_scalars T(R)
#   abelian: T -> charge^2 (q_Y = y/2 normalisation, x as printed)
# ---------------------------------------------------------------------------
SCALARS = [('H_d', 1, 2, Fr(1, 2), Fr(1)), ('H_u', 1, 2, Fr(1, 2), Fr(-1))]


def beta_coefficients(fermions, scalars, nb):
    b = {}
    # SU(3)
    fT = sum(T_FUND * d2 for _, c3, d2, _, _ in fermions if abs(c3) == 3) * nb
    b['SU3'] = -Fr(11, 3) * C_A[3] + Fr(2, 3) * fT
    # SU(2)
    fT2 = sum(T_FUND * abs(c3) for _, c3, d2, _, _ in fermions if d2 == 2) * nb
    sT2 = sum(T_FUND * abs(c3) for _, c3, d2, _, _ in scalars if d2 == 2)
    b['SU2'] = -Fr(11, 3) * C_A[2] + Fr(2, 3) * fT2 + Fr(1, 3) * sT2
    # U(1)_Y, U(1)_X, mixed
    fY = sum(abs(c3) * d2 * qY ** 2 for _, c3, d2, qY, _ in fermions) * nb
    sY = sum(abs(c3) * d2 * qY ** 2 for _, c3, d2, qY, _ in scalars)
    fX = sum(abs(c3) * d2 * x ** 2 for _, c3, d2, _, x in fermions) * nb
    sX = sum(abs(c3) * d2 * x ** 2 for _, c3, d2, _, x in scalars)
    fYX = sum(abs(c3) * d2 * qY * x for _, c3, d2, qY, x in fermions) * nb
    sYX = sum(abs(c3) * d2 * qY * x for _, c3, d2, qY, x in scalars)
    b['U1_Y'] = Fr(2, 3) * fY + Fr(1, 3) * sY
    b['U1_X'] = Fr(2, 3) * fX + Fr(1, 3) * sX
    b['U1_YX_mixing'] = Fr(2, 3) * fYX + Fr(1, 3) * sYX
    # QED below the weak scale (Q = T3 + qY), fermions only (H+- and W+- heavy) : (2/3) sum_Weyl Q^2
    fQ = Fr(0)
    for _, c3, d2, qY, _ in fermions:
        if d2 == 2:
            for t3 in (Fr(1, 2), Fr(-1, 2)):
                fQ += abs(c3) * (t3 + qY) ** 2
        else:
            fQ += abs(c3) * qY ** 2
    b['QED_fermions_only'] = Fr(2, 3) * fQ * nb
    return b


b_model = beta_coefficients(LH_WEYL, SCALARS, N_BLOCKS)
b_sm_check = beta_coefficients(LH_WEYL, [SCALARS[0]], 3)
record('sm_control_b2_minus_19_6_bY_41_6_b3_minus_7', (b_sm_check['SU2'], b_sm_check['U1_Y'], b_sm_check['SU3']) == (Fr(-19, 6), Fr(41, 6), Fr(-7)))
record('model_YX_kinetic_mixing_not_generated_at_one_loop', b_model['U1_YX_mixing'] == 0)
results['one_loop_coefficients_model'] = {k: str(v) for k, v in b_model.items()}
results['one_loop_coefficients_sm_control_3gen_1doublet'] = {k: str(v) for k, v in b_sm_check.items()}
results['one_loop_convention'] = 'd(1/g^2)/d ln mu = - b/(8 pi^2); b = -(11/3)C_A + (2/3) sum_Weyl T + (1/3) sum_complex_scalars T; abelian T = charge^2 with q_Y = y/2.'

# ---------------------------------------------------------------------------
# Scalar degrees of freedom with the axion included: exact rational Hessian
# ---------------------------------------------------------------------------
# Real fields x = (Re Hd1, Im Hd1, Re Hd2, Im Hd2, Re Hu1, Im Hu1, Re Hu2, Im Hu2, theta).
# V = -mu^2(|Hd|^2+|Hu|^2) + ld|Hd|^4 + lu|Hu|^4 + l3|Hd|^2|Hu|^2 + lA|Hd^T i s2 Hu|^2  (theta absent).
# Rational test point chosen so that the aligned vacuum (0, vd), (0, vu) has rational vevs:
#   ld = 1, lu = 5/2, l3 = 1, lA = 3, vd = 2, vu = 1, mu^2 = 9  (both stationarity equations hold exactly;
#   4 ld lu - l3^2 = 9 > 0, so it is a minimum).  The structure, not the values, is being tested.
LD, LU, L3, LA, MU2 = Fr(1), Fr(5, 2), Fr(1), Fr(3), Fr(9)
VD, VU = Fr(2), Fr(1)


def _cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def potential(x):
    hd1, hd2 = (x[0], x[1]), (x[2], x[3])
    hu1, hu2 = (x[4], x[5]), (x[6], x[7])
    nd = sum(t * t for t in x[0:4])
    nu = sum(t * t for t in x[4:8])
    p1, p2 = _cmul(hd1, hu2), _cmul(hd2, hu1)
    w = (p1[0] - p2[0], p1[1] - p2[1])          # Hd^T i s2 Hu = Hd1 Hu2 - Hd2 Hu1
    return -MU2 * (nd + nu) + LD * nd * nd + LU * nu * nu + L3 * nd * nu + LA * (w[0] ** 2 + w[1] ** 2)


X0 = [Fr(0), Fr(0), VD, Fr(0), Fr(0), Fr(0), VU, Fr(0), Fr(0)]
NF = 9


def _second_directional(d):
    """Exact for polynomials of degree <= 5: [-f(2) + 16 f(1) - 30 f(0) + 16 f(-1) - f(-2)]/12."""
    f = {h: potential([X0[i] + h * d[i] for i in range(NF)]) for h in (-2, -1, 0, 1, 2)}
    return (-f[2] + 16 * f[1] - 30 * f[0] + 16 * f[-1] - f[-2]) / 12


def _gradient_zero():
    for i in range(NF):
        e = [Fr(0)] * NF
        e[i] = Fr(1)
        f = {h: potential([X0[k] + h * e[k] for k in range(NF)]) for h in (-2, -1, 1, 2)}
        if (f[-2] - 8 * f[-1] + 8 * f[1] - f[2]) / 12 != 0:   # exact for degree <= 4
            return False
    return True


def _unit(i):
    e = [Fr(0)] * NF
    e[i] = Fr(1)
    return e


HESS = [[Fr(0)] * NF for _ in range(NF)]
for i in range(NF):
    for j in range(NF):
        dp = [a + b for a, b in zip(_unit(i), _unit(j))]
        dm = [a - b for a, b in zip(_unit(i), _unit(j))]
        HESS[i][j] = (_second_directional(dp) - _second_directional(dm)) / 4


def exact_rank(rows):
    m = [list(r) for r in rows]
    rank, ncol = 0, len(m[0]) if m else 0
    for c in range(ncol):
        piv = next((r for r in range(rank, len(m)) if m[r][c] != 0), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        for r in range(len(m)):
            if r != rank and m[r][c] != 0:
                fac = m[r][c] / m[rank][c]
                m[r] = [a - fac * b for a, b in zip(m[r], m[rank])]
        rank += 1
    return rank


# Tangent vectors of gauged generators at the vacuum: dH = i G H for each doublet, d theta = shift.
def _tangent(gd, gu, shift):
    """gd, gu: 2x2 complex matrices as ((re,im),...) acting on (Hd1,Hd2), (Hu1,Hu2); returns real 9-vector of i G H."""
    def act(G, h):
        out = []
        for r in range(2):
            acc = (Fr(0), Fr(0))
            for c in range(2):
                pr = _cmul(G[r][c], h[c])
                acc = (acc[0] + pr[0], acc[1] + pr[1])
            out.append((-acc[1], acc[0]))      # multiply by i
        return out
    hd = [(X0[0], X0[1]), (X0[2], X0[3])]
    hu = [(X0[4], X0[5]), (X0[6], X0[7])]
    td, tu = act(gd, hd), act(gu, hu)
    return [td[0][0], td[0][1], td[1][0], td[1][1], tu[0][0], tu[0][1], tu[1][0], tu[1][1], shift]


Z, ONE, HALF = (Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(1, 2), Fr(0))
T1 = [[Z, HALF], [HALF, Z]]
T2 = [[Z, (Fr(0), Fr(-1, 2))], [(Fr(0), Fr(1, 2)), Z]]
T3 = [[HALF, Z], [Z, (Fr(-1, 2), Fr(0))]]
def _scalar(q):
    return [[(q, Fr(0)), Z], [Z, (q, Fr(0))]]
GAUGED = {
    'T1': _tangent(T1, T1, Fr(0)), 'T2': _tangent(T2, T2, Fr(0)), 'T3': _tangent(T3, T3, Fr(0)),
    'Y': _tangent(_scalar(Fr(1, 2)), _scalar(Fr(1, 2)), Fr(0)),
    'X': _tangent(_scalar(Fr(1)), _scalar(Fr(-1)), Fr(1)),
}
GLOBAL_EXTRA = {   # independent rephasings of the potential (not gauged)
    'U1_d': _tangent(_scalar(Fr(1)), _scalar(Fr(0)), Fr(0)),
    'U1_u': _tangent(_scalar(Fr(0)), _scalar(Fr(1)), Fr(0)),
}

hess_rank = exact_rank(HESS)
nullity = NF - hess_rank
gauge_rank = exact_rank(list(GAUGED.values()))
flat_rank = exact_rank(list(GAUGED.values()) + list(GLOBAL_EXTRA.values()) + [_unit(8)])
in_null = all(all(sum(HESS[i][k] * t[k] for k in range(NF)) == 0 for i in range(NF))
              for t in list(GAUGED.values()) + list(GLOBAL_EXTRA.values()))
q_em = [a + b for a, b in zip(GAUGED['T3'], GAUGED['Y'])]
record('scalar_test_point_is_stationary', _gradient_zero())
record('hessian_rank_4_two_cp_even_two_charged', hess_rank == 4)
record('hessian_nullity_5', nullity == 5)
record('gauge_orbit_rank_4_Q_unbroken', gauge_rank == 4 and all(t == 0 for t in q_em))
record('flat_directions_exactly_global_orbit_plus_theta', flat_rank == nullity and in_null)
record('one_physical_massless_pseudoscalar', nullity - gauge_rank == 1)
results['scalar_degrees_of_freedom'] = {
    'test_point': {'ld': str(LD), 'lu': str(LU), 'l3': str(L3), 'lA': str(LA), 'mu2': str(MU2), 'vd': str(VD), 'vu': str(VU)},
    'real_fields': NF, 'hessian_rank': hess_rank, 'hessian_nullity': nullity,
    'gauged_orbit_rank': gauge_rank, 'global_orbit_plus_theta_rank': flat_rank,
    'physical_massless': nullity - gauge_rank,
    'physical_content': ['h_d, h_u (CP even)', 'H^+- (charged)', 'a (CP odd; massless at tree level; QCD-anomaly mass not computed)'],
    'reason': ('The derived potential is invariant under SU(2) x U(1)_d x U(1)_u and independent of theta; the flat directions at the vacuum are '
               'exactly that orbit plus theta (5), of which the gauged generators remove 4 (Q = T3 + Y unbroken).'),
}

results['checks'] = checks
failed = [k for k, ok in checks.items() if not ok]
(HERE / 'anomaly_sector_results.json').write_text(json.dumps(results, indent=2))
print('anomaly_sector: %d checks, %d failed' % (len(checks), len(failed)))
for k in failed:
    print('  FAILED', k)
print(' one block:', results['anomaly_coefficients_one_block'])
print(' b (model):', results['one_loop_coefficients_model'])
if failed:
    raise SystemExit(1)
