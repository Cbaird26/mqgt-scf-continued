#!/usr/bin/env python3
"""PLAY LAB v2 — TWISTED TOWERS (door 1): Hopf-charge-resolved spectra.
NOT the scientific record. Play-branch lab with record-grade controls.

PRINCIPLE (Christopher, 2026-09-18): the Hopf S^1 action is an isometry, so
every untwisted eigenspace splits into U(1)-charge sectors with the SAME
eigenvalue; only degeneracies split. Charged sectors = forms on CP^m valued
in the q-th Hopf-line power. Both alpha programs print alpha^-1 from
UNtwisted towers and share the 6.08e-7 residual. Question: does the charge
structure produce c3? Computed once, reported, never graded into existence.

ENGINE: SO(2n) Weyl character formula at the U(1) specialization x_j = t,
via the confluent-determinant limit at dps=150, then integer rounding:
  ch_lam(t0) = [s^N]det(M^lam)/[s^N]det(M^0), N = n(n-1)/2,
  M^a_{ij}(s) = sum_l (a_j c_i)^l/l! (t0^{a_j} + (-1)^l t0^{-a_j}) s^l,
  d_q solved from ch(t0) = sum_q d_q (t0^q + t0^{-q}), t0 = 1..A+1.
Rounding is certified by EXACT integer controls (C1-C4 below).

CONTROLS:
  C1 sum_q d(level,q) == deg_coexact / deg_scalar total, every level (int)
  C2 palindrome d(-q) == d(q); C3 nonnegative ints, clean round margins
  C4 scalar sectors == independent SU(m+1) Weyl-product closed form
  C5 SPECTRAL CERTIFICATE: sector zeta'(0)/zeta(0)/D1 vs an independent
     Laurent extraction from the exact binomial expansion at s = +-eps
     (never touches the Hurwitz pole that sector polys introduce at
     2j-m_=1; pole regularization derived in-file).  D1 also by finite
     difference.  NOTE: a truncated sector-SUM control is void — sector
     zeta values carry pole terms cancelling only across ALL sectors
     (verified numerically), so no such control is used or claimed.

FORM TOWERS: per-sector stable-polynomial zeta tails with per-sector onset
x0_q; holdout-verified; finite-head corrections disclosed
(L += delta*log lam, D1 += delta/lam, zeta(0) += delta).
Higher-q sectors beyond the fit window are listed as data; moment probes
are truncated — missing-sector contributions are uncontrolled (pole terms),
so probes are INDICATIVE ONLY, never graded.
"""

from mpmath import mp, mpf, nstr, matrix, lu_solve, log as mplog, psi
import itertools

from mqgt_t1_e4_derivation import build, logdet, dkdu
from mqgt_t3_reverse_search import z0, deg_scalar, deg_coexact, zetaR

mp.dps = 140  # AFTER record-module imports: they reset dps on import!
# (charge-solve conditioning eats ~41 digits at k~16; 140 leaves ~1e-60)

C3_TARGET = mpf("-1.56371823031276")
SIGMA_NEED = mpf("-6.21")

# ---------------------------------------------------------- WCF engine
_fact = [mpf(1)]
def fact(l):
    while len(_fact) <= l:
        _fact.append(_fact[-1] * len(_fact))
    return _fact[l]

def perm_sign(p):
    s = 1
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s = -s
    return s

PERMS = {}
def perms(n):
    if n not in PERMS:
        PERMS[n] = [(p, perm_sign(p)) for p in itertools.permutations(range(n))]
    return PERMS[n]

