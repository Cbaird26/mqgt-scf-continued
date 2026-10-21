"""Read-only independent numerical review of the root measurement fits."""
from pathlib import Path
import json,math,csv
import numpy as np
from scipy.optimize import minimize
from scipy.special import xlogy
ROOT=Path(__file__).resolve().parent
M=ROOT.parent/'measurement'
results=json.loads((M/'measurement_results.json').read_text())
with (M/'scan_poisson_fits.csv').open() as f:records=list(csv.DictReader(f))
diffs=[];joint=0.;pearson=0.;nbin=0;total=0;weakstatus=0
for rec in records:
    path=M/'sources'/'pedalino_original'/'Na-Cluster-Interference'/'Na-Cluster'/'Data_April2025'/'22042025'/'Interference Scans'/(rec['name']+'_s1.dat')
    dat=np.loadtxt(path);y=dat[:,1];a=2*np.pi*dat[:,0]/133
    X=np.column_stack([np.ones(len(y)),np.cos(a),np.sin(a)])*y.mean()
    norm=float(y.sum())
    def f(b):
        mu=X@b
        if np.any(mu<=0):return np.inf
        return np.sum(mu-y+xlogy(y,y/mu))/norm
    def jac(b):
        mu=X@b
        return X.T@(1-y/mu)/norm
    def hess(b):
        mu=X@b
        return X.T@((y/mu**2)[:,None]*X)/norm
    # A generic independent trust-region implementation, starting at zero contrast.
    solved=minimize(f,[1.,0.,0.],jac=jac,hess=hess,method='trust-exact',options={'gtol':2e-9,'maxiter':200})
    if not solved.success:weakstatus+=1
    b=solved.x;mu=X@b;dev=2*f(b)*norm;V=np.linalg.norm(b[1:])/b[0]
    if np.any(mu<=0):raise ValueError('Negative fitted mean')
    joint+=dev;pearson+=np.sum((y-mu)**2/mu);nbin+=len(y);total+=int(y.sum())
    diffs.append(dict(name=rec['name'],visibility_difference=abs(V-float(rec['visibility_poisson'])),
                      deviance_difference=abs(dev-float(rec['deviance'])),
                      normalized_gradient_infinity_norm=float(np.max(np.abs(jac(b)))),
                      all_phase_positivity_margin=float(b[0]-np.linalg.norm(b[1:])),
                      optimizer_success=bool(solved.success),optimizer_message=solved.message))
out=dict(n_scans=len(records),n_bins=nbin,total_counts=total,joint_deviance=joint,
         joint_pearson_dispersion=pearson/(nbin-3*len(records)),
         max_visibility_difference=max(x['visibility_difference'] for x in diffs),
         max_per_scan_deviance_difference=max(x['deviance_difference'] for x in diffs),
         max_normalized_gradient=max(x['normalized_gradient_infinity_norm'] for x in diffs),
         minimum_all_phase_positivity_margin=min(x['all_phase_positivity_margin'] for x in diffs),
         generic_optimizer_non_success_statuses=weakstatus,
         scope='Independent trust-exact optimizer on convex per-bin-positive Poisson mean model; interior solution also satisfies the root all-phase-positive cone; no root files modified.',
         identifiability_review='The analytic shared-A/shared-chi invariance is correct when the attenuation is a multiplicative normalization. The empirical ridge uses free per-scan amplitudes; it demonstrates that nuisance model, not validation of a particular global quantum baseline shape. A physical A<=1 can truncate a ridge and may give a bound with a known baseline, but does not identify a unique mechanism.',
         residual_review='Large dispersion rejects adequacy of this combined sinusoidal-independent-Poisson working model. It does not by itself identify non-Poisson counting noise; omitted mean structure, drift, correlation and calibration can contribute.',
         scans=diffs)
(ROOT/'results'/'independent_measurement_review.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='scans'},indent=2))
