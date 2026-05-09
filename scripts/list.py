#!/usr/bin/env python3
"""
Listar ontologías en caché con tamaño y marca de tiempo de última modificación.
"""

import os
import sys
import pickle
from pathlib import Path
import time

ONTOLOGY_DIR = Path.home() / ".hermes" / "ontology"
CACHE_DIR = ONTOLOGY_DIR / "cache"

def main():
    if not CACHE_DIR.exists():
        print("No se encontró directorio de caché.")
        return
    files = list(CACHE_DIR.glob("*.pkl"))
    if not files:
        print("No hay ontologías en caché.")
        return

    print(f"{'Archivo':<30} {'Tamaño (triples)':<15} {'Modificado'}")
    print("-" * 60)
    for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            with open(f, "rb") as fp:
                g = pickle.load(fp)
            size = len(g)
        except Exception:
            size = "error"
        mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(f.stat().st_mtime))
        print(f"{f.name:<30} {str(size):<15} {mtime}")

if __name__ == "__main__":
    main()