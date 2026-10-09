"""Témoin automatique de fm11.py (SHOGEN-FM11-VERIFIABLE-1 ; ADR-0028 annexe B, B.35 et B.87 ; lot DETTES-T3, DT3-A).
fm11.py tourne tel que versé (sha256 du README), dans un sous-processus, sur des transcriptions synthétiques écrites
ici, jamais une vraie. Les deux lignes de D.2 qu'il repère ne sont jamais lues : DOUBLURE sert à leur place deux lignes
synthétiques (CARTO, ADR) ; hashlib, subprocess et open y sont des doublures qui rendent SHA51 et SHA14 pour ces deux
lignes seules, et refusent toute autre commande et toute lecture sous le dépôt. Comptes attendus écrits à la main :
fragment = 40 caractères pris tous les 20 depuis le début de la ligne ; un bloc compte une fois par ligne interdite."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # scripts/controle
FM11 = os.path.join(ICI, "fm11.py")
SHA_FM11 = "886cc676874e70e3fe49a259fda6cfc8591882d511a29edded5c651860c1e254"   # README, SHA256SUMS, annexe B.35
SHA51 = "5cc89b563f73d213e38021165a360c3bf2e297e36be467786a007021c71db358"      # fm11.py l.12 (cartographie l.51)
SHA14 = "0fe88f1a3810244ecce91b31c1f4e2117f397a7c65d381a75afdbf0b9954b71f"      # fm11.py l.13 (ADR-0025 l.14)
CARTO = "".join(f"c{i:02d}|" for i in range(25))           # 100 caractères ; fragments aux rangs 0, 20 et 40
ADR = "".join(f"a{i:02d}|" for i in range(25))
DOUBLURE = chr(10).join([
    "import builtins, hashlib, io, runpy, sys, types",
    "fm11, transcription, carto, adr, sha51, sha14, mode = sys.argv[1:8]",
    "REPO = '/home/user/shogen'; CHEMIN = REPO + '/docs/rapports/cartographie-2026-09-29.md'",
    "GIT = ['git', '-C', REPO, 'show', '7f8b5cc:docs/adr-0025/ADR-0025-periode-doublee-S2.md']",
    "NL, carto, adr = chr(10), *((carto, adr) if mode != 'absentes' else ('autre', 'autre'))",
    "EMPREINTES = {(carto + NL).encode(): sha51, (adr + NL).encode(): sha14}",
    "vrai, ouvrir = hashlib.sha256, builtins.open",
    "class H:",
    "    def __init__(self, d=b''): self.d = d",
    "    def hexdigest(self): return EMPREINTES.get(self.d) or vrai(self.d).hexdigest()",
    "def run(args, capture_output=False, **k):",
    "    if list(args) != GIT or not capture_output:",
    "        raise PermissionError('commande refusée par la doublure : %r' % (args,))",
    "    return types.SimpleNamespace(stdout=('tete' + NL + adr + NL + 'queue' + NL).encode(), returncode=0)",
    "def lire(f, mode='r', *a, **k):",
    "    if str(f) == CHEMIN and mode == 'rb':",
    "        return io.BytesIO(('tete' + NL + carto + NL + 'queue' + NL).encode())",
    "    if str(f).startswith(REPO + '/'):",
    "        raise PermissionError('lecture refusée par la doublure : ' + str(f))",
    "    return ouvrir(f, mode, *a, **k)",
    "faux_h, faux_s = types.ModuleType('hashlib'), types.ModuleType('subprocess')",
    "faux_h.sha256, faux_s.run, builtins.open, sys.argv = H, run, lire, [fm11, transcription]",
    "sys.modules['hashlib'], sys.modules['subprocess'] = faux_h, faux_s",
    "runpy.run_path(fm11, run_name='__main__')",
    ""])


def lancer(evenements, mode="servies", chemin=None):
    """fm11.py sous DOUBLURE sur la transcription `evenements` (objets JSON, un par ligne) : (code, stdout, stderr)."""
    with tempfile.TemporaryDirectory() as d:
        t = chemin or os.path.join(d, "transcription-synthetique.txt")
        if chemin is None:
            with open(t, "w", encoding="utf-8") as f:
                f.write("".join(json.dumps(e, ensure_ascii=False) + chr(10) for e in evenements))
        env = {k: v for k, v in os.environ.items() if k != "SHOGEN_S2_CAMPAGNE_CONTROL"}
        p = subprocess.run([sys.executable, "-I", "-B", "-c", DOUBLURE, FM11, t, CARTO, ADR, SHA51, SHA14, mode],
                           capture_output=True, text=True, cwd=d, env=env, timeout=120)
    return p.returncode, p.stdout, p.stderr


def texte(t, role="user"):
    return {"type": role, "message": {"role": role, "content": [{"type": "text", "text": t}]}}


def resultat(contenu):
    return {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": contenu}]}}


class Temoin(unittest.TestCase):
    def compter(self, evenements):
        code, sortie, err = lancer(evenements)
        self.assertEqual(code, 0, f"fm11.py sorti en {code} : {err[-400:]}")
        try:
            return json.loads(sortie)
        except ValueError:
            self.fail(f"sortie de fm11.py illisible en JSON : {sortie[:200]!r}")

    def test_entree_propre_zero_fragment(self):
        """Sans fragment ni motif, dont les 39 premiers caractères de chaque ligne : 0 fragment, aucun motif."""
        res = self.compter([texte("bonjour"), resultat("c00|c01|c02|c03|c04|c05|c06|c07|c08|c0"),
                            texte("a00|a01|a02|a03|a04|a05|a06|a07|a08|a0 ; cartographie sans date", "assistant")])
        self.assertEqual(res, {"evenements": 3, "resultats": {}, "entrees": {},
                               "fragments_l51_l14": {"resultats": 0, "entrees": 0}})

    def test_entree_avec_fragments_comptes(self):
        """Cinq événements : un fragment de CARTO en entrée (0), un d'ADR en résultat d'outil (1), un de chaque dans
        un même bloc de contenu en chaîne (2), deux motifs en résultat et un en entrée (3), un événement sans message
        (4) : fragments 1 en résultats et 3 en entrées."""
        res = self.compter([
            texte("avant c05|c06|c07|c08|c09|c10|c11|c12|c13|c14| après"),
            resultat([{"type": "text", "text": "a10|a11|a12|a13|a14|a15|a16|a17|a18|a19|"}]),
            {"type": "assistant", "message": {"role": "assistant", "content":
                "c00|c01|c02|c03|c04|c05|c06|c07|c08|c09| et a00|a01|a02|a03|a04|a05|a06|a07|a08|a09|"}},
            {"type": "user", "message": {"content": [
                {"type": "tool_result", "content": "measure-M009a, measure-M009a et baseline_step0"},
                {"type": "tool_use", "name": "Bash", "input": {"command": "ls shogen-j28/"}}]}},
            {"type": "summary", "summary": "sans message"}])
        self.assertEqual(res, {
            "evenements": 5,
            "resultats": {"FRAGMENT:adr0025_l14": [1], "measure-M009a": [[3, 2]], "baseline_step0": [[3, 1]]},
            "entrees": {"FRAGMENT:carto_l51": [0, 2], "FRAGMENT:adr0025_l14": [2], "shogen-j28": [[3, 1]]},
            "fragments_l51_l14": {"resultats": 1, "entrees": 3}})

    def test_ligne_introuvable_controle_impossible(self):
        """Lignes de D.2 introuvables par leur sha256 : sortie non nulle, motif nommé, aucun compte imprimé."""
        code, sortie, err = lancer([texte("bonjour")], mode="absentes")
        self.assertNotEqual(code, 0)
        self.assertIn("ligne carto_l51 introuvable par sha : contrôle impossible", err)
        self.assertEqual(sortie, "")

    def test_doublure_refuse_le_depot(self):
        """Garde du témoin : toute lecture sous le dépôt autre que la ligne servie est refusée par la doublure."""
        code, _sortie, err = lancer([], chemin="/home/user/shogen/docs/transcription.txt")
        self.assertNotEqual(code, 0)
        self.assertIn("lecture refusée par la doublure", err)


class Empreintes(unittest.TestCase):
    def test_fm11_verse_a_l_octet(self):
        with open(FM11, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), SHA_FM11)

    def test_sommes_couvrent_script_et_sorties(self):
        """SHA256SUMS liste fm11.py et chaque sortie de sorties-fm11/, une fois chacun, au sha256 du fichier."""
        with open(os.path.join(ICI, "SHA256SUMS"), encoding="utf-8") as f:
            lignes = [x.split(" *", 1) for x in f.read().splitlines()]
        listes = [c for _s, c in lignes]
        attendus = {"fm11.py"} | {"sorties-fm11/" + x for x in os.listdir(os.path.join(ICI, "sorties-fm11"))}
        self.assertEqual(sorted(attendus - set(listes)), [], "fichiers non listés")
        self.assertEqual(len(listes), len(set(listes)), "chemin listé deux fois")
        for s, c in lignes:
            with open(os.path.join(ICI, c), "rb") as f:
                self.assertEqual(hashlib.sha256(f.read()).hexdigest(), s, c)
