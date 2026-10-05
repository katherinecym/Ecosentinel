# H3 — What does "fail to reject" actually prove?

**Short answer: it proves that our data could not demonstrate a topology advantage. It does not prove that topology has no advantage.** It is a statement about what this dataset can support — not a finding about how rivers work.

Everything below is computed from `outputs/tables/Project_A_Phase3_TopologyAware_StreamGAT_vs_MLP_LOCO.csv` and `Project_A_H1_H2_H3_FormalTests.csv`.

---

## 1. The test, stated exactly

| | |
|---|---|
| **H₀** | $\text{PR-AUC}_{\text{GAT}} \le \text{PR-AUC}_{\text{MLP}}$ (topology adds nothing) |
| **H₁** | $\text{PR-AUC}_{\text{GAT}} > \text{PR-AUC}_{\text{MLP}}$ (one-sided, pre-registered) |
| **Test** | Paired Wilcoxon signed-rank, one-sided, across the 5 held-out cities |
| **Observed** | $W^{+} = 10$, **p = 0.3125** → fail to reject H₀ |

---

## 2. What "fail to reject" means — and what it does not

| ❌ Wrong reading | ✅ Correct reading |
|---|---|
| "We proved topology doesn't help." | "We did not demonstrate that it helps." |
| "The null hypothesis is confirmed." | "The null hypothesis was not rejected." (a null is never *confirmed*) |
| "p = 0.31, so there's probably no effect." | "p = 0.31 means an effect this size is unremarkable under H₀ — given how little power this test had." |
| "GATs don't work on rivers." | "On these 5 cities, in one summer snapshot, the gain was not reliable." |

**Absence of evidence is not evidence of absence.** A non-significant test is compatible with a real effect that the study was simply too small to detect — and here, that is very likely the case.

---

## 3. Two structural reasons this null proves very little

### Reason A — the design guaranteed 4/5 could never be significant

With $n = 5$ there are only $2^5 = 32$ sign patterns, so the one-sided p-value can only take 16 discrete values. The **minimum achievable** one-sided p is the probability that all five cities favour GAT:

| GAT wins | Smallest possible one-sided p | Can it reach p < 0.05? |
|---|---|---|
| **5 / 5** | $1/32 = 0.03125$ | ✅ yes — and only just |
| 4 / 5 | $2/32 = 0.0625$ | ❌ never |
| 3 / 5 | $4/32 = 0.125$ | ❌ never |

We observed **exactly 4/5**. So the test was **structurally incapable** of rejecting H₀ unless GAT swept all five cities. The result is a statement about the test's power at $n=5$, not a verdict on topology.

> This is the single most important sentence to have ready: *"With five cities, the test could only have rejected the null on a five-out-of-five sweep — so four-out-of-five was never going to be significant."*

### Reason B — Wilcoxon throws away magnitude

The signed-rank test uses **ranks, not sizes**. Our five per-city differences:

| City | Δ PR-AUC (GAT − MLP) | Rank used by the test |
|---|---|---|
| Antwerp | **+0.0251** | 4 |
| Athens | **+0.0140** | 3 |
| Milan | **+0.0051** | 2 |
| Coimbra | **+0.0029** | 1 |
| Toulouse | **−0.3755** | 5 |
| **Mean** | **−0.0657** | $W^{+} = 1+2+3+4 = 10$ |

Toulouse's loss is **~8× larger than all four wins combined** (sum of wins = +0.0471). But the test gives it a single rank of 5 — exactly the same weight it would receive if the loss were −0.003.

So the test is **blind to the real shape of the result**: four tiny, consistent gains and one catastrophic loss. A magnitude-aware summary would not say "no difference" — it would say *"the sign of the effect is not stable across cities."* That is the honest descriptive finding, and it is more informative than the p-value.

---

## 4. What the numbers *do* establish (descriptive, not inferential)

1. On this dataset, adding explicit river topology did **not** improve mean out-of-city PR-AUC — mean paired Δ = **−0.0657**.
2. The effect's **sign is not stable**: positive in 4 of 5 cities, but only by **+0.0029 to +0.0251**; negative in one, by **−0.3755**.
3. Toulouse is a genuine collapse on the **classification** side — GAT ROC-AUC **0.521** (a coin flip) vs MLP 0.875; PR-AUC 0.541 vs 0.916; Brier 0.465 vs 0.186. Notably GAT's *regression* score on Toulouse held up (R² 0.910 vs 0.918), so it was the model's **ranking/discrimination** that broke, not the whole model.
4. **$n = 5$ cities, one cross-sectional snapshot** is the binding constraint on everything above.

---

## 5. Claims you may and may not make

**May claim:**
- "Explicit river topology did not deliver a reliable out-of-city gain on this dataset: mean Δ = −0.066 PR-AUC, four wins of +0.003 to +0.025, one loss of −0.376."
- "Our pre-registered test could not reject H₀ — and at $n=5$ it could only have done so on a 5/5 sweep. We report the result as **not demonstrated**, with the power limitation stated alongside it."
- "That instability is why the product ships an uncertainty gate that defers to a human expert on ambiguous reaches."

**May not claim:**
- ❌ "We proved topology doesn't help." — fail-to-reject is not acceptance of H₀.
- ❌ "GATs are unsuitable for river networks." — $n=5$, one snapshot, and it won 4/5 cities.
- ❌ "Toulouse failed because of braided channels." — the supplied edge table encodes five 17-node/16-edge **simple chains with zero branching nodes**; the mechanism is not identifiable in this data.
- ❌ "We confirmed the null."

---

## 6. The answer to give if a judge asks

> "The test failed to reject, which means our data don't demonstrate the effect — not that the effect is absent. Two reasons to be careful. First, with five cities the test can only reach significance on a five-out-of-five sweep, so four-out-of-five was never going to be significant. Second, Wilcoxon uses ranks, so Toulouse's 0.38 collapse counts exactly the same as a 0.003 loss would. What we can say is that the gain is small and its sign isn't stable across cities. That's precisely why we ship an uncertainty gate instead of a confident claim."

---

## 7. Where this is now reflected

| Artifact | Wording |
|---|---|
| `EcoSentinel_3Min_Pitch_Deck.html` | headline verdict reads **"H3 Not Supported (p = 0.31, underpowered)"**; the H3 card states the 5/5 power floor and that this is *not* proof of absence |
| `EcoSentinel_3Min_Video_Script.md` | Scene 3 adds the power clause; the cheat sheet lists the 5/5 floor |
| `DEVPOST_SUBMISSION.md` | Challenges §1 carries the power argument; the results table reads "not demonstrated" |
| `EcoSentinel_GNW_Horizon_Edition.html` | the "what this cannot prove" panel already stated the $n=5$ / no-branching limitation |
