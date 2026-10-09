from datetime import datetime
from src.usuario import Usuario


class Mensaje:
    """
    Representa un mensaje enviado por un usuario.
    """

    def __init__(
        self,
        id_mensaje: str,
        contenido: str,
        fecha: datetime,
        usuario: Usuario
    ):
        self.id_mensaje = id_mensaje
        self.contenido = contenido
        self.fecha = fecha
        self.usuario = usuario

    def obtener_longitud(self) -> int:
        return len(self.contenido)

    def obtener_palabras(self):
        return self.contenido.split()

    def __repr__(self):
        return f"Mensaje({self.usuario.nombre})"