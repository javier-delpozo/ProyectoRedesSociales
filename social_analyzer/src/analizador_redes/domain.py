"""Modelo de dominio independiente de la entrada y de la persistencia."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .errors import ErrorValidacion


@dataclass(frozen=True, slots=True)
class Usuario:
    """Participante identificado por su nombre visible."""

    nombre: str

    def __post_init__(self) -> None:
        nombre = self.nombre.strip()
        if not nombre:
            raise ErrorValidacion("El nombre del usuario no puede estar vacío")
        object.__setattr__(self, "nombre", nombre)


@dataclass(frozen=True, slots=True)
class Mensaje:
    """Mensaje normalizado de cualquier red social."""

    autor: Usuario
    contenido: str
    fecha: datetime

    def __post_init__(self) -> None:
        contenido = self.contenido.strip()
        if not contenido:
            raise ErrorValidacion("El contenido del mensaje no puede estar vacío")
        if not isinstance(self.fecha, datetime):
            raise ErrorValidacion("La fecha del mensaje debe ser un datetime")
        object.__setattr__(self, "contenido", contenido)


@dataclass(slots=True)
class Conversacion:
    """Agregado que agrupa mensajes y participantes."""

    nombre: str
    mensajes: list[Mensaje] = field(default_factory=list)
    id: int | None = None

    def __post_init__(self) -> None:
        self.nombre = self.nombre.strip()
        if not self.nombre:
            raise ErrorValidacion("El nombre de la conversación no puede estar vacío")

    @property
    def participantes(self) -> tuple[Usuario, ...]:
        nombres = sorted({mensaje.autor.nombre for mensaje in self.mensajes}, key=str.casefold)
        return tuple(Usuario(nombre) for nombre in nombres)

    def agregar(self, mensaje: Mensaje) -> None:
        if not isinstance(mensaje, Mensaje):
            raise ErrorValidacion("Solo se pueden agregar objetos Mensaje")
        self.mensajes.append(mensaje)
