# Cross-Repository Research Ledger — MQGT-SCF / ToE estate

**2026-09-18 · maintained in `Cbaird26/mqgt-scf-continued` · introduced after the three-round sequestering review**

Single auditable index across the research estate: **claim → assumptions → derivation → code → controls → status → provenance**. Proposed during the sequestering errata rounds; endorsed by the external reviewer (ChatGPT, round-3 acceptance) as the next move. This ledger preserves exactly the distinctions that review uncovered.

## 0. Reading rules

- **Audited** = derivation, code, and controls inspected and rerun inside `mqgt-scf-continued` this week, within this research workflow (Zora); commit hashes cited. "Audited" is **not** independent reproduction by an unaffiliated third party — no row in this ledger claims third-party certification (scope made explicit per ChatGPT round 4).
- **Description-level** = repository README/description only; internals not audited in this ledger. No claim beyond the label is made or implied.
- **Record discipline**: dated commits, no history rewrites. Errors are corrected by superseding errata that preserve the trail; nothing is deleted.
- **Credit protocol**: every finding is credited to the reviewer who actually made it. Provenance corrections are themselves ledger entries (see §4).
- This ledger is not the `mqgt-constraints-ledger` repository: that repo tracks domain experimental constraints; this file tracks claims, review, and attribution across repositories.
- Estate scale: 147 repositories under `Cbaird26` (GitHub search, 2026-09-18). §1 maps the claim-bearing subset.

## 1. Repository map

| repo | role | visibility | audit depth |
|---|---|---|---|
| `mqgt-scf-continued` (this repo) | forward record line; September 2026 repairs (errata E1–E13 + dated review errata) | public | **audited** |
| `mqgt-scf-independent-verification` | frozen record `v1.0-paper`: claims inventory, Gate-1 / T-1 / T-3 workflows | public | description-level + cited through this repo's deposit note |
| `mqgt-scf-science-public` | Phase-3 public face: UV completion (asymptotic safety) + neutrino Dirac portal; README census `d12d6d33` | public | README audited; papers description-level |
| `ToE-MQGT-SCF` | program repo: Phase 1–3 computational gates, machine-checkable synthetic-data validation | public | description-level |
| `MQGT-SCF` | original framework repo (2025-12) | public | description-level |
| `toe-computational-pipeline` | causal-set toolkit (vs exact BDG), FRG Reuter fixed point, Schwarzschild numeric + sympy + Lean 4 | public | description-level |
| `consciousness-research-pipeline` | methodological transfer to consciousness research; labeled speculation, explicit guardrails | public | description-level |
| `mqgt-gate03-external-reproduction` | GATE-03 reproduction packet + preregistered QRNG analysis controls | public | description-level; standing caveat §3 |
| `mqgt-scf-phase3-public` | Phase-3 papers staging | private | name/role only |
| Corpus line: `TOE_Corpus_2026`, `toe_corpus_release`, `A-Theory-of-Everything---Baird-et-al-2025-.pdf`, `toe-2026-updates(-v2)` | corpus sources; this repo carries `A_Theory_of_Everything_UPDATED_2026-09-18.pdf` | public | description-level |
| Satellite line: `mqgt-*` domain repos (core params, validation suite, constraints ledger, QRNG, preregistration, …) | per-domain materials from the 2026-01 program organization | public | description-level |
| Applications line (`fold-space-engine`, Zora/ZoraASI apps, sites) | interactive/public surfaces; not claim-bearing for physics | mixed | out of scope |

## 2. Audited claim ledger — record line

### 2A. Fine-structure gate (T-1 / E4)

