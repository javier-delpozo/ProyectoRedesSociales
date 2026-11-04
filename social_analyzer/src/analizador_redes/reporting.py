"""Exportación de resultados a formatos abiertos."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .domain import Conversacion
from .errors import ErrorAplicacion


def exportar_resumen(resumen: dict[str, object], ruta: str | Path) -> Path:
    destino = Path(ruta)
    try:
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(
            json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError as exc:
        raise ErrorAplicacion(f"No se pudo escribir el informe {destino}: {exc}") from exc
    return destino


def exportar_mensajes_csv(conversacion: Conversacion, ruta: str | Path) -> Path:
    destino = Path(ruta)
    try:
        destino.parent.mkdir(parents=True, exist_ok=True)
        with destino.open("w", encoding="utf-8", newline="") as fichero:
            escritor = csv.DictWriter(fichero, fieldnames=["autor", "contenido", "fecha"])
            escritor.writeheader()
            for mensaje in conversacion.mensajes:
                escritor.writerow(
                    {
                        "autor": mensaje.autor.nombre,
                        "contenido": mensaje.contenido,
                        "fecha": mensaje.fecha.isoformat(),
                    }
                )
    except OSError as exc:
        raise ErrorAplicacion(f"No se pudo exportar el CSV {destino}: {exc}") from exc
    return destino
