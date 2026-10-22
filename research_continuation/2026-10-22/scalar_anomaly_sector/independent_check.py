"""Independent floating-point cross-check (NumPy + SciPy) of the stdlib results.

Separately coded heat sums (vectorised, 80 levels), SciPy generalized
eigensolver for the neutral spectrum, SVD null space, Brent root solves for the
stationary radii, dblquad for the sphere integrals, and an independent
enumeration of the Weyl states for the anomaly sums.

Writes independent_check_results.json.  Requires numpy and scipy.
"""
from fractions import Fraction as Fr
from pathlib import Path
import json
import numpy as np
from scipy import linalg, optimize, integrate

HERE = Path(__file__).resolve().parent
checks = {}
out = {}


def record(k, ok):
    checks[k] = bool(ok)


pair = json.loads((HERE / 'inputs' / 'common_vacuum_pair.json').read_text())
weak = json.loads((HERE / 'inputs' / 'inherited_weak_coefficients.json').read_text())
inh = json.loads((HERE / 'inherited_inputs_results.json').read_text())
vm = json.loads((HERE / 'vacuum_matching_results.json').read_text())
an = json.loads((HERE / 'anomaly_sector_results.json').read_text())

nodes = np.array([float(x) for x in pair['nodes']])
Wm = np.array([float(x) for x in pair['weights_minus']])
Wp = np.array([float(x) for x in pair['weights_plus']])
Rs = float(pair['common_R'])
LEVELS = 80
ell = np.arange(1, LEVELS + 1, dtype=float)
SECTORS = [(0, 12.0, 1 / 3, 0.0), (1, 28.0, 32 / 3, 28.0), (2, 16.0, 4 / 3, 64.0)]


def kernels(a, R):
    """Vectorised single-rate kernels: P, P_R, P_RR, J, bY, bX."""
    a = np.atleast_1d(a)[:, None]
    H = 30.0 * np.ones(a.shape[0]); HR = np.zeros(a.shape[0]); HRR = np.zeros(a.shape[0]); HY = 20 / 3 * np.ones(a.shape[0]); HX = 78.0 * np.ones(a.shape[0])
    for n, mult, qy, qx in SECTORS:
        b = a * ell * (ell + n)
        e = np.exp(-b / R ** 2) * (2 * ell + n)
        H += mult * e.sum(1); HR += mult * (e * 2 * b / R ** 3).sum(1); HRR += mult * (e * (4 * b * b / R ** 6 - 6 * b / R ** 4)).sum(1)
        HY += qy * e.sum(1); HX += qx * e.sum(1)
    a = a[:, 0]
    return H / a ** 2, HR / a ** 2, HRR / a ** 2, H / a, HY / (6 * np.pi ** 2), HX / (6 * np.pi ** 2)


def profile(w, R):
    P, PR, PRR, J, bY, bX = kernels(nodes, R)
    P, PR, PRR, J, zY, zX = (w @ P, w @ PR, w @ PRR, w @ J, w @ bY, w @ bX)
    c = P / R ** 2
    return {'P': P, 'P_R': PR, 'F': R * PR - 2 * P, 'J': J, 'c': c, 'K': PRR - 2 * c, 'zY': zY, 'zX': zX}


# 1. inherited pair
res = {}
for name, w in (('minus', Wm), ('plus', Wp)):
    pr = profile(w, Rs)
    rec = inh['profiles'][name]['coefficients_60_levels']
    err = max(abs(pr[k] - float(rec[k])) / max(1.0, abs(float(rec[k]))) for k in ('P', 'P_R', 'J', 'c', 'K', 'zY', 'zX'))
    record('float_profile_matches_decimal_%s' % name, err < 5e-14)
    record('float_stationarity_%s' % name, abs(pr['F']) < 1e-11)
    res[name] = {k: float(v) for k, v in pr.items()}
    res[name]['relative_error_vs_decimal'] = err
