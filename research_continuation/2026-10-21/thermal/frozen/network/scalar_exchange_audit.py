"""Diagnostic only: known Higgs-exchange scalar 2->2 channels.

Unknown independent singlet quartics/cubics are not set by the supplied
scattering benchmark. This computes only s/t/u Higgs exchange, O(K^4) in
the cross section, and does not add these nonlinear kernels to evolution.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import kve,roots_legendre,gamma,gammaincc
from reaction_rates import MASS,MH,KABS,GAMMA_H,VEV,kallen,number_density,hubble

PAIRS=[(0,0),(0,1),(1,1)]
C,CW=roots_legendre(32)


def reduced(q,initial,final):
    a,b=initial;c,d=final
    ma,mb,mc,md=[MASS[k] for k in [a,b,c,d]]
    s=q*q
    li=kallen(s,ma,mb);lf=kallen(s,mc,md)
    if min(li,lf)<=0:return 0.
    pa,pf=math.sqrt(li)/(2*q),math.sqrt(lf)/(2*q)
    ea=(s+ma*ma-mb*mb)/(2*q)
    ec=(s+mc*mc-md*md)/(2*q);ed=(s+md*md-mc*mc)/(2*q)
    t=ma*ma+mc*mc-2*ea*ec+2*pa*pf*C
    u=ma*ma+md*md-2*ea*ed-2*pa*pf*C
    # Kij=K*r_i*r_j, r=(+1,-1): all three channel products have the
    # same sign for fixed external species, so that common sign cancels.
    amp=VEV**2*KABS**2*(1/complex(s-MH*MH,MH*GAMMA_H)
                            +1/(t-MH*MH)+1/(u-MH*MH))
    avg=float(np.dot(CW,np.abs(amp)**2)/2)
    return math.sqrt(li*lf)*avg/(16*math.pi*s*(1+(c==d)))


def thermal(T,initial,final):
    mi,mj=[MASS[k] for k in initial]
    q0=max(sum(MASS[k] for k in initial),sum(MASS[k] for k in final))
    pref=math.exp(-(q0-mi-mj)/T)/(4*mi**2*mj**2*kve(2,mi/T)*kve(2,mj/T))
    val=quad(lambda w: reduced(q0+T*w,initial,final)*math.exp(-w)*kve(1,q0/T+w),
             0,80,epsabs=1e-25,epsrel=2e-9,limit=200)[0]
    ampmax=VEV**2*KABS**2*(1/(MH*GAMMA_H)+2/(MH*MH-(MASS[1]-MASS[0])**2))
    moment=sum(math.comb(2,k)*q0**(2-k)*T**k*gamma(k+1)*gammaincc(k+1,80) for k in range(3))
    tailbound=(pref*ampmax**2/(16*math.pi*(1+(final[0]==final[1])))
               *kve(1,q0/T+80)*moment)
    return pref*val,tailbound


def main():
    rows=[]
    for T in [1/3,.4,.5]:
        ns=np.array([number_density(T,m) for m in MASS])
        values=np.array([[thermal(T,a,b) for b in PAIRS] for a in PAIRS])
        matrix=values[:,:,0];bounds=values[:,:,1]
        per_pair=matrix.sum(axis=1)
        tagged=np.array([ns[0]*per_pair[0]+ns[1]*per_pair[1],
                         ns[0]*per_pair[1]+ns[1]*per_pair[2]])/hubble(T)
        maxreciprocity=0.
        for a,initial in enumerate(PAIRS):
            ni=ns[initial[0]]*ns[initial[1]]/(1+(initial[0]==initial[1]))
            for b,final in enumerate(PAIRS):
                nf=ns[final[0]]*ns[final[1]]/(1+(final[0]==final[1]))
                maxreciprocity=max(maxreciprocity,abs(ni*matrix[a,b]/(nf*matrix[b,a])-1))
        rows.append(dict(T_GeV=T,pair_order=['11','12','22'],
                         sigma_v_initial_to_final_GeV_m2=matrix.tolist(),
                         omitted_thermal_tail_upper_bounds_GeV_m2=bounds.tolist(),
                         maximum_omitted_tail_bound_relative_to_integral=float(np.max(bounds/matrix)),
                         tagged_total_collision_rates_over_H=tagged.tolist(),
                         equilibrium_average_tagged_rate_over_H=float(ns@tagged/ns.sum()),
                         event_reciprocity_max_relative_error=maxreciprocity))
    data=dict(scope='Minimal h-exchange scalar-only diagnostic; not part of evolved leading portal K^2 fermionic network',
              cross_section_order='K^4',vev_GeV=VEV,unknown_independent_singlet_couplings_included=False,
              integration_wmax=80,full_remote_resonance_bound_in_this_diagnostic=True,
              rows=rows)
    Path(__file__).with_name('scalar_exchange_audit.json').write_text(json.dumps(data,indent=2)+'\n')
    for row in rows: print({k:v for k,v in row.items() if 'matrix' not in k and 'sigma_v' not in k})

if __name__=='__main__':main()
