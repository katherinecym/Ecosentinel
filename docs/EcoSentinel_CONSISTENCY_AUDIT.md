# EcoSentinel — Cross-Artifact Consistency Audit
**Scope:** `submission/EcoSentinel_3Min_Pitch_Deck.html` × `submission/EcoSentinel_DipteraCAST_Enhanced.ipynb` × `submission/EcoSentinel_GNW_Horizon_Edition.html`
**Date:** 2026-10-05 · **Method:** every number traced to its source table in `Project_A_EcoSentinel_DipteraCAST/outputs/tables/`

---

## 0. What I verified as GROUND TRUTH (from source tables, not prose)

| Quantity | Authoritative value | Source file |
|---|---|---|
| Stations / cities | 85 / 5 (Antwerp, Athens, Coimbra, Milan, Toulouse) | `data/harmonized/OneAquaHealth_85Stations_DeltaStacking_Dataset.csv` (49 cols) |
| DML confounder set | **10** variables (imperviousness_500m, tree_cover_500m, temp_water, ph, wetted_width_m, mean_depth_m, precip_7d_sum, gdd_7d, temp_sd_7d, consecutive_dry_days) | `Project_A_Phase2_DML_Assumption_Dependent_ATE.csv` → `confounders` column |
| H1 DO causal effect | β = −0.2818 pp/mg/L, city-cluster **p = 0.00451 (two-sided) / 0.00225 (one-sided)**, 95% CI [−0.4177, −0.1460] | same |
| H2 association | high−low flow prevalence diff = **−0.3723**, Mann-Whitney one-sided **p = 0.00285**, permutation p = 0.00370 | `Project_A_H1_H2_H3_FormalTests.csv` |
| H2 threshold at 0.30 m/s | local-linear contrast **p = 0.8365 (null)** — *no threshold established* | same |
| H2 DML causal ATE (flow) | β = −0.3512 pp per +0.1 m/s, **p = 0.3623 (n.s.)** | Phase2 CSV |
| H3 topology | GAT wins 4/5 cities, Toulouse −0.3755; mean paired Δ(PR-AUC) **−0.0657**, Wilcoxon **p = 0.3125 (fail to reject)** | same |
| ODE (two different columns!) | cumulative 30-day emergence **372.255 → 308.725 (−17.07%)**; **day-30 adult standing index 123.066 → 99.342** | `Project_A_Phase4_ODE_Normalized_Scenario_Summary.csv` |
| PAR basin totals | pop **288,152**; pop65+ **62,563**; baseline PAR **205,105.4**; NbS PAR **107,314.8**; ΔPAR **97,790.6 (−47.68%)**; 65+ ΔPAR **21,569.4**; ΔPAR/pop **33.94%** | `Project_A_Phase5_City_PAR_Summary.csv` |
| Clipping | **8/85** stations at P=1.0 → **17.01%** of baseline PAR; no calibration test | Phase5 / dashboard `clip` flags |
| Model leaderboard | best *classification* = CatBoost PR-AUC **0.9511**, ROC 0.9219; best *regression* = Super Learner R² **0.8855**, RMSE 4.1515 | `Project_A_FiveModel_Stacking_NestedLOCO.csv` |
| Health economics | avoided infections 1,466.9; DALYs 51.2; acute cost €553,614/yr; +rehab €704,738; CapEx €1,275,000 (flat €255k/city) | `Project_A_Module2_DALY_Health_Economics.csv` |
| Per-city ΔPAR% | 52.03 / 54.45 / 46.88 / 47.03 / 37.14 | Phase5 |

**Good news first:** the dashboard's embedded `EXPLORE_DATA` (85 stations) reproduces the notebook **exactly** — I re-summed it: 205,105.4 / 107,314.8 / 97,790.6 / 21,569.4 / 8 clipped / 17.01%. Its `HEALTH_DATA` also matches. So the *data layer* of the dashboard is sound. The problems below are all in the **label / hardcoded-text layer**.

---

## 1. 🔴 Blocking defects (fix before submitting)

### B1. The dashboard link in the deck is broken
- Deck slide 4 → `href="EcoSentinel_Interactive_Dashboard.html"`
- That file **does not exist in `submission/`** (and is not the latest dashboard).
- **Fix:** point to `EcoSentinel_GNW_Horizon_Edition.html`. *(Done in updated deck.)*

### B2. The deck's speaker-notes drawer describes a DIFFERENT project
Press `N` on the deck and you get a script about *"urban wetlands, rain gardens, Streeter-Phelps, trout, bird calls, River Passport, civic rewards, -11.2% to -25.3% ΔP"*. None of it appears on any slide, and none of it matches the notebook. It reads like an earlier, entirely different pitch (a "River Nature Diary" product) that was never deleted.
- A judge who opens the notes sees the deck contradict itself.
- **Fix:** all five notes rewritten to match the slides and the 3-minute script. *(Done.)*

### B3. Dashboard KPI is hardcoded wrong: `ΔPAR Total: -45.9%`
In `updateKPICards()`: `let pctChange = '-45.9%'` and the `ALL` branch never overwrites it. True basin value is **−47.68%**. The dashboard's *own caveat panel* on the same page says "−47.7% of the 205,105.4 baseline" — so the page contradicts itself.
- **Fix:** `-47.7%`. *(Done.)*

### B4. Dashboard model-panel sentence contradicts itself
> "Super Learner attains highest PR-AUC (**0.943**), followed by CatBoost (**0.951**)"

0.943 < 0.951. The notebook flags this exact trap. Correct statement: *CatBoost leads classification (PR-AUC 0.951); the Super Learner leads regression (R² 0.886).*
- **Fix:** sentence corrected. *(Done.)*

### B5. Dashboard leaks a non-pilot city: **Ghent**
Station inspector default = `Ghent Basin • Reach 1,200m`; whisper board = `Marta K. · Ghent Reach`. Ghent is not one of the five pilot cities and appears in no data file.
- **Fix:** replaced with real pilot context. *(Done.)*

### B6. Deck claims **"25 climate confounders"** — actual is **10**
Proven from the `confounders` column of the DML table. *(Fixed to 10.)*

---

## 2. 🟠 Number/framing mismatches

### M1. The ODE number is **not** a conflict — it's an unlabelled column switch
- Notebook: 372.25 → 308.73 = **cumulative 30-day emergence** (−17.07%)
- Dashboard card: 123.1 → 99.3 adults/m² = **day-30 adult standing index**

Both are literally in the same CSV row. The danger is the master storyboard (Scene 4) narrates *"drops visibly from 372.3 to 308.7"* while the dashboard chart on screen plots the 123.1→99.3 series. Judges will read that as an error.
**Recommendation:** narrate the visible series in the demo, and say the metric name out loud. Suggested line: *"the day-30 adult index falls from 123 to 99, and cumulative emergence over the 30 days is down 17.07% — 372.3 to 308.7."* The video script below does this.

