"""Note 23: exact tree-level 2x2 mass and portal rotation for an illustrative model.

No loops, hadronic inputs, detector efficiencies or experimental constraints.
"""
from __future__ import annotations
import math

V = 246.0
KPHI, KE = 0.002, 0.0
M1_0, M2_0 = 10.0, 11.5
A0 = (M1_0**2 + M2_0**2) / 2
GAMMA = (M2_0**2 - M1_0**2) / 2
MU_PHI2 = A0 - KPHI * V**2 / 2
MU_E2 = A0 - KE * V**2 / 2


def spectrum(delta_phi2=0.0, delta_e2=0.0, *, kphi=KPHI, ke=KE, gamma=GAMMA):
    """Return ordered masses and rotated portal coefficients.

    delta_*2 shift *bare squared masses* in GeV^2. If portals drift,
    specify new kphi/ke too; both masses and vertices then change.
    """
    values = (delta_phi2, delta_e2, kphi, ke, gamma)
    if not all(map(math.isfinite, values)):
        raise ValueError('all parameters must be finite')
    A = MU_PHI2 + delta_phi2 + kphi * V**2 / 2
    B = MU_E2 + delta_e2 + ke * V**2 / 2
    gap = math.hypot(A-B, 2*gamma)
    low, high = (A+B-gap)/2, (A+B+gap)/2
    if low <= 0:
        raise ValueError('nonpositive squared-mass eigenvalue')
    costwo = (A-B)/gap if gap else 0.0
    sintwo = 2*gamma/gap if gap else 0.0
    k11 = (kphi+ke-(kphi-ke)*costwo)/2
    k22 = (kphi+ke+(kphi-ke)*costwo)/2
    k12abs = abs(kphi-ke)*abs(sintwo)/2
    return dict(m1=math.sqrt(low), m2=math.sqrt(high),
                delta=math.sqrt(high)-math.sqrt(low),
                k11=k11, k22=k22, k12abs=k12abs,
                sin2theta=sintwo, A=A, B=B, gap=gap,
                eig_low=low, eig_high=high)


def window_boundaries(target_delta=2.0):
    """Bare-Phi squared-mass shifts with exact mass gap target_delta.

    This formula holds only at fixed B=A0 and gamma=GAMMA, with
    admissible positive squared-mass eigenvalues at both returned roots.
    """
    if not math.isfinite(target_delta) or target_delta <= 0:
        raise ValueError('target mass gap must be finite and positive')
    radicand = A0*target_delta**2 - GAMMA**2
    if radicand < 0:
        raise ValueError('no real roots for the requested gap')
    eps_low = target_delta**2 - 2*math.sqrt(radicand)
    eps_high = target_delta**2 + 2*math.sqrt(radicand)
    for eps in (eps_low, eps_high):
        if A0*(A0+eps)-GAMMA**2 <= 0:
            raise ValueError('boundary gives nonpositive eigenvalue')
    return eps_low, eps_high


def required_nonleptonic_ratio(length_m, leptonic_ceiling_m=644803.0):
    """Necessary total additional/leptonic width ratio for c*tau<=length_m.

    Uses only Note 22's *unperturbed* conditional leptonic ceiling.
    This does not calculate or infer any actual hadronic or photon width.
    """
    if not all(map(math.isfinite, (length_m, leptonic_ceiling_m))) or length_m <= 0 or leptonic_ceiling_m <= 0:
        raise ValueError('lengths must be positive and finite')
    return max(0.0, leptonic_ceiling_m/length_m-1)


if __name__ == '__main__':
    print('bare squared masses:', MU_PHI2, MU_E2, 'gamma:', GAMMA)
    print('Delta<=2 GeV one-direction epsilon boundaries:', window_boundaries())
    for eps in (0, 1, -1, 5, -5, 16.125, -16.125, 32.25, -32.25):
        s = spectrum(eps)
        print('epsilon=%+8.3f GeV^2: masses=(%.8f, %.8f) GeV, gap=%.8f GeV, |K12|=%.10f' %
              (eps, s['m1'], s['m2'], s['delta'], s['k12abs']))
    for length in (1000, 1, .001):
        print('c*tau<=%g m requires other/leptonic width >= %.9g' %
              (length, required_nonleptonic_ratio(length)))
