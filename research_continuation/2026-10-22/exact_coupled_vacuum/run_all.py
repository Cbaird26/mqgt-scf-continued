"""Solve the restricted exact spectral vacuum and reproduce its checks.

Offline. Python >=3.10, NumPy, SciPy. Results are finite-cutoff floating-point
calculations; no interval certificate or unsearched-domain exclusion.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('VECLIB_MAXIMUM_THREADS','1')
import json,sys,platform,hashlib
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import root,least_squares,minimize_scalar
import vacuum as v
import mode_sums as m
import independent_checks as independent

HERE=Path(__file__).resolve().parent
CHECKS={}


def check(name,condition,metric=None,tolerance=None):
    CHECKS[name]={'passed':bool(condition)}
    if metric is not None:CHECKS[name]['metric']=float(metric)
    if tolerance is not None:CHECKS[name]['tolerance']=float(tolerance)
    if not condition:raise AssertionError((name,metric,tolerance))


def close(name,actual,target,tol):
    error=np.max(abs(np.asarray(actual)-np.asarray(target)))
    check(name,error<tol,error,tol)


def serial(obj):
    if isinstance(obj,np.ndarray):return obj.tolist()
    if isinstance(obj,np.generic):return obj.item()
    raise TypeError(type(obj).__name__)


def solve(alpha,initial,profile='minus',levels=12):
    answer=root(lambda x:v.tuned_equations(x,alpha,profile,levels),initial,jac=True,tol=1e-10)
    residual=np.max(abs(answer.fun))
    if not answer.success and residual>1e-10:raise RuntimeError(answer.message)
    x=answer.x;p,g,H=v.tuned_spectral(x,alpha,profile,levels)
    c=p/x[0]**2;H[0,0]-=2*c
    schur=H[0,0]-H[0,1:]@np.linalg.solve(H[1:,1:],H[1:,0])
    charged=v.charged_orientation_curvature(x,profile,levels)
    # V=V(D,U,P), P=|hd^T i sigma2 hu|^2. At a neutral stationary
    # point the two nonzero charged Cartesian Hessian eigenvalues coincide.
    charged_eigenvalue=charged*(x[1]**2+x[2]**2)/(x[1]**2*x[2]**2)
    metric=v.scalar_amplitude_metric(x,profile,levels)
    k,_=m.full_response(x[0],v.NODES,x[1],x[2],levels)
    ks,_=m.neutral_response(x[0],v.NODES,'single0',(),levels)
    k[:,0,0]+=12*ks[:,0,0]
    for i,a in enumerate(v.NODES):
        heat=sum(2*l*np.exp(-a*l*l/x[0]**2) for l in range(1,levels+1))
        k[i,1,1]+=heat/(18*np.pi**2)
    K=np.tensordot(v.WEIGHTS[profile],k,axes=1);N=np.array([1.,1.,0.])
    record={'x':x,'R_shift':x[0]-v.RSTAR,'c':c,'c_shift':c-v.CSTAR,
        'equations_residual':answer.fun,'P_tuned':p,'radial_amplitude_Hessian':H,
        'Hessian_eigenvalues':np.linalg.eigvalsh(H),'radial_Schur_complement':schur,
        'charged_orientation_curvature':charged,'charged_Cartesian_eigenvalue_twice':charged_eigenvalue,
        'scalar_amplitude_kinetic_metric':metric,'scalar_metric_eigenvalues':np.linalg.eigvalsh(metric),
        'neutral_kinetic_matrix':K,'neutral_kinetic_eigenvalues':np.linalg.eigvalsh(K),
        'photon_inverse_squared_over_kappa':N@K@N,
        'flat_directions':'Four scalar gauge-orbit zeros; with the potential-free Stueckelberg axion there are five zeros, four gauged and one physical phase.',
        'stability_scope':'Positive potential Hessian transverse to exact phase/gauge degeneracies in the retained lowest-harmonic, round-radius family. Radion kinetic metric and omitted-field stability not computed.'}
    return record


def main():
    R=v.RSTAR;wm=v.WEIGHTS['minus'];wp=v.WEIGHTS['plus'];dw=wp-wm
    previous=json.loads((HERE/'inputs/previous_scalar_results.json').read_text())
    origin=v.vacuum_record([R,0.,0.]);p,g,H=v.spectral([R,0.,0.])
    analytic=independent.unbroken_analytic(R)
    close('unbroken_trace_and_radius_derivatives',[p,g[0],H[0,0]],analytic,4e-12)
    close('common_flat_radius_equation',origin['flat_equations'],0.,1e-11)
    close('inherited_radius_curvature',origin['potential_Hessian'][0,0],float(v.INPUT['metrics']['minus']['potential_curvature_factor']),3e-12)
    A,G=wm@m.scalar_quadratic(R,v.NODES,12)
    close('origin_scalar_Hessian_from_predecessor',np.diag(H)[1:],8*np.pi**2*A*v.COUNTS,2e-13)
    close('origin_amplitude_metric_from_predecessor',v.scalar_amplitude_metric([R,0.,0.]),np.diag(G*v.COUNTS),3e-14)
    check('unbroken_stationary_point_is_scalar_saddle',np.all(np.diag(H)[1:]<0))
    xcheck=np.array([1.31,.4,.27]);pp,gg,HH=v.spectral(xcheck)
    close('matrix_exponential_vs_eigenvalue_trace',v.spectral(xcheck,levels=5)[0],independent.matrix_exponential_potential(xcheck),3e-12)
    gf,Hf=independent.finite_gradient_hessian(xcheck)
    close('analytic_gradient_vs_finite_difference',gg,gf,2e-9)
    close('analytic_Hessian_vs_finite_difference',HH,Hf,5e-6)
    print('Trace normalization and independent derivative checks passed.',flush=True)

    # This is a finite search, explicitly not an all-domain no-go theorem.
    scan=[]
    for rr in [.25,.4,.6,.9,R,1.7,2.3,3.]:
        for rho in [.03,.1,.3,1.,2.,4.,8.,12.,24.]:
            for beta in [0.,np.pi/8,np.pi/4,3*np.pi/8,np.pi/2]:
                x=[rr,rho*np.cos(beta),rho*np.sin(beta)]
                L=max(12,int(np.ceil(8*rr+.6*rho)))
                p,g,_=v.spectral(x,levels=L,order=1)
                dilation=np.dot(x[1:],g[1:])
                scan.append({'R':rr,'rho':rho,'beta':beta,'levels':L,'P':p,'scalar_dilation_derivative':dilation})
    maximum=max(t['scalar_dilation_derivative'] for t in scan)
    check('untuned_scalar_dilation_negative_at_all_scan_points',maximum<0,maximum)
    cutoff_controls=[]
    for x in [[3.,24.,0.],[3.,12.,12.],[.25,0.,24.],[R,12.,12.]]:
        L=max(12,int(np.ceil(8*x[0]+.6*np.linalg.norm(x[1:]))))
        p1,g1,_=v.spectral(x,levels=L,order=1);p2,g2,_=v.spectral(x,levels=L+4,order=1)
        error=max(abs(p1-p2),np.max(abs(g1-g2)))
        cutoff_controls.append({'x':x,'levels':[L,L+4],'max_change':error})
    check('untuned_large_field_cutoff_controls',max(a['max_change'] for a in cutoff_controls)<3e-9,max(a['max_change'] for a in cutoff_controls),3e-9)
    search=[]
    for r0 in [.7,R,2.5]:
        for hd0,hu0 in [(.2,.2),(2.,2.),(6.,1.),(1.,6.)]:
            scales=np.array([20.,5.,5.])
            def objective(x):return v.equations(x,levels=24)[0]/scales
            def jacobian(x):return v.equations(x,levels=24)[1]/scales[:,None]
            sol=least_squares(objective,[r0,hd0,hu0],jac=jacobian,bounds=([.25,0.,0.],[3.,12.,12.]),max_nfev=100,ftol=1e-11,xtol=1e-11,gtol=1e-11)
            raw=v.equations(sol.x,levels=24)[0]
            search.append({'start':[r0,hd0,hu0],'end':sol.x,'residual':raw,'evaluations':sol.nfev,'optimizer_status':sol.status,
                           'stationary_tolerance_met':np.max(abs(raw))<1e-7})
    unexpected=[t for t in search if t['stationary_tolerance_met'] and np.linalg.norm(t['end'][1:])>1e-4]
    check('bounded_root_search_no_nonzero_solution_found',not unexpected)
    print('Untuned scan and bounded searches completed.',flush=True)

    m3=wm@(1/v.NODES**3)
    weyl=[]
    for rr in [3.,6.,10.]:
        L=int(np.ceil(8*rr+4))
        exact=v.spectral([rr,2.,2.],levels=L,order=0)[0]/rr**2
        weyl.append({'R':rr,'levels':L,'P_over_R2':exact,'leading':v.weyl_diagonal(2.),'difference':exact-v.weyl_diagonal(2.)})
    check('Weyl_large_radius_control_improves',abs(weyl[-1]['difference'])<abs(weyl[0]['difference'])/8)
    check('analytic_runaway_coefficient_is_negative',v.weyl_diagonal(2.)-v.CSTAR<0,v.weyl_diagonal(2.)-v.CSTAR)
    check('plus_profile_runaway_coefficient_is_negative',v.weyl_diagonal(2.,profile='plus')-v.CSTAR<0,v.weyl_diagonal(2.,profile='plus')-v.CSTAR)

    # A single explicit counterterm, held common between profiles.
    critical={}
    for profile in ['minus','plus']:
        aa,gg=v.WEIGHTS[profile]@m.scalar_quadratic(R,v.NODES,12)
        critical[profile]=-4*np.pi**2*aa/R**2
    alpha0=critical['minus']
    slopes=[]
    for step in [.001,.0005]:
        vals=[wm@m.scalar_quadratic(R+k*step,v.NODES,14) for k in [-2,-1,1,2]]
        slopes.append((vals[0]-8*vals[1]+8*vals[2]-vals[3])/(12*step))
    close('scalar_radius_slope_step_convergence',slopes[0],slopes[1],2e-12)
    combo=slopes[1][0]-2*A/R
    sc=previous['scalar_profiles']['minus'];a4=sc['A4'];c0=sc['C0']
    Q=4*np.pi**2*np.array([[16*a4,6*c0],[6*c0,12*a4]])
    quartic_D=np.linalg.solve(2*Q,-4*np.pi**2*A*v.COUNTS)
    quartic_x=np.r_[R,np.sqrt(quartic_D)]
    quartic_p,quartic_g,_=v.spectral(quartic_x)
    quartic_dilation=quartic_x[1:]@quartic_g[1:]
    check('untuned_quartic_minimum_is_not_full_action_stationary',quartic_dilation<-.1,quartic_dilation)
    b=4*np.pi**2*v.COUNTS*combo
    Kr=origin['potential_Hessian'][0,0]
    Qeff=Q-np.outer(b,b)/(2*Kr)
    check('supercritical_tuned_bifurcation_quartic_positive',np.linalg.eigvalsh(Qeff).min()>0,np.linalg.eigvalsh(Qeff).min())
    limiting_schur=Kr-.5*b@np.linalg.solve(Q,b)
    fixtures={}
    for eps in [1e-2,1e-4]:
        alpha=alpha0-2*np.pi**2*G*eps/R**2
        D=np.linalg.solve(2*Qeff,2*np.pi**2*G*eps*v.COUNTS)
        initial=np.r_[R-b@D/Kr,np.sqrt(D)]
        entry={'epsilon_minus_origin':eps,'alpha':alpha,'delta2_local_convention':4*np.pi*alpha/(wm@(1/v.NODES)),
               'leading_solution':initial,'profiles':{}}
        for profile in ['minus','plus']:
            rec=solve(alpha,initial,profile)
            close(f'flat_equations_eps{eps}_{profile}',rec['equations_residual'],0.,4e-10)
            check(f'positive_restricted_Hessian_eps{eps}_{profile}',rec['Hessian_eigenvalues'].min()>0,rec['Hessian_eigenvalues'].min())
            check(f'positive_charged_curvature_eps{eps}_{profile}',rec['charged_orientation_curvature']>0,rec['charged_orientation_curvature'])
            check(f'positive_scalar_metric_eps{eps}_{profile}',rec['scalar_metric_eigenvalues'].min()>0,rec['scalar_metric_eigenvalues'].min())
            check(f'positive_neutral_metric_eps{eps}_{profile}',rec['neutral_kinetic_eigenvalues'].min()>0,rec['neutral_kinetic_eigenvalues'].min())
            rec16=solve(alpha,rec['x'],profile,16)
            close(f'vacuum_cutoff_12_to_16_eps{eps}_{profile}',rec['x'],rec16['x'],3e-9)
            close(f'Hessian_cutoff_12_to_16_eps{eps}_{profile}',rec['radial_amplitude_Hessian'],rec16['radial_amplitude_Hessian'],3e-10)
            rec['cutoff_12_to_16_max_solution_change']=np.max(abs(rec['x']-rec16['x']))
            rec['cutoff_12_to_16_max_Hessian_change']=np.max(abs(rec['radial_amplitude_Hessian']-rec16['radial_amplitude_Hessian']))
            entry['profiles'][profile]=rec
        minus=entry['profiles']['minus'];plus=entry['profiles']['plus']
        entry['plus_minus']={key:plus[key]-minus[key] for key in ['x','c','photon_inverse_squared_over_kappa','radial_Schur_complement']}
        # At fixed inherited c the same three stationary equations describe
        # a restricted nonflat potential; not a self-consistent curved spacetime.
        def fixed(x):
            p,g,H=v.tuned_spectral(x,alpha);g[0]-=2*v.CSTAR*x[0];H[0,0]-=2*v.CSTAR
            return g,H
        fixed_solution=root(fixed,minus['x'],jac=True,tol=1e-10)
        pp,gg,HH=v.tuned_spectral(fixed_solution.x,alpha)
        entry['fixed_c_stationary_diagnostic']={'x':fixed_solution.x,'W':pp-v.CSTAR*fixed_solution.x[0]**2,'gradient':fixed_solution.fun,
             'c':v.CSTAR,'interpretation':'Stationary point of restricted potential only; nonzero W means no flat spacetime solution.'}
        close(f'fixed_c_stationarity_eps{eps}',fixed_solution.fun,0.,4e-10)
        fixtures[str(eps)]=entry
        print('Exact tuned fixture',eps,'R,h_d,h_u =',minus['x'],'Schur =',minus['radial_Schur_complement'],flush=True)
    first=fixtures['0.01']['profiles']['minus']
    theta_numeric=independent.charged_finite_difference(first['x'])
    close('charged_orientation_analytic_vs_dense_finite_difference',first['charged_orientation_curvature'],theta_numeric,3e-9)
    check('small_epsilon_Schur_limit_approached',abs(fixtures['0.0001']['profiles']['minus']['radial_Schur_complement']-limiting_schur)<.001)
    deltaA=dw@m.scalar_quadratic(R,v.NODES,12)[:,0]
    eps_cross=2*deltaA/G
    phase={'epsilon_cross_plus':eps_cross,'epsilon_example':1e-8,
           'minus_origin_quadratic_mass':-1e-8,
           'plus_origin_quadratic_mass':(-G*1e-8+2*deltaA)/(wp@m.scalar_quadratic(R,v.NODES,12)[:,1]),
           'interpretation':'Locally, for 0<epsilon<epsilon_cross, minus is on a supercritical broken branch while plus has a scalar-stable symmetric stationary point. No numeric tiny-vev solve is asserted.'}
    check('common_counterterm_can_straddle_local_phase_boundary',phase['plus_origin_quadratic_mass']>0 and phase['minus_origin_quadratic_mass']<0)
    result={'title':'Exact spectral scalar-radius vacuum: instability and tuned stationary branches','date':'2026-10-22',
        'normalization':'W=P+alpha R^2(16 hd^2+12 hu^2)-c R^2 = 4 pi^2 V/(kappa Lambda^4)',
        'fixed_fixture':'Nb=4; yhat_d=yhat_e=yhat_u=1; neutral lowest-harmonic amplitudes h_i=H_i/(Lambda R).',
        'R_star':R,'c_star':v.CSTAR,'unbroken_untuned_stationary_point':origin,
        'untuned_scan':scan,'untuned_scan_maximum_dilation':maximum,'untuned_cutoff_controls':cutoff_controls,'untuned_bounded_root_search':search,
        'untuned_quartic_candidate_at_fixed_R':{'x':quartic_x,'full_trace_gradient':quartic_g,'scalar_dilation_derivative':quartic_dilation,'P':quartic_p},
        'runaway':{'m3':m3,'Weyl_coefficient_h2':v.weyl_diagonal(2.),'W_over_R2_limit_h2':v.weyl_diagonal(2.)-v.CSTAR,
                   'plus_W_over_R2_limit_h2':v.weyl_diagonal(2.,profile='plus')-v.CSTAR,
                   'large_R_then_large_h_coefficient_limit':24*m3,'finite_radius_controls':weyl,
                   'scope':'Analytic negative asymptotic direction for fixed inherited subtraction. Proves global unboundedness in this field family, not absence of all metastable extrema.'},
        'tuning':{'alpha_critical':critical,'A2_prime':slopes[1][0],'A2_prime_minus_2A2_over_R':combo,
                  'local_counterpart':-5*(wm@(1/v.NODES))/(48*np.pi**3*R),'Q':Q,'b':b,'Q_eff':Qeff,'Schur_limit':limiting_schur,
                  'definition':'alpha(epsilon)=-4 pi^2 A2_minus(Rstar)/Rstar^2 -2 pi^2 G_minus(Rstar) epsilon/Rstar^2, held identical for both profiles.'},
        'tuned_flat_fixtures':fixtures,'near_critical_phase_split':phase,
        'independent_charged_curvature':theta_numeric,
        'limits':['Explicit extra scalar-mass counterterm is externally chosen, not selected by the spectral action.',
                  'Flat fixtures retune c separately; c is a parameter, not a dynamical field.',
                  'Full finite-field potential on lowest scalar harmonics, round sphere, fixed connection and prescribed anomaly sector only.',
                  'Potential Hessian does not certify radion kinetic positivity, omitted harmonic/metric/gauge stability or physical pole masses.',
                  'No global uniqueness or interval tail certificate; finite root search cannot exclude unsearched extrema.',
                  'Anomaly-sector potential and six-dimensional completion remain unspecified; one physical phase stays flat in the adopted sector.',
                  'No independent kappa/profile selection, quantum thresholds/running, or derivation of measured fine-structure constant.',
                  'AI-assisted self-audit with independent numerical methods, not separate-agent or external peer review.']}
    (HERE/'results.json').write_text(json.dumps(result,indent=2,default=serial)+'\n')
    report={'checks':CHECKS,'passed':sum(x['passed'] for x in CHECKS.values()),'total':len(CHECKS),
        'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()},
        'input_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE/'inputs').iterdir()}}
    (HERE/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',report['passed'],'/',report['total'],flush=True)


if __name__=='__main__':main()
