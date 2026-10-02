"""SHOGEN-SCEAU-VERIFY-CHEMINS-1 (G0 docs/adr-0028/G0-partie-3.md, section P3 ; annexe B.25) : scripts/sceau/make-tsq.sh
et verify.sh sur un dépôt jetable, une seule convention de chemins du manifeste PAQUET.sha256 (chemins relatifs à la
racine du dépôt, relus depuis la racine) ; sonde L1 du journal G1 C-1 rendue reproductible. Autorité RFC 3161 de test
produite par openssl (tests.test_rendu_unique.autorite), aucun réseau ; attendus écrits à la main (codes et lignes
imprimées par les scripts, sha256 des octets écrits par le test)."""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.test_oracle_record import GIT_ENV, HARNESS, g
from tests.test_rendu_unique import OPENSSL, PAQUET, SCEAU, autorite, o, poser

SCRIPTS = os.path.join(os.path.dirname(HARNESS), "scripts", "sceau")
BASH = shutil.which("bash")                 # PATH (CreateProcess lirait System32 d'abord), comme test_oracle_record


def script(nom: str, cwd: str, *args: str) -> subprocess.CompletedProcess:
    """scripts/sceau/<nom> du dépôt sous test, lancé par bash depuis cwd (dépôt jetable), sans variable GIT_*."""
    return subprocess.run([BASH, os.path.join(SCRIPTS, nom), *args], cwd=cwd, capture_output=True, text=True,
                          env=GIT_ENV)


class TestSceauScripts(unittest.TestCase):
    def depot(self) -> str:
        """Dépôt jetable dont un commit porte le paquet de fixture ; openssl ou bash absent : le test échoue."""
        self.assertTrue(OPENSSL and BASH, f"openssl ({OPENSSL}) ou bash ({BASH}) absent : échec, jamais de saut")
        d = os.path.join(tempfile.mkdtemp(), "depot")
        os.makedirs(d), g(d, "init", "-q"), g(d, "config", "core.autocrlf", "false")
        poser(d, {PAQUET: b"# Paquet de fixture\n"})
        return d

    def test_make_tsq_puis_verify_depuis_la_racine(self):
        """make-tsq.sh : manifeste d'une ligne « <sha256> *<chemin relatif à la racine> » ; jeton de la TSA de test sur
        la requête, chaîne dans chain/ : verify.sh lancé à la racine puis depuis un sous-dossier, code 0, dernière
        ligne « SCEAU : VÉRIFIÉ HORS LIGNE … » ; paquet changé après le manifeste : code 2, « MANIFESTE : ÉCART »,
        jeton non examiné. Rougit si : verify.sh relit le manifeste depuis le dossier de sceau (sonde L1 du G1 C-1) ;
        étape (1) qui ne contrôle plus les octets du paquet."""
        d, ac = self.depot(), os.path.join(tempfile.mkdtemp(), "ac")
        p = script("make-tsq.sh", d, SCEAU, PAQUET)
        sha = hashlib.sha256(b"# Paquet de fixture\n").hexdigest()
        self.assertEqual((p.returncode, Path(d, SCEAU, "PAQUET.sha256").read_bytes()),
                         (0, f"{sha} *{PAQUET}\n".encode()), p.stderr)
        a, c = autorite(ac)
        o(ac, "ts", "-reply", "-queryfile", os.path.join(d, SCEAU, "paquet.tsq"), "-signer", "tsa.crt", "-inkey",
          "tsa.key", "-out", os.path.join(d, SCEAU, "paquet.tsr"))
        poser(d, {f"{SCEAU}/chain/cacert.pem": a, f"{SCEAU}/chain/tsa.crt": c}, commit=False)
        for cwd in (d, os.path.join(d, "docs")):
            p = script("verify.sh", cwd)
            with self.subTest(cwd=cwd):
                self.assertEqual((p.returncode, p.stdout.splitlines()[-1][:26]), (0, "SCEAU : VÉRIFIÉ HORS LIGNE"),
                                 p.stdout + p.stderr)
        Path(d, PAQUET).write_bytes("# Paquet changé\n".encode())
        p = script("verify.sh", d)
        self.assertEqual((p.returncode, p.stdout.splitlines()[-1], "== (2)" in p.stdout),
                         (2, "MANIFESTE : ÉCART", False))

    def test_make_tsq_refuse_un_chemin_hors_convention(self):
        """make-tsq.sh, fichier du paquet donné hors de la convention (chemin absolu, segment « .. », lettre de
        lecteur, barre oblique inverse) : code 2, ligne « refus : … », ni manifeste ni requête écrits. Rougit si l'un
        des quatre motifs du contrôle est retiré."""
        d = self.depot()
        for nom, chemin in (("absolu", os.path.join(d, PAQUET)), ("segment ..", "docs/../" + PAQUET),
                            ("lecteur", "C:/" + PAQUET), ("barre inverse", PAQUET.replace("/", "\\"))):
            p = script("make-tsq.sh", d, SCEAU, chemin)
            with self.subTest(variante=nom):
                self.assertEqual((p.returncode, p.stdout.startswith(f"refus : {chemin} "),
                                  sorted(os.listdir(os.path.join(d, SCEAU)))), (2, True, ["chain"]),
                                 p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main()
