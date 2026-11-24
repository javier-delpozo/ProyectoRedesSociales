"""Persistencia transaccional de conversaciones en SQLite."""

from __future__ import annotations

import logging
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from .domain import Conversacion, Mensaje, Usuario
from .errors import ConversacionNoEncontrada, ErrorPersistencia

logger = logging.getLogger(__name__)

ESQUEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS conversaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    creada_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversacion_id INTEGER NOT NULL,
    autor TEXT NOT NULL,
    contenido TEXT NOT NULL,
    fecha TEXT NOT NULL,
    FOREIGN KEY (conversacion_id) REFERENCES conversaciones(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_mensajes_conversacion
    ON mensajes(conversacion_id, fecha, id);
"""


class RepositorioSQLite:
    """Repositorio SQLite; cada operación cierra siempre su conexión."""

    def __init__(self, ruta: str | Path) -> None:
        self.ruta = Path(ruta)

    def inicializar(self) -> None:
        try:
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            with self._conexion() as conexion:
                conexion.executescript(ESQUEMA)
        except (OSError, sqlite3.Error) as exc:
            raise ErrorPersistencia(f"No se pudo inicializar la base de datos: {exc}") from exc

    def guardar(self, conversacion: Conversacion) -> int:
        self.inicializar()
        try:
            with self._conexion() as conexion:
                cursor = conexion.execute(
                    "INSERT INTO conversaciones(nombre) VALUES (?)", (conversacion.nombre,)
                )
                conversacion_id = int(cursor.lastrowid)
                conexion.executemany(
                    """INSERT INTO mensajes(conversacion_id, autor, contenido, fecha)
                       VALUES (?, ?, ?, ?)""",
                    [
                        (conversacion_id, m.autor.nombre, m.contenido, m.fecha.isoformat())
                        for m in conversacion.mensajes
                    ],
                )
        except sqlite3.Error as exc:
            raise ErrorPersistencia(f"No se pudo guardar la conversación: {exc}") from exc

        conversacion.id = conversacion_id
        logger.info(
            "Guardada conversación %d (%d mensajes)",
            conversacion_id,
            len(conversacion.mensajes),
        )
        return conversacion_id

    def obtener(self, conversacion_id: int) -> Conversacion:
        self.inicializar()
        try:
            with self._conexion() as conexion:
                fila = conexion.execute(
                    "SELECT id, nombre FROM conversaciones WHERE id = ?", (conversacion_id,)
                ).fetchone()
                if fila is None:
                    raise ConversacionNoEncontrada(
                        f"No existe la conversación con id {conversacion_id}"
                    )
                mensajes = conexion.execute(
                    """SELECT autor, contenido, fecha FROM mensajes
                       WHERE conversacion_id = ? ORDER BY fecha, id""",
                    (conversacion_id,),
                ).fetchall()
        except ConversacionNoEncontrada:
            raise
        except sqlite3.Error as exc:
            raise ErrorPersistencia(f"No se pudo leer la conversación: {exc}") from exc

        conversacion = Conversacion(fila["nombre"], id=fila["id"])
        for mensaje in mensajes:
            conversacion.agregar(
                Mensaje(
                    Usuario(mensaje["autor"]),
                    mensaje["contenido"],
                    datetime.fromisoformat(mensaje["fecha"]),
                )
            )
        return conversacion

    def listar(self) -> list[dict[str, object]]:
        self.inicializar()
        try:
            with self._conexion() as conexion:
                filas = conexion.execute(
                    """SELECT c.id, c.nombre, c.creada_en, COUNT(m.id) AS mensajes
                       FROM conversaciones c LEFT JOIN mensajes m ON m.conversacion_id = c.id
                       GROUP BY c.id ORDER BY c.id"""
                ).fetchall()
        except sqlite3.Error as exc:
            raise ErrorPersistencia(f"No se pudieron listar las conversaciones: {exc}") from exc
        return [dict(fila) for fila in filas]

    def eliminar(self, conversacion_id: int) -> None:
        self.inicializar()
        try:
            with self._conexion() as conexion:
                cursor = conexion.execute(
                    "DELETE FROM conversaciones WHERE id = ?", (conversacion_id,)
                )
                if cursor.rowcount == 0:
                    raise ConversacionNoEncontrada(
                        f"No existe la conversación con id {conversacion_id}"
                    )
        except ConversacionNoEncontrada:
            raise
        except sqlite3.Error as exc:
            raise ErrorPersistencia(f"No se pudo eliminar la conversación: {exc}") from exc

    @contextmanager
    def _conexion(self) -> Iterator[sqlite3.Connection]:
        """Abre una transacción y cierra la conexión incluso si hay una excepción."""
        conexion = self._conectar()
        try:
            with conexion:
                yield conexion
        finally:
            conexion.close()

    def _conectar(self) -> sqlite3.Connection:
        conexion = sqlite3.connect(self.ruta)
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion
