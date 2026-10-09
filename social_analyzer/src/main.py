from datetime import datetime

from src.usuario import Usuario
from src.mensaje import Mensaje
from src.conversacion import Conversacion
from src.analizador import Analizador


def main():

    javier = Usuario(
        "U001",
        "Javier"
    )

    carlos = Usuario(
        "U002",
        "Carlos"
    )

    conversacion = Conversacion(
        "Grupo TPA"
    )

    conversacion.agregar_mensaje(
        Mensaje(
            "M001",
            "Hola equipo",
            datetime.now(),
            javier
        )
    )

    conversacion.agregar_mensaje(
        Mensaje(
            "M002",
            "Hola Javier",
            datetime.now(),
            carlos
        )
    )

    conversacion.agregar_mensaje(
        Mensaje(
            "M003",
            "Vamos con la práctica",
            datetime.now(),
            javier
        )
    )

    analizador = Analizador(
        conversacion
    )

    print(
        "\n=== ANALIZADOR DE REDES SOCIALES ===\n"
    )

    print(
        "Estadísticas:"
    )

    print(
        analizador.calcular_estadisticas()
    )

    print(
        "\nParticipación:"
    )

    print(
        analizador.calcular_participacion()
    )

    print(
        "\nPalabras frecuentes:"
    )

    print(
        analizador.palabras_frecuentes()
    )

if __name__ == "__main__":
    main()