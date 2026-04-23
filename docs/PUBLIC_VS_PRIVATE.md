## What will be public in this repository

- **Code and configs**: `analysis_agentic_arc.py`, any analysis scripts, and the vendored upstream project under `cve-bench-main/`.
- **Text-based sources**: Markdown (`.md`), plain text (`.txt`), CSV (`.csv`), and JSON (`.json`) that are needed to understand and reproduce the analysis.

## What will be treated as private / not published

- **Raw datasets** under `Dataset/` (often large and may have licensing/usage constraints).
- **Rendered / export artefacts** (Word/PDF/HTML/images) under `outputs/` and the top-level `CVE_BENCH_*` exports.

These are excluded via `.gitignore` so you can safely share the repository link in your final report without accidentally publishing large or private files.

## If you need to publish a specific excluded file

- Move it into a clearly named folder (e.g. `docs/dissertation/`) and remove/override the matching ignore rule, or
- Publish it as a **release asset** (recommended for large PDFs) instead of storing it in git history.

