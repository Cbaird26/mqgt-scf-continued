"""Entropy-consistent EOS sensitivity with unchanged ideal-bath collision banks.

QCD EOS: Borsanyi et al. arXiv:1309.5258v2 Eq.(2), Table 1, together with
t=T/(200 MeV) and pressure integration arXiv:1007.2580v2 Eqs.(3.1)-(3.2).
This is a controlled mixed-model expansion exercise, not QCD-matched kinetics.
"""
from __future__ import annotations
import csv,functools,hashlib,json,math,os,time
from pathlib import Path
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from scipy.integrate import quad
from scipy.special import roots_laguerre,roots_legendre
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply
from run_continuation import ROOT,OUT,T0,TF,NREF,MASS,banks,initialize,cell_data,neq,hubble,observables,positive_step

PARAMETERS=dict(h0=.1396,h1=-.1800,h2=.0350,f0=1.05,f1=6.39,f2=-4.72,g1=-.92,g2=.57)
EOSDIR=ROOT/'eos';EOSDIR.mkdir(exist_ok=True)
EOS_TABLE_URL='https://arxiv.org/src/1309.5258v2/anc/WB-EoS.dat'
EOS_TABLE_SHA256='5f39782b65fcadf36a84c84afc57855cf7d20bc1f0b96f9d28c51737916b9550'
LAG_X,LAG_W=roots_laguerre(64)
LEG_X,LEG_W=roots_legendre(16)

def interaction_measure(T):
    if T==0:return 0.,0.
    t=T/.2;p=PARAMETERS
    E=math.exp(-p['h1']/t-p['h2']/t**2)
    v=math.tanh(p['f1']*t+p['f2']);D=1+p['g1']*t+p['g2']*t*t
    J=E*(p['h0']+p['f0']*(v+1)/D)
    dJ=J*(p['h1']/t+2*p['h2']/t**2)+E*p['f0']*(p['f1']*t*(1-v*v)/D-(v+1)*t*(p['g1']+2*p['g2']*t)/D**2)
    return J,dJ

@functools.lru_cache(maxsize=None)
def qcd_eos(T):
    # The fit itself specifies the low-T completion of this integral. It is not
    # a separate invented pressure integration constant.
    P,error=quad(lambda x:interaction_measure(x)[0]/x,0,T,epsabs=1e-11,epsrel=1e-11,limit=150)
    J,dJ=interaction_measure(T);R=3*P+J;S=4*P+J;C=3*S+4*J+dJ
    return P,R,S,C,error

def fd_moments(T,m,g,order=64):
    y,w=(LAG_X,LAG_W) if order==64 else roots_laguerre(order)
    E=np.sqrt(y*y+(m/T)**2);f=np.exp(-E)/(1+np.exp(-E))
    fw=np.exp(y-E)/(1+np.exp(-E))*w
    P=g/(6*math.pi**2)*np.dot(fw,y**4/E)
    R=g/(2*math.pi**2)*np.dot(fw,y*y*E)
    C=g/(2*math.pi**2)*np.dot(fw,y*y*E*E*(1-f))
    return np.array([P,R,P+R,C])

@functools.lru_cache(maxsize=None)
def eos(T,kind='qcd_leptons_photon'):
    if kind=='constant60':
        R=math.pi**2/30*60;P=R/3;S=4*R/3;C=3*S
    else:
        P,R,S,C,_=qcd_eos(T)
        # Photons: g=2; three thermally coupled massless neutrino species: g=6.
        extra_R=math.pi**2/30*(2+7/8*6)
        extra=np.array([extra_R/3,extra_R,4*extra_R/3,4*extra_R])
        for m in [.00051099895,.1056583755,1.77686]:extra+=fd_moments(T,m,4)
        if kind=='qcd_leptons_photon_ideal_cb':
            for m in [1.3,4.2]:extra+=fd_moments(T,m,12)
        P,R,S,C=np.array([P,R,S,C])+extra
    return dict(T_GeV=T,p_GeV4=P*T**4,rho_GeV4=R*T**4,s_GeV3=S*T**3,
                g_rho=30*R/math.pi**2,g_s=45*S/(2*math.pi**2),
                dln_a_dln_inverse_T=C/(3*S),sound_speed_squared=S/C,
                H_GeV=math.sqrt(8*math.pi/3*R)*T*T/1.2209e19)

def scale_factor(T,kind):
    return (eos(T0,kind)['s_GeV3']/eos(T,kind)['s_GeV3'])**(1/3)