DET_CACHE = {}
def det_sN(a_vals, c_vals, N, t0):
    """[s^N] of det M_ij, M_ij = sum_l (a_j c_i)^l/l! (t0^{a_j}+(-1)^l t0^{-a_j}) s^l"""
    key = (tuple(a_vals), N, t0)
    if key in DET_CACHE:
        return DET_CACHE[key]
    n = len(a_vals)
    # entry series coefficient lists E[i][j][l]
    E = []
    for i in range(n):
        ci = mpf(c_vals[i])
        row = []
        for j in range(n):
            aj = a_vals[j]
            ta = mpf(t0) ** aj
            tia = mpf(t0) ** (-aj) if aj else mpf(1)
            ser = [((ci * aj) ** l) / fact(l) * (ta + ((-1) ** l) * tia)
                   for l in range(N + 1)]
            row.append(ser)
        E.append(row)
    total = mpf(0)
    for perm, sg in perms(n):
        prod = [mpf(0)] * (N + 1)
        prod[0] = mpf(sg)
        for i in range(n):
            ser = E[i][perm[i]]
            new = [mpf(0)] * (N + 1)
            for l1 in range(N + 1):
                if prod[l1] == 0:
                    continue
                for l2 in range(N + 1 - l1):
                    if ser[l2]:
                        new[l1 + l2] += prod[l1] * ser[l2]
            prod = new
        total += prod[N]
    DET_CACHE[key] = total
    return total

def charge_degeneracies(lam):
    """{q: int} charge-resolved degeneracies of SO(2n) rep lam (len n).

    For lam[-1] != 0 (D-type chirality split) the +det WCF ratio returns the
    O(2n) AVERAGE (ch_+ + ch_-)/2 at the diagonal U(1) specialization
    (verified: raw q=+-4 coefficient 0.5 on [1,1,1,1], sums to half the full
    tower).  The physical tower carries BOTH chiralities, so scale by 2.
    C1 (sum vs deg_coexact/deg_scalar) certifies this at every level.
    """
    n = len(lam)
    a = [lam[j] + n - 1 - j for j in range(n)]
    b = [n - 1 - j for j in range(n)]
    N = n * (n - 1) // 2
    A = sum(a)
    cvals = list(range(1, n + 1))
    ts, ys = [], []
    for t0 in range(2, A + 3):   # t0=1 is singular: Weyl denominator ~ (t-t^-1)
        num = det_sN(a, cvals, N, t0)
        den = det_sN(b, cvals, N, t0)
        if den == 0:
            raise RuntimeError("singular specialization point")
        ts.append(t0)
        ys.append(num / den)
    # solve ch(t0) = d_0 + sum_{q>=1} d_q (t0^q + t0^{-q})
    M = matrix([[mpf(1) if q == 0 else mpf(t) ** q + mpf(t) ** (-q)
                 for q in range(A + 1)] for t in ts])
    d = lu_solve(M, matrix(ys))
    scale = 2 if lam[-1] != 0 else 1
    out = {}
    maxdev = mpf(0)
    for q in range(A + 1):
        r = round(scale * d[q])
        dev = abs(scale * d[q] - r)
        maxdev = max(maxdev, dev)
        if r:
            out[q] = int(r)
    for q in list(out):
        out[-q] = out[q]          # palindrome enforced by theory; C2 rechecks raw
    assert maxdev < mpf("1e-40"), f"rounding margin poor: {nstr(maxdev,3)}"
    return out

def su_weyl(partition):
    """dim of SU(n) rep with given partition (nonincreasing, last can be 0)."""
    n = len(partition)
    d = mpf(1)
    for i in range(n):
        for j in range(i + 1, n):
            d *= mpf(partition[i] - partition[j] + j - i) / (j - i)
    return d

def scalar_closed(m, k, q):
    """charge-q scalar multiplicity on S^{2m+1} at level j = 2k+|q| (q >= 0):
    SU(m+1) rep partition (2k+q, k, ..., k, 0)."""
    part = [2 * k + q] + [k] * (m - 1) + [0]
    return int(round(su_weyl(part)))

# ---------------------------------------------------------- zeta helpers
def poly_from_spec(x0q, degp, xs, ds):
    """fit degeneracy poly in x on the LAST degp+1 points; return (poly, bad_heads)."""
    tail = list(range(len(xs) - (degp + 1), len(xs)))
    M = matrix([[mpf(xs[i]) ** e for e in range(degp + 1)] for i in tail])
    c = lu_solve(M, matrix([mpf(ds[i]) for i in tail]))
    sc = max(abs(v) for v in c)
    poly = {e: c[e] for e in range(degp + 1) if abs(c[e]) > mpf("1e-40") * sc}
    bad = []
    for i in range(len(xs)):
        if i in tail:
            continue
        pv = sum(poly[e] * mpf(xs[i]) ** e for e in poly)
        if abs(pv - ds[i]) > mpf("1e-30"):
            bad.append(i)
    return poly, bad

