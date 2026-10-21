# Ultraviolet continuation: reproduced calculation, new projection, and closure conditions

**Date:** 2026-10-21  
**Pinned source:** [`Cbaird26/uv-reconstruction-frg`, commit `0a644a41eb947509280cbd648996d98bad54bdc5`](https://github.com/Cbaird26/uv-reconstruction-frg/tree/0a644a41eb947509280cbd648996d98bad54bdc5)

## Outcome

The source's formal 33-coordinate spectrum is reproducible: eight positive critical exponents, twelve zero linear exponents, and thirteen negative exponents under its convention `theta = -eig(d beta / d coupling)`. Reproduction also identifies a swapped mass/nonminimal label, incompatible background and normalization choices, an inconsistent scalar census, and missing scalar feedback. These prevent interpreting that count as the spectrum of one complete coupled theory.

This continuation performs three new bounded calculations:

1. It computes all scalar-potential Taylor coefficients through field degree six directly from the six-scalar Litim trace, without nested finite differences. This reveals explicit sextic-to-quartic terms omitted by the assembled source flow.
2. It reruns the DEP gravity block with six real scalars, matching the declared Higgs-plus-two-singlet field count, and quantifies the change from the four-scalar benchmark.
3. It follows the nominally marginal gauge subsystem and positive self-quartic rays to nonlinear order, showing why zero linear exponents are insufficient to establish exact marginality.

The program keeps the full-flow gate closed. None of these computations fills in unknown graviton/matter mixed projections or establishes a physical ultraviolet completion.

## 1. What was actually executed

Thirty source files were fetched through the GitHub connector at the pinned commit. Their local Git blob hashes match the fetched blob hashes; SHA-256 values and URLs are recorded in `provenance.json`. No `AGENTS.md` was present in the retrieved tree. The upstream source was not edited.

The upstream command `python -m unittest discover -s tests -v`, run from `upstream/`, completed **44 tests in 91.690 seconds, all passing**. The unmodified nested finite-difference stability calculation was also run directly. Passing those tests establishes the tested numerical identities; it does not reconcile the different projection conventions.

The new commands are:

```bash
python continue_uv.py
python continue_uv.py --reference-difference
```

The second command adds a slower direct comparison with the upstream numerical Jacobian. The first reuses a previously recorded comparison only when its source commit matches. Every run recomputes the new polynomial projections, the formal spectrum evaluated with those projections, the six-scalar benchmark, nonlinear trajectories, completion checks, and provenance. NumPy is the only third-party dependency.

Outputs:

| File | Content |
|---|---|
| `scalar_polynomial_projection.py` | New scalar trace projection through degree six |
| `continue_uv.py` | Reproduction, normalization audit, sensitivity, nonlinear calculation, and validation |
| `results.json` | Numerical results, scope labels, and explicit blockers |
| `nonlinear_flows.csv` | Thirty analytic/numerical trajectory comparisons |
| `projection_contract.json` | Required common conventions and missing-projection definitions |
| `provenance.json` | Pinned source hashes, new-code hashes, environment versions, primary references |
| `continuation_validation.log` | Short machine-readable execution summary |

## 2. The two cosmological numbers are different coordinates

The DEP branch explicitly applies

\[
g_N=\widetilde G=Gk^2,\qquad
\lambda_N=2\widetilde\Lambda=2\Lambda/k^2,
\]

and correspondingly

\[
\beta_{g_N}=\beta_{\widetilde G},\qquad
\beta_{\lambda_N}=2\beta_{\widetilde\Lambda}.
\]

This is implemented by dividing `lambdaN` by two before calling the DEP flow and multiplying its returned cosmological beta by two. See [`partial_flow_41.py`, lines 16–37](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/partial_flow_41.py#L16-L37) and the fixed-point construction in [`joint_fixed_point_stability.py`, lines 64–72](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/joint_fixed_point_stability.py#L64-L72).

Therefore the four-scalar values

\[
\widetilde\Lambda_*=-2.39875475845497,
\qquad \lambda_{N*}=-4.79750951690994
\]

denote the **same point in that branch**. This factor of two is not a new physical effect. A regular constant coordinate change produces a similar stability matrix and leaves its eigenvalues unchanged.

The notation must nevertheless be harmonized before comparing modules. The separate Litim wrapper calls its own cosmological coordinate `lambdaN` while associating it with Litim's `bar lambda/k^2`. The factor two in the Einstein–Hilbert action does not by itself require doubling the convention used to name the cosmological constant. The present audit preserves the DEP branch's implemented map; it does not certify that the same label has one action-level meaning throughout the repository. Litim writes the action and dimensionless variables explicitly in [equations (4) and (5)](https://arxiv.org/pdf/hep-th/0606044).

## 3. Reproduced spectrum and corrected sector labels

At the reported point, the maximum absolute finite beta residual using the polynomial scalar evaluation is **1.78 × 10^-15**. Eight entries remain unavailable. The 33 finite coordinates yield:

| Sector | Critical exponent(s) | Multiplicity | Interpretation in the supplied vector field |
|---|---:|---:|---|
| DEP gravity | 3.96087030, 1.64358588 | 2 | Mixed gravity eigenvectors |
| Scalar mass squared | 2.00000000 | 3 | Canonical; scalar quantum mass derivative vanishes at Gaussian quartics |
| Nonminimal `xi` | 2.85543525 | 3 | Imported frozen-background NP scalar block |
| Gauge, Yukawa, quartic coordinates | 0 at linear order | 12 | Nonlinear analysis required |
| Literal wavefunction coordinates `Z_i` | -0.07562458 | 3 | Normalization coordinates, with singular reported value `Z_i=0` |
| Scalar sextics | -2.00000000 | 10 | Canonical at this Gaussian matter point |

The upstream prose assigns **2.8554 to masses and 2.0000 to `xi`**. The source Jacobian has the opposite assignment. The error is in the labels, and the formal counts do not change. Compare the labels in [`joint_fixed_point_stability.py`, lines 26–38](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/joint_fixed_point_stability.py#L26-L38) with the actual mass and nonminimal functions in [`partial_flow_41.py`, lines 40–87](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/partial_flow_41.py#L40-L87).

The original nested finite differences produce a largest sextic-exponent deviation of **0.0027939677** from its exact canonical value; the outlying value is approximately -1.997206. The polynomial calculation removes this numerical artifact. It does not insert a new physical interaction.

The positive/zero/negative count describes the implemented mathematical array. A physical UV critical-surface dimension cannot be inferred from it because the flow is incomplete, field-normalization coordinates need special treatment, and the zero-exponent sector has not been resolved as a complete coupled center manifold.

## 4. New scalar projection through degree six

The scalar convention follows the source: four real Higgs components `h_i`, two real singlets `phi,e`, invariants `x=sum h_i^2`, `y=phi^2`, `z=e^2`, mass terms `m_i^2 phi_i^2/2`, quartic monomials divided by four, and sextic monomials divided by eight. See the [source sextic convention](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/sextic_lpa.py#L1-L34).

With normalized scalar kinetic terms, `k=1`, and no scalar anomalous dimension within this scalar-only LPA block, the trace is

\[
\partial_t U=\frac{1}{32\pi^2}\operatorname{tr}(I+U^{(2)})^{-1}.
\]

On a background `(h,0,0,0,phi,e)`, the Hessian splits into a three-by-three radial block and three identical Goldstone entries. Write the regularized radial Hessian as `D+E`, where `D=diag(1+m_i^2)` and every term in `E` has field degree at least two. Then

\[
(D+E)^{-1}
=\sum_{n=0}^{3}(-D^{-1}E)^nD^{-1}+O(\text{field}^8).
\]

This finite multivariate polynomial operation gives exact Taylor coefficients through degree six within the stated scalar trace. It retains nonzero mass thresholds and all included scalar quartics/sextics. It does not claim that the full finite-field potential ends at degree six, nor does it calculate any non-scalar trace.

One new result is the scalar feedback at zero mass and quartic couplings:

\[
\left.\frac{\partial\beta_{\lambda_H}}{\partial c_{H6}}\right|_0
=-\frac{24}{32\pi^2}=-0.07599088773,
\]

\[
\left.\frac{\partial\beta_{\lambda_\Phi}}{\partial c_{\Phi6}}\right|_0
=\left.\frac{\partial\beta_{\lambda_E}}{\partial c_{E6}}\right|_0
=-\frac{15}{32\pi^2}=-0.04749430483.
\]

The upstream assembled quartic flow has no sextic arguments, so these derivatives are zero there. This is expected when an MS-bar renormalizable quartic block is combined with a Wilsonian scalar potential trace without the required matching; it means that the assembled array is not the projection of the full declared scalar potential under one regulator. The new module makes the missing feedback calculable within the scalar block. It does not silently add it to the reproduction of the old flow.

Independent validation includes:

- An analytic one-real-scalar resolvent with nonzero mass, quartic and sextic: maximum error **2.71 × 10^-20**.
- Twelve nonzero six-quartic comparisons with the separately implemented tensor-contraction beta function: maximum error **4.34 × 10^-19**.
- A direct six-component Hessian trace at small nonzero field: difference **6.94 × 10^-18**, including the higher-order Taylor remainder.
- Rejection of a scalar threshold pole rather than continuing with an invalid regular chart.
- Reproduction of the formal count and verification of exact Gaussian mass/sextic diagonal entries.

## 5. Six-scalar DEP sensitivity

The source default uses `(n_s,n_d,n_v)=(4,22.5,12)`, while the scalar tensor contains four Higgs components plus two singlets. The default is visible in [`partial_flow_41.py`, line 105](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/partial_flow_41.py#L105) and [`gravity_matter_coupling.py`, line 276](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/gravity_matter_coupling.py#L276).

Keeping the same DEP approximation, table ghost convention, fermion/vector counts, and massless minimally coupled treatment, but setting `n_s=6`, gives:

| Quantity | Four scalars | Six scalars |
|---|---:|---:|
| `Lambda_tilde*` | -2.3987547585 | -2.6261976695 |
| Repository `lambdaN*=2 Lambda_tilde*` | -4.7975095169 | -5.2523953390 |
| `gN*=G_tilde*` | 1.7621271177 | 1.9858609514 |
| First gravity exponent | 3.9608703038 | 3.9595375318 |
| Second gravity exponent | 1.6435858822 | 1.6233745437 |
| Scalar anomalous dimension | -0.0756245819 | -0.0781801165 |

The magnitude of the cosmological coordinate increases **9.48%**, and the Newton coordinate increases **12.70%**. These are conditional block sensitivities, not changes in measured constants, uncertainty estimates for a complete theory, or a complete six-scalar fixed point.

At either nonzero Newton fixed point,

\[
\eta_N\equiv\beta_{g_N}/g_N-2=-2
\]

within numerical precision. The distinct DEP fluctuation quantity `eta_h` is **2.98354199** for four scalars, and **3.33861495** for six scalars. A document's `eta_h approximately 0.27` is the pure-gravity value carried into the wrong context. Background Newton scaling and fluctuation wavefunction scaling must not be identified without a derivation. The flow definitions are [DEP equations (21)–(22)](https://arxiv.org/pdf/1311.2898) and the [implemented beta functions](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/gravity_matter_coupling.py#L165-L189).

## 6. Nonlinear behavior of the zero-linear-exponent sector

Let `t=ln(k/k0)` increase toward the ultraviolet. The source matter baseline contains the autonomous one-loop gauge subsystem

\[
\dot g_i=\frac{b_i}{16\pi^2}g_i^3,
\qquad(b_Y,b_2,b_3)=(41/6,-19/6,-7),
\]

with ordinary hypercharge normalization. Its exact solution is

\[
\frac{1}{g_i^2(t)}=\frac{1}{g_i^2(0)}-\frac{b_i t}{8\pi^2}.
\]

Thus hypercharge is marginally UV-repulsive in this subsystem; the two non-Abelian gauge couplings are marginally UV-attractive. Gauge interactions also generate scalar terms, so a gauge-only axis is not an invariant trajectory of the full matter system. The conclusion refers to the autonomous gauge equations, not to an asserted gravity-coupled center manifold. See [the source gauge equations](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/sm_gauge_core.py#L1-L37).

On each pure self-quartic ray of the supplied matter baseline,

\[
\dot\lambda_H=\frac{24\lambda_H^2}{16\pi^2},\qquad
\dot\lambda_\Phi=\frac{18\lambda_\Phi^2}{16\pi^2},\qquad
\dot\lambda_E=\frac{18\lambda_E^2}{16\pi^2}.
\]

Positive quartics on these rays grow in the UV. The formal one-loop pole is not a quantitatively reliable prediction of the strong-coupling regime. Negative pure quartic rays approach zero from below but make the isolated quartic potential unbounded; they do not rescue the stable positive-ray result.

The illustrative initial values `g_i(0)=0.2`, `lambda_i(0)=0.01` are numerical probes, not empirical inputs. At `t=200`:

| Coupling | Analytic value |
|---|---:|
| `gY` | 0.3605866117 |
| `g2` | 0.1740216080 |
| `g3` | 0.1529774507 |
| `lambdaH` | 0.01436706370 |
| `lambdaPhi`, `lambdaE` | 0.01295290921 |

Independent RK4 integration agrees with the analytic curves to **3.50 × 10^-15** over the saved comparisons. A Yukawa-only probe produces both Yukawa and Higgs-quartic flow; a portal-only probe generates self-quartics. Those axes cannot be treated as independent exact marginal directions. All twelve zero-exponent coordinates are therefore retained as **unresolved by linearization**, with the stated subsystem behavior now explicitly calculated.

## 7. Common-convention audit: remaining blockers

### Background and regulator compatibility

The DEP gravity entries run with the current `gN,lambdaN`. The nonminimal entries call the NP function at hard-coded NP gravity coordinates `lambda0*=0.00862006735`, `xi0*=0.02375468048`, with `eta=2`; they do not use the running DEP gravity coordinates. Labels saying that the gauges are not mixed do not supply the missing matching derivation. This is directly visible in [`partial_flow_41.py`, lines 71–87](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/partial_flow_41.py#L71-L87) and [`scalar_tensor_nonminimal_np.py`, lines 186–205](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/scalar_tensor_nonminimal_np.py#L186-L205).

### NP scalar mass normalization

The NP paper uses `V=lambda2*phi^2+...` with canonical kinetic normalization, while the scalar Hessian in this repository uses curvature mass `m^2` corresponding to `m^2 phi^2/2`. The compatible identification is `lambda2=m^2/2`. The wired identification is `lambda2=m^2`. Its threshold `1+2 lambda2` therefore becomes `1+2m^2`, whereas the scalar Hessian threshold is `1+m^2`. For `m^2=0.2`, these are 1.4 and 1.2. See [NP equations (1), (25), (26)](https://arxiv.org/pdf/0911.0386), [the upstream threshold](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/scalar_tensor_nonminimal_np.py#L85-L103), and [the LPA mass matrix](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/scalar_frg_lpa.py#L16-L41).

Correcting this factor alone would not reconcile the differing backgrounds, the Higgs multiplicity, or the nonminimal action-sign convention. At the quoted zero-matter point it does not change the reported diagonal mass/xi exponent assignment; it changes off-diagonal dependence and trajectories away from that point.

### Separate Litim Newton normalization

This issue is outside the DEP calculation but blocks cross-branch identification. The separate `gravity_frg.py` wrapper implements `g_equation=c4*gN`, where `c4=24*pi`, and calls `gN` the physical dimensionless Newton coupling `G*k^2`. Litim's [equations (5), (6), and (11)](https://arxiv.org/pdf/hep-th/0606044) instead require `G*k^2=c4*g_equation`: the equation-level fixed point `1/64` restores to `3*pi/8`, not `1/(1536*pi)`. The mismatch is a factor `(24*pi)^2` in the claimed physical coordinate. The [wrapper explicitly contains both numbers](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/gravity_frg.py#L12-L25), which makes this a normalization issue rather than a failure to solve its own rescaled equations.

The DEP reproduction does not call this wrapper, so the DEP numbers above are unaffected. A consistent coordinate rescaling also preserves stability eigenvalues; a test that checks only those eigenvalues cannot detect this physical-normalization mistake.

### Kinetic normalization and essential couplings

The source sets `Z_h=Z_phi=Z_E=0` because `beta_Z=-eta_scalar*Z` vanishes there when `eta_scalar` is nonzero. Literal zero kinetic normalizations do not provide a regular canonically normalized propagating scalar sector. A fixed point of essential dimensionless couplings can coexist with running wavefunction factors; it need not be a fixed point of raw `Z_i` values.

For `eta_i=-d ln Z_i/dt`, normalized quantities contain factors such as

\[
\widetilde m_i^2=m_i^2/(Z_i k^2),\quad
\widetilde\lambda_i=\lambda_i/Z_i^2,\quad
\widetilde c_{abc}=k^2c_{abc}/(Z_H^aZ_\Phi^bZ_E^c).
\]

The sextic normalization then contributes `(2+a eta_H+b eta_Phi+c eta_E) c_tilde`, with `a+b+c=3`, before loop terms. An essential-coupling formulation and its consistently transformed projections are required. The new scalar calculation uses a regular `Z=1` scalar LPA chart for its bounded purpose; it does not cure the source's mixed treatment of running `Z` and unnormalized scalar betas.

### Missing operators and a complete beta-vector gate

At the quoted point, the unavailable entries are `a_R2`, `a_C2`, `c_HBox`, `c_PhiBox`, `c_EBox`, `c_HF2`, `c_PhiF2`, and `c_EF2`. The inherited `requires_complete_flow` correctly raises an error.

The two curvature coefficients use inverse coordinates singular at this point. Moreover the standalone CPR expression has `beta_aC2=133/(320*pi^2)=0.04211161695`, so it has no finite zero in that inverse coordinate chart. This is not a proof against a different complete gravity truncation. See [the implemented curvature-coordinate flows](https://github.com/Cbaird26/uv-reconstruction-frg/blob/0a644a41eb947509280cbd648996d98bad54bdc5/r2_gravity_cpr.py#L131-L141).

The dimension-six derivative terms need a chosen integration-by-parts/equations-of-motion basis and momentum projectors. The `F2` label must specify U(1), SU(2), SU(3), or a fixed combination; a general scalar-bilinear gauge-strength sector has a coefficient for each scalar invariant and each gauge factor. Canonical `+2 c` terms are known but do not replace these projections. `projection_contract.json` records the necessary definitions without inventing loop coefficients.

## 8. Concrete completion criteria

A next full coupled claim is reviewable only when it provides:

1. One action and field census with fixed mass, quartic, nonminimal, Newton and cosmological conventions.
2. One regulator/gauge/ghost prescription, or an explicit derived matching map between different schemes and backgrounds.
3. A regular field-normalization chart and removal or consistent treatment of redundant normalization directions.
4. Every retained beta projection, including scalar, gravity, gauge, Yukawa, nonminimal and derivative mixing to the stated truncation order; unresolved entries must remain unavailable.
5. A finite simultaneous residual in the full chosen basis, with Newton scaling checked using its own background anomalous dimension.
6. Nonlinear resolution of the zero-exponent sector, numerical derivative convergence, regulator sensitivity, and a controlled truncation enlargement.
7. A trajectory or matching calculation connecting the UV construction to the independently specified low-energy branch before combining their predictions.

The present package completes a reproducible scalar projection and several targeted diagnostics. The missing common Hessian/projections remain explicit research work; a sum of independently successful block benchmarks is not sufficient to claim a complete theory.
