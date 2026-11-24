"""Genera un registro Markdown a partir del historial Git local."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "contribuciones_generadas.md"
AUTHORS = [
    "Carlos Anguita Rodríguez",
    "Javier del Pozo Pérez",
    "Nicolás García Macías",
    "Quanan Wei",
]


def shortlog() -> list[tuple[int, str, str]]:
    result = subprocess.run(
        ["git", "shortlog", "-sne", "--all"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    rows = []
    for line in result.stdout.splitlines():
        match = re.match(r"\s*(\d+)\s+(.+?)\s+<([^>]+)>", line)
        if match:
            rows.append((int(match.group(1)), match.group(2), match.group(3)))
    return rows


def main() -> int:
    rows = shortlog()
    lines = [
        "# Registro de contribuciones",
        "",
       "Generado desde `git shortlog -sne --all`. "
        "Los commits miden actividad, no calidad ni esfuerzo.",
        "",
        "| Autor Git | Correo | Commits |",
        "|---|---|---:|",
    ]
    if rows:
        lines.extend(f"| {name} | {email} | {count} |" for count, name, email in rows)
    else:
        lines.append("| Sin commits visibles | - | 0 |")

    lines += [
        "",
        "## Resumen cualitativo del equipo",
        "",
        "Completar y revisar en grupo antes de entregar; "
        "no se infieren responsabilidades desde Git.",
        "",
        "| Miembro | Área o entregable principal | Evidencia (PR/commit/documento) |",
        "|---|---|---|",
    ]
    lines.extend(f"| {author} | _Completar_ | _Completar_ |" for author in AUTHORS)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generado: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
