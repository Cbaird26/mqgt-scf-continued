# Read-only review of the common portal interface

Reviewed `../common/portal_interface.py` and `../common/action_parameter_contract.json` as present during this continuation. No changes were made to those files.

## Algebra that is consistent

For `V_portal=(phi^T K phi) HdaggerH/2` and `HdaggerH=(v+h)^2/2`, the common code correctly obtains:

- `Mphysical^2=M0^2+v^2 K/2`.
- `L_hss=-v h (K11 s1^2+2 K12 s1 s2+K22 s2^2)/2`.
- Vertex magnitude `v Kij` for both diagonal and off-diagonal channels.
- Width denominators `32*pi*mh` for identical daughters and `16*pi*mh` for distinct daughters, with the correct two-body phase-space factor.
- In the equal-mass limit, total width proportional to `trace(K^2)`, including twice the off-diagonal square.
- Orthogonal-basis covariance of the mass and portal matrices, with eigenvector signs physically irrelevant to the production widths.

Integrating out the Higgs at small momentum with its point-fermion coupling `-f_a m_a h fbar f/v` yields

`L_eff=(s^T C s) fbar f`, with `C=f_a m_a K/(2 mh^2)`.

This has coefficient dimension GeV^-1 and the positive Lagrangian sign used by the code. The heavy-probe Hamiltonian has the opposite sign. The scalar equation then contains `2 n_a C s`, a multiplicative mass shift; it does not introduce an additive source from zero scalar field.

The quoted approximately 18.974357 keV is a production width at a specified parameter point. The conditional fraction near 0.00460657 assumes that every daughter is invisible and that the other Higgs width is 4.1 MeV. A simultaneous Z2 stabilizes the lightest odd state; it does not by itself make the heavier odd state invisible, because a heavier-to-lighter transition with Standard Model products can be allowed. The contract correctly avoids treating the conditional fraction as an observed invisible branching ratio.

## Action and basis scope

The common simultaneous Z2 allows five independent singlet quartic tensor components: `Phi^4`, `Phi^3 E`, `Phi^2 E^2`, `Phi E^3`, and `E^4`. It also permits `Phi E HdaggerH`. A general orthogonal basis change preserves that full tensor space.

The UV source's declared scalar quartic basis is more restrictive: it contains even powers of each singlet separately and only diagonal Higgs portals. A generic rotation, or the common benchmark's nonzero `K12`, need not remain within that restricted basis. Consequently there is no automatic direct map from the common action to the UV source's six-quartic system. One must either extend that system to the needed tensor components or exhibit a common basis in which the required restrictions and mass matrix can both be imposed. This is a substantive matching condition, not a field-renaming detail.

The common contract appropriately leaves the singlet quartics and global vacuum stability unspecified. Positive eigenvalues of a local quadratic Hessian do not determine the global vacuum when those quartics are unknown.

## Noise notation that should remain explicit

The displayed scalar expression `gamma(d)=c_a^2[S_phi2(0,0)-S_phi2(0,d)]` is a one-operator special case. For the general matrix interface, define connected renormalized composite operators `O_ij=(s_i s_j)_ren` and their spectral tensor, and use

`gamma(d)=sum_ij,kl C_ij C_kl [S_ij,kl(0,0)-Re S_ij,kl(0,d)]`

under the stated homogeneous stationary, heavy point-probe, weak-coupling, Markov assumptions and a consistent full-index summation convention. If only independent symmetric components are summed, the off-diagonal weights must be adjusted. A two-sided Fourier convention must be specified to fix normalization factors. The connected correlation subtracts the mean contribution, which belongs to a deterministic energy shift.

For canonically normalized four-dimensional scalars, the time-integrated `phi^2` correlation has dimension GeV^3; multiplication by `C^2` gives GeV, convertible to s^-1 by division by hbar. The dimensional statement in the contract is correct.

## Minor input-validation issue

`pair_widths` checks the portal matrix for finiteness but does not explicitly reject nonfinite masses or electroweak inputs. A NaN mass can propagate as a NaN result. This does not affect the finite benchmark reviewed here; an external-use interface should reject nonfinite physical inputs before evaluating a width. The analogous finite-input check is useful for point-probe matching parameters.

## Review conclusion

The tree-level production and matching algebra is consistent at the declared benchmark. The basis/symmetry limitation and matrix-valued noise convention are the two conceptual details needed before using this interface as a cross-workstream matching rule. Its tests validate algebraic consistency, not relic abundance, a detector prediction, vacuum stability, or UV completion.
