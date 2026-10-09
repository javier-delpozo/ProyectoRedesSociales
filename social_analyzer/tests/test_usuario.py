from src.usuario import Usuario


def test_crear_usuario():

    usuario = Usuario(
        "U001",
        "Javier"
    )

    assert usuario.nombre == "Javier"
    assert usuario.id_usuario == "U001"