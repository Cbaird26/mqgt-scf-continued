# Research Note 52 — Coupled density, energy and drift relaxation, with a thermal bath-response contract

**Research continuation: 12 October 2026. Scientific-development draft; not peer reviewed.** Prepared for Christopher Michael Baird with ChatGPT (ZoraASI) assistance in derivation, implementation, numerical verification and drafting. Execution/publication timestamps are recorded separately. This is a bounded calculation within the hypothetical two-real-singlet Higgs portal, not empirical evidence for new particles or completion of a Theory of Everything.

## 1. Advance against TOE-COMPLETE-001

The current goal is GitHub issue #3. The live draft PR #1 was read at `9642125db7dfb47328083f33ab129cd202b0416f`. The supplied Note-51 archive was extracted without source changes; all 70 manifest entries passed byte-size/SHA-256 checks. Its main kernel's locally computed Git blob `6ba9dcd73f7ef7325e939cebbcf0e6d482a341b3` matches the file identity returned from that live commit. This verifies the immediate calculation baseline, not the entire corpus or all duplicate test lineages.

G04 requires momentum relaxation rather than an event-count argument. This note computes the first **coupled density/energy and bulk-drift collision moments** for charged-lepton elastic and inelastic scattering. It uses exact relativistic recoil in the declared vacuum-tree/ideal-bath model. It does not replace the collision term by a small-momentum-transfer Fokker–Planck expansion.

The main result is an important separation: at assumed T=0.5 GeV, the restricted count-only scattering mode is 1.76277 H, whereas the slowest projected density/energy mode is 0.604445 H and the slowest projected drift mode is 0.418096 H. Therefore the count-only result does not establish rapid relaxation of momentum distributions. These are finite-dimensional projected diagnostics around a stationary state, not exact eigenvalues of the full momentum-space operator and not a cosmological freeze-out calculation.

G03 is also made explicit as a thermal scalar-response problem in Section 8. No numerical QCD-bath rate is substituted from a timelike annihilation table. The complete G03 and G04 milestones remain open.

## 2. Model, domain and perturbations

Retain the inherited unfitted inputs:

```
m1=10, m2=11.5, mh=125 [GeV];
K11=K22=+0.001, K12=-0.001;
me=0.00051099895, mmu=0.1056583755, mtau=1.77686 [GeV];
g_lepton=4 per flavor (two spins, both charges);
H(T)=sqrt(8*pi^3*60/90) T^2/(1.2209e19 GeV).
```

The diagonal portal entries are those of the earlier 11/12/22 benchmark. New interactions are not fitted to a desired equilibrium condition. The declared temperature interval remains 1/3<=T<=0.5 GeV. The assumed g*=60 is not a new QCD equation of state. The bath is held fixed; scalar number-changing reactions, scalar self-interactions and decay momentum redistribution are excluded from this scattering-only operator. In particular, the old decay width is **not** inserted as a fictitious energy-relaxation matrix element.

Bath leptons initially have Maxwell–Boltzmann occupations with zero chemical potential. Singlets are dilute and have vacuum dispersion E_i=sqrt(p^2+m_i^2). The stationary reference is f_i^0=zeta exp(-E_i/T), with an arbitrary common fugacity zeta. Its absolute normalization cancels from the normalized collision matrix. Linearize by writing f_i=f_i^0(1+chi_i); retain trial functions

```
chi_i(p)=a_i + b_i (E_i-Ebar_i)/T + c_i p_z/T.
```

At fixed species number, b_i corresponds at first order to delta T_i/T. The c_i terms test one component of bulk drift; isotropy makes the other two components equivalent. Drift need not be present in a homogeneous cosmological preparation: it is a relaxation probe, not a claim that the universe has such a velocity.

This trial space is a projection of the linearized equation, not an invariant family of exact distributions. It does not impose that a far-from-equilibrium singlet remains thermal. The established literature [1,2] distinguishes momentum-dependent evolution from integrated abundance equations; our matrix reduction below is derived here, not a transfer of those papers' model-dependent relic densities.

## 3. Collision Dirichlet form and its metric

Let dR_ij be the positive equilibrium event measure for s_i+l -> s_j+l, summed over lepton charge/spin, with the initial-spin-averaged matrix element from Note 51:

```
|M_ij|^2 = Kij^2 ml^2 (4ml^2-t)/(mh^2-t)^2,   t<=0.
```

