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
    main()\n