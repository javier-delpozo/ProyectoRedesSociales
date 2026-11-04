from pathlib import Path

import pytest

from analizador_redes.errors import ErrorImportacion
from analizador_redes.importers import ImportadorCSV


def escribir(ruta: Path, contenido: str, encoding: str = "utf-8") -> Path:
    ruta.write_text(contenido, encoding=encoding)
    return ruta


def test_importar_csv_valido(tmp_path):
    ruta = escribir(
        tmp_path / "chat.csv",
        "autor,contenido,fecha,extra\n"
        "Ana,Hola,2026-10-30T09:00:00+01:00,x\n"
        "Luis,Adiós,2026-10-30T10:00:00+01:00,y\n",
    )

    conversacion = ImportadorCSV().importar(ruta, "  Reunión  ")

    assert conversacion.nombre == "Reunión"
    assert len(conversacion.mensajes) == 2
    assert conversacion.mensajes[0].fecha.utcoffset().total_seconds() == 3600


@pytest.mark.parametrize(
    ("contenido", "esperado"),
    [
        ("autor,contenido\nAna,hola\n", "Faltan columnas"),
        ("autor,contenido,fecha\nAna,hola,no-fecha\n", "Fila 2 inválida"),
        ("autor,contenido,fecha\n", "no contiene mensajes"),
        ("autor,contenido,fecha\n,Hola,2026-10-30\n", "Fila 2 inválida"),
    ],
)
def test_csv_invalido(tmp_path, contenido, esperado):
    ruta = escribir(tmp_path / "mal.csv", contenido)

    with pytest.raises(ErrorImportacion, match=esperado):
        ImportadorCSV().importar(ruta)


def test_ruta_ausente_o_directorio(tmp_path):
    with pytest.raises(ErrorImportacion, match="No existe"):
        ImportadorCSV().importar(tmp_path / "ausente.csv")
    with pytest.raises(ErrorImportacion, match="no es un fichero"):
        ImportadorCSV().importar(tmp_path)


def test_csv_no_utf8(tmp_path):
    ruta = tmp_path / "latin1.csv"
    ruta.write_bytes("autor,contenido,fecha\nAna,mañana,2026-10-30\n".encode("latin-1"))

    with pytest.raises(ErrorImportacion, match="UTF-8"):
        ImportadorCSV().importar(ruta)
