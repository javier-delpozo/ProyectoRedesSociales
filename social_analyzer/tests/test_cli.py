import json

from analizador_redes.cli import main


def test_flujo_cli_completo(tmp_path, capsys):
    csv_path = tmp_path / "chat.csv"
    csv_path.write_text(
        "autor,contenido,fecha\n"
        "Ana,Informe listo,2026-10-30T09:00:00\n"
        "Luis,Revisar informe,2026-10-30T10:00:00\n",
        encoding="utf-8",
    )
    db = tmp_path / "app.sqlite3"

    assert main(["--db", str(db), "validar", str(csv_path)]) == 0
    assert "CSV válido" in capsys.readouterr().out

    assert main(["--db", str(db), "importar", str(csv_path), "--nombre", "Demo"]) == 0
    assert "id 1" in capsys.readouterr().out

    assert main(["--db", str(db), "listar"]) == 0
    assert "1\tDemo\t2 mensajes" in capsys.readouterr().out

    assert main(["--db", str(db), "analizar", "1", "--top", "2"]) == 0
    resumen = json.loads(capsys.readouterr().out)
    assert resumen["total_mensajes"] == 2

    informe = tmp_path / "informe.json"
    assert main(["--db", str(db), "analizar", "1", "-o", str(informe)]) == 0
    assert informe.exists()

    exportado = tmp_path / "mensajes.csv"
    assert main(["--db", str(db), "exportar", "1", str(exportado)]) == 0
    assert exportado.exists()

    assert main(["--db", str(db), "eliminar", "1"]) == 0
    assert main(["--db", str(db), "listar"]) == 0
    assert "No hay conversaciones" in capsys.readouterr().out


def test_cli_error_controlado(tmp_path, capfd):
    codigo = main(["validar", str(tmp_path / "ausente.csv")])

    assert codigo == 2
    assert "No existe el fichero" in capfd.readouterr().err
