# EcoSentinel — Devpost Submission (paste-ready)

> Everything below is written to be pasted directly into the Devpost fields. Section headers marked **[field]** map to the Devpost form.
> Every number is traceable to `Project_A_EcoSentinel_DipteraCAST/outputs/tables/`. Numbers that a judge could reasonably misread are followed by an explicit scope note — that is deliberate, not hedging.

---

## **[field] Project name**

```
EcoSentinel
```

*Technical / repository name:* **EcoSentinel-DipteraCAST**
*(Do not use "…River Network Topology Govern…" as a public title — see the Challenges section: the topology hypothesis was **not demonstrated** (p = 0.31), and at n = 5 the test could only have rejected H₀ on a 5/5 sweep.)*

---

## **[field] Elevator pitch** *(one line, ≤ 200 chars)*

```
Cities spray to kill mosquitoes. EcoSentinel reads the river instead: causal AI that isolates why vector risk rises, maps who is exposed, and simulates restoring the stream.
```

---

## **[field] About the project**

### Inspiration

On a warm summer evening, an urban riverside park fills with people — and then with mosquitoes. The municipal reflex is reactive: dispatch a crew, spray a neurotoxic insecticide, warn residents after they complain.

But a river can look serene on the surface and be suffocating underneath. When urban streamflow drops, dissolved oxygen falls and organic waste accumulates. The oxygen-sensitive predators of mosquito larvae — dragonfly naiads, small fish, water bugs — disappear. What is left is a warm, stagnant, predator-free pool: a near-perfect incubator for *Culex pipiens*, the principal vector of West Nile and Usutu virus in European cities.

**So we asked a different question: what if the mosquito is not the problem — what if it is a symptom?**

That question is a One Health question. Ecosystem degradation, biodiversity loss and human exposure are one causal chain, not three separate policy files. And it is exactly the chain the **OneAquaHealth** mission asks us to instrument: *connect ecosystem health, biodiversity and human well-being.* EcoSentinel is our attempt to make that chain quantitative, falsifiable, and usable by the people who actually allocate the budget.

---

### What it does

EcoSentinel turns a cross-sectional field survey into an end-to-end One Health decision pipeline:

```
[ 85 field stations × 5 European pilot cities ]
                    │
                    ▼
1. 49-dimension biophysical + hydrologic-recession feature engine
                    │
                    ▼
2. Causal attribution — Spatial Double Machine Learning
                    │
                    ▼
3. Mechanistic 30-day Culex life-cycle ODE (scenario, not forecast)
                    │
                    ▼
4. Nature-based-Solution sandbox + Population-at-Risk exposure accounting
```

1. **Reads the river as a system, not a set of dots.** 49 features per station, including four *hydrologic recession* deltas that treat antecedent rainfall as a dynamic signal rather than a static constant.
2. **Separates causation from correlation.** High temperature drives both vector hatching *and* algal blooms; surface imperviousness degrades water quality *and* destroys predator habitat. Naive regression confuses these. Spatial Double Machine Learning isolates the partial causal effect of dissolved oxygen.
3. **Simulates restoration, not just risk.** Temperature-dependent four-stage ODEs project 30-day *Culex* emergence under a polluted versus a restored water-quality scenario, so a planner can compare a nature-based intervention against business-as-usual.
4. **Converts biology into people.** Risk probabilities are multiplied against 500 m-buffer census populations to compute Population Attributable Risk (PAR), with the 65+ cohort reported separately.
5. **Refuses to guess.** When graph topology is ambiguous, an uncertainty gate flags the reach for human review instead of emitting a confident alert.

**Headline results (all model-based, all scoped):**

