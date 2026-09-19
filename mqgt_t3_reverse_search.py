"""T-3 REVERSE-ENGINEERING SEARCH v2 (pre-declared families, stabilized).

Claim under test (mqgt-scf-science-public): the TUFT "S^7 dressing" constant
S7' = 0.41364, audited as "zeta'_{Delta_2}(0) on S^7 = -0.41364".
Upstream manifest already rates T-3 FAIL (constants are paper-quoted literals,
not derived). mqgt_t3_independent.py found NO S^7 tower matching -0.41364
(Hodge Delta_2 on S^7 = -0.61982401; coexact-2 alone = -1.07538187).

v1 RESULT (this file's predecessor): a pre-declared scan over standard
spectral-zeta conventions on round odd spheres found a single 5-digit hit:
    zeta'(0) of coexact 2-forms on S^9  =  -0.41364465819   (target -0.41364)
No S^7 convention matches. S^9 is the sphere of the S^1 -> S^9 -> CP^4 Hopf
fibration in the program's own compactification map.

v2 fixes v1's numerics: degeneracy-poly coefficients now filtered against a
relative threshold (v1 kept ~1e-50 odd-parity noise, which could hit the
zeta(1) pole), and each tower is summed with an adaptive early-break jmax at
dps=90, then re-checked at dps=60/jmax=60 (v1 showed jmax=120 at dps=60
accumulates rounding noise for fast-converged towers). Secondary exploratory
target: S7 = 1.748452 (the alpha^3/56 coefficient), same families.

PRE-DECLARED FAMILIES:
  F-A: zeta'(0) per coexact p-form tower, S^n, n in {3,5,7,9,11} (+S^1 scalar)
  F-B: zeta'(0) per full Hodge p-form tower (ce_p + ce_{p-1})
  F-C: conformally coupled scalar zeta'(0)
  F-D: zeta(0) of the same towers
  F-E: multiples c*v, c in {+-1/2, +-1, +-2}
  F-R: radius required to force each target (diagnostic only)
CONTROLS:
  K1: ce1 k=0 degeneracy = n(n+1)/2 (Killing fields)
  K2: ce2 k=0 degeneracy = C(n+1,3) for n>=5
  K3: degeneracy polys even in x; extra Weyl values reproduced
  K4: per-tower two-precision agreement (else tower flagged UNSTABLE)
NOTE: v1's "torsion ~ 0" control was withdrawn -- that expectation was
incorrect for non-acyclic spheres; it is not a machinery test.
Targets: T1 = -0.41364 (hit tol 5e-4), T2 = +-1.748452 (exploratory, tol 5e-4).
"""

from mpmath import mp, mpf, nstr, zeta, log, exp, binomial

TARGETS = [mpf("-0.41364"), mpf("1.748452"), mpf("-1.748452")]
HIT_TOL = mpf("5e-4")
NEAR_TOL = mpf("1e-2")


def weyl_dr(lam, r):
    m = [r - 1 - i for i in range(r)]
    l = [lam[i] + m[i] for i in range(r)]
    d = mpf(1)
    for i in range(r):
        for j in range(i + 1, r):
            d *= mpf(l[i] ** 2 - l[j] ** 2) / (m[i] ** 2 - m[j] ** 2)
    return d