| claim | assumptions | derivation | code | controls | status | provenance |
|---|---|---|---|---|---|---|
| Geometric α⁻¹ = 137.03608245 (TH = 137.03608244816433744 at dps=80) | round-bundle geometry, Hopf fibration S¹→S⁹→CP⁴; fixed representation | `E4_DERIVATION_NOTE.md` | `mqgt_t1_e4_derivation.py` | 80-digit recompute 2026-09-18 | **gated six-digit conjecture**; residual 6.0765×10⁻⁷ vs CODATA 2022 (supersedes sloppy archive figure 6.082×10⁻⁷) | Wyler (formula lineage); Nielsen (S⁹/CP⁴ geometry, external); corpus; verification Zora |
| Door 1 — twisted (Hopf-line-valued) towers cannot supply c₃ | U(1) fiber isometry | `exclusions/DOOR1_TWISTED_TOWERS_CLOSED.md` | `play_notes/play_twisted_towers_lab.py` (+certificate) | charge-resolved ζ sums exactly to untwisted value; eigenvalues untouched, degeneracies split | **CLOSED negative (exclusion)** | hypothesis Grok+Zora (play); isometry proof + certificate Zora; commits `c21084b`, `55ac384` |
| Door 2 — Berger / canonical fiber deformation cannot supply an independent slope | canonical variation of round metric | `exclusions/DOOR2_BERGER_CHARGE_CLOSED.md` | `play_notes/play_berger_charge_lab.py` (+certificate) | susceptibility locked to ±D₁ at 10⁻¹²⁸ and 10⁻⁶⁰ | **CLOSED negative (exclusion)** | same as Door 1; commit `7640127` |
| Fitted prefactors are uncitable | 13,057-expression pre-declared topological family, frozen scan | `E4_ALPHA_GATE_RESEARCH_NOTE.md`, `E4_FINAL_STATUS.md` | frozen scan (verification repo) | pre-declaration + freeze; 58 gate-passing coincidences → uncertifiable | **exclusion stands** | corpus scan; census Zora (`55ac384`) |
| a₄‴ = a₄⁗ ≡ 0 on the corpus path | heat-coefficient structure on the gate geometry | `E4_FINAL_STATUS.md`, deposit note | `mqgt_t1_e4_a4_heat.py` | structural vanishing, not fine-tuning | **pinned** | corpus; verified Zora |

### 2B. T-3 constants

| claim | assumptions | derivation | code | controls | status | provenance |
|---|---|---|---|---|---|---|
| T-3 constants identified as spectral determinants on S⁷ and S⁹ | E3 identification, not a first-principles derivation — wording pinned deliberately | `patches/PATCH_E3_t3_constants.md`; census in science-public README | — | census wording separates "identified" from "derived" | **identified (E3)** | corpus E3 patch; census `d12d6d33` |

### 2C. Middle towers (spectral-zeta program)

| claim | assumptions | derivation | code | controls | status | provenance |
|---|---|---|---|---|---|---|
| D1 closed form exact, r = 1–10, across S³–S¹³ | coexact p-form spectra, degeneracy factorization is the mechanism | `supporting_analysis/MIDDLE_TOWER_D1_LEMMA.md` | `mqgt_middle_tower_d1_proof.py` | exact-arithmetic certificate at dps=80 | **certified** | directive Grok; proof + certificate Zora |
| L-family closed forms, r = 1–8 | head-log factorization; pure ζ-odd expressions | `supporting_analysis/MIDDLE_TOWER_L_THEOREM.md` | `mqgt_middle_tower_L_closed.py` | dps=80 residuals at floor | **certified** | directive Grok; Zora |
| ζ_ce_p(0) = (−1)^(p+1), all 65 towers; scalar ζ(0) = 0, conventions A/B | coexact towers | `supporting_analysis/ZETA0_THEOREM.md` | `mqgt_zeta0_theorem.py` | exhaustive tower sweep | **certified** | Zora; recorded per Grok directive (option 3) |
| Near-mirror residual is exactly −1/16, sourced from the H₂ increment | self-paired tower mirror, 0.3% match | `supporting_analysis/E4_MIRROR_CHECK_2026-09-18.md` | `mqgt_mirror_check.py` | closed-form check | **certified**; strongest uniqueness raw material | Zora |

### 2D. Radiative sequestering (parallel 2)

