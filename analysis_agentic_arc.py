from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from lifelines import CoxPHFitter
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.metrics import silhouette_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "Dataset" / "agentic_ai_performance_dataset_20250622.csv"
OUT_DIR = ROOT / "outputs"


NUM_COLS_CORE = [
    "autonomy_level",
    "success_rate",
    "accuracy_score",
    "efficiency_score",
    "execution_time_seconds",
    "response_latency_ms",
    "memory_usage_mb",
    "cpu_usage_percent",
    "cost_per_task_cents",
    "error_recovery_rate",
    "privacy_compliance_score",
    "bias_detection_score",
    "data_quality_score",
    "performance_index",
    "cost_efficiency_ratio",
    "autonomous_capability_score",
    "task_complexity",
]


CAT_COLS = [
    "agent_type",
    "model_architecture",
    "deployment_environment",
    "task_category",
    "multimodal_capability",
    "edge_compatibility",
]


def _coerce_bool_series(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    return (
        s.astype(str)
        .str.strip()
        .str.upper()
        .map({"TRUE": True, "FALSE": False, "1": True, "0": False, "YES": True, "NO": False})
    )


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    # Coerce known boolean fields.
    for col in ["human_intervention_required", "multimodal_capability", "edge_compatibility"]:
        if col in df.columns:
            df[col] = _coerce_bool_series(df[col])

    # Timestamp parsing (day-first format in sample).
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", dayfirst=True)

    # Numeric coercion for core numeric fields.
    for col in NUM_COLS_CORE:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


@dataclass(frozen=True)
class TestResult:
    name: str
    n: int
    details: dict


def save_table(df: pd.DataFrame, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_DIR / f"{name}.csv", index=True)


def save_json(obj: dict, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{name}.json").write_text(json.dumps(obj, indent=2), encoding="utf-8")


def fig_save(name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUT_DIR / f"{name}.png", dpi=200)
    plt.close()


def eda_overview(df: pd.DataFrame) -> dict:
    overview = {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "missing_by_col": df.isna().sum().sort_values(ascending=False).head(25).to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }
    return overview


def correlation_block(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in NUM_COLS_CORE if c in df.columns]
    corr = df[cols].corr(numeric_only=True)
    corr_sorted = corr.loc["success_rate"].sort_values(ascending=False).to_frame("corr_with_success_rate")
    save_table(corr_sorted, "corr_with_success_rate")
    return corr


def plot_governance_boundary(df: pd.DataFrame) -> None:
    d = df.dropna(subset=["autonomy_level", "success_rate", "human_intervention_required"]).copy()
    plt.figure(figsize=(9, 6))
    sns.scatterplot(
        data=d,
        x="autonomy_level",
        y="success_rate",
        hue="human_intervention_required",
        alpha=0.5,
        palette={True: "#d62728", False: "#2ca02c"},
    )
    plt.axhline(0.6, linestyle="--", color="black", linewidth=1, label="success_rate=0.6")
    plt.title("Governance boundary view: autonomy vs success")
    plt.legend(title="intervention_required", loc="best")
    fig_save("governance_boundary_autonomy_success")


def kmeans_clustering(df: pd.DataFrame, k_candidates=(2, 3, 4, 5, 6)) -> dict:
    feat_cols = [c for c in ["performance_index", "autonomous_capability_score", "accuracy_score"] if c in df.columns]
    d = df.dropna(subset=feat_cols).copy()
    X = StandardScaler().fit_transform(d[feat_cols].to_numpy())
    best = None
    scores = {}
    for k in k_candidates:
        km = KMeans(n_clusters=k, n_init="auto", random_state=42)
        labels = km.fit_predict(X)
        sil = silhouette_score(X, labels) if k > 1 else float("nan")
        scores[int(k)] = float(sil)
        if best is None or sil > best["silhouette"]:
            best = {"k": int(k), "silhouette": float(sil), "model": km, "labels": labels}

    d = d.assign(cluster=best["labels"])
    # Cluster profiling.
    prof = (
        d.groupby("cluster")[feat_cols + ["success_rate", "privacy_compliance_score", "bias_detection_score"]]
        .mean(numeric_only=True)
        .sort_index()
    )
    save_table(prof, "cluster_profile_means")

    # Plot in 2D: capability vs accuracy; hue cluster, size performance.
    plt.figure(figsize=(9, 6))
    sns.scatterplot(
        data=d,
        x="autonomous_capability_score",
        y="accuracy_score",
        hue="cluster",
        size="performance_index",
        sizes=(10, 120),
        alpha=0.6,
        palette="tab10",
    )
    plt.title(f"K-Means clustering (k={best['k']}, silhouette={best['silhouette']:.3f})")
    fig_save("kmeans_clusters_capability_accuracy")

    return {"features": feat_cols, "silhouette_by_k": scores, "best_k": best["k"], "best_silhouette": best["silhouette"]}


def anova_by_task_category(df: pd.DataFrame) -> TestResult:
    needed = ["accuracy_score", "task_category"]
    d = df.dropna(subset=needed).copy()
    # OLS with categorical predictor.
    model = smf.ols("accuracy_score ~ C(task_category)", data=d).fit()
    aov = sm.stats.anova_lm(model, typ=2)
    save_table(aov, "anova_accuracy_by_task_category")

    # Effect size (eta squared) = SS_effect / SS_total.
    ss_effect = float(aov.loc["C(task_category)", "sum_sq"])
    ss_total = float(aov["sum_sq"].sum())
    eta2 = ss_effect / ss_total if ss_total > 0 else float("nan")

    return TestResult(
        name="ANOVA accuracy_score by task_category",
        n=int(d.shape[0]),
        details={
            "F": float(aov.loc["C(task_category)", "F"]),
            "p": float(aov.loc["C(task_category)", "PR(>F)"]),
            "eta_squared": float(eta2),
            "categories": int(d["task_category"].nunique()),
        },
    )


def ttest_performance_trust_gap(df: pd.DataFrame) -> TestResult:
    d = df.dropna(subset=["performance_index", "human_intervention_required"]).copy()
    a = d.loc[d["human_intervention_required"] == False, "performance_index"]  # noqa: E712
    b = d.loc[d["human_intervention_required"] == True, "performance_index"]  # noqa: E712
    # Welch t-test.
    t, p = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
    # Effect size: Cohen's d (using pooled SD with Welch approximation is messy; use Hedges g-ish via pooled SD).
    sa, sb = a.std(ddof=1), b.std(ddof=1)
    na, nb = len(a), len(b)
    sp = math.sqrt(((na - 1) * sa**2 + (nb - 1) * sb**2) / (na + nb - 2)) if na + nb > 2 else float("nan")
    d_eff = float((a.mean() - b.mean()) / sp) if sp and sp > 0 else float("nan")
    return TestResult(
        name="Welch t-test: performance_index by intervention_required",
        n=int(d.shape[0]),
        details={
            "mean_no_intervention": float(a.mean()),
            "mean_requires_intervention": float(b.mean()),
            "t": float(t),
            "p": float(p),
            "cohens_d_approx": d_eff,
            "n_no_intervention": int(na),
            "n_requires_intervention": int(nb),
        },
    )


def logistic_regression_accountability(df: pd.DataFrame) -> TestResult:
    # Predict human_intervention_required from autonomy_level and task_complexity (+ sensible controls).
    cols = [
        "human_intervention_required",
        "autonomy_level",
        "task_complexity",
        "accuracy_score",
        "privacy_compliance_score",
        "deployment_environment",
        "task_category",
    ]
    cols = [c for c in cols if c in df.columns]
    d = df.dropna(subset=cols).copy()
    # Ensure boolean target is 0/1.
    y = d["human_intervention_required"].astype(bool).astype(int)
    X = d.drop(columns=["human_intervention_required"])

    num_cols = [c for c in X.columns if pd.api.types.is_numeric_dtype(X[c])]
    cat_cols = [c for c in X.columns if c not in num_cols]

    pre = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )
    # statsmodels for interpretability: build formula with categorical handling.
    # We'll use a GLM Binomial to avoid perfect-separation headaches where possible.
    formula = "human_intervention_required ~ autonomy_level + task_complexity + accuracy_score + privacy_compliance_score"
    if "deployment_environment" in d.columns:
        formula += " + C(deployment_environment)"
    if "task_category" in d.columns:
        formula += " + C(task_category)"
    glm = smf.glm(formula=formula, data=d.assign(human_intervention_required=y), family=sm.families.Binomial()).fit()

    # Also compute a simple cross-validated AUC-ish proxy via sklearn (ROC AUC).
    from sklearn.linear_model import LogisticRegression

    clf = LogisticRegression(max_iter=2000)
    pipe = Pipeline([("pre", pre), ("clf", clf)])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    # scikit-learn's built-in scorer avoids version-specific scorer kwargs.
    auc = cross_val_score(pipe, X, y, scoring="roc_auc", cv=cv)

    params = glm.params.to_dict()
    pvals = glm.pvalues.to_dict()
    # Convert key coefficients to odds ratios.
    odds = {k: float(np.exp(v)) for k, v in params.items()}

    # Save full summary for dissertation appendix.
    (OUT_DIR / "logit_glm_summary.txt").write_text(str(glm.summary()), encoding="utf-8")

    return TestResult(
        name="Logistic regression: accountability proxy (intervention_required)",
        n=int(d.shape[0]),
        details={
            "n_features_numeric": int(len(num_cols)),
            "n_features_categorical": int(len(cat_cols)),
            "cv_auc_mean": float(np.mean(auc)),
            "cv_auc_std": float(np.std(auc)),
            "odds_ratios_key": {k: odds[k] for k in odds.keys() if k in ["Intercept", "autonomy_level", "task_complexity", "accuracy_score", "privacy_compliance_score"]},
            "p_values_key": {k: float(pvals[k]) for k in pvals.keys() if k in ["autonomy_level", "task_complexity", "accuracy_score", "privacy_compliance_score"]},
        },
    )


def trust_threshold_models(df: pd.DataFrame) -> dict:
    # Decision tree / random forest to find thresholds where intervention becomes necessary.
    feat_cols = [
        "accuracy_score",
        "error_recovery_rate",
        "autonomy_level",
        "task_complexity",
        "privacy_compliance_score",
        "response_latency_ms",
        "performance_index",
    ]
    feat_cols = [c for c in feat_cols if c in df.columns]
    d = df.dropna(subset=feat_cols + ["human_intervention_required"]).copy()
    y = d["human_intervention_required"].astype(bool).astype(int)
    X = d[feat_cols]

    # Simple interpretable tree (shallow).
    tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=50, random_state=42)
    tree.fit(X, y)

    # Random forest for robustness.
    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=20,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )
    rf.fit(X, y)
    importances = pd.Series(rf.feature_importances_, index=feat_cols).sort_values(ascending=False)
    save_table(importances.to_frame("rf_feature_importance"), "rf_feature_importance")

    # Plot top importances.
    plt.figure(figsize=(8, 5))
    sns.barplot(x=importances.values[:10], y=importances.index[:10], color="#4c72b0")
    plt.title("Random Forest feature importance (top 10)")
    plt.xlabel("importance")
    plt.ylabel("")
    fig_save("rf_feature_importance_top10")

    # Extract a few human-readable thresholds from tree.
    # We'll walk the tree structure and record splits.
    t = tree.tree_
    feature_names = feat_cols

    def recurse(node: int, path: list[dict]) -> list[list[dict]]:
        if t.feature[node] == -2:  # leaf
            return [path + [{"leaf": True, "value": t.value[node][0].tolist()}]]
        feat = feature_names[t.feature[node]]
        thr = float(t.threshold[node])
        left = recurse(t.children_left[node], path + [{"feature": feat, "op": "<=", "threshold": thr}])
        right = recurse(t.children_right[node], path + [{"feature": feat, "op": ">", "threshold": thr}])
        return left + right

    paths = recurse(0, [])
    # Keep the top few leaves with the highest predicted intervention probability.
    leaf_summaries = []
    for p in paths:
        leaf = p[-1]
        if not leaf.get("leaf"):
            continue
        counts = np.array(leaf["value"], dtype=float)
        prob = float(counts[1] / counts.sum()) if counts.sum() > 0 else float("nan")
        leaf_summaries.append({"path": p[:-1], "p_intervention": prob, "counts": leaf["value"]})
    leaf_summaries.sort(key=lambda x: x["p_intervention"], reverse=True)
    top_rules = leaf_summaries[:6]
    save_json({"top_tree_rules": top_rules}, "tree_threshold_rules")

    return {
        "n": int(d.shape[0]),
        "features": feat_cols,
        "tree_depth": int(tree.get_depth()),
        "top_rules_saved": "outputs/tree_threshold_rules.json",
        "rf_importance_saved": "outputs/rf_feature_importance.csv",
    }


