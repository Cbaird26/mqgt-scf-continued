EXPANDING FREE-BATH FERMIONIC NETWORK
21 October 2026

Result
------
The momentum-resolved calculation now includes cosmological redshift and
the leading-portal-order fermionic reaction network. It evolves from
T=0.5 GeV to T=1/3 GeV under a prescribed radiation background.

For the specified initial zero-chemical-potential Maxwell-Boltzmann state,
the final pressure-temperature diagnostic is Tkin/T=0.7502713, the heavy
fraction is 0.03663216 (instantaneous equilibrium: 0.01340992), and net
annihilation removes 31.5358 ppm of the initial comoving scalar number.

These are conditional free-bath benchmark results. The initial absolute
density, constant g*=g*s=60 background, and finite timelike Higgs width
are stated inputs. The calculation does not determine an earlier thermal
history, interacting QCD response, or a physical relic abundance.

Start here
----------
RESEARCH_NOTE.txt
  Complete interpretation, equations, assumptions, controls, refinement
  table, physical scope, and primary references.

report/Expanding_Free_Bath_Fermionic_Network_2026-10-21.png
  Four-panel scientific summary: pressure temperature, heavy fraction,
  comoving number loss, and momentum-shape distance from equilibrium.

report/comparison_summary.json
  Compact machine-readable snapshots and numerical sensitivities.

results/full_final.json
  Final evolution with selected complete momentum-cell populations.

results/convergence_summary.json
  Matched time, momentum-grid, temperature, quadrature, and tail checks.
  Relative abundance-change sensitivity is normalized to the small
  depleted fraction, not the almost-unit remaining population.

network/NETWORK_AUDIT.txt
  Crossing factors, detailed balance, decay recoil, timelike prescription,
  and excluded reaction sectors.

review/THEORY_REVIEW.txt
  Independent internal mathematical and computational review.
  This is not external peer review.

Reproduce
---------
Install requirements.txt, then run:

  python reproduce_all.py

This reruns the evolution, controls, and report using the six supplied
raw scattering/reaction banks. Run with --full to recompute those banks.
No network is required after dependencies are installed. The runner is
portable across working directories and was checked from outside the
package directory. See REPRODUCING.txt for exact scope and commands.

Contents and provenance
-----------------------
solver/ contains the redshift-coordinate scattering implementation and
the two required scattering banks. network/ contains the pair and decay
kernels, their four required banks, and targeted diagnostic records.
results/ contains the final matched comparisons and channel controls.
review/ contains independent analytic and normalization checks.

source_reference/ preserves the pinned inherited model records. These
are provenance inputs; reproduction uses the standalone implementation
in this package. provenance.json identifies the original source commit,
parent package, and newly declared assumptions. SHA256SUMS records the
delivered bytes; regeneration can change timing fields and checksums.

Older q24 and separate q48 eight-interval pilot banks are not included.
The final q48 bank contains the eight-interval nodes as an exact subset.
Refinement differences throughout are empirical sensitivities, not
certified continuum-error bounds.
