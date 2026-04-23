# Full Project Report (ARC × CVE-Bench) — Findings to Date

- **Workspace**: `c:\Users\User\Downloads\cve-bench-main`
- **Date**: 2026-04-15 (updated; quantitative figures unchanged from 2026-04-09 unless re-run)
- **Status note**: **CVE-Bench Inspect `.eval` logs are stored** under `cve-bench-main/logs/` and `cve-bench-main/src/logs/`, with inventory `outputs/CVE_BENCH_EVAL_INVENTORY.json`. Coverage is **partial** (see V2 report for the full CVE-Bench section).

---

## Summary (plain English)

### What this project is about (in one paragraph)
This project studies **why AI “agents” can become risky** when they are given powerful abilities (for example: **browsing the web**, **reading/writing files**, or **running code**). The goal is to identify **which abilities are most associated with which kinds of problems**, and to present the evidence in a way that is easy to understand and defend academically.

### The three simple ideas I used
I organised everything using three buckets:

- **What the agent can do (Capabilities)**: e.g., web search, file access, code execution.
- **How it goes wrong (Failure Modes)**: e.g., the agent makes a mistake, a malicious website tricks it (prompt injection), or a tool fails.
- **What damage it causes (Hazards/Impacts)**: e.g., security breach, privacy leak, breaking an application, disrupting infrastructure.

### What I produced (outputs you can show to a supervisor)
- **NVivo-ready codebook**: a fixed set of codes so the document analysis is consistent and repeatable.
- **“Overlap tables” (from NVivo Matrix Coding Queries)**: these show where a capability and a risk appear together in the same evidence snippet.
- **Statistical results + graphs** (already generated in `outputs/`): these show patterns in a 5,000-row dataset (e.g., which task types have much lower accuracy; what predicts “human intervention required”).
- **CVE-Bench logs (partial)**: see **`outputs/FULL_REPORT_V2.md`** § “CVE-Bench empirical runs” and `outputs/CVE_BENCH_EVAL_INVENTORY.json`.

---

## Research questions alignment (plain English)

You can describe the project to your supervisor like this:

- **I built a practical method** (a codebook + query steps) to turn text evidence into structured results.
- **I used that method on four authoritative PDFs** to systematically extract capability–risk connections.
- **I also ran statistical analysis** on a 5,000-row dataset to support (or challenge) the same story with numbers and graphs.

---

## Data sources used (current state)

### 1) Documents (qualitative secondary data, for NVivo coding)
Located in `Dataset/`:

- `2025_Insider_AI_Threat_Report.pdf`
- `AIGN-Agentic-AI-Governance-Framework-1.0.pdf`
- `Introducing the Agentic Risk & Capability Framework.pdf`
- `The Al Risk Repository.pdf`

### 2) Structured dataset (quantitative)
- `Dataset/agentic_ai_performance_dataset_20250622.csv`
  - **Rows**: 5,000
  - **Columns**: 26
  - Generated statistical outputs are in `outputs/` (see figures and tables below).

### 3) CVE-bench logs (empirical benchmark traces)
- **Present** as `.eval` files; see **`outputs/FULL_REPORT_V2.md`** for the outcome table and interpretation.

---

## Methodology Part A — NVivo (simple explanation)

### Step 1: Make the code folders (once)
In NVivo I create three top-level code folders:

1) **Capabilities** (what the agent can do)  
2) **Root Causes / Failure Modes** (how it goes wrong)  
3) **Hazards / Impacts** (what damage happens)

This is already packaged as importable file:
- `nvivo/ARC_codebook_core.csv`

### Step 2: Code the PDFs (what to do while reading)
When I highlight a sentence/paragraph that describes a risk story, I code that *same* highlight to:

- **A capability** (e.g., “Internet & Search Access”)
- **A failure mode** (e.g., “External Manipulation (Prompt Injection)”)
- **A hazard/impact** (e.g., “Security”)

This is not “extra work”—it’s how we keep the evidence linked.

### What “simultaneous coding” means (one clear example)
If the text says: *the agent searched the web and a malicious page injected instructions*, I code the same highlighted text to:

- `Internet & Search Access` (capability)
- `External Manipulation (Prompt Injection)` (failure mode)
- `Security` (hazard) (and/or `Data Privacy` if the text mentions leakage)