| Finding | Value | Scope |
|---|---|---|
| Dissolved oxygen → vector risk (causal) | **−28.18 pp per +1 mg/L**, one-sided p = 0.0023 (two-sided 0.0045) | DML, 10 pre-specified confounders, city-clustered SE (df = 4) |
| Flow velocity → vector risk | association real (p = 0.0029); **causal effect not significant** (p = 0.36); **no 0.30 m/s threshold** (p = 0.84) | observational |
| River topology (Stream-GAT vs. MLP) | wins 4/5 cities by only **+0.003 to +0.025** PR-AUC, **loses Toulouse by −0.376**; paired Wilcoxon **p = 0.3125 → fail to reject H₀** | **not demonstrated** — at n = 5 only a 5/5 sweep can reach p < 0.05 |
| Restoration scenario, 30-day emergence | **−17.07%** (cumulative emergence 372.26 → 308.73) | mechanistic counterfactual |
| Basin-wide exposure removed | **97,790.6 PAR units = −47.68% of baseline PAR** | model scenario; overlapping buffers |
| Health economics | 1,466.9 infections averted · 51.2 DALYs · **€553,614/yr** avoided acute care | parameterised, not surveillance-derived |

---

### How we built it

**Data.** We harmonised the OneAquaHealth field table (85 stations × one cross-sectional snapshot, Jul–Sep 2024) across Antwerp, Athens, Coimbra, Milan and Toulouse, and joined it to Copernicus ERA5-Land / Open-Meteo daily reanalysis, OpenStreetMap hydrography, Eurostat 2021 Census and Copernicus GHSL-POP R2023A 500 m population grids.

**Feature engineering (49 columns).** Beyond 32 raw measurements we construct 17 mechanistically motivated derived variables, including:

$$\text{DO}_{sat}(T_w) = 14.652 - 0.41022\,T_w + 0.007991\,T_w^2 - 0.000077774\,T_w^3$$

$$\text{Oxygen Deficit} = \max\bigl(0,\ \text{DO}_{sat} - \text{DO}\bigr), \qquad \text{Stagnation} = \frac{1}{v + 0.05}\cdot\frac{D}{W + 0.5}\cdot\frac{\text{Silt}\%}{100}$$

$$\Delta\text{Precip}_{7\text{–}14} = \text{Precip}_{7d} - \bigl(\text{Precip}_{14d} - \text{Precip}_{7d}\bigr), \qquad \text{Recession–Stag} = \bigl|\Delta\text{Precip}_{7\text{–}14}\bigr|\cdot\frac{\text{IMD}_{500}}{100}\cdot\frac{1}{v+0.05}$$

The four Δ-features are our answer to the "static antecedent rainfall" blind spot: when $\Delta\text{Precip}_{7\text{–}14} \ll 0$, the storm is over, the water has stopped, and the receding limb has left exactly the shallow warm pools that drive generational hatching.

**Causal inference.** We fit Robinson's partially linear model with five-fold city-based cross-fitting:

$$\tilde{Y}_i = Y_i - \hat{g}_{-c(i)}(W_i), \qquad \tilde{D}_i = D_i - \hat{m}_{-c(i)}(W_i), \qquad \hat{\beta} = \frac{\sum_i \tilde{D}_i \tilde{Y}_i}{\sum_i \tilde{D}_i^2}$$

with $W$ = 10 pre-specified pre-treatment confounders (imperviousness, tree cover, water temperature, pH, wetted width, mean depth, 7-day precipitation, 7-day growing degree-days, 7-day temperature SD, consecutive dry days) and cluster-robust inference at the city level ($df = 4$).

**Validation.** Strict **leave-one-city-out** (LOCO) with all preprocessing fitted only on the four training cities. Five model families — ElasticNet, Random Forest, XGBoost, LightGBM, CatBoost — plus a non-negative Ridge Super Learner. CatBoost leads classification (PR-AUC **0.951**); the Super Learner leads regression (**R² = 0.886**, RMSE 4.15). All five base models fall inside PR-AUC 0.925–0.951, so the conclusions are not sensitive to model choice.

**Topology.** A directed PyTorch Stream-GAT was trained against an otherwise identical topology-free MLP, using the real river edge table, with distance-decayed attention.

**Mechanistic ODE.** Four coupled stages (egg → larva → pupa → adult) with Brière temperature-dependent development and DO/BOD₅-dependent larval mortality, integrated over 30 days:

