"""Build the research figure and LaTeX tables from results.json."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'results.json').read_text())
(ROOT/'images').mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,
                     'axes.spines.right':False,'pdf.fonttype':42})
fig,ax=plt.subplots(1,2,figsize=(7.1,2.55),layout='constrained')
scan=r['radius_scan'];rad=[v['R'] for v in scan]
ax[0].plot(rad,[v['mass_squared_exact'] for v in scan],color='#137f8c',lw=2,label='Internal mode sum')
ax[0].plot(rad,[v['mass_squared_local'] for v in scan],color='#63758a',ls='--',label=r'Local $a_2$--$a_4$')
ax[0].axhline(0,color='#c4cbd1',lw=.7)
ax[0].axvline(r['R_star'],color='#a8b6c1',ls=':',lw=1)
ax[0].set(xlabel=r'$R=\Lambda r$',ylabel=r'$m_H^2/\Lambda^2$',xlim=(.3,3),ylim=(-2.3,7.5),title='A  Quadratic scalar mass parameter')
ax[0].legend(frameon=False,fontsize=8,loc='upper right')
names=['A2','G','A4','C0','C1'];vals=[r['scalar_profiles']['minus'][x]/r['local_a2_a4'][x] for x in names]
ax[1].bar(range(5),vals,color=['#137f8c','#4d98a1','#18384e','#527189','#8197a9'],width=.63)
ax[1].axhline(1,color='#8d9aa5',ls='--',lw=1)
ax[1].set_xticks(range(5),[r'$A_2$',r'$G$',r'$A_4$',r'$C_0$',r'$C_1$'])
ax[1].set(ylabel='Exact / local coefficient',ylim=(0,1.4),title=r'B  Finite-radius change at $R_*$')
for i,v in enumerate(vals):ax[1].text(i,v+.035,f'{v:.3f}',ha='center',fontsize=8)
fig.savefig(ROOT/'images/scalar_response.pdf')
fig.savefig(ROOT/'images/scalar_response.png',dpi=220)
plt.close(fig)

def num(v,d=8):
    a,b=f'{v:.{d}e}'.split('e')
    return a+r'\times10^{'+str(int(b))+'}'

def matrix(M,dec=8):
    return r'\begin{pmatrix}'+r'\\'.join(' & '.join(f'{x:.{dec}f}' for x in row) for row in M)+r'\end{pmatrix}'

lines=[r'\newcommand{\ScalarTable}{\begin{tabular}{@{}lrrr@{}}\toprule',
       r'Coefficient & Local $a_2$--$a_4$ & Exact $f_-$ & $f_+-f_-$\\\midrule']
labels={'A2':r'$A_2$','G':r'$G$','A4':r'$A_4$','C0':r'$C_0$','C1':r'$C_1$'}
for n in names:
    lines.append(labels[n]+' & $'+num(r['local_a2_a4'][n],6)+'$ & $'+num(r['scalar_profiles']['minus'][n],9)+'$ & $'+num(r['scalar_profiles']['difference'][n],5)+r'$\\')
lines.append(r'\bottomrule\end{tabular}}')
for key,macro in [('down','DownMatrix'),('up','UpMatrix')]:
    lines.append('\\newcommand{\\'+macro+'}{'+matrix(r['higgs_shift_profiles']['minus'][key]['matrix'])+'}')
    val=r['higgs_shift_profiles']['minus'][key]['photon_projection']
    delta=r['higgs_shift_profiles']['difference'][key]['photon_projection']
    lines.append('\\newcommand{\\'+key.title()+'Photon}{'+f'{val:.11f}'+'}')
    lines.append('\\newcommand{\\'+key.title()+'PhotonDelta}{'+num(delta,5)+'}')
lines.append(r'\newcommand{\FixtureK}{'+matrix(r['finite_background_fixture']['K_over_kappa_minus'],9)+'}')
lines.append(r'\newcommand{\FixtureMass}{'+matrix(np.array(r['finite_background_fixture']['mass_over_kappa_Lambda2_minus'])*1e4,7)+'}')
(ROOT/'tables.tex').write_text('\n'.join(lines)+'\n')
print('Built images/scalar_response.pdf, PNG, and tables.tex')
