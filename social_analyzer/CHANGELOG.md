# Changelog

Los cambios relevantes se documentan aquí siguiendo Keep a Changelog y versionado semántico.

## [1.0.0] - 2026-11-24

### Añadido

- Demo reproducible y multiplataforma en `scripts/demo.py`.
- Generación publicable de la documentación API con pdoc.
- Comprobación explícita de versión desde la CLI con `--version`.
- Materiales de exposición, coevaluación y registro de contribuciones para PRAC4.
- Matriz de integración continua en Windows, macOS y Linux.
- Informe visual HTML autocontenido con participación, temas y actividad temporal.

### Cambiado

- Umbral mínimo automatizado de cobertura elevado del 55 % al 70 %.
- Metadatos de licencia actualizados al formato moderno de `pyproject.toml`.
- Documentación y ejemplos preparados para la entrega final.

### Verificado

- Flujo de integración completo: validación, importación, SQLite, análisis, exportación y eliminación.
- Cierre garantizado de conexiones SQLite y manejo de errores de dominio.

## [0.3.0] - 2026-11-04

- Arquitectura por capas, importador abstracto, analizadores especializados y persistencia SQLite.
- Packaging moderno, logging, reporting y suite automatizada de PRAC3.
