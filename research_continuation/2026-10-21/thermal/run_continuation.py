"""Initial-abundance and preparation sensitivity of the frozen free-bath network.

This imports the unmodified, pinned collision-bank and integrator implementation.
It changes only scalar initial conditions, preserving the bath equilibrium inverse
source and normalization n_ref=n_eq,total(T0). It is a finite-window benchmark,
not a physical relic calculation or an interacting-QCD calculation.
"""
from __future__ import annotations
import csv,hashlib,json,math,os,platform,sys,time
from pathlib import Path
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'frozen'/'network'))
sys.path.insert(0,str(ROOT/'frozen'/'solver'))
import numpy as np
import scipy
from scipy.integrate import quad,solve_ivp
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply
from scipy.special import kve
from expanding_free_bath import ScatteringBank,cell_data,hubble,neq,observables,T0,TF,MASS,collisionless_exact
from evolve_network import ReactionBank,evolve as frozen_evolve
from pair_annihilation import positive_step

OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
SCATTER=ROOT/'frozen'/'solver'/'bank_q48_eta16.npz'
PAIR=ROOT/'frozen'/'network'/'pair_bank_eta16.npz'
DECAY=ROOT/'frozen'/'network'/'decay_bank_eta16.npz'
CASES=[dict(id=f'z_{z:g}',z=z,theta=1.,heavy_fraction=None) for z in [1e-6,1e-4,.01,.1,1.,10.,100.,1e4]]
CASES += [dict(id=f'kinetic_{t:g}',z=1.,theta=t,heavy_fraction=None) for t in [.75,1.25]]
CASES += [dict(id=f'heavy_{r:g}',z=1.,theta=1.,heavy_fraction=r) for r in [0.,.25]]
NREF=neq(T0);S0=2*math.pi**2/45*60*T0**3

