# A reproducible operational memory bridge

**Executed 21 October 2026. All data are synthetic.** This experiment tests whether a specified internal memory causally supports prediction of a specified source. It contains no human data, no observations of experience, and no measurement of a new physical field.

## Result

The implemented predictor benefits from access to the previous state of a temporally dependent binary source. On held-out trials, resetting its memory or swapping it with another independent trial worsens both proper prediction scores. The same interventions have negligible effects for an IID source. Relabeling the internal memory states while conjugating the decoder leaves every prediction exactly unchanged.

This completes an operational causal-memory test with an executable mechanism, interventions, controls, held-out evaluation and uncertainty estimates. It does not establish phenomenal consciousness, autonomous agency, or a physical consciousness field. The predictor has no actions that affect its source, no goal-selection mechanism and no reward-driven policy.

## 1. Protocol fixed before generation

`protocol.json` was written and SHA-256 locked before the first simulation. Its hash is

`77061f72bdc30a11f29123166ded858336c358e84f8ac19b096afac17e897155`.

The local lock record is dated 21:49:45 UTC, and the first run began at 21:50:52 UTC. The lock record's `experiment_has_run: false` describes the moment of locking. It is a local prespecification record, not an externally timestamped or registered study. The script refuses to run if the protocol bytes no longer match the locked hash. Seeds, sample sizes, interventions, scores, bootstrap procedure and interpretation criteria were specified before any results were generated [1–3].

For each of two source conditions, 400 independent training trials and 400 independent held-out trials were generated, with 64 transitions per trial. Every trial begins with an independent Bernoulli(0.5) bit. At each step the bit stays unchanged with probability 0.8 in the positive control and 0.5 in the IID negative control. The population marginal is balanced; exact empirical balance is not forced. Train, test, pairing and bootstrap seeds are distinct and recorded in the protocol. No seed search, optional stopping or parameter selection after results was performed.

## 2. Mechanism, scores and interventions

The synthetic graph has a temporally persistent source, an explicitly stored previous bit, a fixed decoder, and a prediction of the next bit. Only the predictor's access to previous-state information is manipulated. The source-generating rule and held-out outcomes are the same across all paired comparisons.

From training transitions alone, the predictor estimates

\[
\widehat P(X_t=1\mid X_{t-1}=s)=\frac{N_{s1}+1}{N_{s0}+N_{s1}+2}.
\]

The two added counts are Laplace smoothing. Reset predictions use the similarly smoothed training marginal. The fitted probabilities are frozen and read-only throughout evaluation. A fitting function rejects a held-out partition before inspecting its labels. Trial IDs and RNG seeds are disjoint between train and test.

| Condition | Memory supplied to the frozen decoder | Controlled feature |
|---|---|---|
| Intact | The trial's own previous bit | Full specified predictive memory |
| Reset | Null state returning the training marginal | Removes access to previous-state information |
| Cross-trial swap | A paired independent trial's previous bit at the same step | Preserves the complete empirical memory marginal at every time while breaking its relation to the recipient's source history |
| State relabel | Complemented memory bit with the decoder table reversed | Changes internal labels without changing the represented information or predictions |

The swap permutation has no fixed points and is composed of reciprocal pairs. Thus each trial supplies memory to its partner and receives memory from that partner. The same permutation is used across all time steps. No contemporaneous target or future state is supplied to a prediction.

The primary score is Brier loss, \((p-y)^2\). The secondary score is natural-log loss, \(-y\log p-(1-y)\log(1-p)\). Lower is better. These reward calibrated probability predictions rather than merely thresholded correct answers. For a true Bernoulli probability q, expected Brier loss is \((p-q)^2+q(1-q)\), minimized at p = q. The log loss is also minimized at the true probability. Effects are paired intervention loss minus intact loss, so positive values mean that the intervention worsened prediction.

## 3. Held-out results