def sensitivity_privacy_latency(df: pd.DataFrame) -> TestResult:
    # Does higher privacy compliance (proxy for stronger privacy controls) trade off latency?
    cols = ["response_latency_ms", "privacy_compliance_score", "deployment_environment"]
    cols = [c for c in cols if c in df.columns]
    d = df.dropna(subset=cols).copy()
    # Use log-latency to reduce skew; add environment controls.
    d["log_latency"] = np.log1p(d["response_latency_ms"])
    formula = "log_latency ~ privacy_compliance_score"
    if "deployment_environment" in d.columns:
        formula += " + C(deployment_environment)"
    model = smf.ols(formula, data=d).fit()
    (OUT_DIR / "privacy_latency_ols_summary.txt").write_text(str(model.summary()), encoding="utf-8")
    return TestResult(
        name="Sensitivity: privacy_compliance_score vs response_latency_ms (log)",
        n=int(d.shape[0]),
        details={
            "coef_privacy": float(model.params.get("privacy_compliance_score", np.nan)),
            "p_privacy": float(model.pvalues.get("privacy_compliance_score", np.nan)),
            "r2": float(model.rsquared),
        },
    )


def survival_time_to_failure(df: pd.DataFrame, acc_threshold: float = 0.6) -> dict:
    # Define "failure event" as accuracy_score < threshold.
    cols = ["execution_time_seconds", "accuracy_score", "autonomy_level", "task_complexity", "privacy_compliance_score"]
    cols = [c for c in cols if c in df.columns]
    d = df.dropna(subset=cols).copy()
    d = d.rename(columns={"execution_time_seconds": "time"})
    d["event"] = (d["accuracy_score"] < acc_threshold).astype(int)
    # Cox model (proportional hazards): how autonomy/complexity/privacy relate to hazard of failure.
    cph = CoxPHFitter()
    covars = ["autonomy_level", "task_complexity", "privacy_compliance_score"]
    cph.fit(d[["time", "event"] + covars], duration_col="time", event_col="event")
    (OUT_DIR / "cox_survival_summary.txt").write_text(str(cph.summary), encoding="utf-8")
    # Save hazard ratios.
    hr = (np.exp(cph.params_)).to_dict()
    return {"n": int(d.shape[0]), "acc_threshold": acc_threshold, "hazard_ratios": {k: float(v) for k, v in hr.items()}}


