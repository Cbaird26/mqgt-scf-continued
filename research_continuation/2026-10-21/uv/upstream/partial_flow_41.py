"""Assemble available contributions into a 41-vector without faking coverage."""
from __future__ import annotations

import numpy as np

from model import INDEX, NAMES
from perturbative_matter_baseline import beta as matter_beta
from gravity_matter_coupling import (beta as dep_beta, eta_system, D as DEP_D,
                                     DEP_TABLE_GHOST_FACTOR)
from scalar_frg_lpa import project_scalar_potential_flow
from r2_gravity_cpr import a_r2_beta, a_c2_beta
from scalar_tensor_nonminimal_np import beta_xi_matter
from sextic_lpa import project_sextic_flow, SEXTIC_NAMES


def gravity_beta_dep(couplings, n_s=0.0, n_d=0.0, n_v=0.0, improved=False,
                     ghost_factor=DEP_TABLE_GHOST_FACTOR):
    """DEP 1311.2898 coupled gravity+matter block in scaffold coordinates.

    Coordinate mapping (both normalizations agree at d = 4):
      - DEP uses (Lambda_tilde, G_tilde) = (Lambda k^-2, G k^(d-2)); the
        scaffold gN = G k^2 equals G_tilde at d = 4, so beta_gN = beta_G_tilde.
      - The scaffold lambdaN = lambda_bar k^-2 (Litim hep-th/0606044, EH
        action written with 2 Lambda) satisfies lambdaN = 2 Lambda_tilde,
        hence beta_lambdaN = 2 beta_Lambda_tilde.

    Convention caveat (no-fabrication rule): the DEP fixed points use the
    type-II cutoff with alpha = rho = 1 and the table ghost factor
    2*2^{[d/2]}; they are regulator- and gauge-dependent and differ from the
    Litim type-A benchmark of gravity_frg.py.  The two convention labels are
    kept distinct and are never mixed in a single solve.
    """
    lam_tilde = couplings[INDEX["lambdaN"]] / 2.0
    g_tilde = couplings[INDEX["gN"]]
    beta_lam_tilde, beta_g_tilde = dep_beta(lam_tilde, g_tilde, n_s, n_d, n_v,
                                            DEP_D, improved, ghost_factor)
    return 2.0 * beta_lam_tilde, beta_g_tilde


def scalar_mass_beta(couplings, improved=False, ghost_factor=DEP_TABLE_GHOST_FACTOR):
    """Scalar LPA quantum trace contributions to (mH2, mPhi2, mE2).

    These are the projected Wetterich-trace contributions of scalar_frg_lpa
    evaluated at the running (masses, quartics); canonical scaling and the
    gauge/top one-loop mass terms are not yet covered.
    """
    masses = (couplings[INDEX["mH2"]], couplings[INDEX["mPhi2"]], couplings[INDEX["mE2"]])
    quartics = (couplings[INDEX["lambdaH"]], couplings[INDEX["lambdaPhi"]], couplings[INDEX["lambdaE"]],
                couplings[INDEX["kappaHPhi"]], couplings[INDEX["kappaHE"]], couplings[INDEX["kappaPhiE"]])
    flow = project_scalar_potential_flow(masses, quartics)
    return flow["mH2"], flow["mPhi2"], flow["mE2"]


def wavefunction_beta(couplings, n_s=0.0, n_d=0.0, n_v=0.0, improved=False,
                      ghost_factor=DEP_TABLE_GHOST_FACTOR):
    """Wavefunction renormalization flow beta_{Z_i} = -eta_i * Z_i.

    The scalar anomalous dimension eta_S is taken from the DEP 1311.2898
    matter block evaluated at the current (Lambda_tilde, G_tilde); at the
    DEP SM fixed point eta_S = -0.076, so the Z_i fixed point is Z_i = 0.
    """
    lam_tilde = couplings[INDEX["lambdaN"]] / 2.0
    g_tilde = couplings[INDEX["gN"]]
    eta_h, eta_c, eta_s, eta_d, eta_v = eta_system(lam_tilde, g_tilde, n_s, n_d, n_v,
                                                   DEP_D, improved, ghost_factor)
    return (-eta_s * couplings[INDEX["Z_h"]],
            -eta_s * couplings[INDEX["Z_phi"]],
            -eta_s * couplings[INDEX["Z_E"]])


def nonminimal_beta(couplings):
    """Nonminimal-coupling flows (xiH, xiPhi, xiE).

    Narain-Percacci 0911.0386 block (convention label NP-DE-DONDER-TYPEA):
    the xi_2 flow of the five-coupling scalar-tensor system is evaluated on
    the GMFP gravity background of that paper with eta = 2, using the
    per-species mapping lambda_2 = m_i^2, xi_2 = xi_i, lambda_4 =
    lambda_i/4 (radial-field coefficient of phi^4).  At Gaussian matter
    (lambda_2 = xi_2 = lambda_4 = 0) the flow vanishes, so xi* = 0 is an
    exact fixed point of this block.
    """
    return (beta_xi_matter(couplings[INDEX["mH2"]], couplings[INDEX["xiH"]],
                           couplings[INDEX["lambdaH"]] / 4.0),
            beta_xi_matter(couplings[INDEX["mPhi2"]], couplings[INDEX["xiPhi"]],
                           couplings[INDEX["lambdaPhi"]] / 4.0),
            beta_xi_matter(couplings[INDEX["mE2"]], couplings[INDEX["xiE"]],
                           couplings[INDEX["lambdaE"]] / 4.0))


