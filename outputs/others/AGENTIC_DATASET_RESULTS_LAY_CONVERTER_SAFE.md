# Agentic AI Performance Dataset - Results (Plain-Language, Converter-Safe)

Dataset: `Dataset/agentic_ai_performance_dataset_20250622.csv`  
Size: 5,000 rows x 26 columns

This file is written to be easy to convert (ASCII-only punctuation, simple Markdown).

## What the dataset measures (plain English)

Each row is one agent run, including:

- Task difficulty: `task_complexity` (1 to 10)
- Independence allowed: `autonomy_level`
- Performance:
  - `success_rate` (did it succeed?)
  - `accuracy_score` (how correct?)
  - `error_recovery_rate` (can it recover after mistakes?)
  - `performance_index` (overall performance signal)
- Time/cost/resources:
  - `response_latency_ms`, `execution_time_seconds`
  - `memory_usage_mb`, `cpu_usage_percent`
  - `cost_per_task_cents`
- Human oversight flag: `human_intervention_required` (True/False)
- Risk proxies:
  - `privacy_compliance_score`
  - `bias_detection_score`

## Result 1 - What goes with success

When `success_rate` is higher, the strongest related variables are:

- `performance_index`: corr = 0.9805
- `error_recovery_rate`: corr = 0.9655
- `accuracy_score`: corr = 0.9145
- `efficiency_score`: corr = 0.9065

Evidence table: `./corr_with_success_rate.csv`  
Evidence plot: `./corr_heatmap_core.png`

## Result 2 - What goes with struggle/failure

Success drops most strongly when:

- `task_complexity`: corr = -0.9340
- `memory_usage_mb`: corr = -0.8988
- `cpu_usage_percent`: corr = -0.7986
- `autonomy_level`: corr = -0.7795
- `cost_per_task_cents`: corr = -0.5274
- `execution_time_seconds`: corr = -0.4468

Evidence table: `./corr_with_success_rate.csv`  
Evidence plot: `./corr_heatmap_core.png`

## Result 3 - Task type changes accuracy a lot

Accuracy differs strongly by `task_category`:

- ANOVA: F = 362.48, p = 0.0

Evidence table: `./anova_accuracy_by_task_category.csv`

## Result 4 - Two clear performance groups (clustering)

The clustering splits runs into two regimes:

Cluster 1 (higher-performing):
- success_rate = 0.6208
- accuracy_score = 0.6813
- performance_index = 0.6573

Cluster 0 (lower-performing):
- success_rate = 0.3666
- accuracy_score = 0.4705
- performance_index = 0.4378

Evidence table: `./cluster_profile_means.csv`  
Evidence plot: `./kmeans_clusters_capability_accuracy.png`

## Result 5 - When humans step in (oversight proxy)

The intervention flag is most strongly associated with:

- higher task complexity (odds ratio approx 7.62; p approx 1.62e-41)
- lower accuracy (odds ratio approx 4.87e-05; p approx 3.75e-10)

Evidence: `./logit_accountability.json` and `./logit_glm_summary.txt`

Note (validity): the model reports CV AUC = 1.000 +/- 0.000, which can indicate the label is close to a built-in rule.

## Result 6 - The trust gap is large

Overall performance differs strongly by intervention status:

- mean performance_index (no intervention) = 0.7680 (n=607)
- mean performance_index (requires intervention) = 0.5141 (n=4393)
- effect size: Cohen's d approx 2.455

Evidence: `./trust_gap_ttest.json`  
Evidence plot: `./governance_boundary_autonomy_success.png`

## Plots (visual evidence)

Correlation heatmap:

![](./corr_heatmap_core.png)

Governance boundary view:

![](./governance_boundary_autonomy_success.png)

Clustering view:

![](./kmeans_clusters_capability_accuracy.png)

Feature importance:

![](./rf_feature_importance_top10.png)

