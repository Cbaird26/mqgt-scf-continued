FIXED-TEMPERATURE MOMENTUM-RESOLVED FREE-BATH EVOLUTION
Prepared 2026-10-21

This package extends the earlier nested-moment calculation to isotropic
momentum-cell evolution at T=0.4 GeV in the same declared ideal bath.
It also contains a conditional analytic proof of a zero uniform L2 gap
when this scattering-only vacuum-tree model is extended to all momenta.

MAIN RESULTS

For two separate initial preparations, f(0)=f_eq*(1+0.05*h), use
  h_P = 1_(species=2) - equilibrium heavy-species fraction,
  h_E = (E - equilibrium mean energy)/T.

At tau=H_reference*t=1, the radial grid leaves 5.59% of the initial
population excess and 41.49% of the initial energy excess. At tau=5,
the corresponding fractions are 0.0326% and 1.990%.

At tau=5, the original and enlarged scalar moment spaces predict 1.740%
and 1.977% energy excess remaining. The enlarged-space difference from
the grid is smaller than the last grid-refinement change of 1.10%.
That comparison is consistent at the tested resolution; it is not a
certified sub-percent continuum-error estimate.

The bath is held fixed. H_reference is only a time unit. No expanding
cosmological history, QCD medium response, or apparatus response was
computed here. The grid treats isotropic radial distributions; it does
not newly evolve angular drift perturbations.

START HERE

RESEARCH_NOTE.txt                 Integrated findings, method, limits, proof.
REPRODUCING.txt                   Environment, commands, and reproduction scope.
report/Free_Bath_Momentum_Evolution_T0p4_GeV.png
                                 Figure of bulk decay and moment comparison.
report/comparison_summary.json   Compact exact numerical summary and metadata.

REPRODUCE

  python -m pip install -r requirements.txt
  python reproduce_all.py

The default reuses supplied raw collision graphs, reruns the numerical
evolution and independent checks, and rebuilds the figure. Add --full to
recompute all four raw collision graphs first. No network is needed after
the dependencies are installed. See REPRODUCING.txt for details.

DIRECTORIES

baseline/     Byte-preserved code/data from the prior nested-moment package.
solver/       Positive reversible collision graphs, evolution, convergence.
comparison/   Evolution in the original and enlarged polynomial spaces.
tail/         Conditional theorem, explicit bound constants, calculator.
review/       Independent internal method review and matrix-exponential check.
report/       Figure and compact machine-readable comparison.

provenance.json records the pinned inherited model sources and parent
package identity. SHA256SUMS.txt covers the delivered files except itself.
The review is an independent internal AI-assisted check, not external
scientific peer review.

NORMALIZATION AND INTERPRETATION

Headline energy curves normalize by their represented initial excess.
The radial grid retains 99.935897% of the continuum initial energy
variance. Both own-initial and continuum-initial normalizations are saved.
The population initial profile is represented exactly.

All grids retain a semi-infinite final energy cell. This retains tail
mass and event weights but cannot represent arbitrarily remote tail
perturbations. A finite graph's positive lowest eigenvalue therefore does
not contradict the conditional zero-gap theorem of the unbounded model.
Zero uniform gap does not imply absent bulk relaxation. Grid/quadrature
refinement differences are sensitivity measures, not certified error bars.