out['profiles'] = res
dzY = res['plus']['zY'] - res['minus']['zY']
record('float_delta_zY', abs(dzY - 9.3119787986548684e-8) < 1e-15)
# pure exponential control via Brent
def F_pure_exponential(R):
    P, PR, _, _, _, _ = kernels(np.array([1.0]), R)
    return R * PR[0] - 2 * P[0]


Re = optimize.brentq(F_pure_exponential, 1.2, 1.4, xtol=1e-15)
record('float_pure_exponential_root', abs(Re - 1.3007832832273603) < 1e-12)
out['pure_exponential_root'] = Re

# 2. anomaly sums by explicit enumeration of Weyl states (LH basis), one block
states = []   # (colour index irrelevant) each entry: (T3, qY, x, colour_rep)  with colour_rep in {3, -3, 1}
for c in range(3):
    for t3 in (0.5, -0.5):
        states.append((t3, Fr(1, 6), Fr(2), 3))        # Q
for t3 in (0.5, -0.5):
    states.append((t3, Fr(-1, 2), Fr(2), 1))            # L
for c in range(3):
    states.append((0.0, Fr(-2, 3), Fr(-1), -3))         # u^c
    states.append((0.0, Fr(1, 3), Fr(-1), -3))          # d^c
states.append((0.0, Fr(1), Fr(-1), 1))                  # e^c
A = {}
A['Y^2 X'] = sum(qY ** 2 * x for _, qY, x, _ in states)
A['Y X^2'] = sum(qY * x ** 2 for _, qY, x, _ in states)
A['X^3'] = sum(x ** 3 for _, qY, x, _ in states)
A['grav^2 X'] = sum(x for _, qY, x, _ in states)
A['Y^3'] = sum(qY ** 3 for _, qY, x, _ in states)
A['grav^2 Y'] = sum(qY for _, qY, x, _ in states)
A['SU2^2 X'] = sum(Fr(1, 2) * x for t3, qY, x, _ in states if t3 != 0) / 2   # each doublet has two states; T(2)=1/2 per doublet
A['SU2^2 Y'] = sum(Fr(1, 2) * qY for t3, qY, x, _ in states if t3 != 0) / 2
A['SU3^2 X'] = sum(Fr(1, 2) * x for _, qY, x, cr in states if abs(cr) == 3) / 3
A['SU3^2 Y'] = sum(Fr(1, 2) * qY for _, qY, x, cr in states if abs(cr) == 3) / 3
record('anomaly_enumeration_matches', all(str(A[k]) == an['anomaly_coefficients_one_block'][k] for k in A))
out['anomaly_one_block_enumeration'] = {k: str(v) for k, v in A.items()}
record('weyl_state_count_15', len(states) == 15)

# 3. neutral spectrum via SciPy generalized eigensolver
zW = {'minus': float(weak['zW_minus']), 'plus': float(weak['zW_plus'])}
hd = np.array([-0.5, 0.5, 1.0]); hu = np.array([-0.5, 0.5, -1.0]); eX = np.array([0, 0, 1.0])
spec = {}
for fx, d in vm['neutral_sector'].items():
    spec[fx] = {}
    for name in ('minus', 'plus'):
        e = d[name]
        vd2, vu2, mst2 = float(e['vd2']), float(e['vu2']), float(e['M_St2'])
        M2 = vd2 * np.outer(hd, hd) + vu2 * np.outer(hu, hu) + mst2 * np.outer(eX, eX)
        K = np.diag([zW[name], res[name]['zY'], res[name]['zX']])
        vals, vecs = linalg.eigh(M2, K)
        vals = np.sort(vals)
        # null space from SVD of M2
        u, s, vt = np.linalg.svd(M2)
        null = vt[-1]
        null = null / null[np.argmax(np.abs(null))]
        einv2 = null @ K @ null / (null[0] ** 2) if abs(null[0]) > 0 else np.nan
        ok = abs(vals[0]) < 1e-12 and abs(vals[1] - float(e['m2_massive_light'])) < 1e-10 and abs(vals[2] - float(e['m2_massive_heavy'])) < 1e-10
        ok &= np.allclose(np.abs(null), [1, 1, 0], atol=1e-10)
        ok &= abs(einv2 - float(e['e_inv2_over_kappa'])) < 1e-12
        record('scipy_spectrum_%s_%s' % (fx, name), ok)
        spec[fx][name] = {'generalized_eigenvalues': vals.tolist(), 'null_vector': null.tolist(), 'e_inv2': einv2}
