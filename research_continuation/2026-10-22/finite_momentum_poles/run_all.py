"""Reproduce finite-momentum kernels, bounded pole searches and targeted checks."""
from pathlib import Path
import hashlib,json,platform
import numpy as np
import scipy
from two_point import TwoPoint,basic
import all_scalars as alls
import direct_vertices
from poles import real_roots,contour,locate_by_contours,polish,complex_residue
HERE=Path(__file__).resolve().parent
PREVIOUS=json.loads((HERE/'inputs/previous_radion_results.json').read_text())
CHECKS={}
def check(name,condition,metric=None,tolerance=None):
    CHECKS[name]={'passed':bool(condition),'metric':metric,'tolerance':tolerance}
    if not condition:print('FAIL',name,metric,tolerance,flush=True)
def close(name,a,b,tol,relative=False):
    a=np.asarray(a);b=np.asarray(b);err=float(np.max(abs(a-b)))
    if relative:err/=max(1.,float(np.max(abs(a))),float(np.max(abs(b))))
    check(name,err<=tol,err,tol)
def serial(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x))
results={'title':'Finite-momentum metric/radion/scalar operator and formal Lorentzian pole tests',
'date':'2026-10-22','source_commit':'1bb152dfbd6bb1e02a3e841b6d73e338f8e5fabf',
'prescription':'z=p_E^2/Lambda^2=-s-i0, s=(omega^2-k^2)/Lambda^2; formal analytic continuation, not a quantum contour construction',
'pole_sector':'CP-even neutral radius/amplitudes with transverse metric trace; independent transverse-traceless graviton',
'real_search_interval':[-20,20],'complex_count_box':[-20,20,-20,20],'branches':{},'controls':{}}
errors=[]
for a,b in [(.8,.6),(1.7,0.),(.4,1.2)]:
    for z in [.1,1.,4.,-.7,1.+2j]:
        raw,pred=direct_vertices.check_one(a,b,z);err=float(np.max(abs(raw-pred)));errors.append(err)
        check(f'direct_vertices_a{a}_b{b}_z{z}',err<3e-12,err,3e-12)
