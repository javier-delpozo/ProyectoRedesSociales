from datetime import datetime

from src.usuario import Usuario
from src.mensaje import Mensaje
from src.conversacion import Conversacion
from src.analizador import Analizador


def test_estadisticas():

    usuario = Usuario(
        "U001",
        "Javier"
    )

    conversacion = Conversacion(
        "Chat"
    )

    conversacion.agregar_mensaje(
        Mensaje(
            "M001",
            "Hola",
            datetime.now(),
            usuario
        )
    )

    analizador = Analizador(
        conversacion
    )

    resultado = analizador.calcular_estadisticas()

    assert resultado["mensajes"] == 1
    assert resultado["participantes"] == 1


def test_participacion():

    usuario = Usuario(
        "U001",
        "Javier"
    )

    conversacion = Conversacion(
        "Chat"
    )

    conversacion.agregar_mensaje(
        Mensaje(
            "M001",
            "Hola",
            datetime.now(),
            usuario
        )
    )

    analizador = Analizador(
        conversacion
    )

    resultado = analizador.calcular_participacion()

    assert resultado["Javier"] == 1