# Checklist de entrega PRAC4

## Automático

- [x] `pytest` termina correctamente y la cobertura es >=70 %.
- [x] `pytest -m integration` ejecuta al menos una prueba de integración.
- [x] `ruff check .` no informa de errores.
- [x] `python -m build` genera sdist y wheel.
- [x] `python scripts/demo.py` completa todo el flujo.
- [x] `python scripts/generar_documentacion.py` genera `build/docs/api`.
- [ ] La CI pasa en Windows, macOS y Linux.

## Documentación y exposición

- [x] README y guía de usuario coinciden con la funcionalidad real.
- [x] CHANGELOG incluye v1.0.0.
- [x] Diapositivas y guion caben en 8-10 minutos.
- [x] Hay plan B de demo y no se usan datos personales reales.
- [x] `python scripts/generar_contribuciones.py` se ejecutó en el clon con historial Git.
- [ ] Cada miembro completó su coevaluación.

## Git y publicación

```powershell
git status
git pull --rebase origin main
python -m pytest
python -m ruff check .
git add .
git commit -m "Preparar entrega final PRAC4 v1.0.0"
git push origin main
git tag -a v1.0.0 -m "Entrega final PRAC4"
git push origin v1.0.0
```

No crear la etiqueta hasta que la rama `main` tenga la CI en verde y la coevaluación esté completada.
