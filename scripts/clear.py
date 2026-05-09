#!/usr/bin/env python3
"""
Limpiar archivos pickle de ontologías en caché.
"""

import os
import sys
from pathlib import Path

ONTOLOGY_DIR = Path.home() / ".hermes" / "ontology"
CACHE_DIR = ONTOLOGY_DIR / "cache"

def main():
    if not CACHE_DIR.exists():
        print("No se encontró directorio de caché.")
        return
    files = list(CACHE_DIR.glob("*.pkl"))
    if not files:
        print("No hay ontologías en caché para limpiar.")
        return
    for f in files:
        try:
            f.unlink()
            print(f"Eliminado: {f.name}")
        except Exception as e:
            print(f"Fallo al eliminar {f.name}: {e}")
    print("Caché limpiada.")

if __name__ == "__main__":
    main()