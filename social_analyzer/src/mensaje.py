from datetime import datetime
from usuario import Usuario

class Mensaje:
    def __init__(self, id_mensaje: str, contenido: str,
                 fecha: datetime, usuario: Usuario):
        self.id_mensaje = id_mensaje
        self.contenido = contenido
        self.fecha = fecha
        self.usuario = usuario

    def obtener_longitud(self):
        return len(self.contenido)

    def __repr__(self):
        return f"Mensaje({self.usuario.nombre})"\n