from src.importador import ImportadorCSV


def test_importar_csv():

    importador = ImportadorCSV()

    conversacion = importador.cargar(
        "tests/datos/conversacion.csv"
    )

    assert conversacion.total_mensajes() == 3
    assert conversacion.total_participantes() == 2



def test_primer_mensaje():

    importador = ImportadorCSV()

    conversacion = importador.cargar(
        "tests/datos/conversacion.csv"
    )

    mensaje = conversacion.mensajes[0]

    assert mensaje.contenido == "Hola equipo"