results['controls']['direct_gamma_vertex_max_error']=max(errors)
F,J,Fp,Jp=basic(np.array([0.]))
close('removable_form_factor_values',[F[0],J[0],Fp[0],Jp[0]],[1,1/6,-1/6,-1/60],2e-15)
kernels={}
for eps,branch in PREVIOUS['branches'].items():
    results['branches'][eps]={'profiles':{}}
    for profile,p in branch['profiles'].items():
        name=eps+'_'+profile;x=np.array(p['x']);H=np.array(p['potential_Hessian'])[:3,:3]
        k=TwoPoint(x,H,profile,levels=12,quadrature=96);kernels[name]=k
        _,_,_,_,H16=alls.full_geometry_hessian(x,branch['alpha'],p['c'],profile,levels=16)
        kr=TwoPoint(x,H16[:3,:3],profile,levels=16,quadrature=96)
        kq=TwoPoint(x,H,profile,levels=12,quadrature=64)
        close(name+'_inherited_gravity',[k.f,*k.df],[p['f'],*p['df'][:3]],3e-13)
        close(name+'_IR_Einstein_metric',k.GE,np.array(p['Einstein_metric'])[:3,:3],2e-12)
        close(name+'_IR_Jordan_metric',k.GJ,np.array(p['Jordan_metric'])[:3,:3],2e-12)
        a,b,c,ap,bp,cp=k.gravity(0.)
        close(name+'_gravity_zero_momentum',[a,b,*c],[k.f,k.f,*(-k.df/2)],2e-13)
        close(name+'_Schur_IR_derivative',k.schur(0.)[1],k.GE,2e-12)
        close(name+'_no_local_R_squared_term',bp,0.,1e-14)
        errors=[];quaderrors=[]
        for z in [-15.,-.7,.13,10.,-3.+7j,15.+15j]:
            K,Kp,T,Tp=k.operator(z);Kr,_,Tr,_=kr.operator(z);Kq,_,Tq,_=kq.operator(z)
            errors.append(float(max(np.max(abs(K-Kr))/max(1.,np.max(abs(K))),abs(T-Tr)/max(1.,abs(T)))))
            quaderrors.append(float(max(np.max(abs(K-Kq))/max(1.,np.max(abs(K))),abs(T-Tq)/max(1.,abs(T)))))
            h=1e-4
            fd=(k.operator(z-2*h)[0]-8*k.operator(z-h)[0]+8*k.operator(z+h)[0]-k.operator(z+2*h)[0])/(12*h)
            close(name+f'_analytic_derivative_z{z}',Kp,fd,2e-8,relative=True)
        check(name+'_finite_momentum_cutoff_12_16',max(errors)<2e-10,max(errors),2e-10)
        check(name+'_quadrature_64_96',max(quaderrors)<2e-10,max(quaderrors),2e-10)
        pp=np.array([.2,.3,-.4,.8]);z=pp@pp;theta=np.eye(4)-np.outer(pp,pp)/z
        P0=np.einsum('ij,kl->ijkl',theta,theta)/3
        P2=(np.einsum('ik,jl->ijkl',theta,theta)+np.einsum('il,jk->ijkl',theta,theta))/2-P0
        K,_,T,_=k.operator(z);metric=T*P2+K[0,0]*P0;mix=z*theta[:,:,None]*k.gravity(z)[2]
        close(name+'_metric_transversality',np.einsum('i,ijkl->jkl',pp,metric),0.,1e-15)
        close(name+'_mixed_transversality',np.einsum('i,ijA->jA',pp,mix),0.,1e-15)
        sr,sbr=real_roots(k.determinant);tr,tbr=real_roots(lambda z:k.gravity(z)[0]);br,bbr=real_roots(lambda z:k.gravity(z)[1])
        check(name+'_observed_scalar_real_roots',len(sr)==5,len(sr),5)
        check(name+'_observed_tensor_real_root',len(tr)==1 and tr[0]>0,tr[0] if tr else None)
        rec=[];cutshift=[];quadshift=[];reserrors=[]
        for j,z in enumerate(sr):
            r=k.residue(z);K,Kp,_,_=k.operator(z);vv=np.array(r['null_vector_tau_R_hd_hu'])
            rel=float(np.linalg.norm(K@vv)/(max(1.,np.linalg.norm(K))*np.linalg.norm(vv)))
            check(name+f'_scalar_pole_{j}_null',rel<2e-11,rel,2e-11)
            zr=float(polish(kr.determinant,kr.determinant_prime,z));zq=float(polish(kq.determinant,kq.determinant_prime,z))
            cutshift.append(abs(zr-z));quadshift.append(abs(zq-z))
            delta=1e-6*max(abs(z),.001)
            estimate=(delta*np.linalg.inv(k.operator(z+delta)[0])-delta*np.linalg.inv(k.operator(z-delta)[0]))/2
            exact=np.outer(vv,vv)/r['slope'];reserrors.append(float(np.linalg.norm(estimate-exact)/np.linalg.norm(exact)))
            rec.append(r)
        check(name+'_scalar_pole_cutoff_shift',max(cutshift)<2e-9,max(cutshift),2e-9)
        check(name+'_scalar_pole_quadrature_shift',max(quadshift)<2e-9,max(quadshift),2e-9)
        check(name+'_scalar_residue_inverse_limit',max(reserrors)<2e-5,max(reserrors),2e-5)
        check(name+'_positive_residue_timelike_poles',all(r['residue_sign']==1 for r in rec if r['z']<0))
        check(name+'_negative_residue_scalar_tachyon',all(r['residue_sign']==-1 for r in rec if r['z']>0))
        zt=tr[0];_,_,T,Tp=k.operator(zt)
        ztr=float(polish(lambda z:kr.gravity(z)[0],lambda z:kr.gravity(z)[3],zt))
        close(name+'_tensor_pole_cutoff_shift',zt,ztr,2e-10)
        check(name+'_negative_residue_tensor_tachyon',Tp<0,float(Tp))
        check(name+'_positive_massless_graviton',k.f/4>0,k.f/4)
        check(name+'_no_sampled_timelike_tensor_zero',min(k.gravity(-s)[0] for s in np.linspace(0,20,201))>0)
        bzeros=[]
        for zb in br:
            ss=np.linalg.svd(k.operator(zb)[0],compute_uv=False)
            check(name+'_metric_B_zero_not_full_pole',ss[-1]/ss[0]>1e-7,float(ss[-1]/ss[0]),1e-7)
            bzeros.append({'z':zb,'full_operator_min_singular_ratio':float(ss[-1]/ss[0]),'regular_determinant':float(k.determinant(zb))})
        counts={}
        for sector,fun in [('tensor',lambda z:k.gravity(z)[0]),('coupled',k.determinant)]:
            coarse=contour(fun,per_side=256);fine=contour(fun,per_side=512)
            check(name+'_'+sector+'_contour_refinement',coarse['rounded_count']==fine['rounded_count'] and fine['max_phase_step']<1.,fine['max_phase_step'],1.)
            counts[sector]={'coarse':coarse,'fine':fine}
        results['branches'][eps]['profiles'][profile]={'x':x,'f':k.f,'IR_Einstein_metric':k.GE,
            'two_derivative_neutral_m2':p['neutral_squared_mass_parameters'],
            'scalar_real_poles':rec,'scalar_real_brackets':sbr,
            'tensor_nonzero_real_poles':[{'z':zt,'mass2_over_Lambda2':-zt,'slope':Tp,'relative_residue_to_massless':k.f/(4*Tp),'residue_sign':-1}],
            'metric_B_zeros':bzeros,'complex_counts':counts,'max_cutoff_kernel_relative_error':max(errors),
            'max_quadrature_kernel_relative_error':max(quaderrors),'max_scalar_pole_cutoff_shift':max(cutshift),
            'max_scalar_pole_quadrature_shift':max(quadshift),'max_scalar_residue_inverse_error':max(reserrors)}
        print(name,'tensor tachyon z',zt,'scalar real z',sr,flush=True)

