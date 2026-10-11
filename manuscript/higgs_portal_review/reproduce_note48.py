"""Reproduce Note48 candidate assembly and finite-convention audit.

Run without arguments for central pair calculations; --full adds scale and
node comparisons. No external data, network connection or parameter fit.
"""
import argparse,json
import decay_assembly_audit as a
import heavy_quark_thermal as h

def run_case(scale=1.,scheme='MSbar',angular_n=24,thermal_n=24,method='laguerre'):
    raw={p:a.thermal_candidate(pair=p,scale=scale,scheme=scheme,
         angular_n=angular_n,thermal_n=thermal_n,method=method) for p in h.PAIRS}
    weights=h.equilibrium_weights(.5)
    eff=sum(weights[p]*raw[p] for p in h.PAIRS)
    def render(x):
        return {part:{**dict(zip(a.LABELS,map(float,x[i]))),
                'bc_square':float(x[i,1]+x[i,2]+x[i,5])} for i,part in enumerate(a.PARTS)}
    return {'scale':scale,'scheme':scheme,'angular_nodes':angular_n,'thermal_nodes':thermal_n,
        'method':method,'pairs_GeV_minus2':{p:render(x) for p,x in raw.items()},
        'conditional_effective_GeV_minus2':render(eff)}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true')
    parser.add_argument('--output',default='RESULTS_NOTE_48.json')
    args=parser.parse_args()
    cases=[('central',{})]
    if args.full:
        cases += [('fine',{'angular_n':32,'thermal_n':32}),
             ('mu_half',{'scale':.5}),('mu_double',{'scale':2.}),
             ('pole1',{'scheme':'pole1'}),
             ('Q_check',{'angular_n':24,'thermal_n':48,'method':'Q'})]
    out={'scope':'Finite-convention candidate assembly and closure diagnostic; not certified full NLO.',
       'temperature_GeV':.5,'chemical_equilibrium_established':False,
       'source_erratum_confirmed':False,'complete_physical_NLO_claimed':False,
       'source_normalization_review_open':True,'Omnes_data_acquired':False,
       'cases':{},'closure_checks':[]}
    for label,kwargs in cases:
        out['cases'][label]=run_case(**kwargs)
        with open(args.output,'w') as f:json.dump(out,f,indent=2,allow_nan=False)
        print('completed',label,flush=True)
    for Q,scale,scheme in [(20.,1.,'MSbar'),(23.,1.,'MSbar'),(40.,1.,'MSbar'),
            (65.,1.,'MSbar'),(20.,.5,'MSbar'),(20.,2.,'MSbar'),(23.,1.,'pole1')]:
        out['closure_checks'].append(a.diagnostic(Q,scale,scheme))
    with open(args.output,'w') as f:json.dump(out,f,indent=2,allow_nan=False)