out['neutral_spectrum'] = spec

# 4. coupled radius in the hierarchical regime (eps = 1e-4) by Brent
m1 = float(inh['profiles']['minus']['local_data']['m1']); m2 = float(inh['profiles']['minus']['local_data']['m2'])
gamma = float(vm['gamma_vev_coefficient']['gamma'])
B = 5 / 6
for eps_str, e in vm['vacuum']['hierarchical_regime'].items():
    eps = float(eps_str)
    delta2 = 2 * m2 / m1 - B / Rs ** 2 - eps
    mu2 = lambda R: 2 * m2 / m1 - delta2 - B / R ** 2
    Gt = lambda R: -(10 * np.pi ** 2 / 3) * gamma * mu2(R)
    for name, w in (('minus', Wm), ('plus', Wp)):
        Ftot = lambda R: profile(w, R)['F'] + Gt(R)
        Rt = optimize.brentq(Ftot, Rs - 0.05, Rs + 0.05, xtol=1e-15)
        record('scipy_hier_%s_%s' % (eps_str, name), abs(Rt - float(e[name]['R_tilde'])) < 1e-11)
        out.setdefault('hierarchical_roots', {})['%s_%s' % (eps_str, name)] = Rt
# untuned: no root on a fine grid
def Gt0(R):
    mu2 = 2 * m2 / m1 - B / R ** 2
    return -(10 * np.pi ** 2 / 3) * gamma * mu2 if mu2 > 0 else 0.0   # no vev below the tachyon threshold


grid = np.linspace(0.1, 6.0, 591)
Ft_grid = np.array([profile(Wm, R)['F'] + Gt0(R) for R in grid])
record('scipy_untuned_F_tot_negative_on_grid', Ft_grid.max() < 0)
out['untuned_max_F_tot_grid_0.1_6'] = float(Ft_grid.max())

# 5. sphere integrals by dblquad: |Y_{1/2,0}|^4 and the mixed integral for fixed random H
rng = np.random.default_rng(7)
Hd = rng.normal(size=2) + 1j * rng.normal(size=2)
Hu = rng.normal(size=2) + 1j * rng.normal(size=2)
Hut = np.array([np.conj(Hu[1]), -np.conj(Hu[0])])
def Y(th, ph):
    c = 1 / np.sqrt(2 * np.pi)
    return c * np.cos(th / 2), c * np.sin(th / 2) * np.exp(1j * ph)
def integrand_quartic(ph, th):
    y1, y2 = Y(th, ph)
    return abs(Hd[0] * y1 + Hd[1] * y2) ** 4 * np.sin(th)
def integrand_mixed(ph, th):
    y1, y2 = Y(th, ph)
    return abs(Hd[0] * y1 + Hd[1] * y2) ** 2 * abs(Hut[0] * y1 + Hut[1] * y2) ** 2 * np.sin(th)
