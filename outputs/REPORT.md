# Agentic ARC analysis report
- Dataset: `C:/Users/User/Downloads/cve-bench-main/Dataset/agentic_ai_performance_dataset_20250622.csv`
- Rows: **5000**, Cols: **26**

## EDA
- Missingness (top 10 columns):
  - agent_id: 0
  - agent_type: 0
  - model_architecture: 0
  - deployment_environment: 0
  - task_category: 0
  - task_complexity: 0
  - autonomy_level: 0
  - success_rate: 0
  - accuracy_score: 0
  - efficiency_score: 0

## RQ1: Capabilities & failure modes
- K-Means best k: **2** (silhouette=0.428).
- Saved: `outputs/cluster_profile_means.csv`, `outputs/kmeans_clusters_capability_accuracy.png`.
- ANOVA accuracy by task_category: F=362.483, p=0, eta²=0.395.
- Saved: `outputs/anova_accuracy_by_task_category.csv`.

## RQ2: Accountability + privacy trade-offs
- Logistic regression (intervention_required): CV AUC=1.000±0.000.
- Key odds ratios: {'Intercept': 3.599873857531763, 'autonomy_level': 0.9883504742917059, 'task_complexity': 7.6207673998464305, 'accuracy_score': 4.871190005526726e-05, 'privacy_compliance_score': 0.4075137048316925}
- Key p-values: {'autonomy_level': 0.8232473043093156, 'task_complexity': 1.6178748446514258e-41, 'accuracy_score': 3.7534018740112005e-10, 'privacy_compliance_score': 0.3169632381654621}
- Saved: `outputs/logit_glm_summary.txt`.
- Privacy↔latency (log): coef=-0.1887, p=0.212, R²=0.003.
- Saved: `outputs/privacy_latency_ols_summary.txt`.

## RQ3: Critical trust thresholds (HOTL triggers)
- Trust gap t-test (performance_index): mean(no intervention)=0.7680, mean(requires)=0.5141, p=0.
- Threshold rules: `outputs/tree_threshold_rules.json`.
- Feature importance: `outputs/rf_feature_importance.csv`, `outputs/rf_feature_importance_top10.png`.

## RQ4: Framework effectiveness simulation
- Circuit-breaker triggered subset n=1693 (trigger_rate=0.339).
- Accuracy before→after: 0.448→0.435; Wilcoxon(p)=1.
- Success before→after: 0.336→0.297; Wilcoxon(p)=1.
- Audit sample: `outputs/hotl_sim_audit_head200.csv`.

## Survival analysis
- Cox model (event=accuracy<0.6): hazard ratios={'autonomy_level': 1.0276883841645719, 'task_complexity': 1.0454722059353798, 'privacy_compliance_score': 0.7234005743905054}.
- Saved: `outputs/cox_survival_summary.txt`.
