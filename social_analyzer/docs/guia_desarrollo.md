# Guía de desarrollo

## 1. Arquitectura

El proyecto separa responsabilidades por capas:

- `domain.py`: entidades e invariantes, sin dependencias de infraestructura.
- `importers.py`: contrato abstracto `Importador` y adaptador concreto `ImportadorCSV`.
- `analysis.py`: analizadores especializados y fachada de compatibilidad `Analizador`.
- `persistence.py`: repositorio SQLite, esquema y ciclo de vida de conexiones.
- `reporting.py`: adaptadores de salida JSON, CSV e informe visual HTML.
- `cli.py`: composición de dependencias y experiencia de terminal.
- `errors.py` y `logging_config.py`: tratamiento transversal de fallos y trazas.

La CLI depende del contrato `Importador`, no del algoritmo de lectura. La fachada `Analizador` delega en `AnalizadorParticipacion`, `AnalizadorTemas` y `AnalizadorTemporal`. El dominio no conoce CSV, SQLite, `argparse` ni formatos de informe.

El [UML de la versión 1.0.0](uml.md) documenta clases y relaciones.

## 2. Preparar el entorno

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## 3. Comprobaciones locales

```bash
pytest
ruff check .
python -W error::ResourceWarning -m pytest
python -m analizador_redes --help
analizador-redes --help
```

La configuración de `pyproject.toml` activa cobertura de líneas y ramas, muestra líneas no cubiertas y exige al menos 70 %.

## 4. Principios OO aplicados

### Importación polimórfica

`Importador` es una clase abstracta (`ABC`) con la operación `importar`. `ImportadorCSV` hereda de ella y sobrescribe esa operación. `cli.ejecutar` permite inyectar cualquier implementación del contrato, lo que facilita añadir formatos y usar dobles de prueba.

Una implementación nueva debe respetar esta forma:

```python
from analizador_redes.importers import Importador

class ImportadorJSON(Importador):
    def importar(self, ruta, nombre=None):
        ...
```

### Análisis por composición

Cada cálculo tiene un servicio especializado. `Analizador` mantiene la API histórica y compone los resultados; no contiene los algoritmos. Los colaboradores se pueden inyectar en el constructor para probar o ampliar el comportamiento sin modificar la fachada.

## 5. Modelo de datos

SQLite usa dos tablas:

```text
conversaciones (id PK, nombre, creada_en)
       1
       |
       N
mensajes (id PK, conversacion_id FK, autor, contenido, fecha)
```

La clave foránea usa `ON DELETE CASCADE`. El índice por conversación y fecha mantiene estable el orden de lectura. Las consultas están parametrizadas.

## 6. Ciclo de vida de SQLite

`RepositorioSQLite._conexion` es un gestor de contexto que:

1. abre la conexión y activa claves foráneas;
2. confirma la transacción al finalizar correctamente o la revierte ante una excepción;
3. ejecuta `close()` en un bloque `finally`.

No se debe usar una conexión fuera de ese contexto. La prueba de regresión `test_repositorio_cierra_todas_las_conexiones` comprueba que las conexiones creadas por una operación pública quedan cerradas.

## 7. Manejo de errores

Las condiciones previsibles deben traducirse a una subclase de `ErrorAplicacion`:

- `ErrorValidacion`: invariantes del dominio.
- `ErrorImportacion`: estructura, codificación o filas de entrada.
- `ErrorPersistencia`: operaciones SQLite.
- `ConversacionNoEncontrada`: identificador inexistente.

No captures `Exception` en las capas internas. Conserva la excepción original con `raise ... from exc`. La frontera CLI convierte errores esperados en mensajes y códigos de salida; los defectos de programación permanecen visibles durante desarrollo.

## 8. Logging

Usa `logging.getLogger(__name__)` en cada módulo. Evita datos personales o contenidos completos en el log. Registra inicio o fin de importaciones, identificadores persistidos, recuentos y fallos técnicos.

## 9. Añadir un importador

1. Hereda de `Importador`.
2. Implementa `importar` y devuelve `Conversacion`.
3. Reutiliza `validar_ruta` cuando la fuente sea un fichero local.
4. Normaliza cada registro a `Usuario`, `Mensaje` y `datetime`.
5. Añade contexto de fila o registro en `ErrorImportacion`.
6. Añade pruebas del caso válido, fichero ausente, estructura incompleta y registro inválido.
7. Registra la implementación en la composición de CLI cuando el formato pase a estar soportado públicamente.

## 10. Añadir una métrica

1. Crea o amplía el analizador especializado responsable.
2. Mantén el cálculo determinista y sin mutar la conversación.
3. Delega desde `Analizador` solo si la métrica forma parte de la API general.
4. Integra el resultado en `resumen` cuando corresponda.
5. Prueba conversación vacía, un mensaje, empates y caracteres Unicode.

## 11. Estrategia de pruebas

- **Unitarias:** dominio y analizadores con objetos en memoria.
- **Arquitectura:** abstracción, herencia, sobrescritura, inyección y polimorfismo.
- **Adaptadores:** CSV y SQLite con `tmp_path`.
- **Reporting:** JSON/CSV e HTML autocontenido, con escape de texto aportado por el usuario.
- **Integración:** `cli.main([...])` con base y ficheros temporales.
- **Regresión:** cada fallo corregido deja una prueba que falla antes del arreglo.

No uses una base compartida entre pruebas. Evita depender del reloj o de la red.

## 12. Compatibilidad y release

- La CI ejecuta Python 3.10 y 3.12 en Windows, macOS y Linux.
- `python scripts/demo.py` evita comandos específicos del sistema operativo.
- `python scripts/generar_documentacion.py` produce la referencia API HTML.
- `python -m build` crea el wheel y el sdist antes de publicar.
- La etiqueta `v1.0.0` se crea solo después de que `main` pase la CI.

## 13. Flujo Git recomendado

1. Crea una rama breve, por ejemplo `release/prac4-v1.0.0`.
2. Realiza commits pequeños por responsabilidad.
3. Ejecuta estilo, pruebas, cobertura y comprobación de `ResourceWarning`.
4. Abre una PR con alcance, decisiones y evidencia de calidad.
5. Solicita revisión antes de fusionar.
