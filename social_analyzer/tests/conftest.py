from datetime import datetime

import pytest

from analizador_redes.domain import Conversacion, Mensaje, Usuario


@pytest.fixture
def conversacion() -> Conversacion:
    return Conversacion(
        "Equipo",
        [
            Mensaje(Usuario("Ana"), "Informe listo para revisar", datetime(2026, 10, 30, 9, 0)),
            Mensaje(Usuario("Luis"), "Revisar informe y datos", datetime(2026, 10, 30, 10, 0)),
            Mensaje(Usuario("Ana"), "Datos compartidos mañana", datetime(2026, 10, 31, 16, 0)),
        ],
    )
