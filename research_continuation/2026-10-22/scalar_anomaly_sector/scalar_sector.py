"""Microscopic scalar sector: representation theory, Yukawa charge conservation,
zero-mode overlaps, Clifford identities, and the local heat-kernel scalar action.

Standard library (fractions, decimal) for every exact statement.  NumPy is used
only for the matrix-level verification of the Clifford/heat-kernel algebra and
for the sphere quadrature cross-check of the exact Beta-function integrals; if
NumPy is absent those checks are skipped and reported as skipped.

Writes scalar_sector_results.json.
"""
from fractions import Fraction as Fr
from decimal import Decimal as D
from math import comb, factorial
from pathlib import Path
import json

import heatsums as hs

HERE = Path(__file__).resolve().parent
hs.set_precision(95)

try:
    import numpy as np
    HAVE_NUMPY = True
except Exception:  # pragma: no cover
    HAVE_NUMPY = False

checks = {}
results = {}


def record(name, ok):
    checks[name] = bool(ok)


# ---------------------------------------------------------------------------
# 1. Charges and Yukawa charge conservation (exact rationals)
# ---------------------------------------------------------------------------
# (SU(3) dim, SU(2)_W rep via monopole index n, q_Y = y/2, x) for the 6D fields
# of one copied block.  n = x (unit X flux); zero modes form spin (n-1)/2.
FIELDS = {
    'Q': {'colour': 3, 'n': 2, 'qY': Fr(1, 6), 'x': Fr(2)},
    'L': {'colour': 1, 'n': 2, 'qY': Fr(-1, 2), 'x': Fr(2)},
    'u': {'colour': 3, 'n': 1, 'qY': Fr(2, 3), 'x': Fr(1)},
    'd': {'colour': 3, 'n': 1, 'qY': Fr(-1, 3), 'x': Fr(1)},
    'e': {'colour': 1, 'n': 1, 'qY': Fr(-1), 'x': Fr(1)},
    'S': {'colour': 3, 'n': 0, 'qY': Fr(1, 6), 'x': Fr(0)},   # n = 0 spectator
}
N_BLOCKS = 4


def sector_weights():
    """Reproduce the inherited sector data D_n, Y_n^2, X_n^2 from the field table."""
    Dn = {0: Fr(0), 1: Fr(0), 2: Fr(0)}
    Yn = {0: Fr(0), 1: Fr(0), 2: Fr(0)}
    Xn = {0: Fr(0), 1: Fr(0), 2: Fr(0)}
    YXn = {0: Fr(0), 1: Fr(0), 2: Fr(0)}
    for f in FIELDS.values():
        n = f['n']
        Dn[n] += N_BLOCKS * f['colour']
        Yn[n] += N_BLOCKS * f['colour'] * f['qY'] ** 2
        Xn[n] += N_BLOCKS * f['colour'] * f['x'] ** 2
        YXn[n] += N_BLOCKS * f['colour'] * f['qY'] * f['x']
    return Dn, Yn, Xn, YXn


Dn, Yn, Xn, YXn = sector_weights()
record('sector_dirac_multiplicities_12_28_16', Dn == {0: 12, 1: 28, 2: 16})
record('sector_hypercharge_weights_1_3_32_3_4_3', Yn == {0: Fr(1, 3), 1: Fr(32, 3), 2: Fr(4, 3)})
record('sector_X_weights_0_28_64', Xn == {0: 0, 1: 28, 2: 64})
record('sector_YX_mixing_vanishes_each_sector', all(v == 0 for v in YXn.values()))
results['sector_weights'] = {'D_n': {k: str(v) for k, v in Dn.items()}, 'Y_n^2': {k: str(v) for k, v in Yn.items()},
                             'X_n^2': {k: str(v) for k, v in Xn.items()}, 'YX_n': {k: str(v) for k, v in YXn.items()}}

# Scalars: Phi_d (qY=1/2, x=+1), Phi_u (qY=1/2, x=-1); in 6D the up-type Yukawa uses Phi_u^*.
SCALARS = {'Phi_d': {'qY': Fr(1, 2), 'x': Fr(1)}, 'Phi_u': {'qY': Fr(1, 2), 'x': Fr(-1)}}


