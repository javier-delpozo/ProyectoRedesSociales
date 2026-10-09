from collections import Counter


class Analizador:

    def __init__(self, conversacion):
        self.conversacion = conversacion

    def calcular_estadisticas(self):

        return {
            "mensajes":
                self.conversacion.total_mensajes(),
            "participantes":
                self.conversacion.total_participantes()
        }

    def calcular_participacion(self):

        contador = Counter()

        for mensaje in self.conversacion.mensajes:
            contador[mensaje.usuario.nombre] += 1

        return dict(contador)

    def palabras_frecuentes(self, top=10):

        palabras = []

        for mensaje in self.conversacion.mensajes:
            palabras.extend(
                mensaje.contenido.lower().split()
            )

        return Counter(
            palabras
        ).most_common(top)