"""Note 28: deliberately partial, nonrelativistic Higgs-current leptonic annihilation and equilibrium weights.

Natural units for sigma_v_gev2. This is NOT a Boltzmann solver or relic-density prediction.
"""
import math

M1, M2, MH, GH, K11 = 10.0, 11.5, 125.0, 0.0041, 0.001
HBAR_GEV_S = 6.582119569e-25
CM2_PER_GEV2 = 0.389379338e-27
C_CM_S = 29979245800.0
MASS = {'electron': 0.00051099895, 'muon': 0.1056583755, 'tau': 1.77686}
LEPTON_FLOOR_S2 = 3.060267688e-22  # GeV, from Note 22; no QCD


def sigma_v_ff_threshold(mchi=M1, mf=MASS['tau'], k=K11, color=1):
    """Zero-relative-speed s1 s1 -> f fbar through h; returned GeV^-2.

    Tree-level stable real scalar: L = -v*K11*h*s1^2/2 -mf/v*h*fbar*f.
    No initial identical-particle factor belongs in sigma*v per collision.
    """
    if not all(map(math.isfinite, (mchi, mf, k, color))) or min(mchi,mf,color) <= 0:
        raise ValueError('finite positive masses/multiplicity and finite coupling required')
    if mf >= mchi or k == 0:
        return 0.0
    s = 4*mchi*mchi
    denom = (MH*MH-s)**2 + (MH*GH)**2
    beta = math.sqrt(1-mf*mf/(mchi*mchi))
    return color*k*k*mf*mf*beta**3/(4*math.pi*denom)


def equilibrium_heavy_fraction(x, m1=M1, m2=M2, g1=1.0, g2=1.0):
    """Maxwell-Boltzmann nonrelativistic EQUILIBRIUM fraction, not actual n2/n_tot."""
    if not all(map(math.isfinite,(x,m1,m2,g1,g2))) or x <= 0 or m1 <= 0 or m2 < m1 or min(g1,g2)<=0:
        raise ValueError('invalid equilibrium inputs')
    rel = m2/m1-1
    ratio = (g2/g1)*(m2/m1)**1.5*math.exp(-x*rel)
    return ratio/(1+ratio)


def coannihilation_coefficients(r2):
    """Only valid when the s1/s2 species share chemical equilibrium."""
    if not math.isfinite(r2) or not 0 <= r2 <= 1:
        raise ValueError('invalid equilibrium fraction')
    r1 = 1-r2
    return r1*r1, 2*r1*r2, r2*r2


def heavier_lifetime_ceiling_seconds(floor=LEPTON_FLOOR_S2):
    if not math.isfinite(floor) or floor <= 0:
        raise ValueError('width floor must be finite and positive')
    return HBAR_GEV_S/floor

if __name__ == '__main__':
    leptons = {name:sigma_v_ff_threshold(mf=mass) for name,mass in MASS.items()}
    total = sum(leptons.values())
    print('s1s1 -> leptons at v_rel -> 0, GeV^-2:',leptons)
    print('leptonic-only sum, cm^3/s:',f'{total*CM2_PER_GEV2*C_CM_S:.12g}')
    print('reference 3e-26 / lepton-only sum:',f'{3e-26/(total*CM2_PER_GEV2*C_CM_S):.12g}')
    for x in (20,25):
        r2=equilibrium_heavy_fraction(x)
        print(f'x={x}, equilibrium r2={r2:.12g}, weights 11/12/22={coannihilation_coefficients(r2)}')
    print('s2 lifetime upper bound s:',f'{heavier_lifetime_ceiling_seconds():.12g}')
