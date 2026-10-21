"""Expanding comoving cell evolution with fermionic annihilation and decay.

M_a = a^3 n_a / n_eq,total(T0), a=T0/T. Scattering and decay conserve
sum(M); pair annihilation and its inverse source change that sum.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'solver'))
from expanding_free_bath import ScatteringBank, cell_data, hubble, neq, observables, T0, TF
from pair_annihilation import pair_kernel, positive_step, rhs, WIDTH


def make_pair_bank(scatter_path,output,radial_order=4,angular_order=24,intervals=None,reuse_bank=None):
    with np.load(scatter_path) as z:
        edges=z['edges'].copy();eta=z['eta'].copy()
    if intervals is not None:
        eta=np.unique(np.r_[np.linspace(0,math.log(T0/TF),intervals+1),math.log(T0/.4)])
    cached={}
    if reuse_bank is not None:
        with np.load(reuse_bank) as z:
            old_meta=json.loads(str(z['metadata']))
            if not np.array_equal(edges,z['edges']):raise ValueError('Reuse bank grid mismatch')
            if (old_meta['radial_order'],old_meta['angular_order'],old_meta['width_GeV'])!=(radial_order,angular_order,WIDTH):
                raise ValueError('Reuse bank quadrature or width mismatch')
            cached={round(float(e),13):A.copy() for e,A in zip(z['eta'],z['kernels'])}
    kernels=[]
    start=time.perf_counter()
    for k,e in enumerate(eta):
        begin=time.perf_counter();T=T0*math.exp(-e)
        key=round(float(e),13)
        kernels.append(cached[key] if key in cached else pair_kernel(T,edges,radial_order,angular_order))
        print(f'pair node {k+1}/{len(eta)} T={T:.8g} elapsed={time.perf_counter()-begin:.3f}s reused={key in cached}',flush=True)
    metadata={'width_GeV':WIDTH,'radial_order':radial_order,'angular_order':angular_order,
              'units':'GeV^-2, conditional equilibrium cell average of sigma*v_M',
              'elapsed_seconds':time.perf_counter()-start,'inverse_source':'same kernel at exact instantaneous zero-mu equilibrium cell masses'}
    np.savez_compressed(output,edges=edges,eta=eta,kernels=np.asarray(kernels),metadata=json.dumps(metadata))
    Path(output).with_suffix('.json').write_text(json.dumps(metadata,indent=2)+'\n')


def interpolation(eta,nodes,values):
    k=min(max(np.searchsorted(nodes,eta)-1,0),len(nodes)-2)
    w=(eta-nodes[k])/(nodes[k+1]-nodes[k])
    if w < -1e-10 or w>1+1e-10:raise ValueError('Requested time outside reaction bank')
    return (1-w)*values[k]+w*values[k+1]


def aggregation_map(fine_edges,coarse_edges):
    fine=len(fine_edges)-1;coarse=len(coarse_edges)-1
    P=np.zeros((2*fine,2*coarse))
    for species in range(2):
        for k in range(fine):
            # Each coarse edge must be a fine edge; aggregate last cells into infinity.
            target=np.searchsorted(coarse_edges[1:-1],fine_edges[k]+1e-10)
            P[species*fine+k,species*coarse+target]=1.
    return P


class ReactionBank:
    def __init__(self,pair_path,decay_path,edges,temperature_stride=1):
        with np.load(pair_path) as z:
            self.eta=z['eta'].copy();fine_edges=z['edges'].copy()
            self.A=z['kernels'].copy();self.pair_metadata=json.loads(str(z['metadata']))
        with np.load(decay_path) as z:
            self.decay_eta=z['eta'].copy();decay_edges=z['edges'].copy()
            self.decayW=z['conductances'].copy()
            units=str(z['conductance_units'])
        self.decay_metadata=json.loads(Path(decay_path).with_suffix('.json').read_text())
        if not np.array_equal(fine_edges,decay_edges):raise ValueError('Incompatible reaction grids')
        if units!='GeV; normalized by N_eq(T); not divided by H':
            raise ValueError('Explicit decay normalization metadata required')
        # Convert physical decay conductances to the scattering bank's dimensionless convention.
        self.decayW/=np.asarray([hubble(T0*math.exp(-e)) for e in self.decay_eta])[:,None,None]
        self.edges=np.asarray(edges)
        if not np.array_equal(fine_edges,self.edges):
            P=aggregation_map(fine_edges,self.edges)
            aggregated=[]
            for e,A in zip(self.eta,self.A):
                pi=cell_data(T0*math.exp(-e),fine_edges)[:,:,0].ravel()
                co=P.T@pi
                aggregated.append((P.T@(A*np.outer(pi,pi))@P)/np.outer(co,co))
            self.A=np.asarray(aggregated)
            self.decayW=np.asarray([P.T@W@P for W in self.decayW])
            for W in self.decayW:np.fill_diagonal(W,0.)
        if temperature_stride!=1:
            def keep_nodes(nodes):
                regular=np.linspace(0,math.log(T0/TF),len(nodes)-1)
                requested=np.r_[regular[::temperature_stride],regular[-1],math.log(T0/.4)]
                return [k for k,e in enumerate(nodes) if np.min(np.abs(requested-e))<1e-12]
            keep=keep_nodes(self.eta);self.eta=self.eta[keep];self.A=self.A[keep]
            keep=keep_nodes(self.decay_eta);self.decay_eta=self.decay_eta[keep];self.decayW=self.decayW[keep]

    def kernel(self,eta):
        return interpolation(eta,self.eta,self.A)

    def decay_conductance(self,eta):
        return interpolation(eta,self.decay_eta,self.decayW)


def evolve(scatter_path,pair_path,decay_path,steps=192,aggregation=1,temperature_stride=1,
           use_scattering=True,use_decay=True,use_annihilation=True,save_every=4,tail_ymax=None):
    scatter=ScatteringBank(scatter_path,aggregation,temperature_stride,tail_ymax)
    reactions=ReactionBank(pair_path,decay_path,scatter.edges,temperature_stride)
    end=math.log(T0/TF)
    observation_T=[T0,.45,.4,.375,TF]
    times=np.unique(np.r_[np.linspace(0,end,steps+1),np.log(T0/np.asarray(observation_T))])
    n0=neq(T0)
    initial=cell_data(T0,scatter.edges)[:,:,0].ravel()
    mass=initial.copy();rows=[]
    max_linear_number_error=0.
    min_population=float(mass.min())
    initial_entropy=2*math.pi**2/45*60*T0**3
    for k,e in enumerate(times):
        T=T0*math.exp(-e)
        snapshot=any(abs(T-v)<1e-12 for v in observation_T)
        if snapshot or k%save_every==0:
            row=observables(mass,T,scatter.edges,snapshot)
            row['yield_Y_total']=row['comoving_number_relative_to_initial']*n0/initial_entropy
            rows.append(row)
        if k+1==len(times):break
        dt=times[k+1]-e;mid=e+dt/2;Tm=T0*math.exp(-mid);a=T0/Tm
        data=cell_data(Tm,scatter.edges);pi=data[:,:,0].ravel()
        eq=a**3*neq(Tm)/n0*pi
        alpha=n0/a**3/hubble(Tm)
        A=reactions.kernel(mid)
        if use_annihilation:
            mass=positive_step(mass,dt/2,A,eq,alpha)
        W=np.zeros((len(mass),len(mass)))
        if use_scattering:W+=scatter.conductance(mid)
        if use_decay:W+=reactions.decay_conductance(mid)
        if use_scattering or use_decay:
            Q=W.copy();np.fill_diagonal(Q,-W.sum(axis=1));Q/=pi[None,:]
            before=float(mass.sum())
            mass=expm_multiply(csr_matrix(Q*dt),mass,traceA=float(np.trace(Q)*dt))
            max_linear_number_error=max(max_linear_number_error,abs(float(mass.sum())-before))
        if use_annihilation:
            mass=positive_step(mass,dt/2,A,eq,alpha)
        min_population=min(min_population,float(mass.min()))
        if np.min(mass)<0 or not np.isfinite(mass).all():raise ValueError('Nonpositive or nonfinite population')
    return {'model':'Expanding ideal MB free-fermion bath with specified Higgs-portal fermionic channels',
            'T0_GeV':T0,'Tf_GeV':TF,'gstar':60,'gstar_s':60,'initial_chemical_potentials':0.,
            'coordinate':'y=p/T, eta=ln(T0/T)','mass_variable':'M_a=a^3 n_a/n_eq,total(T0)',
            'finite_y_cells_per_species':len(scatter.edges)-2,
            'edges_y':[float(v) if np.isfinite(v) else None for v in scatter.edges],
            'eta_steps_nominal':steps,'eta_steps_actual':len(times)-1,
            'temperature_stride':temperature_stride,
            'channels':{'scattering':use_scattering,'decay_and_inverse':use_decay,'annihilation_and_inverse':use_annihilation},
            'scattering_metadata':scatter.metadata,'pair_metadata':reactions.pair_metadata,
            'decay_metadata':reactions.decay_metadata,
            'max_single_linear_step_number_error':max_linear_number_error,
            'minimum_comoving_cell_mass':min_population,
            'initial_number_density_GeV3':n0,'initial_yield_Y':n0/initial_entropy,
            'final_fractional_number_change':float(mass.sum()/initial.sum()-1),
            'QCD_medium_calculated':False,'physical_relic_abundance_claim':False,
            'rows':rows}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    bank=sub.add_parser('make-pair-bank')
    bank.add_argument('--scattering-bank',type=Path,required=True)
    bank.add_argument('--output',type=Path,required=True)
    bank.add_argument('--radial-order',type=int,default=4)
    bank.add_argument('--angular-order',type=int,default=24)
    bank.add_argument('--intervals',type=int)
    bank.add_argument('--reuse-bank',type=Path)
    run=sub.add_parser('evolve')
    run.add_argument('--scattering-bank',type=Path,required=True)
    run.add_argument('--pair-bank',type=Path,required=True)
    run.add_argument('--decay-bank',type=Path,required=True)
    run.add_argument('--output',type=Path,required=True)
    run.add_argument('--steps',type=int,default=192)
    run.add_argument('--aggregation',type=int,default=1)
    run.add_argument('--temperature-stride',type=int,default=1)
    run.add_argument('--tail-ymax',type=float)
    run.add_argument('--no-scattering',action='store_true')
    run.add_argument('--no-decay',action='store_true')
    run.add_argument('--no-annihilation',action='store_true')
    args=parser.parse_args()
    if args.command=='make-pair-bank':
        make_pair_bank(args.scattering_bank,args.output,args.radial_order,args.angular_order,args.intervals,args.reuse_bank)
    else:
        result=evolve(args.scattering_bank,args.pair_bank,args.decay_bank,args.steps,args.aggregation,
                      args.temperature_stride,not args.no_scattering,not args.no_decay,not args.no_annihilation,
                      tail_ymax=args.tail_ymax)
        args.output.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result['rows'][-1].items() if k!='comoving_cell_masses'},indent=2))
