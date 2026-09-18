#!/usr/bin/env python3
"""
mqgt_sequestering_loops.py
Record-side verification for parallel 2: radiative sequestering of J = kappa E S^2
(corpus Part 0 open problem 1; Ch.4 / MATH-02 / MATH-03; monograph sec. 5.3-5.4, sec. 7-8).

Contents
  (a) operator parity classification up to dim 4 (supports Lemma 1': all-orders selection rule)
  (b) corpus benchmark recompute: <S^2>, backreaction cap on kappa_E and E_bar
  (c) one-loop delta m_S^2 from the kappa vertex, exact finite B0 part
  (d) spurion-broken induced E|H|^2 portal, exact finite C0 triangle
  (e) E-mass naturalness, CORRECTED 2026-09-18: one-loop kappa bubble (log)
      + one-loop E^2 X^2 portal tadpoles (quadratic); ChatGPT-review erratum
  (f) boundedness: 3-field condition and single-field reduction lambda_S > 2 kappa^2/m_E^2
  (g) vacuum alignment: E-S1 mixing from <S2> = v2, tachyon condition

All standard one-loop scalar EFT; finite parts by Feynman-parameter integrals (mpmath dps=50).
Conventions: L_int = -kappa E S1 S2 - (lam2H/2) S2^2 h^2 - mu12^2 S1 S2 - V(quartics lam/4).
"""
from mpmath import mp, mpf, sqrt, log, pi, quad

mp.dps = 50

def hdr(t):
    print("\n" + "=" * 72 + "\n" + t + "\n" + "=" * 72)

# ---------------------------------------------------------------- benchmarks
rho_loc = mpf('2.3e-6')   # eV^4   (0.3 GeV/cm^3, corpus eq 5.11)
mE  = mpf('1e-4')         # eV     E mass benchmark
mS  = mpf('1e-3')         # eV     hidden scalar benchmark (m_1 = m_2 = m_S)
S2v = rho_loc / mS**2     # <S^2> = rho_loc / m_S^2  (corpus eq 5.11)

# ---------------------------------------------------------------- (a) parity table
hdr("(a) Z2_h parity of operators, dim <= 4   [E,S1 odd ; S2,h even]")
fields = ['E', 'S1', 'S2', 'h']
odd = {'E', 'S1'}
# mass dimensions: scalar=1, so monomials of total degree <= 4 (with coeff dim 4-deg)
rows = []
for nE in range(5):
    for n1 in range(5):
        for n2 in range(5):
            for nh in range(5):
                deg = nE + n1 + n2 + nh
                if deg < 1 or deg > 4:
                    continue
                name = []
                for f, c in (('E', nE), ('S1', n1), ('S2', n2), ('h', nh)):
                    if c == 1: name.append(f)
                    elif c > 1: name.append(f + '^' + str(c))
                par = (-1) ** (nE + n1)
                rows.append((deg, '*'.join(name), par))
allowed = [r for r in rows if r[2] == +1]
forbidden = [r for r in rows if r[2] == -1]
print(f"  monomials dim<=4: {len(rows)}  allowed(even): {len(allowed)}  forbidden(odd): {len(forbidden)}")
print("  key allowed  : E*S1*S2 (source), S2^2*h^2, S1^2*h^2, E^2*h^2, mass/quartic terms")
print("  key forbidden: E*h^2 (direct portal), E*S2^2, S1*S2 (spurion slot), E*S1^2, tadpole E")
check = all((r[0] != 3 or r[1] != 'E*h^2') for r in allowed)
print("  E|H|^2 in allowed set:", not check, " -> tree+loop selection rule consistent:", check)

# ---------------------------------------------------------------- (b) source cap
hdr("(b) source displacement and backreaction cap (corpus eqs 5.10-5.13 recomputed)")
Ebar_cap = sqrt(2 * rho_loc) / mE                 # 1/2 m_E^2 E_bar^2 = rho_loc
kappa_cap = sqrt(2 * rho_loc) * mE / S2v          # saturation of the cap
print(f"  <S^2>              = {mp.nstr(S2v, 8)} eV^2")
print(f"  E_bar cap          = {mp.nstr(Ebar_cap, 8)} eV      (corpus quote: ~2 eV, conservative)")
print(f"  kappa_E cap        = {mp.nstr(kappa_cap, 8)} eV    (corpus quote: ~1e-6 eV, conservative)")
kappa = kappa_cap   # adopt saturation as conservative benchmark

# ---------------------------------------------------------------- (c) delta m_S^2
hdr("(c) one-loop delta m_S2^2 = kappa^2/(16 pi^2) [ln(Lam^2/mu^2) + B0_fin]")
def B0_fin(p2, ma2, mb2, mu2):
    f = lambda x: log((x * ma2 + (1 - x) * mb2 - x * (1 - x) * p2) / mu2)
    return -quad(f, [0, 1])
mu = mS
for Lam in (mpf('1'), mpf('1e3')):
    b0f = B0_fin(mS**2, mE**2, mS**2, mu**2)
    dm = kappa**2 / (16 * pi**2) * (log(Lam**2 / mu**2) + b0f)
    print(f"  Lam={mp.nstr(Lam,3)} eV: B0_fin={mp.nstr(b0f,8)}  dm_S^2={mp.nstr(dm,6)} eV^2"
          f"   dm_S^2/m_S^2={mp.nstr(dm/mS**2,4)}")