### Step 3: Turn coding into “results tables” (Matrix Coding Query)
After coding, NVivo can automatically count overlaps and produce tables:

1) **Which capabilities are most often involved in which failure modes?**  
   (Capability × Failure Mode)

2) **Which capabilities are most often linked to which harms?**  
   (Capability × Hazard/Impact)

These tables are your “high-density intersections”.

**Plain meaning:** a high number in a cell means:  
“I repeatedly found evidence where this capability and this risk type appear together in the same incident description.”

---

## Process I followed (what I did, step-by-step)

This is the practical workflow I followed to get from “project idea” to “results you can show”.

### Phase 1: Set up the project and evidence
- Collected **four authoritative PDFs** into `Dataset/` (industry report + governance framework + ARC framework + AI risk taxonomy).
- Confirmed the project would use **deductive coding** (pre-defined codes) based on ARC.
- Confirmed the quantitative dataset was available: `Dataset/agentic_ai_performance_dataset_20250622.csv` (5,000 rows).

### Phase 2: Build the NVivo codebook (so coding is consistent)
- Created an ARC-based codebook with three “folders”:
  - **Capabilities** (what the agent can do)
  - **Failure Modes** (how it goes wrong)
  - **Hazards/Impacts** (what damage happens)
- Prepared NVivo-importable codebook file so the hierarchy can be imported quickly and consistently:
  - `nvivo/ARC_codebook_core.csv`

### Phase 3: Code the PDFs in NVivo (deductive + simultaneous coding)
- Imported the PDFs into NVivo 13.
- Read through each PDF and highlighted only the relevant sentences/paragraphs.
- For each highlighted excerpt, applied **multiple codes to the same text** where appropriate:
  - a capability (e.g., web access)
  - a failure mode (e.g., prompt injection)
  - a hazard (e.g., security or privacy)
- This creates evidence that can later be counted as “overlaps”.

### Phase 4: Turn coded evidence into tables (your “intersection density”)
- Ran **Matrix Coding Queries** in NVivo to produce overlap tables such as:
  - Capability × Failure Mode
  - Capability × Hazard/Impact
- Exported those tables (CSV/Excel) to use directly in the dissertation (risk register + prioritisation tables).

### Phase 5: Run statistical analysis and generate figures (quantitative support)
- Ran the Python analysis script `analysis_agentic_arc.py` over the 5,000-row dataset.
- Generated and saved:
  - model summaries (`*.txt`)
  - results (`*.json`)
  - tables (`*.csv`)
  - figures (`*.png`)
  - plus a short summary: `outputs/REPORT.md`

### Phase 6: Write the combined report (what you are reading now)
- Combined the qualitative method + quantitative outputs into one narrative report.
- **CVE-Bench**: logs in repo; see V2 report for details.

---

## Software/tools used (including for your viva)

### For qualitative analysis (coding + queries)
- **NVivo 13**: importing PDFs, coding, simultaneous coding, and Matrix Coding Queries.

### For quantitative/statistical analysis
- **Python** (script: `analysis_agentic_arc.py`) with:
  - **pandas/numpy** (data handling)
  - **matplotlib/seaborn** (figures in `outputs/*.png`)
  - **statsmodels/scipy** (regression and hypothesis tests)
  - **scikit-learn** (clustering, CV AUC)
  - **lifelines** (Cox survival model)

### For writing the dissertation artifacts
- **Markdown** reports:
  - `outputs/REPORT.md` (auto-generated summary)
  - `outputs/FULL_REPORT.md` (full narrative report)
- **Spreadsheet tool** (e.g., Excel) to review exported tables (`outputs/*.csv`) and NVivo matrix exports.

### For your viva presentation
- **Microsoft PowerPoint** (recommended) to build slides using the figures already generated in `outputs/`:
  - `corr_heatmap_core.png`
  - `governance_boundary_autonomy_success.png`
  - `kmeans_clusters_capability_accuracy.png`
  - `rf_feature_importance_top10.png`
- **PDF export** of slides for submission/backup (PowerPoint → Export → PDF).

---

## Methodology Part B — Quantitative analysis (statistical modeling already produced)

The statistical analysis is implemented in:

- `analysis_agentic_arc.py`

