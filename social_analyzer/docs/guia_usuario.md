# Guía de usuario

## 1. Objetivo

El programa transforma una conversación exportada en un conjunto homogéneo de mensajes, la guarda en una base SQLite y genera estadísticas reproducibles. Los datos permanecen en el equipo; no se envían a servicios externos.

## 2. Instalación

1. Instala Python 3.10 o posterior.
2. Abre una terminal en la raíz del proyecto.
3. Crea y activa un entorno virtual.
4. Instala el paquete:

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\Activate.ps1   # Windows PowerShell
python -m pip install -e .
```

Comprueba la instalación con:

```bash
python -m analizador_redes --help
```

## 3. Preparar el CSV

El fichero debe estar codificado en UTF-8 y tener una cabecera con estas columnas exactas:

| Columna | Obligatoria | Descripción |
|---|---:|---|
| `autor` | sí | Nombre visible del participante. |
| `contenido` | sí | Texto no vacío del mensaje. |
| `fecha` | sí | Fecha ISO 8601, por ejemplo `2026-10-30T18:00:00+01:00`. |

Se permiten columnas adicionales. Una fila inválida detiene la importación y el mensaje de error indica su número.

## 4. Flujo recomendado

### Validar sin guardar

```bash
python -m analizador_redes validar conversacion.csv
```

### Importar en SQLite

```bash
python -m analizador_redes --db datos/conversaciones.sqlite3 \
  importar conversacion.csv --nombre "Grupo de proyecto"
```

El comando devuelve el identificador numérico de la conversación.

### Listar datos guardados

```bash
python -m analizador_redes --db datos/conversaciones.sqlite3 listar
```

### Analizar

Mostrar por pantalla:

```bash
python -m analizador_redes --db datos/conversaciones.sqlite3 analizar 1 --top 15
```

Guardar un informe JSON:

```bash
python -m analizador_redes --db datos/conversaciones.sqlite3 \
  analizar 1 --top 15 -o informes/grupo.json
```

El resumen contiene número de mensajes y participantes, participación porcentual, longitud media, términos frecuentes y actividad por fecha y hora.

### Exportar mensajes normalizados

```bash
python -m analizador_redes --db datos/conversaciones.sqlite3 \
  exportar 1 exportaciones/grupo.csv
```

### Eliminar una conversación

```bash
python -m analizador_redes --db datos/conversaciones.sqlite3 eliminar 1
```

La eliminación es permanente y borra también sus mensajes.

## 5. Logging y diagnóstico

`-v` activa mensajes de depuración. `--log-file` añade un fichero rotatorio de hasta 1 MB y tres copias de respaldo.

```bash
python -m analizador_redes -v --log-file logs/app.log \
  --db datos/app.sqlite3 importar conversacion.csv
```

Los errores esperados (fichero ausente, cabecera incorrecta, fila inválida o id inexistente) se muestran sin traceback y devuelven código 2. Los errores del sistema devuelven código 3.

## 6. Copias de seguridad y privacidad

- Cierra el programa antes de copiar el fichero `.sqlite3`.
- Conserva la base y los informes fuera del control de versiones si contienen datos personales.
- Añade técnicas de anonimización antes de compartir conversaciones reales.

## 7. Problemas frecuentes

| Mensaje | Solución |
|---|---|
| `Faltan columnas obligatorias` | Revisa la cabecera y usa los nombres exactos. |
| `Fila N inválida` | Corrige autor, contenido o fecha de esa fila. |
| `El CSV debe estar codificado en UTF-8` | Vuelve a guardar el archivo como UTF-8. |
| `No existe la conversación con id N` | Ejecuta `listar` y usa un id existente. |
