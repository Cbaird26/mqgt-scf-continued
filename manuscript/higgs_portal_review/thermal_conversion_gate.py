"""Note 29: conditional radiation-era expansion versus leptonic conversion.

No hadronic width, bath scattering, real g*(T), thermal history, or relic density.
All energy units GeV; H and widths in GeV. The inverse-decay expression
assumes equilibrium light/heavy MB distributions and a thermal lepton bath.
"""
import math

M1 = 10.0
M2 = 11.5
GAMMA_LEP = 3.060267688e-22
M_PLANCK = 1.2209e19   # non-reduced Planck mass [GeV]
HBAR = 6.582119569e-25  # GeV s


def hubble_radiation(T, gstar=60.0):
    if not (math.isfinite(T) and math.isfinite(gstar) and T > 0 and gstar > 0):
        raise ValueError('T and gstar must be finite and positive')
    return math.sqrt(8 * math.pi**3/90 * gstar) * T*T/M_PLANCK


def equilibrium_heavy_to_light(T, m1=M1, m2=M2):
    if not all(map(math.isfinite, (T,m1,m2))) or min(T,m1,m2)<=0 or m2<=m1:
        raise ValueError('positive T, positive ordered masses required')
    return (m2/m1)**1.5 * math.exp(-(m2-m1)/T)  # NR MB approximation


def rates(T, gstar=60.0, gamma_lep=GAMMA_LEP):
    if not math.isfinite(gamma_lep) or gamma_lep < 0:
        raise ValueError('gamma_lep must be finite nonnegative')
    H = hubble_radiation(T,gstar)
    q = equilibrium_heavy_to_light(T)
    # MB thermal mean time dilation K1(m2/T)/K2(m2/T) <= 1.
    # Reaction density gamma_D^lep = n_2^eq Gamma_lep <m2/E2>.
    # Corresponding inverse events per equilibrium s1:
    # gamma_D^lep/n1^eq = q Gamma_lep <m2/E2> <= q Gamma_lep.
    return dict(T=T, gstar=gstar, H_gev=H, H_per_s=H/HBAR,
                H_time_s=HBAR/H, gamma_lep_H_upper=gamma_lep/H,
                q_nr=q, heavy_fraction=q/(1+q),
                inverse_per_light_H_upper=q*gamma_lep/H,
                gamma_lep_s=gamma_lep/HBAR)


def _scaled_besselk_nu(nu, z, intervals=2400):
    """e^z K_nu(z), by its positive integral; z in [10,100].

    Composite Simpson on t in [0,12] for integral
    exp(-z(cosh(t)-1))*cosh(nu*t) dt. This is a numerical
    approximation, not a mathematically certified error enclosure.
    """
    if nu not in (1, 2) or not math.isfinite(z) or not 10 <= z <= 100:
        raise ValueError('order 1/2 and 10<=z<=100 required')
    if not isinstance(intervals,int) or intervals <= 0 or intervals%2:
        raise ValueError('positive even interval count required')
    upper=12.0
    step=upper/intervals
    def value(t):
        return math.exp(-z * (math.cosh(t)-1))*math.cosh(nu*t)
    accum=value(0)+value(upper)
    for i in range(1, intervals):
        accum += (4 if i%2 else 2)*value(step*i)
    return step*accum/3


def exact_mb_metrics(T, gstar=60.0, gamma_lep=GAMMA_LEP):
    """Numerical Maxwell-Boltzmann correction at 0.115<=T<=1 GeV.

    Uses no bath-medium corrections; reports the *leptonic-only*
    decay and inverse-decay equilibrium rate ratios, not a complete
    chemical-equilibration rate.
    """
    nominal=rates(T,gstar,gamma_lep)
    z1,z2=M1/T,M2/T
    k2_1=_scaled_besselk_nu(2,z1)
    k2_2=_scaled_besselk_nu(2,z2)
    d=_scaled_besselk_nu(1,z2)/k2_2
    q=(M2/M1)**2*math.exp(-(M2-M1)/T)*k2_2/k2_1
    return dict(nominal, mb_q=q, mb_heavy_fraction=q/(1+q),
                time_dilation=d, mb_leptonic_decay_H=d*nominal['gamma_lep_H_upper'],
                mb_inverse_per_light_H=q*d*nominal['gamma_lep_H_upper'])


if __name__ == '__main__':
    for t in (.5,.4):
        r=exact_mb_metrics(t)
        print(f"T={t:g} GeV, assumed g*=60, H={r['H_gev']:.12g} GeV, H^-1={r['H_time_s']:.9g} s")
        print(f"  exact MB n2/n1={r['mb_q']:.9g}, heavy fraction={r['mb_heavy_fraction']:.9g}, Gamma_lep thermal/H={r['mb_leptonic_decay_H']:.9g}, inverse/light/H={r['mb_inverse_per_light_H']:.9g}")