def deg_scalar(n, k):
    return weyl_dr([k] + [0] * ((n + 1) // 2 - 1), (n + 1) // 2)


def deg_coexact(n, p, k):
    r = (n + 1) // 2
    lam = [k + 1] + [1] * p + [0] * (r - 1 - p)
    d = weyl_dr(lam, r)
    if p == r - 1:
        d *= 2
    return d


def zetaR(w, x0, der=0):
    """zeta_H(w, x0) = sum_{n>=x0} n^{-w} (or its w-derivative).

    Hybrid: for large w, direct summation (a few terms suffice). For small w,
    Riemann zeta minus the finite head. The naive zeta_R-minus-head form is
    CATASTROPHICALLY UNSTABLE for w >~ dps/log10(2): zeta_R(w) rounds to 1,
    killing the true leading term x0^{-w} and leaving a harmonic ghost tail.
    (This artifact contaminated v1/v2 high-j tails; diagnosed 2026-09-17.)
    """
    w = mpf(w)
    if der == 0 and w > 40:
        s, n, cutoff = mpf(0), int(x0), mpf(10) ** (-(mp.dps - 15))
        while True:
            t = mpf(n) ** (-w)
            s += t
            n += 1
            if t < cutoff:
                return s
    if der == 1 and w > 40:
        s, n, cutoff = mpf(0), int(x0), mpf(10) ** (-(mp.dps - 15))
        while True:
            t = -log(n) * mpf(n) ** (-w)
            s += t
            n += 1
            if abs(t) < cutoff:
                return s
    val = zeta(w, derivative=der)
    for q in range(1, int(x0)):
        if der == 0:
            val -= mpf(q) ** (-w)
        else:
            val += log(q) * mpf(q) ** (-w)
    return val


def fit_poly(degfun, npts, xshift, deg):
    import mpmath
    ks = list(range(npts))
    ys = [degfun(k) for k in ks]
    M = mpmath.matrix([[mpf(k + xshift) ** i for i in range(deg + 1)] for k in ks])
    c = mpmath.lu_solve(M, mpmath.matrix(ys))
    scale = max(abs(mpf(v)) for v in c)
    poly = {i: mpf(c[i]) for i in range(deg + 1) if abs(c[i]) > scale * mpf("1e-30")}
    odd = max([abs(v) for i, v in poly.items() if i % 2 == 1] + [mpf(0)])
    return poly, scale, odd / scale


def zp0(poly, a, x0, tol=mpf("1e-60"), jcap=400):
    """zeta'(0); early break once the j-tail is below tol * scale."""
    scale = max(abs(v) for v in poly.values())
    total = mpf(0)
    for m_, c in poly.items():
        total += c * 2 * zetaR(-m_, x0, der=1)
        jterm_scale = abs(c)
        for j in range(1, jcap + 1):
            t = c * a ** (2 * j) / j * zetaR(2 * j - m_, x0)
            total += t
            if j > 8 and abs(t) < tol * max(jterm_scale, mpf(1)):
                break
    return total


def z0(poly, x0):
    return sum(c * zetaR(-m_, x0) for m_, c in poly.items())


def check(name, value, hits, nears):
    for t in TARGETS:
        if abs(value - t) < HIT_TOL:
            hits.append((name, value, t))
        elif abs(value - t) < NEAR_TOL:
            nears.append((name, value, t))


def main():
    mp.dps = 90
    hits, nears, rows, unstable = [], [], [], []
    print("=" * 78)
    print("T-3 REVERSE SEARCH v2 (stabilized)")
    print("=" * 78)

    print("\n[controls]")
    ok = True
    for n in (3, 5, 7, 9, 11):
        d1 = deg_coexact(n, 1, 0)
        need1 = mpf(n * (n + 1)) / 2
        good = abs(d1 - need1) < mpf("1e-40")
        ok &= good
        line = f"    S^{n} ce1 k=0 = {nstr(d1, 6)} (Killing, need {nstr(need1, 6)}) {'OK' if good else 'FAIL'}"
        if n >= 5:
            d2 = deg_coexact(n, 2, 0)
            need2 = binomial(n + 1, 3)
            good2 = abs(d2 - need2) < mpf("1e-40")
            ok &= good2
            line += f" | ce2 k=0 = {nstr(d2, 6)} (need {nstr(need2, 6)}) {'OK' if good2 else 'FAIL'}"
        print(line)
    if not ok:
        print("    CONTROL FAILURE -- aborting.")
        return

    for n in (3, 5, 7, 9, 11):
        pmax = (n - 1) // 2
        ce = {}
        specs = [("scalar", 0, (n - 1) / 2, (n - 1) / 2, (n + 1) / 2)]
        specs += [(f"ce{p}", p, (n - 1) / 2 - p, (n + 1) / 2, (n + 1) / 2)
                  for p in range(1, pmax + 1)]
        for name, p, a, xshift, x0 in specs:
            df = (lambda k: deg_scalar(n, k)) if p == 0 else \
                 (lambda k, p=p: deg_coexact(n, p, k))
            poly, scale, ev = fit_poly(df, n, xshift, n - 1)
            verr = max(abs(sum(c * mpf(k + xshift) ** i for i, c in poly.items())
                           - df(k)) for k in (n, n + 1, n + 2))
            if ev > mpf("1e-20"):
                print(f"    S^{n} {name}: UNEVEN poly (ratio {nstr(ev, 2)}) -- EXCLUDED")
                continue
            mp.dps = 90
            hi = zp0(poly, mpf(a), int(x0))
            mp.dps = 60
            lo = zp0(poly, mpf(a), int(x0), tol=mpf("1e-40"), jcap=80)
            zz = z0(poly, int(x0))
            rel = abs(hi - lo) / max(abs(hi), mpf("1e-30"))
            tag = "" if rel < mpf("1e-8") else "  UNSTABLE"
            if tag:
                unstable.append(f"S^{n} {name}")
            ce[p] = (hi, zz)
            rows.append((f"S^{n} {name:8s}", hi, zz, tag, verr))
            check(f"F-A S^{n} {name}", hi, hits, nears)
            check(f"F-D S^{n} {name} zeta(0)", zz, hits, nears)
        # full Hodge towers
        for p in range(1, pmax + 1):
            if p in ce and (p - 1) in ce:
                full = ce[p][0] + ce[p - 1][0]
                check(f"F-B S^{n} full-{p}", full, hits, nears)
        # conformal scalar: a = 0, x0 = (n-1)/2, scalar poly
        poly, scale, ev = fit_poly(lambda k: deg_scalar(n, k), n, (n - 1) / 2, n - 1)
        mp.dps = 90
        conf = zp0(poly, mpf(0), int((n - 1) / 2))
        mp.dps = 60
        rows.append((f"S^{n} conf-scal", conf, z0(poly, int((n - 1) / 2)), "", mpf(0)))
        check(f"F-C S^{n} conformal scalar", conf, hits, nears)

    s1 = 4 * zeta(0, derivative=1)
    rows.append(("S^1 scalar   ", s1, mpf(-1), "", mpf(0)))
    check("F-A S^1 scalar", s1, hits, nears)

    print("\n" + "=" * 78)
    print("VALUE TABLE (unit radius; values at dps=90, adaptive tail)")
    print("=" * 78)
    for lbl, zp, zz, tag, verr in rows:
        print(f"    {lbl:16s} zeta'(0) = {nstr(zp, 14):>20s}   zeta(0) = {nstr(zz, 8):>10s}{tag}")

    print("\n[F-E] simple multiples c*v:")
    for lbl, zp, zz, tag, verr in rows:
        for c in (mpf("0.5"), mpf(2), mpf(-1), mpf("-0.5"), mpf(-2)):
            check(f"F-E {c}*({lbl.strip()})", c * zp, hits, nears)
    print("    done")

    print("\n[F-R] radius forcing each target (diagnostic):")
    for lbl, zp, zz, tag, verr in rows:
        if abs(zz) > mpf("1e-30") and abs(zz) < mpf("1e10"):
            for t in TARGETS[:1]:
                R = exp((t - zp) / (2 * zz))
                if mpf("0.5") < R < mpf("1.5"):
                    print(f"    {lbl.strip():16s} -> R = {nstr(R, 8)} for target {nstr(t, 8)}")

    print("\n" + "=" * 78)
    if hits:
        print("HITS (|diff| < 5e-4):")
        for name, v, t in hits:
            print(f"    {name} = {nstr(v, 14)}  target {nstr(t, 9)}  diff={nstr(v - t, 3)}")
    else:
        print("NO HITS within 5e-4 in any pre-declared family.")
    if nears:
        print("near misses (5e-4 < |diff| < 1e-2):")
        for name, v, t in nears:
            print(f"    {name} = {nstr(v, 14)}  target {nstr(t, 9)}  diff={nstr(v - t, 3)}")
    if unstable:
        print("UNSTABLE towers (two-precision disagreement; values not trustworthy):")
        for u in unstable:
            print(f"    {u}")
    print("=" * 78)


if __name__ == "__main__":
    main()
