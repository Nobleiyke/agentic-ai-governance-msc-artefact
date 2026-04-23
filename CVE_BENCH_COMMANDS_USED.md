 # CVE-Bench commands/scripts used (Windows + Docker Desktop)

This file documents the exact commands and helper scripts used during setup, execution, monitoring, and cleanup of CVE-Bench on Windows (PowerShell), including what each command is for.

> Security note: never paste API keys into chat/logs. If a key is exposed, revoke/rotate it immediately.

## 1) Repo path variables (PowerShell)

**Purpose**: keep paths consistent and avoid Windows/Docker path issues. Use forward slashes in values that Docker Compose will interpolate.

```powershell
$REPO = "C:/Users/User/Downloads/cve-bench-main/cve-bench-main"
$CHALLENGES_DIR = "$REPO/src/critical/challenges"
```

## 2) Required environment variables for Docker Compose templates

**Purpose**: CVE compose files reference shared templates (e.g. `compose-target.yml`, `compose-include.yml`, `mariadb/compose.yml`) via `CVEBENCH_DOCKER_DIR`, and mount challenge metadata via `CVEBENCH_METADATA_DIR`. Without these, Compose looks in the wrong place and fails.

```powershell
$env:CVEBENCH_TAG           = "2.1.0"
$env:CVEBENCH_DOCKER_DIR    = "$REPO/src/common/docker"
$env:CVEBENCH_SANDBOXES_DIR = "$REPO/src/common/sandboxes"
$env:CVEBENCH_CHALLENGE_DIR = "$REPO/src/critical/challenges"
$env:CVEBENCH_METADATA_DIR  = "$REPO/src/critical/metadata"
```

Optional (smaller agent image):

```powershell
$env:CVEBENCH_KALI_SIZE = "core"
```

## 3) Starting ONE CVE stack manually (Docker Compose)

### 3.1 Select a CVE and compose file

**Purpose**: explicitly tell Docker Compose which CVE to run (bypasses any path resolution bugs).

```powershell
$CVE = "CVE-2024-37849"
$env:COMPOSE_PROJECT_NAME = $CVE.ToLower()
$env:COMPOSE_FILE = "$REPO/src/critical/challenges/$CVE/compose.yml"
```

### 3.2 Bring containers up and wait for healthchecks

**Purpose**: start the target application, database (if used), and the agent sandbox, then wait until services are healthy.

```powershell
docker compose up -d --wait --wait-timeout 180
docker compose ps
```

## 4) Publishing ports on localhost (the “expose overlay”)

By default many CVE stacks are only reachable on the internal Docker network (Compose shows `80/tcp` but no `0.0.0.0:PORT->80/tcp`).

### 4.1 Script used: `scripts/get_expose_services.py`

**Purpose**: generate a small compose YAML overlay that adds `ports:` mappings, typically:
- `9090:80` for the `target` web app
- `9091:9091` for the evaluator upload endpoint

Command used (writes overlay file):

```powershell
$overlay = "$env:TEMP/$CVE.expose.yml"
uv run --directory "$REPO/scripts" python "$REPO/scripts/get_expose_services.py" $CVE | Out-File -Encoding ascii $overlay
```

### 4.2 Apply overlay by using BOTH compose files

**Purpose**: enable `http://localhost:9090` (target) and `http://localhost:9091` (evaluator).

```powershell
$env:COMPOSE_FILE = "$REPO/src/critical/challenges/$CVE/compose.yml;$overlay"
docker compose up -d --force-recreate
docker compose ps
```

Expected ports (example):
- Target: `http://localhost:9090`
- Evaluator: `http://localhost:9091`

Quick check used:

```powershell
curl.exe -I http://localhost:9090
```

## 5) Running the evaluation (Inspect + CVE-Bench task)

### 5.1 OpenAI key (PowerShell session variable)

**Purpose**: required for `--model openai/...` calls.

```powershell
$env:OPENAI_API_KEY = "sk-PASTE-YOUR-KEY-HERE"
```

Safe verification used (without printing full key):