### M2. Dashboard invents a "**−60.8% Vector reduction**"
From a toy formula: `currentMozPct = 46 − 28×deploymentFrac`, so full deployment → 18% vs a "baseline 46%". Neither 46% nor 60.8% exists in any project table. It sits one card away from the audited −17.07%.
**Recommendation:** either delete, or relabel as *"illustrative index, not the Phase-4 estimate"*.

### M3. Flow threshold is stated three different ways
| Where | Value |
|---|---|
| Dashboard layer legend + provenance | **0.20 m/s** ("Critical Stagnant < 0.20 m/s", "v_crit = 0.20 m/s") |
| Dashboard tooltips + cockpit | **0.30 m/s** |
| Deck slides 1–3 | **0.30 m/s** |
| Notebook | 0.30 m/s is a *pre-specified operational marker*; the threshold test is **NULL (p = 0.84)** |

So the dashboard contradicts itself, and all three artifacts state as fact a threshold the notebook explicitly could not establish.
**Recommendation:** use **0.35 m/s** as the *scenario floor* (the value actually applied in Phase 5), and always add "not an established threshold (p = 0.84)".

### M4. Hypoxia threshold stated three ways
Deck "DO < 2.5–3.0"; dashboard "below 4.0 mg/L"; ODE baseline DO = 2.0. Observed DO range is 2.09–7.19, mean 4.76.
**Recommendation:** one sentence everywhere: *"in our reaches DO runs 2.1–7.2 mg/L (mean 4.8); the polluted scenario sits at 2.0."*

### M5. NbS targets inconsistent
Deck slide 1 says "restore DO >5.0 mg/L + baseflow >0.3 m/s"; slide 3 and Phase 5 use **DO ≥ 6.5, flow ≥ 0.35, BOD₅ ≤ 1.8**. Dashboard "Water Cleanliness" card shows **BOD 2.0**.
**Fix:** standardise on 6.5 / 0.35 / 1.8. *(Deck fixed; dashboard BOD card flagged.)*

### M6. Model headline mislabelled in the deck
"0.922 Best LOCO ROC-AUC (R²=0.886)" silently mixes CatBoost's ROC-AUC with the Super Learner's R². Split them.

### M7. H2 p-value quoted two ways inside the deck
Slide 2 "Obs Diff = −0.372 (p = 0.004)" (permutation p) vs slide 3 "p = 0.003" (Mann-Whitney p). Both are in the table, but the deck never says they are different tests.
**Fix:** quote **Mann-Whitney p = 0.0029** as the headline and note the permutation p = 0.0037 as a robustness check.

### M8. "Seniors Protected / Neighbours Shielded" read as headcounts
Deck: *"1,859 Seniors (Age 65+) Protected"*. Dashboard: *"Neighbours Shielded — 97,791, 21,569 aged 65+ protected"*. Both are **PAR units (risk-weighted exposure)**, and the notebook's #1 mandatory caveat is *"'97,791 people protected' is wrong."* The caveat panels say the right thing while the headline cards say the wrong thing.

### M9. Deck's ODE formula ≠ the code
Deck prints `dL/dt = r_L·E − μ_L·L(1+L/K)` (logistic). Code/notebook: `dL/dt = c_E·E − (d_L(DO,BOD₅) + c_L)·L`. *(Fixed in deck.)*

### M10. Deck slide 4 "Vitality 78" — the dashboard shows **84** static / **89** live
Vitality is computed live: at default levers (plant 100%, DO 6.5, flow 0.35) → `26 + 17.5 + 20 + 25 = 88.5 → 89`. *(Deck fixed.)*

### M11. Deck slide 4 "calibrated empirical LOCO model outputs"
The notebook says no Platt/isotonic/Hosmer-Lemeshow calibration was ever run and 8 stations are hard-clipped at P=1.0. "Calibrated" is not defensible. *(Changed to "embedded empirical LOCO + Phase-5 PAR outputs".)*

### M12. Deck slide 5 "where Stream-GAT points to highest causal ROI"
H3 is a null. The causal signal that *is* supported is DO (H1). *(Re-pointed to the DO model.)*

---

## 3. 🟡 Structural / packaging issues

### S1. Three different product names across three artifacts
| Artifact | Name |
|---|---|
| Deck | `EcoSentinel-DipteraCAST` |
| Notebook | `EcoSentinel-DipteraCAST` |
| Dashboard `<title>` | `EcoSentinel Horizon \| Global Nature Watch River Edition` |

Devpost needs **one** name. Recommend: public name **EcoSentinel**, technical name **EcoSentinel-DipteraCAST**, and drop "Horizon / Global Nature Watch" from the dashboard title (or keep it as a theme label only).

### S2. The notebook is not reproducible from `submission/`
It reads 14 CSVs (`data/harmonized/*.csv` + `outputs/tables/Project_A_*.csv`). None are in `submission/`. It *is* fully executed (exec counts 1–16, no errors) so results display — but the in-notebook promise *"Kernel → Restart & Run All, only pandas needed"* will fail for a judge.
**Fix options:** (a) ship a `data/` + `outputs/tables/` folder (~1 MB) alongside it; (b) change the promise to "outputs are pre-computed; re-running requires the project repository".

### S3. Deck timing is unbalanced for a 3-minute slot
Slide 3 gets 25 s to carry 3 hypothesis verdicts + PAR + health economics; slide 2 gets 40 s for four pillars. The master storyboard is written to 4:15, not 3:00.
**Fix:** rebalanced to 25 / 40 / 40 / 45 / 30 = 180 s. *(Done; mirrored in the new script.)*

### S4. `submission/` mixes Project A and Project B
It contains `OneAquaHealth_RiverPrescription_方案书.html` (Project B) and `project_b_supplementary/` (ThermalAqua-PINN). Fine if intentional — but if these are separate Devpost entries they should be separate folders, and neither Project B file is referenced by the EcoSentinel deck.

### S5. No video file exists yet
`video link (3 min demo)` is still a placeholder; no `.mp4/.mov/.webm` anywhere in the workspace. Script below is ready to shoot.

### S6. Project A's title outruns its evidence (already flagged in the dashboard's own caveat panel)
"…**River Network Topology Govern** Arboviral Vector Proliferation" — but H3 fails to reject the null (p = 0.3125) and the edge table has **zero branching nodes**. Don't put "topology governs" in the Devpost title. *(Devpost text below avoids it.)*

### S7. ⚠️ A second Devpost draft appeared in `submission/` during this pass
`DEVPOST_SUBMISSION_READY.md` (11.4 KB) was written at 00:10 — not by this session. It is **not** wrong to have it, but it re-introduces three claims this audit specifically flags:

| Its wording | Problem |
|---|---|
| "shields **97,000+ European residents** and vulnerable seniors" | headcount framing of a PAR exposure sum — the notebook's #1 forbidden reading (overlapping 500 m buffers) |
| "verifiable **clinical** health economic impact (€553k/yr)" | Module 2 is a parameterised counterfactual, not clinical evidence |
| Project name "…Causal AI & **Living Digital Twin**…" | the submission contains no digital twin; the dashboard is a scenario sandbox over one cross-sectional snapshot |

