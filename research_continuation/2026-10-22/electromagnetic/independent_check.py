"""Independent float64/vectorized sums and bracketed root check."""
from fractions import Fraction
import json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

here=Path(__file__).parent
d=json.loads((here/'stationary_profiles_results.json').read_text())
a=np.array(list(map(float,d['nodes'])))
wm=np.array(list(map(float,d['weights_minus'])))
wp=np.array(list(map(float,d['weights_plus'])))
R=float(d['common_R'])

def allco(r):
    H=np.full(10,30.); HR=np.zeros(10); Y=np.full(10,20/3)
    for n,mult,q in [(0,12,1/3),(1,28,32/3),(2,16,4/3)]:
        ell=np.arange(1,81)
        b=a[:,None]*ell*(ell+n)
        vals=(2*ell+n)*np.exp(-b/r**2)
        H+=mult*np.sum(vals,axis=1)
        HR+=mult*np.sum(vals*(2*b/r**3),axis=1)
        Y+=q*np.sum(vals,axis=1)
    return H/a**2,HR/a**2,H/a,Y

P,PR,J,Y=allco(R)
mat=np.vstack([a**k for k in [-3,-2,-1,0,1,2]]+[P,PR,J])
mat/=np.max(np.abs(mat),axis=1)[:,None]
sv=np.linalg.svd(mat,compute_uv=False)
aug=np.vstack([mat,Y/np.max(np.abs(Y))])
results={}
for name,w in [('minus',wm),('plus',wp)]:
    def stationarity(r):
        co=allco(r)
        return np.dot(w,r*co[1]-2*co[0])
    root=brentq(stationarity,1.25,1.30,xtol=1e-14)
    results[name]={
        'bracketed_80_level_root':float(root),
        'gY_inverse_squared_per_kappa':float(np.dot(w,allco(root)[3])/(6*np.pi**2)),
    }
scale=sum(Fraction(1,i*i) for i in range(1,11))/sum(Fraction(1,i) for i in range(1,11))
results.update({
    'exact_node_scale':str(scale),
    'scaled_constraint_singular_values':sv.tolist(),
    'scaled_constraint_condition':float(sv[0]/sv[-1]),
    'augmented_determinant':float(np.linalg.det(aug)),
    'augmented_smallest_singular_value':float(np.linalg.svd(aug,compute_uv=False)[-1]),
    'constraint_scaled_pair_difference':float(np.max(np.abs(mat@(wp-wm)))),
    'caveat':'Independent finite numerical diagnostics; not interval-certified rank or root proof.',
})
(here/'independent_check_results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
