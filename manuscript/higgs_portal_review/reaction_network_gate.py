"""Research Note 38: two-species collision bookkeeping gate.

Pure bookkeeping for a hypothetical two-real-singlet odd sector.
No relic density, detector limit, or missing rate is inferred.
"""

from __future__ import annotations
import math

def _finite_nonnegative(*xs: float) -> None:
    if not all(math.isfinite(x) and x >= 0 for x in xs):
        raise ValueError("finite nonnegative inputs required")

def odd_number_delta(initial: tuple[int,int], final: tuple[int,int]) -> int:
    """Change in total odd-particle count for one forward reaction event."""
    if len(initial) != 2 or len(final) != 2:
        raise ValueError("two-species stoichiometry required")
    vals = (*initial, *final)
    if not all(isinstance(x, int) and x >= 0 for x in vals):
        raise ValueError("stoichiometric counts must be nonnegative integers")
    return sum(final)-sum(initial)

def forward_event_rates(n1: float, n2: float,
                        sv11: float, sv12: float, sv22: float) -> dict:
    """Unordered forward annihilation event densities, common-volume units."""
    _finite_nonnegative(n1,n2,sv11,sv12,sv22)
    return {
        "11": 0.5*n1*n1*sv11,
        "12": n1*n2*sv12,
        "22": 0.5*n2*n2*sv22,
    }

def forward_total_number_loss(n1: float, n2: float,
                              sv11: float, sv12: float, sv22: float) -> float:
    """d(n1+n2)/dt from forward annihilations only; negative or zero."""
    r=forward_event_rates(n1,n2,sv11,sv12,sv22)
    return -2.0*(r["11"]+r["12"]+r["22"])

def species_annihilation_terms(n1: float,n2: float,
                               n1eq: float,n2eq: float,
                               sv11: float,sv12: float,sv22: float) -> tuple[float,float]:
    """Detailed-balance form for 11,12,22 annihilation/inverse production.

    sv12 is the physical s1+s2 cross-section convention (no duplicate ordered
    initial-state copy). Each mixed annihilation removes one particle of each
    species, so it appears once in each species equation.
    """
    _finite_nonnegative(n1,n2,n1eq,n2eq,sv11,sv12,sv22)
    d11=n1*n1-n1eq*n1eq
    d12=n1*n2-n1eq*n2eq
    d22=n2*n2-n2eq*n2eq
    c1=-sv11*d11-sv12*d12
    c2=-sv22*d22-sv12*d12
    return c1,c2

def conversion_terms(net_2_to_1: float) -> tuple[float,float]:
    """Species collision terms for any net 2->1 conversion flux.

    Positive flux means net s2->s1; negative means net s1->s2.
    The total odd-particle count is conserved exactly.
    """
    if not math.isfinite(net_2_to_1):
        raise ValueError("finite conversion flux required")
    return net_2_to_1,-net_2_to_1

def sigma_eff(r2: float,sv11: float,sv12: float,sv22: float) -> float:
    """Chemical-equilibrium coannihilation reduction, conditional only."""
    _finite_nonnegative(sv11,sv12,sv22)
    if not math.isfinite(r2) or not 0 <= r2 <= 1:
        raise ValueError("r2 must be a fraction")
    r1=1-r2
    return r1*r1*sv11+2*r1*r2*sv12+r2*r2*sv22

def reduced_total_collision(N: float,Neq: float,r2: float,
                            sv11: float,sv12: float,sv22: float) -> float:
    """Conditional total collision term when n_i/r_i share equilibrium ratios."""
    _finite_nonnegative(N,Neq)
    return -sigma_eff(r2,sv11,sv12,sv22)*(N*N-Neq*Neq)

def full_total_collision(n1: float,n2: float,n1eq: float,n2eq: float,
                         sv11: float,sv12: float,sv22: float) -> float:
    c1,c2=species_annihilation_terms(n1,n2,n1eq,n2eq,sv11,sv12,sv22)
    return c1+c2

def equilibrium_weights(r2: float) -> tuple[float,float,float]:
    """Return 11, 12, 22 coefficients in sigma_eff."""
    if not math.isfinite(r2) or not 0 <= r2 <= 1:
        raise ValueError("r2 must be a fraction")
    r1=1-r2
    return r1*r1,2*r1*r2,r2*r2

if __name__ == "__main__":
    r2=0.05784749058  # Note-28 illustrative NR equilibrium fraction at x=20
    print("conditional weights 11,12,22 =",equilibrium_weights(r2))
    print("sum =",sum(equilibrium_weights(r2)))
    print("conversion odd-number delta 2->1+SM =",odd_number_delta((0,1),(1,0)))
    print("annihilation odd-number delta 1+2->SM =",odd_number_delta((1,1),(0,0)))
