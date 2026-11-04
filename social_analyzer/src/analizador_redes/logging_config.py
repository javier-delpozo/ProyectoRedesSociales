"""Configuración centralizada del registro de actividad."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configurar_logging(verbose: bool = False, fichero: str | Path | None = None) -> None:
    nivel = logging.DEBUG if verbose else logging.INFO
    formato = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if fichero:
        ruta = Path(fichero)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(
            RotatingFileHandler(ruta, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        )
    for handler in handlers:
        handler.setFormatter(formato)
    logging.basicConfig(level=nivel, handlers=handlers, force=True)
