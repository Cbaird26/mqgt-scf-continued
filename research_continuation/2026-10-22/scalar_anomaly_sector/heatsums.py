"""Shared exact-internal-mode heat sums for the stipulated spectral action.

Standard library only (decimal).  Conventions follow the pinned predecessor
notes (research_continuation/2026-10-21 and 2026-10-22, electromagnetic):

    h_n(u)  = n/2 + sum_{l>=1} (2l+n) exp(-u l(l+n)),      u = a/R^2
    H       = 12 h_0 + 28 h_1 + 16 h_2                     (Dirac multiplicities)
    H_Y     = (1/3) h_0 + (32/3) h_1 + (4/3) h_2            (hypercharge weights)
    H_X     =          28 h_1 +     64 h_2                  (X weights, n = x)

    P(a,R)  = a^-2 H,   J(a,R) = a^-1 H,   b_Y = H_Y/(6 pi^2),  b_X = H_X/(6 pi^2)

For a profile f(u) = sum_j w_j exp(-a_j u) every coefficient is the w-weighted
sum of the single-rate kernel.  The flat-vacuum prescription is
F(R) = R P'(R) - 2 P(R) = 0, c = P/R^2, K = P'' - 2c.
"""
from decimal import Decimal as D, getcontext
from fractions import Fraction as Fr

PI_STR = ('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')
DEFAULT_PREC = 95
DEFAULT_LEVELS = 40

# Sector data, inherited (four copied blocks, colour dimensions included)
DIRAC_MULT = {0: Fr(12), 1: Fr(28), 2: Fr(16)}
Y_WEIGHT = {0: Fr(1, 3), 1: Fr(32, 3), 2: Fr(4, 3)}
X_WEIGHT = {0: Fr(0), 1: Fr(28), 2: Fr(64)}


def set_precision(prec=DEFAULT_PREC):
    getcontext().prec = prec


def pi():
    return D(PI_STR)


def frac_to_dec(fr):
    return D(fr.numerator) / D(fr.denominator)


def single_rate_kernels(a, R, levels=DEFAULT_LEVELS):
    """Return dict with P, P_R, P_RR, J, bY, bX for one exponential rate a at radius R.

    Mirrors the predecessor implementation (stationary_profiles.py) but also
    returns the X kernel.  All sums use `levels` internal radial levels.
    """
    H = D(30)            # zero-mode halves: 28*(1/2) + 16*(2/2)
    HR = D(0)
    HRR = D(0)
    HY = D(20) / 3       # (32/3)*(1/2) + (4/3)*1
    HX = D(14) + D(64)   # 28*(1/2) + 64*(2/2) = 78
    HYR = D(0)           # d H_Y / dR
    HXR = D(0)           # d H_X / dR
    R2 = R * R
    R3 = R2 * R
    R4 = R2 * R2
    R6 = R3 * R3
    for n in (0, 1, 2):
        mult = frac_to_dec(DIRAC_MULT[n])
        qy = frac_to_dec(Y_WEIGHT[n])
        qx = frac_to_dec(X_WEIGHT[n])
        for ell in range(1, levels + 1):
            b = a * ell * (ell + n)
            e = (-b / R2).exp()
            val = (2 * ell + n) * e
            H += mult * val
            HR += mult * val * 2 * b / R3
            HRR += mult * val * (4 * b * b / R6 - 6 * b / R4)
            HY += qy * val
            HX += qx * val
            HYR += qy * val * 2 * b / R3
            HXR += qx * val * 2 * b / R3
    six_pi2 = 6 * pi() ** 2
    return {
        'P': H / (a * a), 'P_R': HR / (a * a), 'P_RR': HRR / (a * a),
        'J': H / a, 'bY': HY / six_pi2, 'bX': HX / six_pi2,
        'bY_R': HYR / six_pi2, 'bX_R': HXR / six_pi2,
    }


def profile_coefficients(nodes, weights, R, levels=DEFAULT_LEVELS):
    """Weighted coefficients for a finite exponential mixture at radius R."""
    acc = {k: D(0) for k in ('P', 'P_R', 'P_RR', 'J', 'bY', 'bX', 'bY_R', 'bX_R')}
    for a, w in zip(nodes, weights):
        k = single_rate_kernels(a, R, levels)
        for key in acc:
            acc[key] += w * k[key]
    P, P_R, P_RR, J = acc['P'], acc['P_R'], acc['P_RR'], acc['J']
    c = P / (R * R)
    out = dict(acc)
    out.update({
        'F': R * P_R - 2 * P,
        'c': c,
        'K': P_RR - 2 * c,
        'u_grav': R * R * J / (24 * pi() ** 2),   # (M_4 r)^2 / kappa
        'zY': acc['bY'],                            # Z_Y / kappa
        'zX': acc['bX'],                            # Z_X / kappa
        'zY_R': acc['bY_R'],                        # d(Z_Y/kappa)/dR
        'zX_R': acc['bX_R'],                        # d(Z_X/kappa)/dR
    })
    return out


def local_data(nodes, weights):
    """Inverse moments and derivatives at zero: the retained local profile data."""
    m = {}
    for k in (1, 2, 3):
        m['m%d' % k] = sum((w / a ** k for a, w in zip(nodes, weights)), D(0))
    m['f0'] = sum(weights, D(0))
    m['minus_fprime0'] = sum((w * a for a, w in zip(nodes, weights)), D(0))
    m['fsecond0'] = sum((w * a * a for a, w in zip(nodes, weights)), D(0))
    return m


def newton_stationary_radius(nodes, weights, R0, levels=DEFAULT_LEVELS, tol=None, maxit=60):
    """Solve F(R) = R P'(R) - 2 P(R) = 0 by Newton iteration from R0."""
    if tol is None:
        tol = D(10) ** (-(getcontext().prec - 6))
    R = D(R0)
    for it in range(maxit):
        co = profile_coefficients(nodes, weights, R, levels)
        F = co['F']
        Fp = R * co['K']          # F'(R) = R K(R)
        step = F / Fp
        R = R - step
        if abs(step) < tol:
            return R, it + 1
    raise RuntimeError('Newton did not converge')
