"""Exportación de resultados a formatos abiertos."""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path

from .domain import Conversacion
from .errors import ErrorAplicacion


def exportar_resumen(resumen: dict[str, object], ruta: str | Path) -> Path:
    destino = Path(ruta)
    try:
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(
            json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError as exc:
        raise ErrorAplicacion(f"No se pudo escribir el informe {destino}: {exc}") from exc
    return destino


def _numero(valor: object) -> float:
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        return float(valor)
    return 0.0


def _filas(valor: object) -> list[dict[str, object]]:
    if not isinstance(valor, list):
        return []
    return [fila for fila in valor if isinstance(fila, dict)]


def _serie(valor: object) -> list[tuple[str, float]]:
    if not isinstance(valor, dict):
        return []
    return [(str(etiqueta), _numero(cantidad)) for etiqueta, cantidad in valor.items()]


def _barra(etiqueta: object, valor: float, maximo: float, sufijo: str = "") -> str:
    proporcion = 0 if maximo <= 0 else min(max(valor / maximo * 100, 0), 100)
    etiqueta_segura = html.escape(str(etiqueta))
    valor_legible = f"{valor:g}{sufijo}"
    return (
        '<div class="bar-row">'
        f'<div class="bar-label">{etiqueta_segura}</div>'
        '<div class="bar-track">'
        f'<div class="bar-fill" style="width:{proporcion:.2f}%"></div>'
        "</div>"
        f'<div class="bar-value">{html.escape(valor_legible)}</div>'
        "</div>"
    )


def exportar_informe_html(resumen: dict[str, object], ruta: str | Path) -> Path:
    """Genera un informe visual HTML autocontenido, sin JavaScript ni dependencias externas."""
    destino = Path(ruta)
    participacion = _filas(resumen.get("participacion"))
    temas = _filas(resumen.get("temas"))
    fechas = _serie(resumen.get("actividad_por_fecha"))
    horas = _serie(resumen.get("actividad_por_hora"))

    barras_participacion = "".join(
        _barra(fila.get("usuario", ""), _numero(fila.get("porcentaje")), 100, "%")
        for fila in participacion
    ) or '<p class="empty">Sin datos de participación.</p>'

    max_temas = max((_numero(fila.get("frecuencia")) for fila in temas), default=0)
    barras_temas = "".join(
        _barra(fila.get("termino", ""), _numero(fila.get("frecuencia")), max_temas)
        for fila in temas
    ) or '<p class="empty">Sin temas frecuentes.</p>'

    max_fechas = max((cantidad for _, cantidad in fechas), default=0)
    barras_fechas = "".join(
        _barra(etiqueta, cantidad, max_fechas) for etiqueta, cantidad in fechas
    ) or '<p class="empty">Sin actividad por fecha.</p>'

    max_horas = max((cantidad for _, cantidad in horas), default=0)
    barras_horas = "".join(
        _barra(etiqueta, cantidad, max_horas) for etiqueta, cantidad in horas
    ) or '<p class="empty">Sin actividad por hora.</p>'

    nombre = html.escape(str(resumen.get("nombre", "Conversación")))
    mensajes = int(_numero(resumen.get("total_mensajes")))
    participantes = int(_numero(resumen.get("total_participantes")))
    documento = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Informe visual - {nombre}</title>
  <style>
    :root {{ color-scheme: light; --ink:#0f172a; --slate:#475569; --line:#dbe4ee;
      --paper:#f8fafc; --teal:#0f766e; --mint:#2dd4bf; --orange:#f97316; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--paper); color:var(--ink);
      font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }}
    header {{ background:var(--ink); color:white; padding:48px max(6vw,24px); }}
    header p {{ color:#cbd5e1; margin:8px 0 0; }}
    h1 {{ margin:0; font-size:clamp(28px,4vw,48px); }}
    h2 {{ margin:0 0 18px; font-size:20px; }}
    main {{ max-width:1120px; margin:-22px auto 40px; padding:0 20px; }}
    .summary {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px;
      margin-bottom:16px; }}
    .metric,.card {{ background:white; border:1px solid var(--line); border-radius:14px;
      box-shadow:0 8px 28px rgba(15,23,42,.07); }}
    .metric {{ padding:22px; }}
    .metric strong {{ display:block; color:var(--teal); font-size:34px; }}
    .metric span {{ color:var(--slate); }}
    .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }}
    .card {{ padding:24px; }}
    .wide {{ grid-column:1/-1; }}
    .bar-row {{ display:grid; grid-template-columns:minmax(90px,1.15fr) 3fr 58px;
      gap:10px; align-items:center; margin:12px 0; }}
    .bar-label {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
    .bar-track {{ height:14px; background:#e2e8f0; border-radius:999px; overflow:hidden; }}
    .bar-fill {{ height:100%; min-width:2px; border-radius:999px;
      background:linear-gradient(90deg,var(--teal),var(--mint)); }}
    .bar-value {{ text-align:right; color:var(--slate); font-variant-numeric:tabular-nums; }}
    .split {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:28px; }}
    .split h3 {{ margin:0 0 12px; color:var(--slate); font-size:14px;
      text-transform:uppercase; letter-spacing:.08em; }}
    .empty {{ color:var(--slate); font-style:italic; }}
    footer {{ max-width:1120px; margin:0 auto; padding:0 20px 36px; color:var(--slate); }}
    @media (max-width:760px) {{ .grid,.summary,.split {{ grid-template-columns:1fr; }}
      .wide {{ grid-column:auto; }} .bar-row {{ grid-template-columns:90px 1fr 52px; }} }}
    @media print {{ body {{ background:white; }} header {{ padding:28px; }} main {{ margin:0; }}
      .metric,.card {{ box-shadow:none; break-inside:avoid; }} }}
  </style>
</head>
<body>
  <header>
    <h1>{nombre}</h1>
    <p>Informe visual del Analizador de Redes Sociales</p>
  </header>
  <main>
    <section class="summary" aria-label="Resumen">
      <div class="metric"><strong>{mensajes}</strong><span>mensajes analizados</span></div>
      <div class="metric"><strong>{participantes}</strong><span>participantes</span></div>
    </section>
    <div class="grid">
      <section class="card"><h2>Participación</h2>{barras_participacion}</section>
      <section class="card"><h2>Temas frecuentes</h2>{barras_temas}</section>
      <section class="card wide"><h2>Actividad temporal</h2>
        <div class="split"><div><h3>Por fecha</h3>{barras_fechas}</div>
        <div><h3>Por hora</h3>{barras_horas}</div></div>
      </section>
    </div>
  </main>
  <footer>Informe estático, autocontenido y generado localmente. No envía datos a Internet.</footer>
</body>
</html>
"""
    try:
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(documento, encoding="utf-8")
    except OSError as exc:
        raise ErrorAplicacion(f"No se pudo escribir el informe visual {destino}: {exc}") from exc
    return destino


def exportar_mensajes_csv(conversacion: Conversacion, ruta: str | Path) -> Path:
    destino = Path(ruta)
    try:
        destino.parent.mkdir(parents=True, exist_ok=True)
        with destino.open("w", encoding="utf-8", newline="") as fichero:
            escritor = csv.DictWriter(fichero, fieldnames=["autor", "contenido", "fecha"])
            escritor.writeheader()
            for mensaje in conversacion.mensajes:
                escritor.writerow(
                    {
                        "autor": mensaje.autor.nombre,
                        "contenido": mensaje.contenido,
                        "fecha": mensaje.fecha.isoformat(),
                    }
                )
    except OSError as exc:
        raise ErrorAplicacion(f"No se pudo exportar el CSV {destino}: {exc}") from exc
    return destino