# ---------------------------------------------------------------- (d) induced E|H|^2
hdr("(d) spurion mu12^2 S1S2 -> induced E|H|^2 coefficient (one-loop triangle, exact C0)")
def C0_zero(ma2, mb2, mc2):
    inner = lambda x: quad(lambda y: 1 / (x * ma2 + y * mb2 + (1 - x - y) * mc2), [0, 1 - x])
    return -quad(inner, [0, 1])          # dimension eV^-2, negative-definite integrand
c0 = C0_zero(mS**2, mS**2, mS**2)        # propagators (S1,S2,S2), all external p=0
print(f"  C0(0; mS^2,mS^2,mS^2) = {mp.nstr(c0, 8)} eV^-2   (exact value -1/(2 mS^2) = {mp.nstr(-1/(2*mS**2),8)})")
mu12 = mS**2                              # maximal soft spurion benchmark
lam2H = mpf('1')                          # report per unit portal coupling
dgH = kappa * lam2H * mu12 / (16 * pi**2) * (-c0)   # sign convention of L_int; magnitude quoted
print(f"  delta g_H = kappa lam2H mu12^2 |C0| /(16 pi^2)")
print(f"            = {mp.nstr(dgH, 6)} eV   per lam2H=1, mu12^2=mS^2 (maximal spurion)")
print(f"  scaling: delta g_H ~ {mp.nstr(kappa/(16*pi**2)*(-c0)*mpf('1'),4)} eV^-1 x lam2H x mu12^2[eV^2]")

# ---------------------------------------------------------------- (e) delta m_E^2
hdr("(e) E mass naturalness — CORRECTED 2026-09-18 (ChatGPT review verified)")
print("  ERRATUM (previous version said): 'kappa vertex reaches the E propagator")
print("  only at two loops, dm_E^2 ~ kappa^2 Lam^2/(16 pi^2)^2' -- wrong twice:")
print("  (i) two kappa vertices make a ONE-loop bubble (S1,S2 internal lines);")
print("  (ii) kappa^2 Lam^2 has mass dimension 4, not the dim-2 of a mass")
print("       correction. Both points due to ChatGPT's review (relayed by")
print("       Christopher; initially mis-credited to Grok). Verified here.")
print("  Correct content: (e1) one-loop kappa bubble (log-divergent, dim 2);")
print("  (e2) one-loop tadpoles from the Z2-allowed E^2 X^2 portal quartics")
print("       (quadratic divergence; THE actual E-mass naturalness constraint).")
print()
print("(e1) one-loop kappa bubble: dm_E^2 = kappa^2/(16 pi^2) [ln(Lam^2/mu^2) + B0_fin]")
mu = mS
b0fE = B0_fin(mE**2, mS**2, mS**2, mu**2)
print(f"  B0_fin(m_E^2; m_S^2, m_S^2; mu^2) = {mp.nstr(b0fE, 8)}")
for Lam in (mpf('1'), mpf('1e3'), mpf('1e6')):
    dm = kappa**2 / (16 * pi**2) * (log(Lam**2 / mu**2) + b0fE)
    print(f"  Lam={mp.nstr(Lam,3)} eV: dm_E^2={mp.nstr(dm,4)} eV^2"
          f"   dm_E^2/m_E^2={mp.nstr(dm/mE**2,4)}")
print("  -> kappa channel alone is natural to cutoffs far above 1 MeV (log only).")
print()
print("(e2) portal tadpoles: dm_E^2 = (lam_E1+lam_E2+lam_EH) Lam^2/(16 pi^2)")
print("  [coefficient corrected 32->16 pi^2: ChatGPT round 2, verified via")
print("   background-field V1: d^2V1/dE^2 = lam_EX Lam^2/(16 pi^2)]")
print("  Z2-even, so NOT sequestered (and do not regenerate E|H|^2 either).")
print("  Naturalness bounds |dm_E^2|, so the condition is on the ABSOLUTE")
print("  VALUE of the net sum (ChatGPT round-4 refinement): a one-sided")
print("  < would admit arbitrarily large NEGATIVE corrections (e3a induces")
print("  negative quartics). |net sum| allows cancellation; the stricter")
print("  no-cancellation criterion bounds each magnitude separately.")
for Lam in (mpf('1'), mpf('1e3'), mpf('1e6')):
    lamcrit = 16 * pi**2 * mE**2 / Lam**2
    print(f"  Lam={mp.nstr(Lam,3)} eV: naturalness needs"
          f"  |lam_E1+lam_E2+lam_EH| <~ {mp.nstr(lamcrit,4)}"
          f"  (or each |lam_EX| separately)")
