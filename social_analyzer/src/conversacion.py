class Conversacion:
    def __init__(self, titulo: str):
        self.titulo = titulo
        self.mensajes = []
        self.participantes = []

    def agregar_mensaje(self, mensaje):
        self.mensajes.append(mensaje)

    def agregar_participante(self, usuario):
        if usuario not in self.participantes:
            self.participantes.append(usuario)

    def total_mensajes(self):
        return len(self.mensajes)\n