def conserved(op):
    """op = list of (field or scalar label, conjugate flag).  Returns (dqY, dx)."""
    dq = Fr(0)
    dx = Fr(0)
    for label, conj in op:
        tab = FIELDS.get(label) or SCALARS[label]
        s = -1 if conj else 1
        dq += s * tab['qY']
        dx += s * tab['x']
    return dq, dx


# Yukawa operators in 6D: conj(Psi_2) Phi Psi_1  (bar = conjugate)
YUKAWAS = {
    'bar(Q) Phi_d d': [('Q', True), ('Phi_d', False), ('d', False)],
    'bar(L) Phi_d e': [('L', True), ('Phi_d', False), ('e', False)],
    'bar(Q) Phi_u^* u': [('Q', True), ('Phi_u', True), ('u', False)],
}
yuk_table = {}
for name, op in YUKAWAS.items():
    dq, dx = conserved(op)
    yuk_table[name] = {'delta_qY': str(dq), 'delta_x': str(dx), 'monopole_charge_sum_check': str(sum((-1 if c else 1) * (FIELDS.get(l) or SCALARS[l])['x'] for l, c in op) / 2)}
record('all_three_yukawas_conserve_Y_and_X', all(conserved(op) == (0, 0) for op in YUKAWAS.values()))
results['yukawa_charge_conservation'] = yuk_table

# One-doublet obstruction: a single scalar of charge x_H must satisfy all three
one_doublet = {}
for xH in (Fr(1), Fr(-1), Fr(0), Fr(2)):
    ok_d = (-2 + xH + 1 == 0)      # bar(Q) H d
    ok_e = (-2 + xH + 1 == 0)      # bar(L) H e
    ok_u = (-2 - xH + 1 == 0)      # bar(Q) H^* u
    one_doublet[str(xH)] = {'down': ok_d, 'lepton': ok_e, 'up': ok_u}
record('no_single_X_charge_supports_all_three_yukawas', not any(all(v.values()) for v in one_doublet.values()))
results['one_scalar_obstruction'] = one_doublet

# The scalar X charge required by Yukawa conservation is |x|=1; the monopole
# harmonic lowest weight is j = |x|/2 = 1/2: an SU(2)_W doublet.  A Y-charged,
# X-neutral scalar would be an isometry singlet.
record('scalar_x_charge_forces_doublet', all(abs(s['x']) / 2 == Fr(1, 2) for s in SCALARS.values()))
results['lowest_monopole_harmonic_spin'] = {k: str(abs(v['x']) / 2) for k, v in SCALARS.items()}

# ---------------------------------------------------------------------------
# 2. Monopole harmonics: KK spectrum and exact overlaps
# ---------------------------------------------------------------------------
# Charged scalar with monopole charge q = x/2 on S^2_r:  -D^2 Y_{j,m} = [j(j+1) - q^2]/r^2 Y_{j,m},  j = |q|, |q|+1, ...
def scalar_kk_levels(q, count=4):
    j = abs(q)
    out = []
    for _ in range(count):
        out.append({'j': str(j), 'eigenvalue_r2': str(j * (j + 1) - q * q), 'degeneracy': int(2 * j + 1)})
        j += 1
    return out


results['scalar_kk_levels_q_half'] = scalar_kk_levels(Fr(1, 2))
record('lowest_scalar_kk_eigenvalue_is_one_half', Fr(results['scalar_kk_levels_q_half'][0]['eigenvalue_r2']) == Fr(1, 2))
record('next_scalar_kk_eigenvalue_is_seven_halves', Fr(results['scalar_kk_levels_q_half'][1]['eigenvalue_r2']) == Fr(7, 2))

# Fermion internal spectrum: D_n^2 eigenvalues l(l+n)/r^2 (l>=1, degeneracy 2l+n per chirality), n zero modes
results['fermion_kk_levels'] = {str(n): [{'l': l, 'eigenvalue_r2': l * (l + n), 'degeneracy_per_chirality': 2 * l + n} for l in range(1, 4)] for n in (0, 1, 2)}
results['fermion_zero_modes'] = {str(n): {'count': n, 'spin': str(Fr(n - 1, 2)) if n > 0 else 'none'} for n in (0, 1, 2)}

# Orthonormal sections of O(m) in the unitary frame with round measure dOmega = 4 d^2z/(1+|z|^2)^2:
#   s_{m,k}(z) = sqrt((m+1) C(m,k) / (4 pi)) z^k / (1+|z|^2)^{m/2},   k = 0..m
# Zero modes of the charge-n/2 monopole Dirac operator are sections of O(n-1).
# Scalar lowest harmonics for charge 1/2 are sections of O(1).


