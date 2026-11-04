import csv
import json
import sqlite3

import pytest

from analizador_redes.errors import ConversacionNoEncontrada
from analizador_redes.persistence import RepositorioSQLite
from analizador_redes.reporting import exportar_mensajes_csv, exportar_resumen


def test_repositorio_ciclo_completo(tmp_path, conversacion):
    repo = RepositorioSQLite(tmp_path / "datos" / "app.sqlite3")

    assert repo.listar() == []
    identificador = repo.guardar(conversacion)
    assert identificador == 1
    assert conversacion.id == 1
    assert repo.listar()[0]["mensajes"] == 3

    recuperada = repo.obtener(identificador)
    assert recuperada.id == 1
    assert recuperada.nombre == "Equipo"
    assert [mensaje.autor.nombre for mensaje in recuperada.mensajes] == ["Ana", "Luis", "Ana"]

    repo.eliminar(identificador)
    assert repo.listar() == []
    with pytest.raises(ConversacionNoEncontrada):
        repo.obtener(identificador)
    with pytest.raises(ConversacionNoEncontrada):
        repo.eliminar(identificador)


def test_repositorio_cierra_todas_las_conexiones(tmp_path, monkeypatch):
    conexiones: list[sqlite3.Connection] = []
    conectar_real = sqlite3.connect

    def conectar_registrando(*args, **kwargs):
        conexion = conectar_real(*args, **kwargs)
        conexiones.append(conexion)
        return conexion

    monkeypatch.setattr(sqlite3, "connect", conectar_registrando)
    RepositorioSQLite(tmp_path / "app.sqlite3").listar()

    assert conexiones
    for conexion in conexiones:
        with pytest.raises(sqlite3.ProgrammingError, match="closed"):
            conexion.execute("SELECT 1")


def test_exportadores(tmp_path, conversacion):
    resumen = {"nombre": "Equipo", "total": 3, "unicode": "mañana"}
    json_path = exportar_resumen(resumen, tmp_path / "salida" / "informe.json")
    assert json.loads(json_path.read_text(encoding="utf-8")) == resumen

    csv_path = exportar_mensajes_csv(conversacion, tmp_path / "salida" / "mensajes.csv")
    with csv_path.open(encoding="utf-8", newline="") as fichero:
        filas = list(csv.DictReader(fichero))
    assert len(filas) == 3
    assert filas[0]["autor"] == "Ana"
    assert filas[0]["fecha"].startswith("2026-10-30T09:00")