$$\frac{dE}{dt} = f(T_w)A - (d_E + c_E)E, \qquad \frac{dL}{dt} = c_E E - \bigl(d_L(\text{DO},\text{BOD}_5) + c_L\bigr)L$$

$$\frac{dP}{dt} = c_L L - (d_P + c_P)P, \qquad \frac{dA}{dt} = c_P P - d_A A$$

**Delivery.** A single-file, zero-install interactive dashboard (Leaflet + Chart.js, 85 real station coordinates) with a policy sandbox: three levers (riparian canopy, aeration, baseflow flushing) drive a live river cross-section and the counterfactual outcome cards.

---

### Challenges we faced

**1. Our headline hypothesis failed — and we kept it.** Our pre-registered H3 claim was that explicit river-network topology would improve cross-city transfer. The Stream-GAT won 4 of 5 held-out cities, but lost **Toulouse by −0.3755 PR-AUC**, dragging the mean paired difference negative (**−0.0657**) and leaving the paired Wilcoxon test unable to reject the null (**p = 0.3125**, n = 5).

The tempting move is to explain it away with "Toulouse has braided channels." We audited that and it does not hold: the supplied edge table encodes **five 17-node, 16-edge simple chains with zero branching nodes in any city**. Every city's graph is isomorphic (identical Fiedler value $\lambda_2 = 0.0192$). Ranking cities by edge homophily puts Toulouse mid-pack at $h = 0.500$; the *least* homogeneous city is Antwerp at 0.1875, which also has the highest Dirichlet energy (34.20) — the opposite of the braided-channel story. With n = 5, the correlations (r = −0.077, r = −0.261) are exploratory.

**What "fail to reject" does and does not prove.** This is the part we most want read carefully, because it is easy to overstate in both directions. Failing to reject $H_0$ means our data **did not demonstrate** a topology advantage — it does **not** mean topology has no advantage. Two structural facts make that distinction concrete:

- **The test could not have rejected $H_0$ unless GAT won all five cities.** With $n = 5$ there are only $2^5 = 32$ sign patterns, so the smallest achievable one-sided p-value is $1/32 = 0.03125$. A 4-out-of-5 result caps out at $2/32 = 0.0625$. We observed exactly 4 of 5 — so the study design, not the ecology, decided this outcome.
- **The Wilcoxon test discards magnitude.** It uses ranks, so Toulouse's $-0.3755$ collapse carries exactly the same weight as a $-0.003$ loss would. Our four wins sum to $+0.0471$; the single loss is roughly 8× larger than all of them combined. A magnitude-aware reading would say *"the sign of the effect is not stable across cities"* — not *"no difference."*

So our claim is deliberately narrow: **explicit river topology did not deliver a reliable out-of-city gain on this dataset.** That is not evidence that graph models are unsuitable for rivers — 5 cities and one cross-sectional snapshot cannot support such a claim, and the GAT still won 4 of 5. A worked version of this argument, with the exact null distribution, is in `EcoSentinel_H3_What_The_Null_Proves.md`.

**So we report the honest version: this dataset cannot identify why Toulouse failed.** What we *did* do is turn the failure into product behaviour — an **Uncertainty-Aware Discrepancy Gate** that marks ambiguous reaches *"Topologically Complex — Expert Review Requested"* rather than emitting a confident automated alert. Responsible AI is not a slide; it is a refusal path in the code.

**2. A silent bug in the counterfactual that made our impact look *worse*.** Our restoration simulator raised flow velocity but wrote two derived features under column names that did not exist (`dead_zone_stagnation_index`, `stream_power_index` instead of `vector_stagnation_index`, `stream_power_proxy`). pandas accepted the assignment silently, so the model was queried with `flow = 0.35 m/s` alongside a stream-power value corresponding to `v ≈ 0.03` — a combination that cannot occur in any real observation. Because stream power scales **cubically** with flow, the 27 stations where the flow floor binds had their exposure *overstated*.

We verified the fix by running old and new code paths side by side and gating on exact reproduction of the shipped table (`max|diff| = 0.000000`), then re-derived all three feature formulas against the harmonised dataset (85/85 rows, relative error ≤ 1e-13). Correcting it moved ΔPAR from 95,163.9 → **97,790.6**, and we re-ran all five downstream scripts so every published table stays mutually consistent. A guard now asserts that each flow-dependent feature actually moved on the stations whose flow was raised.

**3. Resisting the temptation to extrapolate our own strongest result.** Our DML estimate of −28.18 pp per mg/L is a **local linear slope** over an observed DO range of 2.09–7.19 mg/L. Applying it to the +4.5 mg/L jump used in the ODE scenario would imply −127 percentage points — impossible for a probability. So we explicitly forbid that reading in the notebook and quote it only as "a 1 mg/L change near the observed mean."

**4. Keeping the honest numbers honest in the interface.** PAR is a *risk-weighted exposure sum* over **overlapping** 500 m buffers. "97,791 residents protected" would be false, and the 65+ cohort shows the *same* relative reduction as everyone else because the risk model carries no age term. We surface all of this in the dashboard's own "what this cannot prove" panel, and we quote 97,790.6 **PAR units**, never a headcount.

---

### What we learned

1. **Ecological integrity is preventative healthcare.** Restoring stream hydraulics and oxygen regimes is a durable, non-toxic barrier against vector proliferation — and it is cheaper than the chemical cycle it replaces.
2. **Causal rigour beats black-box fitting.** A model that mistakes summer heat for water-quality degradation will send municipal money to the wrong intervention.
3. **Publishing a failure buys more trust than inflating a benchmark.** The Toulouse null is the single most credible thing in this project: it is pre-registered, it is reported against our own interest, and it produced a real product feature.
4. **Small-n honesty is a design constraint, not an afterthought.** With 5 cities, we deliberately avoided claims that need 20. Every "not supported" in this submission is a decision we made on purpose.
5. **An uncertainty gate is only worth having if it can fire.** Building a refusal path forced us to define, precisely, what "ambiguous" means.

---

### What's next

- **Sensor-in-the-loop validation.** Replace the single summer snapshot with continuous optical DO / turbidity telemetry so the 30-day ODE can finally be validated against an observed emergence series — the one thing this dataset structurally cannot provide.
- **Two-way OneAquaHealth citizen-app integration.** Our ingestion layer is specified against the official app schema but has never been exercised; connecting it would turn citizen stagnation and swarm reports into topological Bayesian priors.
- **Replace the flat cost split with a bill of quantities.** The €1,275,000 CapEx is currently divided evenly across five cities on no engineering basis; per-city payback ranges from 1.4 to 5.6 years depending on the allocation.
- **Subtropical transfer.** Adapt to basins facing dengue and chikungunya, where the same hypoxia-release mechanism is plausible but the species and thermal parameters change.

---

## **[field] Image gallery**

Upload these in this order. All five PNGs are already sitting in `submission/`.

| # | Image | Caption to paste |
|---|---|---|
| 1 | `final_clean_overview.png` | **EcoSentinel — basin overview.** All 85 real monitoring stations across Antwerp, Athens, Coimbra, Milan and Toulouse, coloured by modelled *Culex* transmission risk. |
| 2 | `river_cockpit_snapshot.png` | **The NbS cockpit.** Three levers — riparian canopy, aeration, baseflow flushing — drive a live river cross-section and the counterfactual exposure outcomes. |
| 3 | `verified_badges_and_predictive_clean.png` | **Alert roster and predictive panel.** Per-station risk badges alongside the model-based 30-day scenario view. |
| 4 | `science_drawer_cleaned_verified.png` | **Transparent model core.** The dashboard exposes the Streeter–Phelps oxygen-deficit and Brière thermal-kinetics derivations, parameters and state equations. |
| 5 | `submission_dashboard_current.png` | **"What this cannot prove."** The dashboard states its own limits in-product: overlapping buffers, no calibration test, flat cost split, unvalidated 30-day curve. |

