# DjangoVibe demo launcher (PowerShell)
# Usage:  .\run.ps1
#
# Spawns three windows: Streamlit #1 (8501), Streamlit #2 (8502), Django (8000).
# Close each window to stop that server.

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
Set-Location $root

if (-not (Test-Path "$root\venv\Scripts\Activate.ps1")) {
    Write-Host ""
    Write-Host "[!] venv not found. First-time setup:" -ForegroundColor Yellow
    Write-Host "    python -m venv venv"
    Write-Host "    .\venv\Scripts\Activate.ps1"
    Write-Host "    pip install -r requirements.txt"
    Write-Host "    python manage.py migrate"
    Write-Host ""
    exit 1
}

# Each child window activates the venv first, then runs its server.
$activate = ". '$root\venv\Scripts\Activate.ps1'"

Write-Host "Launching Streamlit dashboard #1 on http://localhost:8501 ..." -ForegroundColor Magenta
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "$activate; streamlit run streamlit_apps\dashboard1.py --server.port 8501"
)

Write-Host "Launching Streamlit dashboard #2 on http://localhost:8502 ..." -ForegroundColor Magenta
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "$activate; streamlit run streamlit_apps\dashboard2.py --server.port 8502"
)

Write-Host "Launching Django on http://localhost:8000 ..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "$activate; python manage.py runserver"
)

Write-Host ""
Write-Host "All three servers are starting up." -ForegroundColor Green
Write-Host "Open http://localhost:8000 in your browser." -ForegroundColor Green
Write-Host "Close each PowerShell window to stop a server."
