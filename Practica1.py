from pathlib import Path

# Estructura del proyecto
folders = [
    "social_analyzer/src",
    "social_analyzer/tests",
]

files = {
    "social_analyzer/README.md": "# Analizador de Redes Sociales\n",
    "social_analyzer/requirements.txt": "",
    "social_analyzer/.gitignore": """
__pycache__/
*.pyc
.venv/
venv/
.env
.coverage
.pytest_cache/
""",

    "social_analyzer/src/__init__.py": "",

    "social_analyzer/src/usuario.py": """
class Usuario:
    def __init__(self, id_usuario: str, nombre: str):
        self.id_usuario = id_usuario
        self.nombre = nombre

    def __repr__(self):
        return f"Usuario({self.nombre})"
""",

    "social_analyzer/src/mensaje.py": """
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
        return f"Mensaje({self.usuario.nombre})"
""",

    "social_analyzer/src/conversacion.py": """
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
        return len(self.mensajes)
""",

    "social_analyzer/src/analizador.py": """
class Analizador:
    def __init__(self, conversacion):
        self.conversacion = conversacion

    def calcular_estadisticas(self):
        return {
            "mensajes": self.conversacion.total_mensajes(),
            "participantes": len(self.conversacion.participantes)
        }
""",

    "social_analyzer/src/main.py": """
from usuario import Usuario
from conversacion import Conversacion
from analizador import Analizador

def main():
    usuario = Usuario("U001", "Javier")

    conversacion = Conversacion(
        "Conversación de prueba"
    )

    conversacion.agregar_participante(usuario)

    analizador = Analizador(conversacion)

    print("=== Analizador de Redes Sociales ===")
    print(analizador.calcular_estadisticas())

if __name__ == "__main__":
    main()
""",

    "social_analyzer/tests/test_modelo.py": """
from src.usuario import Usuario

def test_usuario():
    usuario = Usuario("U001", "Javier")
    assert usuario.nombre == "Javier"
"""
}

# Crear carpetas
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Crear archivos
for file_path, content in files.items():
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\\n")

print("Proyecto creado correctamente.")