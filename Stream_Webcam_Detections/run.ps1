# Windows launcher for Stream Webcam Detections
$ErrorActionPreference = "Stop"

Write-Host "Stream Webcam Detections" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

$pythonExe = Join-Path (Get-Location) ".venv\Scripts\python.exe"

Write-Host "Installing/updating Python dependencies..." -ForegroundColor Yellow
& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r requirements.txt

if (Test-Path ".env") {
    Write-Host "Loading .env configuration..." -ForegroundColor Cyan
    Get-Content ".env" | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#") -and $line -match "^([^=]+)=(.*)$") {
            $name = $matches[1].Trim()
            $value = ($matches[2] -split "#", 2)[0].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
}

$hostAddr = if ($env:HOST) { $env:HOST } else { "0.0.0.0" }
$port = if ($env:PORT) { $env:PORT } else { "8080" }

Write-Host ""
Write-Host "Dashboard: http://127.0.0.1:$port/" -ForegroundColor Green
Write-Host "Stream:    http://127.0.0.1:$port/stream" -ForegroundColor Green
Write-Host "Health:    http://127.0.0.1:$port/healthz" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

# app.py starts Flask with threaded streaming support.
& $pythonExe app.py
