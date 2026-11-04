"""Importadores de ficheros al modelo común de conversación."""

from __future__ import annotations

import csv
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from .domain import Conversacion, Mensaje, Usuario
from .errors import ErrorImportacion, ErrorValidacion

logger = logging.getLogger(__name__)


class Importador(ABC):
    """Contrato abstracto para convertir una fuente en una conversación.

    Las capas consumidoras trabajan contra este contrato y no contra un formato
    concreto. Cada implementación decide cómo leer y normalizar su fuente.
    """

    @abstractmethod
    def importar(self, ruta: str | Path, nombre: str | None = None) -> Conversacion:
        """Importa ``ruta`` y devuelve una conversación normalizada."""

    @staticmethod
    def validar_ruta(ruta: str | Path) -> Path:
        """Valida una ruta de entrada y devuelve su representación como ``Path``."""
        origen = Path(ruta)
        if not origen.exists():
            raise ErrorImportacion(f"No existe el fichero de entrada: {origen}")
        if not origen.is_file():
            raise ErrorImportacion(f"La ruta de entrada no es un fichero: {origen}")
        return origen


class ImportadorCSV(Importador):
    """Importa CSV UTF-8 con las columnas ``autor``, ``contenido`` y ``fecha``."""

    COLUMNAS = {"autor", "contenido", "fecha"}

    def importar(self, ruta: str | Path, nombre: str | None = None) -> Conversacion:
        """Sobrescribe el contrato de :class:`Importador` para el formato CSV."""
        origen = self.validar_ruta(ruta)
        conversacion = Conversacion(nombre or origen.stem)
        try:
            with origen.open("r", encoding="utf-8-sig", newline="") as fichero:
                lector = csv.DictReader(fichero)
                columnas = set(lector.fieldnames or [])
                faltantes = self.COLUMNAS - columnas
                if faltantes:
                    detalle = ", ".join(sorted(faltantes))
                    raise ErrorImportacion(f"Faltan columnas obligatorias: {detalle}")
                for numero_linea, fila in enumerate(lector, start=2):
                    conversacion.agregar(self._crear_mensaje(fila, numero_linea))
        except UnicodeDecodeError as exc:
            raise ErrorImportacion("El CSV debe estar codificado en UTF-8") from exc
        except OSError as exc:
            raise ErrorImportacion(f"No se pudo leer {origen}: {exc}") from exc

        if not conversacion.mensajes:
            raise ErrorImportacion("El CSV no contiene mensajes")
        logger.info("Importados %d mensajes desde %s", len(conversacion.mensajes), origen)
        return conversacion

    @staticmethod
    def _crear_mensaje(fila: dict[str, str | None], numero_linea: int) -> Mensaje:
        try:
            autor = (fila.get("autor") or "").strip()
            contenido = (fila.get("contenido") or "").strip()
            fecha_texto = (fila.get("fecha") or "").strip()
            fecha = datetime.fromisoformat(fecha_texto.replace("Z", "+00:00"))
            return Mensaje(Usuario(autor), contenido, fecha)
        except (ValueError, ErrorValidacion) as exc:
            raise ErrorImportacion(f"Fila {numero_linea} inválida: {exc}") from exc