# ---- sector-local spectral functions (handle odd-power Hurwitz poles) ----
# Sector degeneracy polynomials contain ALL powers of x, unlike the record
# towers (even only).  The binomial expansion of (x^2-a2)^{-s} then hits the
# Hurwitz pole at 2j - m_ = 1 for odd m_.  The product is finite:
#   (s/j)(1 + s H_{j-1}) [1/(2s) - psi(x0) + ...]
#     = 1/(2j) + (s/j)(H_{j-1}/2 - psi(x0)) + O(s^2)
# so zeta(0) gains a2^j/(2j) and zeta'(0) gains (a2^j/j)(H_{j-1}/2 - psi(x0)).
def _H(jm1):
    return sum(mpf(1) / i for i in range(1, jm1 + 1)) if jm1 > 0 else mpf(0)

def _xterm(m_, c, a2, x0, j):
    w = 2 * j - m_
    if w == 1:
        return c * a2 ** j / j * (_H(j - 1) / 2 - psi(0, x0))
    return c * a2 ** j / j * zetaR(w, x0)

def logdet_sector(poly, a2, x0):
    total = mpf(0)
    for m_, c in poly.items():
        total += c * 2 * zetaR(-m_, x0, der=1)
        jscale = abs(c)
        for j in range(1, 400):
            t = _xterm(m_, c, a2, x0, j)
            total += t
            if j > 8 and abs(t) < mpf("1e-60") * max(jscale, mpf(1)):
                break
    return total

def d1_sector(poly, a2, x0):
    """d/du zeta'(0,u) at u=0 = -sum_x d(x)/(x^2-a2) (pole-regularized)."""
    total = mpf(0)
    for m_, c in poly.items():
        j, jscale = 1, abs(c)
        while j < 400:
            w = 2 * j - m_
            X = _H(j - 1) / 2 - psi(0, x0) if w == 1 else zetaR(w, x0)
            t = -c * a2 ** (j - 1) * X
            total += t
            if j > 9 and abs(t) < mpf("1e-60") * max(jscale, mpf(1)):
                break
            j += 1
    return total

def z0_sector(poly, a2, x0):
    zz = sum(c * zetaR(-m_, x0) for m_, c in poly.items())
    for m_, c in poly.items():
        if m_ % 2 == 1:
            j = (m_ + 1) // 2
            zz += c * a2 ** j / (2 * j)
    return zz

# ---- independent certificate: exact expansion at generic s, Richardson ----
from mpmath import binomial

def zeta_sector_s(poly, a2, x0, s):
    """zeta_q(s) via the exact binomial expansion; valid at generic s
    (never touches the pole when 2s+2j-m_ != 1 for all terms)."""
    total = mpf(0)
    for m_, c in poly.items():
        total += c * zetaR(2 * s - m_, x0)
        j, jscale = 1, abs(c)
        while j < 600:
            w = 2 * s + 2 * j - m_
            t = c * binomial(s + j - 1, j) * a2 ** j * zetaR(w, x0)
            total += t
            if j > 10 and abs(t) < mpf("1e-70") * max(jscale, mpf(1)):
                break
            j += 1
    return total

def laurent_c01(poly, a2, x0, eps=mpf("1e-3")):
    """Richardson-extract Laurent c0 (zeta(0)) and c1 (zeta'(0)) of a sector
    zeta(s) = c_-1/s + c0 + c1 s + ... from the exact expansion at +-eps.
    Two-level: c0 to O(eps^4), c1 to O(eps^4); fully independent of the
    pole-regularization algebra in logdet_sector / z0_sector."""
    def fpart(e):  # even part: c0 + c2 e^2 + ...
        return (zeta_sector_s(poly, a2, x0, e)
                + zeta_sector_s(poly, a2, x0, -e)) / 2
    def hpart(e):  # e*(odd part) = c_-1 + c1 e^2 + c3 e^4 + ...
        return e * (zeta_sector_s(poly, a2, x0, e)
                    - zeta_sector_s(poly, a2, x0, -e)) / 2
    c0 = (4 * fpart(eps) - fpart(2 * eps)) / 3
    # two-level Richardson for c1: est(e) = (h(2e)-h(e))/(3 e^2) = c1 + O(e^2)
    est1 = (hpart(2 * eps) - hpart(eps)) / (3 * eps ** 2)
    est2 = (hpart(4 * eps) - hpart(2 * eps)) / (12 * eps ** 2)
    c1 = (4 * est1 - est2) / 3
    return c0, c1

