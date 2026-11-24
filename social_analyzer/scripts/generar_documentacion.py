"""Genera documentación API HTML con pdoc de forma multiplataforma."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "docs" / "api"


def main() -> int:
    shutil.rmtree(OUTPUT, ignore_errors=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, "-m", "pdoc", "-o", str(OUTPUT), "analizador_redes"],
        cwd=ROOT,
        check=True,
    )
    print(f"Documentación generada en {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