def radial_beta_integral(k, m):
    """4 pi * Integral_0^inf t^k (1+t)^{-(m+2)} dt = 4 pi * B(k+1, m+1-k): returns the rational factor multiplying pi."""
    # B(k+1, m+1-k) = k! (m-k)! / (m+1)!
    return 4 * Fr(factorial(k) * factorial(m - k), factorial(m + 1))


# Triple overlap: conj(s_{1,k}) * s_{1,k} * s_{0,0}  (n=2 zero mode, charge-1/2 scalar, n=1 zero mode)
# integrand: N2 N1 N0 |z|^{2k} /((1+|z|^2)^{1/2} (1+|z|^2)^{1/2} (1+|z|^2)^0) dOmega
# = N2*N1*N0 * [4 pi B(k+1, 3-k-... )]: total power of (1+|z|^2) in the denominator: 1 + 2 = 3 => m+2 = 3, m = 1
def overlap_squared(k):
    N2sq = Fr(2 * comb(1, k), 4)   # times 1/pi
    N1sq = Fr(2 * comb(1, k), 4)   # times 1/pi
    N0sq = Fr(1, 4)                # times 1/pi
    rad = radial_beta_integral(k, 1)  # times pi
    # overlap = sqrt(N2sq N1sq N0sq / pi^3) * rad * pi  -> overlap^2 = N2sq N1sq N0sq rad^2 / pi
    return N2sq * N1sq * N0sq * rad * rad   # times 1/pi


ov = {k: overlap_squared(k) for k in (0, 1)}
record('zero_mode_yukawa_overlap_squared_is_1_over_4pi', all(v == Fr(1, 4) for v in ov.values()))
record('zero_mode_overlap_su2_covariant_both_components_equal', ov[0] == ov[1])
results['zero_mode_yukawa_overlap'] = {'overlap_squared_times_pi': {str(k): str(v) for k, v in ov.items()},
                                       'statement': 'Integral_S2 conj(psi^(2)_k) Y_{1/2,k} psi^(1)_0 dOmega = 1/sqrt(4 pi) for k = 0, 1 (exact).'}

# Quartic sphere integrals of the lowest harmonics (charge 1/2, m = 1 sections)
# |Phi|^4 with Phi = sum_k H_k s_{1,k}:   Integral = (1/(3 pi)) (H^dagger H)^2
# |Phi_d|^2 |Phi_u^*|^2 = (1/(6 pi)) [ |H_d|^2 |H_u|^2 + |H_d^T i sigma_2 H_u|^2 ]
I0 = radial_beta_integral(0, 2)   # 4 pi B(1,3) = 4pi/3   (times pi)
I1 = radial_beta_integral(1, 2)   # 4 pi B(2,2) = 2pi/3
I2 = radial_beta_integral(2, 2)   # 4 pi B(3,1) = 4pi/3
c4 = Fr(2, 4) ** 2                # (N^2)^2 = (2/(4pi))^2 -> times 1/pi^2
record('quartic_beta_integrals_4pi3_2pi3_4pi3', (I0, I1, I2) == (Fr(4, 3), Fr(2, 3), Fr(4, 3)))
# |Phi|^4 with Phi = H_1 s_{1,0} + H_2 s_{1,1}: after the phi average the surviving terms are
#   |H_1|^4 c4 I0 + |H_2|^4 c4 I2 + |H_1|^2|H_2|^2 c4 (4 I1),
# the last from the 4 = 2 (diagonal pairings) + 2 (interference) equal-weight contributions.
# SU(2) invariance requires the cross coefficient to be twice the self coefficient.
quartic_self = c4 * I0           # coefficient of |H_1|^4 (and of |H_2|^4, since I2 = I0); times 1/pi
record('quartic_self_coefficient_1_over_3pi', quartic_self == Fr(1, 3))
# For the SU(2)-invariant form c (H^dag H)^2 = c(|H1|^4 + |H2|^4 + 2|H1|^2|H2|^2) we need cross = 2c: I0*c4*2 == c4*(2 I1 + 2 I1)
record('quartic_is_su2_invariant_combination', 2 * c4 * I0 == c4 * (2 * I1 + 2 * I1))
# mixed d-u integral: (1/(4 pi^2)) [ (4pi/3) D1 + (2pi/3)(D2 + 2 Re(alpha beta^*)) ] = (1/(6 pi)) [ |Hd|^2|Hu|^2 + |Hd^dag Hu~|^2 ]
mixed_diag = c4 * I0     # coefficient of |Hd1|^2|Hu1|^2 (times 1/pi) = 1/3
mixed_off = c4 * I1      # coefficient of |Hd1|^2|Hu2|^2 = 1/6
mixed_int = c4 * 2 * I1  # coefficient of 2 Re(alpha beta^*) ... = 1/3
record('mixed_quartic_reduces_to_one_sixth_pi_times_two_invariants', (mixed_diag, mixed_off, mixed_int) == (Fr(1, 3), Fr(1, 6), Fr(1, 3)))
results['quartic_sphere_integrals'] = {
    'single_doublet': 'Integral |Phi|^4 dOmega = (1/(3 pi)) (H^dagger H)^2',
    'two_doublets': 'Integral |Phi_d|^2 |Phi_u|^2 dOmega = (1/(6 pi)) [ (H_d^dagger H_d)(H_u^dagger H_u) + |H_d^T i sigma_2 H_u|^2 ]',
    'beta_integrals_times_pi': {'I0': str(I0), 'I1': str(I1), 'I2': str(I2)},
}

