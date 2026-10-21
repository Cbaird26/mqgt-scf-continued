"""Report the bounded entropy-consistent EOS sensitivity calculation."""
from pathlib import Path
import json,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/toe_thermal_matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent;D=ROOT/'eos'
r=json.loads((D/'eos_sensitivity_results.json').read_text());v=r['validation']
table_status=v.get('table_validation_status','historical_prepublication_validation')
if v.get('max_table_pressure_deviation_in_quoted_errors') is not None:
    table_scope=('The original prepublication run' if table_status=='historical_prepublication_validation'
                 else 'This run')
    table_validation_text=(
        f"{table_scope} compared the analytic fit with the authors' WB-EoS.dat table. "
        f"The maximum deviations in the solved window were "
        f"{v['max_table_pressure_deviation_in_quoted_errors']:.3f} quoted-error units "
        f"in pressure and {v['max_table_energy_deviation_in_quoted_errors']:.3f} in energy density. "
        "This checks the published central fit; it is not an independent uncertainty "
        "estimate or a new lattice calculation.")
else:
    table_validation_text=(
        "The optional comparison against the authors' WB-EoS.dat table was skipped "
        "in this run because the source file is absent. The analytic EOS, derivative "
        "checks and Fermi-Dirac quadrature checks were still evaluated. The separately "
        "labeled historical_table_validation.json preserves the original local comparison "
        "and its source hash; those historical checks are not presented as rerun here.")
table_validation_text+=(
    " The raw ancillary table and reading PDFs are not redistributed in the public "
    "package. Source URLs, hashes and reuse-status notes are recorded in source_provenance.json. "
    "To repeat the optional table comparison, explicitly run "
    "python thermal/fetch_eos_validation_table.py from the package root, then rerun this suite.")
KINDS=['constant60','qcd_leptons_photon','qcd_leptons_photon_ideal_cb']
runs={kind:json.loads((D/(kind+'_standard.json')).read_text()) for kind in KINDS}
checks={}
for kind in KINDS[1:]:
    std=runs[kind]['rows'][-1];checks[kind]={}
    for label in ['time384','grid96']:
        other=json.loads((D/(kind+'_'+label+'.json')).read_text())['rows'][-1]
        checks[kind][label]={k:other[k]-std[k] for k in ['Tkin_over_T','heavy_fraction','comoving_number_over_actual_initial']}
checks['max_remap_count_error']=max(x['max_remap_number_error'] for x in runs.values())
checks['max_linear_count_error']=max(x['max_linear_step_number_error'] for x in runs.values())
checks['max_entropy_relative_error']=max(abs(y['entropy_comoving_over_initial']-1) for x in runs.values() for y in x['rows'])
(D/'eos_review_summary.json').write_text(json.dumps(checks,indent=2)+'\n')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                    'axes.labelcolor':'#26364a','xtick.color':'#526273','ytick.color':'#526273','axes.titleweight':'bold','grid.color':'#e2e7ed'})
fig,ax=plt.subplots(1,3,figsize=(14.7,5.1));fig.subplots_adjust(left=.055,right=.985,bottom=.19,top=.80,wspace=.28)
colors=['#203b64','#168888','#d48123'];labels=['Constant 60','2+1 QCD + ideal leptons/photons','Plus ideal charm and bottom']
for kind,color,label in zip(KINDS,colors,labels):
    rows=runs[kind]['rows'];T=[x['T_GeV'] for x in rows]
    for axes,key in zip(ax,['g_s','Tkin_over_T','heavy_fraction']):axes.plot(T,[x[key] for x in rows],label=label,color=color,lw=2)
for axes,title,ylabel in zip(ax,['A  Entropy degrees of freedom','B  Kinetic-temperature sensitivity','C  Species-fraction sensitivity'],['Entropy g*s','Scalar Tkin / bath T','Heavy scalar number fraction']):
    axes.set(xlim=(.5,1/3),xlabel='Bath temperature (GeV)',ylabel=ylabel,title=title);axes.grid(True,alpha=.8);axes.set_axisbelow(True)
