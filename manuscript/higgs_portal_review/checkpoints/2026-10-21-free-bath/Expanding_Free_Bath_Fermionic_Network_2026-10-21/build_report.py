"""Build the expanding-bath result summary and scientific comparison figure."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import tempfile

os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'expanding_free_bath_mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'solver'))
from expanding_free_bath import collisionless_exact


def main():
    full=json.loads((HERE/'results/full_final.json').read_text())
    convergence=json.loads((HERE/'results/convergence_summary.json').read_text())
    rates=json.loads((HERE/'network/reaction_rates.json').read_text())
    rows=full['rows']
    selected=[r for r in rows if 'comoving_cell_masses' in r]
    table=[]
    for row in selected:
        entry={k:v for k,v in row.items() if k!='comoving_cell_masses'}
        entry['number_loss_ppm']=1e6*(1-entry['comoving_number_relative_to_initial'])
        entry['collisionless_continuum']=collisionless_exact(row['T_GeV'])
        table.append(entry)
    summary={
        'title':'Expanding free-bath evolution with a leading-portal-order fermionic network',
        'prepared_date':'2026-10-21',
        'initial_state':'f_i(y, T0)=exp[-sqrt(m_i^2+(T0*y)^2)/T0], T0=0.5 GeV; zero chemical potentials',
        'background':'gstar=gstar_s=60 prescribed constant; a0=1; T*a=T0; radiation H(T) inherited',
        'temperature_window_GeV':[.5,1/3],
        'elapsed_H_T0_times_t':.625,'elapsed_H_T0p4_times_t':.4,
        'evolved_channels':full['channels'],
        'kinetic_temperature_definition':'Tkin=P_scalar/n_scalar = <p^2/(3E)>; a moment diagnostic, not an imposed thermal fit',
        'initial_number_density_GeV3':full['initial_number_density_GeV3'],
        'initial_yield_Y':full['initial_yield_Y'],
        'timelike_higgs_width_GeV':rates['timelike_Higgs_width_GeV'],
        'width_is_new_declared_input':True,
        'new_assumed_entropy_dof':60,
        'total_free_fermion_phi2_width_GeV':rates['vacuum_phi2_total_free_fermion_width_GeV'],
        'selected_snapshots':table,
        'final_refinement_sensitivities':convergence['refinements'],
        'refinement_changes_are_certified_errors':False,
        'numerical_controls':convergence['checks'],
        'not_computed':['interacting QCD response','general scalar self-interaction sector',
                        'loop-induced gluonic channels','early-time preparation before T0',
                        'physical relic abundance','apparatus response'],
        'gap_scope':'Previous zero-gap theorem applies to its fixed-bath scattering operator; no spectral-gap theorem is asserted here for the nonlinear time-dependent system',
    }
    report=HERE/'report';report.mkdir(exist_ok=True)
    (report/'comparison_summary.json').write_text(json.dumps(summary,indent=2)+'\n')

    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11.5,
                         'axes.titlesize':13,'axes.labelsize':11.5,
                         'axes.spines.top':False,'axes.spines.right':False,
                         'figure.facecolor':'white','savefig.facecolor':'white'})
    fig,axes=plt.subplots(2,2,figsize=(13.8,9.7))
    fig.subplots_adjust(left=.08,right=.97,bottom=.18,top=.80,wspace=.25,hspace=.40)
    fig.text(.08,.94,'Expanding free-bath evolution',fontsize=23,weight='bold',color='#16283f')
    fig.text(.08,.895,r'$T: 0.5\ \to\ 1/3$ GeV  |  Initial zero-chemical-potential MB state  |  $g_*=g_{*s}=60$',fontsize=13,color='#4b5f73')
    fig.text(.08,.853,'Momentum-resolved scattering, annihilation / inverse production, and heavy decay / inverse absorption',fontsize=11.5,color='#4b5f73')
    a=np.array([r['scale_factor'] for r in rows])
    temperature=np.array([r['T_GeV'] for r in rows])
    free=[collisionless_exact(T) for T in temperature]
    blue='#1764a3';orange='#c36521';green='#138576';purple='#8061a9';gray='#788693'
    ax=axes[0,0]
    ax.plot(a,[r['Tkin_over_T'] for r in rows],lw=2.6,color=blue,label='Evolved fermionic network')
    ax.plot(a,[r['Tkin_over_T'] for r in free],lw=2,ls='--',color=orange,label='Collisionless continuum')
    ax.axhline(1,color=green,lw=1.6,ls=':',label='Instantaneous MB value')
    ax.set_ylim(.68,1.035);ax.set_ylabel(r'$T_{\rm kin}/T=\langle p^2/(3E)\rangle/T$')
    ax.set_title('A  Scattering partly offsets redshift cooling',loc='left',pad=11)
    ax.legend(loc='lower left',fontsize=9,frameon=False)
    ax=axes[0,1]
    ax.plot(a,[100*r['heavy_fraction'] for r in rows],lw=2.6,color=blue,label='Evolved fermionic network')
    ax.plot(a,[100*r['heavy_fraction'] for r in free],lw=2,ls='--',color=orange,label='Collisionless population')
    ax.plot(a,[100*r['instantaneous_eq_heavy_fraction'] for r in rows],lw=1.9,ls=':',color=green,label='Instantaneous equilibrium mixture')
    ax.set_ylim(1,6.15);ax.set_ylabel('Heavy-species population (%)')
    ax.set_title('B  Species conversion lags the changing bath',loc='left',pad=11)
    ax.legend(loc='lower left',fontsize=9,frameon=False)
    ax=axes[1,0]
    ax.plot(a,[1e6*(1-r['comoving_number_relative_to_initial']) for r in rows],color=blue,lw=2.6)
    ax.axhline(0,color=gray,ls=':',lw=1.6)
    ax.set_ylim(-.7,35)
    ax.set_ylabel(r'Comoving number loss $(1-a^3 n/n_0)\times10^6$')
    ax.set_title('C  Net annihilation removes about 31.5 ppm',loc='left',pad=11)
    ax.text(.04,.82,'Scattering and decay alone conserve\ntotal comoving scalar number.',transform=ax.transAxes,fontsize=10,color='#4b5f73')
    ax=axes[1,1]
    ax.plot(a,[100*r['total_variation_to_common_fugacity_MB'] for r in rows],color=purple,lw=2.4,label='Common-fugacity MB mixture')
    ax.plot(a,[100*r['total_variation_to_same_species_MB'] for r in rows],color=blue,lw=2.4,ls='--',label='MB shapes at actual species fractions')
    ax.set_ylim(-.3,17.5);ax.set_ylabel('Total-variation distance (%)')
    ax.set_title('D  Momentum shapes also depart from equilibrium',loc='left',pad=11)
    ax.legend(loc='upper left',fontsize=9,frameon=False)
    for ax in axes.ravel():
        ax.set_xlim(1,1.5);ax.set_xlabel(r'Scale factor $a/a_0=T_0/T$')
        ax.grid(axis='y',color='#dfe5eb',lw=.75);ax.set_axisbelow(True)
    fig.text(.08,.105,'Conditional benchmark: fixed ideal free-fermion bath model and prescribed radiation history; no physical relic-abundance prediction.',fontsize=10.6,color='#3a5068')
    fig.text(.08,.067,'192 finite comoving-momentum cells plus a semi-infinite tail per species. Final refinement changes: 0.035% in Tkin/T and 0.279% in heavy fraction.',fontsize=10.2,color='#4b5f73')
    fig.text(.08,.032,'Refinement changes are empirical sensitivities, not certified errors. The initial absolute density is specified; number-changing results depend on it.',fontsize=10.2,color='#4b5f73')
    target=report/'Expanding_Free_Bath_Fermionic_Network_2026-10-21.png'
    fig.savefig(target,dpi=185);plt.close(fig)
    print('Wrote',target.name,'and comparison_summary.json')


if __name__=='__main__':main()