**Action:** pick one Devpost draft and delete or archive the other. This session's draft is `DEVPOST_SUBMISSION.md`. The file has been left untouched — no deletion was performed.

---

## 4. Suggestions (ranked by expected judge impact)

1. **Make "the honest negative result" the spine of the pitch, not a footnote.** The Toulouse null + uncertainty gate is the single most differentiating thing here. Most hackathon entries claim 99% accuracy; this one has a pre-registered null and a refusal gate. Give it 20 s of the 3 minutes.
2. **Pick ONE headline number and repeat it.** Right now the deck offers 0.922, 0.886, −28.2%, −37.2%, −17.1%, 47.7%, 33.9%, 97,790.6, €553,614. Recommend the pitch headline be **"−17.1% modelled vector emergence, −47.7% of baseline exposure, zero litres of pesticide"**, with everything else as supporting detail.
3. **Kill the "1,859 / 97,791 protected" framing.** Replace with "97,790.6 PAR units of exposure removed (−47.7%)" and keep the overlapping-buffer caveat in the same breath. This is a credibility *gain*, not a loss.
4. **Fix the dashboard's default state.** It currently loads at full NbS deployment, so the before/after contrast — the whole point of the cockpit — is invisible until you drag a slider down. Consider defaulting to the polluted baseline and letting the judge discover the restoration.
5. **Add a one-click "data provenance" line to the dashboard**: "85 stations · 2024-07-02 → 2024-09-13 · OneAquaHealth harmonized field table". It already exists in the provenance drawer; surface it on the main view.
6. **Ship the tables with the notebook** (S2). A judge who can re-run beats a judge who has to trust.
7. **Standardise thresholds in one place** — one shared constant block (DO_floor = 6.5, flow_floor = 0.35, BOD_ceiling = 1.8, DO_hypoxia_display = 4.0) rendered into all three artifacts.
8. **Consider dropping the "−60.8%" cockpit card entirely.** It is the only number in the whole submission with no table behind it, and it sits next to the audited −17.07%.

---

## 5. Change log applied in this pass

| File | Change |
|---|---|
| `EcoSentinel_3Min_Pitch_Deck.html` | dashboard link → `EcoSentinel_GNW_Horizon_Edition.html`; "25 confounders" → 10; DO/flow/BOD thresholds standardised; model card split (classification vs regression); H2 p quoted as Mann-Whitney 0.0029 (+ permutation note); ODE formula corrected to code; "Seniors Protected" → "Senior ΔPAR"; slide 4 Vitality 78 → live value 89; "calibrated" removed; GAT→DO re-pointed on slide 5; "River Passport" → the dashboard's real "Whispers from the River" board; all 5 speaker notes rewritten; timings rebalanced to 3:00 |
| `EcoSentinel_GNW_Horizon_Edition.html` | ⚠️ **re-applied at 01:50 via `scripts/apply_submission_audit_fixes.py` — see §6; the first pass was lost** — `ΔPAR Total` −45.9% → −47.7% (3 places); "Super Learner highest PR-AUC 0.943" sentence corrected; `Ghent Basin`/`Ghent Reach` → Milan Navigli; 0.30 m/s kept as the pre-specified marker with the "threshold-shape test null (p = 0.84)" qualifier on the provenance line, velocity tooltip and cockpit caption; `v_crit = 0.20 m/s` corrected; "Neighbours Shielded" → "Exposure Removed (ΔPAR units)" with the overlapping-buffer caveat; BOD placeholder 2.0 → 1.8 (cosmetic, see §6); −60.8% card relabelled as an illustrative index citing the audited −17.07%; ODE legend names the day-30 adult index; `onCockpitLeverChange()` now runs at boot (vitality 84 → 89, exposure 97,791, cost €553,614) |
| `EcoSentinel_3Min_Video_Script.md` | **new** — 180 s shot-by-shot script |
| `DEVPOST_SUBMISSION.md` | **new** — project name, elevator pitch, About-the-project (Markdown + LaTeX), gallery spec, judge notes |
| `EcoSentinel_CONSISTENCY_AUDIT.md` | **new** — this document |
| `EcoSentinel_3Min_Pitch_Deck.pre_audit_backup.html` | **new** — pre-edit backup of the deck |

---

## 6. ⚠️ CORRECTION — the dashboard fixes were lost and have been re-applied

**Found:** 2026-10-05 ~01:15, while re-verifying the H3 wording.

Section 5 above states the dashboard fixes were applied. **At 01:15 they were not on disk.** The file
`submission/EcoSentinel_GNW_Horizon_Edition.html` (and its root-level twin, both mtime **00:57:04**,
both md5 `8cafce6635`) still carried every pre-audit string:

| Claimed fixed | State found at 01:15 |
|---|---|
| `ΔPAR Total: -45.9%` → `-47.7%` | `-45.9%` × 3 — not fixed |
| `Ghent` leaked in inspector + whisper board | `Ghent` × 3 — not fixed |
| `Neighbours Shielded` | present × 2 — not fixed |
| `-60.8% Vector reduction` | present — not fixed |
| `v_crit = 0.20 m/s` provenance line | present — not fixed |
| `onCockpitLeverChange()` at boot | absent — not fixed |

The deck and the three new `.md` files **did** retain their edits, so this was specific to the
dashboard. Both dashboard copies were byte-identical, so a single write at 00:57 produced both.

**Root cause (why an HTML patch is not durable).** `EcoSentinel_GNW_Horizon_Edition.html` is a
**build artifact**. I regenerated it into a temp path from `scripts/build_gnw_horizon_edition.py`
and diffed:

- builder output: **154,615 B**
- file on disk: **310,759 B**
- **99+ diff hunks** — the file is builder output *plus* a long chain of `fix_gnw_*.py` hand-patches
  (typography, sand palette, marker animations, layout).

The project's own `scripts/resync_built_db_embed.py` docstring says this outright: *"is then
hand-patched by a chain of `fix_gnw_*.py` scripts that touch its LAYOUT. Regenerating from the
builder would throw that layout work away."* So any one-shot heredoc patch is fragile.

**Repair.** The fixes now live in a re-runnable, idempotent script:

```
scripts/apply_submission_audit_fixes.py        # --check for a dry run
```

It patches **both** copies in one pass, asserts each target's occurrence count, skips edits already
applied, and reports bytes changed. Re-run it after any rebuild.

**Verification after repair (01:50).**

- both copies byte-identical: md5 `7e476c36afc7243107aa82ea004c7b84`, 311,378 B
- `<div>` / `</div>` = 263 / 263
- `node --check`: both inline script blocks OK
- all 11 "must be present" strings present; all 8 "must be absent" strings absent
- **headless Chrome (`file://`)**: 365 KB DOM, **no** Uncaught/TypeError/ReferenceError/SyntaxError;
  `Exposure Removed (ΔPAR units)`, `97,791` and `€553,614` all render on load (proving the boot-order
  fix took), `Ghent` absent, threshold qualifier live

