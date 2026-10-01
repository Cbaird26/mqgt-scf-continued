"""Note 26: relativistic kinematics and restricted free-singlet pair thresholds.

No optical amplitudes, SM h-gamma matching, QCD, H2 rates, or laboratory data.
All energies GeV and s in GeV^2. Optical photon energy is illustrative.
"""
import math

M1 = 10.0
M2 = 11.5
EV_TO_GEV = 1.0e-9


def pair_threshold(m_a, m_b):
    """Invariant squared-mass threshold for two positive-mass particles."""
    if not all(math.isfinite(x) and x > 0 for x in (m_a, m_b)):
        raise ValueError('finite strictly positive final masses required')
    return (m_a + m_b) ** 2


def two_photon_s(energy_a, energy_b, cos_angle):
    """Mandelstam s for two incident real photons, energies GeV.

    Their relative three-momentum angle is between 0 and pi. No material
    target/external-field energy transfer is included.
    """
    if not all(map(math.isfinite, (energy_a, energy_b, cos_angle))):
        raise ValueError('nonfinite input')
    if energy_a <= 0 or energy_b <= 0 or not -1 <= cos_angle <= 1:
        raise ValueError('photons have positive energy, cosine in [-1,1]')
    return 2 * energy_a * energy_b * (1 - cos_angle)


def photon_pair_open(energy_a, energy_b, cos_angle, m_a, m_b):
    return two_photon_s(energy_a, energy_b, cos_angle) >= pair_threshold(m_a, m_b)


def min_equal_head_on_photon_energy(m_a, m_b):
    """Energy per photon required at the two-to-two head-on threshold."""
    return math.sqrt(pair_threshold(m_a, m_b)) / 2


def monochromatic_max_s(energy):
    """Highest invariant mass squared of two freely colliding equal-energy photons."""
    return two_photon_s(energy, energy, -1)


def free_vacuum_bilinear_cut(m_a, m_b):
    """Lowest two-free-singlet cut for normal-ordered :s_a s_b: at tree level.

    NOT the spectral support of the full interacting SM+singlet theory.
    """
    return pair_threshold(m_a, m_b)


def f2_wavespeed(kinetic_normalization):
    """Vacuum plane-wave phase speed from pure L=-Z F^2/4, Z>0.

    Constant Z changes wavefunction/coupling normalization; it cannot on
    its own alter the source-free Maxwell dispersion omega^2=|k|^2.
    """
    if not math.isfinite(kinetic_normalization) or kinetic_normalization <= 0:
        raise ValueError('positive constant kinetic normalization required')
    return 1.0


if __name__ == '__main__':
    optical = 2 * EV_TO_GEV
    print('toy optical photon: E=', optical, 'GeV')
    print('head-on two-photon sqrt(s)=', math.sqrt(monochromatic_max_s(optical)), 'GeV')
    for label, a, b in (('11', M1, M1), ('12', M1, M2), ('22', M2, M2)):
        th = pair_threshold(a, b)
        print(label, 'threshold sqrt(s) [GeV]=', math.sqrt(th),
              '; equal head-on E per photon [GeV]=', min_equal_head_on_photon_energy(a,b))
    print('optical 2gamma invariant energy / 11 threshold=',
          math.sqrt(monochromatic_max_s(optical)) / (2*M1))