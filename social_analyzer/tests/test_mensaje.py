from datetime import datetime

from src.usuario import Usuario
from src.mensaje import Mensaje


def test_longitud_mensaje():

    usuario = Usuario(
        "U001",
        "Javier"
    )

    mensaje = Mensaje(
        "M001",
        "Hola mundo",
        datetime.now(),
        usuario
    )

    assert mensaje.obtener_longitud() == 10