# ---------------------------------------------------------------------------
# 3. Clifford algebra and heat-kernel assembly, verified at matrix level
# ---------------------------------------------------------------------------
if HAVE_NUMPY:
    rng = np.random.default_rng(20261022)
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    Z2 = np.zeros((2, 2), dtype=complex)
    g = [np.block([[Z2, -1j * s], [1j * s, Z2]]) for s in (s1, s2, s3)] + [np.block([[Z2, I2], [I2, Z2]])]
    g5 = g[0] @ g[1] @ g[2] @ g[3]
    G = [np.kron(gm, I2) for gm in g] + [np.kron(g5, s1), np.kron(g5, s2)]
    G7 = np.kron(g5, s3)
    I8 = np.eye(8, dtype=complex)
    ok = True
    for A in range(6):
        for B in range(6):
            ok &= np.allclose(G[A] @ G[B] + G[B] @ G[A], 2 * (A == B) * I8)
        ok &= np.allclose(G[A] @ G7 + G7 @ G[A], 0)
        ok &= np.allclose(G[A], G[A].conj().T)
    ok &= np.allclose(G7 @ G7, I8) and np.allclose(G7, G7.conj().T)
    record('clifford_6d_euclidean_algebra', ok)
    # chirality from the product of the six gammas
    prod = I8.copy()
    for A in range(6):
        prod = prod @ G[A]
    record('gamma7_equals_minus_i_times_product_of_six_gammas_up_to_sign', np.allclose(prod, 1j * G7) or np.allclose(prod, -1j * G7))
    # trace identities used in the a_4 assembly
    tr = lambda M: np.trace(M)
    ok_tr = True
    for A in range(6):
        for B in range(6):
            ok_tr &= abs(tr(G[A] @ G7 @ G[B] @ G7) - (-8.0 * (A == B))) < 1e-12
            ok_tr &= abs(tr(G[A] @ G[B]) - 8.0 * (A == B)) < 1e-12
            if A != B:
                GAB = 0.5 * (G[A] @ G[B] - G[B] @ G[A])
                ok_tr &= abs(tr(GAB)) < 1e-12
                for C in range(6):
                    ok_tr &= abs(tr(GAB @ G[C] @ G7)) < 1e-12
        ok_tr &= abs(tr(G[A] @ G7)) < 1e-12
    record('spinor_trace_identities_for_a4', ok_tr)

    # operator-square identity: (D0 + G7 x M)^2 = D0^2 + i G^A G7 x [K_A, M] + 1 x M^2
    # with D0 = i G^A x K_A for arbitrary (not necessarily commuting) matrices K_A, M.
    nint = 5
    def rand_herm(n):
        X = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        return X + X.conj().T
    K = [rand_herm(nint) for _ in range(6)]
    M = rand_herm(nint)
    D0 = sum(1j * np.kron(G[A], K[A]) for A in range(6))
    S = np.kron(G7, M)
    lhs = (D0 + S) @ (D0 + S)
    rhs = D0 @ D0 + sum(1j * np.kron(G[A] @ G7, K[A] @ M - M @ K[A]) for A in range(6)) + np.kron(I8, M @ M)
    record('yukawa_insertion_square_identity_random_matrices', np.allclose(lhs, rhs))

    # Heat-kernel assembly check: with E = E0 + E_Phi, E_Phi = -(1 x M^2) - i G^A G7 x N_A (N_A plays grad_A M),
    # E0 = -(R/4) 1 + (i/2) G^{AB} x F_AB q with G^{AB} = (1/2)[G^A, G^B] (spinor-traceless; the
    # prefactor is irrelevant for every Phi-dependent trace and is left at i/4 below).  Verify
    #   tr E_Phi = -8 tr M^2 ;  tr(E^2) - tr(E0^2) = 4 R tr M^2 + 8 tr M^4 + 8 sum_A tr N_A^2 .
    Rcur = 0.7311
    N = [rand_herm(nint) for _ in range(6)]
    F = rng.normal(size=(6, 6)); F = F - F.T
    q = np.diag(rng.normal(size=nint)).astype(complex)
    E0 = -(Rcur / 4) * np.kron(I8, np.eye(nint)) + sum((1j / 4) * F[A, B] * np.kron(0.5 * (G[A] @ G[B] - G[B] @ G[A]), q) for A in range(6) for B in range(6))
    EPhi = -np.kron(I8, M @ M) - sum(1j * np.kron(G[A] @ G7, N[A]) for A in range(6))
    E = E0 + EPhi
    trM2 = np.trace(M @ M).real
    trM4 = np.trace(M @ M @ M @ M).real
    trN2 = sum(np.trace(N[A] @ N[A]).real for A in range(6))
    ok_hk = abs(np.trace(EPhi).real + 8 * trM2) < 1e-9
    ok_hk &= abs((np.trace(E @ E) - np.trace(E0 @ E0)).real - (4 * Rcur * trM2 + 8 * trM4 + 8 * trN2)) < 1e-8
    # full a_4 Phi-dependent part: (1/360)[60 R tr E_Phi + 180 (tr E^2 - tr E0^2)] = (2/3) R tr M^2 + 4 tr M^4 + 4 tr N^2
    a4_phi = (60 * Rcur * np.trace(EPhi).real + 180 * (np.trace(E @ E) - np.trace(E0 @ E0)).real) / 360
    ok_hk &= abs(a4_phi - (Fr(2, 3) * Rcur * trM2 + 4 * trM4 + 4 * trN2)) < 1e-8
    record('a2_a4_phi_dependent_assembly_matches_formula', ok_hk)

    # sphere quadrature cross-check of the exact quartic integrals (theta, phi grid)
    nth, nph = 1200, 1200
    th = (np.arange(nth) + 0.5) * np.pi / nth
    ph = (np.arange(nph) + 0.5) * 2 * np.pi / nph
    TH, PH = np.meshgrid(th, ph, indexing='ij')
    w = np.sin(TH) * (np.pi / nth) * (2 * np.pi / nph)
    cnorm = 1 / np.sqrt(2 * np.pi)
    Y1 = cnorm * np.cos(TH / 2)
    Y2 = cnorm * np.sin(TH / 2) * np.exp(1j * PH)
    ok_q = abs((np.abs(Y1) ** 2 * w).sum() - 1) < 1e-6 and abs((np.abs(Y2) ** 2 * w).sum() - 1) < 1e-6
    Hd = rng.normal(size=2) + 1j * rng.normal(size=2)
    Hu = rng.normal(size=2) + 1j * rng.normal(size=2)
    Hut = np.array([Hu[1].conj(), -Hu[0].conj()])   # i sigma_2 Hu^*  (components up to overall sign convention)
    Phid = Hd[0] * Y1 + Hd[1] * Y2
    Phiut = Hut[0] * Y1 + Hut[1] * Y2
    quart = (np.abs(Phid) ** 4 * w).sum()
    ok_q &= abs(quart - (np.vdot(Hd, Hd).real ** 2) / (3 * np.pi)) < 1e-6
    mixed = (np.abs(Phid) ** 2 * np.abs(Phiut) ** 2 * w).sum()
    inv1 = np.vdot(Hd, Hd).real * np.vdot(Hu, Hu).real
    inv2 = abs(Hd[0] * Hu[1] - Hd[1] * Hu[0]) ** 2
    ok_q &= abs(mixed - (inv1 + inv2) / (6 * np.pi)) < 1e-6
    record('sphere_quadrature_confirms_quartic_reductions', ok_q)
    results['numpy_quadrature'] = {'quartic_single': quart, 'quartic_single_formula': (np.vdot(Hd, Hd).real ** 2) / (3 * np.pi),
                                   'mixed': mixed, 'mixed_formula': (inv1 + inv2) / (6 * np.pi)}