p=PREVIOUS['branches']['0.01']['profiles']['minus'];k=kernels['0.01_minus']
k9=TwoPoint(p['x'],p['potential_Hessian'],all_fields=True,quadrature=96)
close('all_nine_IR_metric',k9.GE,p['Einstein_metric'],3e-12)
close('all_nine_neutral_block_finite_momentum',k9.scalar(-.7)[0][:3,:3],k.scalar(-.7)[0],3e-12)
close('all_nine_metric_mixing_selection_rule',k9.gravity(1.+2j)[2][3:],0.,2e-13)
results['controls']['all_nine_fixed_metric_kernel_at_z1']=k9.scalar(1.)[0]
complex_results={}
for sector,fun,prime in [('tensor',lambda z:k.gravity(z)[0],lambda z:k.gravity(z)[3]),('coupled',k.determinant,k.determinant_prime)]:
    roots,cells=locate_by_contours(fun);roots=[polish(fun,prime,z) for z in roots];entries=[]
    for i,z in enumerate(roots):
        if sector=='tensor':
            a,b,c,ap,bp,cp=k.gravity(z);slope=z*ap/4;err=float(abs(a)/max(1.,abs(z*ap)))
            check(f'complex_tensor_{i}_root',err<1e-11,err,1e-11)
            entry={'z':[z.real,z.imag],'inverse_K2_residue':[float((1/slope).real),float((1/slope).imag)]}
        else:
            entry=complex_residue(k,z);err=entry['normalized_smallest_singular_value']
            check(f'complex_scalar_{i}_null',err<2e-11,err,2e-11)
        entries.append(entry)
    realcount=len(results['branches']['0.01']['profiles']['minus']['tensor_nonzero_real_poles' if sector=='tensor' else 'scalar_real_poles'])
    total=results['branches']['0.01']['profiles']['minus']['complex_counts'][sector]['fine']['rounded_count']
    check(sector+'_isolated_roots_match_box_count',realcount+2*len(roots)==total,realcount+2*len(roots),total)
    complex_results[sector]={'upper_half_plane_roots':entries,'isolation_cells':cells,'searched_upper_rectangle':[-20,20,.1,20],
                            'lower_half_plane':'complex conjugates; real coefficients',
                            'interpretation':'Numerical bounded count and isolation, not interval certification or global zero enumeration.'}
    print(sector,'upper-plane isolated roots',len(roots),flush=True)
