"""Offline two-derivative dynamics calculation and targeted verification.

Reuses the sealed tuned coordinates, checks their equations with fixed alpha
and c, and writes results.json/checks.json. A failed check exits nonzero.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('VECLIB_MAXIMUM_THREADS','1')
import json,sys,platform,hashlib
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import eigh
import dynamics as d
import all_scalars as all_s
import independent_checks as independent

HERE=Path(__file__).resolve().parent
PREVIOUS=json.loads((HERE/'inputs/previous_vacuum_results.json').read_text())
CHECKS={}


def check(name,condition,metric=None,tolerance=None):
    CHECKS[name]={'passed':bool(condition)}
    if metric is not None:CHECKS[name]['metric']=float(metric)
    if tolerance is not None:CHECKS[name]['tolerance']=float(tolerance)
    if not condition:raise AssertionError((name,metric,tolerance))


def close(name,actual,target,tol):
    err=np.max(abs(np.asarray(actual)-np.asarray(target)))
    check(name,err<tol,err,tol)


def serial(obj):
    if isinstance(obj,np.ndarray):return obj.tolist()
    if isinstance(obj,np.generic):return obj.item()
    raise TypeError(type(obj).__name__)


results={'title':'Radion kinetics and scalar mixing in the exact spectral vacuum',
    'date':'2026-10-22','coordinates':all_s.NAMES,
    'normalization':'L_J=kappa Lambda^2/2 [f R4-G_AB dq^A dq^B]-kappa Lambda^4 W/(4 pi^2); signature (-+++). At each fixture choose f0=f_vac, so the Einstein and Jordan vacuum units coincide.',
    'status':'Two-external-derivative restricted scalar/gravity calculation. The squared masses are generalized eigenvalues of the truncated action, not poles of the complete momentum-dependent spectral theory.',
    'branches':{},'unbroken':{},'controls':{}}

for profile in ('minus','plus'):
    x=[d.v.RSTAR,0.,0.]
    f,df,G,E=d.spectral_geometry(x,profile)
    control=d.unbroken_heat_control(d.v.RSTAR,profile)
    close(profile+'_unbroken_independent_heat_sums',[f,df[0],G[0,0],E[0,0]],control,2e-13)
    close(profile+'_unbroken_no_radion_scalar_mixing',E[0,1:],0.,1e-14)
    results['unbroken'][profile]={'f':f,'df':df,'Jordan_metric':G,'Einstein_metric':E}
close('inherited_common_gravity',results['unbroken']['minus']['f'],float(d.v.INPUT['metrics']['minus']['J'])/(24*np.pi**2),2e-14)
close('profile_common_gravity_at_unbroken_radius',results['unbroken']['minus']['f'],results['unbroken']['plus']['f'],2e-14)

for eps,old in PREVIOUS['tuned_flat_fixtures'].items():
    case={'alpha':old['alpha'],'profiles':{}}
    for profile,record in old['profiles'].items():
        name=eps+'_'+profile; x=np.array(record['x']);alpha=old['alpha'];c=record['c']
        p,grad,H3=d.v.tuned_spectral(x,alpha,profile,levels=12)
        grad[0]-=2*c*x[0];H3[0,0]-=2*c
        close(name+'_fixed_c_stationarity',grad,0.,2e-11)
        close(name+'_flatness',p-c*x[0]**2,0.,2e-12)
        f,df,G,E,H=all_s.full_geometry_hessian(x,alpha,c,profile,levels=12)
        f3,df3,G3,E3=d.spectral_geometry(x,profile,levels=12)
        close(name+'_independent_neutral_assembly',E[:3,:3],E3,2e-13)
        close(name+'_independent_gravity_assembly',np.r_[f,df[:3]],np.r_[f3,df3],2e-14)
        close(name+'_neutral_Hessian_preserved',H[:3,:3],H3,1e-10)
        close(name+'_inherited_scalar_metric',G[1:3,1:3],record['scalar_amplitude_kinetic_metric'],3e-13)
        close(name+'_inherited_charged_curvature',np.linalg.eigvalsh(H[5:7,5:7])[-1],record['charged_Cartesian_eigenvalue_twice'],1e-10)
        f16,df16,G16,E16,H16=all_s.full_geometry_hessian(x,alpha,c,profile,levels=16)
        close(name+'_cutoff_12_16_metric',E,E16,2e-12)
        close(name+'_cutoff_12_16_Hessian',H,H16,1e-10)
        evalG=np.linalg.eigvalsh(E);evalH=np.linalg.eigvalsh(H)
        check(name+'_positive_gravitational_coefficient',f>0,f)
        check(name+'_positive_full_Einstein_metric',evalG.min()>0,evalG.min())
        check(name+'_Jordan_radion_negative',G[0,0]<0,G[0,0])
        check(name+'_five_positive_potential_directions',np.count_nonzero(evalH>1e-9)==5)
        close(name+'_four_symmetry_flat_directions',evalH[:4],0.,1e-9)
        mass,modes=d.eigenmodes(H,E)
        m3,U3=d.eigenmodes(H3,E3)
        close(name+'_generalized_eigen_residual',H@modes/(4*np.pi**2)-(E@modes)*mass[None,:],0.,1e-12)
        close(name+'_canonical_normalization',modes.T@E@modes,np.eye(9),2e-12)
        m16,_=d.eigenmodes(H16,E16)
        close(name+'_cutoff_12_16_masses',mass,m16,1e-9)
        check(name+'_positive_massive_scalar_parameters',mass[4:].min()>0,mass[4:].min())
        # A constant invertible change to (R,H_d/Lambda,H_u/Lambda).
        EY,J=d.geometry_in_H_coordinates(x,E3)
        close(name+'_field_coordinate_mass_invariance',d.eigenmodes(J.T@H3@J,EY)[0],m3,1e-12)
        # At fixed flat metric the Einstein addition is exactly the conformal completion.
        close(name+'_Weyl_rank_one_completion',E-G,1.5*np.outer(df,df)/f,2e-15)
        close(name+'_charged_pair_degeneracy',mass[4],mass[5],1e-10)
        # A gauge-invariant potential has no curvature on neutral phases.
        close(name+'_neutral_phase_Hessian',H[3:5,3:5],0.,1e-9)
        # Independent neutral gauge response must agree with covariantizing
        # the two phase directions (a low-momentum Ward-identity control).
        R,hd,hu=x
        charge_tangents=np.array([[-hd/2,hd/2,hd],[hu/2,-hu/2,hu]])
        _,mass_nodes=d.m.full_response(R,d.v.NODES,hd,hu,levels=12)
        gauge_mass=np.tensordot(d.v.WEIGHTS[profile],mass_nodes,axes=1)
        close(name+'_neutral_gauge_phase_Ward_identity',gauge_mass,
              charge_tangents.T@E[3:5,3:5]@charge_tangents,2e-12)
        # Fractional radial participation: projection onto the unit metric-normal
        # to constant-R slices, rather than a coordinate-dependent vector entry.
        invE=np.linalg.inv(E3)
        radial_fraction=U3[0,:]**2/invE[0,0]
        close(name+'_radial_participation_sum',radial_fraction.sum(),1.,2e-13)
        case['profiles'][profile]={'x':x,'c':c,'f':f,'df':df,'Jordan_metric':G,
            'Einstein_metric':E,'Einstein_metric_eigenvalues':evalG,
            'potential_Hessian':H,'potential_Hessian_eigenvalues':evalH,
            'squared_mass_parameters_over_Lambda2':mass,'G_orthonormal_modes':modes,
            'neutral_squared_mass_parameters':m3,'neutral_G_orthonormal_modes':U3,
            'neutral_radial_participation':radial_fraction,
            'neutral_kinetic_correlation':E3/np.sqrt(np.outer(np.diag(E3),np.diag(E3))),
            'neutral_gauge_Higgs_mass_matrix':gauge_mass,'neutral_phase_charge_tangents':charge_tangents,
            'radial_metric_after_kinetic_diagonalization':1/invE[0,0],
            'largest_rate_m2_over4':d.v.NODES.max()*m3/4,
            'radion_parameter_over_first_spectator_KK_mass':np.sqrt(m3[-1])*x[0],
            'cutoff_metric_change':np.max(abs(E-E16)),
            'cutoff_mass_change':np.max(abs(mass-m16))}
        print(name,'minimum G_E',evalG.min(),'neutral m2',m3,flush=True)
    a,b=case['profiles']['minus'],case['profiles']['plus']
    case['plus_minus_difference']={'f':b['f']-a['f'],
        'Einstein_radial_metric':b['Einstein_metric'][0,0]-a['Einstein_metric'][0,0],
        'neutral_squared_mass_parameters':b['neutral_squared_mass_parameters']-a['neutral_squared_mass_parameters']}
    results['branches'][eps]=case

x=np.array(PREVIOUS['tuned_flat_fixtures']['0.01']['profiles']['minus']['x'])
f,df,G,E=d.spectral_geometry(x,levels=3)
integral=independent.matrix_integral_metric(x,levels=3)
close('direct_matrix_exponential_radion_scalar_metric',G,integral,2e-11)
results['controls']['independent_matrix_integral_max_error']=np.max(abs(G-integral))
old=PREVIOUS['tuned_flat_fixtures']['0.01']
f9,df9,G9,E9,H9=all_s.full_geometry_hessian(x,old['alpha'],old['profiles']['minus']['c'],levels=3)
dense=independent.dense_charged_kinetic(x,levels=3)
close('dense_angular_charged_metric',G9[5:7,5:7],dense,2e-11)
results['controls']['independent_dense_charged_metric_max_error']=np.max(abs(G9[5:7,5:7]-dense))

f,df,G,E=d.spectral_geometry(x,levels=12)
fd=independent.finite_gravity_gradient(x,'minus',d.spectral_geometry)
close('gravity_gradient_finite_differences',df,fd,2e-10)
results['controls']['gravity_gradient_max_error']=np.max(abs(df-fd))
s4=independent.sphere4_gravity(x)
close('external_S4_curvature_gravity_normalization',s4['Richardson'][-1],f,2e-9)
results['controls']['external_S4']=s4

# Low-q kernel uses numerical quadrature rather than analytic heat moments.
small=d.fixed_metric_momentum_delta(x,1e-5,levels=8,quadrature=64)
close('finite_momentum_derivative_limit',small,G,2e-6)
qs=[1e-5,.01,.1,float(results['branches']['0.01']['profiles']['minus']['neutral_squared_mass_parameters'][-1])]
momentum=[]
for q2 in qs:
    kernel=d.fixed_metric_momentum_delta(x,q2,levels=10,quadrature=64)
    momentum.append({'Euclidean_q2':q2,'fixed_Jordan_metric_kernel':kernel,
                     'RR_relative_change':(kernel[0,0]-G[0,0])/G[0,0],
                     'neutral_amplitude_relative_norm_change':np.linalg.norm(kernel[1:,1:]-G[1:,1:])/np.linalg.norm(G[1:,1:])})
results['controls']['fixed_metric_momentum_diagnostic']=momentum

# Independent 6D Einstein-Hilbert reduction: f~A R^2, G_RR~-2A,
# G_E,RR~4A. This is a limit, not the value at R_star.
m2=np.dot(d.v.WEIGHTS['minus'],d.v.NODES**-2);A=7*m2/(3*np.pi**2)
large=[]
for R in (16.,32.,64.,128.):
    ff,ffp,gg,ee=d.unbroken_heat_control(R,levels=int(12*R/np.sqrt(d.v.NODES.min())))
    large.append({'R':R,'f_over_R2':ff/R**2,'df_over_2R':ffp/(2*R),'Jordan_RR':gg,'Einstein_RR':ee})
close('large_radius_Einstein_Hilbert_reduction',[ff/R**2,ffp/(2*R),gg,ee],[A,A,-2*A,4*A],1e-5)
results['controls']['six_dimensional_EH_limit']={'A':A,'samples':large}

# The potential Hessian is unchanged at a flat stationary point by a Weyl
# factor; verify the field-dependent potential independently by finite differences.
c=old['profiles']['minus']['c'];alpha=old['alpha'];f0=f
def einstein_potential(y):
    pp=d.v.tuned_spectral(y,alpha,order=0)[0]-c*y[0]**2
    fy=d.spectral_geometry(y,levels=8)[0]
    return (f0/fy)**2*pp/(4*np.pi**2)
I=np.eye(3);step=.0005;HE=np.zeros((3,3));base=einstein_potential(x)
for i in range(3):
    vals=[einstein_potential(x+k*step*I[i]) for k in (-2,-1,1,2)]
    HE[i,i]=(-vals[0]+16*vals[1]-30*base+16*vals[2]-vals[3])/(12*step**2)
    for j in range(i):
        HE[i,j]=HE[j,i]=sum(si*sj*einstein_potential(x+step*(si*I[i]+sj*I[j])) for si in (-1,1) for sj in (-1,1))/(4*step**2)
H=np.array(old['profiles']['minus']['radial_amplitude_Hessian'])/(4*np.pi**2)
close('Einstein_potential_Hessian_at_flat_vacuum',HE,H,3e-7)
results['controls']['Einstein_potential_Hessian_max_error']=np.max(abs(HE-H))

results['caveats']=[
    'Conditional torsion-free warped round sphere, fixed monopole connection, unit Yukawas, four copied blocks, and lowest scalar harmonics.',
    'Additional mass counterterm and flatness subtraction are chosen inputs, assumed to add no derivative or curvature operators. No independent gravitational/kinetic counterterms are included.',
    'All internal spectral orders are retained, but only two external derivatives in the Einstein action. The radion-dominated eigenvalue is near the cutoff, so it is not a certified physical pole.',
    'A Euclidean spectral trace is continued to a Lorentzian low-derivative action with kappa>0. Full nonlocal analytic continuation, reflection positivity, and higher-derivative graviton poles are not established.',
    'All eight retained scalar tangents and the radion have a positive Einstein kinetic matrix; omitted higher harmonics, metric/gauge fluctuations and their tadpoles are not solved. This is not full compactification stability.',
    'A potential-free axion with positive independent kinetic coefficient is an assumption. Four gauge directions are quotiented; one physical phase remains massless. Anomaly completion and the full axion/gauge dynamics are not derived.',
    'Finite-cutoff float64/complex128 values, not interval or uniform-tail certificates. Small profile differences have limited significant digits.',
    'No independent kappa or Lambda selection, measured coupling fit, quantum loops, running, or experimentally validated prediction. The measured fine-structure constant is unexplained.',
    'Same-session AI-assisted self-audit with independent computational methods; no separate-agent referee or external peer review.'
]
environment={'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()}
input_hashes={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((HERE/'inputs').glob('*.json'))}
checks={'checks':CHECKS,'passed':sum(c['passed'] for c in CHECKS.values()),'total':len(CHECKS),'environment':environment,'input_hashes':input_hashes}
(HERE/'results.json').write_text(json.dumps(results,default=serial,indent=2)+'\n')
(HERE/'checks.json').write_text(json.dumps(checks,default=serial,indent=2)+'\n')
print(f"PASS {checks['passed']}/{checks['total']}",flush=True)
