# Report 2 — Supervisor-ready summary (agentic ARC quantitative analysis)

This document translates the auto-generated `outputs/REPORT.md` into **plain English**, while keeping the **same quantitative results** and using standard technical vocabulary (effect sizes, cross-validation, inference, survival hazards).

---

## What was analysed

- **Dataset**: `C:/Users/User/Downloads/cve-bench-main/Dataset/agentic_ai_performance_dataset_20250622.csv`
- **Scale**: **5,000** observations (rows) and **26** variables (columns)
- **Purpose**: quantify how **agent capability**, **task context**, and **performance signals** relate to **operational risk proxies** (especially whether **human intervention** is required), and to stress-test a simple **human-on-the-loop (HOTL)** style intervention simulation.

---

## EDA (data quality and completeness)

**What we checked:** missing values for the main modelling fields.

**What we found:** the top-listed core fields show **0 missing** values for:

`agent_id`, `agent_type`, `model_architecture`, `deployment_environment`, `task_category`, `task_complexity`, `autonomy_level`, `success_rate`, `accuracy_score`, `efficiency_score`.

**How to explain this to a supervisor:** the core analysis is not being distorted by large-scale missing-data dropout on these variables. (You can still mention that other columns may have missingness; this section only reports the “top missingness” slice from the automated report.)

---

## RQ1 — Do “capability/performance regimes” exist, and does task type matter?

### 1) Unsupervised structure (K-means clustering)

- **Result**: best cluster count **k = 2**, silhouette score **0.428**.
- **Plain English**: the sample separates into **two broad performance/capability regimes** rather than looking like one homogeneous cloud.
- **Technical reading**: silhouette **~0.43** indicates **moderate cluster separation** (useful structure, not a perfect partition).
- **Evidence files**:
  - `outputs/kmeans_clusters_capability_accuracy.png`
  - `outputs/cluster_profile_means.csv`

### 2) Task category effect on accuracy (one-way ANOVA)

- **Result**: **F = 362.483**, **p ≈ 0**, **η² = 0.395**
- **Plain English**: **which task category you are in** explains a large portion of why accuracy differs between runs.
- **Technical reading**:
  - a very small **p-value** means the between-group differences are **extremely unlikely** to be due to chance under the ANOVA assumptions.
  - **η² = 0.395** is a **large effect size** (roughly: task category accounts for a substantial share of variance in `accuracy_score` in this model framing).
- **Governance implication**: risk controls and evaluation need to be **contextualised by use case / task category**, not judged only from headline “average agent performance.”
- **Evidence file**: `outputs/anova_accuracy_by_task_category.csv`

---

## RQ2 — Accountability proxy: what predicts “human intervention required”?

### 1) Logistic regression (GLM binomial) + cross-validated discrimination (ROC AUC)

- **Result**: **CV ROC AUC = 1.000 ± 0.000**
- **Plain English (careful wording)**: with the predictors used, the model can **separate** intervention vs non-intervention cases almost perfectly in cross-validation **on this dataset**.

**Key estimated associations (odds ratios, OR):**

| Predictor | Odds ratio | Interpretation (plain English) |
|-----------|------------|----------------------------------|
| `task_complexity` | **7.621** | Holding other model terms constant, higher complexity is strongly associated with higher odds of requiring intervention. |
| `accuracy_score` | **4.87e-05** (very small) | Higher accuracy is strongly associated with **lower** odds of intervention (directionally: better outcomes correlate with less oversight demand). |
| `autonomy_level` | **0.988** | A tiny OR near 1; combined with the p-value below, it is **not** a compelling “main trigger” in this model. |
| `privacy_compliance_score` | **0.408** | Higher privacy compliance is associated with **lower** odds of intervention in this fit (see p-value caveat below). |

**Key p-values (statistical significance of coefficients):**

- `task_complexity`: **p ≈ 1.62 × 10⁻⁴¹** (very strong evidence of association in this model)
- `accuracy_score`: **p ≈ 3.75 × 10⁻¹⁰** (strong evidence)
- `autonomy_level`: **p ≈ 0.823** (not statistically significant in this model)
- `privacy_compliance_score`: **p ≈ 0.317** (not statistically significant at conventional α = 0.05)

**Supervisor-safe caveat about AUC = 1.0**