ax[0].legend(frameon=False,fontsize=8,loc='lower left')
fig.suptitle('Changing the expansion background changes the free-bath solution',y=.96,fontsize=15,fontweight='bold',color='#203b64')
fig.text(.5,.045,'Entropy-conserving expansion · same ideal collision kernels · initial zero-mu MB state · EOS central-fit sensitivity, not QCD-matched kinetics',ha='center',fontsize=9,color='#526273')
fig.savefig(D/'eos_sensitivity.png',dpi=180);fig.savefig(D/'eos_sensitivity.svg');plt.close(fig)
lines='\n'.join(f"{x['eos']:32s} {x['initial_g_rho']:8.4f} {x['final_g_rho']:8.4f} {x['initial_g_s']:8.4f} {x['final_g_s']:8.4f} {x['final_a']:8.5f} {x['final_Tkin_over_T']:10.7f} {x['final_heavy_fraction']:10.7f} {x['net_number_loss_ppm']:9.4f}" for x in r['summary'])
note=f'''ENTROPY-CONSISTENT EOS SENSITIVITY WITH FROZEN FREE-BATH KINETICS
21 October 2026

RESULT AND SCOPE

Replacing the prescribed constant g*=g*s=60 radiation background with a stated
lattice-QCD-based equation of state changes the final kinetic-temperature ratio
from 0.75027 to 0.72220. A separately labeled addition of ideal charm and bottom
thermodynamics changes it to 0.70567. The collision kernels, portal parameters,
initial zero-mu MB scalar preparation and 0.5 -> 1/3 GeV window remain exactly
the same. Entropy conservation, temperature-time conversion and the changing
p/T coordinate are all included. This isolates dependence on the background;
it is not a QCD-matched kinetic calculation or a physical relic prediction.

SOURCE AND COMPLETE EOS PRESCRIPTION

The QCD sector uses the 2+1-flavor central trace-anomaly fit in Borsanyi et al.,
arXiv:1309.5258v2, Eq. (2), Table 1:

  J(T) = (rho_QCD-3p_QCD)/T^4
       = exp(-h1/t-h2/t^2) [h0 + f0*(tanh(f1*t+f2)+1)/(1+g1*t+g2*t^2)].

The coefficients are h0=0.1396, h1=-0.1800, h2=0.0350, f0=1.05, f1=6.39,
f2=-4.72, g1=-0.92 and g2=0.57. The dimensionless variable is t=T/(0.2 GeV).
The pressure follows the explicitly published integration prescription in the
earlier source arXiv:1007.2580v2, Eqs. (3.1)-(3.2):

  P(T)=p_QCD/T^4=integral_0^T J(T') dT'/T'.
  rho_QCD/T^4=3P+J,     s_QCD/T^3=4P+J.

Thus no free radiation-like pressure constant is introduced.
{table_validation_text}

Background QCD+leptons+photons adds a two-polarization photon gas; ideal Fermi-Dirac
e+/-, mu+/-, tau+/- gases using the benchmark masses; and three massless neutrino
species, with both particle and antiparticle and the same temperature. The charged
leptons have degeneracy 4 each and neutrinos have total degeneracy 6. Massive
FD moments are integrated explicitly. The source's ideal MB collision treatment
is not changed by these equilibrium-background choices.

The second variation adds ideal FD charm and bottom gases, each with degeneracy
12 and masses 1.3 and 4.2 GeV. The 2+1-flavor lattice EOS does not contain these
heavy flavors. This addition exposes a background-model choice rather than
claiming to be an interacting 2+1+1 or full Standard Model EOS. The two variations
are not asserted to bracket the true EOS or its uncertainty.

ENTROPY, TIME AND MOMENTUM NORMALIZATION

At zero chemical potential, s=(rho+p)/T. We set a(T0)=1 and impose

  a(T)=[s(T0)/s(T)]^(1/3),     a^3*s=constant,
  H(T)=sqrt(8*pi*rho/3)/M_Pl,  M_Pl=1.2209e19 GeV,
  eta=ln(T0/T),               dt/deta=kappa/H,
  kappa=[T*(ds/dT)]/(3*s)=1+(1/3)*d ln(g*s)/d ln(T).

The last derivative is computed from the analytic trace-anomaly derivative and
the ideal-gas integrals. For FD gases, T ds/dT=d rho/dT, with the derivative
evaluated directly from f(1-f). The entropy derivative is cross-checked by finite
differences; the maximum kappa difference is below 5.1e-10. Increasing FD
quadrature from 64 to 128 nodes changes its moments by at most 1.2e-8 relatively.

The cell population remains M=a^3*n_cell/n_ref with n_ref=n_eq,total(T0). The
unchanged collision banks tabulate the original conductances divided by H60.
Their new generator is therefore multiplied by H60/H_new times kappa. The pair
coefficient becomes alpha=n_ref/(a^3*H_new)*kappa; its bath equilibrium source is
E=a^3*n_eq,total(T)/n_ref times the instantaneous cell probabilities. Inverse
creation is still fixed by the bath; it is never adjusted to fit scalar abundance.

When g*s varies, y=p/T is not comoving. Free redshift transports it by

  y_new/y_old = [g*s(T_new)/g*s(T_old)]^(1/3).

The solver applies positive conservative momentum-cell overlap remaps around
each midpoint collision step. Each cell uses the original conditional MB closure;
the infinite tail is retained. The small temperature steps ensure that a cell
overlaps at most its own bin and its lower neighbor. Number is transferred, not
clipped or renormalized. Omitting this transport would not be an entropy-consistent
EOS change. In the constant-60 limit the remap becomes the identity, kappa=1,
and the original result is recovered exactly at all reported comparison endpoints.

ENDPOINT COMPARISON

EOS                              g_rho0   g_rhof   g_s0     g_sf       a_f      Tkin/T      heavy r  loss ppm
{lines}

The kinetic-temperature shifts relative to the fixed background are about 3.7%
and 5.9%. The final heavy fractions decrease by about 0.00192 and 0.00196. Pair
annihilation still changes number only by tens of ppm in this z=1 preparation.
Yield columns in the machine-readable output use each background's own initial
entropy density; a change of that normalization is not itself extra annihilation.

NUMERICAL CHECKS AND THEIR LIMITS

The maximum absolute comoving-number discrepancy in one redshift remap is
{checks['max_remap_count_error']:.3g}; in a number-conserving collision step it is
{checks['max_linear_count_error']:.3g}. The maximum saved a^3*s/s0 discrepancy is
{checks['max_entropy_relative_error']:.3g}. All populations remain nonnegative.

With 192 finite cells per species, changing 192 to 384 nominal temperature steps
changes final Tkin/T by 6.7e-7 for QCD+leptons+photons and 1.5e-6 with ideal c/b.
Changing 192 to 96 cells changes it by 0.00058 and 0.00074, respectively. Those
cell changes are much smaller than the 0.0281 and 0.0446 background-induced shifts.

A separate continuum integral evolves the initial MB distribution by the exact
p=p_initial/a(T) law without collisions. It predicts final Tkin/T=0.67289758 and
0.65438558 for the two backgrounds. The remapped 192-cell collisionless solutions
differ from those values by 0.000456 and 0.000653; errors increase to 0.001109 and
0.001510 on 96 cells. This makes the finite-cell transport approximation visible.
The reported last digits are computational values; these tests are empirical
sensitivities, not certified continuum-error bounds. The original reaction-bank
quadrature and interpolation uncertainties also remain inherited.

The EOS parameter covariance has not been propagated, and no temperature-dependent
interacting scalar-current spectral function, hadronic scattering kernel, thermal
mass, or QCD-matched inverse channel has been supplied. The exercise establishes
that expansion thermodynamics matters within the finite window, while retaining
a declared mismatch between interacting bulk EOS and ideal collision physics.
No earlier thermal history or reheating calculation is implied.

REPRODUCTION

From the parent thermal directory:

  OPENBLAS_NUM_THREADS=1 python eos_sensitivity.py
  python make_eos_report.py

Runtime for the completed suite was {r['elapsed_seconds']:.2f} seconds. The analytic EOS
and kinetic calculations require no network access with the delivered frozen
collision banks. Only the optional table comparison requires its separately
retrieved source file. eos_sensitivity_results.json, eos_review_summary.json, eos_summary.csv
and individual trajectories contain all numerical comparisons. The source URLs are:

https://arxiv.org/pdf/1309.5258v2
https://arxiv.org/pdf/1007.2580v2
https://arxiv.org/src/1309.5258v2/anc/WB-EoS.dat
'''
(D/'EOS_NOTE.txt').write_text(note)
print('Wrote EOS note, PNG/SVG, review summary.')
