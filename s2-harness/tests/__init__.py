"""Suite du harnais S2. SHOGEN-TESTS-TMP-1 (ADR-0028, lot B0) : tout `mkdtemp` de la suite est
rangé sous un dossier unique, retiré à la fin du processus (0 entrée laissée dans TMP)."""
import atexit
import os
import shutil
import sys
import tempfile

tempfile.tempdir = tempfile.mkdtemp(prefix="s2suite_")
atexit.register(shutil.rmtree, tempfile.tempdir)
sys.dont_write_bytecode = True                  # E-4 (G2 B0) : aucun __pycache__ dans l'arbre,
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"     # ni par les sous-processus (cli(), chemin servi)