ROC AUC = 1.0 can occur when the outcome is **highly separable** from features, but it can also indicate issues such as **label leakage**, **near-deterministic label construction**, or dataset artefacts. For a dissertation/viva, you should present the result **and** commit to a short **sanity audit** (e.g., checking whether any feature is a near-proxy for the label, reviewing how `human_intervention_required` was defined/collected).

**Evidence file**: `outputs/logit_glm_summary.txt`

### 2) Privacy controls vs latency (OLS on log latency)

- **Model**: ordinary least squares on **log(1 + latency)** with controls as specified in the pipeline.
- **Result**: privacy coefficient **−0.1887**, **p = 0.212**, **R² = 0.003**
- **Plain English**: we do **not** find statistically significant evidence that higher `privacy_compliance_score` increases latency in this specification; the model also explains **very little** of latency overall.
- **Technical reading**: this is a useful **negative result** / null finding: latency is likely dominated by other factors not captured here.

**Evidence file**: `outputs/privacy_latency_ols_summary.txt`

---

## RQ3 — “Trust gap” and interpretable threshold patterns

### 1) Welch t-test on `performance_index` by intervention requirement

- **Means**:
  - no intervention: **0.7680**
  - intervention required: **0.5141**
- **p-value**: **≈ 0** (extremely small in practice)
- **Plain English**: cases flagged as needing intervention sit in a **materially lower performance band** on this index—consistent with a measurable **trust/performance gap** between regimes.
- **Evidence file**: `outputs/trust_gap_ttest.json`

### 2) Interpretable thresholds (shallow decision tree + random forest)

- **Random forest feature importance** highlights which variables contribute most to predicting intervention in a non-linear ensemble model.
- **Shallow tree paths** provide human-readable “if–then” style thresholds (exported as JSON rules).
- **Evidence files**:
  - `outputs/rf_feature_importance_top10.png`
  - `outputs/rf_feature_importance.csv`
  - `outputs/tree_threshold_rules.json`

---

## RQ4 — HOTL / circuit-breaker simulation (counterfactual stress test)

This is **not** a claim that HOTL “works in production”; it is a **transparent counterfactual** using a defined trigger and uplift mechanism from the script.

- **Trigger prevalence**: **33.9%** of rows trigger the breaker (`trigger_rate = 0.339`)
- **Triggered subset size**: **n = 1693**
- **Mean accuracy (triggered rows)**: **0.448 → 0.435** (after vs before in the simulation framing)
- **Mean success rate (triggered rows)**: **0.336 → 0.297**
- **Wilcoxon tests (one-sided “greater” improvement)**: **p = 1.0** for both accuracy and success in the reported summary

**Plain English:** under the **current** simulation parameters, we **do not** observe statistically supported uplift on the triggered subset.

**How to frame this positively in a meeting:** this is exactly what a design-science cycle expects—an **explicitly falsifiable** governance policy prototype, measured, then revised (trigger definition, matching/imputation of “post-intervention” outcomes, covariate controls, etc.).

**Evidence file**: `outputs/hotl_sim_audit_head200.csv`

---

## Survival analysis — time-to-threshold-failure framing (Cox proportional hazards)

**Event definition:** `accuracy_score < 0.6`  
**Interpretation of hazard ratios (HR):** HR > 1 means **higher hazard** (more risk of hitting the “failure” threshold sooner, holding other covariates in the model).

Reported hazard ratios:

- `task_complexity`: **1.045** (higher complexity → higher hazard of crossing below 0.6 accuracy)
- `autonomy_level`: **1.028** (higher autonomy → slightly higher hazard in this fit)
- `privacy_compliance_score`: **0.724** (higher privacy compliance → **lower** hazard; interpret cautiously depending on model significance details in the full Cox table)

**Evidence file**: `outputs/cox_survival_summary.txt`

---

## Where to find the raw “machine summary”

If you need the exact one-liner outputs as produced by the script, see:

- `outputs/REPORT.md` (original compact export)

---

## Suggested one-sentence takeaway for a supervisor meeting

“We show that agent outcomes are **strongly task-dependent**, cluster into **distinct performance regimes**, and that **intervention demand** aligns more with **complexity and measured performance** than autonomy alone; a first-pass HOTL simulation **does not** demonstrate uplift yet, which gives us a concrete iteration target rather than a vague risk story.”