results['complex_poles_representative_fixture']=complex_results
close('complex_conjugation_of_kernel',k.operator(-3.+7j)[0].conj(),k.operator(-3.-7j)[0],2e-13)
complex_residue_errors=[]
for i,entry in enumerate(complex_results['coupled']['upper_half_plane_roots']):
    z=complex(*entry['z']);R=np.array(entry['complex_residue_matrix_real'])+1j*np.array(entry['complex_residue_matrix_imag'])
    h=1e-7
    estimate=(h*np.linalg.inv(k.operator(z+h)[0])-h*np.linalg.inv(k.operator(z-h)[0]))/2
    err=float(np.linalg.norm(estimate-R)/np.linalg.norm(R));complex_residue_errors.append(err)
    check(f'complex_scalar_{i}_residue_inverse_limit',err<2e-5,err,2e-5)
results['controls']['complex_residue_inverse_max_error']=max(complex_residue_errors)
branch=PREVIOUS['branches']['0.01'];p=branch['profiles']['minus']
_,_,_,_,HH=alls.full_geometry_hessian(p['x'],branch['alpha'],p['c'],levels=16)
kr=TwoPoint(p['x'],HH[:3,:3],levels=16,quadrature=96);kq=TwoPoint(p['x'],np.array(p['potential_Hessian'])[:3,:3],quadrature=64)
shifts=[]
for sector,data in complex_results.items():
    for entry in data['upper_half_plane_roots']:
        z=complex(*entry['z'])
        for label,other in [('cutoff',kr),('quadrature',kq)]:
            if sector=='tensor':zz=polish(lambda z:other.gravity(z)[0],lambda z:other.gravity(z)[3],z)
            else:zz=polish(other.determinant,other.determinant_prime,z)
            shifts.append({'sector':sector,'z':[z.real,z.imag],'control':label,'shift':float(abs(zz-z))})
err=max(r['shift'] for r in shifts);check('complex_pole_cutoff_quadrature_refinement',err<2e-7,err,2e-7)
results['controls']['complex_pole_refinement']=shifts
zplot=np.linspace(0,20,201)
results['plot_data']={'z':zplot,'tensor_A_over_f':[k.gravity(z)[0]/k.f for z in zplot]}
results['caveats']=[
'Exact quadratic external-momentum dependence of the declared warped family; finite numerical fermion cutoffs, not a complete compactification fluctuation calculation.',
'Potential counterterm and flatness subtraction remain selected inputs with covariant volume factor and no independent derivative/curvature operators. Additional operators alter the result.',
'Formal direct continuation z=-s-i0 is tested. Entire form factors do not select a causal quantum contour or establish reflection positivity, temperedness, ultraviolet unitarity or quantum completion.',
'Positive-z tensor and coupled neutral poles are tachyonic under this continuation. Their negative residues and non-real poles obstruct a healthy unrestricted interpretation of the minimal action; above-cutoff pole locations are not empirical particles.',
'The ordinary massless gravitational constraint is not counted as a scalar ghost. A zero of the eliminated metric denominator B(z) is not a pole unless the full operator is singular.',
'All nine fixed-metric scalar entries are supplied, but pole tests concern the closed CP-even neutral/metric and TT sectors. Charged vectors, gauge/axion constraints, higher harmonics, nonspherical metric modes and omitted tadpoles remain unresolved.',
'No global zero enumeration, interval enclosure or uniform tail certificate. Contour counts, finite search domains, near-degenerate complex poles and float64 limitations are explicit.',
'No quantum loops, profile selection, kappa/Lambda normalization, measured coupling fit, running or empirical prediction. The measured fine-structure constant remains unexplained.',
'AI-assisted same-session self-audit, no separate agent or external peer review; no priority claim for nonlocal heat-kernel or spectral-action methods.'
]
checks={'checks':CHECKS,'passed':sum(q['passed'] for q in CHECKS.values()),'total':len(CHECKS),
'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()},
'input_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((HERE/'inputs').glob('*'))}}
(HERE/'results.json').write_text(json.dumps(results,default=serial,indent=2)+'\n')
(HERE/'checks.json').write_text(json.dumps(checks,default=serial,indent=2)+'\n')
print('PASS',checks['passed'],'/',checks['total'],flush=True)
if checks['passed']!=checks['total']:raise SystemExit(1)