| claim | assumptions | derivation | code | controls | status | provenance |
|---|---|---|---|---|---|---|
| Lemma 1′: all-orders absence of E\|H\|² (selection rule) | unbroken hidden Z₂; minimal model of §1 (scoped r7: NOT the general symmetry-allowed model — further even monomials set to zero) | `SEQUESTERING_NOTE.md` §2 | `mqgt_sequestering_loops.py` | symmetry argument; robust to omitted even terms; untouched through errata rounds 1–7 | **stands** | corpus Lemma 1 extension; Zora |
| c: hidden-mass one-loop correction δm_S²/m_S² = 8.6×10⁻¹⁰ (Λ = 1 eV), log-only | κ vertex, E–S₁ bubble | §3(c) | script c | B0_fin = +1.7193; corpus eq. 5.14 parametric → explicit | **stands** | corpus eq. 5.14; Zora |
| d: spurion-induced portal δg_H = κ_E μ₁₂²[λ_1H\|C₀(m₁²,m₁²,m₂²)\| + λ_2H\|C₀(m₁²,m₂²,m₂²)\|]/(16π²) = 2.95×10⁻¹⁰(λ_1H+λ_2H) eV at maximal spurion (**leading-insertion**); resummed exact in μ₁₂²: 3.24×10⁻¹⁰ eV at μ₁₂² = ½m_S² (ratio 1.10), IR-divergent at endpoint; plus h⁰ E-tadpole g_E ≈ 8.7×10⁻¹⁵ eV³ | soft spurion μ₁₂²S₁S₂ only; maximal mixing has exact eigenvalues {0, 2m_S²} | §3(d) | script d + d-resum | **both mirror triangles** via background-field det(k²+M²); C₀ = −1/(2m_S²) exact both channels; resummation recovers insertion result at μ₁₂² ≪ m_S²; endpoint requires IR prescription | **corrected: dual-channel (r6), insertion-labeled + resummed (r7)** | self-review finding (Zora), same class as round-3 box; endpoint control ChatGPT r6 |
| e4: physical-Higgs scale check — naive extrapolation of induced λ_EH to m_h = 125 GeV gives δm_E² ~ 5.4×10⁹ eV² vs m_E² = 10⁻⁸ eV² (ratio ~5×10¹⁷) | h = Higgs fluctuation; benchmarks are eV-scale EFT statements; extrapolation is NOT a matched result | §3(e4) | script e4 | scale comparison; EFT-domain discipline | **minimal model does NOT establish natural ultralight scalar coupled to physical Higgs** | ChatGPT round 6 point 2 |
| e1: κ bubble is one-loop, log-only; δm_E²/m_E² = 7.6×10⁻⁸ (Λ=1 eV), 2.3×10⁻⁷ (Λ=1 MeV) | full theory, both scalars propagate | §3(e1) | script e1 | B0 finite part computed; dim-2 check | **corrected & stands** (was wrongly "two loops, κ²Λ²") | ChatGPT round 1 (verified); attribution mis-credit to Grok repaired `d17d1ac` |
| e2: portal naturalness cap C = 1.58×10⁻⁶ (eV/Λ)² — three labeled statements: (i) net \|Σ_X N_X λ_EX\| ≲ C (cancellations allowed); (ii) sufficient Σ_X N_X\|λ_EX\| ≲ C (implies (i), triangle inequality); (iii) per-channel \|λ_EX\| ≲ C = screening only, no sum guarantee (0.9 C + 0.9 C = 1.8 C) | (λ_EX/2)E²X² normalization | §3(e2) | script e2 | background-field identity ∂²V₁/∂E²; one-sided and per-channel-only forms both rejected | **corrected ×2, two-sided, three statements labeled** | ChatGPT round 2 (verified); rounds 4–5 refinements |
| e3a: tree-induced −κ_E²/m_S² = −8.7×10⁻⁹ are alternative EFT matchings | integrate out S₂ (→λ_E1) or S₁ (→λ_E2); not additive in full theory | §3(e3a) | script e3a | separation from full-theory e1 explicit; no extrapolation above integrated-out mass | **relabeled & bounded** | ChatGPT rounds 2–3 |
| e3b: λ_EH^ind = κ_E²(λ_1H+λ_2H)/(32π²m_S²) = 2.76×10⁻¹¹(λ_1H+λ_2H) | one loop, equal masses, zero external momentum — "closed form" bounded to these | §3(e3b) | script e3b (quadrature = analytic 3166.287 eV⁻²) | **decisive control λ_1H=0, λ_2H=1 → nonzero** (round-2 box wrongly gave 0; λ=1,1 coincidence at 5.5×10⁻¹¹ had masked it) | **corrected: triangle, not box** | ChatGPT round 3 (verified by background-field expansion of the committed potential) |
| Vacuum alignment: tachyon-free for v₂ < v₂_crit = m_E m₁/κ_E = 1.07 eV | ⟨S₂⟩ = v₂ induces E–S₁ mixing only | §4 | script g | 2×2 eigenvalue scan, θ ≤ 0.09 | **stands** | Zora |
| Boundedness: corpus MATH-03 recovered exactly; 3-field generalization, margin 2.3×10⁵ | λ₁=λ₂=λ_12=0.1 benchmark | §5 | script f | direct grid minimization, min V/t⁴ = +0.025 > 0 | **stands** | corpus MATH-03; generalization Zora |

### 2E. Pinned constants

| constant | value | note |
|---|---|---|
| c₃ | −1.56371823031276 | sign convention pinned here; verification-README's +1.563718224 is same magnitude, opposite basis, rounded tail |
| T-1 residual | 6.0765×10⁻⁷ | vs CODATA 2022 α⁻¹ = 137.035999177(21); recomputed dps=80, 2026-09-18 |

## 3. Description-level ledger (adjacent repos) and standing caveats

