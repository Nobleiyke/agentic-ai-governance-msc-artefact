from __future__ import annotations

"""
Main runner for `analysis_agentic_arc.py`.

- Leaves `analysis_agentic_arc.py` unchanged.
- Prints progress checkpoints + timings.
- Reuses the original module's functions and output paths.
"""

import time
from dataclasses import asdict

import matplotlib.pyplot as plt
import seaborn as sns

import analysis_agentic_arc as arc


def checkpoint(msg: str, started: float, last: float) -> float:
    now = time.perf_counter()
    total = now - started
    step = now - last
    print(f"[{total:6.1f}s | +{step:5.1f}s] {msg}", flush=True)
    return now


def main() -> None:
    started = time.perf_counter() 
    last = started

    print("Agentic ARC analysis (main)", flush=True)
    last = checkpoint("Setting seaborn theme", started, last)
    sns.set_theme(style="whitegrid")
    arc.OUT_DIR.mkdir(parents=True, exist_ok=True)

    last = checkpoint(f"Loading dataset: {arc.DATA_PATH}", started, last)
    df = arc.load_data()
    last = checkpoint(f"Loaded data: rows={df.shape[0]} cols={df.shape[1]}", started, last)

    last = checkpoint("EDA overview + correlation outputs", started, last)
    overview = arc.eda_overview(df)
    arc.save_json(overview, "eda_overview")

    corr = arc.correlation_block(df)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, cmap="vlag", center=0, linewidths=0.5)
    plt.title("Correlation matrix (core numeric features)")
    arc.fig_save("corr_heatmap_core")

    last = checkpoint("Plotting governance boundary figure", started, last)
    arc.plot_governance_boundary(df)

    last = checkpoint("RQ1: Running clustering", started, last)
    cluster_info = arc.kmeans_clustering(df)
    arc.save_json(cluster_info, "kmeans_summary")

    last = checkpoint("RQ1: Running ANOVA (accuracy by task category)", started, last)
    anova_res = arc.anova_by_task_category(df)
    arc.save_json(asdict(anova_res), "anova_accuracy_task_category")

    last = checkpoint("RQ2: Logistic regression (intervention_required)", started, last)
    logit_res = arc.logistic_regression_accountability(df)
    arc.save_json(asdict(logit_res), "logit_accountability")

    last = checkpoint("RQ2: Privacy-latency sensitivity model", started, last)
    privacy_latency = arc.sensitivity_privacy_latency(df)
    arc.save_json(asdict(privacy_latency), "sensitivity_privacy_latency")

    last = checkpoint("RQ3: Trust gap t-test", started, last)
    gap_res = arc.ttest_performance_trust_gap(df)
    arc.save_json(asdict(gap_res), "trust_gap_ttest")

    last = checkpoint("RQ3: Threshold models (tree + random forest)", started, last)
    thr_models = arc.trust_threshold_models(df)
    arc.save_json(thr_models, "trust_threshold_models")

    last = checkpoint("RQ4: HOTL circuit-breaker simulation", started, last)
    hotl_res = arc.hotl_circuit_breaker_simulation(df)
    arc.save_json(asdict(hotl_res), "hotl_sim_tests")

    last = checkpoint("Survival: Cox model", started, last)
    surv = arc.survival_time_to_failure(df, acc_threshold=0.6)
    arc.save_json(surv, "survival_cox")

    last = checkpoint("Writing outputs/REPORT.md summary", started, last)
    report_lines = []
    report_lines.append("# Agentic ARC analysis report\n")
    report_lines.append(f"- Dataset: `{arc.DATA_PATH.as_posix()}`\n")
    report_lines.append(f"- Rows: **{overview['rows']}**, Cols: **{overview['cols']}**\n")
    report_lines.append("\n## EDA\n")
    report_lines.append("- Missingness (top 10 columns):\n")
    for k, v in list(overview["missing_by_col"].items())[:10]:
        report_lines.append(f"  - {k}: {v}\n")
    report_lines.append("\n## RQ1: Capabilities & failure modes\n")
    report_lines.append(f"- K-Means best k: **{cluster_info['best_k']}** (silhouette={cluster_info['best_silhouette']:.3f}).\n")
    report_lines.append("- Saved: `outputs/cluster_profile_means.csv`, `outputs/kmeans_clusters_capability_accuracy.png`.\n")
    report_lines.append(
        f"- ANOVA accuracy by task_category: F={anova_res.details['F']:.3f}, p={anova_res.details['p']:.3g}, eta²={anova_res.details['eta_squared']:.3f}.\n"
    )
    report_lines.append("- Saved: `outputs/anova_accuracy_by_task_category.csv`.\n")
    report_lines.append("\n## RQ2: Accountability + privacy trade-offs\n")
    report_lines.append(
        f"- Logistic regression (intervention_required): CV AUC={logit_res.details['cv_auc_mean']:.3f}±{logit_res.details['cv_auc_std']:.3f}.\n"
    )
    report_lines.append(f"- Key odds ratios: {logit_res.details['odds_ratios_key']}\n")
    report_lines.append(f"- Key p-values: {logit_res.details['p_values_key']}\n")
    report_lines.append("- Saved: `outputs/logit_glm_summary.txt`.\n")
    report_lines.append(
        f"- Privacy↔latency (log): coef={privacy_latency.details['coef_privacy']:.4f}, p={privacy_latency.details['p_privacy']:.3g}, R²={privacy_latency.details['r2']:.3f}.\n"
    )
    report_lines.append("- Saved: `outputs/privacy_latency_ols_summary.txt`.\n")
    report_lines.append("\n## RQ3: Critical trust thresholds (HOTL triggers)\n")
    report_lines.append(
        f"- Trust gap t-test (performance_index): mean(no intervention)={gap_res.details['mean_no_intervention']:.4f}, "
        f"mean(requires)={gap_res.details['mean_requires_intervention']:.4f}, p={gap_res.details['p']:.3g}.\n"
    )
    report_lines.append("- Threshold rules: `outputs/tree_threshold_rules.json`.\n")
    report_lines.append("- Feature importance: `outputs/rf_feature_importance.csv`, `outputs/rf_feature_importance_top10.png`.\n")
    report_lines.append("\n## RQ4: Framework effectiveness simulation\n")
    report_lines.append(
        f"- Circuit-breaker triggered subset n={hotl_res.n} (trigger_rate={hotl_res.details['trigger_rate']:.3f}).\n"
    )
    report_lines.append(
        f"- Accuracy before→after: {hotl_res.details['before_means']['accuracy']:.3f}→{hotl_res.details['after_means']['accuracy']:.3f}; "
        f"Wilcoxon(p)={hotl_res.details['wilcoxon_accuracy_greater']['p']:.3g}.\n"
    )
    report_lines.append(
        f"- Success before→after: {hotl_res.details['before_means']['success']:.3f}→{hotl_res.details['after_means']['success']:.3f}; "
        f"Wilcoxon(p)={hotl_res.details['wilcoxon_success_greater']['p']:.3g}.\n"
    )
    report_lines.append("- Audit sample: `outputs/hotl_sim_audit_head200.csv`.\n")
    report_lines.append("\n## Survival analysis\n")
    report_lines.append(
        f"- Cox model (event=accuracy<{surv['acc_threshold']}): hazard ratios={surv['hazard_ratios']}.\n"
    )
    report_lines.append("- Saved: `outputs/cox_survival_summary.txt`.\n")

    (arc.OUT_DIR / "REPORT.md").write_text("".join(report_lines), encoding="utf-8")

    last = checkpoint("All done. Outputs written to outputs/", started, last)
    print("Done. See outputs/REPORT.md and outputs/*.png/*.csv/*.json", flush=True)


if __name__ == "__main__":
    main()

