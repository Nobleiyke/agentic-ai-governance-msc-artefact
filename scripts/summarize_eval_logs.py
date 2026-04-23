"""Summarize Inspect .eval archives under cve-bench-main/logs and cve-bench-main/src/logs."""
from __future__ import annotations

import json
import zipfile
from pathlib import Path


def roots(repo: Path) -> list[Path]:
    return [repo / "logs", repo / "src" / "logs"]


def load_eval(p: Path) -> tuple[dict, list | dict]:
    with zipfile.ZipFile(p) as z:
        header = json.loads(z.read("header.json"))
        summaries = json.loads(z.read("summaries.json"))
    return header, summaries


def exploit_values(summaries: list | dict) -> list[float | None]:
    if not isinstance(summaries, list):
        return []
    out: list[float | None] = []
    for item in summaries:
        if not isinstance(item, dict):
            out.append(None)
            continue
        scores = item.get("scores") or {}
        ce = scores.get("check_exploit") if isinstance(scores, dict) else None
        if isinstance(ce, dict) and "value" in ce:
            v = ce["value"]
            out.append(float(v) if isinstance(v, (int, float)) else None)
        else:
            out.append(None)
    return out


def summarize_file(p: Path, repo: Path) -> dict:
    h, summaries = load_eval(p)
    ev = h.get("eval") if isinstance(h.get("eval"), dict) else {}
    task = ev.get("task") or h.get("task")
    model = ev.get("model") or h.get("model")
    task_args = ev.get("task_args") if isinstance(ev.get("task_args"), dict) else {}
    rel = p.relative_to(repo).as_posix() if p.is_relative_to(repo) else str(p)
    vals = exploit_values(summaries) if isinstance(summaries, list) else []
    mean_e = sum(v for v in vals if v is not None) / len([v for v in vals if v is not None]) if any(v is not None for v in vals) else None
    errors = []
    sample_ids = []
    if isinstance(summaries, list):
        for item in summaries:
            if isinstance(item, dict):
                sample_ids.append(item.get("id"))
                if item.get("error"):
                    errors.append(str(item["error"])[:200])
    return {
        "file": p.name,
        "path_posix": rel,
        "mtime_iso": __import__("datetime")
        .datetime.fromtimestamp(p.stat().st_mtime, tz=__import__("datetime").timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "task": task,
        "model": model,
        "task_args": task_args,
        "sample_ids": sample_ids,
        "exploit_values": vals,
        "mean_check_exploit": mean_e,
        "errors": errors,
    }


def main() -> None:
    workspace = Path(__file__).resolve().parents[1]
    repo = workspace / "cve-bench-main"
    out_dir = workspace / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    files: list[Path] = []
    for r in roots(repo):
        if r.is_dir():
            files.extend(r.glob("*.eval"))
    files = sorted(files, key=lambda x: x.stat().st_mtime)

    rows = []
    for p in files:
        try:
            rows.append(summarize_file(p, repo))
        except Exception as e:
            rows.append({"file": p.name, "error": str(e)})

    (out_dir / "CVE_BENCH_EVAL_INVENTORY.json").write_text(
        json.dumps({"repo": str(repo), "count": len(rows), "evals": rows}, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {out_dir / 'CVE_BENCH_EVAL_INVENTORY.json'}")
    for row in rows:
        if "error" in row:
            print(row["file"], "ERROR", row["error"])
            continue
        print(
            f"{row['file']}\t{row['task']}\t{row['model']}\tmean={row['mean_check_exploit']}\t"
            f"n_samples={len(row.get('sample_ids') or [])}"
        )
        if row.get("errors"):
            print("  errors:", row["errors"][0][:120], "..." if len(row["errors"][0]) > 120 else "")


if __name__ == "__main__":
    main()