```powershell
$env:OPENAI_API_KEY.Length
$env:OPENAI_API_KEY.Substring(0,3)  # should be "sk-"
```

### 5.2 Single-CVE run

**Purpose**: run the benchmark agent against a specific CVE.

```powershell
uv run inspect eval "$REPO/src/cvebench/cvebench.py@cvebench" --model openai/gpt-4o -T challenges="$CVE"
```

### 5.3 “All CVEs” run (key fix: absolute `challenges_dir`)

The default in `src/cvebench/cvebench.py` is `challenges`, which is relative and caused:
`ValueError: root_dir must be an absolute path. Got 'challenges'`

**Purpose**: run the whole benchmark set with an absolute challenges root.

```powershell
uv run inspect eval "$REPO/src/cvebench/cvebench.py@cvebench" `
  --model openai/gpt-4o `
  -T challenges_dir="$CHALLENGES_DIR" `
  --display plain `
  --log-level warning
```

Low-concurrency “quota-safe” variant used/recommended:

```powershell
uv run inspect eval "$REPO/src/cvebench/cvebench.py@cvebench" `
  --model openai/gpt-4o `
  -T challenges_dir="$CHALLENGES_DIR" `
  --max-connections 1 `
  --max-samples 1 `
  --display plain `
  --log-level warning
```

## 6) Monitoring

### 6.1 Docker containers created by Inspect

**Purpose**: confirm sandboxes/containers exist while an eval is running.

```powershell
docker ps -a --format "table {{.Names}}\t{{.Status}}" | findstr /i inspect-cvebench
```

### 6.2 Inspect log viewer

Your `inspect view` CLI requires a subcommand. We used `start`.

**Purpose**: view `.eval` logs in a browser UI (local).

```powershell
uv run inspect view start --log-dir "$REPO/src/logs" --recursive
```

This prints a local URL (e.g. `http://127.0.0.1:7575`).

Note: Inspect wrote **early** runs under `"$REPO/src/logs"`. **2026-04-14** runs are under **`"$REPO/logs"`** (same `.eval` format). A consolidated list is generated to **`../outputs/CVE_BENCH_EVAL_INVENTORY.json`** when you run `python ../scripts/summarize_eval_logs.py` from the workspace root (or `python scripts/summarize_eval_logs.py` with cwd set to the parent folder that contains both `scripts/` and `cve-bench-main/`).

## 7) Cleanup

### 7.1 Stop a manually-started CVE stack (and remove volumes)

**Purpose**: avoid “volume is still in use” during later cleanup; reclaim volumes.

```powershell
docker compose down --timeout 0 --volumes
```

### 7.2 Remove leftover Inspect containers (after abort/exit)

**Purpose**: clean up any remaining `inspect-cvebench-*` containers.

```powershell
docker ps -aq --filter "name=inspect-cvebench" | ForEach-Object { docker rm -f $_ }
```

### 7.3 Confirm everything is stopped

**Purpose**: validate there are no running containers.

```powershell
docker ps
```

## 8) Errors encountered and what fixed them (quick mapping)

- **`required variable CVEBENCH_TAG is missing`**
  - Fix: set `$env:CVEBENCH_TAG = "2.1.0"`.

- **`CVEBENCH_DOCKER_DIR variable is not set` / missing `compose-target.yml`**
  - Fix: set `$env:CVEBENCH_DOCKER_DIR = "$REPO/src/common/docker"`.

- **Target not reachable on localhost; `docker compose port target 80` → `invalid IP:0`**
  - Fix: generate and apply expose overlay via `scripts/get_expose_services.py`, then include it in `COMPOSE_FILE`.

- **`inspect` “program not found”**
  - Fix: run from the repo root (where `uv` can find the project) or use `uv run --directory "$REPO" ...`.

- **`root_dir must be an absolute path. Got 'challenges'`**
  - Fix: pass `-T challenges_dir="$REPO/src/critical/challenges"`.

- **`429 insufficient_quota`**
  - Fix: enable billing/add quota; optionally reduce concurrency (`--max-connections 1 --max-samples 1`).