*(If you prefer fresh captures, shoot 1600×1000 from the live dashboard — gallery images render ~2:1 in the Devpost layout.)*

---

## **[field] Video link (3 min demo)**

```
[PASTE YOUR 3-MINUTE DEMO URL HERE — YouTube / Vimeo, unlisted is fine]
```

**Shot-by-shot script, timing sheet and a spoken-numbers cheat sheet:** `EcoSentinel_3Min_Video_Script.md`

**Runtime:** 3:00 exactly (180 s). **Must-say line:** *"Don't wait for the mosquito. Read the river first."*

---

## **[field] Additional info — for judges and organizers**

*(Not shown on the public project page.)*

### Built with

Python · pandas · NumPy · SciPy · scikit-learn · XGBoost · LightGBM · CatBoost · PyTorch / PyTorch Geometric (directed Stream-GAT) · EconML-style Robinson orthogonalisation with city-clustered robust SE · Matplotlib · Leaflet · Chart.js · Tailwind · single-file HTML delivery.

### Tracks claimed

- **Primary — Track 2: Data-to-Insight.** The dataset is a cross-sectional spatial snapshot (85 stations × one sample, Jul–Sep 2024). That supports pattern, risk and health-impact insight; it does **not** support a validated temporal forecast, which is why we claim Track 2 and not a predictive early-warning track.
- **Secondary — Track 3: AI-Supported Assessment.** The responsible-AI evidence is genuinely in hand: nested LOCO, an OOD refusal gate, SHAP/PDP, and a pre-registered negative result.
- **Narrative style — Track 4.** The dashboard is deliberately framed as a "river diary" so non-specialists can use it.

### Data provenance

| Layer | Source | Period / resolution |
|---|---|---|
| Stream chemistry & benthic bio-assessment | OneAquaHealth harmonized field table | 85 stations, 2024-07-02 → 2024-09-13 |
| River network topology | Project-supplied directed edge table | 5 × (17 nodes / 16 edges), simple chains |
| Meteorology | Copernicus ERA5-Land + Open-Meteo daily reanalysis | trailing 7 / 14 / 21-day windows |
| Hydrography | OpenStreetMap | — |
| Population & age structure | Eurostat 2021 Census + Copernicus GHSL-POP R2023A | 500 m station buffers |
| Basemap tiles | Esri World Topographic Map / World Imagery / Dark Gray Canvas | web tiles (the dashboard also loads Tailwind / Chart.js / ECharts / Leaflet / Google Fonts from public CDNs — see the limitation note below) |

### Reproducibility — please read

- **The notebook is pre-executed.** All 16 code cells carry stored outputs (execution counts 1–16, no errors), so every table and figure is visible without running anything.
- **Re-running requires the project repository.** The notebook references **17** CSVs (15 from `outputs/tables/` + 2 from `data/harmonized/`), none of which are bundled in the submission folder. The in-notebook note "only pandas is needed" refers to *reading the pre-computed tables*, not to regenerating them. To regenerate from scratch, run `scripts/run_phase1_phase2_dml.py` → `run_phase3_phase4_topology_ode.py` → `run_phase5_par_exposure.py` → `run_module1…5` → `run_pillar1…3`.
- **Random seed 2026** is fixed globally across NumPy, scikit-learn and PyTorch.

### Known limitations we want on the record

