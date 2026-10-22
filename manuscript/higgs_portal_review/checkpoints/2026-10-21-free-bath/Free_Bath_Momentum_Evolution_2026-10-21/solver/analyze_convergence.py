"""Evaluate graph/grid/quadrature/tail sensitivity with frozen initial data.

Refinement differences are empirical numerical sensitivities, not certified
continuum errors or statistical confidence intervals.
"""
from pathlib import Path
import json
import numpy as np
from radial_free_bath import evolution,aggregate_graph

HERE=Path(__file__).resolve().parent
TIMES=[.25,.5,1.,2.,5.]

def load(name):return json.loads((HERE/name).read_text())

def collapse(source,tail_start,width):
    n=source['finite_bins_per_species']; fine_width=source['tail_start_x']/n
    bins=int(round(tail_start/width));factor=int(round(width/fine_width))
    assert abs(factor*fine_width-width)<1e-12
    assert abs(bins*width-tail_start)<1e-12
    assert tail_start<=source['tail_start_x']
    P=np.zeros((2*(n+1),2*(bins+1)))
    for i in range(2):
        for a in range(n):P[i*(n+1)+a,i*(bins+1)+min(a//factor,bins)]=1
        P[(i+1)*(n+1)-1,(i+1)*(bins+1)-1]=1
    D=P.T@np.array(source['D_per_N_GeV'])@P
    data=(P.T@np.array(source['cell_moments']).reshape(-1,3)).reshape(2,bins+1,3)
    return D,data

def compact(record):
    result={'number_null_relative_residual':record['number_null_relative_residual'],
            'symmetry_relative_residual':record['symmetry_relative_residual'],
            'metric_total':record['metric_total'],
            'tail_equilibrium_mass':record['metric_tail_mass'],
            'count_only_rate_over_H':record['count_only_rate_over_H'],
            'finite_graph_lowest_positive_rate_over_H':record['positive_eigenvalues_over_H'][0],
            'initial_conditions':{}}
    for ic in ['population','temperature']:
        source=record['initial_conditions'][ic]
        rows=[next(row for row in source['rows'] if abs(row['tau_Ht']-t)<1e-9) for t in TIMES]
        result['initial_conditions'][ic]={
            'initial_shape_variance':source['initial_shape_variance'],
            'continuum_initial_shape_variance':source['continuum_initial_shape_variance'],
            'initial_variance_retained_fraction':source['initial_variance_retained_fraction'],
            'tau_Ht':TIMES,
            'correlation':[row['autocorrelation_relative_to_initial'] for row in rows],
            'correlation_divided_by_continuum_variance':[row['autocorrelation_divided_by_continuum_variance'] for row in rows],
            'L2_squared_norm_ratio':[row['chi2_relative_to_initial'] for row in rows],
            'max_absolute_number_error':max(abs(row['total_number_relative_error']) for row in source['rows']),
            'minimum_relative_occupation':min(row['minimum_relative_occupation'] for row in source['rows']),
        }
    return result

def checks(D,data,record):
    metric=data[:,:,0].ravel()
    assert np.all(metric>0)
    assert abs(metric.sum()-1)<1e-12
    assert np.max(D-np.diag(np.diag(D)))<=0
    assert record['number_null_relative_residual']<1e-13
    assert abs(record['smallest_eigenvalue_over_H'])<1e-10
    assert min(record['positive_eigenvalues_over_H'])>0
    for source in record['initial_conditions'].values():
        rows=source['rows']; cor=np.array([r['autocorrelation_relative_to_initial'] for r in rows])
        assert np.max(np.diff(cor))<1e-12
        assert min(r['minimum_relative_occupation'] for r in rows)>0
        assert max(abs(r['total_number_relative_error']) for r in rows)<1e-12
        for tau in [.25,.5,1,2]:
            a=next(r for r in rows if abs(r['tau_Ht']-tau)<1e-9)
            b=next(r for r in rows if abs(r['tau_Ht']-2*tau)<1e-9)
            assert abs(a['chi2_relative_to_initial']-b['autocorrelation_relative_to_initial'])<1e-12

def analyze():
    summaries={};final=None
    names=['res32_bins128.json','res48_bins128.json','res64_bins128.json','res80_bins192_tail24.json']
    for name in names:
        source=load(name);tag=str(source['resolution']['q']);summaries[tag]={}
        for n in [32,64,128]:
            D,data=collapse(source,16.,16./n)
            out=evolution(D,data,.4);checks(D,data,out)
            summaries[tag][str(n)]=compact(out)
            if tag=='80' and n==128:
                final={'T_GeV':.4,'model':source['model'],'source_graph':name,
                       'resolution':source['resolution'],'finite_bins_per_species':128,
                       'tail_start_x':16.,'edges_x':np.r_[np.linspace(0,16,129),np.nan].tolist(),
                       'D_per_N_GeV':D.tolist(),'cell_moments':data.tolist(),
                       'evolution':out,'full_gap_certified':False,'expanding_background_evolved':False}
                final['edges_x'][-1]=None
        coarse=summaries[tag]['32']['finite_graph_lowest_positive_rate_over_H']
        medium=summaries[tag]['64']['finite_graph_lowest_positive_rate_over_H']
        fine=summaries[tag]['128']['finite_graph_lowest_positive_rate_over_H']
        assert fine<=medium<=coarse
    last=load(names[-1]);tails={}
    for L in [12.,16.,20.,24.]:
        D,data=collapse(last,L,.125)
        result=evolution(D,data,.4);checks(D,data,result)
        tails[str(int(L))]=compact(result)
    diffs={}
    for desc,a,b in [('quadrature_48_to_64',summaries['48']['128'],summaries['64']['128']),
                     ('quadrature_64_to_80',summaries['64']['128'],summaries['80']['128']),
                     ('grid_32_to_64',summaries['80']['32'],summaries['80']['64']),
                     ('grid_64_to_128',summaries['80']['64'],summaries['80']['128']),
                     ('tail_12_to_16',tails['12'],tails['16']),
                     ('tail_16_to_24',tails['16'],tails['24'])]:
        diffs[desc]={}
        for ic in ['population','temperature']:
            x=np.array(a['initial_conditions'][ic]['correlation']);y=np.array(b['initial_conditions'][ic]['correlation'])
            diffs[desc][ic]={'tau_Ht':TIMES,'absolute_change':(y-x).tolist(),'relative_change':((y-x)/y).tolist()}
    result={'T_GeV':.4,'quadrature_and_grid':summaries,'tail_bin_start_sensitivity':tails,
            'refinement_changes':diffs,'all_invariants_passed':True,
            'refinement_changes_are_certified_error_bounds':False,'full_gap_certified':False}
    (HERE/'convergence_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'final_evolution.json').write_text(json.dumps(final,indent=2)+'\n')
    print(json.dumps(diffs,indent=2))

if __name__=='__main__':analyze()