def hotl_circuit_breaker_simulation(df: pd.DataFrame) -> TestResult:
    """
    Counterfactual "after HOTL circuit breaker" simulation:
    - Define a breaker condition (low accuracy or weak recovery) at high autonomy/high complexity.
    - For triggered cases, assume HOTL moves them into an "intervened" regime by imputing
      success_rate/accuracy_score from comparable already-intervened cases (same task_category & complexity bin).

    This yields paired before/after values for hypothesis tests.
    """
    cols = [
        "task_category",
        "task_complexity",
        "autonomy_level",
        "accuracy_score",
        "success_rate",
        "error_recovery_rate",
        "human_intervention_required",
    ]
    d = df.dropna(subset=[c for c in cols if c in df.columns]).copy()

    # Define breaker triggers (tunable).
    trig = (
        (d["autonomy_level"] >= 7)
        & (d["task_complexity"] >= 7)
        & ((d["accuracy_score"] < 0.6) | (d["error_recovery_rate"] < 0.55))
    )
    d["breaker_triggers"] = trig

    # Complexity bin (for matching comparables).
    d["complexity_bin"] = pd.cut(d["task_complexity"], bins=[0, 3, 6, 10], labels=["low", "mid", "high"], include_lowest=True)

    # Create counterfactual after-values via regression adjustment (avoids bias from "intervened"
    # cases being systematically harder tasks).
    after_accuracy = d["accuracy_score"].copy()
    after_success = d["success_rate"].copy()

    # Fit outcome models with controls + intervention indicator.
    # Interpret the intervention coefficient as an average "uplift" under HOTL governance.
    base_controls = []
    for c in ["autonomy_level", "task_complexity", "error_recovery_rate", "privacy_compliance_score"]:
        if c in d.columns:
            base_controls.append(c)

    formula_controls = " + ".join(base_controls) if base_controls else "1"
    if "task_category" in d.columns:
        formula_controls += " + C(task_category)"
    if "deployment_environment" in d.columns:
        formula_controls += " + C(deployment_environment)"
    if "model_architecture" in d.columns:
        formula_controls += " + C(model_architecture)"

    acc_model = smf.ols(f"accuracy_score ~ human_intervention_required + {formula_controls}", data=d).fit(cov_type="HC3")
    succ_model = smf.ols(f"success_rate ~ human_intervention_required + {formula_controls}", data=d).fit(cov_type="HC3")
    (OUT_DIR / "hotl_outcome_model_accuracy.txt").write_text(str(acc_model.summary()), encoding="utf-8")
    (OUT_DIR / "hotl_outcome_model_success.txt").write_text(str(succ_model.summary()), encoding="utf-8")

    uplift_acc = float(acc_model.params.get("human_intervention_required[T.True]", acc_model.params.get("human_intervention_required", 0.0)))
    uplift_succ = float(succ_model.params.get("human_intervention_required[T.True]", succ_model.params.get("human_intervention_required", 0.0)))

    # Apply only to triggered cases: assume HOTL flips them into "intervened" regime and adds uplift.
    idx = d.index[d["breaker_triggers"]].tolist()
    after_accuracy.loc[idx] = np.clip(after_accuracy.loc[idx] + uplift_acc, 0.0, 1.0)
    after_success.loc[idx] = np.clip(after_success.loc[idx] + uplift_succ, 0.0, 1.0)

    # Paired tests over triggered subset.
    before_acc = d.loc[idx, "accuracy_score"]
    after_acc_t = after_accuracy.loc[idx]
    before_succ = d.loc[idx, "success_rate"]
    after_succ_t = after_success.loc[idx]

    # Use Wilcoxon signed-rank if non-normal; also provide paired t-test.
    t_acc = stats.ttest_rel(after_acc_t, before_acc, nan_policy="omit")
    w_acc = stats.wilcoxon(after_acc_t - before_acc, zero_method="wilcox", correction=False, alternative="greater")
    t_succ = stats.ttest_rel(after_succ_t, before_succ, nan_policy="omit")
    w_succ = stats.wilcoxon(after_succ_t - before_succ, zero_method="wilcox", correction=False, alternative="greater")

    # Save a small audit sample.
    audit = d.loc[idx, ["agent_id", "task_category", "task_complexity", "autonomy_level", "accuracy_score", "success_rate"]].copy()
    audit["after_accuracy_score"] = after_acc_t.values
    audit["after_success_rate"] = after_succ_t.values
    save_table(audit.head(200), "hotl_sim_audit_head200")

    return TestResult(
        name="HOTL circuit-breaker simulation (triggered subset)",
        n=int(len(idx)),
        details={
            "trigger_rate": float(d["breaker_triggers"].mean()),
            "estimated_uplift": {"accuracy": uplift_acc, "success": uplift_succ},
            "paired_t_accuracy": {"t": float(t_acc.statistic), "p": float(t_acc.pvalue)},
            "wilcoxon_accuracy_greater": {"stat": float(w_acc.statistic), "p": float(w_acc.pvalue)},
            "paired_t_success": {"t": float(t_succ.statistic), "p": float(t_succ.pvalue)},
            "wilcoxon_success_greater": {"stat": float(w_succ.statistic), "p": float(w_succ.pvalue)},
            "before_means": {"accuracy": float(before_acc.mean()), "success": float(before_succ.mean())},
            "after_means": {"accuracy": float(after_acc_t.mean()), "success": float(after_succ_t.mean())},
        },
    )


