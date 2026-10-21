#!/usr/bin/env python3
"""Prespecified synthetic causal-memory intervention experiment.

This experiment does not measure consciousness, human agency or a physical field.
Run: python synthetic_causal_memory.py
Dependencies: numpy, matplotlib. Protocol is hash-locked before data generation.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE=Path(__file__).resolve().parent


@dataclass(frozen=True)
class Partition:
    role: str
    ids: tuple[str,...]
    seed: int
    states: np.ndarray


@dataclass(frozen=True)
class FrozenPredictor:
    probabilities: np.ndarray
    marginal: float
    counts: np.ndarray
    train_digest: str


def digest(array):
    return hashlib.sha256(np.ascontiguousarray(array).tobytes()).hexdigest()


def generate(name,role,seed,n_trials,n_transitions,stay):
    rng=np.random.default_rng(seed)
    x=np.empty((n_trials,n_transitions+1),dtype=np.int8)
    x[:,0]=rng.integers(0,2,n_trials)
    flips=rng.random((n_trials,n_transitions))>=stay
    for t in range(n_transitions):
        x[:,t+1]=np.bitwise_xor(x[:,t],flips[:,t])
    x.setflags(write=False)
    return Partition(role,tuple(f'{name}-{role}-{i}' for i in range(n_trials)),seed,x)


def fit(train):
    # This guard runs before touching labels or counts.
    if train.role!='train':
        raise ValueError('Predictor fit accepts the training partition only.')
    prev=train.states[:,:-1].ravel()
    next_=train.states[:,1:].ravel()
    counts=np.bincount(2*prev+next_,minlength=4).reshape(2,2)
    probabilities=(counts[:,1]+1)/(counts.sum(axis=1)+2)
    marginal=float((next_.sum()+1)/(len(next_)+2))
    probabilities.setflags(write=False)
    counts.setflags(write=False)
    return FrozenPredictor(probabilities,marginal,counts,digest(train.states))


def reciprocal_derangement(n,seed):
    if n%2:
        raise ValueError('Reciprocal trial derangement needs an even trial count.')
    pairs=np.random.default_rng(seed).permutation(n).reshape(-1,2)
    donor=np.empty(n,dtype=int)
    donor[pairs[:,0]]=pairs[:,1]
    donor[pairs[:,1]]=pairs[:,0]
    return pairs,donor


def loss_per_trial(prediction,target,clip):
    p=np.clip(prediction,clip,1-clip)
    return {'brier':np.mean((prediction-target)**2,axis=1),
            'log':np.mean(-target*np.log(p)-(1-target)*np.log1p(-p),axis=1)}


def theoretical_losses(stay):
    return {'assumptions':'Infinite training; exact source transition probabilities and stationary balanced marginal',
            'brier':{'intact':stay*(1-stay),'reset':.25,
                     'cross_trial_swap':.25+(stay-.5)**2},
            'log':{'intact':-stay*math.log(stay)-(1-stay)*math.log1p(-stay),
                   'reset':math.log(2),
                   'cross_trial_swap':-.5*math.log(stay*(1-stay))}}


def main():
    protocol_bytes=(HERE/'protocol.json').read_bytes()
    protocol_hash=hashlib.sha256(protocol_bytes).hexdigest()
    locked_hash=(HERE/'protocol.sha256').read_text().split()[0]
    if protocol_hash!=locked_hash:
        raise RuntimeError('Protocol hash mismatch: do not alter protocol after seeing results.')
    protocol=json.loads(protocol_bytes)
    started=datetime.now(timezone.utc).isoformat()
    checks=[]
    def check(name,condition):
        if not bool(condition):
            raise AssertionError(name)
        checks.append({'name':name,'passed':True})
    all_seeds=[s[k] for s in protocol['source']['conditions'] for k in
               ['train_seed','test_seed','pairing_seed','bootstrap_seed']]
    check('all_rng_seeds_prespecified_and_distinct',len(set(all_seeds))==len(all_seeds))
    ntrain=protocol['sample']['training_trials_per_source']
    ntest=protocol['sample']['held_out_trials_per_source']
    nt=protocol['sample']['transitions_per_trial']
    nboot=protocol['uncertainty']['replicates']
    conditions=['intact','reset','cross_trial_swap','state_relabel']
    sources=[];csv_rows=[]
    for source in protocol['source']['conditions']:
        name=source['name'];stay=source['stay']
        train=generate(name,'train',source['train_seed'],ntrain,nt,stay)
        test=generate(name,'test',source['test_seed'],ntest,nt,stay)
        check(name+'_train_test_ids_disjoint',not set(train.ids)&set(test.ids))
        predictor=fit(train)
        try:
            fit(test)
        except ValueError:
            rejected=True
        else:
            rejected=False
        check(name+'_fit_rejects_held_out_partition',rejected)
        pairs,donor=reciprocal_derangement(ntest,source['pairing_seed'])
        pair_ids=np.empty(ntest,dtype=int)
        pair_ids[pairs[:,0]]=np.arange(len(pairs))
        pair_ids[pairs[:,1]]=np.arange(len(pairs))
        check(name+'_derangement_no_fixed_points',np.all(donor!=np.arange(ntest)))
        check(name+'_swap_is_reciprocal',np.array_equal(donor[donor],np.arange(ntest)))
        # Every condition receives bits strictly earlier than its target.
        previous=test.states[:,:-1]
        target=test.states[:,1:]
        swapped=previous[donor]
        check(name+'_exact_memory_marginal_preserved_at_every_time',
              np.array_equal(previous.sum(axis=0),swapped.sum(axis=0)))
        check(name+'_prediction_uses_only_previous_time',
              np.all(np.arange(nt)<np.arange(1,nt+1)))
        predictions={
            'intact':predictor.probabilities[previous],
            'reset':np.full(target.shape,predictor.marginal),
            'cross_trial_swap':predictor.probabilities[swapped],
            'state_relabel':predictor.probabilities[::-1][1-previous]}
        check(name+'_relabel_predictions_bitwise_identical',
              np.array_equal(predictions['intact'],predictions['state_relabel']))
        check(name+'_frozen_train_state_unchanged',digest(train.states)==predictor.train_digest)
        check(name+'_frozen_predictor_read_only',not predictor.probabilities.flags.writeable)
        losses={k:loss_per_trial(predictions[k],target,protocol['scores']['clipping']) for k in conditions}
        means={k:{metric:float(values.mean()) for metric,values in loss.items()} for k,loss in losses.items()}
        # A cluster contains both reciprocal donor trials and all their times.
        # This avoids pretending donor-coupled trials or transitions are independent.
        boot=np.random.default_rng(source['bootstrap_seed']).integers(
            0,len(pairs),size=(nboot,len(pairs)))
        effects={}
        for condition in conditions[1:]:
            effects[condition]={}
            for metric in ['brier','log']:
                paired_diff=losses[condition][metric]-losses['intact'][metric]
                cluster_diff=paired_diff[pairs].mean(axis=1)
                samples=cluster_diff[boot].mean(axis=1)
                low,high=np.quantile(samples,[.025,.975])
                effects[condition][metric]={
                    'mean_paired_loss_increase':float(paired_diff.mean()),
                    'ci95_low':float(low),'ci95_high':float(high),
                    'bootstrap_standard_error':float(samples.std(ddof=1)),
                    'independent_trial_pair_clusters':len(pairs)}
        check(name+'_relabel_losses_exactly_equal',all(
            effects['state_relabel'][metric]['mean_paired_loss_increase']==0
            and effects['state_relabel'][metric]['ci95_low']==0
            and effects['state_relabel'][metric]['ci95_high']==0 for metric in ['brier','log']))
        if stay==.8:
            interpretation_checks={
                'prespecified_primary_positive_control_passed':all(
                    effects[c]['brier']['ci95_low']>0 for c in ['reset','cross_trial_swap']),
                'secondary_log_loss_corroborates':all(
                    effects[c]['log']['ci95_low']>0 for c in ['reset','cross_trial_swap'])}
        else:
            interpretation_checks={
                'prespecified_negative_control_brier_equivalence_passed':all(
                    effects[c]['brier']['ci95_low']>-.01 and effects[c]['brier']['ci95_high']<.01
                    for c in ['reset','cross_trial_swap']),
                'prespecified_negative_control_log_equivalence_passed':all(
                    effects[c]['log']['ci95_low']>-.02 and effects[c]['log']['ci95_high']<.02
                    for c in ['reset','cross_trial_swap'])}
        for trial in range(ntest):
            row={'source':name,'trial_id':test.ids[trial],'swap_pair':int(pair_ids[trial]),
                 'donor_trial_id':test.ids[donor[trial]]}
            for c in conditions:
                for metric in ['brier','log']:
                    row[c+'_'+metric]=float(losses[c][metric][trial])
            csv_rows.append(row)
        sources.append({
            'name':name,'stay_probability':stay,'seeds':source,
            'train_transition_counts':predictor.counts.tolist(),
            'trained_p_next_one_given_previous':predictor.probabilities.tolist(),
            'trained_marginal_p_one':predictor.marginal,
            'test_empirical_marginal_p_one':float(target.mean()),
            'train_array_sha256':digest(train.states),'test_array_sha256':digest(test.states),
            'donor_index_sha256':digest(donor.astype('<i8')),
            'mean_losses':means,'paired_effects':effects,
            'prespecified_interpretation_checks':interpretation_checks,
            'ideal_population_losses':theoretical_losses(stay)})
    result={
        'status':'Entirely synthetic causal-memory test; not consciousness or physical-field evidence',
        'protocol_id':protocol['protocol_id'],'protocol_sha256':protocol_hash,
        'run_started_utc':started,'run_completed_utc':datetime.now(timezone.utc).isoformat(),
        'environment':{'python':platform.python_version(),'numpy':np.__version__,
                       'rng':'numpy.default_rng PCG64'},
        'sample':protocol['sample'],'uncertainty':protocol['uncertainty'],
        'sources':sources,'checks':checks,
        'limitations':[
            'Source law and mechanism are stipulated by executable synthetic construction',
            'No observations of human or machine phenomenology',
            'No test of scalar-field dynamics, gravity or quantum coupling',
            'Predictor has no actions that affect the source and no goal or reward criterion',
            'Bootstrap is conditional on the fitted predictor and this simulated population',
            'Intervals retain dependence within trajectories and reciprocal donor pairs',
            'Local hash lock is not externally registered preregistration']}
    (HERE/'synthetic_memory_results.json').write_text(json.dumps(result,indent=2)+'\n')
    with (HERE/'held_out_trial_scores.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=csv_rows[0].keys())
        writer.writeheader();writer.writerows(csv_rows)
    make_plot(result)
    print(json.dumps({'protocol_sha256':protocol_hash,'algorithm_checks_passed':len(checks),
        'effects':[{'source':x['name'],'effects':x['paired_effects'],
                    'interpretation_checks':x['prespecified_interpretation_checks']} for x in sources]},indent=2))


def make_plot(result):
    os.environ.setdefault('MPLCONFIGDIR','/tmp/toe_agency_matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    labels=[];data=[]
    for source in result['sources']:
        short='Markov (stay 0.8)' if source['stay_probability']==.8 else 'IID (stay 0.5)'
        for condition in ['reset','cross_trial_swap']:
            labels.append(short+' / '+('reset' if condition=='reset' else 'swap'))
            data.append(source['paired_effects'][condition])
    fig,axes=plt.subplots(1,2,figsize=(10.2,4.3),layout='constrained',sharey=True)
    y=np.arange(len(labels))[::-1]
    for ax,metric,title in zip(axes,['brier','log'],['Brier loss','Log loss (natural units)']):
        values=np.array([r[metric]['mean_paired_loss_increase'] for r in data])
        lo=np.array([r[metric]['ci95_low'] for r in data]);hi=np.array([r[metric]['ci95_high'] for r in data])
        for i in range(len(data)):
            ax.errorbar(values[i],y[i],xerr=[[values[i]-lo[i]],[hi[i]-values[i]]],
                        fmt='o',color='#176181' if i<2 else '#c16735',capsize=4,markersize=6)
        ax.axvline(0,color='.5',lw=.8)
        ax.set_title(title);ax.set_xlabel('Intervention loss minus intact loss')
        ax.set_yticks(y,labels);ax.grid(axis='x',alpha=.2)
    fig.suptitle('Synthetic memory intervention: held-out paired effects\n95% bootstrap intervals preserve complete donor-linked trial pairs',fontsize=11)
    fig.savefig(HERE/'synthetic_memory_interventions.png',dpi=180)
    plt.close(fig)


if __name__=='__main__':
    main()
