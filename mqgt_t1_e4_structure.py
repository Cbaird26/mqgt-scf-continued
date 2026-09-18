#!/usr/bin/env python3
"""E4 RESEARCH RUN: anatomy of the alpha^-1 gate residual.

Open erratum E4 (frozen record: mqgt-scf-independent-verification v1.0-paper).
The T-1 identity gives alpha^-1 = 137.03608245; CODATA 2022 is
137.035999178(21); relative deviation 6.077e-7 vs a 1e-8 gate. A pre-declared
13,057-expression topological family already contains 58 gate-passing
coincidences, so NO fitted correction is citable. This script does NOT search
for fits. It:

  1. Pins the exact target any structural derivation must hit:
     delta = CODATA / theory, decomposed on alpha^3 and alpha^4 bases.
  2. Tests the one physically motivated (non-fitted) hypothesis: that the
     identity yields a bare/geometric alpha and the gap is QED running.
     Computes the scale ratio the running hypothesis would require.
  3. Establishes the exclusion criterion: the program's natural alpha^3
     coefficient pi/2 differs from the needed coefficient by 4.5e-3 relative
     -- far outside rounding -- so the known F3 hit (1-(pi/2)alpha^3) is an
     excluded identity even before multiplicity arguments.
  4. States the resolution standard: c = 1.563718224... must be PRODUCED by a
     trace/spectral invariant of the program's operator content, not fitted.

All arithmetic at 80 digits. No candidate search is performed here; the
multiplicity ceiling from the frozen scan is quoted for context only.
"""

from mpmath import mp, mpf, nstr, pi, log, zeta

mp.dps = 80

CODATA = mpf("137.035999178")
CODATA_ERR = mpf("0.000000035")          # (21) -> ~2.6e-10 relative

def theory_alpha_inv():
    return 1 / ((mpf(9) / (8 * pi ** 4)) * (pi ** 5 / 1920) ** (mpf(1) / 4))

def main():
    th = theory_alpha_inv()
    alpha = 1 / CODATA                    # use measured alpha for bases
    print("=" * 78)
    print("E4 RESEARCH RUN — anatomy of the alpha gate residual")
    print("=" * 78)

    print("\n[1] Exact target for any structural derivation")
    delta = CODATA / th
    need = delta - 1
    print(f"    theory alpha^-1   : {nstr(th, 20)}")
    print(f"    CODATA 2022       : {nstr(CODATA, 15)} +/- {nstr(CODATA_ERR, 3)}")
    print(f"    abs gap           : {nstr(th - CODATA, 10)}")
    print(f"    rel gap           : {nstr((th - CODATA) / CODATA, 6)}  (gate 1e-8: FAIL stands)")
    print(f"    delta - 1         : {nstr(need, 20)}")
    print(f"    log(delta)        : {nstr(log(delta), 20)}")
    c3 = need / alpha ** 3
    c4 = need / alpha ** 4
    print(f"    on alpha^3 basis  : c3 = {nstr(c3, 15)}   <- THE pinned coefficient")
    print(f"    on alpha^4 basis  : c4 = {nstr(c4, 15)}")

    print("\n[2] Running-coupling hypothesis (the one non-fitted physical story)")
    print("    If the identity gives a BARE alpha at scale q, then to one loop:")
    print("      alpha^-1(0) = alpha^-1(q) + (1/(3 pi)) * sum_f N_c Q_f^2 ln(q^2/m_f^2)")
    print("    Required ln(q^2/m_e^2) to bridge the gap with electron alone:")
    gap = th - CODATA
    lnR_e = 3 * pi * gap
    print(f"      ln(q^2/m_e^2) = 3*pi*gap = {nstr(lnR_e, 6)}")
    print(f"      -> q/m_e = exp({nstr(lnR_e/2, 6)}) = {nstr(__import__('mpmath').exp(lnR_e/2), 12)}")
    print("    A scale ratio within 4e-4 of the electron mass is not a threshold;")
    print("    no physical scale sits there. For context, running from q=0 to")
    print("    m_Z moves alpha^-1 by ~9 (alpha^-1(m_Z) = 127.951). VERDICT: the gap")
    print("    is NOT vacuum-polarization running at any natural scale.")

    print("\n[3] Exclusion of the known F3 coincidence")
    c3_natural = -pi / 2   # the F3 hit was 1 - (pi/2) alpha^3: coefficient is negative
    print(f"    needed c3 = {nstr(c3, 15)}")
    print(f"    -pi/2     = {nstr(c3_natural, 15)}")
    print(f"    relative difference = {nstr(abs(c3-c3_natural)/abs(c3), 4)}")
    print("    4.5e-3 off: (1-(pi/2)alpha^3) is excluded as an identity outright,")
    print("    independent of the multiplicity argument (58 gate-passers/13,057).")

    print("\n[3b] Illustrative coincidence (why fits are uncertifiable)")
    c4_rat = -mpf(1500) / 7
    resid = abs((th * (1 + c4_rat * alpha ** 4)) - CODATA) / CODATA
    print(f"    c4 = {nstr(c4, 12)} is within 1.1e-7 of -1500/7 = {nstr(c4_rat, 12)};")
    print(f"    (1 - (1500/7) alpha^4) passes the 1e-8 gate with residual {nstr(resid, 3)}.")
    print("    -1500/7 has no derivation from the program. This is what one of the")
    print("    58 gate-passing coincidences looks like up close: gate-passing is")
    print("    necessary, not sufficient.")

    print("\n[4] Resolution standard (what would close E4)")
    print("    A derivation must PRODUCE c3 = 1.563718224... from the program's")
    print("    operator content (e.g. a trace anomaly, heat-kernel coefficient, or")
    print("    index density of the Hopf/Beltrami fields already in the theory),")
    print("    with each factor identifiable BEFORE comparison to CODATA.")
    print("    Program constants available to such a derivation (for reference):")
    print(f"      zeta(3)*13/(24pi) = {nstr(zeta(3)*13/(24*pi), 12)}")
    print(f"      zeta(5)/(4pi^2)   = {nstr(zeta(5)/(4*pi**2), 12)}")
    print(f"      S7/56             = {nstr(mpf('1.74845220445')/56, 12)}")
    print(f"      S7'/16            = {nstr(mpf('0.41364465819')/16, 12)}")
    print("    NOTE: listing these is NOT a candidate search; any combination found")
    print("    by fitting remains coincidence-class per the frozen E4 scan.")

    print("\n[5] Status")
    print("    E4 REMAINS OPEN. The target is pinned to 15 digits; the running")
    print("    hypothesis is excluded numerically; the resolution standard is set.")
    print("    Next honest step: attempt the heat-kernel/index derivation of the")
    print("    alpha^3 coefficient from the T-3 operator content (S7, S7' above).")

if __name__ == "__main__":
    main()
