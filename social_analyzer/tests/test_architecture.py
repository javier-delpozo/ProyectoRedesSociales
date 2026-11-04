from argparse import Namespace
from datetime import datetime
from pathlib import Path

import pytest

from analizador_redes.analysis import (
    Analizador,
    AnalizadorParticipacion,
    AnalizadorTemas,
    AnalizadorTemporal,
)
from analizador_redes.cli import ejecutar
from analizador_redes.domain import Conversacion, Mensaje, Usuario
from analizador_redes.importers import Importador, ImportadorCSV


class ImportadorMemoria(Importador):
    """Doble de prueba que demuestra sustitución polimórfica del importador."""

    def importar(self, ruta: str | Path, nombre: str | None = None) -> Conversacion:
        return Conversacion(
            nombre or "Memoria",
            [Mensaje(Usuario("Ana"), "Mensaje simulado", datetime(2026, 10, 30, 9, 0))],
        )


class TemasFijos(AnalizadorTemas):
    def analizar(self, conversacion: Conversacion, limite: int = 10) -> list[tuple[str, int]]:
        return [("inyectado", len(conversacion.mensajes))][:limite]


def test_importador_es_abstracto_y_csv_lo_implementa():
    with pytest.raises(TypeError):
        Importador()  # type: ignore[abstract]

    assert issubclass(ImportadorCSV, Importador)
    assert isinstance(ImportadorCSV(), Importador)


def test_cli_acepta_cualquier_implementacion_de_importador(tmp_path, capsys):
    args = Namespace(
        db=str(tmp_path / "sin_uso.sqlite3"),
        comando="validar",
        fichero="origen.virtual",
        nombre="Polimorfismo",
    )

    assert ejecutar(args, ImportadorMemoria()) == 0
    assert "1 mensajes" in capsys.readouterr().out


def test_analizadores_especializados_y_fachada(conversacion):
    participacion = AnalizadorParticipacion().analizar(conversacion)
    temas = AnalizadorTemas().analizar(conversacion, 2)
    temporal = AnalizadorTemporal()

    assert participacion[0].usuario == "Ana"
    assert temas[0] == ("informe", 2)
    assert temporal.por_fecha(conversacion)["2026-10-30"] == 2
    assert temporal.por_hora(conversacion)["16:00"] == 1

    resumen = Analizador(temas=TemasFijos()).resumen(conversacion, 1)
    assert resumen["temas"] == [{"termino": "inyectado", "frecuencia": 3}]
