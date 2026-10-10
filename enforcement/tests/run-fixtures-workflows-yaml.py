"""Shōgen, lot DETTES-T5, DT5-8 (adjudication C-2 du 2026-10-09) : cas de enforcement/workflows-yaml.py, chacun dans un
arbre temporaire, sauf W-01 (l'arbre du dépôt). W-02 : la forme de DT4-a (« cas : » dans un nom d'étape en scalaire
simple). Lancé par l'interpréteur qui porte PyYAML (python3-yaml, docs/R-8-outillage.md). Sortie : 0 tout passe (CAS
cas joués, ni plus ni moins), 1 un cas échoue, 3 erreur."""
import os
import shutil
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(os.path.dirname(ICI), "workflows-yaml.py")
RACINE = os.path.dirname(os.path.dirname(ICI))
CAS = 11
NL = chr(10)
BON = NL.join(["name: w", "on: push", "jobs:", "  a:", "    runs-on: ubuntu-24.04", "    steps:", ""])
ok, ko = [], []


def controler(*argv, env=None):
    p = subprocess.run([sys.executable, "-B", SCRIPT, *argv], capture_output=True, text=True, timeout=60, env=env)
    return p.returncode, p.stdout, p.stderr


def arbre(fichiers, w):
    d = tempfile.mkdtemp(dir=w)
    os.makedirs(os.path.join(d, ".github", "workflows"))
    for nom, texte in fichiers.items():
        chemin = os.path.join(d, ".github", "workflows", nom)
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with open(chemin, "wb") as f:
            f.write(texte if isinstance(texte, bytes) else texte.encode("utf-8"))
    return d


def cas(nom, vrai, detail=""):
    (ok if vrai else ko).append(nom)
    if not vrai:
        print(f"ÉCHEC {nom} : {detail[:300]}", file=sys.stderr)


def refus(nom, w, fichiers, attendu):
    """Sortie 1 et un refus nommant `attendu` (fichier et motif), rien sur stdout."""
    code, out, err = controler(arbre(fichiers, w))
    cas(nom, code == 1 and out == "" and attendu in err, f"sortie {code} ; {err!r}")


def main():
    w = tempfile.mkdtemp()
    try:
        code, out, err = controler(RACINE)
        cas("W-01 arbre du dépôt conforme", code == 0 and out.startswith("workflows-yaml : conforme ("), err)
        dt4a = BON + "      - name: x (a ; cas : b)" + NL + "        run: c" + NL
        refus("W-02 forme de DT4-a refusée", w, {"g.yml": dt4a},
              "g.yml : ligne 7, colonne")
        refus("W-03 clé répétée refusée (job)", w, {"g.yml": BON + "  a:" + NL + "    runs-on: x" + NL},
              "g.yml : ligne 7, colonne 3 : clé répétée « a »")
        refus("W-04 clé répétée refusée (étape)", w, {"g.yml": BON + "      - run: a" + NL + "        run: b" + NL},
              "g.yml : ligne 8, colonne 9 : clé répétée « run »")
        refus("W-05 tabulation d'indentation refusée", w, {"g.yml": BON.replace("    steps:", chr(9) + "steps:")},
              "g.yml : ligne")
        vide = "g.yml : document vide ou autre qu'un mapping"
        refus("W-06 document vide refusé", w, {"g.yml": "# rien" + NL}, vide)
        refus("W-07 liste au premier niveau refusée", w, {"g.yml": "- a" + NL}, vide)
        refus("W-08 deux documents refusés", w, {"g.yml": BON + "---" + NL + BON}, "g.yml : ligne")
        refus("W-09 octets hors UTF-8 refusés, .yaml lu", w, {"g.yaml": BON.encode("utf-8") + b"# \xff" + NL.encode()},
              "g.yaml : octets hors UTF-8")
        d = arbre({"g.yml": BON, "sous/x.yml": "a: : b" + NL, "x.txt": "a: : b" + NL}, w)
        code, out, err = controler(d)
        cas("W-10 sous-dossier et .txt non lus ; aucun workflow refusé", code == 0 and "conforme (1 workflow(s)" in out
            and controler(arbre({}, w))[0] == 1, f"{code} {out!r} {err!r}")
        faux = os.path.join(w, "faux", "yaml")
        os.makedirs(faux)
        with open(os.path.join(faux, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("raise ImportError('absent')" + NL)
        sorties = [controler()[0], controler(RACINE, RACINE)[0], controler(w)[0],
                   controler(RACINE, env=dict(os.environ, PYTHONPATH=os.path.dirname(faux)))[0]]
        cas("W-11 erreurs en 3 (arguments, racine sans workflows, PyYAML absent)", sorties == [3] * 4, str(sorties))
    finally:
        shutil.rmtree(w, ignore_errors=True)
    joues = len(ok) + len(ko)
    print(f"workflows-yaml : {len(ok)} ok, {len(ko)} échec ({joues} cas joués, {CAS} exigés)")
    return 0 if not ko and joues == CAS else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERREUR FATALE : {e!r}", file=sys.stderr)
        raise SystemExit(3)
