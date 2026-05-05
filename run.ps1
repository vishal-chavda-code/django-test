# DjangoVibe demo launcher (PowerShell)
# Usage:  .\run.ps1
#
# Spawns three windows: Streamlit #1 (8501), Streamlit #2 (8502), Django (8000).
# Calls the venv binaries directly so spawned shells don't need to re-activate
# (avoids ExecutionPolicy quirks). Close each window to stop that server.

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
Set-Location $root

$pythonExe    = Join-Path $root "venv\Scripts\python.exe"
$streamlitExe = Join-Path $root "venv\Scripts\streamlit.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host ""
    Write-Host "[!] venv not found. First-time setup:" -ForegroundColor Yellow
    Write-Host "    python -m venv venv"
    Write-Host "    .\venv\Scripts\Activate.ps1"
    Write-Host "    pip install -r requirements.txt"
    Write-Host "    python manage.py migrate"
    Write-Host ""
    exit 1
}

# Streamlit flags ensure the apps render correctly when embedded in
# Django iframes — disable CORS and XSRF checks (these block cross-port
# websocket connections) and run headless so no extra browser tab opens.
$st1 = "& '$streamlitExe' run streamlit_apps\dashboard1.py --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false --browser.gatherUsageStats false"
$st2 = "& '$streamlitExe' run streamlit_apps\dashboard2.py --server.port 8502 --server.headless true --server.enableCORS false --server.enableXsrfProtection false --browser.gatherUsageStats false"
$dj  = "& '$pythonExe' manage.py runserver 8000"

Write-Host "Launching Streamlit dashboard #1 on http://localhost:8501 ..." -ForegroundColor Magenta
Start-Process powershell -WorkingDirectory $root -ArgumentList @("-NoExit", "-Command", $st1) | Out-Null

Write-Host "Launching Streamlit dashboard #2 on http://localhost:8502 ..." -ForegroundColor Magenta
Start-Process powershell -WorkingDirectory $root -ArgumentList @("-NoExit", "-Command", $st2) | Out-Null

Write-Host "Launching Django on http://localhost:8000 ..." -ForegroundColor Cyan
Start-Process powershell -WorkingDirectory $root -ArgumentList @("-NoExit", "-Command", $dj) | Out-Null

Write-Host ""
Write-Host "All three servers are starting up." -ForegroundColor Green
Write-Host "Streamlit takes 5-10 seconds to fully initialize on first load."
Write-Host "Open http://localhost:8000 in your browser when ready."
Write-Host "Close each PowerShell window to stop a server."
