"""Analizadores especializados y fachada de composición."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from statistics import mean

from .domain import Conversacion

PALABRAS_VACIAS = {
    "a",
    "al",
    "algo",
    "como",
    "con",
    "de",
    "del",
    "el",
    "ella",
    "en",
    "es",
    "esta",
    "este",
    "esto",
    "hay",
    "la",
    "las",
    "lo",
    "los",
    "más",
    "me",
    "mi",
    "no",
    "o",
    "para",
    "pero",
    "por",
    "que",
    "se",
    "si",
    "sin",
    "su",
    "un",
    "una",
    "y",
    "ya",
}


@dataclass(frozen=True, slots=True)
class Participacion:
    """Métricas de participación de un usuario."""

    usuario: str
    mensajes: int
    porcentaje: float
    longitud_media: float


class AnalizadorParticipacion:
    """Calcula volumen y longitud media de mensajes por participante."""

    def analizar(self, conversacion: Conversacion) -> list[Participacion]:
        total = len(conversacion.mensajes)
        if total == 0:
            return []

        contenidos: dict[str, list[int]] = defaultdict(list)
        for mensaje in conversacion.mensajes:
            contenidos[mensaje.autor.nombre].append(len(mensaje.contenido))

        resultado = [
            Participacion(
                usuario=usuario,
                mensajes=len(longitudes),
                porcentaje=round(len(longitudes) * 100 / total, 2),
                longitud_media=round(mean(longitudes), 2),
            )
            for usuario, longitudes in contenidos.items()
        ]
        return sorted(resultado, key=lambda item: (-item.mensajes, item.usuario.casefold()))


class AnalizadorTemas:
    """Extrae términos frecuentes aplicando normalización y palabras vacías."""

    def analizar(self, conversacion: Conversacion, limite: int = 10) -> list[tuple[str, int]]:
        if limite < 1:
            raise ValueError("El límite debe ser mayor que cero")

        contador: Counter[str] = Counter()
        for mensaje in conversacion.mensajes:
            contador.update(self._terminos(mensaje.contenido))
        return contador.most_common(limite)

    @staticmethod
    def _terminos(texto: str) -> list[str]:
        normalizado = unicodedata.normalize("NFKC", texto).casefold()
        palabras = re.findall(r"[^\W\d_]{3,}", normalizado, flags=re.UNICODE)
        return [palabra for palabra in palabras if palabra not in PALABRAS_VACIAS]


class AnalizadorTemporal:
    """Agrupa la actividad de una conversación por fecha y por hora."""

    def por_fecha(self, conversacion: Conversacion) -> dict[str, int]:
        contador = Counter(mensaje.fecha.date().isoformat() for mensaje in conversacion.mensajes)
        return dict(sorted(contador.items()))

    def por_hora(self, conversacion: Conversacion) -> dict[str, int]:
        contador = Counter(f"{mensaje.fecha.hour:02d}:00" for mensaje in conversacion.mensajes)
        return dict(sorted(contador.items()))


class Analizador:
    """Fachada que compone analizadores especializados sin duplicar su lógica."""

    def __init__(
        self,
        participacion: AnalizadorParticipacion | None = None,
        temas: AnalizadorTemas | None = None,
        temporal: AnalizadorTemporal | None = None,
    ) -> None:
        self._participacion = participacion or AnalizadorParticipacion()
        self._temas = temas or AnalizadorTemas()
        self._temporal = temporal or AnalizadorTemporal()

    def participacion(self, conversacion: Conversacion) -> list[Participacion]:
        return self._participacion.analizar(conversacion)

    def temas(self, conversacion: Conversacion, limite: int = 10) -> list[tuple[str, int]]:
        return self._temas.analizar(conversacion, limite)

    def actividad_por_fecha(self, conversacion: Conversacion) -> dict[str, int]:
        return self._temporal.por_fecha(conversacion)

    def actividad_por_hora(self, conversacion: Conversacion) -> dict[str, int]:
        return self._temporal.por_hora(conversacion)

    def resumen(self, conversacion: Conversacion, limite: int = 10) -> dict[str, object]:
        """Compone el informe general a partir de los analizadores inyectados."""
        return {
            "id": conversacion.id,
            "nombre": conversacion.nombre,
            "total_mensajes": len(conversacion.mensajes),
            "total_participantes": len(conversacion.participantes),
            "participacion": [asdict(item) for item in self.participacion(conversacion)],
            "temas": [
                {"termino": termino, "frecuencia": frecuencia}
                for termino, frecuencia in self.temas(conversacion, limite)
            ],
            "actividad_por_fecha": self.actividad_por_fecha(conversacion),
            "actividad_por_hora": self.actividad_por_hora(conversacion),
        }