There is no timelike Higgs width in this propagator. Detailed balance of the fixed bath allows the weak collision form to be symmetrized:

```
D[chi,psi] = (1/2) sum_(ordered i,j) integral dR_ij
             [chi_i(p)-chi_j(p')] [psi_i(p)-psi_j(p')].
```

Thus D is symmetric and nonnegative. A constant common chi is a null direction because scattering conserves total singlet count. For i!=j, the two directions are equal after exchanging initial/final variables; compute **21 once**, with no additional one-half. For elastic ii scattering, the one-half remains. It avoids counting reverse jumps twice in the Dirichlet form, not identical initial particles in a cross section.

For the ordered six basis coefficients (a1,a2,b1,b2,c1,c2), define

```
G_ab = sum_i integral d^3p/(2pi)^3 f_i^0 phi_a phi_b,
G dot(theta) = -D theta,
C = G^(-1/2) D G^(-1/2).
```

Normalize both G and D by N_eq=n1_eq+n2_eq, with zeta omitted since it cancels. Write x_i=m_i/T, R_i=K1(x_i)/K2(x_i), r_i=n_i_eq/N_eq. The diagonal metric is

```
Ebar_i = 3T + m_i R_i,
v_i = Var(E_i)/T^2 = 3+x_i^2(1-R_i^2)-3x_i R_i,
p_i = <p_z^2>/T^2 = Ebar_i/T+1,
G/N_eq = diag(r1,r2,r1*v1,r2*v2,r1*p1,r2*p2).
```

The density and centered-energy functions are orthogonal. Scalar/vector cross blocks vanish by parity. The exact total-number direction is removed algebraically; it is not identified by discarding an eigenvalue below an arbitrary numerical threshold. Three scalar projected rates and two drift projected rates remain.

Restricting the trial space to a1,a2 recovers Note 51's Gamma_down+Gamma_up. Allowing energy perturbations introduces nonzero density–energy couplings, so that count-only value is not an exact eigenvalue of the larger matrix.

## 4. Exact invariant reduction of the energy and momentum moments

At q=sqrt(s), let A_i=(s+m_i^2-ml^2)/(2q) and p_i*=sqrt(lambda_i)/(2q) be CM scalar energy and momentum. For a CM scattering angle c,

```
t=m_i^2+m_j^2-2 A_i A_j+2 p_i* p_j* c.
```

The invariant CM-boost measure is sinh(eta)^2 exp[-(q/T)cosh(eta)] d eta. With z=q/T and R=K2(z)/K1(z), its normalized moments are

```
<cosh eta>=R,
<cosh^2 eta>=1+3R/z,
<sinh^2 eta>=3R/z.
```

They follow by differentiating K1(z)/z; they are also checked by direct rapidity integration. Averaging boost directions gives

```
<E_i>=A_i R,
<E_i E_j>=A_i A_j(1+3R/z)+p_i* p_j* c R/z,
<vec(p_i).vec(p_j)> = <E_i E_j>-(m_i^2+m_j^2-t)/2.
```

A final isotropic rotation divides the spatial dot product by three for a single drift component. These identities include the mass-changing recoil; replacing -t by the entire spatial momentum transfer would incorrectly omit the energy transfer.

Only two t moments are required:

```
W0(q) = integral dt |M|^2/(16pi),
Wu(q) = integral dt (-t)|M|^2/(16pi).
```

For elastic ii scattering, the energy/drift entries before the invariant thermal integral become particularly simple:

```
D_EE integrand = (1/2) Wu * R/(z*T^2),
D_pp integrand = (1/2) Wu * [1+R/z]/(3*T^2).
```

All four scalar inelastic entries and their cross terms use the displayed energy moments. The independent numerical reference performs explicit Lorentz boosts and integrates boost directions and scattering angles; it does not call the production Bessel-reduced Gram formulas.

The common invariant event measure is the Note-51 normalization:

```
integral dR = g_l T/(16pi^4) integral_(q0)^infinity dq W0(q) K1(q/T),
q0=max(m_i,m_j)+ml.
```

The implementation substitutes the appropriate weighted jump Gram matrix for W0. Production integration uses w=(q-q0)/T and scaled Bessels; a separate q integration uses ordinary Bessels. The relative-energy window is w in [0,90]; the CM boost has already been integrated over its full mathematical range.

## 5. Calculated rates

All numbers below use the stated ideal MB lepton bath, both elastic channels and 21 conversion, exact tree recoil, and assumed radiation H. No QCD collision, decay moment or number-changing collision is included.

