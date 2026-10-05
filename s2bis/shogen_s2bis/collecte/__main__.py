"""python3 -m shogen_s2bis.collecte : points d'entrée du collecteur (CB-18c ; `entree.py`)."""
import sys

from shogen_s2bis.collecte import entree

if __name__ == "__main__":
    raise SystemExit(entree.main(sys.argv[1:]))
