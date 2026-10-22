# Scientific checkpoint — 21 October 2026

## Disposition and scope

The three computational stages are ready to preserve together as a reproducible **conditional free-bath benchmark**. The freeze records a completed numerical chain and a scoped analytic result. It does not promote GATE-03, establish a physical relic abundance, or validate the broader theory. Refinement differences below are empirical sensitivities, not certified continuum errors or physical uncertainty estimates.

The common inherited model has scalar masses 10 and 11.5 GeV, a 125 GeV Higgs mediator, portal couplings `K11=K22=+0.001`, `K12=-0.001`, and an ideal Maxwell–Boltzmann bath of `e, mu, tau, u, d, s, c, b` with fixed masses. The original model lineage is pinned to `Cbaird26/mqgt-scf-continued` commit `994e51cb28b51ade500bb0e1902f3b082ef8e594`. Each package carries its own provenance record. [1–3]

## 1. Enlarged moment spaces

At $T=0.4$ GeV, the saved rates divided by the prescribed $H(T)$ are:

| Diagnostic | Original space | Enlarged space |
|---|---:|---:|
| Slow scalar mode | 0.788181031 | 0.747848884 |
| Slow drift mode | 0.521608084 | 0.510586637 |
| Count-only contrast | 2.974745765 | — |
| Quadrupole sector, newly evaluated | — | 0.920803280 |

The slow scalar and drift rates decrease by **5.1171%** and **2.1130%**. The independently integrated original six-moment collision matrix agrees with the inherited implementation to a relative Frobenius difference of approximately $9.63\times10^{-14}$. Common-number null, positivity, symmetry, and interlacing checks pass. Endpoint checks at $T=1/3$ and $0.5$ GeV are also archived. [1]

For the fixed reversible operator and exact integrals, enlarging a trial space decreases variational upper bounds after removing the common-number mode. Rates above $H$ in a restricted space do not establish a positive full-operator lower bound or kinetic equilibrium. Drift and quadrupole need not be excited in an isotropic cosmological preparation.

## 2. Fixed-temperature momentum evolution and the tail theorem

The next stage evolves specified positive isotropic perturbations at fixed $T=0.4$ GeV. With $\tau=H_{\rm ref}t$, the resolved fractions of the initial excess remaining are:

| $\tau$ | Population excess | Mean-total-energy excess |
|---|---:|---:|
| 1 | 0.055912970 | 0.414928883 |
| 5 | 0.000325885 | 0.019895727 |

These use each represented initial perturbation's own normalization. The energy projection retains 99.935897% of the continuum initial variance; a separate common-continuum normalization is supplied. The enlarged scalar moments track the tested bulk-energy residual within the reported grid sensitivity. At $\tau=5$, the enlarged-versus-grid energy difference is 0.655%, while the 64-to-128-cell change is 1.101%. This conclusion is specific to the tested states, observables, and times. [2]

The separate analytic tail argument establishes a **zero uniform equilibrium-weighted $L^2$ gap** for the scattering-only operator if the stated vacuum-tree model is extended unchanged to unbounded momentum. The proved bound is

$$\nu_i(p)\leq B_i(T)/E_i(p),$$

not an asserted exact $1/E$ asymptotic law. Centered high-energy indicators then have Rayleigh quotients tending to zero. The conclusion applies already in the isotropic sector and is compatible with the finite-time bulk relaxation above. It is conditional on the fixed ideal bath, retained massive propagator, channel list, unbounded domain, and chosen norm; it does not describe an unspecified ultraviolet completion. The finite graph's positive lowest rate is not the continuum gap. [2]

## 3. Expanding fermionic network

The third stage evolves $T=0.5\rightarrow1/3$ GeV with redshift, scattering/conversion, pair annihilation/inverse production, and heavy decay/inverse absorption with recoil. The coordinates $y=p/T$ and $\eta=\ln(a/a_0)$ follow free streaming for the prescribed $aT=$ constant background. Scattering and decay conserve scalar count; pair reactions change it. [3]

| Final observable at $T=1/3$ GeV | Saved value |
|---|---:|
| $T_{\rm kin}/T$, with $T_{\rm kin}=P_\phi/n_\phi$ | 0.750271338 |
| Continuum collisionless $T_{\rm kin}/T$ | 0.709060074 |
| Heavy fraction | 0.036632159 |
| Instantaneous equilibrium heavy fraction | 0.013409921 |
| Comoving number / initial number | 0.9999684642 |
| Net comoving-number loss | 31.5358 ppm |
| Total-variation distance to MB momentum shapes at actual species fractions | 0.141561602 |

The shape comparison retains the actual species abundances, so it resolves momentum-shape departure independently of the heavy/light abundance mismatch. $T_{\rm kin}$ is a pressure moment, not an assumed thermal fit. Channel controls show scattering and redshift dominate this trajectory. [3]

