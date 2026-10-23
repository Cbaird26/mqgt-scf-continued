from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
R=json.loads((HERE/'results.json').read_text());C=json.loads((HERE/'checks.json').read_text())
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'font.family':'DejaVu Sans','pdf.fonttype':42})
fig,ax=plt.subplots(1,2,figsize=(10,3.7),layout='constrained')
p=R['branches']['0.01']['profiles']['minus'];zt=p['tensor_nonzero_real_poles'][0]['z']
ax[0].plot(R['plot_data']['z'],R['plot_data']['tensor_A_over_f'],color='#18384e',lw=2)
ax[0].axhline(0,color='#777777',lw=.8);ax[0].axvspan(zt,20,color='#ba3f3f',alpha=.10)
ax[0].scatter([zt],[0],color='#ba3f3f',zorder=3)
ax[0].annotate(f'Tensor zero: {zt:.4f}',(zt,0),(6,.22),arrowprops={'arrowstyle':'->','color':'#555555'},fontsize=9)
ax[0].set(xlabel=r'$z=p_E^2/\Lambda^2$',ylabel=r'$\mathsf{a}(z)/f$',title='Tensor response on the Euclidean axis',xlim=(0,20),ylim=(-.2,1.05))
ax[0].grid(alpha=.15)
for sector,marker,col,label in [('tensor','x','#18384e','Tensor zeros'),('coupled','o','#b43e43','Coupled neutral zeros')]:
    zz=[complex(*e['z']) for e in R['complex_poles_representative_fixture'][sector]['upper_half_plane_roots']]
    zz=zz+[z.conjugate() for z in zz]
    zz+=([complex(zt)] if sector=='tensor' else [complex(e['z']) for e in p['scalar_real_poles']])
    if marker=='o':ax[1].scatter([z.real for z in zz],[z.imag for z in zz],marker=marker,s=27,facecolors='none',edgecolors=col,lw=.9,label=label)
    else:ax[1].scatter([z.real for z in zz],[z.imag for z in zz],marker=marker,s=31,color=col,lw=1.2,label=label)
ax[1].axvline(0,color='#999999',lw=.6);ax[1].axhline(0,color='#999999',lw=.6)
ax[1].set(xlabel=r'$\mathrm{Re}\,z$',ylabel=r'$\mathrm{Im}\,z$',title='Nonzero poles: representative fixture',xlim=(-7,12),ylim=(-21,21))
ax[1].legend(loc='upper right',frameon=False,fontsize=8);ax[1].grid(alpha=.15)
(HERE/'images').mkdir(exist_ok=True)
fig.savefig(HERE/'images/finite_momentum_poles.pdf',metadata={'CreationDate':None,'ModDate':None})
fig.savefig(HERE/'images/finite_momentum_poles.png',dpi=180)
plt.close(fig)

def fmt(x):
    if abs(x)<.001 and x!=0:
        a,b=f'{x:.7e}'.split('e');return '$'+a+r'\times10^{'+str(int(b))+'}$'
    return '$'+f'{x:.9f}'+ '$'

def table(cols,head,rows):
    return r'\begin{tabular}{'+cols+'}\n'+r'\toprule '+head+r'\\\midrule'+'\n'+'\n'.join(' & '.join(r)+r'\\' for r in rows)+'\n'+r'\bottomrule\end{tabular}'
rows=[];tach=[];count=[]
for eps,b in R['branches'].items():
    for prof,p in b['profiles'].items():
        poles=sorted([q for q in p['scalar_real_poles'] if q['z']<0],key=lambda q:-q['z'])
        label='$f_-$' if prof=='minus' else '$f_+$'
        rows.append(['$'+eps+'$',label]+[fmt(-q['z']) for q in poles])
        s=[q for q in p['scalar_real_poles'] if q['z']>0][0];t=p['tensor_nonzero_real_poles'][0]
        tach.append(['$'+eps+'$',label,fmt(t['z']),fmt(s['z'])])
        count.append(['$'+eps+'$',label,str(p['complex_counts']['tensor']['fine']['rounded_count']),str(p['complex_counts']['coupled']['fine']['rounded_count'])])
macros={'TimelikeTable':table('llrrrr',r'$\epsilon$ & profile & $s_1$ & $s_2$ & $s_r$ & $s_{\rm extra}$',rows),
        'TachyonTable':table('llrr',r'$\epsilon$ & profile & $z_T$ & $z_S$',tach),
        'CountTable':table('llrr',r'$\epsilon$ & profile & tensor zeros & coupled zeros',count)}
p=R['branches']['0.01']['profiles']['minus'];rr=[]
for q in sorted(p['scalar_real_poles'],key=lambda q:-q['z']):
    rr.append([fmt(-q['z']),fmt(q['relative_residue']),'positive' if q['residue_sign']>0 else 'negative'])
macros['ResidueTable']=table('rrl',r'$s=-z$ & $Z$ & residue sign',rr)
macros['CheckCount']=str(C['total'])
allp=[p for b in R['branches'].values() for p in b['profiles'].values()]
def sci(x):
    a,b=f'{x:.1e}'.split('e');return '$'+a+r'\times10^{'+str(int(b))+'}$'
for macro,key in [('RealResidueError','max_scalar_residue_inverse_error'),('CutoffError','max_cutoff_kernel_relative_error'),('QuadratureError','max_quadrature_kernel_relative_error'),('PoleShift','max_scalar_pole_cutoff_shift')]:macros[macro]=sci(max(p[key] for p in allp))
macros['ComplexShift']=sci(max(p['shift'] for p in R['controls']['complex_pole_refinement']))
macros['ComplexResidueError']=sci(R['controls']['complex_residue_inverse_max_error'])
(HERE/'tables.tex').write_text('\n'.join('\\newcommand{\\'+k+'}{'+v+'}' for k,v in macros.items())+'\n')
print('Generated figure and numerical LaTeX tables from sealed results.')
