"""Research Note 24: conditional Higgs pair rates and detector-agnostic envelope.

Restricted common-Z2 symmetric-vacuum two-singlet EFT; no hadronic inputs,
detector simulation, or experimental constraint calculations.
"""
import math

MH = 125.0  # GeV, illustrative
V = 246.0  # GeV, illustrative
SM_WIDTH = 0.0041  # GeV, illustrative; no other exotic decays
M1, M2 = 10.0, 11.5  # GeV, Note 22 toy point
K11, K12, K22 = 0.001, -0.001, 0.001


def pair_widths(m1=M1, m2=M2, k11=K11, k12=K12, k22=K22):
    """Return identical 11, nonidentical 12, identical 22 Higgs widths (GeV)."""
    if not all(math.isfinite(x) for x in (m1,m2,k11,k12,k22)) or not 0 < m1 <= m2:
        raise ValueError('Require finite ordered positive scalar masses and finite portals')
    def identical(m, k):
        if 2*m >= MH:
            return 0.0
        return V*V*k*k/(32*math.pi*MH)*math.sqrt(1-4*m*m/(MH*MH))
    mixed = 0.0
    if m1+m2 < MH:
        product=(1-(m1+m2)**2/MH**2)*(1-(m2-m1)**2/MH**2)
        mixed=V*V*k12*k12/(16*math.pi*MH)*math.sqrt(max(product,0.0))
    return identical(m1,k11),mixed,identical(m2,k22)


def branching_envelope(widths=None, sm_width=SM_WIDTH):
    """Branching interval only in SM + exactly three pair-channel model.

    Lower: stable s1s1 alone, upper: all three channels detector-invisible.
    No other Higgs widths or detector effects are assumed in denominator.
    """
    if widths is None:
        widths=pair_widths()
    if len(widths)!=3 or any(not math.isfinite(x) or x<0 for x in widths):
        raise ValueError('Three finite nonnegative widths required')
    if not math.isfinite(sm_width) or sm_width<=0:
        raise ValueError('SM reference width must be finite and positive')
    denominator=sm_width+sum(widths)
    return widths[0]/denominator, sum(widths)/denominator


def conditional_invisible_width(p12,p22,widths=None):
    """User-supplied abstract invisible-classification probabilities, not acceptances."""
    if not all(math.isfinite(x) and 0<=x<=1 for x in (p12,p22)):
        raise ValueError('Probabilities must lie in [0,1]')
    w11,w12,w22 = pair_widths() if widths is None else widths
    return w11+p12*w12+p22*w22


if __name__ == '__main__':
    w=pair_widths()
    low,high=branching_envelope(w)
    print('Gamma11, Gamma12, Gamma22 [GeV]:',*(f'{x:.12g}' for x in w))
    print('Gamma exotic total [GeV]:',f'{sum(w):.12g}')
    print('SM+exotic denominator [GeV]:',f'{SM_WIDTH+sum(w):.12g}')
    print('Conditional invisible fraction [s1s1-only, all-exotic]:',f'{low:.12g}',f'{high:.12g}')
    print('Conditional invisible fraction [%]:',f'{100*low:.9g}',f'{100*high:.9g}')
    print('Ratio upper/lower:',f'{high/low:.9g}')
