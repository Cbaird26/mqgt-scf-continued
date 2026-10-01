"""Research Note 25: exact common-Z2 selection and symbolic low-energy Higgs matching.

Pure algebra, NOT a computation of SM h->gamma gamma loops, H2 noise, or rates.
"""
from fractions import Fraction


def is_z2_even(n_s1: int, n_s2: int) -> bool:
    """The common parity changes the sign of both odd real singlets."""
    if not isinstance(n_s1, int) or not isinstance(n_s2, int) or min(n_s1, n_s2) < 0:
        raise ValueError('singlet monomial powers must be nonnegative integers')
    return (n_s1 + n_s2) % 2 == 0


def photon_contact_coefficients(k11, k12, k22, c_gamma, mh):
    """Coefficients of F^2*(s1^2, s1*s2, s2^2) after tree h exchange.

    Convention: L=-mh^2*h^2/2 -v*h*(K11*s1^2/2 + K12*s1*s2
    + K22*s2^2/2) + c_gamma*h*F^2/(4*v).
    This is a leading local term for four-momentum well below mh; Cgamma
    is UNCOMPUTED and may be momentum dependent in the UV theory.
    """
    if mh <= 0:
        raise ValueError('Higgs mass must be positive')
    return (-c_gamma*k11/(8*mh*mh),
            -c_gamma*k12/(4*mh*mh),
            -c_gamma*k22/(8*mh*mh))


def integrate_h_tree(h_source, mh):
    """For L_h=-mh^2*h^2/2+h*J, stationary h=J/mh^2 gives J^2/2mh^2."""
    if mh <= 0:
        raise ValueError('Higgs mass must be positive')
    return h_source*h_source/(2*mh*mh)


def contact_cross_term(s1, s2, f2, k11, k12, k22, c_gamma, v, mh):
    """Extract all terms linear in F^2 from integrating out h, by subtraction."""
    if v == 0:
        raise ValueError('v must be nonzero')
    singlet_source = -v*(k11*s1*s1/2 + k12*s1*s2 + k22*s2*s2/2)
    photon_source = c_gamma*f2/(4*v)
    return (integrate_h_tree(singlet_source+photon_source,mh)
            - integrate_h_tree(singlet_source,mh)
            - integrate_h_tree(photon_source,mh))


def contact_cross_term_from_coefficients(s1,s2,f2,k11,k12,k22,c_gamma,mh):
    c11,c12,c22 = photon_contact_coefficients(k11,k12,k22,c_gamma,mh)
    return f2*(c11*s1*s1+c12*s1*s2+c22*s2*s2)
