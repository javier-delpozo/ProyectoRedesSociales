class Usuario:
    """
    Representa a un participante de una conversación.
    """

    def __init__(self, id_usuario: str, nombre: str):
        self.id_usuario = id_usuario
        self.nombre = nombre

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f"Usuario({self.nombre})"