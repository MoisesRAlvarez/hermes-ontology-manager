#!/usr/bin/env python3
"""
Cargar un archivo de ontología en un grafo RDFLib, opcionalmente aplicar razonamiento,
y almacenarlo en caché como un pickle para reutilización rápida.
"""

import os
import sys
import pickle
import importlib.util
from pathlib import Path
from rdflib import Graph

ONTOLOGY_DIR = Path.home() / ".hermes" / "ontology"
CACHE_DIR = ONTOLOGY_DIR / "cache"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Cargar un archivo de ontología.")
    parser.add_argument(
        "--file",
        required=True,
        help="Ruta al archivo de ontología (relativa a ~/.hermes/ontology o absoluta).",
    )
    parser.add_argument(
        "--format",
        default=None,
        help="Formato (turtle, xml, json-ld, etc.). Si se omite, se adivina de la extensión.",
    )
    parser.add_argument(
        "--reasoner",
        action="store_true",
        help="Aplicar razonamiento Owlready2 si está disponible.",
    )
    args = parser.parse_args()

    # Resolver ruta absoluta
    if os.path.isabs(args.file):
        onto_path = Path(args.file)
    else:
        onto_path = ONTOLOGY_DIR / args.file

    if not onto_path.exists():
        print(f"Error: Archivo no encontrado: {onto_path}")
        sys.exit(1)

    # Cargar grafo
    g = Graph()
    try:
        g.parse(str(onto_path), format=args.format)
    except Exception as e:
        print(f"Fallo al analizar ontología: {e}")
        sys.exit(1)

    # Razonamiento opcional
    if args.reasoner:
        if importlib.util.find_spec("owlready2") is not None:
            from owlready2 import *
            # NOTA: La integración completa copiaría el grafo en un mundo Owlready2 y ejecutaría un razonador.
            # Por brevedad, solo notamos que la bandera fue honrada.
            print("Bandera de razonador establecida – marcador de posición de razonamiento (no se realizó inferencia real).")
        else:
            print("Advertencia: --reasoner solicitado pero owlready2 no instalado. Omitiendo razonamiento.")

    # Almacenar en caché
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / (onto_path.stem + ".pkl")
    with open(cache_file, "wb") as f:
        pickle.dump(g, f)

    print(f"Ontología '{onto_path.name}' cargada en grafo con {len(g)} triples.")
    print(f"Almacenada en caché en: {cache_file}")

if __name__ == "__main__":
    main()