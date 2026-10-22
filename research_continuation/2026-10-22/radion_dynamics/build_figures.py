"""Build manuscript tables and scientific figure from recorded results."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'results.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
navy='#18384e';teal='#137f8c';orange='#ba632e'
p=r['branches']['0.01']['profiles']['minus']
fig,ax=plt.subplots(1,2,figsize=(10.5,3.7),layout='constrained')
ax[0].barh([1,0],[p['Jordan_metric'][0][0],p['Einstein_metric'][0][0]],color=[orange,teal],height=.45)
ax[0].axvline(0,color='#555555',lw=.8)
ax[0].set_yticks([1,0],['Jordan $G_{RR}$','Einstein $G^E_{RR}$'])
ax[0].set_xlim(-.40,.44);ax[0].set_xlabel('Dimensionless coefficient, fixed scalar coordinates')
ax[0].set_title(r'(a) Gravitational mixing changes the sign',loc='left',fontsize=11)
for y,val in zip([1,0],[p['Jordan_metric'][0][0],p['Einstein_metric'][0][0]]):
    ax[0].text(val/2,y,f'{val:.6f}',ha='center',va='center',fontsize=10,color='white',fontweight='bold')
eps=np.array([.0001,.01])
for index,label,color,marker in [(4,'Charged pair',teal,'s'),(6,'Neutral light',navy,'o'),(7,'Neutral heavy','#6892ab','^'),(8,'Radion dominated',orange,'D')]:
    vals=[r['branches'][str(e)]['profiles']['minus']['squared_mass_parameters_over_Lambda2'][index] for e in eps]
    ax[1].loglog(eps,vals,marker=marker,color=color,label=label,lw=1.5)
ax[1].set_xlabel(r'Chosen tuning $\epsilon$');ax[1].set_ylabel(r'Two-derivative parameter $m^2/\Lambda^2$')
ax[1].set_title('(b) The radion remains near the cutoff',loc='left',fontsize=11)
ax[1].set_xlim(7e-5,.014);ax[1].set_ylim(5e-5,1.6);ax[1].grid(axis='y',alpha=.18)
ax[1].legend(loc='center left',fontsize=8,frameon=False)
(HERE/'images').mkdir(exist_ok=True)
fig.savefig(HERE/'images/kinetics_and_scales.pdf',metadata={'CreationDate':None,'ModDate':None})
fig.savefig(HERE/'images/kinetics_and_scales.png',dpi=180)
plt.close(fig)

def matrix(a,fmt='.7f'):
    return r'\begin{pmatrix}'+r'\\'.join(' & '.join(format(v,fmt) for v in row) for row in a)+r'\end{pmatrix}'

rows=[]
for eps,case in r['branches'].items():
    for pr,p in case['profiles'].items():
        mm=p['squared_mass_parameters_over_Lambda2']
        rows.append(f"${eps}$ & $f_{{{'-' if pr=='minus' else '+'}}}$ & {p['f']:.9f} & {p['Einstein_metric'][0][0]:.9f} & {mm[4]:.8g} & {mm[6]:.8g} & {mm[7]:.8g} & {mm[8]:.8g} \\")
        rows[-1]+='\\'
table=r'\begin{tabular}{llrrrrrr}\toprule $\epsilon$ & Profile & $f$ & $G^E_{RR}$ & $m_C^2$ & $m_1^2$ & $m_2^2$ & $m_r^2$\\\midrule'+'\n'+'\n'.join(rows)+r'\bottomrule\end{tabular}'
p=r['branches']['0.01']['profiles']['minus']
text='\\newcommand{\\BranchTable}{'+table+'}\n'
text+='\\newcommand{\\JordanMatrix}{'+matrix(np.array(p['Jordan_metric'])[:3,:3])+'}\n'
text+='\\newcommand{\\EinsteinMatrix}{'+matrix(np.array(p['Einstein_metric'])[:3,:3])+'}\n'
text+='\\newcommand{\\PhaseMatrix}{'+matrix(np.array(p['Einstein_metric'])[3:5,3:5])+'}\n'
text+='\\newcommand{\\ChargedMatrix}{'+matrix(np.array(p['Einstein_metric'])[5:7,5:7])+'}\n'
(HERE/'tables.tex').write_text(text)
print('Figure and generated tables written.')
