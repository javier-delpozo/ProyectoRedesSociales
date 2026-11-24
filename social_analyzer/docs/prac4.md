# Evidencias de entrega PRAC4

## Correspondencia con el guion

| Requisito | Evidencia preparada |
|---|---|
| Funcionalidades cerradas | CLI completa, demo reproducible y limitaciones explícitas |
| Informe visual del guion inicial | `--html`, panel autocontenido y prueba de escape de contenido |
| Cobertura >=70 % | Umbral `--cov-fail-under=70` y `fail_under=70` en `pyproject.toml` |
| Al menos una integración | `tests/test_cli.py::test_flujo_cli_completo`, marcada `integration` |
| API + guía de uso | pdoc generable, `docs/guia_usuario.md` y script multiplataforma |
| Etiqueta v1.0.0 + changelog | Versión coherente, `CHANGELOG.md` y comandos de etiquetado |
| Exposición 8-10 min | `presentacion/PRAC4_Exposicion_Final.pptx` y guion temporizado |
| Registro de contribuciones | Generador desde `git shortlog` y tabla cualitativa en README |
| Coevaluación | Plantilla breve con escala común y evidencia observable |

## Decisión de alcance basada en PRAC3

La evaluación de seguimiento calificó el proyecto como sólido, consistente y bien alineado entre documentación, arquitectura e implementación. Destacó la persistencia SQLite, la separación de analizadores, la claridad del código y las pruebas de comportamientos completos. También aconsejó no crecer por crecer, mantener las pruebas, preservar la simplicidad y distinguir claramente lo implementado de las extensiones futuras.

Por ese motivo, PRAC4 no añade un segundo formato de entrada ni análisis semántico. Sí cubre el único
hueco funcional directo del guion inicial: un informe visual ligero. Se implementa como HTML estático
autocontenido para evitar un servidor, una GUI o dependencias gráficas de plataforma. La versión cierra
así un flujo fiable con mejor reproducibilidad, documentación publicable, CI multiplataforma,
materiales de exposición y controles de release.

## Validación esperada en un clon limpio

```powershell
python -m pip install -e ".[dev]"
pytest
pytest -m integration
ruff check .
python -m build
python scripts/demo.py
python scripts/generar_documentacion.py
```

Antes de etiquetar, adjuntar una captura de la CI y conservar el resumen de cobertura producido por `pytest`.

## Trazabilidad honesta

El ZIP de entrega no contiene `.git`; por tanto, no se inventa un reparto de contribuciones. `scripts/generar_contribuciones.py` debe ejecutarse dentro del clon completo para obtener el shortlog y completar después las evidencias cualitativas.
