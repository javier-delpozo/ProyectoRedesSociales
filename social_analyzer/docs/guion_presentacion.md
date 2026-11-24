# Guion de exposición final (8-10 minutos)

## Reparto de tiempo

| Minuto | Diapositiva | Mensaje y acción |
|---:|---|---|
| 0:00-0:30 | 1. Portada | Presentar el objetivo: importar, persistir y analizar conversaciones de forma local y reproducible. |
| 0:30-1:15 | 2. Problema y solución | Explicar entrada CSV, normalización, análisis y salidas abiertas. |
| 1:15-2:30 | 3. Arquitectura | Recorrer capas y destacar dominio desacoplado, importador abstracto, fachada y repositorio. |
| 2:30-3:15 | 4. Calidad | Mostrar pruebas, umbral >=70 %, integración extremo a extremo y CI multiplataforma. |
| 3:15-6:00 | 5-6. Demo | Ejecutar el flujo reproducible; abrir el JSON final y señalar participación, temas y actividad. |
| 6:00-7:00 | 7. Feedback PRAC3 | Resumir fortalezas y decisión de consolidar antes que añadir complejidad. |
| 7:00-8:15 | 8. Lecciones | Separación de responsabilidades, recursos SQLite, pruebas útiles y packaging. |
| 8:15-9:00 | 9. Cierre | Recordar v1.0.0, documentación generable y limitaciones explícitas. |

## Demo segura

Desde la raíz, con el entorno activado:

```powershell
python scripts/demo.py
```

El script limpia únicamente `build/demo`, ejecuta versión, validación, importación, listado, análisis y exportación, y comprueba el resultado. Tener preparado además:

```powershell
python -m analizador_redes --help
Get-Content build\demo\resumen.json
```

En macOS/Linux, el segundo comando es `cat build/demo/resumen.json`.

## Plan B sin improvisación

1. Conservar una captura del terminal tras una ejecución correcta.
2. Abrir `build/demo/resumen.json` y `build/demo/mensajes.csv` ya generados.
3. Si falla el proyector o la terminal, explicar el flujo con las diapositivas 5 y 6 sin modificar datos en directo.

## Preguntas previsibles

- **¿Por qué CSV?** Es el alcance implementado y documentado; el contrato `Importador` permite otros formatos sin acoplar el dominio.
- **¿Por qué SQLite?** Persistencia local, portable y suficiente para el volumen objetivo.
- **¿Qué prueba es de integración?** `test_flujo_cli_completo`, que cruza CLI, importación, SQLite, análisis, reporting y eliminación.
- **¿Qué queda fuera?** NLP semántico, migraciones complejas y procesamiento por lotes de archivos muy grandes.
