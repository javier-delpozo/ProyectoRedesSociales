from datetime import datetime

from src.usuario import Usuario
from src.mensaje import Mensaje
from src.conversacion import Conversacion


def test_conversacion_vacia():

    conversacion = Conversacion(
        "Prueba"
    )

    assert conversacion.total_mensajes() == 0


def test_agregar_mensaje():

    usuario = Usuario(
        "U001",
        "Javier"
    )

    mensaje = Mensaje(
        "M001",
        "Hola",
        datetime.now(),
        usuario
    )

    conversacion = Conversacion(
        "Chat"
    )

    conversacion.agregar_mensaje(
        mensaje
    )

    assert conversacion.total_mensajes() == 1


def test_participantes_unicos():

    usuario = Usuario(
        "U001",
        "Javier"
    )

    conversacion = Conversacion(
        "Chat"
    )

    conversacion.agregar_participante(
        usuario
    )

    conversacion.agregar_participante(
        usuario
    )

    assert len(
        conversacion.participantes
    ) == 1