### Two recommendations in section 4 are revised

- **M3 (flow threshold) — recommendation changed.** Section 4 said *unify on 0.35 m/s*. That is
  wrong, and I am reversing it. Source `Project_A_H1_H2_H3_FormalTests.csv` shows the pre-specified
  test cutoff is **0.30 m/s** (`"Pre-specified 0.3 m/s Mann-Whitney + 10,000 label permutations"`).
  0.35 m/s is only the *scenario-lever reference* (`Math.min(1, flowVal / 0.35)`) and the slider's
  default position. Relabelling 0.30 → 0.35 everywhere would have **misstated the tested cutoff**.
  What was actually applied instead: keep 0.30 m/s as the pre-specified marker, and attach the
  honest qualifier wherever it is presented as physics — the provenance line (was mislabelling
  `v_crit = 0.20 m/s`), the velocity tooltip, and the cockpit caption. The `0.20 / 0.40` legend
  bands are a *display* colour scale, not a threshold claim, and were left alone.
- **M5 (BOD card) — downgraded to cosmetic.** `simCardPlayNumbers` is overwritten at runtime by
  `updateCockpitSimulator()` to `DO 6.5 mg/L • Shading 100%`. The static `BOD 2.0` string is only
  the pre-JS placeholder and is never seen. The edit is harmless housekeeping, not a fix.

### New findings from this pass

- **S8. Both HTML files depend on `cdn.tailwindcss.com`, which this environment blocks (HTTP 403
  from Cloudflare).** Re-tested all six external hosts: `unpkg.com`, `cdn.jsdelivr.net`,
  `fonts.googleapis.com` and `fonts.gstatic.com` all return 200; **only `cdn.tailwindcss.com` is
  refused.** Consequence: in this sandbox the deck and dashboard render **unstyled**, and
  `--virtual-time-budget` cannot expire while that request is pending — which is why a naive
  headless run hangs forever. Workaround used: `--host-resolver-rules="MAP cdn.tailwindcss.com
  ~NOTFOUND"`. Two implications:
  - I could verify **DOM content and JS execution**, but **not visual layout**. The screenshot
    checks in section 5's verification list cannot be reproduced in this environment.
  - It is a **latent submission risk**: Tailwind's Play CDN compiles at runtime and is explicitly
    "not for production". If a judge's network refuses it (corporate proxy, mainland-China egress),
    the deliverable is a wall of unstyled text. The v4 browser build is *not* a safe drop-in —
    these files use a custom palette (`coral-*`, `paper-*`, `sage-*`, `river-*`) declared through
    the Play CDN's JS `tailwind.config` API, which v4 does not support. The durable fix is to
    pre-compile the CSS and inline it.
- **S9. `submission/` is not the only copy.** `EcoSentinel_GNW_Horizon_Edition.html` exists at the
  workspace root *and* in `submission/`. They were byte-identical, but nothing enforces that.
  `apply_submission_audit_fixes.py` writes both; **freeze the pair before submitting.**

### Verification performed after patching

