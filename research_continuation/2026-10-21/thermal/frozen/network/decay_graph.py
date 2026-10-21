"""Positive phi2 <-> phi1 f fbar graph in y=p/T cells.

Forward decay events are integrated against equilibrium parent populations.
The reverse three-body absorption events follow from the same conductances
by Maxwell-Boltzmann detailed balance. Total singlet count is conserved.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.special import roots_legendre, roots_laguerre, kve

from reaction_rates import MASS, FERMIONS, decay_differential, decay_width, number_density


def parent_cell_quadrature(T,lo,hi,order,tail_order,total_density):
    z=MASS[1]/T
    if np.isfinite(hi):
        points,weights=roots_legendre(order)
        y=(lo+hi)/2+(hi-lo)*points/2
        weights=weights*(hi-lo)/2
        e=np.hypot(z,y)
        metric=weights*T**3*y*y*np.exp(-e)/(2*math.pi**2*total_density)
    else:
        points,weights=roots_laguerre(tail_order)
        x0=math.hypot(z,lo)-z
        x=x0+points
        e=z+x
        y=np.sqrt(x*(2*z+x))
        metric=(weights*T**3*y*e*math.exp(-z-x0)
                /(2*math.pi**2*total_density))
    return y,metric


def spectral_nodes(mf,Nc,order):
    lo,hi=4*mf*mf,(MASS[1]-MASS[0])**2
    if lo>=hi: return np.empty(0),np.empty(0)
    points,weights=roots_legendre(order)
    theta=(points+1)*math.pi/4
    z=lo+(hi-lo)*np.sin(theta)**2
    dz=weights*math.pi/4*(hi-lo)*np.sin(2*theta)
    rates=dz*np.array([decay_differential(float(value),mf,Nc) for value in z])
    return z,rates


def decay_graph(T,edges,parent_order=8,spectral_order=64,tail_order=64):
    """Return physical D/N_eq (GeV), species-major; inverse is included.

    edges is the common y=p/T grid, ending in infinity. D is symmetric
    positive semidefinite. The mass generator is -D diag(pi)^(-1).
    No separate decay or inverse-decay rate should be added to that graph.
    """
    edges=np.asarray(edges,float)
    if edges[0]!=0 or not np.isinf(edges[-1]) or np.any(np.diff(edges)<=0):
        raise ValueError('edges must increase from0 to infinity')
    nb=len(edges)-1
    parent,daughter=MASS[1],MASS[0]
    densities=np.array([number_density(T,m) for m in MASS])
    total=float(densities.sum())
    target_energy_edges=np.hypot(daughter,T*edges)
    target_lo=target_energy_edges[:-1]
    target_hi=target_energy_edges[1:]
    spectral=[];widths={};quadrature_widths={}
    for name,mf,Nc in FERMIONS:
        z,rates=spectral_nodes(mf,Nc,spectral_order)
        widths[name]=decay_width(mf,Nc)
        quadrature_widths[name]=float(rates.sum())
        if len(z): spectral.append((z,rates))
    z=np.concatenate([item[0] for item in spectral])
    rate_weights=np.concatenate([item[1] for item in spectral])
    estar=(parent*parent+daughter*daughter-z)/(2*parent)
    kstar=np.sqrt(np.maximum(0.,(((parent-daughter)**2-z)*((parent+daughter)**2-z))))/(2*parent)
    flows=np.zeros((nb,nb)) # row daughter1 cell, column parent2 cell
    parent_mass_quadrature=0.
    maximum_angle_probability_error=0.
    for a,(lo,hi) in enumerate(zip(edges[:-1],edges[1:])):
        y,metric=parent_cell_quadrature(T,lo,hi,parent_order,tail_order,total)
        parent_mass_quadrature+=metric.sum()
        momentum=T*y
        energy=np.hypot(parent,momentum)
        gamma=energy/parent
        beta_gamma=momentum/parent
        central=gamma[:,None]*estar[None,:]
        halfwidth=beta_gamma[:,None]*kstar[None,:]
        # Analytic uniform-cosine CDF avoids cancellation when the daughter
        # energy interval is much narrower than a cell. The physical first
        # and last boundaries cover all allowed energies, exactly.
        cdf=np.clip((target_energy_edges[None,None,:]-central[:,:,None])
                    /halfwidth[:,:,None],-1.,1.)
        cdf[:,:,0]=-1.
        cdf[:,:,-1]=1.
        probabilities=np.diff(cdf,axis=-1)/2
        maximum_angle_probability_error=max(maximum_angle_probability_error,
                                            float(np.max(np.abs(probabilities.sum(axis=-1)-1))))
        weights=metric[:,None]*(parent/energy)[:,None]*rate_weights[None,:]
        flows[:,a]=np.einsum('ab,abc->c',weights,probabilities,optimize=True)
    D=np.zeros((2*nb,2*nb))
    D[:nb,nb:]=-flows
    D[nb:,:nb]=-flows.T
    D[np.arange(nb),np.arange(nb)]=flows.sum(axis=1)
    D[nb+np.arange(nb),nb+np.arange(nb)]=flows.sum(axis=0)
    count=float(flows.sum())
    total_width=sum(widths.values())
    expected_count=(densities[1]/total)*total_width*kve(1,parent/T)/kve(2,parent/T)
    norm=np.linalg.norm(D)
    return dict(T_GeV=T,edges_y=[None if np.isinf(x) else float(x) for x in edges],
                D_per_Neq_GeV=D.tolist(),
                quadrature=dict(parent_order=parent_order,spectral_order=spectral_order,tail_order=tail_order),
                vacuum_partial_widths_GeV=widths,
                spectral_quadrature_partial_widths_GeV=quadrature_widths,
                decay_forward_events_per_Neq_GeV=count,
                independent_thermal_forward_events_per_Neq_GeV=expected_count,
                thermal_event_relative_difference=count/expected_count-1,
                parent_metric_relative_difference=parent_mass_quadrature/(densities[1]/total)-1,
                maximum_angle_probability_sum_error=maximum_angle_probability_error,
                number_null_relative_residual=float(np.linalg.norm(D@np.ones(2*nb))/norm),
                inverse_absorption_included_by_detailed_balance=True,
                total_scalar_number_changing=False,
                construction='Forward decay equilibrium event weights, exact isotropic daughter-angle bin probabilities; reverse absorbed pair supplied by detailed balance')


def decay_conductance(T,edges,**kwargs):
    """Return (W_per_Neq_GeV, metadata), with W positive off-diagonal.

    Root's eta generator may add W/H to its scattering conductances.
    """
    data=decay_graph(T,edges,**kwargs)
    D=np.asarray(data.pop('D_per_Neq_GeV'))
    W=-D
    np.fill_diagonal(W,0.)
    return W,data


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--temperature',type=float,default=.4)
    parser.add_argument('--step',type=float,default=.25)
    parser.add_argument('--last',type=float,default=48)
    parser.add_argument('--parent-order',type=int,default=8)
    parser.add_argument('--spectral-order',type=int,default=64)
    parser.add_argument('--tail-order',type=int,default=64)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('decay_graph_T0p4.json'))
    args=parser.parse_args()
    edges=np.r_[np.arange(0,args.last+args.step/2,args.step),np.inf]
    result=decay_graph(args.temperature,edges,args.parent_order,args.spectral_order,args.tail_order)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if k not in ['D_per_Neq_GeV','edges_y']})
