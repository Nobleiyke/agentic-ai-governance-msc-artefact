[README.md](https://github.com/user-attachments/files/27021797/README.md)
# agentic-ai-governance-msc-artefact
Reproducible analysis pipeline and results for ARC/NVivo mixed-methods study, with CVE-Bench (Inspect AI) evaluation artefacts and inventories.
# Agentic Risk (ARC) + NVivo + CVE-Bench Artefact Repository

This repository contains the **computing artefact** for an MSc dissertation on **agentic AI governance** using the **Agentic Risk & Capability (ARC)** framework, **NVivo** qualitative coding outputs, quantitative analysis on a 5,000-record dataset, and empirical **CVE-Bench** logs (Inspect AI `.eval` archives).

It also vendors the upstream **CVE-Bench** project under `cve-bench-main/` (original license and README retained).

This repository is licensed under the terms in `LICENSE`. The vendored upstream project retains its own license in `cve-bench-main/LICENSE`.

## Quick navigation

- **Dissertation / integrated report**
  - `outputs/Dissertation_Report_ARC_NVivo_Quant_CVE_MSc.md` (source)
  - `outputs/Dissertation_Report_ARC_NVivo_Quant_CVE_MSc.docx` (submission format)
  - `outputs/FULL_REPORT_FINAL_NVIVO_QUANT_CVE_2026-04-21.md` (integrated report snapshot)
- **Qualitative (NVivo) artefacts**
  - Codebooks and excerpts are exported into `outputs/` (CSV/MD) for reproducibility
  - Heavy NVivo exports (PDF/HTML/images/XLSX) are excluded from the public repo (see `docs/PUBLIC_VS_PRIVATE.md`)
- **Quantitative pipeline**
  - `analysis_agentic_arc.py` (main pipeline)
  - Raw input datasets are intentionally excluded from the public repo (see `docs/PUBLIC_VS_PRIVATE.md`)
  - `outputs/` (figures + tables + model summaries)
- **CVE-Bench empirical artefacts**
  - `CVE_BENCH_COMMANDS_USED.md` (command diary)
  - `scripts/summarize_eval_logs.py` (inventory generator)
  - `outputs/CVE_BENCH_EVAL_INVENTORY.json` (inventory)
  - `cve-bench-main/` (upstream code + `logs/*.eval`)

## Folder layout (recommended for publishing)

This repo currently includes working files at the top level. For a cleaner “publish” shape (especially for GitHub), see:

- `docs/PUBLISH_STRUCTURE.md` (what goes where)
- `docs/PUBLIC_VS_PRIVATE.md` (what is safe to publish vs excluded)
- `scripts/repo_publish_layout.ps1` (optional mover script with `-WhatIf` dry-run)

## Reproducibility (high level)

- **Quantitative pipeline**
  - Run `analysis_agentic_arc.py` from the repo root; outputs are written to `outputs/` using deterministic filenames referenced in the dissertation.
- **CVE-Bench**
  - Follow upstream instructions in `cve-bench-main/README.md`.
  - Windows command blocks used in this project are consolidated in `CVE_BENCH_LATEST_SCRIPT.md` / `CVE_BENCH_TEST_SCRIPT_WITH_RESULTS.md`.