| T [GeV] | Count-only conversion/H | Slowest projected density/energy rate/H | Slowest projected drift rate/H |
|---|---:|---:|---:|
| 0.5 | 1.7627736 | 0.6044447 | 0.4180960 |
| 0.4 | 0.7037969 | 0.1938651 | 0.1293177 |
| 1/3 | 0.2918624 | 0.0670393 | 0.0435385 |

At T=0.5 GeV the three scalar projected rates are (0.604445,1.783991,2.141335)H and the two drift projected rates are (0.418096,1.987710)H. The slow scalar vector carries about 97.05% of its metric norm in the two centered-energy components. It is temperature-dominated within this trial space, not purely a number-ratio perturbation.

For comparison, using **only diagonal elastic scattering**, the species energy-moment rates are (0.486507,0.372954)H and drift rates are (0.325135,0.241861)H. Inelastic scattering changes these through coupled species/energy transfer; adding independent scalar event counts does not reproduce the matrix problem.

Interpretation is deliberately one-sided. A positive self-adjoint detailed-balance collision operator has a gap defined by the infimum of its Rayleigh quotient orthogonal to the conserved number. Minimizing over a finite trial space restricts that infimum, so the smallest projected rate is an **upper bound**, not a lower bound, on the corresponding full operator's gap. The actual full momentum spectrum has not been computed and can contain slower behavior. This variational statement applies only to the declared lepton-scattering operator, not to a full model with missing positive collision terms.

Therefore these results do not establish the actual singlet distributions or a kinetic-decoupling temperature. They show why the calculated lepton channel does not provide a uniform rapid-relaxation justification for imposing a common MB shape. QCD, other scattering, and internal interactions may change that conclusion after they are calculated.

## 6. Quantum statistics and numerical control

For the same dilute scalar reference, vacuum bath dispersion and zero lepton chemical potential, Note 51's pointwise inequality applies to every nonnegative quadratic jump form:

```
B_l=(1+exp(-ml/T))^(-2),
B_l D_l,MB <= D_l,FD <= D_l,MB  [Loewner matrix order].
```

Sum flavor by flavor before diagonalizing. At T=.5 the slowest projected energy rate lies in [0.568214,0.604445]H and the slowest projected drift rate in [0.393180,0.418096]H. These are **bounds on the FD-projected matrix eigenvalues**, not confidence intervals, not a numerical FD phase-space integral and not lower bounds on the full kinetic spectral gap. Applying a single averaged suppression factor to every matrix element is not done.

Eighteen q/w matrix comparisons give a largest relative Frobenius difference about 3.70e-15. Refining t quadrature from 24 to 48 nodes changes the central matrix by about 2.27e-16 relatively. These numerical comparisons do not establish comparable physical accuracy.

An analytic conservative bound controls the omitted mathematical tail. Use W0 <= Kij^2 ml^2(4ml^2 q^2+q^4/2)/(16pi mh^4), positivity of the Gram form, E_i<=P0, and monotonic scaled K1,K2. The resulting polynomial moments through degree six integrate to upper incomplete Gamma functions. Dividing the trace bound by the smallest metric diagonal bounds the normalized operator norm of the tail. Summed over all channels at T=.5, its floating evaluation is <1.80e-29 H. The bound concerns this mathematical MB/vacuum-tree extension, not omitted physical interactions; its numerical evaluation is not a directed-rounding certificate. The code includes the full upper expression.

## 7. Execution and milestone status

The first new 31-test suite passed without changes to its assertions or physics implementation. An initial foreground combined attempt timed out before completing the inherited chain and is retained as an incomplete log, not counted as a pass. The separately completed combined run passed 339 tests (308 inherited plus 31 new), zero failures/errors, exit code zero. Clean-package validation is recorded separately after it is actually performed.

The tests cover independent thermodynamic moments, explicit boost/orientation integration, 60-digit transfer integrals, reciprocity, number conservation, positive collision forms, density–energy coupling, metric eigenproblems, FD matrix order, window/refinement controls and absent-channel rejection. They are mathematical/software checks. The inherited chain is the attached local lineage, including its 26-test Note 49; the alternate live Note-49 suite and original standalone Note-41/45-real suites are not silently counted. No whole-repository or unaffiliated review is claimed.

