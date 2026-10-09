from src.mensaje import Mensaje
from src.usuario import Usuario


class Conversacion:
    """
    Contiene los mensajes y participantes.
    """

    def __init__(self, titulo: str):
        self.titulo = titulo
        self.mensajes = []
        self.participantes = []

    def agregar_participante(
        self,
        usuario: Usuario
    ) -> None:

        if usuario not in self.participantes:
            self.participantes.append(usuario)

    def agregar_mensaje(
        self,
        mensaje: Mensaje
    ) -> None:

        self.mensajes.append(mensaje)

        if mensaje.usuario not in self.participantes:
            self.participantes.append(
                mensaje.usuario
            )

    def total_mensajes(self) -> int:
        return len(self.mensajes)

    def total_participantes(self) -> int:
        return len(self.participantes)