For the persistent source, the fitted probabilities were 0.203799 for a preceding zero and 0.801812 for a preceding one. The reset prediction was 0.507968. For the IID source, the two fitted probabilities were 0.498442 and 0.499060, with reset prediction 0.498750 [3].

### Absolute mean losses

| Source | Condition | Brier loss | Log loss |
|---|---|---:|---:|
| Markov, stay = 0.8 | Intact | 0.1582798 | 0.4964579 |
| Markov, stay = 0.8 | Reset | 0.2502247 | 0.6935967 |
| Markov, stay = 0.8 | Swap | 0.3397861 | 0.9153662 |
| IID, stay = 0.5 | Intact | 0.2499927 | 0.6931326 |
| IID, stay = 0.5 | Reset | 0.2499928 | 0.6931327 |
| IID, stay = 0.5 | Swap | 0.2499923 | 0.6931318 |

The relabel condition is exactly equal to intact in both rows of source conditions, down to bitwise equality of the probability arrays.

### Paired loss increases and 95% bootstrap intervals

| Source and intervention | Brier increase [95% interval] | Log-loss increase [95% interval] |
|---|---:|---:|
| Markov reset | 0.0919449 [0.0887336, 0.0951169] | 0.1971388 [0.1897429, 0.2044036] |
| Markov swap | 0.1815062 [0.1734237, 0.1897301] | 0.4189084 [0.4002543, 0.4378886] |
| IID reset | 6.35×10⁻⁸ [−3.84×10⁻⁶, 3.95×10⁻⁶] | 1.27×10⁻⁷ [−7.68×10⁻⁶, 7.91×10⁻⁶] |
| IID swap | −3.86×10⁻⁷ [−5.94×10⁻⁶, 5.45×10⁻⁶] | −7.72×10⁻⁷ [−1.19×10⁻⁵, 1.09×10⁻⁵] |
| Relabel, either source | Exactly 0 [0, 0] | Exactly 0 [0, 0] |

Both positive-control Brier intervals are strictly above zero, as prespecified. The log scores corroborate that result. Both IID Brier intervals lie within the prespecified equivalence band [−0.01, 0.01], and the IID log-loss intervals lie within [−0.02, 0.02]. These are results of the stipulated synthetic mechanism and fixed protocol; they are not evidence about a biological population or an unobserved consciousness variable.

![Held-out synthetic intervention effects](synthetic_memory_interventions.png)

## 4. Why the outcome is expected under this mechanism

For an ideal predictor trained on infinite data from the stay = 0.8 source, intact, reset and swap have expected Brier losses 0.16, 0.25 and 0.34. Their expected log losses are 0.5004024, 0.6931472 and 0.9162907. These values follow directly from the defined binary transition law [2–3].

Reset loses temporal information while retaining a reasonable constant forecast. Swap supplies another trial's irrelevant state and therefore produces unjustified confidence in a forecast that is unrelated to the recipient's next bit. Its expected loss is accordingly larger than reset. This comparison does not make an ordinary correlation into a novel physical effect: the causal mechanism is explicitly built into the simulation and the interventions expose that mechanism.

For the IID source, the previous bit has no predictive value. The ideal prediction is 0.5 for either memory state, giving expected Brier loss 0.25 and log loss log 2 under all three conditions. The very small fitted-probability differences and finite held-out fluctuations account for the near-zero observed effects.

## 5. Dependence-aware uncertainty and checks

The analysis uses 4,000 percentile bootstrap replicates. It first computes paired losses within each held-out trial, then resamples **200 independent blocks of two complete reciprocal donor trials**. Every 64-transition trajectory and both sides of each memory swap remain together. Resampling individual time steps would discard serial dependence. Resampling a receiver separately from its donor would discard dependence introduced by the swap. The chosen block keeps both dependencies represented.

The intervals describe held-out sampling variation conditional on the fitted predictor and specified synthetic source. They do not include training-estimation uncertainty, changes of source law, sensor error or real-world model discrepancy. Reported intervals are individual comparison intervals, not a simultaneous familywise confidence region.