NUMPY_CHECKS = ['clifford_6d_euclidean_algebra', 'gamma7_equals_minus_i_times_product_of_six_gammas_up_to_sign',
                'spinor_trace_identities_for_a4', 'yukawa_insertion_square_identity_random_matrices',
                'a2_a4_phi_dependent_assembly_matches_formula', 'sphere_quadrature_confirms_quartic_reductions']
if not HAVE_NUMPY:
    for k in NUMPY_CHECKS:
        checks[k] = 'skipped (no numpy)'
results['numpy_dependent_checks'] = NUMPY_CHECKS

# ---------------------------------------------------------------------------
# 4. Local heat-kernel scalar action: exact coefficient bookkeeping
# ---------------------------------------------------------------------------
# Tr f(D^2/Lambda^2) = sum_n Lambda^{6-n} (sum_j w_j a_j^{(n-6)/2}) a_n(D^2),  a_n = (4pi)^{-3} Int tr(alpha_n)
# alpha_2^Phi = -8 tr M^2 ;  alpha_4^Phi = (2/3) R_6 tr M^2 + 4 tr M^4 + 4 tr |grad M|^2
# tr M^2 = 2 tr(Y^dag Y),  tr M^4 = 2 tr (Y^dag Y)^2,  tr|grad M|^2 = 2 tr |grad Y|^2
# S_Phi^loc = (kappa/2)(4pi)^-3 Int d^6x sqrt g [ -16 Lambda^4 m2 tr Y^dag Y + Lambda^2 m1 ( 8 tr|grad Y|^2 + 8 tr (Y^dag Y)^2 + (4/3) R_6 tr Y^dag Y ) ]
# 6D kinetic normalisation per unit Yukawa trace: Z6 = (kappa/2)(4pi)^-3 * 8 Lambda^2 m1 = kappa Lambda^2 m1 / (16 pi^3)
local = {
    'alpha_2_phi': '-8 tr(M^2)',
    'alpha_4_phi': '(2/3) R_6 tr(M^2) + 4 tr(M^4) + 4 tr(|grad_A M|^2)',
    'Z6_over_kappa_Lambda2_m1': str(Fr(1, 16)) + ' / pi^3',
    'm6_squared_over_Lambda2': '-2 (m2/m1) + 1/(3 R^2)      [R_6 = 2/r^2 = 2 Lambda^2/R^2 ; coefficient (4/3)R_6/8 = R_6/6]',
    'doublet_mass_squared_over_Lambda2': '-2 (m2/m1) + 5/(6 R^2)   [adds the exact lowest-harmonic eigenvalue 1/(2 r^2)]',
}
# Yukawa trace structures (per block multiplicities; N_BLOCKS identical copies)
#   N_d = Nb(3 yd^2 + ye^2), N_u = Nb(3 yu^2),  Lam_d = Nb(3 yd^4 + ye^4), Lam_u = Nb(3 yu^4), Lam_A = Nb * 6 yu^2 yd^2
# 4D: V = Z6 sum_i N_i (-mu^2)|H_i|^2 + (Z6 Lambda^2/R^2)[ Lam_d|H_d|^4/(3pi) + Lam_u|H_u|^4/(3pi) + Lam_A(|H_d|^2|H_u|^2 + |H_d^T i s2 H_u|^2)/(6pi) ]
# canonical:  lam_d = Lam_d Lambda^2/(3 pi R^2 Z6 N_d^2), lam_u = Lam_u Lambda^2/(3 pi R^2 Z6 N_u^2), lam_3 = lam_A = Lam_A Lambda^2/(6 pi R^2 Z6 N_d N_u)
# with Z6 = kappa Lambda^2 m1/(16 pi^3):  lam_u = 16 pi^2 / (9 kappa m1 R^2 Nb)  (Yukawa independent)
local['canonical_quartics'] = {
    'lambda_u': '16 pi^2 Lam_u /(3 kappa m1 R^2 N_u^2) = 16 pi^2 /(9 kappa m1 R^2 N_b)',
    'lambda_d': '16 pi^2 Lam_d /(3 kappa m1 R^2 N_d^2)',
    'lambda_3 = lambda_A': '8 pi^2 Lam_A /(3 kappa m1 R^2 N_d N_u)',
    'boundedness': 'all four quartic couplings are positive, so V is bounded below',
    'two_vev_minimum': ('4 lambda_d lambda_u - lambda_3^2 = C^2 Nb^2 yu^4 [27 yd^4 + 12 ye^4]/(N_d^2 N_u^2) > 0 with C = 16 pi^2/(3 kappa m1 R^2) '
                        '(equivalently 16 Lam_d Lam_u > Lam_A^2): an aligned stationary point with both vevs nonzero, when it exists, is a minimum'),
}
results['local_scalar_action'] = local