New inputs are explicit: zero-chemical-potential scalar MB distributions at $T_0=0.5$ GeV, initial total density $1.7005907436\times10^{-9}$ GeV$^3$, constant $g_*=g_{*s}=60$, and a fixed timelike Higgs-width prescription $\Gamma_h=0.0041$ GeV. The 31.5358 ppm loss depends on that initial abundance. Initial equilibrium is imposed rather than derived from an earlier thermal history.

The final grid has 192 finite momentum cells plus a semi-infinite tail per species. The largest observed refinements among the listed controls are 0.03524% in $T_{\rm kin}/T$ (momentum grid), 0.27873% in heavy fraction (temperature interpolation), and 0.006819% of the small annihilation-loss fraction (time steps). Number-conserving channel controls preserve total comoving number within $2.89\times10^{-15}$; all evolved populations remain positive. The supplied-bank reproduction, structural checks, and independent thermal/collisionless controls are archived. [3]

The earlier fixed-temperature gap theorem is not automatically a theorem for this nonlinear, time-dependent evolution.

## Open work and priority order

1. **Thermal prehistory and initial abundance.** Derive or explicitly vary the initial fugacity and momentum preparation within a stated validity range. The present starting abundance is not evidence for earlier chemical equilibrium. The saved yield is not a physical relic prediction.
2. **Interacting QCD response and matching.** Specify the renormalized operator basis, scale, coefficients, finite-temperature correlators, gluonic terms, and uncertainty treatment. Avoid counting explicit heavy quarks again through matched effective gluon contributions. Match free-quark decay diagnostics onto a physical hadronic spectrum where required.
3. **Physical network and thermodynamic closure.** Supply the omitted loop-induced channels, specified scalar self-interactions, and temperature-dependent equation of state and entropy history. The known higher-order scalar-exchange audit is an equilibrium diagnostic, not a trajectory-wide bound. The evolved network remains the leading-portal-order fermionic subset.
4. **GATE-03 apparatus branch remains open.** Preserve the earlier source audit's Objects 1–5: calibrated physical source; field transfer and estimand; device generator/readout; nuisance likelihood and controls; accessible interval and sensitivity. Laboratory source density, geometry, boundaries, normalization, detector coupling, acquisition/noise records, and endpoint/promotion rules still require concrete inputs. No operator-ready protocol or gate promotion follows from these cosmological runs. [4]
5. **Electromagnetic construction remains conditional.** The prior audit identifies physical profile/normalization selection, finite matching, electroweak embedding, and evolution to the measurement scale as remaining requirements. Leading spectral constraints alone did not uniquely select the coupling in the audited examples. This freeze does not turn a conditional coefficient or numerical fit into a parameter-free prediction. [4]

The numerical next steps in the first package are historical. The second and third packages complete the specified momentum and expansion targets within their declared free-bath scopes; the physical medium, apparatus, and electromagnetic requirements remain separate.

## Attribution and evidence

Christopher Michael Baird supplied project direction, source material, and the Grok roadmap/commentary in the conversation. ChatGPT/Codex produced the enclosed numerical continuations, analytic argument, diagnostics, and internal review records. Grok's supplied comments informed task selection and interpretation; this snapshot does not claim that Grok independently executed or reproduced the enclosed code. Internal checks by separate AI agents are not external scientific peer review or experimental validation.

The numerical claims above were checked against the delivered JSON records without rerunning or modifying the frozen packages. Repository publication preserves a scientific checkpoint; it is not evidence for stronger physical claims.

### Evidence map

- **[1]** `Free_Bath_Nested_Moments_2026-10-21`: `RESEARCH_NOTE.txt`, `numerics/results_q80.json`, `numerics/verification.json`, `numerics/three_temperature_summary.json`, and `provenance.json`.
- **[2]** `Free_Bath_Momentum_Evolution_2026-10-21`: `RESEARCH_NOTE.txt`, `report/comparison_summary.json`, `solver/final_evolution.json`, `solver/convergence_summary.json`, `tail/CONDITIONAL_ZERO_GAP_THEOREM.txt`, and `provenance.json`.
- **[3]** `Expanding_Free_Bath_Fermionic_Network_2026-10-21`: `RESEARCH_NOTE.txt`, `results/full_final.json`, `results/convergence_summary.json`, `report/comparison_summary.json`, `network/NETWORK_AUDIT.txt`, `review/reproduction_check.txt`, and `provenance.json`.
- **[4]** `Free_Bath_Nested_Moments_2026-10-21/NEXT_STEPS.txt` and its `provenance.json` record the earlier apparatus/EM source audit, inspected collection ranges, and GATE-03 source identities. These are retained audit findings, not a claim to have re-audited the current external repositories during this scientific checkpoint review.