def remap(M,T,edges,factor):
    """Positive conservative leftward redshift remap in y=p/T.

    Each cell uses its inherited instantaneous MB conditional shape. For these
    small steps it overlaps its original cell and its immediate lower neighbor.
    The exact infinite-cell probability is used in the normalization. This is
    finite-volume closure, not an exact continuum distribution reconstruction.
    """
    if abs(factor-1)<1e-13:return M.copy()
    if not 0<factor<1:raise ValueError('This leftward remap requires declining g_s')
    nb=len(edges)-1
    if np.any(factor*edges[1:-1]<edges[:-2]-1e-14):raise ValueError('Remap crosses more than one cell; refine eta grid')
    lo=edges[1:-1];hi=lo/factor
    yy=(lo[:,None]+hi[:,None])/2+(hi-lo)[:,None]/2*LEG_X
    ww=(hi-lo)[:,None]/2*LEG_W
    pi=cell_data(T,edges)[:,:,0]
    from scipy.special import kve
    norm=sum(m*m*T*kve(2,m/T)*math.exp(-(m-MASS[0])/T)/(2*math.pi**2) for m in MASS)
    fractions=[]
    for i,m in enumerate(MASS):
        p=T*yy;kin=p*p/(np.sqrt(m*m+p*p)+m)
        w=T**3*yy*yy*np.exp(-(kin+m-MASS[0])/T)/(2*math.pi**2*norm)
        fractions.append((ww*w).sum(axis=1)/pi[i,1:])
    fraction=np.array(fractions)
    if fraction.min()<0 or fraction.max()>1+1e-12:raise ValueError('Invalid remap probability')
    original=M.reshape(2,nb);result=original.copy()
    transferred=original[:,1:]*fraction
    result[:,:-1]+=transferred;result[:,1:]-=transferred
    return result.ravel()

def record(M,T,edges,kind):
    r=observables(M,T,edges);bg=eos(T,kind);a=scale_factor(T,kind)
    N=r.pop('comoving_number_relative_to_initial')
    r['comoving_number_over_actual_initial']=N
    r['physical_number_GeV3']=N*NREF/a**3;r['scale_factor']=a
    r['instantaneous_eq_number_over_reference']=a**3*neq(T)/NREF
    r.pop('instantaneous_eq_total_number_relative_to_initial')
    r['yield_Y_total']=N*NREF/eos(T0,kind)['s_GeV3']
    r['rho_scalar_over_background']=r['physical_number_GeV3']*r['mean_total_energy_GeV']/bg['rho_GeV4']
    r.update({k:bg[k] for k in ['g_rho','g_s','H_GeV','dln_a_dln_inverse_T']})
    r['entropy_comoving_over_initial']=a**3*bg['s_GeV3']/eos(T0,kind)['s_GeV3']
    return r

def run(kind,steps=192,aggregation=1,collisions=True):
    scatter,reactions=banks(aggregation)
    grid=np.unique(np.r_[np.linspace(0,math.log(T0/TF),steps+1),np.log(T0/np.array([T0,.45,.4,.375,TF]))])
    M=initialize(dict(z=1.,theta=1.,heavy_fraction=None),scatter.edges)
    minimum=float(M.min());remap_error=0.;linear_error=0.;rows=[]
    for k,eta in enumerate(grid):
        T=T0*math.exp(-eta)
        if k%4==0 or k==len(grid)-1:rows.append(record(M,T,scatter.edges,kind))
        if k==len(grid)-1:break
        dt=grid[k+1]-eta;mid=eta+dt/2;Tm=T0*math.exp(-mid);Tnext=T0*math.exp(-grid[k+1])
        # Free expansion changes y even though the inherited grid uses fixed y.
        ratio=(eos(Tm,kind)['g_s']/eos(T,kind)['g_s'])**(1/3)
        before=M.sum();M=remap(M,T,scatter.edges,ratio);remap_error=max(remap_error,abs(M.sum()-before))
        if collisions:
            a=scale_factor(Tm,kind);bg=eos(Tm,kind)
            pi=cell_data(Tm,scatter.edges)[:,:,0].ravel();eq=a**3*neq(Tm)/NREF*pi
            kappa=bg['dln_a_dln_inverse_T'];alpha=NREF/a**3/bg['H_GeV']*kappa
            A=reactions.kernel(mid)
            W=(scatter.conductance(mid)+reactions.decay_conductance(mid))*hubble(Tm)/bg['H_GeV']*kappa
            Q=W.copy();np.fill_diagonal(Q,-W.sum(axis=1));Q/=pi[None,:]
            M=positive_step(M,dt/2,A,eq,alpha)
            before=M.sum();M=expm_multiply(csr_matrix(Q*dt),M,traceA=float(np.trace(Q)*dt));linear_error=max(linear_error,abs(M.sum()-before))
            M=positive_step(M,dt/2,A,eq,alpha)
        ratio=(eos(Tnext,kind)['g_s']/eos(Tm,kind)['g_s'])**(1/3)
        before=M.sum();M=remap(M,Tm,scatter.edges,ratio);remap_error=max(remap_error,abs(M.sum()-before))
        minimum=min(minimum,float(M.min()))
        if M.min()<0 or not np.isfinite(M).all():raise ValueError('Invalid cell population')
    return dict(eos=kind,steps=steps,finite_cells_per_species=len(scatter.edges)-2,collisions=collisions,
                max_remap_number_error=remap_error,max_linear_step_number_error=linear_error,
                minimum_cell_population=minimum,final_cell_masses=M.reshape(2,-1).tolist(),rows=rows)

