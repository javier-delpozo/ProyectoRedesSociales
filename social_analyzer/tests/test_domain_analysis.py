from datetime import datetime

import pytest

from analizador_redes.analysis import Analizador
from analizador_redes.domain import Conversacion, Mensaje, Usuario
from analizador_redes.errors import ErrorValidacion


def test_entidades_normalizan_y_validan():
    usuario = Usuario("  Ana  ")
    mensaje = Mensaje(usuario, "  Hola equipo  ", datetime(2026, 10, 30, 8, 0))

    assert usuario.nombre == "Ana"
    assert mensaje.contenido == "Hola equipo"

    with pytest.raises(ErrorValidacion):
        Usuario("  ")
    with pytest.raises(ErrorValidacion):
        Mensaje(usuario, "", datetime.now())
    with pytest.raises(ErrorValidacion):
        Mensaje(usuario, "texto", "2026-10-30")  # type: ignore[arg-type]
    with pytest.raises(ErrorValidacion):
        Conversacion(" ")


def test_conversacion_participantes_ordenados_y_agregar():
    conversacion = Conversacion(" Demo ")
    conversacion.agregar(Mensaje(Usuario("zoe"), "uno", datetime.now()))
    conversacion.agregar(Mensaje(Usuario("Ana"), "dos", datetime.now()))
    conversacion.agregar(Mensaje(Usuario("Ana"), "tres", datetime.now()))

    assert conversacion.nombre == "Demo"
    assert [usuario.nombre for usuario in conversacion.participantes] == ["Ana", "zoe"]
    with pytest.raises(ErrorValidacion):
        conversacion.agregar("no es mensaje")  # type: ignore[arg-type]


def test_analisis_completo(conversacion):
    analizador = Analizador()

    participacion = analizador.participacion(conversacion)
    assert participacion[0].usuario == "Ana"
    assert participacion[0].mensajes == 2
    assert participacion[0].porcentaje == 66.67
    assert dict(analizador.temas(conversacion, 3))["informe"] == 2
    assert analizador.actividad_por_fecha(conversacion) == {
        "2026-10-30": 2,
        "2026-10-31": 1,
    }
    assert analizador.actividad_por_hora(conversacion) == {
        "09:00": 1,
        "10:00": 1,
        "16:00": 1,
    }

    resumen = analizador.resumen(conversacion, 2)
    assert resumen["total_mensajes"] == 3
    assert resumen["total_participantes"] == 2
    assert len(resumen["temas"]) == 2


def test_analisis_vacio_y_limite_invalido():
    conversacion = Conversacion("Vacía")
    analizador = Analizador()

    assert analizador.participacion(conversacion) == []
    assert analizador.temas(conversacion) == []
    assert analizador.actividad_por_fecha(conversacion) == {}
    with pytest.raises(ValueError):
        analizador.temas(conversacion, 0)
