$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if (Test-Path ".venv") { Remove-Item -Recurse -Force ".venv" }
py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
& .\.venv\Scripts\python.exe -m pytest
& .\.venv\Scripts\python.exe -m ruff check .
& .\.venv\Scripts\python.exe scripts\demo.py
& .\.venv\Scripts\python.exe scripts\generar_documentacion.py
Write-Host "Entorno y evidencias de PRAC4 preparados correctamente."
