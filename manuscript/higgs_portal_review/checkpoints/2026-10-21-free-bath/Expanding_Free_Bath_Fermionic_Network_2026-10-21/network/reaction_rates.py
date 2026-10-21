"""Independent invariant thermal rates for the declared free-fermion network.

Tree portal normalization: L = -(v/2) h sum_ij Kij phi_i phi_j.
The timelike annihilation propagator has an explicitly declared constant width.
Natural GeV units. These are ideal MB/vacuum rates, not a QCD calculation.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

from scipy.integrate import quad
from scipy.special import kve, gamma, gammaincc

MASS = (10., 11.5)
MH = 125.
KABS = .001
GAMMA_H = .0041
VEV = 246.22
FERMIONS = [('e', .00051099895, 1), ('mu', .1056583755, 1),
            ('tau', 1.77686, 1), ('u', .002, 3), ('d', .005, 3),
            ('s', .100, 3), ('c', 1.300, 3), ('b', 4.200, 3)]


def hubble(T):
    return math.sqrt(8*math.pi**3*60/90)*T*T/1.2209e19


def number_density(T, mass):
    return mass*mass*T*math.exp(-mass/T)*kve(2,mass/T)/(2*math.pi**2)


def kallen(s,mi,mj):
    return max(0., (s-(mi+mj)**2)*(s-(mi-mj)**2))


def annihilation_sigma_v(p_i,p_j,cosine,mi,mj,mf,Nc=1,width=GAMMA_H):
    Ei,Ej=math.hypot(p_i,mi),math.hypot(p_j,mj)
    s=mi*mi+mj*mj+2*(Ei*Ej-p_i*p_j*cosine)
    if s<=4*mf*mf: return 0.
    den=(s-MH*MH)**2+(MH*width)**2
    return Nc*KABS**2*mf**2*(s-4*mf**2)**1.5/(16*math.pi*math.sqrt(s)*Ei*Ej*den)


def annihilation_reduced(q,mi,mj,mf,Nc=1,width=GAMMA_H):
    """lambda_initial*sigma, with final spin/color sum and no bath factor4."""
    s=q*q
    if q<=mi+mj or q<=2*mf: return 0.
    den=(s-MH*MH)**2+(MH*width)**2
    return Nc*KABS**2*mf**2*math.sqrt(kallen(s,mi,mj))*(s-4*mf**2)**1.5/(8*math.pi*q*den)


def thermal_annihilation(T,mi,mj,mf,Nc=1,width=GAMMA_H):
    """Return the thermal integral plus an upper bound on its remote tail.

    The finite positive width makes a simple global bound valid even through
    the thermally remote Higgs resonance; no resonance is silently skipped.
    """
    q0=max(mi+mj,2*mf)
    denominator=4*mi**2*mj**2*kve(2,mi/T)*kve(2,mj/T)
    # Main thermal part uses w=(q-q0)/T. The omitted remainder is bounded
    # with D_h(s)>=(MH*width)^2, including the narrow resonance.
    qsplit=min(q0+80*T, .8*MH)
    wsplit=(qsplit-q0)/T
    pref=math.exp(-(q0-mi-mj)/T)/denominator
    main,err=quad(lambda w: annihilation_reduced(q0+T*w,mi,mj,mf,Nc,width)
                  *math.exp(-w)*kve(1,q0/T+w),0,wsplit,
                  epsabs=1e-25,epsrel=3e-10,limit=200)
    moment=sum(math.comb(4,k)*q0**(4-k)*T**k*gamma(k+1)*gammaincc(k+1,wsplit)
               for k in range(5))
    bound=(Nc*KABS**2*mf**2/(8*math.pi*(MH*width)**2)
           *kve(1,qsplit/T)*moment)
    return dict(value_GeV_m2=pref*main,
                omitted_remote_tail_upper_bound_GeV_m2=pref*bound,
                quadrature_estimate_GeV_m2=pref*err,
                remote_split_q_GeV=qsplit)


def decay_differential(z,mf,Nc=1,parent=MASS[1],daughter=MASS[0]):
    """dGamma(phi2->phi1 f fbar)/dz, z=m_ffbar^2; no initial spin average."""
    if z<=4*mf*mf or z>=(parent-daughter)**2: return 0.
    lam=max(0., ((parent-daughter)**2-z)*((parent+daughter)**2-z))
    return (Nc*KABS**2*mf**2*math.sqrt(lam)*(z-4*mf**2)**1.5
            /(128*math.pi**3*parent**3*math.sqrt(z)*(MH*MH-z)**2))


def decay_width(mf,Nc=1,parent=MASS[1],daughter=MASS[0]):
    if parent-daughter<=2*mf: return 0.
    lo,hi=4*mf*mf,(parent-daughter)**2
    # Sine-squared substitution removes both square-root endpoints.
    def f(theta):
        z=lo+(hi-lo)*math.sin(theta)**2
        return 1e30*decay_differential(z,mf,Nc,parent,daughter)*(hi-lo)*math.sin(2*theta)
    return quad(f,0,math.pi/2,epsabs=1e-10,epsrel=1e-10,limit=200)[0]/1e30


def higgs_portal_width(mi,mj):
    if MH<=mi+mj: return 0.
    symmetry=2 if mi==mj else 1
    return VEV**2*KABS**2*math.sqrt(kallen(MH*MH,mi,mj))/(16*math.pi*MH**3*symmetry)


def run(temperatures):
    decay={name:decay_width(m,Nc) for name,m,Nc in FERMIONS}
    total_decay=sum(decay.values())
    hpartials={f'{i+1}{j+1}':higgs_portal_width(mi,mj)
               for i,mi in enumerate(MASS) for j,mj in enumerate(MASS) if i<=j}
    rows=[]
    for T in temperatures:
        n=[number_density(T,m) for m in MASS]; N=sum(n)
        fractions=[x/N for x in n]; H=hubble(T)
        channels={}; matrix=[[0.,0.],[0.,0.]]
        max_remote=0.
        for i,mi in enumerate(MASS):
            for j,mj in enumerate(MASS):
                if i>j: continue
                per_flavor={}
                for name,m,Nc in FERMIONS:
                    r=thermal_annihilation(T,mi,mj,m,Nc)
                    per_flavor[name]=r
                    max_remote=max(max_remote,r['omitted_remote_tail_upper_bound_GeV_m2']/r['value_GeV_m2'])
                value=sum(x['value_GeV_m2'] for x in per_flavor.values())
                matrix[i][j]=matrix[j][i]=value
                channels[f'{i+1}{j+1}']={'sigma_v_GeV_m2':value,
                    'event_density_GeV4':n[i]*n[j]*value/(1+(i==j)),
                    'per_flavor':per_flavor}
        effective=sum(fractions[i]*fractions[j]*matrix[i][j] for i in range(2) for j in range(2))
        decay_down=total_decay*kve(1,MASS[1]/T)/kve(2,MASS[1]/T)
        rows.append(dict(T_GeV=T,H_GeV=H,n_equilibrium_GeV3=n,
                         sigma_v_matrix_GeV_m2=matrix,channels=channels,
                         sigma_v_effective_GeV_m2=effective,
                         equilibrium_annihilation_loss_per_particle_over_H=N*effective/H,
                         common_fugacity_linearized_chemical_rate_over_H=2*N*effective/H,
                         maximum_remote_tail_upper_bound_fraction=max_remote,
                         decay_down_thermal_over_H=decay_down/H,
                         decay_up_thermal_over_H=decay_down*n[1]/n[0]/H,
                         decay_species_contrast_rate_over_H=decay_down*(1+n[1]/n[0])/H))
    return dict(model='same ideal MB free-fermion benchmark, crossed Higgs portal, constant timelike-width prescription',
                timelike_Higgs_width_GeV=GAMMA_H,
                timelike_width_is_new_declared_input=True,
                width_source='https://pdg.lbl.gov/2025/reviews/rpp2025-rev-higgs-boson.pdf',
                scalar_masses_GeV=MASS,
                vacuum_phi2_partial_widths_GeV=decay,
                vacuum_phi2_total_free_fermion_width_GeV=total_decay,
                vacuum_phi2_e_plus_mu_width_GeV=decay['e']+decay['mu'],
                inherited_e_plus_mu_reference_GeV=3.060267688e-22,
                h_to_scalar_partial_widths_GeV=hpartials,
                h_to_scalar_total_width_GeV=sum(hpartials.values()),
                rows=rows)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('reaction_rates.json'))
    parser.add_argument('--temperatures',type=float,nargs='+',default=[1/3,.4,.5,.6,.8,1.])
    args=parser.parse_args()
    data=run(args.temperatures)
    args.output.write_text(json.dumps(data,indent=2)+'\n')
    print('vacuum free-fermion decay width',data['vacuum_phi2_total_free_fermion_width_GeV'])
    print('e+mu width',data['vacuum_phi2_e_plus_mu_width_GeV'])
    for row in data['rows']:
        print({k:row[k] for k in ['T_GeV','equilibrium_annihilation_loss_per_particle_over_H',
              'common_fugacity_linearized_chemical_rate_over_H','decay_species_contrast_rate_over_H',
              'maximum_remote_tail_upper_bound_fraction']})
