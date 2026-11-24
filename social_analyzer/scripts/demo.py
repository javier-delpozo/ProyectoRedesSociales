"""Demo reproducible y multiplataforma de la versión 1.0.0."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = ROOT / "build" / "demo"
DB = DEMO_DIR / "demo.sqlite3"
REPORT = DEMO_DIR / "resumen.json"
EXPORT = DEMO_DIR / "mensajes.csv"
INPUT = ROOT / "ejemplos" / "conversacion.csv"


def run(*args: str) -> str:
    command = [sys.executable, "-m", "analizador_redes", *args]
    print(f"\n$ {' '.join(command)}")
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        env=env,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout:
        print(result.stdout.rstrip())
    return result.stdout


def main() -> int:
    shutil.rmtree(DEMO_DIR, ignore_errors=True)
    DEMO_DIR.mkdir(parents=True)

    run("--version")
    run("validar", str(INPUT))
    run("--db", str(DB), "importar", str(INPUT), "--nombre", "Demo PRAC4")
    run("--db", str(DB), "listar")
    run("--db", str(DB), "analizar", "1", "--top", "5", "-o", str(REPORT))
    run("--db", str(DB), "exportar", "1", str(EXPORT))

    data = json.loads(REPORT.read_text(encoding="utf-8"))
    assert data["total_mensajes"] > 0
    assert EXPORT.exists()
    print(f"\nDemo completada. Artefactos: {DEMO_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
