COMMON ACTION AND PARAMETER CONTRACT
====================================

This continuation implements a common interface for the source archive's
restricted symmetric two-singlet portal. The machine-readable contract fixes
the factor 1/2 in V_portal, the exact simultaneous Z2, mass-basis transforms,
units, width factors, and the low-transfer point-probe matching. Inputs that
have not been derived or measured are JSON null, not invented values.

The general quartic tensor is recorded because simultaneous inversion permits
all degree-four terms and a change of basis rotates them. Its numerical values
remain unknown. The September archive's restricted quartic ansatz is a source
branch, not an automatically closed renormalized operator basis.

In particular, the pinned UV repository's separate-even scalar potential is
more restrictive than this simultaneous-Z2 interface. Its six-quartic scalar
basis cannot be identified with generic Phi^3 E, Phi E^3 and mixed Higgs portal
terms without a basis-compatible restriction or an extended projection. For
the two-field detector interface, contract the full connected spectral tensor
of O_ij=(s_i s_j)_ren with C_ij C_kl. The one-scalar rate is a special case.

Run: python common/portal_interface.py

The output checks production-width basis invariance, matching covariance,
degenerate trace normalization, thresholds, identical-particle factors, and
the algebraic collider-to-noise coefficient relation. These tests cannot prove
global vacuum stability, a complete operator inventory, a relic abundance,
detector invisibility, or a physical scalar population.

This interface does not merge GeV and ultralight benchmarks, a cosmological
bath and a laboratory bath, or the low-energy EFT and the assembled FRG flow.
Each identification requires its own matching calculation. The physical field
E_phys remains distinct from a normative or policy functional E_norm.

Provenance: uploaded archive SHA256
4b52a5fb57716168d354b5c3dcb4bbf2ca4c0fe6744733b6ca0d3b3eae48f921,
physical pages 7561-7563 and 7576-7582; thermal benchmark pinned at
Cbaird26/mqgt-scf-continued@48f9dcbd34e7cfb86504167a0483f732a5dd5e8e.