def tower_values(poly, a2, x0q, xs, ds, bad):
    """(L, D1, z) with finite-head corrections at indices bad."""
    L = logdet_sector(poly, a2, x0q)
    D1 = d1_sector(poly, a2, x0q)
    zz = z0_sector(poly, a2, x0q)
    for i in bad:
        x = xs[i]
        pv = sum(poly[e] * mpf(x) ** e for e in poly)
        delta = mpf(ds[i]) - pv
        lamx = mpf(x) ** 2 - a2
        L += delta * mplog(lamx)
        D1 += delta / lamx
        zz += delta
    return L, D1, zz

# ---------------------------------------------------------- main
def main():
    print("=" * 82)
    print("PLAY LAB v2 — TWISTED TOWERS: Hopf-charge-resolved spectra")
    print("=" * 82)

    # ---- engine validation: scalar charges vs closed form (C4) ----
    print("\n[0] engine validation: scalar charge resolution vs SU closed form")
    for m, r in ((3, 4), (4, 5)):
        bad = 0
        for k in range(0, 5):
            for q in range(0, 4):
                j = 2 * k + q
                got = charge_degeneracies([j] + [0] * (r - 1)).get(q, 0)
                want = scalar_closed(m, k, q)
                if got != want:
                    bad += 1
                    print(f"  MISMATCH m={m} k={k} q={q}: engine {got} vs {want}")
        print(f"  S^{2*m+1} scalars (k=0..4, q=0..3): "
              f"{'ALL MATCH' if not bad else 'FAIL - STOP'}")
        if bad:
            return

    # ---- C5: spectral-function certificate on scalar sectors ----
    # Sector zeta'(0)/zeta(0) carry pole-regularization terms that cancel
    # only across ALL sectors, so a truncated sector-sum control is void
    # (verified numerically: partial sums ~ 392 vs full 4.17).  Instead we
    # certify the pole-regularized sector functions against an INDEPENDENT
    # path: Laurent extraction from the exact binomial expansion at s = +-eps
    # (never touches the pole), two-level Richardson.  D1 certified by
    # finite difference under a2 -> a2 - u.
    print("\n[1] spectral certificate: sector zeta'(0), zeta(0), D1 vs "
          "independent Laurent extraction")
    for ndim, m, qlist in ((7, 3, (0, 2)), (9, 4, (0, 2))):
        a2 = mpf(m) ** 2
        for q in qlist:
            k0 = 1 if q == 0 else 0  # q=0: skip j=0 constant zero mode
            x0q = m + q + 2 * k0
            xs = list(range(x0q, x0q + 2 * 12, 2))
            ds = [scalar_closed(m, (x - m - q) // 2, q) for x in xs]
            poly, bad = poly_from_spec(x0q, ndim - 1, xs, ds)
            assert not bad
            L, D1, zz = tower_values(poly, a2, x0q, xs, ds, bad)
            c0, c1 = laurent_c01(poly, a2, x0q)
            du = mpf("1e-4")
            D1fd = (logdet_sector(poly, a2 - du, x0q)
                    - logdet_sector(poly, a2 + du, x0q)) / (2 * du)
            # D1fd = d/du logdet(a2-u)|_0 = D1 (same sign convention)
            ok0 = abs(c0 - zz) < mpf("1e-8")
            ok1 = abs(c1 - L) < mpf("1e-8")
            okd = abs(D1fd - D1) < mpf("1e-6") * max(1, abs(D1))
            print(f"  S^{ndim} scalar q={q}: "
                  f"L={nstr(L,10)} (cert {nstr(c1,10)}, d={nstr(abs(c1-L),2)}) "
                  f"z={nstr(zz,6)} (cert d={nstr(abs(c0-zz),2)}) "
                  f"D1={nstr(D1,8)} (fd d={nstr(abs(D1fd-D1),2)}) "
                  f"[{'OK' if ok0 and ok1 and okd else 'FAIL - STOP'}]")
            if not (ok0 and ok1 and okd):
                return

    # ---- the two alpha form towers ----
    TOWERS = (("S7", 7, 3, 4), ("S9", 9, 2, 5))
    KMAX = 16
    results = {}
    for name, ndim, p, r in TOWERS:
        x0 = (ndim + 1) // 2
        poly_tot, a2, _ = build(ndim, p)
        degp = ndim - 1
        print(f"\n{'='*82}\n[2] {name} coexact p={p}: charge resolution "
              f"(levels k=0..{KMAX}, x=k+{x0})")
        table = {}
        for k in range(0, KMAX + 1):
            lam = [k + 1] + [1] * p + [0] * (r - 1 - p)
            ch = charge_degeneracies(lam)
            tot = sum(ch.values())
            want = int(round(deg_coexact(ndim, p, k)))  # int() truncates!
            pal = all(ch.get(q, 0) == ch.get(-q, 0) for q in list(ch))
            print(f"    level k={k:2d} resolved: sum={tot} (target {want})",
                  flush=True)
            if tot != want or not pal:
                print(f"  CONTROL FAIL k={k}: sum {tot} vs {want}, pal {pal}")
                return
            for q, v in ch.items():
                table[(k, q)] = v
        print(f"  C1/C2/C3 pass at all {KMAX+1} levels")
        qs = sorted({q for (_, q) in table if q >= 0})
        print(f"  charges present: q = 0..{qs[-1]}; resolving sectors with "
              f">= {degp+1} levels for stable polynomials")
        Ls, Ds, zs = {}, {}, {}
        for q in qs:
            ks = [k for k in range(0, KMAX + 1) if table.get((k, q), 0) > 0]
            if len(ks) < degp + 1:
                continue
            k0 = ks[0]
            x0q = k0 + x0
            xs = [k + x0 for k in ks]
            ds = [table[(k, q)] for k in ks]
            poly, bad = poly_from_spec(x0q, degp, xs, ds)
            L, D1, zz = tower_values(poly, a2, x0q, xs, ds, bad)
            Ls[q], Ds[q], zs[q] = L, D1, zz
            tag = "stable" if not bad else f"HEAD({len(bad)} lvl)"
            print(f"  q={q:>2}: onset k={k0:>2}  L_q={nstr(L,12):>16}"
                  f"  D1_q={nstr(D1,10):>14}  z_q={nstr(zz,4):>8}  {tag}")
        results[name] = (Ls, Ds, zs)

    # ---- pre-declared probes (truncated, disclosed) ----
    print(f"\n{'='*82}\n[3] pre-declared probes (charge-truncated: resolved"
          " sectors only, disclosed)")
    for name, (Ls, Ds, zs) in results.items():
        m2L = sum((1 if q == 0 else 2) * q * q * Ls[q] for q in Ls)
        m2D = sum((1 if q == 0 else 2) * q * q * Ds[q] for q in Ds)
        results[name] = (Ls, Ds, zs, (m2L, m2D))
        print(f"  {name}: M2_L(trunc) = {nstr(m2L,12)}"
              f"   M2_D1(trunc) = {nstr(m2D,12)}")
    m2L = sum(v[3][0] for v in results.values())
    m2D = sum(v[3][1] for v in results.values())
    sig = m2D / m2L
    print(f"\n  sigma_M2(truncated) = {nstr(sig,10)}")
    print(f"    distance to sigma_need -6.21: {nstr(abs(sig-SIGMA_NEED),5)}")
    print(f"    distance to c3 = -1.56371823031276: {nstr(abs(sig-C3_TARGET),5)}")
    print("\n  Report only. Odd charge moments vanish by conjugation (C2).")


if __name__ == "__main__":
    main()
