# Agentic AI Performance Dataset — Results in Simple Terms (Lay Summary)

**Dataset:** `Dataset/agentic_ai_performance_dataset_20250622.csv`  
**Size:** 5,000 agent runs (rows) × 26 variables (columns)  

This document explains the results in everyday language and points to the **plots** and **numbers** you can use as evidence in your dissertation or NVivo memos.

---

## What the dataset is measuring (plain English)

Each row is one “agent run” with:

- **How hard the job was**: `task_complexity` (1–10)
- **How independent the agent was allowed to be**: `autonomy_level`
- **How well it performed**:
  - `success_rate` (did it succeed?)
  - `accuracy_score` (how correct was it?)
  - `error_recovery_rate` (can it recover after mistakes?)
  - `performance_index` (overall combined performance signal)
- **How expensive/slow it was**:
  - `response_latency_ms`, `execution_time_seconds`
  - `memory_usage_mb`, `cpu_usage_percent`
  - `cost_per_task_cents`
- **Whether a human had to step in**: `human_intervention_required` (True/False)
- **Risk-related proxies**:
  - `privacy_compliance_score`
  - `bias_detection_score`

---

## Result 1 — What tends to go with “success” (simple cause-and-effect story)

When `success_rate` is higher, the strongest “travel companions” in the data are:

- **Higher overall performance**: `performance_index` correlation with success is **0.9805**
- **Better recovery from errors**: `error_recovery_rate` correlation is **0.9655**
- **Higher accuracy**: `accuracy_score` correlation is **0.9145**
- **Higher efficiency**: `efficiency_score` correlation is **0.9065**

**Evidence table:** `outputs/corr_with_success_rate.csv`  
**Evidence plot:** `outputs/corr_heatmap_core.png`

Interpretation in plain English:
- Agents succeed more when they are **accurate**, **efficient**, and can **recover from mistakes**.

---

## Result 2 — What tends to go with “struggle or failure”

Success drops most strongly when:

- **Tasks are harder**: `task_complexity` correlation with success is **-0.9340**
- **Memory usage is high**: `memory_usage_mb` correlation is **-0.8988**
- **CPU usage is high**: `cpu_usage_percent` correlation is **-0.7986**
- **Autonomy is higher** (in this dataset): `autonomy_level` correlation is **-0.7795**
- **Cost is higher**: `cost_per_task_cents` correlation is **-0.5274**
- **Execution takes longer**: `execution_time_seconds` correlation is **-0.4468**

**Evidence table:** `outputs/corr_with_success_rate.csv`  
**Evidence plot:** `outputs/corr_heatmap_core.png`

Interpretation in plain English:
- The dataset shows a consistent pattern: **more complex tasks + more resource load = lower success**.

---

## Result 3 — Task type matters a lot (some categories are harder)

Agents’ `accuracy_score` changes a lot depending on `task_category`.

- Statistical test (ANOVA): **F = 362.48**, **p = 0.0**

**Evidence table:** `outputs/anova_accuracy_by_task_category.csv`

Interpretation in plain English:
- Performance isn’t “one number for the agent.” It depends heavily on **what kind of task** the agent is doing.

---

## Result 4 — The dataset naturally separates into two performance “regimes”

When we group agents by performance patterns (clustering), we get **two clear groups**:

### Higher-performing group (Cluster 1)
- `success_rate` **0.6208**
- `accuracy_score` **0.6813**
- `performance_index` **0.6573**

### Lower-performing group (Cluster 0)
- `success_rate` **0.3666**
- `accuracy_score` **0.4705**
- `performance_index` **0.4378**

**Evidence table:** `outputs/cluster_profile_means.csv`  
**Evidence plot:** `outputs/kmeans_clusters_capability_accuracy.png`  
**Model fit evidence:** silhouette score for best k=2 is **0.4284** in `outputs/kmeans_summary.json`

Interpretation in plain English:
- There is a “more reliable” group and a “less reliable” group.
- This supports a governance idea: **not all agent deployments should be governed the same way**.

---

## Result 5 — When humans have to step in (accountability proxy)

A regression model predicting `human_intervention_required` shows:

- **Task complexity is a strong driver** (odds ratio ≈ **7.62**, p ≈ **1.62e-41**)
- **Accuracy is strongly related** (odds ratio ≈ **4.87e-05**, p ≈ **3.75e-10**)
- Autonomy level is **not significant** in this model (p ≈ **0.823**)

**Evidence:** `outputs/logit_accountability.json` and full model text in `outputs/logit_glm_summary.txt`

Interpretation in plain English:
- Humans tend to step in when tasks are **complex** and the agent’s **accuracy signal is weak**.

Important “validity” note (still plain English):
- The model’s predictive score is **perfect** here (CV AUC **1.000 ± 0.000**). That often means the “intervention required” label might be **very close to a built-in rule** in the dataset, rather than a naturally messy real-world outcome.

---

## Result 6 — The “trust gap” is large (intervention group performs much worse)

Comparing overall performance (`performance_index`):

- Mean when **no intervention**: **0.7680** (n=607)
- Mean when **intervention required**: **0.5141** (n=4393)
- Effect size is very large: Cohen’s d ≈ **2.455**

**Evidence:** `outputs/trust_gap_ttest.json`  
**Evidence plot to show a governance boundary visually:** `outputs/governance_boundary_autonomy_success.png`

Interpretation in plain English:
- The “needs intervention” group is **not just slightly worse**—it is **much worse** on the main performance signal.
- This supports the idea of a **governance boundary** (a point where you stop trusting the agent alone).

---

## Plots index (visual evidence you can cite)

If you keep this `.md` file in `outputs/`, these image links should render in most Markdown viewers:

### Correlations overview (what moves together)
![Correlation heatmap](corr_heatmap_core.png)

### Governance boundary view (autonomy vs success; shows oversight separation)
![Governance boundary](governance_boundary_autonomy_success.png)

### Two performance regimes (cluster plot)
![KMeans capability vs accuracy](kmeans_clusters_capability_accuracy.png)

### What most drives intervention classification (importance)
![RF feature importances](rf_feature_importance_top10.png)

---

## One-sentence takeaway (for your dissertation)

In this dataset of 5,000 agent runs, **success is most strongly associated with overall performance, error recovery, and accuracy**, while **failure is most strongly associated with higher task complexity and heavy resource usage**; task type strongly affects accuracy, and cases needing human intervention show a large measurable performance gap—supporting the idea of **governance boundaries** backed by both numbers and plots.

