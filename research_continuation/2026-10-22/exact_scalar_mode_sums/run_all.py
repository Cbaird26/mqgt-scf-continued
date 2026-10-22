"""Reproduce the note's numerical results and independent validation.

Usage: python run_all.py
Requires Python >=3.10, NumPy, SciPy. No network or external programs used.
Writes results.json and checks.json. Exit nonzero on a failed check.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('VECLIB_MAXIMUM_THREADS','1')
from pathlib import Path
import json,sys,hashlib,platform
import numpy as np
import scipy
import mode_sums as m
from independent_checks import run_external_vertex_check,gauss_heat_moments,angular_overlap_checks

HERE=Path(__file__).resolve().parent
checks={}


def check(name,condition,metric=None,tolerance=None):
    checks[name]={'passed':bool(condition)}
    if metric is not None:checks[name]['metric']=float(metric)
    if tolerance is not None:checks[name]['tolerance']=float(tolerance)
    if not condition:raise AssertionError(name+': '+str(metric))


def close(name,actual,expected,tol):
    error=float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    check(name,error<tol,error,tol)


def unbroken(R,nodes,L):
    k,_=m.full_response(R,nodes,0.,0.,L)
    ks,_=m.neutral_response(R,nodes,'single0',(),L)
    for i,a in enumerate(nodes):
        h0=sum(2*l*np.exp(-a*l*l/R**2) for l in range(1,L+1))
        k[i,0,0]+=12*ks[i,0,0]
        k[i,1,1]+=h0/(18*np.pi*np.pi)
    return k


def main():
    p=json.loads((HERE/'inputs/common_vacuum_pair.json').read_text())
    R=float(p['common_R']);nodes=np.array(p['nodes'],float)
    wm=np.array(p['weights_minus'],float);wp=np.array(p['weights_plus'],float);dw=wp-wm
    m1=wm@(1/nodes);m2=wm@(1/nodes**2)
    close('six_retained_profile_moments',np.array([dw@(nodes**k) for k in (-3,-2,-1,0,1,2)]),0.,2e-15)
    ang=angular_overlap_checks();check('independent_Wigner_sphere_quadratures',ang['max_absolute_error']<5e-14,ang['max_absolute_error'],5e-14)
    close('zero_mode_Yukawa_overlap',m.yukawa_element((1,1,-1),(1,0,0),-.5),1/np.sqrt(4*np.pi),1e-15)
    for n in (0,1,2):
        heat=0.
        for b in m.blocks('single'+str(n),8):
            close('Dirac_chirality_n%d_k%d'%(n,b['k2']),b['D']@b['gamma']+b['gamma']@b['D'],0.,1e-14)
            heat+=np.exp(-.7*np.linalg.eigvalsh(b['D'])**2).sum()
        target=n+2*sum((2*l+n)*np.exp(-.7*l*(l+n)) for l in range(1,9))
        close('internal_Dirac_heat_multiplicity_n'+str(n),heat,target,3e-14)
    hm=m.heat_moments(np.array([0.,1e-7,.3,3.,30.]),1.2)
    hq=gauss_heat_moments(np.array([0.,1e-7,.3,3.,30.]),1.2)
    close('analytic_heat_moments_vs_quadrature',np.array(hm),np.array(hq),3e-14)
    ev=run_external_vertex_check();check('full_external_Clifford_finite_q_response',ev['absolute_difference']<2e-10,ev['absolute_difference'],2e-10)
    print('Angular, heat, and full external-vertex checks passed.',flush=True)
    cutoff=[];prev=None
    for L in (8,10,12):
        sq=m.scalar_quadratic(R,nodes,L)
        pc=m.potential_coefficients(R,nodes,levels=L)
        qc=m.potential_coefficients(R,nodes,kind='quark',levels=L)
        shifts=m.cauchy_shifts(R,nodes,L)
        close('quadratic_Duhamel_vs_Toeplitz_L'+str(L),sq[:,0],pc[:,0],1e-13)
        close('Cauchy_imaginary_residual_L'+str(L),shifts.imag,0.,2e-12)
        if prev is not None:
            diffs={'from_levels':L-2,'to_levels':L,
                   'scalar_max_difference':max(np.max(abs(sq-prev[0])),np.max(abs(pc-prev[1])),np.max(abs(qc-prev[2]))),
                   'kinetic_shift_max_difference':np.max(abs(shifts-prev[3])),
                   'profile_difference_of_shift_max_change':np.max(abs(np.tensordot(dw,shifts-prev[3],axes=(0,1))))}
            cutoff.append(diffs)
            check('scalar_cutoff_convergence_L'+str(L),diffs['scalar_max_difference']<1e-10,diffs['scalar_max_difference'],1e-10)
            check('kinetic_cutoff_convergence_L'+str(L),diffs['kinetic_shift_max_difference']<1e-10,diffs['kinetic_shift_max_difference'],1e-10)
        prev=(sq,pc,qc,shifts)
        print('Computed scalar and kinetic coefficients through level',L,flush=True)
    shifts=shifts.real
    contour=m.cauchy_shifts(R,nodes,12,radius=.3,points=24)
    close('kinetic_contour_radius_and_order',shifts,contour,2e-12)
    pc_ind=m.potential_coefficients(R,nodes,levels=12,method='cauchy',radius=.3,points=24)
    close('scalar_Toeplitz_vs_Cauchy',pc,pc_ind,2e-11)
    parallel=m.potential_coefficients(R,nodes,'parallel',10)
    close('parallel_Yukawa_flavour_rotation_quartic',parallel[:,1],4*pc[:,1],1e-12)
    close('quark_quadratic_additivity',qc[:,0],2*pc[:,0],1e-13)
    scalars=np.column_stack([sq,pc[:,1],qc[:,1]-2*pc[:,1],4*pc[:,1]-qc[:,1]])
    scalar_names=['A2','G','A4','C0','C1']
    scalar_profiles={label:dict(zip(scalar_names,w@scalars)) for label,w in [('minus',wm),('plus',wp),('difference',dw)]}
    check('positive_scalar_wavefunction_and_quartics',np.all((wm@scalars)[1:]>0))
    for label in ('minus','plus'):
        v=scalar_profiles[label];v['canonical_mass_squared_over_Lambda2']=2*v['A2']/v['G']
        v['canonical_quartics_times_kappa']={'lambda_d':v['A4']/(4*v['G']**2),
            'lambda_u':v['A4']/(3*v['G']**2),'lambda_cross':v['C0']/(4*v['G']**2),
            'lambda_alignment':v['C1']/(4*v['G']**2)}
    local={'A2':(-2*R*R*m2+5*m1/6)/(16*np.pi**3),'G':R*R*m1/(8*np.pi**3),'A4':R*R*m1/(48*np.pi**4)}
    local.update(C0=local['A4'],C1=local['A4'],canonical_mass_squared_over_Lambda2=-2*m2/m1+5/(6*R*R))
    K0=unbroken(R,nodes,12)
    expected=np.diag([.199544788403314737,.200445639903622954,1.843191195308218923])
    close('all_unbroken_neutral_coefficients_match_predecessor',np.tensordot(wm,K0,axes=1),expected,2e-13)
    close('unbroken_weak_profile_difference',dw@K0[:,0,0],6.20710121949330644e-8,2e-15)
    N=np.array([1.,1.,0.]);photon0=K0[:,0,0]+K0[:,1,1]+2*K0[:,0,1]
    close('unbroken_photon_profile_difference',dw@photon0,1.55190800181481749e-7,2e-15)
    rs,rms,rerr=m.higgs_shifts(R,nodes,12,step=.06)
    close('kinetic_Cauchy_vs_real_Richardson',shifts,rs,3e-10)
    hcharges=[np.array([-.5,.5,1.]),np.array([-.5,.5,-1.])]
    for i,nd in enumerate((16,12)):
        target=sq[:,1,None,None]*nd*np.outer(hcharges[i],hcharges[i])
        close('scalar_kinetic_gauge_mass_Ward_identity_'+str(i),rms[i],target,8e-11)
    sph={}
    for label,w in [('minus',wm),('plus',wp),('difference',dw)]:
        sph[label]={}
        for i,key in enumerate(('down','up')):
            matrix=np.tensordot(w,shifts[i],axes=1)
            sph[label][key]={'matrix':matrix,'photon_projection':N@matrix@N}
    hd=.1;hu=.08
    kbase,_=m.full_response(R,nodes,0.,0.,12)
    kh,mh=m.full_response(R,nodes,hd,hu,12)
    kh+=K0-kbase
    km=np.tensordot(wm,kh,axes=1);mm=np.tensordot(wm,mh,axes=1)
    close('finite_background_photon_mass_null',mm@N,0.,2e-14)
    check('finite_background_kinetic_positive',np.linalg.eigvalsh(km).min()>0,np.linalg.eigvalsh(km).min())
    for kind,amps in [('quark',(hd,hu)),('lepton',(hd,))]:
        kreal,_=m.neutral_response(R,nodes,kind,amps,10)
        close('holomorphic_similarity_vs_Hermitian_'+kind,m.analytic_response(R,nodes,kind,amps,10),kreal,1e-12)
        for b in m.blocks(kind,8):
            B=b['D']/R+sum((h*S for h,S in zip(amps,b['S'])),np.zeros_like(b['D']))
            Q=b['T'][0]+b['T'][1]
            close('exact_unbroken_generator_'+kind+'_k'+str(b['k2']),B@Q-Q@B,0.,2e-14)
    # Radius derivative formerly unavailable in the scalar continuation.
    derivs=[]
    for dr in (.001,.0005):
        samples=[unbroken(R+s*dr,nodes,12) for s in (-2,-1,1,2)]
        derivs.append((samples[0]-8*samples[1]+8*samples[2]-samples[3])/(12*dr))
    close('weak_radius_derivative_step_convergence',derivs[0],derivs[1],3e-11)
    radius_derivatives={label:np.tensordot(w,derivs[1],axes=1) for label,w in [('minus',wm),('plus',wp),('difference',dw)]}
    # Independent asymptotic controls; these are numerical checks, not proofs.
    smallR=.02;small=wm@m.scalar_quadratic(smallR,nodes,7)
    limits={'A2':-m1/(16*np.pi**3),'G':1/(16*np.pi**3),'A4':1/(128*np.pi**4),'C0':0.,'C1':1/(64*np.pi**4),'canonical_mass_squared_over_Lambda2':-2*m1}
    close('small_radius_zero_mode_A2',small[0],limits['A2'],2e-14)
    close('small_radius_zero_mode_G',small[1],limits['G'],2e-10)
    local_controls=[]
    for rr in (2.,4.,8.):
        ss=m.scalar_quadratic(rr,[1.],int(8*rr))[0]
        sloc=np.array([(-2*rr*rr+5/6)/(16*np.pi**3),rr*rr/(8*np.pi**3)])
        kk=[]
        for h in (0.,.04,.02):kk.append(m.neutral_response(rr,[1.],'pair',(h,),int(8*rr))[0][0,0,0])
        dW=(4*(kk[2]-kk[0])/.02**2-(kk[1]-kk[0])/.04**2)/3
        leading=-rr**4/(144*np.pi**3)
        local_controls.append({'R':rr,'A2':ss[0],'G':ss[1],'local_A2_G':sloc,'weak_h2':dW,'a4_curvature_leading':leading,'weak_ratio':dW/leading})
    check('large_radius_scalar_local_limit_improves',abs(local_controls[-1]['G']/local_controls[-1]['local_A2_G'][1]-1)<.006)
    check('geometric_a4_Higgs_shift_limit_improves',abs(local_controls[-1]['weak_ratio']-1)<.03)
    scan=[]
    for rr in np.linspace(.3,3.,55):
        vv=wm@m.scalar_quadratic(rr,nodes,max(8,int(9*rr)))
        scan.append({'R':rr,'mass_squared_exact':2*vv[0]/vv[1],'mass_squared_local':-2*m2/m1+5/(6*rr*rr),'G_exact':vv[1]})
    check('radius_scan_scalar_kinetic_positive',min(x['G_exact'] for x in scan)>0)
    # Operational low-momentum definition, not a selection of a Wilson basis.
    result={'title':'Exact internal mode sums and Higgs-induced neutral kinetics','date':'2026-10-22',
        'R_star':R,'nodes':nodes,'weights_minus':wm,'weights_plus':wp,
        'field_convention':'h_i=H_i/(Lambda R), M/Lambda=yhat_i h_i Y; displayed matrices use Nb=4 and yhat_d=yhat_e=yhat_u=1.',
        'scalar_per_node_columns':scalar_names,'scalar_per_node':scalars,'scalar_profiles':scalar_profiles,'local_a2_a4':local,
        'neutral_unbroken_per_node':K0,'higgs_shift_per_node':shifts,'higgs_shift_profiles':sph,
        'finite_background_fixture':{'h_d':hd,'h_u':hu,'K_over_kappa_minus':km,'mass_over_kappa_Lambda2_minus':mm,
             'photon_inverse_squared_over_kappa_minus':N@km@N,'photon_pair_difference':dw@(kh[:,0,0]+kh[:,1,1]+2*kh[:,0,1]),
             'photon_second_order_remainder_minus':N@(km-np.tensordot(wm,K0+hd**2*shifts[0]+hu**2*shifts[1],axes=1))@N},
        'unbroken_radius_derivatives':radius_derivatives,'small_R_limits':limits,'local_limit_controls':local_controls,'radius_scan':scan,
        'numerical_validation':{'cutoffs':cutoff,'kinetic_contour_max_change':np.max(abs(contour-shifts)),
            'scalar_contour_max_change':np.max(abs(pc-pc_ind)),'real_Richardson_vs_Cauchy_max':np.max(abs(shifts-rs)),
            'independent_external_vertex':ev,'angular_quadrature':ang},
        'limits':['No interval rounding or uniform tail certificate.','Exact internal spectral representation; finite-cutoff numerical evaluations.',
            'Small-field scalar coefficients and O(h^2) kinetic shifts; full finite-field fixture also supplied.',
            'Fixed inherited radius and prescribed background, not a newly solved coupled vacuum.',
            'No six-dimensional anomaly completion, axion loop sector, higher-boson integration, kappa selection, thresholds or running.',
            'The measured fine-structure constant is not derived.']}
    def convert(obj):
        if isinstance(obj,np.ndarray):return obj.tolist()
        if isinstance(obj,np.generic):return obj.item()
        raise TypeError(type(obj).__name__)
    (HERE/'results.json').write_text(json.dumps(result,indent=2,default=convert)+'\n')
    report={'checks':checks,'total':len(checks),'passed':sum(c['passed'] for c in checks.values()),
        'environment':{'python':sys.version,'platform':platform.platform(),'numpy':np.__version__,'scipy':scipy.__version__},
        'input_sha256':hashlib.sha256((HERE/'inputs/common_vacuum_pair.json').read_bytes()).hexdigest()}
    (HERE/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: %d/%d checks'%(report['passed'],report['total']),flush=True)
    print('Scalar minus:',scalar_profiles['minus'],flush=True)


if __name__=='__main__':main()