Twenty-one implementation checks pass, including the protocol-related seed constraints, disjoint training/test IDs, rejection of held-out fitting, immutable predictor probabilities, derangement and reciprocity, exact preservation of memory counts at every prediction time, and exact relabel equivalence. Generated arrays and donor indices have recorded SHA-256 digests. The supplied CSV records every held-out trial's scores, source, donor and cluster assignment. No human observations were generated or inferred.

## 6. What the operational bridge does and does not support

The supported statement is precise: **in this specified computational mechanism, intervening on access to temporally informative memory changes held-out predictive performance.** The IID control shows that the effect depends on predictive temporal structure. The swap control distinguishes useful linkage to the recipient's history from the mere distribution of memory values. The relabel control demonstrates that an internal symbol name has no identifiable causal significance when encoding and decoding are transformed together.

This predictor is not an autonomous agent in the experiment: it does not choose an action that changes the source, pursue a goal or adapt a policy to reward. Predictive memory can be a component of such a system, but these outputs do not establish those additional properties. They also provide no phenomenal report, experience measure or bridge law between information processing and experience.

If two proposed descriptions predict the same distribution of all available observations under every performed intervention, these data cannot distinguish them. The exact state-relabel equivalence supplies a transparent example. Adding the word “consciousness” or naming a latent scalar does not itself change the likelihood of the observed outcomes.

## 7. Concrete requirements for a further bridge

The following are requirements for a subsequent experiment or physical theory, not claims established by this run.

| Proposed extension | Concrete additional specification | Distinguishing prediction required |
|---|---|---|
| Operational agency | Actions, an environment transition law, an explicit objective or reward, policy state, and randomized interventions on action selection or memory | Out-of-sample action/outcome or policy-adaptation differences predicted in advance beyond a passive predictor with the same inputs |
| Relation to reported experience | Define the observable report or independently operationalized outcome, how it is measured, and how memory, attention, arousal, task demand and report ability enter competing models | Prespecified quantitative predictions that differ between the proposed experience model and a functional memory/report model under matched interventions; a memory-performance effect alone does not distinguish them |
| A proposed physical field | Field variable and units, action or evolution equation, couplings to measured apparatus variables, relevant boundary conditions, and an identifiable nonzero parameter range | A quantitative observable shift, scaling or correlation that differs from the ordinary physical model for the same apparatus and remains after measured conventional influences are modeled |
| Unification with the broader physical theory | A common set of parameters, compatible dynamics and a map from theoretical variables to measured observables | Joint predictions across independent experiments using parameters fixed in advance, with stated rejection thresholds and no adjustment of an unconstrained bridge function to each result |

For an actual consciousness claim, operational outcomes would need to be chosen and justified independently of this toy success. Even a reliable relation to reports would require interpretation; the present experiment supplies no rule that makes a report or a score identical to experience. For a physical-field claim, a model with no observable coupling or one that is exactly observationally equivalent to the ordinary model cannot be identified by these data. A nonzero coupling must produce a stated, measurable difference before an empirical test can decide between them.

The next concrete computational extension, if agency rather than memory is the target, is to add a specified action and reward interface and test whether interventions alter policy-dependent outcomes while retaining the passive predictor as a baseline. That is a different experiment. This deliverable completes only the prespecified causal-memory stage.

## Sources and reproducibility

[1] `protocol.json`, `protocol.sha256`, and `protocol_lock.json`: prospective local design, fixed seeds, interpretation criteria and hash record.

[2] `synthetic_causal_memory.py`: source law, train-only estimator, frozen interventions, theoretical losses, dependence-aware bootstrap and executable checks.

[3] `synthetic_memory_results.json` and `held_out_trial_scores.csv`: complete observed synthetic outputs, fitted probabilities, score differences, intervals, data hashes and environmental versions.

All source statements in this note concern the declared construction and its executed outputs. No external empirical study or uploaded passage is being represented as evidence of consciousness.
