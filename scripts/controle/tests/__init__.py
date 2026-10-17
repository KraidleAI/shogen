"""Tests des outils de contrôle de l'orchestrateur (scripts/controle ; SHOGEN-FM11-VERIFIABLE-1, lot DETTES-T3), sur
transcriptions synthétiques seulement, jamais une vraie ; depuis scripts/controle :
env -u SHOGEN_S2_CAMPAGNE_CONTROL python3 -B -m unittest discover -s tests -t ."""
import os

# GARDE-FOUS phase 3 : le crochet GARDE-FAITS lancé par les cas n'écrit jamais au journal des refus du dépôt
os.environ.setdefault("SHOGEN_GARDE_REFUS", os.devnull)
