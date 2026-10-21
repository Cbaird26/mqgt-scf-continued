"""Build scientific note, derived diagnostics and exact-data plots from saved runs."""
from pathlib import Path
import json,math,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/toe_thermal_matplotlib')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'results'
read=lambda name:json.loads((OUT/name).read_text())
scan=read('initial_condition_scan.json');summary=read('scan_summary.json');v=read('validation.json');meta=read('run_metadata.json')
source=v['independent_source_integral'];B=source['no_loss_inverse_creation_integral_over_reference']
rows={x['case']:x for x in summary};curves={x['initial_condition']['id']:x['rows'] for x in scan['cases']}
ode={x['initial_condition']['id']:x['rows'][-1] for x in read('independent_ode.json')['cases']}
step384={x['initial_condition']['id']:x['rows'][-1] for x in read('step384.json')['cases']}
metrics=['comoving_number_over_actual_initial','Tkin_over_T','heavy_fraction','total_variation_to_same_species_MB']
maxima={key:{metric:max(val[metric]['absolute_difference'] for val in v[key].values()) for metric in metrics}
        for key in ['step_192_vs_384','momentum_grid_192_vs_96','temperature_intervals_16_vs_8','scattering_quadrature48_vs40_at_temperature8','split_vs_independent_unsplit_ODE']}
conv={}
for cid in ode:
    ref=ode[cid]['comoving_number_over_actual_initial']
    coarse=abs(rows[cid]['final_number_over_actual_initial']-ref)
    fine=abs(step384[cid]['comoving_number_over_actual_initial']-ref)
    conv[cid]=dict(error192=coarse,error384=fine,error_ratio=coarse/fine if fine else None)
bound_discrepancy=abs(ode['z_1e-06']['comoving_number_over_equilibrium_reference']-(1e-6+B))
scalar_audit=json.loads((ROOT/'frozen'/'network'/'scalar_exchange_audit.json').read_text())
scalar_rate_T0=next(x['equilibrium_average_tagged_rate_over_H'] for x in scalar_audit['rows'] if x['T_GeV']==.5)
review=dict(refinement_maximum_absolute_changes=maxima,independent_ODE_time_convergence=conv,
            source_only_low_z_absolute_difference=bound_discrepancy,
            source_only_low_z_relative_difference=bound_discrepancy/(1e-6+B),
            omitted_scalar_only_initial_rate_over_H_at_z1=scalar_rate_T0,
            omitted_scalar_only_initial_rate_over_H_at_z10000=1e4*scalar_rate_T0,
            high_z10000_status='Formal stress test of the declared fermionic network; omitted nonlinear scalar channels can alter detailed results.',
            no_physical_relic_claim=True)
(OUT/'review_summary.json').write_text(json.dumps(review,indent=2)+'\n')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                     'axes.labelcolor':'#26364a','xtick.color':'#526273','ytick.color':'#526273','axes.titleweight':'bold',
                     'grid.color':'#e2e7ed','grid.linewidth':.7})
fig,axes=plt.subplots(1,3,figsize=(15.2,5.3))
fig.subplots_adjust(left=.055,right=.985,bottom=.19,top=.80,wspace=.30)
navy='#203b64';teal='#168888';orange='#d48123';purple='#8056a6';gray='#8a95a2'
z=np.array([x['initial_abundance_z'] for x in summary[:8]])
ret=np.array([x['final_number_over_actual_initial'] for x in summary[:8]])
axes[0].plot(z,ret,'o-',color=navy,lw=2,ms=5,label='Full frozen network')
axes[0].axhline(1,color=gray,ls='--',lw=1,label='Conserved comoving number')
axes[0].set(xscale='log',xlabel='Initial fugacity z',ylabel='Final / initial comoving number',title='A  Abundance memory',ylim=(.55,3.85))
axes[0].annotate('Inverse creation\nadds to the dilute state',xy=(1e-6,ret[0]),xytext=(2e-4,3.1),fontsize=9,
                 arrowprops={'arrowstyle':'->','color':gray},color=navy)
axes[0].annotate('10⁴: formal stress test',xy=(1e4,ret[-1]),xytext=(.05,1.7),fontsize=9,
                 arrowprops={'arrowstyle':'->','color':gray},color=navy)
axes[0].legend(frameon=False,loc='upper right',fontsize=8)
for cid,color,label in [('kinetic_0.75',teal,'Initial scalar temperature = 0.75 T'),('z_1',navy,'Initial scalar temperature = T'),('kinetic_1.25',orange,'Initial scalar temperature = 1.25 T')]:
    r=curves[cid];axes[1].plot([x['T_GeV'] for x in r],[x['Tkin_over_T'] for x in r],color=color,lw=2,label=label)