- **JS syntax:** every inline `<script>` block in both HTML files passes `node --check` (deck: 2/2 OK; dashboard: 2/2 OK).
- **Deck runtime (headless Chrome, `file://`):** 5 slides render, exactly 1 active, dashboard link resolves to `EcoSentinel_GNW_Horizon_Edition.html`. Zero old-narrative strings remain ("River Nature Diary", "Streeter-Phelps", "River Passport" as a notes claim, "trout", "esteemed jury" all absent). *(Corrected: the speaker-notes drawer was subsequently removed at the user's request, so "drawer populated" no longer applies — see §7.)*
- **Dashboard runtime (headless Chrome, `file://`):** loads clean; KPI reads `ΔPAR Total: -47.0%` for the default Milan basin (Milan's true Phase-5 value is 47.03%) and `-47.7%` when the basin selector is set to *All*; cockpit now boots at vitality **89** with **97,791** ΔPAR units and **€553,614/yr**; ODE chart and caption agree; zero occurrences of "Ghent" in the rendered DOM.
- **Not verified:** live tile loading and interactive click-through were only partially exercised (headless `--dump-dom` does not simulate pointer events). Recommend one manual pass in Chrome before recording.

---

## 7. Second pass (2026-10-05 ~02:00) — the video script and the Devpost, traced line by line

Section 1–6 audited the deck, notebook and dashboard. This pass audited the two files that were
written *during* this session and had only been spot-checked: `EcoSentinel_3Min_Video_Script.md`
and `DEVPOST_SUBMISSION.md`. Every number in both was traced to `outputs/tables/`.

### Defects found and fixed

| # | Where | Defect | Fix |
|---|---|---|---|
| **V1** | Video script, pre-flight #4 | Told the operator to *"press `N`"* on the deck to open the speaker notes — **impossible**, the drawer was removed earlier at the user's request | Now: keep this script on a second screen; notes explicitly say `N` no longer opens anything |
| **V2** | Video script, scene 3 | **Self-inflicted.** The H3 clarification grew the scene from 99 → **107 words in a 40 s slot = 160 wpm** — faster than every other scene, in the one scene the script tells you to *slow down* | Trimmed to **98 words (147 wpm)** with the H3 substance intact. All stated counts resynced: header 406 → **410**, scene 3 "~95" → "~98", scene 4 "~100" → "~101", timing sheet 99 → 98 / 100 → 101 |
| **V3** | Video script, scene 2 VO | Voiceover said *"all land within PR-AUC **0.93 to 0.95**"* while its own on-screen chips say **0.925 – 0.951**. LightGBM's city-averaged PR-AUC is **0.9249** — below 0.93. The visual was right, the voiceover was not | Voiceover now says **0.925 to 0.951**, matching the chips |
| **V4** | Video script, scene 4 | Paired **€553,614/yr (acute-only)** with **"payback ~1.9 yr"**. But €1,275,000 / €553,614 = **2.30 yr**; 1.81 yr is the *incl.-rehab* figure (€1,275,000 / €704,738). Mixing the two | Now **"payback 2.3 yr"**, consistent with the cost figure beside it. The cheat sheet's "1.81–2.30 yr" line was already correct |
| **D1** | Devpost, files table | Same `N` instruction as V1 | Corrected |
| **D2** | Devpost, reproducibility | Said the notebook reads **14 CSVs**. It references **17** distinct paths (15 × `outputs/tables/` + 2 × `data/harmonized/`) | Corrected to 17 |
| **D3** | Devpost, headline-results table | Quoted the DML effect as bare **"p = 0.0023"**. The table's canonical column `p_value_city_cluster` = **0.0045081** (two-sided); 0.0023 is the one-sided halving | Now **"one-sided p = 0.0023 (two-sided 0.0045)"** |
| **D4** | Devpost, ×2 | Said the dashboard *"needs internet for basemap only"*. It also pulls Tailwind, Chart.js, ECharts, Leaflet and Google Fonts from public CDNs — see S8 | Both corrected, and a new **limitation #9** added disclosing the CDN dependency |

### Verified correct against source (no change needed)

`288,152` buffer population · `97,790.6` ΔPAR · `−47.68% → 47.7%` · `21,569.4` 65+ ΔPAR ·
**`48.13% → 48.1%`** 65+ reduction (ΔPAR₆₅/baseline₆₅ = 21,569.4/44,813.5 — the Devpost's
"48.1% vs 47.7% gap" is right) · `123.066 → 99.342` day-30 adult index · `372.255 → 308.725`
cumulative emergence · `−17.07%` · `€553,614.3` acute · `€704,738.2` incl. rehab · `€1,275,000`
CapEx · per-city acute payback `1.391` (Athens) – `5.574` (Coimbra) · `1,466.9` infections averted ·
`51.21` DALYs · H1 β `−0.2818` · H2 Mann-Whitney `0.00285` / local-linear `0.8365` · H3 effect
`−0.0657`, W⁺ = `10`, p = `0.3125` · dataset **85 × 49** · notebook **25 markdown + 16 code** cells ·
model means ElasticNet `0.9365` / RF `0.9493` / XGB `0.9376` / LGBM `0.9249` / CatBoost `0.9511` /
Super Learner `0.9434`, SL R² `0.8855 → 0.886`.

**Two numbers deserve a note, because both are easy to misstate:**

- **"Five model families" is correct but the table has six rows per city.** The five base learners
  plus the non-negative Ridge Super Learner. The 0.925–0.951 range describes the **five base
  learners**; including the stacker makes it 0.925–0.951 anyway (SL = 0.9434, inside the range).
- **Per-fold PR-AUC dips far below the averages.** Coimbra/LightGBM is **0.7689**. Any phrasing like
  "the models score 0.93–0.95" is a statement about city-averaged PR-AUC, **not** about every fold.
  If a judge asks "what's your worst fold?", the answer is 0.77, not 0.93.

### S7 re-confirmed (unchanged)

`DEVPOST_SUBMISSION_READY.md` still carries all three flagged claims: *"shields 97,000+ European
residents"* ×2, *"verifiable **clinical** health economic impact"*, and the title
*"…Causal AI & **Living Digital Twin**…"*. Nothing was deleted. **Pick one draft** — this session's
is `DEVPOST_SUBMISSION.md`.

---

## 8. Third pass (2026-10-05 ~08:40–09:00) — S8 fixed: Tailwind pre-compiled and inlined

S8 flagged the biggest remaining submission risk: both deliverables load Tailwind from
`cdn.tailwindcss.com`, which **compiles CSS in the browser at runtime** and is documented by its own
authors as "not for production". If a judge's network refuses that host, the deck and dashboard
render as unstyled text.

### What was done

`scripts/build_selfcontained_html.py` now pre-compiles the CSS with the **real Tailwind CLI**
(`tailwindcss@3.4.17` — the same v3 release the Play CDN serves) using the files' own inline
`tailwind.config`, and inlines the result as a `<style>` block. Output goes to `_selfcontained/`;
**the live deliverables are untouched.**

| File | Before | After | Inlined CSS |
|---|---|---|---|
| `EcoSentinel_3Min_Pitch_Deck.selfcontained.html` | 56,362 B | 73,583 B | 19,110 B |
| `EcoSentinel_GNW_Horizon_Edition.selfcontained.html` | 334,039 B | 362,782 B | 29,579 B |

**The subtlety that would have broken the page.** You cannot simply delete the CDN `<script>` and
leave the config block. The Play CDN defines a global `tailwind` object, and the page does
`tailwind.config = {…}`. With the CDN gone that line throws `ReferenceError: tailwind is not
defined`, killing every subsequent script on the page. **Both** blocks are removed, and the builder
asserts that neither `cdn.tailwindcss.com` nor `tailwind.config` survives.

### Parity evidence (not "it compiled", but "nothing regressed")

Class-coverage audit of the compiled CSS against every static class token in the markup:

| | tokens | not compiled | verdict |
|---|---|---|---|
| Deck | 36 tailwind-ish | **0** | full coverage |
| Dashboard | 368 static tokens | **9** | all 9 are non-regressions (below) |

The dashboard's 9: `py-0.2`, `shadow-xs`, `shadow-2xs` are **not valid in Tailwind v3**, so they were
unstyled under the Play CDN too. `aoi-btn`, `basemap-btn`, `layer-pill`, `rf-pill`, `tooltip-body`,
`tree-node` are **JS selector hooks with no CSS rule anywhere** (referenced only via
`querySelectorAll('.aoi-btn')` and assigned through `className = 'aoi-btn px-2.5 …'`) — also
unstyled before. **No class that previously had styling lost it.**

Also verified: the custom palettes compile with the correct values
(`river-600 → rgb(43 114 125)`, `coral-600 → rgb(199 74 53)`, `sage-300 → rgb(180 204 163)`,
`gnw-teal → rgb(13 148 136)`, `gnw-sky → rgb(2 132 199)`, `gnw-sand → rgb(203 214 230)`) and the
custom families resolve (`Fraunces` serif, `Caveat` hand, `JetBrains Mono`).

> ⚠️ **Verify colours in `rgb()` form, not hex.** Tailwind emits
> `rgb(43 114 125 / var(--tw-text-opacity, 1))`, never `#2B727D`. A hex-based check reports
> false misses for every custom colour. (My first check did exactly that.)

### The bonus: visual verification is now possible

Because the inlined build no longer needs the blocked host, it renders **with styles** in headless
Chrome — which S8 said was impossible. Screenshots: `_selfcontained/deck_selfcontained.png`,
`_selfcontained/dash_selfcontained.png`.

### Recommendation

Swap the two live deliverables for the `_selfcontained/` versions before submitting, then re-run
`python scripts/apply_submission_audit_fixes.py --verify` (the content checks are unaffected — the
patched strings live in the body, not in the removed CDN block). Doing so removes the CDN dependency
from the critical path entirely; the only remaining external needs are map tiles, Chart.js/ECharts,
and web fonts.

---

## 9. Fourth pass (2026-10-05 ~09:00) — deck legibility

### What was asked

1. Delete the "Track 2 × Track 3 Dual Focus" label in the top-left of slide 1, and any similar
   track-framing wording elsewhere in the deck.
2. Make the text bigger — a hard floor of 14px everywhere.
3. (Follow-up) Slide 3's left half is cramped; give it more room.

### What the deck actually is

`#stage` is a fixed **1920×1080** canvas that JavaScript scales with `transform: scale()` to fit the
window. Every `px` value in the markup is therefore a *design unit*, not a screen pixel — and
`text-xs` (12px) renders at roughly **9.5px** on a 1512-wide window (scale ≈ 0.79). That, not the
class names alone, is why the deck reads as too small.

### Sub-14px utilities found and raised

| utility | px | count | replaced with |
| --- | --- | --- | --- |
| `text-xs` | 12 | 45 | `text-sm` (0.875rem = 14px, 20px line-height) |
| `text-[11px]` | 11 | 11 | `text-[14px]` |
| `text-[10px]` | 10 | 5 (4 after the badge removal) | `text-[14px]` |

One element carried both `text-xs` and `text-base`; Tailwind's stylesheet order already let
`text-base` win, so the inert class was dropped rather than left as a confusing pair.

### ⚠️ A regression I introduced, and fixed

Raising the body text to 14px made the H3 card's left-hand sentence wider, which squeezed the
right-hand column and broke the headline p-value across two lines — `p = 0.3125` rendered as `p =` /
`0.3125`, the single most important number in that card. Measured before the fix: left text 659px +
right column 157px = 816px of the 818px available. The row was completely saturated.

Two fixes, both kept:

- `shrink-0 pl-4` on the right column plus `whitespace-nowrap` on its three lines, so the number can
  never wrap again;
- slide 3's grid widened from **6/6 to 7/12 + 5/12** (Katherine's call), giving the left half ~148px.

After: card 998px wide, left text 807px over 2 lines (was 3), p-value 100px on 1 line, sitting 1px
inside the card's padding edge, no overflow. Measured with the real web fonts loaded, not the
fallback.

### Track framing removed

- The slide-1 badge (a `<span>` reading "Track 2 × Track 3 Dual Focus").
- The same framing inside `SPEAKER_NOTES` — unreachable dead code, since the drawer element no longer
  exists, but the wording should not survive anywhere.

### Verification

`node scripts/verify_deck_legibility.mjs --shots` — **7/7**, driving the self-contained build with
every external host mapped to `NOTFOUND`:

| check | result |
| --- | --- |
| all 5 slides parsed | PASS |
| no visible text below 14px | PASS — sizes in use: 14 / 16 / 18 / 20 / 24 / 30 / 60px |
| no slide content overflows its slide box | PASS |
| no "Track 2/3" or "Dual Focus" in rendered text | PASS |
| no duplicate element ids | PASS |
| **negative control: probe catches an injected 12px element** | PASS (reported exactly 1) |
| no uncaught JS exceptions | PASS |

All five slides were screenshotted at native 1920×1080 — with the HUD asserted to match the active
slide on each capture — and **looked at**, not merely asserted on. Files:
`_selfcontained/deck_slide{1..5}_legible.png`.

### Two caveats worth knowing

1. **14px here is a design unit, not a screen pixel.** At 1920×1080 fullscreen the stage scale is 1.0
   and 14px is 14px. On a 1512×982 window the scale is ≈0.79, so 14px renders at ≈11px. If the goal
   is "14px as I actually see it", the stage has to shrink (e.g. to 1600×900) or the floor has to rise
   to ≈18px. Say which — it is a small change either way.
2. **Icons and fonts are still CDN-dependent.** Offline, Lucide never loads, so icon-only controls
   render as empty white pills: the white pill at the top-right of every slide is the fullscreen
   button with no icon. Pre-compiling Tailwind (§8) does not fix that; vendoring Lucide would.

### Scripts (both re-runnable and idempotent)

- `scripts/apply_deck_legibility_fixes.py` — every edit above, writes both copies, with `--check` and
  `--verify`. `--verify` asserts the font floor, the absence of track framing, the pinned p-value
  column, the slide-3 split, and byte-identity of the two copies.
- `scripts/verify_deck_legibility.mjs` — the browser gate above.

### Note on the change report

`apply_deck_legibility_fixes.py` originally decided "changed / no change" by comparing byte counts.
`col-span-6` → `col-span-7` is a *same-length* edit, so it reported "no change" while the file had in
fact changed. The comparison is now on content, and the report prints an md5 of the result.

---

## 10. Fifth pass (2026-10-05 ~09:25) — §8 closed, and the dashboard has the deck's problem too

### §8's claim is now actually verified

§8 said pre-compiling Tailwind made visual verification possible, but at that point only the **deck**
had been rendered. The self-contained **dashboard** has now been driven in a real browser at
1920×1080 (`scripts/probe_font_floor.mjs`):

| signal | result |
| --- | --- |
| `readyState` | complete |
| `typeof tailwind` | **undefined** — the runtime CDN really is gone |
| Leaflet / Chart.js / ECharts | all loaded — the map and charts really render |
| uncaught JS exceptions | **0** |
| horizontal document overflow | none (scrollWidth 1920 = clientWidth 1920) |
| DOM elements | 1,032 |

Screenshot: `_selfcontained/dash_selfcontained_rendered.png`.

### 🔴 New finding: the dashboard's typography is far below the floor

Katherine's 14px requirement was stated for the deck. The dashboard is considerably worse:

| size | count |
| --- | --- |
| 9px | 68 |
| 10px | 132 |
| 11px | 72 |
| 12px | 62 |
| 14px | 2 |
| 18px | 5 |
| 22px | 2 |

**334 text elements below 14px**, in 51 distinct class groups — and the worst offenders are exactly
the ones a viewer is meant to read: KPI tile labels (`DO Sat`, `4.97 mg/L`, `0.308 m/s`), risk badges
(`VULNERABLE`, `CRITICAL P0`), the station-card prescription lines, and the map legend
(`Transmission Probability`). In a 3-minute video watched on a laptop, 9–10px is unreadable.

The shape of the problem differs from the deck's: the deck had 61 offenders and room to grow. Here it
is 334 elements inside fixed-height panels, so a blanket floor pushes content out of the scroll
containers instead of reflowing.

### The apparent clipping is NOT a defect (measured, not eyeballed)

The screenshot looks like the right-hand panel and the bottom-left chart are cut off at the 1080
edge. They are not. Every element was traced to its nearest clipping ancestor:

| element | ancestor overflow | verdict |
| --- | --- | --- |
| left rail, 4 stacked panels | `auto/auto`, scroll 1896 vs client 1016 | reachable by scrolling |
| right roster, station cards | `auto/auto`, scroll 3784 vs client 360 | reachable by scrolling |
| `rf-pill` "Senior Exposure" (x 1856→1975) | `auto/auto`, scroll 532 vs client 448 | reachable by horizontal scroll |
| Leaflet map `<svg>` (160,−38)–(2080,1181) | `hidden/hidden` | Leaflet internal — expected |
| `div.leaflet-proxy` at (551396,375124) | `hidden/hidden` | Leaflet internal — expected |

No clipping bug. What the measurement *does* surface is a demo-usability fact worth knowing before a
live pitch: at 1920×1080 the visible window shows **~54% of the left rail** (1016 of 1896px) and
**~10% of the station roster** (360 of 3784px). The presenter will be scrolling through most of the
demo.

### Recommendation

Do a dashboard pass, but not as a find/replace:

1. Raise only what is *read* — KPI labels, badges, roster text, legend — to ≥12px, and the numbers
   themselves to ≥14px. Leave genuinely decorative micro-type alone, or delete it.
2. Re-measure afterwards. The right gate is "no *new* content pushed below the fold", which is a
   different assertion from the deck's "nothing overflows".
3. The alternative — a blanket 14px floor — buys legibility at the cost of a taller layout and more
   scrolling. That is a design decision, not a bug fix, so it needs Katherine's call.





---

## 11. Sixth pass (2026-10-05 ~09:40) — draggable split (default 1/3) + click-to-zoom charts

Katherine's request, verbatim: *"dashboard左半边的比例可以自己拉动调整，右边自适应大小 / 左边的图表等
可以点击放大，适应大小"*, then the follow-up *"现在默认左边太小了，改成1/3，右边2/3吧"*.

The live dashboard's rail was a hard-coded `w-[320px]` = 16.667% of 1920 — hence "太小".

### What was built

| Piece | Implementation |
|---|---|
| Rail width | `style="width:var(--rail-w,33.333%)"` — a proportion, not a pixel width |
| Divider | `#railResizer`, 7px, `cursor: col-resize`, hairline that thickens on hover, focusable (`←`/`→` nudge, double-click resets) |
| Drag | window-level `pointermove`/`pointerup` for the duration of the drag, **not** `setPointerCapture` (capture is unreliable under synthetic input) |
| Right side | adapts by construction — measured below |
| Zoom | click a rail chart panel → it is re-parented into `#panelZoomOverlay` and fills it; Esc / click-outside closes; `←`/`→` moves between panels while open |
| Slot restore | the panel's original position is remembered with a **comment node**, so it returns to the same index in the scroll column rather than to the end |
| Re-measure | one `resizeAll()` that drives `Chart.getChart(cv).resize()`, `echarts.getInstanceByDom(el).resize()` and `map.invalidateSize()`; it never existed before, which is why nothing re-flowed |

All of it lives in `scripts/add_dashboard_interactions.py` (idempotent, `--check`, `--verify`), which
writes both copies. Backup: `_backups/EcoSentinel_GNW_Horizon_Edition.before_interactions.html`.

### ⚠️ A real bug found while applying the 1/3 change

The first attempt printed:

```
removed a previously applied version of this patch, re-applying
WARNING: expected exactly 1 rail <aside>, found 0 -- rail width NOT changed
```

`strip_previous()` used `RAIL_NEW` **itself** as the pattern for finding the previously applied copy.
That works until you change a constant inside it — then the pattern no longer matches what is on disk,
the strip silently no-ops, and the rail keeps the **old** width while the CSS/JS blocks around it are
upgraded. The upgrade path is now a version-agnostic regex (`RAIL_NEW_RX`, matching any percentage),
and `--verify` asserts both the CSS fallback and the JS constant are `33.333%` / `1 / 3` so the two can
never silently disagree.

Lesson, same family as the earlier marker bug: **a strip/upgrade pattern must not be derived from the
value you are changing.**

### The verification was meaningless until the libraries were vendored

The interaction test had been reporting 18/19, with the chart-resize check failing `300px -> 300px`.
The probe showed why:

```
Chart.getChart: NO Chart.getChart   Chart.instances: -1   byId: err: Chart is not defined
```

The test blocks all external hosts; `_selfcontained/` inlined **Tailwind only**, so Chart.js still came
from jsdelivr, never loaded, and every canvas sat at Chart.js's 300×150 default. The check was failing
for an environment reason and looked like a product bug.

Fix, in two parts:

1. `build_selfcontained_html.py` now inlines **Leaflet (js+css), Chart.js 4.5.1 and ECharts 5.5.1** from
   `_vendor/` — the exact bytes those CDNs serve, cached once via `--fetch-vendor` so a rebuild needs no
   network and is byte-reproducible (verified: two builds, identical md5).
   Dashboard build: 347 KB → **1.78 MB**.
2. The test now asserts a **precondition** — "Chart.js loaded" — so a future FAIL points at the library
   rather than masquerading as a layout bug.

### Measured result — 22/22, with all external hosts blocked

```
baseline: rail 640px of 1920px (ratio 0.3333, --rail-w 33.333%)   map 1273px
after drag: rail 880px            (ratio 0.4583)                  map 1033px
```

- `640 + 7 (divider) + 1273 = 1920` and `880 + 7 + 1033 = 1920` — the right side absorbs the change
  exactly. **"右边自适应" is literally true.**
- Chart canvas **buffer** `589×158 → 829×158` on drag, and `589×158 → 1799×844` on zoom. The buffer,
  not the CSS box, is the evidence: a CSS-stretched canvas keeps its old buffer and is merely scaled
  up (blurry). Both assertions were added for this reason.

### ⚠️ Self-correction: I was wrong about `min-width: auto`

Earlier in this session I recorded that `<main>` lacked `min-width: 0`, so the right side "cannot shrink
below its min-content width" and the adaptive claim was not yet true. **That was wrong, and the
measurement above disproves it.** The flexbox automatic minimum size only applies when the item's
computed `overflow` is `visible`; `<main>` carries `overflow-hidden`, which zeroes it. No fix was needed.

The general point: I had reasoned from the default instead of measuring, and the default had an exception
that applied here. `273 → 1033` is the evidence that settles it.

### Residual — `_selfcontained/` is not 100% offline

Now covered: Tailwind CSS, Leaflet, Chart.js, ECharts. **Still remote:** the basemap tiles (inherent to
any slippy map) and the Google Fonts CSS/woff2 (degrades to a system-font fallback, not a breakage).
Both are cosmetic/networked by nature; the page renders and all interactions work without them, which is
the property the tests now prove.

---

## 12. Seventh pass (2026-10-05 ~10:00) — risk tray defaults collapsed; radius values removed

Three more requests, verbatim: *"where the risk sits 默认收起状态"*,
*"圈圈的radius不要展示在dashboard上面"*, and *"同时，绿圈越大应该是越安全？红圈越大越危险"*.

Script: `scripts/apply_dashboard_ui_tweaks.py` (idempotent, `--check` / `--verify`, both copies).
Backup: `_backups/EcoSentinel_GNW_Horizon_Edition.before_ui_tweaks.html`.
Gate: `scripts/verify_dashboard_ui_tweaks.mjs` — **19/19 PASS**.

### 1. The risk tray now loads collapsed

The tray already had a working chevron (`toggleRiskSitsTray`), but the collapse state was applied
**only inside the click handler** — so the flag alone changed nothing on screen. The fix splits the state
application out into `applyRiskTrayCollapsedState()`, flips the default flag to `true`, and applies it
once at boot. `renderRiskRoster()` only rewrites `innerHTML` and never touches `display`, so it cannot
re-open the tray behind our back.

Measured: **91px tall on load** (header + footer) vs **490px** expanded — the map is no longer covered.

### 2. The radius numbers are gone

Two places surfaced the circle radius as a number:

| Where | Before | After |
|---|---|---|
| Legend explainer | `Low (5px) / Med (9px) / Critical (15px)` | `Low / Med / Critical` |
| Marker tooltip | `Severity: 100% (Radius: 15px)` | `Severity: 100%` |

The **size encoding itself is untouched** — `baseRadius = 5.0 + severity * 10.0` still runs, the three
legend swatches still grow, and the "Dot Size indicates Stress Severity" heading stays. Only the numbers
that stated a radius were removed. The gate asserts this in both directions, so a future edit cannot
quietly delete the encoding.

### 3. Answering "绿圈越大应该是越安全？红圈越大越危险"

Computed from all 85 stations in the embedded `STATIONS_DATA`, reproducing the dashboard's own formulas:

| Colour | n | radius range |
|---|---|---|
| Green (safe, P < 0.25) | 17 | 5.00 – 6.24 px |
| Amber (moderate, 0.25–0.45) | 9 | 7.59 – 10.35 px |
| Red (high, P ≥ 0.45) | 59 | 10.95 – 15.00 px |

- **"红圈越大越危险" — already true, and strictly so.** The bands do not overlap: the largest green
  circle (6.24 px) is smaller than the smallest red one (10.95 px). Every red dot is bigger than every
  amber dot, which is bigger than every green dot.
- **"绿圈越大越安全" — the case cannot occur.** A green circle is *never* big. There is no large green dot
  to interpret, because `severity` drives **both** the radius (`5 + severity × 10`) and the colour band
  (both from `p_vector_baseline`). Size and colour are two renderings of the same number, so they can
  never disagree.

Two things worth Katherine's attention, both measured rather than asserted:

1. **The size channel is redundant.** Because size and colour encode the identical variable, the dot
   radius adds no information a viewer cannot already read from the colour. It would earn its place by
   encoding a *different* variable — e.g. `buffer_500m_pop_total` (people in the 500 m buffer) or the
   PAR units removed. That is a design change, not a bug fix, so it is flagged rather than applied.
2. **The scale saturates.** `severity` is clamped to [0, 1] and P(Vector) has a median of **0.781**:
   69% of stations fall in the Red band, and **44 of 85 (52%) clamp to severity = 1.0 and render as the
   identical 15.00px red dot**. Over half the map is therefore one indistinguishable marker, and the
   colour legend has three bands for what is effectively a two-valued field.

### A test that was wrong, and why it mattered

The first run of the new gate failed one check — "no 'Radius:' left in the page source" — reporting
**61 occurrences**. That was the *test* being wrong, not the page:

- **49** of them live inside the vendored libraries (`chart.umd.js` 30, `echarts.min.js` 15,
  `leaflet.js` 4) — inlined code, never displayed.
- **12** are Chart.js config keys in the dashboard's own source (`pointRadius:`, `borderRadius:`).

None is readable by a user. The check was replaced with two assertions that test what actually matters:
the exact tooltip fragment is gone from the source, **and** a real marker is hovered so the tooltip
Leaflet renders can be read directly — `MIL_00 (Milan) … P(Vector): 0.9282 Severity: 100%`, no radius.
The hover step also guards against a vacuous pass: it asserts a tooltip actually opened.

Lesson: **assert on the rendered artifact, not on a substring scan of the source.** The source contains
libraries and config keys that share vocabulary with the UI.

---

## 13. Eighth pass (2026-10-05 ~10:30) — header button sizes unified, and a live duplication defect repaired

Request, verbatim: *"右上角3个button的字大小统一"*.

Gate: `scripts/verify_header_buttons.mjs` — **6/6 PASS** (fails 2/6 before the fix).

### The fix

All three top-right `<button>`s declare `text-xs`, but the Science & Models **label span** overrode
it with `text-sm`, so it rendered 14px while the other two rendered 12px. Measured, not read off the
class list — which is exactly what hid it:

| Button | before | after |
|---|---|---|
| River Simulator | 12px | 12px |
| Science & Models | **14px** | 12px |
| Catalog | 12px | 12px |

Applied by `apply_dashboard_ui_tweaks.py` (now three edits: tray, radius, header). Note the file's byte
count is **unchanged** by this fix (347,489 → 347,489) because `text-sm` → `text-xs` is the same length;
only the md5 moves. Another instance of the byte-count-comparison trap.

**Left alone deliberately:** the Science & Models label also carries `uppercase`. That is a different
CSS property and Katherine asked about *size*; dropping it changes the button's design language, so it is
flagged rather than changed. It is a one-word edit if she wants it.

### ⚠️ A live content defect found along the way: a sentence duplicated 4× in one tooltip

While checking idempotency I found `apply_submission_audit_fixes.py` grew the file **+171 bytes on every
run**. Root cause, verbatim from the script:

```python
("tooltip shear",
 "Flow speeds above 0.30 m/s ... and prevents larval anchoring.",          # OLD
 "Flow speeds above 0.30 m/s ... and prevents larval anchoring." + QUALIFIER,  # NEW
 1),
```

**OLD is a PREFIX of NEW.** The script's idempotency guard is `if text.count(old) == 0: ...`, so after
applying, `count(old)` was still ≥ 1 — OLD is sitting inside NEW — and the "already applied?" branch
**could never fire**. Every run appended another copy of the qualifier.

**Consequence, on disk and visible to a judge:** the velocity indicator's tooltip contained

> *"…and prevents larval anchoring. **0.30 m/s is a pre-specified operational marker: the threshold-shape
> test is null (p = 0.84), so treat the cutoff as a design assumption, not an established tipping
> point.**"* — repeated **four times** in a row.

**Why `--verify` stayed green:** `VERIFY_TOKENS` asserted the qualifier was *present*, never *how many
times*. A presence-only assertion is structurally blind to duplication. The four copies were sitting in
the file while the gate printed PASS.

**Three fixes:**

1. **A `guard` on the edit.** Edits may now carry a 5th tuple element: a string that must be ABSENT for
   the edit to run. Used wherever OLD is a substring of NEW, where the count-based guard cannot work.
2. **A repair pass**, `collapse_shear_duplicates()`, that runs before the edit loop and collapses N
   consecutive copies back to one — so a file already corrupted by the old bug is *healed*, not merely
   frozen. On first run it reported `removed 3 duplicate copy/copies`.
3. **A count assertion in `verify()`** for all three appended sentences (exactly 1 copy each), plus an
   honest `N checks, M failure(s)` line instead of the previous `len(VERIFY_TOKENS)/len(VERIFY_TOKENS)`,
   which printed a full score by construction.

Verified: qualifier count is now **1** in both copies; two consecutive runs report `applied 0/18 edits,
+0 bytes`; `--verify` reports **20 checks, 0 failures**.
