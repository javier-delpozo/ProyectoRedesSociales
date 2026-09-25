class Analizador:
    def __init__(self, conversacion):
        self.conversacion = conversacion

    def calcular_estadisticas(self):
        return {
            "mensajes": self.conversacion.total_mensajes(),
            "participantes": len(self.conversacion.participantes)
        }\n