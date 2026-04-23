<#
.SYNOPSIS
  Reorganize this repository into a publish-ready folder layout.

.DESCRIPTION
  - Creates a clean folder structure (docs/, data/, analysis/, results/, vendor/)
  - Moves existing top-level folders/files into those locations
  - Designed to be safe: run with -WhatIf first to preview changes

.EXAMPLE
  # Dry run (recommended)
  pwsh -File .\scripts\repo_publish_layout.ps1 -WhatIf

.EXAMPLE
  # Apply moves
  pwsh -File .\scripts\repo_publish_layout.ps1
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param()

$ErrorActionPreference = "Stop"

function Ensure-Dir([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) {
    if ($PSCmdlet.ShouldProcess($Path, "Create directory")) {
      New-Item -ItemType Directory -Path $Path | Out-Null
    }
  }
}

function Move-IfExists([string]$From, [string]$To) {
  if (Test-Path -LiteralPath $From) {
    $toParent = Split-Path -Parent $To
    Ensure-Dir $toParent
    if ($PSCmdlet.ShouldProcess("$From -> $To", "Move")) {
      Move-Item -LiteralPath $From -Destination $To
    }
  }
}

function Move-Glob([string]$FromDir, [string[]]$Patterns, [string]$ToDir) {
  if (-not (Test-Path -LiteralPath $FromDir)) { return }
  Ensure-Dir $ToDir
  foreach ($pat in $Patterns) {
    Get-ChildItem -LiteralPath $FromDir -Filter $pat -File -ErrorAction SilentlyContinue | ForEach-Object {
      $src = $_.FullName
      $dst = Join-Path $ToDir $_.Name
      if ($PSCmdlet.ShouldProcess("$src -> $dst", "Move")) {
        Move-Item -LiteralPath $src -Destination $dst
      }
    }
  }
}

$root = (Resolve-Path ".").Path

# Target dirs
$docsDissertation = Join-Path $root "docs\dissertation"
$docsPublishNotes = Join-Path $root "docs\publish-notes"
$dataRaw          = Join-Path $root "data\raw"
$dataNvivo        = Join-Path $root "data\nvivo"
$analysisPipeline  = Join-Path $root "analysis\pipeline"
$resultsRoot       = Join-Path $root "results"
$resultsTables     = Join-Path $resultsRoot "tables"
$resultsLogs       = Join-Path $resultsRoot "logs"
$vendorCveBench    = Join-Path $root "vendor\cve-bench"

Ensure-Dir $docsDissertation
Ensure-Dir $docsPublishNotes
Ensure-Dir $dataRaw
Ensure-Dir $dataNvivo
Ensure-Dir $analysisPipeline
Ensure-Dir $resultsTables
Ensure-Dir $resultsLogs
Ensure-Dir $vendorCveBench

# Upstream CVE-Bench (vendored)
Move-IfExists (Join-Path $root "cve-bench-main") $vendorCveBench

# Source datasets (PDFs, CSVs)
Move-IfExists (Join-Path $root "Dataset") $dataRaw

# NVivo exports (your current folder is already named nvivo/)
Move-IfExists (Join-Path $root "nvivo") $dataNvivo

# Analysis scripts you authored at repo root
Move-Glob $root @("analysis_*.py", "export_md_to_pdf_simple.py") $analysisPipeline

# Reports & outputs
if (Test-Path -LiteralPath (Join-Path $root "outputs")) {
  # Keep machine-readable results in git-friendly places
  Move-Glob (Join-Path $root "outputs") @("*.json", "*.csv", "*.txt") $resultsLogs

  # Dissertation/report sources (md/docx)
  Move-Glob (Join-Path $root "outputs") @("*.md", "*.docx") $docsDissertation
}

# Keep existing scripts folder (yours) and merge if needed
# Note: If you already have root ./scripts with other scripts, this script is inside it.
# Nothing is moved out of ./scripts by default.

Write-Host "Done. Review changes (git status) and adjust layout rules as needed."