def save(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')

def banks(aggregation=1,temperature_stride=1,coarse_quad=False):
    scatter=ScatteringBank(ROOT/'frozen'/'solver'/'bank_q40.npz' if coarse_quad else SCATTER,
                           aggregation,1 if coarse_quad else temperature_stride)
    reactions=ReactionBank(PAIR,DECAY,scatter.edges,temperature_stride)
    return scatter,reactions

def initialize(case,edges):
    """Integrate exactly specified normalized MB preparations into y=p/T0 cells.

    z changes total abundance only. theta changes each species' momentum shape
    while its initial species fraction stays at T0 equilibrium, unless overridden.
    For theta!=1 or overridden species fractions there is no common fugacity.
    """
    base=cell_data(T0,edges)[:,:,0]
    fractions=base.sum(axis=1)
    if case['heavy_fraction'] is not None:
        fractions=np.array([1-case['heavy_fraction'],case['heavy_fraction']])
    shaped=cell_data(T0*case['theta'],edges/case['theta'])[:,:,0]
    shaped=shaped/shaped.sum(axis=1)[:,None]*fractions[:,None]
    # Do not renormalize later during evolution; this defines the initial condition.
    return case['z']*shaped.ravel()

def terms(eta,scatter,reactions):
    T=T0*math.exp(-eta);a=math.exp(eta)
    pi=cell_data(T,scatter.edges)[:,:,0].ravel()
    eq=a**3*neq(T)/NREF*pi
    alpha=NREF/a**3/hubble(T)
    A=reactions.kernel(eta)
    W=scatter.conductance(eta)+reactions.decay_conductance(eta)
    Q=W.copy();np.fill_diagonal(Q,-W.sum(axis=1));Q/=pi[None,:]
    return Q,A,eq,alpha

def record(M,T,edges,case):
    r=observables(M,T,edges)
    reference=r.pop('comoving_number_relative_to_initial')
    r['comoving_number_over_equilibrium_reference']=reference
    r['comoving_number_over_actual_initial']=reference/case['z']
    r['instantaneous_eq_number_over_equilibrium_reference']=r.pop('instantaneous_eq_total_number_relative_to_initial')
    r['yield_Y_total']=reference*NREF/S0
    rho_rad=math.pi**2/30*60*T**4
    r['rho_scalar_over_prescribed_radiation']=r['physical_number_GeV3']*r['mean_total_energy_GeV']/rho_rad
    return r

def evolve_batch(cases,steps=192,aggregation=1,temperature_stride=1,pairs=True,coarse_quad=False):
    scatter,reactions=banks(aggregation,temperature_stride,coarse_quad)
    snapshots=[T0,.45,.4,.375,TF]
    grid=np.unique(np.r_[np.linspace(0,math.log(T0/TF),steps+1),np.log(T0/np.array(snapshots))])
    M=np.column_stack([initialize(c,scatter.edges) for c in cases]);initial=M.copy()
    rows=[[] for c in cases];linear_error=0.;minimum=float(M.min())
    for k,eta in enumerate(grid):
        T=T0*math.exp(-eta)
        if k%4==0 or k==len(grid)-1 or any(abs(T-t)<1e-12 for t in snapshots):
            for j,c in enumerate(cases):rows[j].append(record(M[:,j],T,scatter.edges,c))
        if k==len(grid)-1:break
        dt=grid[k+1]-eta;mid=eta+dt/2
        Q,A,eq,alpha=terms(mid,scatter,reactions)
        if pairs:M=positive_step(M,dt/2,A,eq[:,None],alpha)
        before=M.sum(axis=0)
        M=expm_multiply(csr_matrix(Q*dt),M,traceA=float(np.trace(Q)*dt))
        linear_error=max(linear_error,float(np.max(np.abs(M.sum(axis=0)-before)/np.maximum(before,1e-300))))
        if pairs:M=positive_step(M,dt/2,A,eq[:,None],alpha)
        minimum=min(minimum,float(M.min()))
        if np.min(M)<0 or not np.isfinite(M).all():raise ValueError('Population became negative/nonfinite')
    result=dict(steps=steps,actual_steps=len(grid)-1,finite_cells_per_species=len(scatter.edges)-2,
                temperature_stride=temperature_stride,coarse_scattering_quadrature=coarse_quad,
                annihilation_and_inverse=pairs,max_relative_linear_number_error=linear_error,
                minimum_population=minimum,
                cases=[dict(initial_condition=c,rows=rows[j]) for j,c in enumerate(cases)])
    return result,initial,M,scatter.edges

def summarize(result):
    return {x['initial_condition']['id']:x['rows'][-1] for x in result['cases']}

def compare(a,b):
    aa,bb=summarize(a),summarize(b)
    keys=['comoving_number_over_actual_initial','Tkin_over_T','heavy_fraction','total_variation_to_same_species_MB']
    return {cid:{key:dict(reference=aa[cid][key],comparison=bb[cid][key],absolute_difference=abs(aa[cid][key]-bb[cid][key]),
                         relative_difference=abs(aa[cid][key]-bb[cid][key])/max(abs(aa[cid][key]),1e-300)) for key in keys} for cid in aa}

def independent_ode(cases):
    """DOP853 directly solves the unsplit coupled equation, normalized per initial z.

    Integrate separately between known bank knots to respect interpolation kinks.
    No positivity projection, renormalization, or splitting is used here.
    """
    scatter,reactions=banks();z=np.array([c['z'] for c in cases]);n=len(scatter.edges)*2-2
    state=np.column_stack([initialize(c,scatter.edges) for c in cases])/z[None,:]
    times=np.unique(np.r_[scatter.eta,reactions.eta,reactions.decay_eta]);nfev=0
    def fun(t,v):
        P=v.reshape(n,len(cases));M=P*z[None,:]
        Q,A,eq,alpha=terms(t,scatter,reactions)
        out=Q@M+alpha*(eq[:,None]*(A@eq)[:,None]-M*(A@M))
        return (out/z[None,:]).ravel()
    for left,right in zip(times[:-1],times[1:]):
        solved=solve_ivp(fun,(left,right),state.ravel(),method='DOP853',rtol=2e-10,atol=2e-13)
        if not solved.success:raise RuntimeError(solved.message)
        nfev+=solved.nfev;state=solved.y[:,-1].reshape(n,len(cases))
    M=state*z[None,:]
    return dict(method='DOP853 direct unsplit ODE; relative coordinates M/z; piecewise bank-knot intervals',
                rtol=2e-10,atol=2e-13,function_evaluations=nfev,minimum_normalized_population=float(state.min()),
                cases=[dict(initial_condition=c,rows=[record(M[:,j],TF,scatter.edges,c)]) for j,c in enumerate(cases)])

def independent_source_and_equilibrium():
    scatter,reactions=banks()
    def source(t):
        T=T0*math.exp(-t);a=math.exp(t);pi=cell_data(T,scatter.edges)[:,:,0].ravel()
        eq=a**3*neq(T)/NREF*pi;A=reactions.kernel(t);alpha=NREF/a**3/hubble(T)
        return float(alpha*eq@(A@eq))
    nodes=reactions.eta;contributions=[];errors=[]
    for a,b in zip(nodes[:-1],nodes[1:]):
        value,error=quad(source,a,b,epsabs=1e-15,epsrel=1e-10)
        contributions.append(value);errors.append(error)
    # Exact equilibrium is stationary for the fixed-temperature full operator.
    residuals=[]
    for t in [0.,math.log(T0/.4),math.log(T0/TF)]:
        Q,A,eq,alpha=terms(t,scatter,reactions)
        pair=alpha*(eq*(A@eq)-eq*(A@eq))
        scale=np.linalg.norm(Q,ord=1)*np.linalg.norm(eq,ord=1)
        residuals.append(dict(T_GeV=T0*math.exp(-t),relative_linear_stationarity=float(np.linalg.norm(Q@eq,ord=1)/scale),
                             relative_column_sum=float(np.max(np.abs(Q.sum(axis=0)))/np.max(np.abs(Q))),pair_residual=float(abs(pair).max())))
    return dict(no_loss_inverse_creation_integral_over_reference=sum(contributions),quadrature_error_estimate=sum(errors),
                expression='B=integral d_eta alpha E^T A E; N_final <= N_initial+B because annihilation is nonnegative and linear channels conserve number',
                fixed_temperature_equilibrium_residuals=residuals)

def analytic_initial_checks():
    """Continuum initial density, dilution and occupancy checks independent of cell closure."""
    species_density=np.array([m*m*T0*kve(2,m/T0)*math.exp(-m/T0)/(2*math.pi**2) for m in MASS])
    basefractions=species_density/species_density.sum();rows=[]
    for c in CASES:
        t=T0*c['theta'];r=basefractions if c['heavy_fraction'] is None else np.array([1-c['heavy_fraction'],c['heavy_fraction']])
        n=c['z']*NREF*r
        eq_t=np.array([m*m*t*kve(2,m/t)*math.exp(-m/t)/(2*math.pi**2) for m in MASS])
        # f_i(p)=n_i/n_eq,i(Ts)*exp(-E_i/Ts); occupation largest at p=0.
        occupation=n/eq_t*np.exp(-MASS/t)
        energy=np.array([m*kve(1,m/t)/kve(2,m/t)+3*t for m in MASS])
        rows.append(dict(case=c['id'],exact_initial_Tkin_over_T0=c['theta'],initial_heavy_fraction=float(r[1]),
                         maximum_phase_space_occupation=float(occupation.max()),
                         rho_scalar_over_radiation=float(n@energy/(math.pi**2/30*60*T0**4)),
                         common_mu_GeV=T0*math.log(c['z']) if c['theta']==1 and c['heavy_fraction'] is None else None))
    return rows

def main():
    start=time.perf_counter()
    baseline=frozen_evolve(SCATTER,PAIR,DECAY)
    save('reproduced_baseline.json',baseline)
    archived=json.loads((ROOT/'frozen'/'results'/'full_final.json').read_text())
    baseline_diff={k:abs(baseline['rows'][-1][k]-archived['rows'][-1][k]) for k in ['Tkin_over_T','heavy_fraction','comoving_number_relative_to_initial','total_variation_to_same_species_MB']}
    print('Frozen baseline max endpoint difference:',max(baseline_diff.values()),flush=True)
    main_result,initial,final,edges=evolve_batch(CASES)
    save('initial_condition_scan.json',main_result)
    np.savez_compressed(OUT/'initial_final_cells.npz',initial=initial,final=final,edges_y=edges,case_ids=np.array([c['id'] for c in CASES]))
    print('Main scan complete',flush=True)
    # Refinements each change one named choice; empirical sensitivities, not bounds.
    refined,_,_,_=evolve_batch(CASES,steps=384)
    coarse,_,_,_=evolve_batch(CASES,aggregation=2)
    temperature8,_,_,_=evolve_batch(CASES,temperature_stride=2)
    quad40,_,_,_=evolve_batch(CASES,temperature_stride=2,coarse_quad=True)
    save('step384.json',refined);save('grid96.json',coarse);save('temperature8.json',temperature8);save('quadrature40_temperature8.json',quad40)
    print('Step, momentum, temperature and quadrature refinements complete',flush=True)
    selected=[CASES[0],CASES[4],CASES[7],CASES[8],CASES[9],CASES[11]]
    ode=independent_ode(selected);save('independent_ode.json',ode)
    subset=dict(cases=[c for c in main_result['cases'] if c['initial_condition']['id'] in {x['id'] for x in selected}])
    # Independent mathematical limit: number-conserving operators are linear,
    # so normalized endpoint shapes must be independent of initial fugacity.
    no_pair,_,end_no_pair,_=evolve_batch(CASES[:8],pairs=False)
    normalized=end_no_pair/np.array([c['z'] for c in CASES[:8]])[None,:]
    no_pair_check=dict(max_abs_number_error=max(abs(x['rows'][-1]['comoving_number_over_actual_initial']-1) for x in no_pair['cases']),
                       max_L1_normalized_shape_difference=float(np.max(np.abs(normalized-normalized[:,4:5]).sum(axis=0))))
    save('no_pair_control.json',no_pair)
    source=independent_source_and_equilibrium();initial_checks=analytic_initial_checks()
    low=main_result['cases'][0]['rows'][-1]['comoving_number_over_equilibrium_reference']
    source['low_fugacity_no_loss_relative_discrepancy']=abs(low-(CASES[0]['z']+source['no_loss_inverse_creation_integral_over_reference']))/low
    checks=dict(baseline_endpoint_absolute_differences=baseline_diff,
                batched_vs_original_baseline_absolute_differences={k:abs(main_result['cases'][4]['rows'][-1][k]-baseline['rows'][-1][k]) for k in ['Tkin_over_T','heavy_fraction','total_variation_to_same_species_MB']},
                step_192_vs_384=compare(main_result,refined),momentum_grid_192_vs_96=compare(main_result,coarse),
                temperature_intervals_16_vs_8=compare(main_result,temperature8),
                scattering_quadrature48_vs40_at_temperature8=compare(temperature8,quad40),
                split_vs_independent_unsplit_ODE=compare(subset,ode),no_pair_scaling_limit=no_pair_check,
                independent_source_integral=source,continuum_initial_checks=initial_checks,
                continuum_collisionless_Tf=collisionless_exact(TF),
                refinement_status='Empirical sensitivities within inherited cell closure and fixed free bath; no certified continuum or physical-model error bound')
    save('validation.json',checks)
    summary=[]
    for result in main_result['cases']:
        c=result['initial_condition'];initial_row=result['rows'][0];row=result['rows'][-1]
        summary.append(dict(case=c['id'],initial_abundance_z=c['z'],initial_kinetic_temperature_ratio=c['theta'],initial_heavy_fraction=initial_row['heavy_fraction'],
                            final_number_over_equilibrium_reference=row['comoving_number_over_equilibrium_reference'],
                            final_number_over_actual_initial=row['comoving_number_over_actual_initial'],
                            fractional_number_change=row['comoving_number_over_actual_initial']-1,
                            final_Tkin_over_T=row['Tkin_over_T'],final_heavy_fraction=row['heavy_fraction'],
                            final_shape_TV=row['total_variation_to_same_species_MB'],final_yield=row['yield_Y_total'],
                            max_rho_scalar_over_radiation=max(r['rho_scalar_over_prescribed_radiation'] for r in result['rows'])))
    with (OUT/'scan_summary.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)
    save('scan_summary.json',summary)
    save('run_metadata.json',dict(utc_date='2026-10-21',source_commit='48f9dcbd34e7cfb86504167a0483f732a5dd5e8e',
        Python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform(),elapsed_seconds=time.perf_counter()-start,
        n_reference_GeV3=NREF,initial_entropy_density_GeV3=S0,T0_GeV=T0,Tf_GeV=TF,gstar=60,gstar_s=60,
        initial_condition_mass_definition='M_a=a^3 n_a/n_eq,total(T0); sum M(T0)=z; every relative-to-initial output divides by z',
        channels='Frozen free-fermion scattering and conversion, heavy decay and inverse absorption, pair annihilation and bath inverse creation',
        inverse_source='Unchanged zero-chemical-potential bath source; never multiplied by imposed scalar z',
        closure='Inherited instantaneous equilibrium conditional moments and collision kernels within each momentum cell',
        earlier_cosmology_calculated=False,interacting_QCD_calculated=False,physical_relic_abundance_claim=False))
    print(json.dumps(summary,indent=2),flush=True)
    print('Elapsed',time.perf_counter()-start,flush=True)

if __name__=='__main__':main()