axes[1].axhline(1,color=gray,ls='--',lw=1)
axes[1].set(xlim=(.5,1/3),ylim=(.58,1.3),xlabel='Bath temperature (GeV)',ylabel='Scalar Tkin / bath T',title='B  Kinetic memory')
axes[1].legend(frameon=False,loc='upper right',fontsize=8)
for cid,color,label in [('heavy_0',teal,'Initial heavy fraction = 0'),('z_1',navy,'Initial heavy fraction = 0.0572'),('heavy_0.25',purple,'Initial heavy fraction = 0.25')]:
    r=curves[cid];axes[2].plot([x['T_GeV'] for x in r],[x['heavy_fraction'] for x in r],color=color,lw=2,label=label)
r=curves['z_1'];axes[2].plot([x['T_GeV'] for x in r],[x['instantaneous_eq_heavy_fraction'] for x in r],color=gray,ls='--',lw=1,label='Instantaneous equilibrium')
axes[2].set(xlim=(.5,1/3),ylim=(0,.275),xlabel='Bath temperature (GeV)',ylabel='Heavy scalar number fraction',title='C  Species memory')
axes[2].legend(frameon=False,loc='upper right',fontsize=8)
for ax in axes:ax.grid(True,alpha=.75);ax.set_axisbelow(True)
fig.suptitle('Initial conditions remain visible in the free-bath solution',y=.96,fontsize=16,fontweight='bold',color=navy)
fig.text(.5,.025,'0.5 → 1/3 GeV · g* = g*s = 60 · exact frozen banks · imposed initial states · no interacting-QCD or physical relic claim',ha='center',fontsize=10,color='#526273')
fig.savefig(OUT/'thermal_initial_condition_sensitivity.png',dpi=180)
fig.savefig(OUT/'thermal_initial_condition_sensitivity.svg')
plt.close(fig)

