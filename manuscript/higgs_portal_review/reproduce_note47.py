"""Regenerate Note47 numerical output; default runs six prescriptions/checks.
An argument such as central restricts output to that one calculation.
"""
from pathlib import Path
import json,time,sys
import three_gluon_remainder as r
import heavy_quark_thermal as h
out=Path('RESULTS_NOTE_47_REGENERATED.json')
data={'date':'2026-10-10','scope':'Finite coherent b/c-loop three-gluon real remainder with independently reconstructed soft normalization; not a complete NLO rate.',
      'T_GeV':.5,'finite_window_w':[0,90],'inherited_head':'1abb5e2769dc77657ed6080e2c0c2ce1e0d77cbf',
      'chemical_equilibrium_established':False,'full_coherent_NLO_computed':False,
      'normalization_note':'Printed source (C.14) fails its heavy/collinear limit. Amplitude (C.7) retained; common prefactor 1/2 derived independently.',
      'runs':{}}
# New result file is written incrementally; no historical results are loaded.
start=time.time()
configs=[('central',1.,'MSbar',32,24,'laguerre'),('fine',1.,'MSbar',48,32,'laguerre'),
         ('independent_Q',1.,'MSbar',32,48,'Q'),('mu_half',.5,'MSbar',32,24,'laguerre'),
         ('mu_double',2.,'MSbar',32,24,'laguerre'),('pole1',1.,'pole1',32,24,'laguerre')]
if len(sys.argv)>1:configs=[c for c in configs if c[0] in sys.argv[1:]]
for label,scale,scheme,an,tn,method in configs:
 if label in data['runs'] and 'conditional_effective_GeV_minus2' in data['runs'][label]:continue
 channels=data['runs'].get(label,{}).get('pair_components_GeV_minus2',{})
 for p in h.PAIRS:
  if p in channels:continue
  v=r.thermal_components(.5,p,scale,scheme,an,tn,method)
  channels[p]=dict(zip(r.COMPONENTS,map(float,v)))
  print(label,p,channels[p],time.time()-start,flush=True)
  data['runs'][label]={'pair_components_GeV_minus2':channels}
  out.write_text(json.dumps(data,indent=2)+'\n')
 weights=h.equilibrium_weights(.5)
 data['runs'][label]={'scale':scale,'scheme':scheme,'angular_n':an,'thermal_n':tn,'method':method,
   'pair_components_GeV_minus2':channels,
   'conditional_effective_GeV_minus2':{c:sum(weights[p]*channels[p][c] for p in h.PAIRS) for c in r.COMPONENTS}}
 out.write_text(json.dumps(data,indent=2)+'\n')
