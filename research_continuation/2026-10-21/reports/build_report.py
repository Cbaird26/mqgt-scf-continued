#!/usr/bin/env python3
"""Create the research continuation report from the executed result records."""
from __future__ import annotations

import html
import json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    PageBreak, Preformatted, KeepTogether,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "Theory_of_Everything_Continuation_2026-10-21.pdf"
FONTS = Path("/usr/share/fonts/truetype/dejavu")
for name, filename in [("Body", "DejaVuSans.ttf"), ("Bold", "DejaVuSans-Bold.ttf"),
                       ("Mono", "DejaVuSansMono.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Bold", italic="Body", boldItalic="Bold")
NAVY = colors.HexColor("#142e43")
TEAL = colors.HexColor("#136c80")
ORANGE = colors.HexColor("#a65324")
PALE = colors.HexColor("#edf4f6")
GRAY = colors.HexColor("#52616d")
WIDTH = A4[0] - 92
styles = {
    "title": ParagraphStyle("title", fontName="Bold", fontSize=25, leading=30, textColor=NAVY, spaceAfter=15),
    "subtitle": ParagraphStyle("subtitle", fontName="Body", fontSize=13, leading=19, textColor=TEAL, spaceAfter=12),
    "h1": ParagraphStyle("h1", fontName="Bold", fontSize=18.5, leading=23, textColor=NAVY, spaceAfter=12),
    "h2": ParagraphStyle("h2", fontName="Bold", fontSize=11.6, leading=16, textColor=TEAL, spaceBefore=9, spaceAfter=6, keepWithNext=True),
    "body": ParagraphStyle("body", fontName="Body", fontSize=9.6, leading=13.5, textColor=NAVY, spaceAfter=6,allowOrphans=0,allowWidows=0),
    "small": ParagraphStyle("small", fontName="Body", fontSize=8.3, leading=11.5, textColor=GRAY, spaceAfter=6,allowOrphans=0,allowWidows=0),
    "table": ParagraphStyle("table", fontName="Body", fontSize=8.6, leading=11.8, textColor=NAVY),
    "th": ParagraphStyle("th", fontName="Bold", fontSize=8.5, leading=11.5, textColor=colors.white),
    "eq": ParagraphStyle("eq", fontName="Mono", fontSize=8.6, leading=12.8, textColor=NAVY, backColor=PALE, borderPadding=8, spaceBefore=5, spaceAfter=11),
}
story = []


def load(path):
    return json.loads((ROOT / path).read_text())


def p(text, style="body"):
    story.append(Paragraph(html.escape(text), styles[style]))


def h(text):
    p(text, "h2")


def chapter(number, title):
    if story:
        story.append(PageBreak())
    p(f"{number:02d} / {title}", "h1")


def eq(text):
    story.append(Preformatted(text, styles["eq"]))


def table(headers, rows, widths):
    data = [[Paragraph(html.escape(str(x)), styles["th"]) for x in headers]]
    data += [[Paragraph(html.escape(str(x)), styles["table"]) for x in row] for row in rows]
    t = Table(data, colWidths=[WIDTH*x for x in widths], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PALE]),
        ("LINEBELOW", (0,-1), (-1,-1), .5, colors.HexColor("#c7d5de")),
    ]))
    story.append(t)
    story.append(Spacer(1,10))


def figure(path, caption, max_height=235):
    from PIL import Image as PILImage
    file = ROOT / path
    with PILImage.open(file) as im:
        w, hgt = im.size
    scale = min(WIDTH/w, max_height/hgt)
    story.append(Image(str(file), width=w*scale, height=hgt*scale, hAlign="CENTER"))
    p(caption,"small")


def source(text):
    p(text,"small")


def footer(canvas, doc):
    canvas.saveState()
    w, hg = A4
    canvas.setStrokeColor(colors.HexColor("#c7d5de"))
    canvas.line(46, hg-35, w-46, hg-35)
    canvas.setFont("Body",7.7)
    canvas.setFillColor(GRAY)
    canvas.drawString(46,hg-26,"MQGT-SCF / ZoraASI research continuation")
    canvas.drawRightString(w-46,hg-26,"21 October 2026")
    canvas.line(46,35,w-46,35)
    canvas.drawString(46,23,"Conditional calculations | Source and interpretation boundaries retained")
    canvas.drawRightString(w-46,23,str(doc.page))
    canvas.restoreState()


