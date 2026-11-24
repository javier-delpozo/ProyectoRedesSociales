# Integrar la entrega en Windows

## Opción recomendada: conservar el historial Git

1. Clona el repositorio y crea una rama:

```powershell
git clone https://github.com/javier-delpozo/ProyectoRedesSociales.git
cd ProyectoRedesSociales
git switch -c release/prac4-v1.0.0
```

2. Localiza la raíz Python. Es la carpeta que contiene `pyproject.toml`; en el historial anterior era `social_analyzer`:

```powershell
Get-ChildItem -Recurse -Filter pyproject.toml
cd social_analyzer
```

3. Copia **el contenido** de la carpeta entregada sobre esa raíz. No copies ninguna carpeta `.git` ni borres el `.git` del clon.

4. Ejecuta la preparación:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\preparar_windows.ps1
```

5. Revisa las diferencias y completa datos humanos:

```powershell
git status
git diff
python scripts\generar_contribuciones.py
```

Completa las áreas/evidencias de contribución y `docs/coevaluacion.md` con datos reales del equipo.

6. Publica la rama y abre una PR:

```powershell
git add .
git commit -m "Preparar entrega final PRAC4 v1.0.0"
git push -u origin release/prac4-v1.0.0
```

7. Tras fusionar y comprobar la CI:

```powershell
git switch main
git pull --ff-only origin main
git tag -a v1.0.0 -m "Entrega final PRAC4"
git push origin v1.0.0
```

## Si PowerShell bloquea la activación

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

La política se cambia solo para esa terminal.