def continuum_collisionless(kind):
    """Independent continuum redshift using p(Tf)=p_initial/a(Tf)."""
    a=scale_factor(TF,kind);values=[]
    for m in MASS:
        def integrand(x,k):
            E0=m+T0*x;p0=math.sqrt(T0*x*(2*m+T0*x));p=p0/a;E=math.sqrt(m*m+p*p)
            w=p0*E0*T0*math.exp(-m/T0-x)/(2*math.pi**2*NREF)
            return w*[1.,E,p*p/(3*E*TF)][k]
        values.append([quad(integrand,0,np.inf,args=(k,),epsabs=1e-12,epsrel=2e-11)[0] for k in range(3)])
    values=np.array(values)
    return dict(scale_factor=a,Tkin_over_T=float(values[:,2].sum()),heavy_fraction=float(values[1,0]),
                mean_energy_GeV=float(values[:,1].sum()),comoving_number=float(values[:,0].sum()))

def validate_eos():
    # This ancillary table is an optional validation input, never an input to
    # the fitted EOS or kinetic evolution. Public packages retain its URL/hash
    # and the original validation record but do not redistribute the raw file.
    table_path=EOSDIR/'WB-EoS.dat';checks=[]
    table_status='skipped_missing_optional_source'
    if table_path.is_file():
        if hashlib.sha256(table_path.read_bytes()).hexdigest()!=EOS_TABLE_SHA256:
            raise ValueError('EOS validation table does not match the pinned SHA-256')
        table=np.atleast_2d(np.loadtxt(table_path))
        if table.shape[1]!=11 or not np.isfinite(table).all():
            raise ValueError('Unexpected EOS validation table shape or values')
        for row in table:
            T=row[0]/1000
            if not TF<=T<=T0:continue
            P,R,S,C,error=qcd_eos(T);J=interaction_measure(T)[0]
            checks.append(dict(T_GeV=T,fit_I_over_T4=J,table_I_over_T4=row[1],table_I_error=row[2],
                               fit_P_over_T4=P,table_P_over_T4=row[3],table_P_error=row[4],
                               fit_rho_over_T4=R,table_rho_over_T4=row[5],table_rho_error=row[6],
                               fit_s_over_T3=S,table_s_over_T3=row[7],table_s_error=row[8],
                               fit_cs2=S/C,table_cs2=row[9]))
        if not checks:raise ValueError('EOS validation table has no points in the solved interval')
        table_status='performed_this_run'
    derivative=[];fdcheck=[]
    for T in [TF,.4,T0]:
        for kind in ['qcd_leptons_photon','qcd_leptons_photon_ideal_cb']:
            bg=eos(T,kind);eps=1e-5
            sp=eos(T*math.exp(eps),kind)['s_GeV3'];sm=eos(T*math.exp(-eps),kind)['s_GeV3']
            kp=(math.log(sp)-math.log(sm))/(6*eps)
            derivative.append(dict(T_GeV=T,eos=kind,analytic_kappa=bg['dln_a_dln_inverse_T'],finite_difference_kappa=kp,absolute_difference=abs(kp-bg['dln_a_dln_inverse_T'])))
        for mass,g in [(.00051099895,4),(.1056583755,4),(1.77686,4),(1.3,12),(4.2,12)]:
            low=fd_moments(T,mass,g);high=fd_moments(T,mass,g,128)
            fdcheck.append(dict(T_GeV=T,mass_GeV=mass,max_relative_64_vs128=float(np.max(abs(low-high)/high))))
    return dict(table_validation_status=table_status,table_source_url=EOS_TABLE_URL,
                table_source_sha256=EOS_TABLE_SHA256,
                table_validation_note=('Optional comparison only; omitted raw source can be retrieved explicitly with '
                                       'thermal/fetch_eos_validation_table.py. No automatic download is performed. '
                                       'Historical results are in thermal/eos/historical_table_validation.json.'),
                table_checks=checks,derivative_checks=derivative,FD_quadrature_checks=fdcheck,
                max_table_pressure_deviation_in_quoted_errors=(max(abs(x['fit_P_over_T4']-x['table_P_over_T4'])/x['table_P_error'] for x in checks) if checks else None),
                max_table_energy_deviation_in_quoted_errors=(max(abs(x['fit_rho_over_T4']-x['table_rho_over_T4'])/x['table_rho_error'] for x in checks) if checks else None))