q4, _ = integrate.dblquad(integrand_quartic, 0, np.pi, 0, 2 * np.pi, epsabs=1e-10, epsrel=1e-10)
qm, _ = integrate.dblquad(integrand_mixed, 0, np.pi, 0, 2 * np.pi, epsabs=1e-10, epsrel=1e-10)
inv1 = np.vdot(Hd, Hd).real * np.vdot(Hu, Hu).real
inv2 = abs(Hd[0] * Hu[1] - Hd[1] * Hu[0]) ** 2
record('dblquad_quartic_single', abs(q4 - np.vdot(Hd, Hd).real ** 2 / (3 * np.pi)) < 1e-8)
record('dblquad_quartic_mixed', abs(qm - (inv1 + inv2) / (6 * np.pi)) < 1e-8)
out['dblquad'] = {'quartic': q4, 'quartic_formula': np.vdot(Hd, Hd).real ** 2 / (3 * np.pi), 'mixed': qm, 'mixed_formula': (inv1 + inv2) / (6 * np.pi)}
# Zero modes derived from the monopole Dirac operator, independently of the O(n-1)-section form used in Lemma 2.
# Unit sphere, north gauge A = q(1 - cos th) d phi, frame e1 = d th, e2 = sin th d phi:
#   D_q = s1 (d_th + cot(th)/2) + s2 (1/sin th)(d_phi - i A_phi).
# Upper-component modes u = e^{i m phi} g(th) satisfy g'/g = -cot(th)/2 + (m - q(1 - cos th))/sin th.
# Integrate numerically from th = pi/2, normalise, and compare with the claimed densities; then compute the overlap.
from scipy.integrate import solve_ivp, quad


def zero_mode_profile(q, m):
    rhs = lambda th, y: [y[0] * (-0.5 / np.tan(th) + (m - q * (1 - np.cos(th))) / np.sin(th))]
    th_lo, th_hi = 1e-6, np.pi - 1e-6
    up = solve_ivp(rhs, (np.pi / 2, th_hi), [1.0], rtol=1e-12, atol=1e-14, dense_output=True)
    dn = solve_ivp(rhs, (np.pi / 2, th_lo), [1.0], rtol=1e-12, atol=1e-14, dense_output=True)
    g = lambda th: up.sol(th)[0] if th >= np.pi / 2 else dn.sol(th)[0]
    norm2 = 2 * np.pi * (quad(lambda t: g(t) ** 2 * np.sin(t), th_lo, np.pi / 2, limit=200)[0]
                         + quad(lambda t: g(t) ** 2 * np.sin(t), np.pi / 2, th_hi, limit=200)[0])
    return lambda th: g(th) / np.sqrt(norm2), norm2


modes = {(1.0, 0.5): None, (1.0, 1.5): None, (0.5, 0.5): None}
for key in modes:
    modes[key] = zero_mode_profile(*key)[0]
# claimed unit-normalised densities: q=1 -> cos^2(th/2)/(2pi), sin^2(th/2)/(2pi); q=1/2 -> 1/(4pi)
ths = np.linspace(0.05, np.pi - 0.05, 60)
dens_ok = (max(abs(modes[(1.0, 0.5)](t) ** 2 - np.cos(t / 2) ** 2 / (2 * np.pi)) for t in ths) < 1e-8
           and max(abs(modes[(1.0, 1.5)](t) ** 2 - np.sin(t / 2) ** 2 / (2 * np.pi)) for t in ths) < 1e-8
           and max(abs(modes[(0.5, 0.5)](t) ** 2 - 1 / (4 * np.pi)) for t in ths) < 1e-8)
record('dirac_ode_zero_mode_densities_match_O_n_minus_1_sections', dens_ok)
# normalisability selects exactly n modes: neighbouring m values are not normalisable (log-divergent norm)
def norm_grows(q, m):
    rhs = lambda th, y: [y[0] * (-0.5 / np.tan(th) + (m - q * (1 - np.cos(th))) / np.sin(th))]
    vals = []
    for eps_ in (1e-3, 1e-5):
        up = solve_ivp(rhs, (np.pi / 2, np.pi - eps_), [1.0], rtol=1e-10, atol=1e-14, dense_output=True)
        dn = solve_ivp(rhs, (np.pi / 2, eps_), [1.0], rtol=1e-10, atol=1e-14, dense_output=True)
        n2 = quad(lambda t: dn.sol(t)[0] ** 2 * np.sin(t), eps_, np.pi / 2, limit=400)[0] + quad(lambda t: up.sol(t)[0] ** 2 * np.sin(t), np.pi / 2, np.pi - eps_, limit=400)[0]
        vals.append(n2)
    return vals[1] > vals[0] * 1.5