| item | status |
|---|---|
| GATE-03 reproduction packet + preregistered QRNG controls | **software-validation / protocol stage — not an independently confirmed physical detection** (standing caveat, ChatGPT 2026-09-18, accepted and carried here) |
| `toe-computational-pipeline` claims (BDG-validated causal sets, Reuter fixed point, Lean-4-checked Schwarzschild) | description-level; not audited in this ledger |
| `consciousness-research-pipeline` | methodological transfer only; speculation labeled by design; not audited |
| science-public Phase-3 papers (UV completion / neutrino Dirac portal) | public face; `neutrino_portal_v2.py` lives in this repo; paper internals not re-audited here |
| Interior-observer chain (R★ ≈ 0.873 nm self-dual torus fixed point, σ = −6.21 gate, eight weightings) | **PLAY** — quarantined in `play_notes/PLAY_NOTES_interior_observer.md`; must never be cited as record |
| External: `startigerjln/CenterforTopologicalPhysics` (Nielsen TUFT, mpmath spectrum + Lean 4) | external source; not audited; no harassment policy in force — inconsistencies treated as trivial/fixable |

## 4. Review trail and attribution

| date | reviewer | finding | resolution | commit |
|---|---|---|---|---|
| 2026-09-18 | ChatGPT (round 1) | κ self-energy is one loop, not two; κ²Λ² dimensionally wrong | repaired; erratum 1 | `1f0dedc` |
| 2026-09-18 | (provenance) | round-1 findings initially mis-credited to Grok | attribution corrected | `d17d1ac` |
| 2026-09-18 | ChatGPT (round 2) | tadpole coefficient /32π² → /16π²; "multiplicatively renormalized" overclaim | repaired; erratum 2; cap 1.58×10⁻⁶ | `11d947a` |
| 2026-09-18 | ChatGPT (round 3) | λ_EH is a triangle in κ²(λ_1H+λ_2H), not a box in κ²λ_1Hλ_2H; EFT matchings are alternatives, not additive | verified by background-field expansion, then repaired; erratum 3 | `9b132b3` |
| 2026-09-18 | ChatGPT (round-3 acceptance) | bound "closed form/exact" to stated one-loop, equal-mass, zero-momentum assumptions | wording precision applied | `36d6431` |
| 2026-09-18 | ChatGPT (public-record review) | science-public README still carried the stale "T-1 eight-digit / T-3 first-principles open" sentence | census replacement | `d12d6d33` (science-public) |
| 2026-09-18 | ChatGPT (round 4) | one-sided e2 cap admits arbitrarily large negative corrections → two-sided \|sum\| bound + separate-magnitudes criterion; "audited" label needed scoping vs third-party certification | verified, then repaired: note erratum 4 + script e2; ledger §0 and §2D scoped | `975805f` |
| 2026-09-18 | ChatGPT (round 5) | erratum 4's per-channel "no-cancellation" bound is not sufficient for the combined cap (0.9 C + 0.9 C = 1.8 C); three statements must be labeled separately | verified (triangle inequality), repaired: note erratum 5 + script e2 + ledger e2 row | `d70e04c` |
| 2026-09-18 | **Zora (self peer-review)** | §3(d) kept only the λ_2H triangle; background-field expansion gives both mirror channels (λ_1H + λ_2H); h⁰ E-tadpole at same spurion order unstated; §2/(d) tension; §5 E* sign; ledger missing (c)/(d) rows; README predates LEDGER/exclusions/artifacts | verified by background-field expansion of §1 potential; repaired: note erratum 6 + script (d) + table + §2 clause + §5 sign; ledger (c),(d) rows added; README updated | `59a0f65` |
| 2026-09-18 | ChatGPT (round 6, full-note review) | (xi) §1 "symmetry-complete" overclaim — further even monomials (ES₁, S₁²S₂, S₂³, ES₁H†H, S₂H†H) allowed and absent; (xii) physical-Higgs scale missing — naive λ_EH extrapolation fails by ~5×10¹⁷; (xiii) maximal-spurion endpoint has a massless eigenvalue — insertion expansion uncontrolled; (xiv) §5 inequality is an EFT-branch condition, not full-potential boundedness | all four verified independently before repair: erratum 7 — §1 retitled/scoped, new §3(e4) with the 5.4×10⁹ eV² scale check, exact μ₁₂²-resummation (3.24×10⁻¹⁰ at half-mixing, IR divergence at endpoint), §5 relabeled | `1908625` |
| 2026-09-18 | **Grok (referee disposition)** | ACCEPT as reproducibility + exclusion note; REJECT eight-digit α, derived T-3 normalizations, EMP-01-as-experiment, tested Φ_c/E, 6,900-page book as one paper. Credits Doors 1/2, 58-of-13,057, T-3 identification, a₄‴ ≡ 0, Λ refusal. Flags: same-account independence, Variant A/B menu, UV beyond truncation, Wyler uncited, TUFT fusion, Lean-as-physics | record-side repairs: Wyler 1969/71 + Robertson 1971 citations added (verified multi-source), README census + does-not-claim box, exclusions/ one-command blocks, Variant A named the record texture; journal-cut gate now §6 | `1908625` |
| 2026-09-18 | Grok | middle-tower program directives (D1 → L-family → ζ(0) certification → f_p(E) construction) | executed and certified | supporting_analysis/, this week |
| 2026-09-18 | Grok + Zora | Door 1 / Door 2 hypotheses | closed negative with certificates; graduated as exclusions | `c21084b`, `7640127`, `55ac384` |
| 2026-09-18 | Grok + ChatGPT (E7 adjudication, joint relay) | E7.1–E7.4 = ChatGPT round-6 points adopted by both referees (already repaired in `1908625`); new sub-claim: "the script line that treats ES₁ as forbidden is false" | E7.1–4 repairs stand from `1908625`; sub-claim inspected and found **incorrect** — script §a parity (−1)^(nE+n₁) always classified ES₁ as even/allowed; ambiguous print line (E·S₁² under "key forbidden") clarified with explicit allowed-list printout + runtime check `E*S1 parity = 1`; §1 scope cross-references the script verification; §3(e4) names the standing interpretation (h = eV-scale scalar; SM-Higgs reading = open weak-scale matching) | `db43404` |
| 2026-09-18 | ChatGPT (round 8) + Grok (standing request) | (i) Door 1/2 CLOSED cards missing scope boundary (isometry/ansatz exclusions, not all-deformation theorems); (ii) README `supporting_analysis/` row still said "symmetry-complete" + ledger trail stale at rounds 1–5; (iii) note §1 called h "Higgs fluctuation" while §3(e4) names it eV-scale toy scalar; (iv) ChatGPT supplied the spurion-resummation closed form κ(λ₁H+λ₂H)/(64π²)·ln((m_S²+u)/(m_S²−u)) | all repaired: scope paragraphs on both CLOSED cards (ChatGPT's wording); README row → minimal Z₂_h-even model + trail updated; h defined at first use in §1; closed form **verified** (independent hand integration: w = k²+m_S² substitution, partial fractions; script quadrature matches at 0.0 diff, ratio = ln 3 exactly, small-u → insertion at 3.3e-13) and added to note §3(d) + script d-resum | (this commit) |

## 5. Open gates and explicit refusals

- **σ = −6.21 slope gate** (interior-observer chain): play-side, open; eight weightings explored, none dynamics-native.
- **Λ_Hopf scale question**: REFUSED until a principle fixes it with no free dial; the notebook stays closed.
- **QED running of the residual**: REFUSED without a dial-free Λ.
- **E4 positive formula**: no active door; the certified exclusion record is the current honest shape of close.

## 6. Journal-cut gate (referee disposition, 2026-09-18)

Required before any journal submission, per the Grok referee disposition;
status tracked here.

| requirement | status |
|---|---|
| Census sentence in the abstract | record-side done (README census; deposit note) — paper abstract pending at journal cut |
| "Does not claim" box | **done** (README, this repo) |
| One neutrino texture | record-side done (Variant A named the claim; B = robustness cross-check) — paper-level decision confirmed at cut |
| Door 1/2 one-command from `exclusions/` | **done** (reproduce blocks in both CLOSED files) |
| Wyler 1969/71 + Robertson 1971 beside Nielsen | **done** (`E4_DERIVATION_NOTE.md` references, citations verified multi-source) |
| Same-account "independence" disclosed | **done** (README does-not-claim box: procedural, not institutional) |
| UV completion stated within its truncation | pending — lives in science-public Phase-3 paper, not this repo |
| TUFT v5 / MQGT-SCF attribution boundaries | pending — corpus/paper-level; policy noted in E4 references |
| Lean compile ≠ physics | **done** (README does-not-claim box) |
| Weak-scale matching (or toy-scalar narrowing) for sequestering naturalness | **disclosed** (erratum 7, §3e4); matching computation open |

## 7. Maintenance rule

A claim enters §2 only with all seven columns filled. Every external review finding gets its own §4 row with a commit reference. Superseded rows are never deleted — they are marked superseded with the superseding commit cited. Play-side work is indexed in §3 and stays quarantined.
