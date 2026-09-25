from src.usuario import Usuario

def test_usuario():
    usuario = Usuario("U001", "Javier")
    assert usuario.nombre == "Javier"\n