Immediate scope achieved: the Note-51 dependency is hash-verified; the lepton subproblem has a declared model/domain and numerical checks; G04 now has energy and momentum-transfer diagnostics rather than only counts. These are component advances, not closure of G01/G02/G04 across the whole program. The full QCD response in Section 8 is not yet evaluated, so G03 remains open. The complete abundance, total lifetime, H2 observable and broader foundational milestones remain separate.

## 8. Explicit QCD-bath response to compute next

Define the renormalized scalar operator O_S by the chosen matching convention L_int=-h O_S/v. In the QCD sector it includes the retained quark mass operators and, when heavy flavors are integrated out, the matched gluonic operator with its specified Wilson coefficient. The same flavor must not be included both explicitly and as an integrated-out contribution.

For a stationary thermal bath define

```
W_S^>(omega,k;T) = integral d^4x exp[i omega t-i k.x] <O_S(x) O_S(0)>_T.
```

It has mass dimension four. Its Lehmann representation is a sum over squared operator matrix elements weighted by initial bath probabilities and delta(omega+E_a-E_b). Swapping a and b gives the detailed-balance identity

```
W_S^>(-omega,-k)=exp(-omega/T) W_S^>(omega,k).
```

At leading portal order with the vacuum Higgs propagator, the differential scalar transition kernel is

```
dGamma_(i->j)(p)/d^3p' = Kij^2 W_S^>(E_i-E_j,p-p';T)
 /[(2pi)^3 2E_i 2E_j (mh^2-(p-p')^2)^2].
```

This formula follows directly by inserting the bath matrix-element sum in the same transition probability used above. It implies thermal detailed balance with the scalar Boltzmann weights. For a free lepton bath, inserting its scattering cut recovers the Note-51 spin trace and the collision measure used in this note. For interacting QCD, the response and its matching are additional calculations/inputs, not specified by the lepton result.

Crucially, a thermal response depends separately on omega, |k| and T. A timelike vacuum function of invariant mass alone does not determine it. Its full support also contains pair-emission/absorption cuts; blindly using the full response and then adding the same separately computed decay again would double count. G03 must specify the scattering contribution and its relation to the separately retained decay cuts. At the same-particle free-bath scattering level, transfer is spacelike. The full inclusive response need not have only that support.

A free-quark reference requires a declared dispersion/occupation prescription and Yukawa/current-mass convention; a color factor times a lepton result is not, by itself, a controlled finite-temperature QCD estimate. The primary singlet-DM kinetic study [1], Sec. III.1, likewise treats the plasma treatment as a separate uncertainty rather than deriving it from the vacuum Higgs width. No quark/gluon thermal response value has been produced here.

Next executable task: evaluate a clearly labeled weak-coupling/free-bath reference for that response, verify its scattering support and reciprocity against direct amplitudes, then assess the relevant medium/strong-coupling corrections and regime matching before promoting it to the physical bath kernel. Add the resulting **momentum-weighted** matrix, not merely a population rate, to the current diagnostic. No arbitrary enhancement is used to force equilibrium.

## Sources, attribution and historical boundary

[1] T. Binder, T. Bringmann, M. Gustafsson and A. Hryczuk, *Early kinetic decoupling of dark matter: when the standard way of calculating the thermal relic density fails*, arXiv:1706.07433v3. https://arxiv.org/html/1706.07433v3 . Sections II and III.1 supply the phase-space collision framework, the distinction from a Fokker–Planck approximation, the diagonal Higgs-portal scattering normalization, and the separate plasma uncertainty. The six-moment matrix and numerical values in this note are new derivations in the declared benchmark, not results quoted from that paper. Their spin-summed amplitude must be mapped to our initial-spin average and g_l=4, not multiplied by g_l a second time.

[2] M. Garny, J. Heisig, B. Lulf and S. Vogl, *Coannihilation without chemical equilibrium*, arXiv:1705.09292v2. https://arxiv.org/html/1705.09292v2 . Eq. (7) and Appendix C supply inherited reaction-density conventions and the need to distinguish a kinetic ansatz from a momentum-dependent solution. No cosmological result from that distinct model is imported.

Internal: Note 51 and `COLLISION_INVENTORY_NOTE_51.json` at the inspected commit; its supplied archive; the master goal in issue #3. The broader corpus retains Part-0/audit rules and separately typed interpretations. No prior virtual or real-QCD result is altered by this lepton-moment calculation. No Omnes arrays, laboratory data, complete relic abundance, journal submission, or new DOI is claimed.