def main() -> None:
    sns.set_theme(style="whitegrid")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()

    # 0) EDA: overview + basic plots.
    overview = eda_overview(df)
    save_json(overview, "eda_overview")

    corr = correlation_block(df)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, cmap="vlag", center=0, linewidths=0.5)
    plt.title("Correlation matrix (core numeric features)")
    fig_save("corr_heatmap_core")

    plot_governance_boundary(df)

    # 1) RQ1: capabilities & failure modes.
    cluster_info = kmeans_clustering(df)
    save_json(cluster_info, "kmeans_summary")

    anova_res = anova_by_task_category(df)
    save_json(asdict(anova_res), "anova_accuracy_task_category")

    # 2) RQ2: accountability proxy regression + privacy/latency sensitivity.
    logit_res = logistic_regression_accountability(df)
    save_json(asdict(logit_res), "logit_accountability")

    privacy_latency = sensitivity_privacy_latency(df)
    save_json(asdict(privacy_latency), "sensitivity_privacy_latency")

    # 3) RQ3: critical trust thresholds.
    gap_res = ttest_performance_trust_gap(df)
    save_json(asdict(gap_res), "trust_gap_ttest")

    thr_models = trust_threshold_models(df)
    save_json(thr_models, "trust_threshold_models")

    # 4) RQ4: framework effectiveness simulation + survival analysis.
    hotl_res = hotl_circuit_breaker_simulation(df)
    save_json(asdict(hotl_res), "hotl_sim_tests")

    surv = survival_time_to_failure(df, acc_threshold=0.6)
    save_json(surv, "survival_cox")

    # Create a human-readable markdown report.
    report_lines = []
    report_lines.append("# Agentic ARC analysis report\n")
    report_lines.append(f"- Dataset: `{DATA_PATH.as_posix()}`\n")
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

    (OUT_DIR / "REPORT.md").write_text("".join(report_lines), encoding="utf-8")

    print("Done. See outputs/REPORT.md and outputs/*.png/*.csv/*.json")


if __name__ == "__main__":
    main()