and exports results to:

- `outputs/REPORT.md` (overview)
- `outputs/*.csv`, `outputs/*.json`, `outputs/*.txt`, and `outputs/*.png` (tables, model summaries, figures).

---

## Results Part 1 — Descriptive and correlation analysis

### Correlation heatmap (core numeric features)
Figure:

![Correlation heatmap](corr_heatmap_core.png)

File: `outputs/corr_heatmap_core.png`

Supporting table:
- `outputs/corr_with_success_rate.csv`

---

## Results Part 2 — RQ1: Capability/performance structure (clustering + task effects)

### 2.1 Capability–accuracy landscape (K-Means)
K-Means clustering was applied to:
- `performance_index`
- `autonomous_capability_score`
- `accuracy_score`

Best \(k\) by silhouette score:
- **best_k = 2**, **best_silhouette = 0.428**

Figure:

![KMeans capability vs accuracy](kmeans_clusters_capability_accuracy.png)

File: `outputs/kmeans_clusters_capability_accuracy.png`  
Summary: `outputs/kmeans_summary.json`  
Cluster means: `outputs/cluster_profile_means.csv`

**Interpretation (how to explain to supervisor):**
- The dataset separates into **two distinct performance/capability regimes**.
- This supports an argument that “agentic capability + performance is not uniform”; governance should be **differentiated by regime** (e.g., higher autonomy/capability may require stronger controls even if average accuracy looks acceptable).

### 2.2 Task category is strongly associated with accuracy (ANOVA)
ANOVA on `accuracy_score ~ task_category`:
- \(F = 362.48\), \(p = 0.0\)
- \(\eta^2 = 0.395\) (large effect)
- categories = 10, \(n = 5000\)

Files:
- Table: `outputs/anova_accuracy_by_task_category.csv`
- Summary: `outputs/anova_accuracy_task_category.json`

**Interpretation:**
- Accuracy differences are **not random**; they vary substantially by task type.
- This supports a capability-centric governance position: risks cannot be assessed “in aggregate”; they must be contextualised by **task category / use case**.

---

## Results Part 3 — RQ2: Accountability/governance proxy (intervention required)

### 3.1 Logistic regression: predicting `human_intervention_required`
Model:
- GLM Binomial (Logit), cross-validated AUC via scikit-learn pipeline.

Key output:
- **CV AUC = 1.000 ± 0.000**

Key odds ratios (selected):
- `task_complexity`: **7.62**
- `autonomy_level`: **0.99** (not significant)
- `accuracy_score`: very small OR (negative coefficient in model), significant

Key p-values (selected):
- `task_complexity`: **1.62e-41**
- `accuracy_score`: **3.75e-10**
- `autonomy_level`: 0.823 (not significant)

Files:
- Summary JSON: `outputs/logit_accountability.json`
- Full model summary: `outputs/logit_glm_summary.txt`

**Interpretation (how to explain):**
- The “intervention required” flag is (in this dataset) **dominated by task complexity and performance signals**, not autonomy alone.
- For governance: this supports **threshold-based oversight triggers** that incorporate complexity + outcome indicators (not just “autonomy level”).

### 3.2 Privacy–latency tradeoff (sensitivity test)
OLS: `log(1 + latency) ~ privacy_compliance_score + deployment_environment`

Key output:
- `privacy_compliance_score` coefficient: **-0.1887**, \(p=0.212\)
- \(R^2 = 0.003\)

File:
- `outputs/privacy_latency_ols_summary.txt`

**Interpretation:**
- In this dataset, privacy compliance score does **not** show a strong linear latency penalty.
- This is a useful *negative result*: it suggests privacy controls (as represented here) may not necessarily impose major latency costs—though the low \(R^2\) also indicates many other factors dominate latency.

---

## Results Part 4 — RQ3: Trust threshold evidence (trust gap)

Welch t-test on `performance_index` by intervention requirement:

- mean(no intervention): **0.7680** (n=607)
- mean(requires intervention): **0.5141** (n=4393)
- \(t = 100.79\), \(p = 0.0\)
- Cohen’s \(d \approx 2.46\) (very large)

File:
- `outputs/trust_gap_ttest.json`

**Interpretation:**
- There is a large measurable “trust gap” consistent with a governance boundary: cases requiring intervention have substantially worse performance_index.

