"""Note 22: illustrative compressed two-singlet collider benchmark.

Only tree-level, off-shell Higgs leptonic partial widths and Higgs-pair rates.
No hadronic source data, detector acceptance, or QCD widths are evaluated.
"""
from __future__ import annotations

import math

M_H = 125.0  # GeV, illustrative
G_H = 0.0041  # GeV, illustrative fixed-width propagator
V = 246.0  # GeV, illustrative
SM_H_WIDTH = 0.0041  # GeV, separate illustrative Higgs total width
HBAR_C = 1.973269804e-16  # GeV m
LEPTONS = {'electron': 0.00051099895, 'muon': 0.1056583755, 'tau': 1.77686}


def composite_simpson(f, a, b, n=8192):
    if n < 2 or n % 2:
        raise ValueError('Simpson n must be a positive even integer')
    h = (b - a) / n
    return h / 3 * (f(a) + f(b)
                    + 4 * sum(f(a + j*h) for j in range(1, n, 2))
                    + 2 * sum(f(a + j*h) for j in range(2, n, 2)))


def width_lepton(m1, delta, k12, mf, *, n=8192, contact=False):
    """GeV: Gamma(s2 -> s1 l+l-) with m2=m1+delta, no other channels.

    Integrates s=4mf^2+(delta^2-4mf^2)sin^2(pi*t/2) on t in [0,1].
    This smooths the threshold and recoil endpoint; Yukawa mf is retained.
    """
    if m1 <= 0 or delta <= 0 or mf <= 0 or not all(map(math.isfinite,(m1,delta,k12,mf))):
        raise ValueError('finite positive masses and finite portal coupling required')
    m2 = m1 + delta
    lo, hi = 4*mf*mf, delta*delta
    if lo >= hi or k12 == 0:
        return 0.0
    def integrand(t):
        angle = math.pi*t/2
        s = lo + (hi-lo)*math.sin(angle)**2
        ds_dt = (hi-lo)*math.pi/2*math.sin(math.pi*t)
        if ds_dt <= 0:
            return 0.0
        lam = ((m2+m1)**2-s)*(hi-s)
        beta3 = max(0, 1-lo/s)**1.5
        D = M_H**4 if contact else (M_H*M_H-s)**2 + (M_H*G_H)**2
        return (k12*k12*mf*mf*s*math.sqrt(max(0,lam))*beta3
                /(128*math.pi**3*m2**3*D) * ds_dt)
    return composite_simpson(integrand,0,1,n=n)


def leptonic_floor(m1, delta, k12, *, n=8192):
    widths = {name:width_lepton(m1,delta,k12,mf,n=n) for name,mf in LEPTONS.items()}
    total = sum(widths.values())
    return widths,total,(HBAR_C/total if total > 0 else math.inf)


def reconstructed_mass_matrix(m1, m2, kappa_phi=0.002, kappa_e=0.0):
    """theta=45 degrees. Choose gamma positive; its sign is convention-dependent."""
    if m1 <= 0 or m2 <= m1:
        raise ValueError('require 0 < m1 < m2')
    A = (m1*m1+m2*m2)/2
    gamma = (m2*m2-m1*m1)/2
    mu_phi2 = A-kappa_phi*V*V/2
    mu_e2 = A-kappa_e*V*V/2
    return mu_phi2,mu_e2,gamma,mu_phi2*mu_e2-gamma*gamma


def higgs_pair_widths(m1,m2,k11=0.001,k22=0.001,k12=-0.001):
    """Tree-level widths for h->s1s1, s1s2, s2s2, in GeV."""
    if not (0 < m1 <= m2) or not all(map(math.isfinite,(m1,m2,k11,k22,k12))):
        raise ValueError('masses must be finite, positive, ordered')
    def identical(m,k):
        return 0 if 2*m >= M_H else V*V*k*k/(32*math.pi*M_H)*math.sqrt(1-4*m*m/M_H**2)
    l=(1-(m1+m2)**2/M_H**2)*(1-(m2-m1)**2/M_H**2)
    mixed=(V*V*k12*k12/(16*math.pi*M_H)*math.sqrt(max(l,0))
           if m1+m2 < M_H else 0)
    return identical(m1,k11),mixed,identical(m2,k22)


def contact_ratio_ceiling(delta):
    if not 0 < delta < M_H:
        raise ValueError('require virtual mass endpoint below Higgs pole')
    return 1 / ((1-delta*delta/M_H**2)**2 + (G_H/M_H)**2)


if __name__ == '__main__':
    for delta in (0.8,1.5,2.0,15.0):
        widths,floor,ctau = leptonic_floor(10,delta,0.001)
        print(f'delta={delta:g} GeV: {widths}; leptonic floor={floor:.10g} GeV; c*tau<= {ctau:.10g} m')
    print('m1=10, m2=11.5 bare matrix:',reconstructed_mass_matrix(10,11.5))
    gammas=higgs_pair_widths(10,11.5)
    print('Higgs pair widths:',gammas,'sum=',sum(gammas),'BR=',sum(gammas)/(SM_H_WIDTH+sum(gammas)))