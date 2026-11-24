"""Interfaz de línea de comandos del analizador."""

from __future__ import annotations

import argparse
import json
import logging
from collections.abc import Sequence

from . import __version__
from .analysis import Analizador
from .errors import ErrorAplicacion
from .importers import Importador, ImportadorCSV
from .logging_config import configurar_logging
from .persistence import RepositorioSQLite
from .reporting import exportar_mensajes_csv, exportar_resumen

logger = logging.getLogger(__name__)


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="analizador-redes",
        description="Importa, persiste y analiza conversaciones exportadas.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--db", default="datos/conversaciones.sqlite3",
                        help="ruta de SQLite (por defecto: %(default)s)")
    parser.add_argument("--log-file", help="guardar también el log en este fichero")
    parser.add_argument("-v", "--verbose", action="store_true", help="activar log de depuración")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    importar = subparsers.add_parser("importar", help="importar un CSV en SQLite")
    importar.add_argument("fichero")
    importar.add_argument("--nombre", help="nombre de la conversación")

    validar = subparsers.add_parser("validar", help="validar un CSV sin persistirlo")
    validar.add_argument("fichero")
    validar.add_argument("--nombre")

    subparsers.add_parser("listar", help="listar conversaciones persistidas")

    analizar = subparsers.add_parser("analizar", help="calcular un resumen completo")
    analizar.add_argument("id", type=_entero_positivo)
    analizar.add_argument("--top", type=_entero_positivo, default=10)
    analizar.add_argument("-o", "--salida", help="guardar el resumen como JSON")

    exportar = subparsers.add_parser("exportar", help="exportar mensajes normalizados a CSV")
    exportar.add_argument("id", type=_entero_positivo)
    exportar.add_argument("salida")

    eliminar = subparsers.add_parser("eliminar", help="eliminar una conversación")
    eliminar.add_argument("id", type=_entero_positivo)
    return parser


def _entero_positivo(valor: str) -> int:
    numero = int(valor)
    if numero < 1:
        raise argparse.ArgumentTypeError("debe ser un entero mayor que cero")
    return numero


def ejecutar(args: argparse.Namespace, importador: Importador | None = None) -> int:
    """Ejecuta un comando; el importador se puede sustituir polimórficamente."""
    repo = RepositorioSQLite(args.db)
    if args.comando in {"importar", "validar"}:
        importador_entrada = importador or ImportadorCSV()
        conversacion = importador_entrada.importar(args.fichero, args.nombre)
        if args.comando == "validar":
            print(f"CSV válido: {len(conversacion.mensajes)} mensajes, "
                  f"{len(conversacion.participantes)} participantes")
            return 0
        conversacion_id = repo.guardar(conversacion)
        print(f"Conversación importada con id {conversacion_id}: "
              f"{len(conversacion.mensajes)} mensajes")
        return 0

    if args.comando == "listar":
        filas = repo.listar()
        if not filas:
            print("No hay conversaciones guardadas")
        for fila in filas:
            print(f"{fila['id']}\t{fila['nombre']}\t{fila['mensajes']} mensajes")
        return 0

    if args.comando == "analizar":
        resumen = Analizador().resumen(repo.obtener(args.id), args.top)
        if args.salida:
            destino = exportar_resumen(resumen, args.salida)
            print(f"Informe guardado en {destino}")
        else:
            print(json.dumps(resumen, ensure_ascii=False, indent=2))
        return 0

    if args.comando == "exportar":
        destino = exportar_mensajes_csv(repo.obtener(args.id), args.salida)
        print(f"Mensajes exportados a {destino}")
        return 0

    if args.comando == "eliminar":
        repo.eliminar(args.id)
        print(f"Conversación {args.id} eliminada")
        return 0

    raise AssertionError(f"Comando no controlado: {args.comando}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = crear_parser()
    args = parser.parse_args(argv)
    try:
        configurar_logging(args.verbose, args.log_file)
        return ejecutar(args)
    except ErrorAplicacion as exc:
        logger.error("%s", exc)
        return 2
    except OSError as exc:
        logger.error("Error del sistema: %s", exc)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
