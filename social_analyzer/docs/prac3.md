# Evidencias de avance de PRAC3

## Alcance cubierto

| Requisito | Implementación | Evidencia |
|---|---|---|
| Herencia y abstracción | `Importador` es una ABC y `ImportadorCSV` implementa el contrato | `src/analizador_redes/importers.py` |
| Sobrescritura y polimorfismo | `ImportadorCSV.importar` sobrescribe el método abstracto; la CLI acepta cualquier `Importador` | `importers.py`, `cli.py`, `test_architecture.py` |
| Separación de responsabilidades | Participación, temas y tiempo tienen analizadores propios; `Analizador` solo compone | `analysis.py` |
| Persistencia y E/S | CSV de entrada, SQLite transaccional, JSON de informe y CSV de exportación | `importers.py`, `persistence.py`, `reporting.py` |
| Cierre de recursos | Gestor de contexto transaccional con `close()` en `finally` y prueba de regresión | `persistence.py`, `test_persistence_reporting.py` |
| Errores y logging | Jerarquía de errores, contexto de fila, códigos de salida, consola y fichero rotatorio | `errors.py`, `cli.py`, `logging_config.py` |
| Packaging y ejecución | Proyecto `src`, `pyproject.toml`, módulo ejecutable y script de consola | `python -m analizador_redes`, `analizador-redes` |
| Pruebas y cobertura | Pruebas unitarias, de arquitectura, adaptadores e integración; umbral del 55 % | `tests/`, `pyproject.toml`, workflow |
| Documentación y UML | Inicio rápido, guías, criterios y diagrama de clases Mermaid | `README.md`, `docs/` |

## Criterios de aceptación

- Un CSV válido puede validarse, importarse, persistirse y recuperarse.
- Una importación fallida no crea una conversación parcial.
- `Importador` no puede instanciarse y `ImportadorCSV` puede sustituirse por otra implementación.
- El usuario puede listar, analizar, exportar y eliminar por identificador.
- La fachada conserva `participacion`, `temas`, `actividad_por_fecha`, `actividad_por_hora` y `resumen`.
- Los algoritmos están separados en tres analizadores especializados.
- Todas las conexiones SQLite se cierran tras éxito o error.
- Los errores esperados no muestran traceback y devuelven código 2.
- El paquete funciona como módulo y como script instalado.
- La ejecución de `pytest` falla por debajo del 55 % de cobertura.
- CI ejecuta estilo, pruebas y cobertura en Python 3.10 y 3.12.

## Validación local

La entrega debe validarse desde un entorno limpio con:

```bash
python -m pip install -e ".[dev]"
ruff check .
python -W error::ResourceWarning -m pytest
python -m analizador_redes --help
analizador-redes --help
```

Validación final realizada el 4 de noviembre de 2026 con Python 3.12:

- **19 pruebas superadas** en modo estricto para `ResourceWarning`;
- **91,57 % de cobertura de líneas** (402 de 439 líneas ejecutables), medida además con `trace` de la biblioteca estándar;
- wheel `analizador_redes_sociales-0.3.0-py3-none-any.whl` construido correctamente;
- wheel instalado en un entorno virtual limpio;
- `python -m analizador_redes --help` y `analizador-redes --help` comprobados tras la instalación.

El umbral reproducible para desarrollo y CI sigue configurado mediante `pytest-cov` en `pyproject.toml`, con cobertura de ramas y fallo por debajo del 55 %.

## Compatibilidad con PRAC2

Se conservan las entidades `Usuario`, `Mensaje` y `Conversacion`, la clase pública `Analizador` y sus métodos, `ImportadorCSV`, `RepositorioSQLite`, la sintaxis de la CLI y los dos puntos de entrada. La evolución se realiza por composición e inyección, sin obligar a cambiar el código cliente existente.

## Riesgos y mitigaciones

- **Nuevos formatos:** el contrato existe, pero solo CSV está registrado; cada formato deberá aportar implementación y pruebas.
- **Evolución del esquema:** PRAC3 crea el esquema de forma idempotente; cambios incompatibles futuros requerirán migraciones versionadas.
- **Volumen:** las importaciones cargan los mensajes en memoria; para ficheros muy grandes se recomienda procesamiento por lotes.
- **Temas:** la frecuencia de términos es explicable y reproducible, pero no sustituye un análisis semántico.
