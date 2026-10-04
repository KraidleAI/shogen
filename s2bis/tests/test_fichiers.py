"""CB-2, E-C-20 : fichiers quotidiens bornés à 00:00 UTC, clos par `cloture`, sommés ; la chaîne continue d'un fichier
au suivant. Sommes recalculées ici sur les octets lus ; chaîne recalculée par `chaine` (tests/test_journal.py)."""
import hashlib
import os

from tests.test_journal import WS, Base, chaine

J1, J2, J3 = WS + 3660, WS + 3720, WS + 3720 + 86400   # 2026-10-04 23:59, 2026-10-05 00:00, 2026-10-06 00:00 (UTC)
NOMS = ["pool-2026-10-04-0.jsonl", "pool-2026-10-05-0.jsonl", "pool-2026-10-06-0.jsonl"]


class Fichiers(Base):
    def test_bascules_cloture_sommes_et_chaine_continue(self):
        jl = self.journal(J1 - 60)
        for ws in range(J1, J3 + 60, 60):
            jl.ecrire("lecture", ws, k=1)
            jl.marqueur(ws)
        e, seq, prec, par_fichier = self.etat(), 0, "0" * 64, []
        for n in NOMS:
            seq, prec, enrs = chaine(e[n], seq, prec)
            par_fichier.append((enrs[0]["type"], enrs[0]["jour"], enrs[0]["suivante"], enrs[-1]["type"],
                                enrs[-1].get("jour")))
        self.assertEqual(par_fichier, [("ouverture", "2026-10-04", J1, "cloture", "2026-10-04"),
                                       ("ouverture", "2026-10-05", J2, "cloture", "2026-10-05"),
                                       ("ouverture", "2026-10-06", J3, "marqueur", None)])
        sommes = "".join(f"{hashlib.sha256(e[n]).hexdigest()}  {n}\n" for n in NOMS[:2])
        self.assertEqual(e["pool.sha256"], sommes.encode())
        ino = {n: os.stat(os.path.join(self.d, n)).st_ino for n in (NOMS[0], "pool.sha256")}
        self.assertEqual((self.fsyncs.count(ino[NOMS[0]]), self.fsyncs.count(ino["pool.sha256"])), (2, 2))
