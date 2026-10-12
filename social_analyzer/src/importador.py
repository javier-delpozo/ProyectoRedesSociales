import csv
from datetime import datetime

from src.usuario import Usuario
from src.mensaje import Mensaje
from src.conversacion import Conversacion


class ImportadorCSV:
    """
    Importa conversaciones desde un fichero CSV.

    Formato esperado:

    fecha,usuario,mensaje
    2026-10-01 10:00,Javier,Hola
    2026-10-01 10:05,Carlos,Buenos días
    """

    def cargar(self, ruta_csv: str) -> Conversacion:

        conversacion = Conversacion(
            "Conversación importada"
        )

        usuarios = {}

        with open(
            ruta_csv,
            mode="r",
            encoding="utf-8"
        ) as fichero:

            lector = csv.DictReader(fichero)

            for fila in lector:

                nombre_usuario = fila["usuario"]

                if nombre_usuario not in usuarios:

                    usuarios[nombre_usuario] = Usuario(
                        str(len(usuarios) + 1),
                        nombre_usuario
                    )

                usuario = usuarios[nombre_usuario]

                mensaje = Mensaje(
                    id_mensaje=str(
                        conversacion.total_mensajes() + 1
                    ),
                    contenido=fila["mensaje"],
                    fecha=datetime.strptime(
                        fila["fecha"],
                        "%Y-%m-%d %H:%M"
                    ),
                    usuario=usuario
                )

                conversacion.agregar_mensaje(
                    mensaje
                )

        return conversacion