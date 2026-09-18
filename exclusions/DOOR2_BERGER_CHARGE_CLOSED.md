# EXCLUSION — Door 2: Berger charge susceptibility — CLOSED

**Date:** 2026-09-18 · **Label:** CLOSED (exclusion, not a positive formula)
**Reproduce:** `python3 ../play_notes/play_berger_charge_lab.py`
(output: `../play_notes/play_berger_charge_lab_out.txt`)

## Declared principle (pre-computation)

The dial-free geometric source of charge-to-eigenvalue coupling is the
canonical variation (Berger squash) of the Hopf fibration — the unique
metric deformation holding the CP^m base fixed and scaling the S¹ fiber.
On scalars it provably shifts λ → λ + κq², κ = t⁻² − 1 from the round
point (κ = 0 is the record, already excluded). Applied as the Landau-form
ansatz to both coexact α towers.

## Why truncation-free

Door 1's failure mode is structurally absent: the total charge moment
Q2(k) = Σ_q d_q(k)q² is an exact EVEN polynomial in x (Dynkin-index
polynomiality; holdout-certified to 1.5e-134; evenness keeps the Hurwitz
pole out of the λ² sums). The round-point linear responses
dL/dκ = +Σ_x Q2/λ and dD1/dκ = −Σ_x Q2/λ² are exact full-tower zeta
values — no sectors, no cutoff.

## Results

| tower | dL/dκ | dD1/dκ | σ_κ | distance to σ_need = −6.21 |
|---|---|---|---|---|
| S⁷ ce3 | +1/7 (exact) | +0.664425606401 | +4.650979245 | 10.86 |
| S⁹ ce2 | −1/9 (exact) | +19/720 (exact) | −0.2375 | 5.97 |
| combined | | | +21.7606566 | 27.97 |

**Verdict: CLOSED, excluded.**

## Structural finding — the D1 lock (control C4)

**σ_κ = ±D1(tower) exactly** in both towers (deviations 1.5e-128 and
1.1e-60): each tower's charge susceptibility is locked to its own
self-response. The canonical-variation route cannot generate an
independent slope in the (L, D1) plane — and σ_need = −6.21 requires
exactly such independence. Exact rational pattern: dL/dκ = ±1/n
(+1/7, −1/9), i.e. (−1)^{(n+1)/2}/n — noted, not proved.

Sign honesty: per-mode responses are sign-definite; zeta-regularized
tower totals are not. Reported signs are the exact regularized values,
same convention as the record scorecards.