def main():
    started=time.perf_counter();runs={};valid=validate_eos()
    for kind in ['constant60','qcd_leptons_photon','qcd_leptons_photon_ideal_cb']:
        for label,steps,aggregation,collisions in [('standard',192,1,True),('time384',384,1,True),('grid96',192,2,True),('collisionless',192,1,False),('collisionless96',192,2,False)]:
            if kind=='constant60' and label not in ['standard','collisionless']:continue
            result=run(kind,steps,aggregation,collisions);runs[kind+'_'+label]=result
            (EOSDIR/(kind+'_'+label+'.json')).write_text(json.dumps(result,indent=2)+'\n')
            print(kind,label,{k:result['rows'][-1][k] for k in ['Tkin_over_T','heavy_fraction','comoving_number_over_actual_initial','scale_factor']},flush=True)
    frozen=json.loads((OUT/'reproduced_baseline.json').read_text())['rows'][-1]
    constant=runs['constant60_standard']['rows'][-1]
    valid['constant60_baseline_differences']={k:abs(constant[k]-frozen[k]) for k in ['Tkin_over_T','heavy_fraction','total_variation_to_same_species_MB']}
    valid['collisionless_continuum']={kind:continuum_collisionless(kind) for kind in ['constant60','qcd_leptons_photon','qcd_leptons_photon_ideal_cb']}
    valid['collisionless_grid_errors']={kind:{label:abs(runs[kind+'_'+label]['rows'][-1]['Tkin_over_T']-valid['collisionless_continuum'][kind]['Tkin_over_T']) for label in ['collisionless','collisionless96']} for kind in ['qcd_leptons_photon','qcd_leptons_photon_ideal_cb']}
    summary=[]
    for kind in ['constant60','qcd_leptons_photon','qcd_leptons_photon_ideal_cb']:
        row=runs[kind+'_standard']['rows'][-1]
        summary.append(dict(eos=kind,initial_g_rho=eos(T0,kind)['g_rho'],final_g_rho=row['g_rho'],initial_g_s=eos(T0,kind)['g_s'],final_g_s=row['g_s'],
                            final_a=row['scale_factor'],final_Tkin_over_T=row['Tkin_over_T'],final_heavy_fraction=row['heavy_fraction'],
                            final_number_over_initial=row['comoving_number_over_actual_initial'],net_number_loss_ppm=1e6*(1-row['comoving_number_over_actual_initial']),final_yield=row['yield_Y_total']))
    with (EOSDIR/'eos_summary.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)
    result=dict(parameters_2014=PARAMETERS,parameter_source='https://arxiv.org/pdf/1309.5258v2 Eq.(2), Table 1',
                temperature_and_pressure_prescription_source='https://arxiv.org/pdf/1007.2580v2 Eqs.(3.1)-(3.2)',
                data_table='https://arxiv.org/src/1309.5258v2/anc/WB-EoS.dat',
                EOS_additions='Ideal photon + e/mu/tau Fermi-Dirac gases + 3 massless coupled neutrino species; second variation adds ideal c,b gases using inherited vacuum masses',
                entropy_prescription='a(T)=[s(T0)/s(T)]^(1/3), eta=ln(T0/T), dt/deta=[T ds/dT]/[3 H s]',
                momentum_remap='y=p/T changes by [g_s(Tnext)/g_s(T)]^(1/3); conservative positive MB-cell overlap remap',
                scope='Expansion/EOS sensitivity only; unchanged ideal free-bath collision kernels; no QCD-matched rates, no prehistory or physical relic',
                validation=valid,summary=summary,elapsed_seconds=time.perf_counter()-started,
                error_status='Empirical time/grid/continuum-redshift comparisons; EOS central fit only, no lattice covariance propagation')
    (EOSDIR/'eos_sensitivity_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)
    print('Elapsed',result['elapsed_seconds'],flush=True)

if __name__=='__main__':main()
