# run_all.ps1: Windows (PowerShell) version of run_all.sh.
# Runs the R scripts of part 04 one after another, like a small pipeline.
# For every sample in ground_truth.tsv: composition table + bar chart (composition.R).
# Then: diversity of all samples (diversity.R). Every R run writes a log file.
# Stops at the first failed step (like "set -e" in Bash) and exits with code 1.
#
# Usage (Rscript must be on PATH, see 04_R_Packages/01_Install_Packages/00_lesson_windows.md):
#   powershell -ExecutionPolicy Bypass -File run_all.ps1 <ground_truth.tsv> <output_folder>
#
# Written from the PowerShell documentation; not yet tested on Windows.
param(
    [Parameter(Mandatory = $true)][string]$Table,
    [Parameter(Mandatory = $true)][string]$Out
)
$ErrorActionPreference = "Stop"   # stop on errors of PowerShell commands themselves

$Table = (Resolve-Path $Table).Path   # full path, before we change folder (like realpath)
$here = $PSScriptRoot                 # folder of this script
$R01 = Join-Path $here "..\..\01_Install_Packages\scripts"
$R02 = Join-Path $here "..\..\02_Run_Rscript\scripts"
$R03 = Join-Path $here "..\..\03_Bioc_Examples\scripts"

New-Item -ItemType Directory -Force -Path (Join-Path $Out "logs") | Out-Null
Set-Location $Out
$work = (Get-Location).Path

# Run Rscript with one argument string; stdout and stderr go to two files.
# Rscript's exit code is checked: anything but 0 stops the pipeline.
function Invoke-R([string]$Arguments, [string]$OutFile, [string]$ErrFile) {
    $p = Start-Process -FilePath "Rscript" -ArgumentList $Arguments -WorkingDirectory $work `
        -RedirectStandardOutput (Join-Path $work $OutFile) -RedirectStandardError (Join-Path $work $ErrFile) `
        -NoNewWindow -Wait -PassThru
    if ($p.ExitCode -ne 0) {
        Write-Host "FAILED (exit $($p.ExitCode)); see $ErrFile"
        exit 1
    }
}

# 1. record the R and package versions used for this run
Invoke-R "`"$R01\check_packages.R`" ggplot2 vegan" "versions.txt" "logs\versions.log"

# 2. one composition chart per sample
$samples = Import-Csv $Table -Delimiter "`t" | ForEach-Object { $_.sample } | Sort-Object -Unique
foreach ($s in $samples) {
    Write-Host "composition: $s"
    Invoke-R "--vanilla `"$R02\composition.R`" `"$Table`" $s ${s}_composition.png" `
        "logs\${s}_composition.out" "logs\${s}_composition.log"
}

# 3. diversity of all samples together (genus level)
Write-Host "diversity: all samples"
Invoke-R "--vanilla `"$R03\diversity.R`" `"$Table`" diversity genus" "logs\diversity.out" "logs\diversity.log"

Write-Host "done; outputs in $Out"
