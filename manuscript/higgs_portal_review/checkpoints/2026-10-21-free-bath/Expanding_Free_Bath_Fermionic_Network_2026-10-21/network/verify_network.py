"""Regenerate the targeted decay-shape and width-sensitivity checks."""
import json,math
from pathlib import Path
import numpy as np
from decay_graph import decay_conductance
from reaction_rates import thermal_annihilation,FERMIONS,MASS,GAMMA_H

HERE=Path(__file__).resolve().parent


def main():
    bank=np.load(HERE/'decay_bank.npz')
    edges=bank['edges'];eta=bank['eta']
    k=int(np.argmin(abs(eta-math.log(1.25))))
    T=.5*math.exp(-float(eta[k]))
    W0=bank['conductances'][k]
    W1,metadata=decay_conductance(T,edges,parent_order=16,spectral_order=128,tail_order=96)
    D0=np.diag(W0.sum(axis=1))-W0;D1=np.diag(W1.sum(axis=1))-W1
    nb=len(edges)-1
    centers=np.empty(nb)
    centers[:-1]=(edges[:-2]+edges[1:-1])/2
    centers[-1]=edges[-2]+1
    energy=np.concatenate([np.hypot(m,T*centers)/T for m in MASS])
    pop=np.r_[np.zeros(nb),np.ones(nb)]
    result=dict(T_GeV=T,coarse_orders=[8,64,64],fine_orders=[16,128,96],
        shape_definition='E_i(y_midpoint)/T, with y=ymax+1 for the aggregate tail; a smooth diagnostic shape, not a resolved-tail asymptotic claim',
        conductance_relative_Frobenius_change=float(np.linalg.norm(W1-W0)/np.linalg.norm(W1)),
        D_relative_Frobenius_change=float(np.linalg.norm(D1-D0)/np.linalg.norm(D1)),
        total_event_relative_change=float(W1.sum()/W0.sum()-1),
        energy_shape_form_relative_change=float(energy@D1@energy/(energy@D0@energy)-1),
        population_energy_cross_form_relative_change=float(pop@D1@energy/(pop@D0@energy)-1),
        fine_metadata=metadata)
    for width in [GAMMA_H/2,GAMMA_H*2,GAMMA_H+1.9e-5]:
        largest=0.
        for temperature in [1/3,.4,.5]:
            for i,mi in enumerate(MASS):
                for j,mj in enumerate(MASS):
                    if i>j:continue
                    original=sum(thermal_annihilation(temperature,mi,mj,m,Nc)['value_GeV_m2'] for _,m,Nc in FERMIONS)
                    varied=sum(thermal_annihilation(temperature,mi,mj,m,Nc,width)['value_GeV_m2'] for _,m,Nc in FERMIONS)
                    largest=max(largest,abs(varied/original-1))
        result.setdefault('annihilation_width_sensitivity',[]).append(dict(
            width_GeV=width,maximum_relative_change=largest,temperatures_GeV=[1/3,.4,.5]))
    (HERE/'decay_graph_convergence.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(HERE/'decay_T0p4_refined.npz',edges=edges,conductances=W1)
    print({key:value for key,value in result.items() if key not in ['fine_metadata','annihilation_width_sensitivity']})


if __name__=='__main__':main()
