"""Note 27: restricted tree-level Higgs-portal elastic nucleon scattering.

GeV natural units except sigma_cm2. No relic-density calculation or limit test.
"""
from __future__ import annotations
import math

M_H = 125.0            # illustrative Higgs pole mass, GeV
V = 246.0              # illustrative Higgs vacuum expectation value, GeV
M_N = 0.9382720813     # illustrative proton mass, GeV
GEV_MINUS2_TO_CM2 = 0.389379338e-27


def _positive_finite(**parameters):
    if any(not math.isfinite(value) or value <= 0 for value in parameters.values()):
        raise ValueError('all supplied masses, v and f_N must be positive and finite')


def higgs_to_light_pair_width(m1=10.0, k11=0.001, *, mh=M_H, v=V):
    """GeV; L_int=-v*k11*h*s1**2/2; zero for closed threshold."""
    _positive_finite(m1=m1, mh=mh, v=v)
    if not math.isfinite(k11):
        raise ValueError('portal must be finite')
    if 2*m1 >= mh:
        return 0.0
    beta = math.sqrt(1-4*m1*m1/(mh*mh))
    return v*v*k11*k11*beta/(32*math.pi*mh)


def nucleon_cross_section(m1=10.0, k11=0.001, *, f_n=0.30,
                          mn=M_N, mh=M_H):
    """cm^2; leading zero-momentum Higgs-exchange s1-N SI cross section."""
    _positive_finite(m1=m1, f_n=f_n, mn=mn, mh=mh)
    if not math.isfinite(k11):
        raise ValueError('portal must be finite')
    sigma_gev2=(k11*k11*f_n*f_n*mn**4 /
                (4*math.pi*(m1+mn)**2*mh**4))
    return sigma_gev2*GEV_MINUS2_TO_CM2


def crossing_ratio_cm2_per_gev(m1=10.0, *, f_n=0.30,
                                mn=M_N, mh=M_H, v=V):
    """sigma_SI / Gamma(h->s1s1) when 2*m1<m_h, k11 != 0."""
    _positive_finite(m1=m1, f_n=f_n, mn=mn, mh=mh, v=v)
    if 2*m1 >= mh:
        raise ValueError('crossing ratio requires an open Higgs pair channel')
    beta=math.sqrt(1-4*m1*m1/(mh*mh))
    ratio=(8*f_n*f_n*mn**4/
           (v*v*mh**3*(m1+mn)**2*beta))
    return ratio*GEV_MINUS2_TO_CM2


def density_rescaled_cross_section(sigma_cm2, xi):
    """Effective sigma for local density fraction xi, equal velocity distribution.

    This is a rate rescaling, NOT a new microscopic scattering cross section.
    """
    if not math.isfinite(sigma_cm2) or sigma_cm2 < 0:
        raise ValueError('cross section must be finite and nonnegative')
    if not math.isfinite(xi) or not 0 <= xi <= 1:
        raise ValueError('xi must be in [0,1]')
    return xi*sigma_cm2


def inelastic_target_kinetic_threshold(m1=10.0, m2=11.5, target_mass=M_N):
    """Incident s1 laboratory kinetic energy in GeV for s1+T->s2+T (T at rest)."""
    _positive_finite(m1=m1, m2=m2, target_mass=target_mass)
    if m2 <= m1:
        raise ValueError('requires heavier final singlet')
    return ((m2+target_mass)**2-m1*m1-target_mass*target_mass)/(2*target_mass)-m1


if __name__ == '__main__':
    gamma=higgs_to_light_pair_width()
    sigma=nucleon_cross_section()
    print('Gamma(h->s1s1) [GeV]:',format(gamma,'.12g'))
    print('sigma_SI(s1-proton) [cm^2] with f_N=0.30:',format(sigma,'.12g'))
    print('sigma/Gamma [cm^2/GeV]:',format(crossing_ratio_cm2_per_gev(),'.12g'))
    print('inelastic free-proton kinetic threshold [GeV]:',
          format(inelastic_target_kinetic_threshold(),'.12g'))