---

## Results Part 5 — RQ4: HOTL circuit-breaker simulation (governance intervention)

Triggered subset:
- \(n = 1693\)
- trigger rate: **0.3386**

Before → after means (triggered):
- accuracy: **0.448 → 0.435**
- success: **0.336 → 0.297**

Tests:
- Wilcoxon (greater) p-values reported as **1.0** (no evidence of improvement in this run).

Files:
- Summary: `outputs/hotl_sim_tests.json`
- Audit sample: `outputs/hotl_sim_audit_head200.csv`
- Outcome models: `outputs/hotl_outcome_model_accuracy.txt`, `outputs/hotl_outcome_model_success.txt`

**Interpretation (how to present carefully):**
- The implemented simulation, as currently parameterized, does **not** demonstrate an uplift on triggered cases.
- This is still valuable: it motivates refining the intervention policy (trigger rule and/or the counterfactual uplift mechanism) and supports an iterative DSR cycle (redesign → re-evaluate).

---

## Results Part 6 — Survival analysis (time to performance failure)

Cox model: event defined as `accuracy_score < 0.6`.

Hazard ratios (exp(coef)):
- `autonomy_level`: **1.028** (p≈0.060)
- `task_complexity`: **1.045** (p≈0.008)
- `privacy_compliance_score`: **0.723** (p≈0.156)

Files:
- Summary: `outputs/cox_survival_summary.txt`
- JSON: `outputs/survival_cox.json`

**Interpretation:**
- Higher task complexity is associated with a higher hazard of dropping below the accuracy threshold.
- Autonomy is borderline in this fitted model; privacy compliance trends protective but is not significant here.

---

## Figures index (all generated and stored locally)

- `outputs/corr_heatmap_core.png`
- `outputs/governance_boundary_autonomy_success.png`
- `outputs/kmeans_clusters_capability_accuracy.png`
- `outputs/rf_feature_importance_top10.png`

To view them inside this report, open the files directly in the `outputs/` folder (some markdown renderers require relative paths from the same folder).

Governance boundary figure:

![Governance boundary](governance_boundary_autonomy_success.png)

Random forest top-10 importance figure:

![RF feature importances](rf_feature_importance_top10.png)

---

## CVE-Bench (updated)

CVE-Bench Inspect **`.eval`** logs and a scored outcome summary are documented in **`outputs/FULL_REPORT_V2.md`** (section “CVE-Bench empirical runs”) and listed in **`outputs/CVE_BENCH_EVAL_INVENTORY.json`**.

---

## Conclusions (findings to date)

- **Capability/performance is structured**, not uniform: clustering suggests distinct regimes in capability/accuracy/performance.
- **Task category strongly shapes accuracy** (large ANOVA effect), supporting context-specific governance.
- **Intervention requirement is strongly explained by complexity/performance signals** in this dataset; autonomy alone is not a sufficient governance trigger.
- **Trust gap is large**: intervention-required cases show much lower performance_index.
- **The current HOTL simulation does not show uplift**; this is an actionable redesign target in the next DSR iteration.
- **CVE-Bench (partial)**: solution runs on CVE-2024-2624 pass grader checks; gpt-4o-mini agent runs score 0.0 with protocol/API misuse in transcripts. See V2 report for the full table.

---

## Appendix: key output files (for examiner/supervisor verification)

- CVE-Bench: `outputs/CVE_BENCH_EVAL_INVENTORY.json`, `CVE_BENCH_COMMANDS_USED.md`, `cve-bench-main/logs/*.eval`
- Main script: `analysis_agentic_arc.py`
- Short generated summary: `outputs/REPORT.md`
- Statistical summaries:
  - `outputs/kmeans_summary.json`
  - `outputs/anova_accuracy_task_category.json`
  - `outputs/logit_accountability.json`
  - `outputs/trust_gap_ttest.json`
  - `outputs/hotl_sim_tests.json`
  - `outputs/survival_cox.json`
- Figures:
  - `outputs/corr_heatmap_core.png`
  - `outputs/governance_boundary_autonomy_success.png`
  - `outputs/kmeans_clusters_capability_accuracy.png`
  - `outputs/rf_feature_importance_top10.png`

