"""Regenerate the scientific figure and typeset tables from results.json."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('VECLIB_MAXIMUM_THREADS','1')
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import vacuum as v

HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'results.json').read_text())
c=json.loads((HERE/'checks.json').read_text())
previous=json.loads((HERE/'inputs/previous_scalar_results.json').read_text())
out=HERE/'images';out.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold'})
fig,axes=plt.subplots(1,2,figsize=(10.2,3.6),layout='constrained')
hs=np.linspace(0,4.5,75);p0=v.spectral([v.RSTAR,0,0],order=0)[0]
ps=np.array([v.spectral([v.RSTAR,h,h],order=0)[0]-p0 for h in hs])
s=previous['scalar_profiles']['minus']
poly=4*np.pi**2*(28*s['A2']*hs**2+(28*s['A4']+12*s['C0'])*hs**4)
axes[0].plot(hs,ps,color='#137F8C',lw=2.3,label='Full finite-field trace')
axes[0].plot(hs,poly,color='#B86738',lw=1.8,ls='--',label='Quartic Taylor polynomial')
axes[0].set(xlabel=r'Equal amplitudes $h_d=h_u=h$',ylabel=r'$W(R_*,h,h)-W(R_*,0,0)$',title='Scalar polynomial versus full action')
axes[0].axhline(0,color='#AAB2B8',lw=.6);axes[0].legend(frameon=False,fontsize=9)
controls=r['runaway']['finite_radius_controls'];rs=[d['R'] for d in controls]
ys=[d['P_over_R2']-v.CSTAR for d in controls]
axes[1].plot(rs,ys,'o-',color='#18384E',lw=1.6,label='Finite-mode evaluation')
limit=r['runaway']['W_over_R2_limit_h2']
axes[1].axhline(limit,color='#B86738',ls='--',label='Analytic large-radius limit')
axes[1].set(xlabel=r'Radius $R$',ylabel=r'$W(R,2,2)/R^2$',title='Negative asymptotic direction')
axes[1].legend(frameon=False,fontsize=9,loc='lower right')
for ax in axes:ax.grid(alpha=.16)
fig.savefig(out/'untuned_action.pdf',metadata={'CreationDate':None,'ModDate':None})
fig.savefig(out/'untuned_action.png',dpi=190)
plt.close(fig)

def sci(x,digits=4):
    if x==0:return '0'
    mant,exp=f'{x:.{digits}e}'.split('e')
    return mant+r'\times10^{'+str(int(exp))+'}'

def table(name,columns,header,rows):
    return '\\newcommand{\\'+name+'}{%\n\\begin{tabular}{@{}'+columns+'@{}}\\toprule\n'+header+r'\\\midrule'+'\n'+'\n'.join(row+r'\\' for row in rows)+'\n\\bottomrule\\end{tabular}}\n'

rows=[]
for eps,key in [('10^{-2}','0.01'),('10^{-4}','0.0001')]:
    for label in ['minus','plus']:
        d=r['tuned_flat_fixtures'][key]['profiles'][label];x=d['x']
        rows.append('$f_'+('-' if label=='minus' else '+')+'$ & $'+eps+'$ & '+f'{x[0]:.11f} & {x[1]:.9f} & {x[2]:.9f} & {d["radial_Schur_complement"]:.8f}')
tex=table('VacuumTable','lrrrrr',r'Profile & $\varepsilon$ & $R$ & $h_d$ & $h_u$ & $K_{\rm rel}$',rows)
# Split the long eigenvalue lists over dedicated rows to keep them legible.
rows=[]
for name,field,index in [('Smallest radial/amplitude eigenvalue','Hessian_eigenvalues',0),
                         ('Second radial/amplitude eigenvalue','Hessian_eigenvalues',1),
                         ('Largest radial/amplitude eigenvalue','Hessian_eigenvalues',2),
                         ('Charged eigenvalue (twice)','charged_Cartesian_eigenvalue_twice',None),
                         ('Smallest scalar kinetic eigenvalue','scalar_metric_eigenvalues',0),
                         ('Smallest neutral kinetic eigenvalue','neutral_kinetic_eigenvalues',0)]:
    vals=[]
    for key in ['0.01','0.0001']:
        val=r['tuned_flat_fixtures'][key]['profiles']['minus'][field]
        vals.append(val if index is None else val[index])
    rows.append(name+' & $'+sci(vals[0],5)+'$ & $'+sci(vals[1],5)+'$')
tex+=table('StabilityTable','lrr',r'Quantity in the stated coordinates & $\varepsilon=10^{-2}$ & $\varepsilon=10^{-4}$',rows)
rows=[]
for title,key,index in [(r'$\Delta R$','x',0),(r'$\Delta h_d$','x',1),(r'$\Delta h_u$','x',2),(r'$\Delta c$','c',None),
                         (r'$\Delta(e^{-2}/\kappa)$','photon_inverse_squared_over_kappa',None)]:
    vals=[]
    for eps in ['0.01','0.0001']:
        d=r['tuned_flat_fixtures'][eps]['plus_minus'][key]
        vals.append(d if index is None else d[index])
    rows.append(title+' & $'+sci(vals[0],3)+'$ & $'+sci(vals[1],3)+'$')
tex+=table('DifferenceTable','lrr',r'Difference $f_+-f_-$ & $\varepsilon=10^{-2}$ & $\varepsilon=10^{-4}$',rows)
tex+='\\newcommand{\\SchurLimit}{'+f'{r["tuning"]["Schur_limit"]:.10f}'+'}\n'
tex+='\\newcommand{\\EpsilonCross}{'+sci(r['near_critical_phase_split']['epsilon_cross_plus'],7)+'}\n'
tex+='\\newcommand{\\CheckCount}{'+str(c['passed'])+'/'+str(c['total'])+'}\n'
(HERE/'tables.tex').write_text(tex)
print('Scientific figure and tables regenerated.')