1. **Exposure is not a headcount.** PAR = P(vector) × population, summed over *overlapping* 500 m buffers. ΔPAR = 97,790.6 is a risk-weighted exposure sum; it is **not** 97,791 distinct people.
2. **The elderly are not differentially protected.** The risk model contains no age term, so the 65+ cohort is reduced in exactly the same proportion as the whole population. The basin-wide 48.1% vs 47.7% gap is aggregation across cities with different age structures.
3. **Probabilities are hard-clipped.** 8 of 85 stations hit exactly P = 1.0000 and carry 17.0% of baseline exposure. No Hosmer–Lemeshow, Platt or isotonic calibration was run — treat the top of the risk scale as compressed.
4. **The cost split has no engineering basis.** €1,275,000 is divided flat at €255,000 per city. Per-city payback on acute-care savings alone spans 1.39 yr (Athens) to 5.57 yr (Coimbra).
5. **The 30-day curve is a scenario, not a forecast.** The ODE is integrated from published *Culex* thermal parameters and has never been validated against an observed emergence time series, because none exists in this dataset.
6. **Toulouse cannot be explained by braided channels.** All five graphs are simple chains with zero branching nodes. We report the failure as an unexplained cross-city generalisation limit at n = 5.
7. **Health economics are parameterised counterfactuals.** 1,466.9 averted infections, 51.2 DALYs and €553,614/yr are model exposure pushed through fixed epidemiological parameters — not surveillance-derived clinical burden.
8. **Citizen science is designed, not integrated.** The OneAquaHealth app ingestion path is specified against the official schema but has never been exercised; no citizen observation records exist in this workspace. Any claim of a live citizen feed would be false.
9. **The dashboard depends on public CDNs for its styling and charts.** Tailwind, Chart.js, ECharts, Leaflet and Google Fonts are loaded from `cdn.tailwindcss.com` / `cdn.jsdelivr.net` / `unpkg.com` / `fonts.googleapis.com`. If a judge's network refuses any of them (corporate proxy, restricted egress), the page still functions but renders unstyled. Tailwind's Play CDN also compiles at runtime, which is why we describe the dashboard as a demo instrument rather than a production deployment.
10. **Climate results are additive sensitivities.** The +1.5 / +2.5 / +2.8 / +4.0 °C scenarios offset observed 2 m air temperature; they are not a downscaled CMIP6 ensemble.

### Provenance & hackathon-period contribution

- **Pre-existing foundation:** public OSM hydrography, Copernicus ERA5-Land reanalysis, Eurostat 2021 Census and Copernicus GHSL-POP rasters, the OneAquaHealth harmonized field table and river edge table, and the published *Culex* thermal-biology parameters (Mordecai et al. 2019; Ewing et al. 2016).
- **Built during the hackathon:** the 49-dimension feature engine; the Spatial-DML causal attribution module with city-clustered inference; the strict-LOCO five-model benchmark and non-negative Ridge Super Learner; the directed Stream-GAT and the Toulouse discrepancy diagnosis; the Uncertainty-Aware Discrepancy Gate; the four-stage Brière ODE scenario engine; the counterfactual NbS policy engine; the Phase-5 PAR exposure accounting; the frontier modules (climate sensitivity, DALY economics, Pareto classification, spectral graph diagnostics, alert SOP); and the single-file interactive decision dashboard.

### Files in this submission

| File | What it is |
|---|---|
| `EcoSentinel_3Min_Pitch_Deck.html` | 5-slide pitch deck (`F` for fullscreen, arrow keys to navigate; the speaker-notes drawer was removed, so narrate from `EcoSentinel_3Min_Video_Script.md`) |
| `EcoSentinel_3Min_Video_Script.md` | 180-second shot-by-shot video script + timing sheet |
| `EcoSentinel_GNW_Horizon_Edition.html` | The live interactive dashboard (open in Chrome; needs internet for its CDN-hosted CSS/JS **and** map tiles — if those CDNs are blocked it still runs but renders unstyled) |
| `EcoSentinel_DipteraCAST_Enhanced.ipynb` | Full analytical notebook, pre-executed (25 markdown + 16 code cells, 9 result sections + 5 frontier modules + 3 publication pillars + errata) |
| `projectA-abstract.md` | Technical abstract and full research logic chain |
| `PROJECT_A_DEVPOST_AND_STORYBOARD_MASTER.md` | Submission master document |
| `EcoSentinel_H3_What_The_Null_Proves.md` | What the H3 null does and does not establish, with the exact n = 5 null distribution |
| `EcoSentinel_CONSISTENCY_AUDIT.md` | Cross-artifact consistency audit (deck × notebook × dashboard) |
