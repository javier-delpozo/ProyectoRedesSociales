class Usuario:
    def __init__(self, id_usuario: str, nombre: str):
        self.id_usuario = id_usuario
        self.nombre = nombre

    def __repr__(self):
        return f"Usuario({self.nombre})"\n