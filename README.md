# Agentic Risk (ARC) + NVivo + CVE-Bench Artefact Repository

This repository contains the **computing artefact** for an MSc dissertation on **agentic AI governance** using the **Agentic Risk & Capability (ARC)** framework, **NVivo** qualitative coding outputs, quantitative analysis on a 5,000-record dataset, and empirical **CVE-Bench** logs (Inspect AI `.eval` archives).

It also vendors the upstream **CVE-Bench** project under `cve-bench-main/` (original license and README retained).

This repository is licensed under the terms in `LICENSE`. The vendored upstream project retains its own license in `cve-bench-main/LICENSE`.

## Quick navigation

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
  - Run from the repo root:

    ```bash
    python analysis_agentic_arc.py
    ```

  - Outputs are written to `outputs/` using deterministic filenames referenced in the dissertation.
  - What is excluded (and why): `docs/PUBLIC_VS_PRIVATE.md`
- **CVE-Bench**
  - Follow upstream instructions in `cve-bench-main/README.md`.
  - Windows command blocks used in this project are consolidated in `CVE_BENCH_LATEST_SCRIPT.md` / `CVE_BENCH_TEST_SCRIPT_WITH_RESULTS.md`.