table='\n'.join(f"{x['case']:16s} {x['final_number_over_actual_initial']:14.7g} {x['final_Tkin_over_T']:12.7f} {x['final_heavy_fraction']:12.7f} {x['final_shape_TV']:12.7f}" for x in summary)
note=f'''THERMAL-HISTORY CONTINUATION: INITIAL ABUNDANCE AND PREPARATION
21 October 2026

RESULT

The actual 386-state momentum network was rerun and extended to twelve imposed
initial conditions. It retains substantial memory of initial abundance, momentum
shape and species fraction across the solved 0.5 -> 1/3 GeV interval. This is a
new conditional calculation within the frozen free-bath benchmark. It does not
establish an earlier equilibration history, an interacting-QCD response, or a
physical relic abundance.

The zero-chemical-potential baseline reproduced all four archived comparison
observables exactly at their recorded precision. The modified batched solver
matches its original baseline to floating-point roundoff. New files are separate
from the unchanged frozen scripts and banks.

1. DEFINED MODEL AND INITIAL DATA

The inherited masses are 10 and 11.5 GeV. The Higgs mass is 125 GeV, the portal
matrix is K11=K22=0.001 and K12=-0.001, and the constant timelike Higgs width is
0.0041 GeV. The bath consists of ideal Maxwell-Boltzmann e, mu, tau, u, d, s, c,
b fermions with the source's fixed vacuum masses. The radiation background has
g*=g*s=60 and a*T=constant. No thermal QCD medium is supplied.

The full declared network includes scalar-fermion scattering and conversion,
heavy-scalar decay and inverse absorption with momentum recoil, and scalar-pair
annihilation and inverse creation. It inherits the source's cell closure:
instantaneous equilibrium conditional shapes within finite momentum cells,
with a semi-infinite tail cell for each species. This closure is an approximation
even when the total distribution is nonthermal; grid sensitivities are reported.

The invariant normalization is n_ref=n_eq,total(T0)={meta['n_reference_GeV3']:.12g}
GeV^3, and M_a=a^3*n_a/n_ref. Consequently sum(M_initial)=z. Every new output
distinguishes N_ref=sum(M) from N_actual=N_ref/z; the source's original row name
would otherwise mislabel fugacity scans. Yield is N_ref*n_ref/s(T0), not a measured
or claimed present-day cosmological yield.

At theta=Ts/T0=1 and the equilibrium initial species ratio, the distribution is
f_i(p)=z*exp[-E_i(p)/T0]. Thus z is a common fugacity and mu=T0*ln(z). The scanned
z values are 10^-6, 10^-4, 0.01, 0.1, 1, 10, 100 and 10^4.

For kinetic preparation, each species' MB momentum distribution at Ts is normalized
to the SAME initial species fraction at T0 (heavy fraction 0.0572145986), and total
number is fixed to z=1. The two extra values are theta=0.75 and 1.25. These are
shape changes; they are not full chemical equilibrium at Ts. Two further runs
set the initial heavy fraction to 0 or 0.25, keep theta=1 and z=1, and evolve the
resulting conversion dynamics. Species chemical potentials need not be equal.

The bath inverse-creation source is never rescaled by imposed scalar fugacity.
Writing E for instantaneous zero-mu equilibrium comoving cell populations, the
same equation is solved in every run:

  dM/deta = Q(eta) M + alpha [E*(A E) - M*(A M)],
  eta=ln(T0/T), alpha=n_ref*a^-3/H(T).

Q combines the two number-conserving conductance operators, A is the positive
pair-annihilation kernel, and * denotes componentwise multiplication. Changing
z changes only the boundary condition, not Q, A, E, H, or the bath.

2. NUMERICAL RESULTS AT T=1/3 GeV

Case                Nfinal/Ninitial      Tkin/T       heavy r     shape TV
{table}

The reference state has Tkin/T=0.75027134, heavy fraction=0.03663216 and
31.5358 ppm net number loss. Its instantaneous equilibrium heavy fraction is
0.01340992. The shape-TV metric compares the normalized momentum distribution
with MB shapes at the ACTUAL evolved species fractions; it is not a fit p-value.

The kinetic preparations leave final Tkin/T=0.62818 and 0.87076. The initial
species preparations leave heavy fractions 0.02320 and 0.08189. Differences are
far larger than the tested numerical sensitivities. The solved interval therefore
does not establish independence from either momentum or species preparation.

For z=0.01 to 100, the final abundance remains nearly proportional to the imposed
initial abundance. The finite interval does not select a unique cosmological
abundance. At z=10^-6, inverse creation raises the number by a factor about 3.564;
this is a source-driven floor within the specified bath and window. At z=10^4,
the DECLARED network annihilates 25.4274% of its initial population. That final
case is a formal stress test, with an additional truncation limitation below.

3. INDEPENDENT SOURCE LIMIT AND NUMERICAL CHECKS

Summing the equation gives dN/deta=alpha*(E^T A E - M^T A M), because Q conserves
number. Since A and M are nonnegative, N_final <= z+B, where

  B = integral alpha E^T A E d_eta = {B:.12g}.

B was independently integrated with adaptive scalar quadrature between bank
knots, not inferred from the evolved abundance. The direct unsplit DOP853 solution
at z=10^-6 gives N_final={ode['z_1e-06']['comoving_number_over_equilibrium_reference']:.12g};
its difference from z+B is {bound_discrepancy:.3g} in reference units. The tiny loss
in this limit independently confirms that inverse creation was kept tied to the
bath, including when the scalar sector begins very dilute.

The standard split evolution uses 192 nominal eta steps and 195 actual intervals,
192 finite momentum cells plus an infinite tail per species, and 16 regular
temperature-bank intervals plus the T=0.4 node. The original 192-step settings
were retained to reproduce the frozen baseline. A 384-step run, a 96-cell run,
an 8-temperature-interval run, and matched lower scattering quadrature were also
executed for every initial condition. Six representative cases were independently
integrated with unsplit DOP853 (rtol=2e-10, atol=2e-13 in M/z), restarting at
interpolation knots; this required 274 RHS evaluations.

Maximum absolute changes across the twelve cases:
                               Nfinal/Ninitial    Tkin/T       heavy r       TV
192 -> 384 eta steps            {maxima['step_192_vs_384'][metrics[0]]:.3g}             {maxima['step_192_vs_384'][metrics[1]]:.3g}      {maxima['step_192_vs_384'][metrics[2]]:.3g}       {maxima['step_192_vs_384'][metrics[3]]:.3g}
192 -> 96 finite cells          {maxima['momentum_grid_192_vs_96'][metrics[0]]:.3g}             {maxima['momentum_grid_192_vs_96'][metrics[1]]:.3g}      {maxima['momentum_grid_192_vs_96'][metrics[2]]:.3g}       {maxima['momentum_grid_192_vs_96'][metrics[3]]:.3g}
16 -> 8 temperature intervals   {maxima['temperature_intervals_16_vs_8'][metrics[0]]:.3g}             {maxima['temperature_intervals_16_vs_8'][metrics[1]]:.3g}      {maxima['temperature_intervals_16_vs_8'][metrics[2]]:.3g}       {maxima['temperature_intervals_16_vs_8'][metrics[3]]:.3g}
q48 -> q40, both at 8 intervals {maxima['scattering_quadrature48_vs40_at_temperature8'][metrics[0]]:.3g}             {maxima['scattering_quadrature48_vs40_at_temperature8'][metrics[1]]:.3g}      {maxima['scattering_quadrature48_vs40_at_temperature8'][metrics[2]]:.3g}       {maxima['scattering_quadrature48_vs40_at_temperature8'][metrics[3]]:.3g}

The worst split-versus-unsplit Nfinal/Ninitial difference is 0.000723786, occurring
at z=10^-6, or 0.0203% relative. Its 192/384-step error ratio against the independent
solution is {conv['z_1e-06']['error_ratio']:.6f}, consistent with second-order convergence.
For other cases the abundance agreement is much tighter. These are measured
sensitivities of this implementation, not certified continuum-error bounds.
Do not interpret all displayed CSV digits as independent physical precision.

Disabling annihilation and its inverse conserves number to 2.8e-15 and gives
fugacity-independent normalized endpoint shapes to 1.9e-15 in L1. No clipping or
normalization repair is applied during evolution. Populations remain nonnegative
in all runs; the heavy-zero preparation legitimately starts with zero populations
in its second species. The fixed-temperature equilibrium operator has relative
linear stationarity residual below 3.3e-17. The continuum MB initial identity
Tkin/T0=theta holds exactly; cell moment reconstruction differs by about 1.1e-4
in the cooler case and 9.9e-5 in the hotter case, consistent with finite-cell
closure rather than a redefinition of the preparation.

4. PHYSICAL LIMITS THAT REMAIN

The maximum INITIAL phase-space occupation among these preparations is
2.0612e-5. The maximum scalar/radiation energy-density ratio among saved states is
1.6101e-4. Those checks support dilute scalars and a prescribed radiation background
for this exercise; they do not validate omitted interactions.

In particular, the frozen source independently audits higher-portal-order
Higgs-exchange scalar-only 2->2 processes, outside the evolved K^2 fermionic
network. Their initial equilibrium average tagged rate/H is
{scalar_rate_T0:.9g} at z=1, hence {1e4*scalar_rate_T0:.6f} at z=10^4 for the
same normalized initial shape. Such channels can affect high-z shapes and species
redistribution even when scalar energy density is small. Their nonlinear kernels
and any independent scalar quartics/cubics are not supplied here. Therefore the
10^4 point is a diagnostic of the specified truncated equations, not a robust
precision prediction of the full underlying scalar theory.

The free quark bath near this temperature window remains a model assumption.
No lattice-QCD or hadronic spectral function has been substituted or invented.
Changing initial z does not compute the earlier process that generated z. Changing
theta or the heavy fraction does not supply a reheating or production mechanism.
The result establishes initial-condition sensitivity of the declared window,
not failure or success of a unique complete cosmology.

5. REPRODUCTION AND PROVENANCE

From this directory, with NumPy/SciPy/Matplotlib installed:

  OPENBLAS_NUM_THREADS=1 python run_continuation.py
  python make_report.py
  python verify_provenance.py

The numerical suite took {meta['elapsed_seconds']:.2f} seconds in the recorded environment.
It does not use network access. Outputs are written only to results/. Frozen
scripts and raw banks are imported/read without modification. To reacquire the
pinned public inputs when needed, run download_frozen.py followed by
restore_banks.py; these acquisition steps require read-only network access.

All 55 acquired Git blobs were checked against the pinned tree, all 41 acquired
files with archived SHA-256 entries matched them, and all four split large banks
were reconstructed to their archived SHA-256 checksums. The two decay banks were
downloaded directly and likewise verified. source_provenance.json records full
source URLs, Git blob hashes, SHA-256 hashes and byte counts. The complete repository
and unused diagnostic outputs are not claimed to have been mirrored.

Source commit:
https://github.com/Cbaird26/mqgt-scf-continued/tree/48f9dcbd34e7cfb86504167a0483f732a5dd5e8e/manuscript/higgs_portal_review/checkpoints/2026-10-21-free-bath

Primary equations/implementation: frozen/network/evolve_network.py,
frozen/network/pair_annihilation.py, frozen/solver/expanding_free_bath.py.
Original physical scope and review: frozen/REPRODUCING.txt,
frozen/RESEARCH_NOTE.txt, frozen/review/THEORY_REVIEW.txt.
Scalar-channel limitation: frozen/network/scalar_exchange_audit.json and .py.

6. NEXT SCIENTIFIC DECISION

An earlier-time calculation must show how a physical initial state is produced
or demonstrate attraction from a specified range of initial states. The present
equilibrium boundary at 0.5 GeV cannot be promoted to a unique thermal history
merely by rerunning this later interval. The practical next calculation is a
stated prehistory with controlled medium response, followed by matching onto this
validated momentum-network window and repeating the initial-state tests. The
observed memory gives a quantitative target for that work.
'''
(ROOT/'SCIENTIFIC_NOTE.txt').write_text(note)
print('Saved scientific note, review summary and PNG/SVG figures.')