def main():
    common=load("common/common_results.json")
    thermal=load("thermal/results/scan_summary.json")
    tr={r["case"]:r for r in thermal}
    measurement=load("measurement/measurement_results.json")
    em=load("electromagnetic/profile_identifiability_results.json")
    uv=load("uv/results.json")
    memory=load("agency/synthetic_memory_results.json")

    p("Theory of Everything\nResearch Continuation", "title")
    p("Six workstreams carried into executable calculations, public-data analysis and explicit scientific tests", "subtitle")
    p("Prepared from the supplied Baird research archive, pinned Cbaird26 source repositories and primary technical sources. This report records the work executed on 21 October 2026. The accompanying package includes scripts, input provenance, tables, study protocols and full technical notes.")
    h("What changed")
    table(["Workstream", "Executed advance", "Consequence"], [
        ("Common action", "Fixed portal normalization, basis rules and unresolved parameters.", "Cross-route calculations now have a checkable interface."),
        ("Thermal history", "Reproduced the momentum network; evolved 12 initial preparations.", "The solved interval retains initial-state memory."),
        ("Measurement", "Refit all 3,895 real public count bins and tested attenuation identifiability.", "Residual statistics and contrast calibration block a naive scalar limit."),
        ("Electromagnetic", "Extended the positive profile family and built a stronger same-local-data example.", "Finite local spectral data do not select a unique exact coupling."),
        ("Ultraviolet", "Projected the scalar trace through degree six and audited the assembled flow.", "Several convention and feedback defects are now explicit."),
        ("Operational bridge", "Ran a prespecified synthetic causal-memory experiment with held-out controls.", "The defined memory mechanism is testable; no experience bridge is supplied."),
    ], [.20,.42,.38])
    h("Scientific status")
    p("The strongest common result is a more constrained research program. Several calculations reproduce, several new conditional results are established, and specific obstacles are now quantified. A complete, empirically validated Theory of Everything is not established by these outputs. Unspecified physics remains an explicit dependency rather than a fitted explanation.")
    source("Notation: [A1] identifies the uploaded archive; [T1], [U1] the pinned repositories; [D1-D2] public experimental sources; [P1-P5] primary theory papers. [N-*] denotes new results in this package. Full source map: section 13.")

    chapter(2,"Common action and parameter contract")
    p("The shared low-energy branch uses two real gauge-singlet scalars, canonical positive kinetic terms, a zero singlet vacuum and an unmixed Higgs. The exact symmetry is simultaneous inversion of both scalars. Separate sign flips are generally not symmetries. Natural units are used for field calculations; apparatus quantities retain SI units with an explicit conversion boundary. [A1, pp.7561-7563, 7576-7582]")
    eq("V = V_SM + (1/2) phi^T M0^2 phi\n    + (1/2) (phi^T K phi) H^dagger H\n    + (1/4!) lambda_abcd phi_a phi_b phi_c phi_d\nMphysical^2 = M0^2 + (v^2/2) K")
    p("The quartic tensor is fully symmetric and has five independent singlet components. Their values are not supplied. Curvature couplings, higher operators, the renormalization prescription and global vacuum conditions are also unfinished. This is a common interface, not an assertion that the displayed terms are a complete renormalized theory.")
    h("A numerical point that is now normalized consistently")
    p("The thermal checkpoint fixes masses 10 and 11.5 GeV, m_h=125 GeV, v=246 GeV, K11=K22=0.001 and K12=-0.001. With the same portal convention, the new code obtains the following tree-level Higgs pair-production widths. [T1; N-common]")
    widths=common["tree_widths_GeV"]
    table(["Channel", "Production width (keV)"],[("h to s1 s1",f"{widths['11']*1e6:.6f}"),("h to s1 s2",f"{widths['12']*1e6:.6f}"),("h to s2 s2",f"{widths['22']*1e6:.6f}"),("Total",f"{widths['total_production']*1e6:.6f}")],[.62,.38])
    p("The mixed final state has twice the identical-channel normalization at equal masses and equal portal entries. If every daughter were detector-invisible and the other Higgs width were 4.1 MeV, the conditional fraction would be 0.460657%. This is not an observed branching fraction: the heavier state can decay to the lighter state plus Standard Model products.")
    h("Cross-workstream matching")
    eq("C = f_a m_a K_mass / (2 m_h^2),   [C] = GeV^-1\nL_eff = (s^T C s) fbar f\n(Box I + M^2) s = 2 n_a C s + ...")
    p("Matter changes the scalar mass matrix multiplicatively; zero scalar field remains a solution. For two fields, detector noise contracts C_ij C_kl with the connected spectrum of the composite operators s_i s_j. A one-scalar noise formula is a special case. The contract states its two-sided Fourier convention and the needed stationary, heavy-probe approximations.")
    source("Seven algebraic checks pass. Rotating all mass and portal data changes the total width by at most 8.9e-16 relatively. The UV repository's separately even scalar potential is narrower than this simultaneous-Z2 interface; an explicit basis/extension match remains required. Files: common/action_parameter_contract.json and common/portal_interface.py.")

    chapter(3,"Thermal history: initial-state memory")
    p("The frozen network was downloaded at a pinned commit and its source hashes verified. It contains 192 finite momentum cells plus a semi-infinite tail for each species: 386 states in total. The inherited model evolves scalar-fermion scattering/conversion, heavy decay and inverse absorption, and pair annihilation/inverse creation through T=0.5 to 1/3 GeV. The bath remains an ideal Maxwell-Boltzmann fermion gas in this baseline. [T1]")
    p("The equilibrium-prepared baseline reproduces the archived endpoint: Tkin/T=0.750271338, heavy fraction 0.036632159 and net number loss 31.5358 parts per million. Tkin is the pressure moment P_scalar/n_scalar. The equilibrium heavy fraction at the endpoint is 0.01340992, so this is not full kinetic and species equilibrium. [N-thermal]")
    h("New preparations, same evolution equations")
    table(["Initial preparation", "Final Tkin/T", "Final heavy fraction"], [
        ("Reference at Tscalar/Tbath=1",f"{tr['z_1']['final_Tkin_over_T']:.6f}",f"{tr['z_1']['final_heavy_fraction']:.6f}"),
        ("Cooler shape: Tscalar/Tbath=0.75",f"{tr['kinetic_0.75']['final_Tkin_over_T']:.6f}",f"{tr['kinetic_0.75']['final_heavy_fraction']:.6f}"),
        ("Hotter shape: Tscalar/Tbath=1.25",f"{tr['kinetic_1.25']['final_Tkin_over_T']:.6f}",f"{tr['kinetic_1.25']['final_heavy_fraction']:.6f}"),
        ("Initial heavy fraction 0",f"{tr['heavy_0']['final_Tkin_over_T']:.6f}",f"{tr['heavy_0']['final_heavy_fraction']:.6f}"),
        ("Initial heavy fraction 0.25",f"{tr['heavy_0.25']['final_Tkin_over_T']:.6f}",f"{tr['heavy_0.25']['final_heavy_fraction']:.6f}"),
    ], [.54,.23,.23])
    p("The cooler/hotter cases keep total abundance and initial species fractions fixed while changing each species' normalized momentum shape. The species-preparation cases keep abundance and shape temperature fixed. These distinctions prevent a temperature change from silently changing chemical abundance at the same time.")
    figure("thermal/results/thermal_initial_condition_sensitivity.png", "New conditional evolution of imposed initial states. Abundance, momentum shape and species preparation are separate tests. Numerical sensitivity and model limitations are reported in the thermal note.",max_height=235)
    p("The differences in endpoint temperature and heavy fraction are much larger than the measured numerical sensitivities. The declared interval therefore does not erase preparation information. Any claimed physical cosmology must explain how its initial state was produced or demonstrate attraction over a justified larger history.")

    chapter(4,"Thermal abundance, validation and thermodynamics")
    p("At the equilibrium initial shape, a common scalar fugacity z multiplies f_i(p)=exp(-E_i/T0). The scan uses z from 10^-6 to 10^4. Only the boundary condition changes; the bath's inverse-creation term is kept fixed. Scaling that source with z would describe a different physical problem. [N-thermal]")
    table(["Initial z", "Final number / actual initial", "Interpretation within this window"], [
        ("10^-6", "3.563015 (split); 3.563739 (independent ODE)", "Inverse creation dominates a tiny initial population."),
        ("0.01", "1.000256", "Abundance remains nearly proportional to its initial value."),
        ("1", "0.9999685", "Reproduced reference population."),
        ("100", "0.996602", "Only 0.340% of the imposed abundance is lost."),
        ("10^4", "0.745726", "Formal high-density stress test of the declared reaction network."),
    ], [.13,.34,.53])
    h("An independent source bound")
    eq("N_final <= z + B\nB = integral d_eta alpha E^T A E\n  = 2.56373920516e-6  (reference population units)")
    p("The inequality follows from number conservation of the linear operators and nonnegative annihilation. Adaptive quadrature of the source gives B independently of the evolved population. An unsplit DOP853 solve at z=10^-6 differs from z+B by only 2.8e-16 reference units. The small split-solver error decreases consistently with second-order time stepping.")
    p("Time, momentum-grid, temperature-bank and quadrature changes were tested, with an unsplit solver for six representative cases. Disabling pair creation and annihilation conserves number to 2.8e-15. These are numerical checks within a cell closure and a specified bath, not certified physical uncertainty bounds.")
    h("What the high-z point means")
    p("Dilute phase-space occupancy and small scalar/radiation energy density hold for the scanned boundary conditions. However, omitted Higgs-mediated scalar-only collisions grow with z: the source audit's initial tagged rate/H reaches about 0.135 at z=10^4. That case is a stress test of the truncated equations; it is not a robust full-theory prediction.")
    h("Equation-of-state extension")
    eos_text=HERE/"eos_report_insert.txt"
    if eos_text.is_file():
        for paragraph in eos_text.read_text().split("\n\n"):
            if paragraph.strip(): p(paragraph.strip() + " [P4-P5; N-EOS]")
    else:
        p("A separately scoped extension uses the published 2+1-flavor lattice-QCD thermodynamics and ideal photon/lepton/neutrino contributions. Entropy conservation requires a^3 s(T)=constant; changing g_s(T) also changes the p/T momentum transport and dt/dln(T0/T). The completed numerical record and its collision-kernel limitations are provided in the thermal extension note. [P4-P5]")

    chapter(5,"Measurement: real count data and model adequacy")
    p("The measurement work uses the authors' public sodium-cluster interference dataset, not simulated detection data. Its original zip matches the published MD5 and is preserved with SHA-256 and CC BY 4.0 attribution. The 95 April 22 power scans contain 3,895 position bins and 10,772,714 recorded counts. [D1-D2]")
    eq("mu_jk = a_j [1 + b_j cos(2 pi x_jk/d)\n                 + c_j sin(2 pi x_jk/d)]\nd = 133 nm;  sqrt(b_j^2+c_j^2) < 1")
    p("Each scan is fit directly at its recorded positions with a separate normalization, cosine and sine coefficient. This avoids artificial phase bounds and modulo-period binning. Independent Poisson counts are a working likelihood to be evaluated against the residuals, not an assumed detector truth. [N-measurement]")
    table(["Diagnostic", "Result"], [
        ("Pooled Poisson deviance", f"{measurement['joint_deviance']:.3f}"),
        ("Residual degrees of freedom", str(measurement['total_residual_dof'])),
        ("Pooled Pearson statistic / df",f"{measurement['joint_pearson_dispersion']:.6f}"),
        ("Scans with individual Pearson/df above 2", "92 of 95"),
        ("Maximum visibility difference from ordinary least squares", "0.00072196 = 0.072196 percentage points"),
        ("Dispersion with second harmonic and scan-order trend", "3.401120"),
    ], [.63,.37])
    figure("measurement/measurement_diagnostics.png", "Left: fitted first-harmonic visibility. Middle: residual variation relative to the Poisson sinusoid. Right: an attenuation/contrast reparameterization that leaves all predicted counts unchanged.",max_height=165)
    p("Central visibilities change little between these Poisson and ordinary least-squares fits, while residual variation is about 3.44 times the naive Poisson expectation. Adding a second harmonic and a linear scan-order trend does not remove that discrepancy. The cause could involve the signal model, detector statistics, drift or correlations; these calculations do not diagnose a unique noise mechanism.")
    source("A separate trust-region optimizer from zero contrast reproduces all 95 fits, with maximum visibility difference 8.7e-10. Conditional Fisher errors in the CSV are not claimed to have calibrated coverage. No new-field detection or exclusion is inferred.")

    chapter(6,"Measurement: separating attenuation from contrast")
    p("For a scalar proposal that only supplies a common attenuation across a power scan, the central identifiability question can be answered exactly, before choosing a statistical optimizer. [N-measurement]")
    eq("V_observed(P) = A V_Q(P) exp(-chi)\nlog A -> log A + delta\nchi   -> chi   + delta")
    p("These simultaneous changes leave every expected count unchanged. The log-contrast and attenuation derivative columns are negatives of one another, so their Fisher block has rank one. The data can determine A exp(-chi), but cannot uniquely separate the two factors without calibration or a distinct predicted dependence. Bounds on A can truncate the ambiguity without identifying its physical mechanism.")
    p("The supplied numerical ridge applies this symmetry to each fitted scan contrast over chi=0 to 0.4; all rescaled contrasts remain below one. Counts agree within 9.1e-13 and total deviance within 3.9e-11. It demonstrates the free per-scan nuisance model. The global identity for a fixed quantum visibility curve is analytical; no absolute V_Q curve was fitted in this new count analysis.")
    h("A matched experiment requires more than a rate parameter")
    p("The source apparatus has 133 nm gratings, equal gaps of 0.98375 m, mean speed 158 m/s and spread 9 m/s. Its author-code mass selection is near 168.94 kDa. These imply a mean total flight of 12.4525 ms and a first-harmonic triangular-path maximum near 110.57 nm. A full Talbot-Lau prediction averages complex harmonics over mass and velocity before forming visibility. [D1; A1, pp.7600-7605]")
    p("The portal matching must be extended from a point fermion/nucleon to the nanoparticle's composite response, form factor and recoil. A moving probe generally samples nonzero-frequency bath noise. A stationary zero-frequency Markov coefficient alone is insufficient for a finite-time path filter. A cosmological GeV bath is not a measured local laboratory scalar population.")
    table(["Required input", "Concrete completion test"], [
        ("Composite coupling and baseline", "Match the object response and reconcile absolute optical/absorption conventions."),
        ("Local scalar state", "Specify measured or explicitly conditioned occupation, spectrum and source preparation."),
        ("Finite-time response", "Compute the moving-object harmonic filters and validity of the approximations."),
        ("Instrument statistics", "Validate a count/correlation model using repeated reference acquisitions."),
        ("Distinguishing intervention", "Predict velocity, geometry or material dependence outside the calibrated nuisance space."),
        ("Inference and replication", "Freeze the test, verify interval coverage and assess held-out acquisition."),
    ], [.30,.70])
    source("Full implementation-ready specification: measurement/APPARATUS_AND_INFERENCE_PROTOCOL.txt. Public-data analysis does not create unprovided GATE03 apparatus data or turn the authors' collapse-model analysis into a portal-field limit.")

    chapter(7,"Electromagnetic normalization: a continuum of profiles")
    p("The continued archive model uses a common spectral action with an overall normalization kappa, a profile f, a round compact internal sphere and a stated hypercharge charge convention. For positive exponential mixtures f(u)=sum w_j exp(-a_j u), exact internal mode sums determine the gauge and gravitational-radius coefficients after the imposed flat-vacuum subtraction. This remains a low-external-derivative construction. [A1, pp.7592-7599]")
    eq("a_j = (5269/8220) j,   j=1,...,5\nw_j(t) = 1/5 + t v_j/2560\nv = (1, -32, 162, -256, 125)\nStrict positivity:  -256/81 < t < 2")
    p("Four moment constraints have exact rank four and leave one free direction. Every member has the same f(0), m1, m2 and m3. The archived t=-1,+1 pair reproduces. The new 1,001-point scan follows the stationary-radius branch near R=1.3 across the complete positive interval and its nonnegative closure endpoints. [N-electromagnetic]")
    table(["Coefficient", "Lower closure endpoint", "Upper closure endpoint"], [
        ("Stationary R", "1.3023809226", "1.3017554722"),
        ("Z_Y / kappa", "0.2452149581", "0.2455287756"),
        ("Z_Y / (M4 r*)^2", "0.5212645830", "0.5230776785"),
    ], [.38,.31,.31])
    figure("electromagnetic/spectral_profile_sensitivity.png", "The exact compactified coefficients vary despite identical specified leading local profile data. Orange points reproduce the archive's pair; the continuous curve is new.",max_height=215)
    p("The endpoint change is 0.1279765% for Z_Y/kappa and 0.3478263% for the ratio that removes the common normalization. The latter shows that the ambiguity cannot be absorbed solely into kappa while preserving both observables. Sampled monotonicity and positive restricted potential curvature do not prove global uniqueness of roots or complete radion stability.")

    chapter(8,"Electromagnetic: what extra data can actually fix")
    p("Within the five fixed nodes, one extra derivative datum closes the one-dimensional ambiguity. The relation is exact and has a nonzero slope. [N-electromagnetic]")
    eq("f_t'(0) = -5269/2740 - t (5269/876800)")
    p("A supplied value of f'(0) therefore gives a unique t, if it falls in the admissible interval. An extra Mellin moment also identifies t in that finite ansatz. This is mathematical identification after restricting the function class; it does not explain which value nature supplies or why that class should be selected.")
    h("A stronger counterexample in a larger positive class")
    eq("a_j = (5269/8220) j,   j=1,...,6\nb = (1/5,1/5,1/5,1/5,1/5,0)\nv6 = (-1,40,-270,640,-625,216)\nw_j(s) = b_j + s (v6)_j/7680")
    p("The new six-node family preserves the original five-node center's exact f(0), m1, m2, m3 and f'(0). Thus it preserves the same specified local profile factors through the next heat coefficient a8. Both s=1 and s=2 have strictly positive weights, yet their exact compactified coefficients differ:")
    table(["Quantity", "s=1", "s=2"], [
        ("Stationary R", "1.30210699943201", "1.30221755151233"),
        ("Z_Y/kappa", "0.245420268242143", "0.245433772799502"),
        ("Z_Y/(M4 r*)^2", "0.522230265240659", "0.522085021526615"),
    ], [.34,.33,.33])
    p("The gauge coefficient changes by 0.005502625%; the normalization-independent ratio changes by -0.027812198%. This is a counterexample to uniqueness from those local data in the declared positive-mixture class. It does not show that every possible microscopic selection rule must fail.")
    h("Verification and the remaining physical task")
    p("Thirty-eight checks cover exact rational constraints, positivity, rank, source reproduction, scale rescaling, derivative checks and finite-family inversion. Independently coded 70-digit Decimal evaluations agree with the ordinary calculation at about 2.3e-15 at selected points. Tail bounds apply to truncated heat values; they do not certify every printed digit or globally enclose every stationary root.")
    p("The missing physical inputs are a justified profile and normalization, quantum consistency, the full electroweak embedding, threshold running and a canonically normalized radion sector. Each profile's subtraction is determined by the same imposed flat-vacuum rule; a universal fixed numerical subtraction was not held across the comparison. Hypercharge normalization at this stage is not the measured photon fine-structure constant.")
    source("Complete identities, stationary sums, positivity domains, derivative conditioning and convergence records are in electromagnetic/RESEARCH_NOTE.md and profile_identifiability_results.json.")

    chapter(9,"Ultraviolet: reproducible array, unresolved common flow")
    p("The pinned UV source's partial fixed point and formal sign count reproduce. The new scalar evaluation has a maximum finite beta residual of 1.78e-15. The interpretation must remain the spectrum of an assembled 33-coordinate vector field: eight of the declared 41 entries are unavailable at the selected point. [U1; N-uv]")
    table(["Sector", "Critical exponent theta", "Count"], [
        ("Gravity", "3.96087030; 1.64358588", "2"),
        ("Scalar mass squared", "+2.00000000", "3"),
        ("Nonminimal xi", "+2.85543525", "3"),
        ("Gauge, Yukawa and quartic", "Zero at linear order", "12"),
        ("Literal wavefunction Z_i", "-0.07562458", "3"),
        ("Scalar sextics", "-2.00000000", "10"),
    ], [.44,.42,.14])
    p("The upstream prose swaps the mass and xi labels. Correcting the labels does not change the 8 positive / 12 zero / 13 negative count. The two reported cosmological numbers are also reconciled: the DEP repository branch defines lambda_N=2 Lambda_tilde, so -4.7975095 and -2.3987548 are the same point in different coordinates.")
    h("Concrete compatibility problems")
    table(["Issue found", "Why it matters"], [
        ("Different gravity backgrounds", "DEP gravity runs with current coordinates; the NP nonminimal block uses a different frozen background."),
        ("Four versus six scalars", "The gravity census has four scalars while the Hessian has four Higgs components plus two singlets."),
        ("Literal Z_i=0", "Zero kinetic normalizations are a singular chart for canonically propagating scalars."),
        ("Mass normalization", "NP lambda2 phi^2 matches m^2 phi^2/2 only with lambda2=m^2/2; wiring uses m^2."),
        ("Separate Litim conversion", "The wrapper reverses the c4=24 pi restoration while labeling its coordinate as G k^2."),
        ("Incomplete projections", "Curvature and six derivative/gauge-strength entries remain unavailable; the general portal basis is also broader."),
    ], [.32,.68])
    p("The Litim paper's equation-coordinate g*=1/64 restores to 3 pi/8 in its stated convention, rather than 1/(1536 pi). This is a coordinate conversion diagnosis, not a measured Newton-constant discrepancy. The DEP run does not call that wrapper. The mass-map and Litim findings were checked against the primary papers. [P1-P2]")
    source("The inherited full-flow guard still refuses a 41-dimensional fixed-point solve. All 44 upstream tests pass, which validates their checked identities but does not reconcile these conventions. The report does not infer a physical UV critical-surface dimension from the formal sign count.")

    chapter(10,"Ultraviolet: a new scalar projection and nonlinear tests")
    p("A new module projects the scalar Wetterich trace algebraically through field degree six. It uses four real Higgs components, two singlets, a regular normalized kinetic chart and the declared scalar potential. The finite polynomial resolvent avoids nested numerical differentiation. [N-uv]")
    eq("d_t U = tr[(I + U'')^-1] / (32 pi^2)\n(D+E)^-1 = sum_(n=0)^3 (-D^-1 E)^n D^-1\n           + O(field^8)")
    p("Every term in E has degree at least two; the displayed powers include all retained Taylor coefficients. 'Exact' refers to this specified scalar trace and truncation. It does not include additional fields, omitted higher operators, or a globally exact potential.")
    h("Feedback omitted by the assembled quartic block")
    eq("d beta_lambdaH / d c_H6 = -24/(32 pi^2)\n                         = -0.07599088773\nd beta_lambdaPhi / d c_Phi6 = -15/(32 pi^2)\n                           = -0.04749430483")
    p("The same singlet coefficient applies to E. The upstream quartic block has no sextic arguments, so these derivatives are zero there. The new module makes that feedback calculable within one scalar trace. It is not silently inserted into reproduction of the original partial array. A one-field resolvent, a separate tensor quartic calculation and a direct six-field Hessian provide independent checks.")
    p("The exact Gaussian sextic exponents are -2. Nested finite differences in the source produce a largest deviation of 0.00279397; the algebraic projection removes that numerical artifact.")
    table(["DEP gravity block only", "Four scalars", "Six scalars"], [
        ("Lambda_tilde*", "-2.3987547585", "-2.6261976695"),
        ("g_N*", "1.7621271177", "1.9858609514"),
        ("Gravity exponent pair", "3.960870; 1.643586", "3.959538; 1.623375"),
    ], [.38,.31,.31])
    p("Changing the scalar census moves the Newton coordinate by 12.70% within this gravity block. This is sensitivity to the declared model, not a completed six-scalar coupled theory. Background Newton scaling satisfies eta_N=-2; it must not be confused with the separate fluctuation eta_h. [P3; N-uv]")
    h("Zero linear exponent does not mean no running")
    p("The supplied one-loop matter subsystem has beta_g=b g^3/(16 pi^2). Hypercharge is marginally UV-repulsive; SU(2) and SU(3) are marginally UV-attractive. Positive isolated self-quartics grow toward the UV. Yukawa-only and portal-only probes generate other couplings. These bounded nonlinear checks resolve useful subsystem behavior while leaving the full coupled zero-exponent sector open.")

    chapter(11,"Operational bridge: an executed synthetic memory test")
    p("The sixth workstream now contains a concrete causal experiment on a specified computational mechanism. All its data are synthetic. Its protocol, seeds, sample sizes, scores and uncertainty procedure were written and hash-locked before generation; this is local prespecification, not external study registration. [N-memory]")
    p("For each of two sources, 400 independent training trials and 400 held-out trials contain 64 transitions. One balanced binary source stays in the same state with probability 0.8; the IID control uses 0.5. A Laplace-smoothed predictor is trained only on the training transitions and then frozen.")
    table(["Intervention", "What changes"], [
        ("Intact", "The decoder receives the trial's own previous state."),
        ("Reset", "It receives a null state returning the training marginal."),
        ("Cross-trial swap", "It receives another independent trial's previous state; the memory marginal is preserved exactly."),
        ("Relabel", "The state labels and decoder are conjugated together; every prediction remains identical."),
    ], [.25,.75])
    table(["Persistent-source intervention", "Brier-loss increase", "95% interval"], [
        ("Reset", "0.0919449", "[0.0887336, 0.0951169]"),
        ("Cross-trial swap", "0.1815062", "[0.1734237, 0.1897301]"),
        ("Relabel", "Exactly zero", "[0, 0]"),
    ], [.42,.24,.34])
    figure("agency/synthetic_memory_interventions.png", "Synthetic held-out intervention effects. The IID source's effects are near zero, and the exact relabel control is observationally identical. Lower prediction loss is better.",max_height=165)
    p("The 4,000 bootstrap replicates preserve complete reciprocal donor-linked pairs of trials, retaining both serial dependence and swap-induced dependence. Intervals are conditional on the trained predictor and stipulated source. Twenty-one integrity checks pass; the IID equivalence controls pass. The expected mechanism is confirmed: useful temporal memory supports prediction, while unrelated memory can create unjustified confidence.")
    source("This test supplies no action/reward system, phenomenal observation or physical scalar measurement. A consciousness or field claim needs an explicit observable map and a prespecified prediction different from a functional memory/report model. Renaming an internal state cannot supply that discrimination.")

    chapter(12,"How the six routes now connect")
    p("The archive already articulates the need for compatible cross-scale maps and interventions. This continuation implements specific pieces of that principle. The workstreams can constrain each other only when they share a consistent action, parameter point, state and measurement map. [A1, pp.6457-6468]")
    table(["Connection", "What is available", "What must be supplied"], [
        ("Action to thermal", "One portal normalization and one benchmark mass matrix.", "Quartics, complete reaction inventory and physical initial history."),
        ("Action to detector", "Point-probe Higgs matching and composite-operator noise conventions.", "Local bath state, composite response and moving finite-time filter."),
        ("Spectral action to gauge observables", "Exact profile-family coefficients and sensitivity.", "Physical profile/normalization selection, electroweak matching and running."),
        ("UV to low energy", "A bounded scalar projection and explicit coordinate audit.", "Common regulator/background, full beta vector and compatible IR trajectory."),
        ("Operational variables to interpretation", "A causal-memory experiment with intervention controls.", "A justified measurement map and genuinely different predictions for the proposed interpretation."),
    ], [.25,.34,.41])
    h("The next scientific decisions are now concrete")
    p("First fix the compatible operator basis and renormalization conventions before joining the UV and low-energy claims. Then establish a physical population history and QCD-matched interaction response; the measured preparation sensitivity sets a quantitative target. For laboratory inference, obtain independent contrast and detector-statistics calibration before assigning an attenuation to a new field.")
    p("For electromagnetic normalization, select the profile and common normalization by a physical principle or independently justified data, and propagate that choice through the full electroweak calculation. For the operational route, specify the actual observable and competing models before extending memory performance to agency, experience or a field interpretation.")
    h("Claim discipline is part of the executable record")
    p("The machine-readable contract uses null for unknown inputs. The UV completion flag remains false, the measurement result has no new-field constraint, and the memory experiment is labeled synthetic throughout. Numerical agreement certifies specified computations; it does not turn assumptions into empirical facts. The separate internal calculation reviews are not external peer review or independent experimental replication.")
    p("This package is ready for technical inspection and rerunning. It makes successful calculations usable, errors correctable and remaining dependencies reviewable. Completion requires new matched derivations or observations at the specific interfaces listed above.")

    chapter(13,"Reproduction and source map")
    p("The complete code bundle is self-contained for the delivered numerical runs: pinned source files, collision banks, public count data, scripts, full notes, JSON/CSV outputs and hashes are included. The large uploaded source PDF is identified by hash and physical page numbers rather than duplicated.")
    eq("python reproduce.py\n# Verify delivered file hashes without modifying outputs.\n\npython reproduce.py --rerun\n# Rerun common, measurement, spectral, UV and memory work.\n\npython reproduce.py --rerun --include-thermal\n# Also rerun the frozen-bank thermal calculation.")
    p("Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, pandas 2.2.3, openpyxl 3.1.5 and matplotlib 3.10.8 were used. Report creation uses reportlab 4.4.9. Exact environment versions and every delivered file hash are recorded. Re-execution changes generated timestamps, and floating-point last digits may vary with versions.")
    table(["ID", "Source and role"], [
        ("A1", "User-supplied Baird expanded archive, public edition 20 October 2026, 9,252 pages. Relevant sections and physical page numbers are recorded in sources/source_catalog.json."),
        ("T1", "Cbaird26/mqgt-scf-continued, commit 48f9dcbd34e7cfb86504167a0483f732a5dd5e8e. Frozen free-bath checkpoint of 21 October."),
        ("U1", "Cbaird26/uv-reconstruction-frg, commit 0a644a41eb947509280cbd648996d98bad54bdc5. Formal partial flow and source conventions."),
        ("D1", "Pedalino et al., public dataset/code. DOI 10.5281/zenodo.17502163. CC BY 4.0. Original zip preserved; new reanalysis is separate."),
        ("D2", "Pedalino et al., nanoparticle matter-wave interferometry. DOI 10.1038/s41586-025-09917-9; author preprint arXiv:2507.21211."),
        ("P1", "Litim, On fixed points of quantum gravity. arXiv:hep-th/0606044, equations 4-6 and 11."),
        ("P2", "Narain and Percacci, Renormalization Group Flow in Scalar-Tensor Theories. I. arXiv:0911.0386, equations 1, 25, 26."),
        ("P3", "Dona, Eichhorn and Percacci, Matter matters in asymptotically safe quantum gravity. arXiv:1311.2898."),
        ("P4-P5", "Borsanyi et al., QCD thermodynamics: arXiv:1309.5258 and arXiv:1007.2580. See thermal EOS provenance and its explicit scope."),
    ], [.12,.88])
    source("Archive SHA-256: 4b52a5fb57716168d354b5c3dcb4bbf2ca4c0fe6744733b6ca0d3b3eae48f921. Public dataset MD5: 7917961b27676f4e9df3af6d3b01c374. Synthetic protocol SHA-256: 77061f72bdc30a11f29123166ded858336c358e84f8ac19b096afac17e897155.")
    source("[N-common], [N-thermal], [N-EOS], [N-measurement], [N-electromagnetic], [N-uv] and [N-memory] are the corresponding result JSON files listed in sources/source_catalog.json. Full source URLs, immutable code links and attribution are in that catalog and the per-workstream notes. No cited source repository or original uploaded document was modified.")

    doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=46,leftMargin=46,
                          topMargin=51,bottomMargin=48,title="Theory of Everything Research Continuation - 21 October 2026",
                          author="Research continuation prepared with ChatGPT",subject="Conditional computations and source audit for the MQGT-SCF program")
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(OUT)


if __name__=="__main__":
    main()