# Evaluate the exact profile-independent numbers for the pair (m1, m2, R_* from inherited inputs)
inh = json.loads((HERE / 'inherited_inputs_results.json').read_text())
R = D(inh['common_R'])
m1 = D(inh['profiles']['minus']['local_data']['m1'])
m2 = D(inh['profiles']['minus']['local_data']['m2'])
m1p = D(inh['profiles']['plus']['local_data']['m1'])
m2p = D(inh['profiles']['plus']['local_data']['m2'])
record('m1_m2_common_to_pair', abs(m1 - m1p) < D('1e-90') and abs(m2 - m2p) < D('1e-90'))
record('scale_convention_m2_over_m1_is_one', abs(m2 / m1 - 1) < D('1e-85'))
mu2 = 2 * m2 / m1 - D(5) / (6 * R * R)            # mu^2/Lambda^2 (positive => tachyonic doublet)
m6sq = -2 * m2 / m1 + 1 / (3 * R * R)
results['pair_evaluation'] = {
    'R_star': str(R), 'm1': str(m1), 'm2': str(m2), 'm2_over_m1': str(m2 / m1),
    'm6_squared_over_Lambda2': str(m6sq),
    'mu_squared_over_Lambda2 (= -doublet mass^2 / Lambda^2)': str(mu2),
    'tachyon_condition_R2_m2_over_m1_gt_5_over_12': str(R * R * m2 / m1),
    'next_harmonic_mass2_over_Lambda2 (j=3/2)': str(m6sq + D(7) / (2 * R * R)),
    'lambda_u_times_kappa_m1_R2_Nb': str(16 * hs.pi() ** 2 / 9),
    'lambda_u_times_kappa (Nb=4)': str(16 * hs.pi() ** 2 / (9 * m1 * R * R * 4)),
}
record('lowest_doublet_tachyonic_in_local_truncation', mu2 > 0)
record('next_harmonic_j_3_2_not_tachyonic', m6sq + D(7) / (2 * R * R) > 0)
# Yukawa-weighted vev scale of the truncated minimum in the special case y_e = 0 (all four quartics equal):
#   M^2_max = mu^2/2, independent of kappa, Nb and the remaining Yukawas.  The general case (fixture y_e = 1)
#   is evaluated from the actual vacuum in vacuum_matching.py.
results['pair_evaluation']['yukawa_weighted_vev_M2max_over_Lambda2_if_ye_0'] = str(mu2 / 2)
nodes = [D(x) for x in json.loads((HERE / 'inputs' / 'common_vacuum_pair.json').read_text())['nodes']]
results['pair_evaluation']['expansion_parameters_a_j_M2max_over_Lambda2_if_ye_0'] = [str((a * mu2 / 2).quantize(D('1e-12'))) for a in nodes]
record('truncated_minimum_outside_local_validity_if_ye_0', max(a * mu2 / 2 for a in nodes) > 1)

results['checks'] = checks
failed = [k for k, ok in checks.items() if ok is False]
(HERE / 'scalar_sector_results.json').write_text(json.dumps(results, indent=2, default=str))
print('scalar_sector: %d checks, %d failed, %d skipped' % (len(checks), len(failed), sum(1 for v in checks.values() if isinstance(v, str))))
for k in failed:
    print('  FAILED', k)
print(' mu^2/Lambda^2 =', str(mu2)[:20], ' m6^2/Lambda^2 =', str(m6sq)[:20], ' R^2 m2/m1 =', str(R * R * m2 / m1)[:12])
if failed:
    raise SystemExit(1)