def sextic_beta(couplings):
    """Sixth-order scalar LPA trace projections (c_H6 ... c_H2Phi2E2).

    Same Wetterich trace as the mass-squared block, evaluated with the full
    sixth-order potential; scalar loops only (canonical scaling and
    non-scalar traces remain separate inputs).
    """
    masses = (couplings[INDEX["mH2"]], couplings[INDEX["mPhi2"]], couplings[INDEX["mE2"]])
    quartics = (couplings[INDEX["lambdaH"]], couplings[INDEX["lambdaPhi"]], couplings[INDEX["lambdaE"]],
                couplings[INDEX["kappaHPhi"]], couplings[INDEX["kappaHE"]], couplings[INDEX["kappaPhiE"]])
    sextics = tuple(couplings[INDEX[name]] for name in SEXTIC_NAMES)
    flow = project_sextic_flow(masses, quartics, sextics)
    return tuple(flow[name] for name in SEXTIC_NAMES)


def beta_partial(couplings, gravity="dep", gravity_counts=(4.0, 22.5, 12.0)):
    if len(couplings) != 41:
        raise ValueError("expected 41 couplings")
    if gravity not in ("dep",):
        raise ValueError(f"unknown gravity block {gravity!r}")
    result = np.full(41, np.nan)
    # Map the coupled 10-coordinate perturbative baseline.
    source = matter_beta((
        couplings[INDEX["g1"]], couplings[INDEX["g2"]], couplings[INDEX["g3"]], couplings[INDEX["yt"]],
        couplings[INDEX["yb"]], couplings[INDEX["ytau"]], couplings[INDEX["lambdaH"]], couplings[INDEX["lambdaPhi"]], couplings[INDEX["lambdaE"]],
        couplings[INDEX["kappaHPhi"]], couplings[INDEX["kappaHE"]], couplings[INDEX["kappaPhiE"]],
    ))
    for name, value in zip(("g1", "g2", "g3", "yt", "yb", "ytau", "lambdaH", "lambdaPhi", "lambdaE", "kappaHPhi", "kappaHE", "kappaPhiE"), source):
        result[INDEX[name]] = value
    # Gravity block (DEP 1311.2898) fills entries 0 (gN) and 1 (lambdaN).
    beta_lam, beta_g = gravity_beta_dep(couplings, *gravity_counts)
    result[INDEX["gN"]] = beta_g
    result[INDEX["lambdaN"]] = beta_lam
    # Scalar LPA mass-squared trace contributions (mH2, mPhi2, mE2).
    m_h2, m_phi2, m_e2 = scalar_mass_beta(couplings)
    result[INDEX["mH2"]] = m_h2
    result[INDEX["mPhi2"]] = m_phi2
    result[INDEX["mE2"]] = m_e2
    # Wavefunction renormalizations (Z_h, Z_phi, Z_E) from the DEP etas.
    z_h, z_phi, z_e = wavefunction_beta(couplings, *gravity_counts)
    result[INDEX["Z_h"]] = z_h
    result[INDEX["Z_phi"]] = z_phi
    result[INDEX["Z_E"]] = z_e
    # R^2 sector (Codello-Percacci-Rahmede 0805.2909, one-loop): a_R2 = 1/xi,
    # a_C2 = 1/(2 lambda4); defined only for a_C2 != 0, NaN at the Gaussian
    # point where the 1/(2 lambda4) parametrization is singular.
    result[INDEX["a_R2"]] = a_r2_beta(couplings[INDEX["a_R2"]],
                                      couplings[INDEX["a_C2"]])
    result[INDEX["a_C2"]] = a_c2_beta() if couplings[INDEX["a_C2"]] != 0.0 else np.nan
    # Nonminimal couplings (Narain-Percacci 0911.0386 GMFP background).
    for name, value in zip(("xiH", "xiPhi", "xiE"), nonminimal_beta(couplings)):
        result[INDEX[name]] = value
    # Sixth-order scalar LPA trace projections.
    for name, value in zip(SEXTIC_NAMES, sextic_beta(couplings)):
        result[INDEX[name]] = value
    return result


def coverage(couplings, gravity="dep", gravity_counts=(4.0, 22.5, 12.0)):
    values = beta_partial(couplings, gravity, gravity_counts)
    return {"derived": tuple(NAMES[i] for i, value in enumerate(values) if np.isfinite(value)),
            "missing": tuple(NAMES[i] for i, value in enumerate(values) if not np.isfinite(value))}


def requires_complete_flow(couplings, gravity="dep", gravity_counts=(4.0, 22.5, 12.0)):
    values = beta_partial(couplings, gravity, gravity_counts)
    if not np.all(np.isfinite(values)):
        missing = [NAMES[i] for i, value in enumerate(values) if not np.isfinite(value)]
        raise RuntimeError(f"Cannot solve a 41-dimensional fixed point; missing beta functions: {', '.join(missing)}")
    return values
