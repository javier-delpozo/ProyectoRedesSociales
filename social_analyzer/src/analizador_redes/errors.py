"""Excepciones de aplicación con mensajes aptos para mostrar al usuario."""


class ErrorAplicacion(Exception):
    """Error esperado que no requiere mostrar un traceback al usuario."""


class ErrorValidacion(ErrorAplicacion):
    """Los datos de dominio no cumplen las reglas mínimas."""


class ErrorImportacion(ErrorAplicacion):
    """No se pudo interpretar un fichero de entrada."""


class ErrorPersistencia(ErrorAplicacion):
    """No se pudo leer o escribir en el repositorio."""


class ConversacionNoEncontrada(ErrorPersistencia):
    """No existe una conversación con el identificador solicitado."""