print()
print("(e3) radiative stability of zero portals (ChatGPT rounds 2-3):")
print("  NOT stable; portals INDUCED at calculable values.")
print()
print("  (e3a) tree-level exchange -- EFT MATCHING, not full-theory quartics")
print("   (ChatGPT round 3): integrate out S2 -> lam_E1 = -kappa^2/m_2^2;")
print("   integrate out S1 -> lam_E2 = -kappa^2/m_1^2. Two ALTERNATIVE")
print("   low-energy descriptions, NOT additive quartics in the full theory")
print("   (both scalars propagate there; the full kappa-only answer is e1).")
print(f"   magnitude {mp.nstr(kappa**2/mS**2,4)}; no quadratic EFT estimate is")
print("   extrapolated above the integrated-out mass.")
print()
print("  (e3b) one-loop TRIANGLE for lam_EH (ChatGPT round 3, verified):")
print("   lam_EH^ind = kappa^2 ∫ d^4k/(2pi)^4 [lam_1H/((k^2+m1^2)^2(k^2+m2^2))")
print("                                     + lam_2H/((k^2+m1^2)(k^2+m2^2)^2)]")
def tri_int(a, b):
    # ∫ d^4k/(2π)^4 1/((k²+a)²(k²+b)) = (1/16π²) ∫₀¹ x dx/(xa+(1-x)b)
    return quad(lambda x: x / (x * a + (1 - x) * b), [0, 1]) / (16 * pi**2)
ti_eq = tri_int(mS**2, mS**2)
print(f"   numeric equal-mass integral = {mp.nstr(ti_eq,8)} eV^-2"
      f"  (analytic 1/(32 pi^2 m_S^2) = {mp.nstr(1/(32*pi**2*mS**2),8)})")
tri = kappa**2 / (32 * pi**2 * mS**2)
print(f"   equal masses: lam_EH^ind = kappa^2 (lam_1H+lam_2H)/(32 pi^2 m_S^2)")
print(f"                 = {mp.nstr(tri,4)} x (lam_1H+lam_2H)")
print(f"   decisive control lam_1H=0, lam_2H=1: nonzero {mp.nstr(tri,4)}")
print("   (round-2 box formula wrongly gave 0 there; benchmark coincidence")
print("    2.76e-11 x 2 = 5.5e-11 at lam=1,1 masked the wrong dependence)")
print("   vs cap 1.58e-6 (eV/Lam)^2: induced floor sits orders below; cap")
print("   applies to (bare + induced) total; N_X species divide it.")

# ---------------------------------------------------------------- (f) boundedness
hdr("(f) potential boundedness (MATH-03 generalization)")
# single-field reduction: s1=s2=S, E minimized: E* = kappa S^2/m_E^2
print("  single-field reduction: V_eff quartic = [lam_S/4 - kappa^2/(2 m_E^2)] S^4")
print("  -> stability lambda_S > 2 kappa^2/m_E^2  (corpus MATH-03 formula recovered exactly)")
print(f"     with lam_S = lam_1 + lam_2 + 2 lam_12 ; 2 kappa^2/m_E^2 = {mp.nstr(2*kappa**2/mE**2,4)}")
# 3-field condition: min over x=s1/s2 of  V/t^4 = lam1 x^4/4 + lam2/4 + lam12 x^2/2 - kappa^2 x^2/(2 mE^2)
lam1, lam2, lam12 = mpf('0.1'), mpf('0.1'), mpf('0.1')
cond_rhs = lam12 + sqrt(lam1 * lam2)
print(f"  3-field boundedness: kappa^2/m_E^2 < lam_12 + sqrt(lam_1 lam_2) = {mp.nstr(cond_rhs,6)}")
print(f"     kappa^2/m_E^2 = {mp.nstr(kappa**2/mE**2,4)}  -> margin factor {mp.nstr(cond_rhs/(kappa**2/mE**2),4)}")
# numeric grid check
xs = [mpf(10) ** (mpf(i) / 20 - 2) for i in range(81)]
vmin = min(lam1 * x**4 / 4 + lam2 / 4 + lam12 * x**2 / 2 - kappa**2 * x**2 / (2 * mE**2) for x in xs)
print(f"     grid min of V/t^4 over x in [1e-2,1e2]: {mp.nstr(vmin,6)}  (positive => bounded)")

# ---------------------------------------------------------------- (g) vacuum alignment
hdr("(g) vacuum alignment: <S2> = v2 induces E-S1 mixing")
print("  mass matrix [[m_E^2, kappa v2],[kappa v2, m_1^2]]; tachyon iff kappa^2 v2^2 > m_E^2 m_1^2")
v2crit = mE * mS / kappa
print(f"  v2 crit = m_E m_1/kappa = {mp.nstr(v2crit,6)} eV")
for v2 in (mpf('0.01'), mpf('0.1'), mpf('1.0')):
    a, b, c = mE**2, kappa * v2, mS**2
    tr, det = a + c, a * c - b**2
    lo = (tr - sqrt(tr**2 - 4 * det)) / 2
    theta = mpf('0.5') * __import__('mpmath').atan(2 * b / (c - a))
    print(f"  v2={mp.nstr(v2,3)} eV: lightest eigenvalue={mp.nstr(lo,6)} eV^2"
          f"  mixing theta={mp.nstr(theta,4)}  tachyon: {det < 0}")

print("\nALL SECTIONS COMPUTED.")
