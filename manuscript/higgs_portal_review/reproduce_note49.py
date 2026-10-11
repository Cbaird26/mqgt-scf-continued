"""Regenerate the independent virtual source audit; no full real/virtual rerun."""
from __future__ import annotations
import json,math
import numpy as np
import abdv_virtual_check as a
import bc_virtual_finite as hk
import coherent_bc_rg as rg
import heavy_quark_thermal as h
from prove_note49 import proof

def run():
    scan=[]
    for Q in (20.,21.5,23.,40.,65.,80.):
        for scale in (.5,1.,2.):
            for scheme in ('MSbar','OS'):
                for q,mass in zip(('b','c'),a.masses(Q,scale,scheme)):
                    r=(mass/Q)**2;c=a.coefficients(r,scale,scheme)
                    F,D=rg.form_and_mass_derivative(r)
                    old=hk.hk_product(r)+(2*math.log(scale*scale/r)*D if scheme=='MSbar' else -(8/3)*D)
                    matched=old+(8/3)*D
                    scan.append({'Q_GeV':Q,'mu_over_Q':scale,'scheme':scheme,'flavor':q,
                      'G_ABDV':[c['G'].real,c['G'].imag],
                      'G_Note48_matched':[matched.real,matched.imag],
                      'matched_absolute_difference':abs(c['G']-matched),
                      'matched_relative_difference':abs(c['G']-matched)/max(abs(c['G']),1e-300),
                      'literal_absolute_difference':abs(c['G']-old)})
    pairs={p:{co:a.thermal(.5,p,component=co)[0] for co in ('bb','cc','bc','coherent')} for p in h.PAIRS}
    w=h.equilibrium_weights(.5)
    eff={co:sum(w[p]*pairs[p][co] for p in h.PAIRS) for co in ('bb','cc','bc','coherent')}
    comparison={p:abs(a.thermal(.5,p)[0]-a.thermal(.5,p,method='Q')[0]) for p in h.PAIRS}
    scopes={'full_real_plus_virtual_rate_rerun':False,'independent_real_normalization_check':False,
            'external_HDECAY_or_HIGLU_run':False,'chemical_equilibrium_established':False,
            'empirical_validation':False,'relic_abundance_computed':False}
    return {'note':49,'research_date':'2026-10-10','third_source':'hep-ph/0611266v3',
      'symbolic':proof(),'scan':scan,'scan_count':len(scan),
      'max_matched_absolute_difference':max(p['matched_absolute_difference'] for p in scan),
      'max_matched_relative_difference':max(p['matched_relative_difference'] for p in scan),
      'max_literal_absolute_difference':max(p['literal_absolute_difference'] for p in scan),
      'temperature_GeV':.5,'window_w':[0.,90.],
      'pair_finite_virtual_GeV_minus2':pairs,'equilibrium_weights_ASSUMED':w,
      'conditional_effective_virtual_GeV_minus2':eff,
      'Q_vs_w_absolute_difference_GeV_minus2':comparison,
      'scope':'Third-source mass-dependent finite virtual numerator only, not full NLO decay',**scopes}

if __name__=='__main__':print(json.dumps(run(),indent=2))
