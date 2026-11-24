#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."

rm -rf .venv
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
.venv/bin/python scripts/demo.py
.venv/bin/python scripts/generar_documentacion.py
printf '%s\n' 'Entorno y evidencias de PRAC4 preparados correctamente.'
