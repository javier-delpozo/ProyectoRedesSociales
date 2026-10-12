from src.importador import ImportadorCSV
from src.analizador import Analizador


def main():

    importador = ImportadorCSV()

    conversacion = importador.cargar(
        "tests/datos/conversacion.csv"
    )

    analizador = Analizador(
        conversacion
    )

    print(
        "\n=== ANALIZADOR DE REDES SOCIALES ===\n"
    )

    print(
        analizador.calcular_estadisticas()
    )

    print(
        analizador.calcular_participacion()
    )

    print(
        analizador.palabras_frecuentes()
    )


if __name__ == "__main__":
    main()