record('dirac_ode_exactly_n_normalisable_modes', norm_grows(1.0, -0.5) and norm_grows(1.0, 2.5) and norm_grows(0.5, -0.5) and norm_grows(0.5, 1.5))
# scalar monopole harmonics q = 1/2: check -D^2 Y = Y/2 by finite differences (Lemma 1)
qs = 0.5
Theta = {0: lambda t: np.cos(t / 2) / np.sqrt(2 * np.pi), 1: lambda t: np.sin(t / 2) / np.sqrt(2 * np.pi)}
def minus_D2_over_Y(k, t, h=1e-4):
    f = Theta[k]
    d1 = lambda tt: (f(tt + h) - f(tt - h)) / (2 * h)
    lap = -((np.sin(t + h) * d1(t + h) - np.sin(t - h) * d1(t - h)) / (2 * h)) / np.sin(t)
    return (lap + (k - qs * (1 - np.cos(t))) ** 2 / np.sin(t) ** 2 * f(t)) / f(t)
eig_ok = all(abs(minus_D2_over_Y(k, t) - 0.5) < 1e-5 for k in (0, 1) for t in np.linspace(0.3, np.pi - 0.3, 25))
record('scalar_monopole_harmonics_eigenvalue_one_half_finite_difference', eig_ok)
# overlap: phi integral gives 2 pi delta_{m, k + 1/2}; theta integral with the ODE-derived profiles
def overlap(m, k):
    return 2 * np.pi * quad(lambda t: modes[(1.0, m)](t) * Theta[k](t) * modes[(0.5, 0.5)](t) * np.sin(t), 1e-6, np.pi - 1e-6, limit=200)[0]
ov = [overlap(0.5, 0), overlap(1.5, 1)]
record('ode_derived_zero_mode_overlap_1_over_sqrt_4pi', all(abs(abs(o) - 1 / np.sqrt(4 * np.pi)) < 1e-7 for o in ov))
out['zero_mode_overlap'] = ov

# 6. scalar Hessian (untuned fixture) via numpy eig
sp = vm['scalar_spectrum_untuned_fixture']
ld, lu, l3 = (float(vm['canonical_quartics_times_kappa_R2'][k]) / Rs ** 2 for k in ('ell_d', 'ell_u', 'ell_3=ell_A'))
sd, su = float(vm['vacuum']['at_common_radius_untuned']['sigma_d = vhat_d^2/(kappa Lambda^2)']), float(vm['vacuum']['at_common_radius_untuned']['sigma_u'])
Hs = np.array([[2 * ld * sd, l3 * np.sqrt(sd * su)], [l3 * np.sqrt(sd * su), 2 * lu * su]])
ev = np.sort(np.linalg.eigvalsh(Hs))
record('numpy_scalar_hessian', abs(ev[0] - float(sp['m2_h_light_over_Lambda2'])) < 1e-10 and abs(ev[1] - float(sp['m2_h_heavy_over_Lambda2'])) < 1e-10)
# stationarity of the untuned vevs
mu2s = float(vm['vacuum']['at_common_radius_untuned']['mu2_over_Lambda2'])
record('numpy_vev_stationarity', abs(2 * ld * sd + l3 * su - 2 * mu2s) < 1e-12 and abs(l3 * sd + 2 * lu * su - 2 * mu2s) < 1e-12)

out['checks'] = checks
out['environment'] = {'numpy': np.__version__, 'scipy': __import__('scipy').__version__}
failed = [k for k, v in checks.items() if not v]
(HERE / 'independent_check_results.json').write_text(json.dumps(out, indent=2, default=float))
print('independent_check: %d checks, %d failed' % (len(checks), len(failed)))
for k in failed:
    print('  FAILED', k)
if failed:
    raise SystemExit(1)
