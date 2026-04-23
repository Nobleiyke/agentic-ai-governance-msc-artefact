# Publish-ready structure (recommended)

The repository currently mixes:

- **Upstream CVE-Bench code** (vendored in `cve-bench-main/`)
- **Your dissertation artefacts** (datasets, NVivo exports, analysis pipeline, report outputs)
- **Rendered exports** (PDF/HTML/PNG/JPEG) that are convenient locally and may bloat a public git repo if very large

This document proposes a clean structure that works well for GitHub (or ZIP submission) and makes examiner navigation straightforward.

## Target structure

```
.
├─ README.md
├─ LICENSE                      (your repo license, if you add one)
├─ docs/
│  ├─ dissertation/             (submission + source)
│  └─ publish-notes/            (what was removed/kept, how to reproduce)
├─ data/
│  ├─ raw/                      (input datasets, PDFs used as sources)
│  └─ nvivo/                    (codebooks + NVivo exports)
├─ analysis/
│  ├─ pipeline/                 (python scripts you wrote)
│  └─ notebooks/                (optional)
├─ results/
│  ├─ figures/                  (tracked, small)
│  ├─ tables/                   (tracked)
│  └─ logs/                     (tracked summaries, inventories)
├─ vendor/
│  └─ cve-bench/                (upstream CVE-Bench project)
└─ scripts/
   └─ repo_publish_layout.ps1   (mover script)
```

## Practical guidance

- Put **sources** under version control (CSV, MD, TXT, JSON).
- In this repo, **PDFs and figures are kept tracked** (per your publishing preference).
- If you later decide to slim down the repo, consider Git LFS or publishing heavy renderings as release assets instead of normal git blobs.
- Keep upstream CVE-Bench isolated under `vendor/` so readers don’t confuse upstream code with your artefact code.

## Automated move script

If you want the repo physically rearranged to this layout, use:

- `scripts/repo_publish_layout.ps1`

Run it first with `-WhatIf` (dry run) to confirm the moves.

