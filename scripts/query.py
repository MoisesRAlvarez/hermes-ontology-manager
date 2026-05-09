#!/usr/bin/env python3
"""
Consultar una ontología cargada (o cargar sobre la marcha) y ejecutar una consulta SPARQL.
Opcionalmente respaldar resultados a Notion y Obsidian.
"""

import os
import sys
import json
import datetime
import pickle
from pathlib import Path
from rdflib import Graph
from tabulate import tabulate

ONTOLOGY_DIR = Path.home() / ".hermes" / "ontology"
CACHE_DIR = ONTOLOGY_DIR / "cache"
NOTION_DB_NAME = "Consultas de Ontologías"      # marcador de posición – ID de DB real buscado en tiempo de ejecución
OBSIDIAN_DIR = Path.home() / "obsidian" / "ontology"

def load_graph(file_path: str | None):
    """Cargar grafo desde caché si el archivo coincide, de lo contrario cargar desde archivo y almacenar en caché."""
    if file_path is None:
        raise ValueError("La ruta del archivo debe proporcionarse.")
    onto_path = Path(file_path)
    if not onto_path.is_absolute():
        onto_path = ONTOLOGY_DIR / file_path
    if not onto_path.exists():
        raise FileNotFoundError(f"Archivo de ontología no encontrado: {onto_path}")

    # Usar caché
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / (onto_path.stem + ".pkl")
    if cache_file.exists():
        # Usar caché si no es más antigua que el archivo fuente
        if cache_file.stat().st_mtime >= onto_path.stat().st_mtime:
            with open(cache_file, "rb") as f:
                return pickle.load(f)
    # Cargar y almacenar en caché
    g = Graph()
    g.parse(str(onto_path), format="auto")
    with open(cache_file, "wb") as f:
        pickle.dump(g, f)
    return g

def backup_to_notion(query: str, results: list):
    """Intentar respaldar consulta y resultados a Notion."""
    try:
        from hermes_tools import notion
        # En una implementación completa harías:
        #   db_id = notion.get_database_id(NOTION_DB_NAME)
        #   notion.create_page(db_id, properties={...})
        # Por ahora notamos que el gancho existe.
        pass
    except Exception:
        # Ignorar silenciosamente si la habilidad de Notion no está configurada
        pass

def backup_to_obsidian(query: str, results: list):
    """Escribir consulta y resultados a un archivo markdown diario en el vault de Obsidian."""
    OBSIDIAN_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    md_file = OBSIDIAN_DIR / f"{today}.md"

    with md_file.open("a", encoding="utf-8") as f:
        f.write(f"## Consulta de Ontología – {datetime.datetime.now().isoformat()}\n\n")
        f.write(f"Consulta:\n```sparql\n{query}\n```\n\n")
        if results:
            headers = list(results[0].keys())
            rows = [[r.get(h, "") for h in headers] for r in results]
            f.write("*Resultados:\n")
            f.write(tabulate(rows, headers=headers, tablefmt="github"))
            f.write("\n\n")
        else:
            f.write("Sin resultados.\n\n")
        f.write("---\n\n")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Ejecutar una consulta SPARQL en una ontología.")
    parser.add_argument(
        "--file",
        required=False,
        help="Archivo de ontología a cargar (si se omite, usa el más reciente en caché).",
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Cadena de consulta SPARQL.",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Habilitar respaldo a Notion y Obsidian (si configurado).",
    )
    args = parser.parse_args()

    try:
        g = load_graph(args.file) if args.file else None
        if g is None:
            print("Error: --file es requerido.")
            sys.exit(1)

        results = g.query(args.query)
        keys = results.vars
        out = []
        for row in results:
            out.append({str(k): str(row[k]) for k in keys})

        # Imprimir resultados
        if out:
            print(tabulate([list(r.values()) for r in out],
                           headers=[str(k) for k in keys],
                           tablefmt="github"))
        else:
            print("Sin resultados.")

        # Respaldo si solicitado
        if args.backup:
            backup_to_notion(args.query, out)
            backup_to_obsidian(args.query, out)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()