# PATCH E1 — UV-completion wording (`uv_completion.tex`)

**Erratum:** E1 (wording only; physics conclusion unchanged)
**Frozen record:** `mqgt-scf-independent-verification`, `MQGT_SCF_ERRATA_2026-09-17.md` §E1
**Target:** canonical corpus, `uv_completion.tex` (and the same sentence in `bridge_d_uv.py` output text)

## Why

The beta system (Machacek–Vaughn one-loop matter + gravitational screening at
fixed g_N* = 1.7621271) possesses exact non-Gaussian fixed points at
λ₁ = λ₂ = 0.9c, g = 0.3c and λ₁ = λ₂ = g = c/2, with c = 16πg_N/3 ≈ 29.5
(i.e. λ ≈ 26.6, g ≈ 8.9). These lie far outside the one-loop validity domain
and outside the searched positivity cone, so the physical conclusion is
unchanged — but the unqualified sentence "No non-Gaussian fixed point found"
is false as stated.

## Abstract (line 28)

OLD:
```
\textbf{Result: No non-Gaussian fixed point found.} All 91 trajectories from the positivity cone flow to the Gaussian fixed point ($\lambda=g=0$) in the UV.
```

NEW:
```
\textbf{Result: No non-Gaussian fixed point exists \emph{in the perturbative domain} (positivity cone, couplings $\lesssim 1$); all UV trajectories from that domain flow to the Gaussian fixed point ($\lambda=g=0$).} (Exact non-Gaussian fixed points of the truncated system exist at $\lambda\approx 26.6$, $g\approx 8.9$, far outside the one-loop validity domain.)
```

## Conclusion (line 88)

OLD:
```
The scalar sector of MQGT-SCF is asymptotically free in the UV. ... This confirms the corpus statement that the ``matter sector is Gaussian at joint FP'' and removes the scalar sector as a UV completion barrier.
```

NEW: prepend the qualifier
```
The scalar sector of MQGT-SCF is asymptotically free in the UV throughout the perturbative domain (positivity cone, couplings $\lesssim 1$). ...
```

## Companion recommendation (from E1)

Always print the dynamical one-coupling closure with its truncation label:
g_N* = 4.4352 (2-scalar) / 5.0265 (4-scalar) / −7.94 (full-SM); the
two-coupling Einstein–Hilbert truncation gives g* = 0.707321 (scheme
dependence).

**Independent confirmation behind this patch:** 125/125 cone trajectories →
Gaussian; 5000-seed Newton survey finds only the Gaussian FP in the
perturbative region (`mqgt_c6_independent_uv.py`, verification repo).
