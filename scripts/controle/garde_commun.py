"""Bibliothèque commune des contrôles avant l'acte (lot GARDE-FOUS-ORCH ; G0 docs/adr-0028/G0-lots-DETTES.md, ajout
GF-0 ; adjudication de l'orchestrateur du 2026-10-10). Bibliothèque standard seule (R-8), Python 3.10 à 3.13.
GF-1, horloge et heures (E14) : l'horloge est lue par `date -u` en sous-processus, jamais par celle de Python ; les
tests la fixent par un faux `date` en tête du PATH. `horodatages_fautifs` juge chaque ligne hors code (accents graves)
et hors guillemets français : heure-future, une date du jour suivie (25 caractères au plus, sans autre date entre)
d'une heure plus tard que l'horloge + TOLERANCE_S, sans mot de PLAN dans les 40 caractères d'avant ; heure-approchee,
une heure écrite HH:Mx ou HH:xx. Une date d'un autre jour n'est pas jugée (échéance, veille). Limite : une heure
écrite sans sa date, ou une heure passée fausse, n'est pas vue.
GF-4 : interdits (E19, LA-N08 ; une seule source, jamais un nom de D.2 affiché), racines, analyse des lignes ajoutées
d'un diff, disque (E4 : refus sous 3 Gio libres, avertissement sous 6, avis Q-13 adopté)."""
import ast
import fnmatch
import functools
import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone

TOLERANCE_S = 120
PLAN = re.compile(r"(?i)(prévue?s?|échéance|jalon|d['’]ici|à partir de)")
DATE = r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
DATE_HEURE = re.compile("(" + DATE + ")(?:(?!" + DATE + ").){0,25}?"
                        r"(?<![0-9])([01][0-9]|2[0-3]):([0-5][0-9])(?::([0-5][0-9]))?(?![0-9])")
APPROCHEE = re.compile(r"(?<![0-9:])(?:[01][0-9]|2[0-3]):(?:[0-5]x|xx)(?![0-9A-Za-z_])")
MASQUE = re.compile("`[^`]*`|«[^»]*»")
RACINE_OUTILS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEUILS_GIO = (3, 6)
ENTETE = re.compile("@@ -([0-9]+)(?:,([0-9]+))? [+]([0-9]+)(?:,([0-9]+))? @@")


def maintenant():
    """Heure UTC lue par `date -u` (règle de l'investisseur : lire l'horloge avant d'écrire une date)."""
    s = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True, check=True).stdout
    return datetime.strptime(s.strip(), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def horodatages_fautifs(texte, horloge):
    """[(ligne, code, extrait)] : heure-future et heure-approchee, lignes comptées depuis 1."""
    fautes, borne, jour = [], horloge + timedelta(seconds=TOLERANCE_S), horloge.strftime("%Y-%m-%d")
    for n, ligne in enumerate(texte.split(chr(10)), 1):
        nue = MASQUE.sub(lambda m: " " * len(m.group()), ligne)
        for m in DATE_HEURE.finditer(nue):
            if m.group(1) != jour or PLAN.search(nue[max(0, m.start() - 40):m.start()]):
                continue
            h = datetime.strptime(f"{m.group(1)} {m.group(2)}:{m.group(3)}:{m.group(4) or '00'}", "%Y-%m-%d %H:%M:%S")
            if h.replace(tzinfo=timezone.utc) > borne:
                fautes.append((n, "heure-future", m.group(0).strip()))
        fautes += [(n, "heure-approchee", m.group(0)) for m in APPROCHEE.finditer(nue)]
    return fautes


def constante(chemin, nom):
    """Valeur littérale de `nom` dans un fichier Python, lue par ast sans exécuter le fichier."""
    with open(chemin, encoding="utf-8") as f:
        arbre = ast.parse(f.read())
    for n in arbre.body:
        if isinstance(n, ast.Assign) and any(isinstance(c, ast.Name) and c.id == nom for c in n.targets):
            return ast.literal_eval(n.value)
    raise LookupError(f"{nom} absent de {chemin}")


@functools.lru_cache(maxsize=1)
def interdits():
    """(motifs par composants, motifs de D.2). INTERDITS de enforcement/docs-sha256sums.py (égal à xtask/src/sg5.rs par
    un cas) ; noms de D.2 : `motifs` de fm11.py, jamais exécuté (il ouvrirait un interdit) ni affiché. Un préfixe sans
    barre finale (docs/15-) devient un motif de composant (15-*)."""
    pre = constante(os.path.join(RACINE_OUTILS, "enforcement", "docs-sha256sums.py"), "INTERDITS")
    d2 = constante(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fm11.py"), "motifs")
    motifs = [p.casefold().rstrip("/").split("/") for p in pre]
    for p, m in zip(pre, motifs):
        m[-1] += "" if p.endswith("/") else "*"
    return motifs, [re.compile(x) for x in d2]


def chemin_interdit(chemin):
    """Vrai si un composant finit en .jsonl, si des composants consécutifs suivent un motif interdit (toute copie,
    casse pliée) ou si un motif de D.2 paraît sous le dernier composant `scratchpad` (le chemin du scratchpad de la
    session en porte un : mesuré) ; chemin donné et chemin réel (liens suivis) jugés."""
    motifs, d2 = interdits()
    for c in {os.path.normpath(chemin), os.path.realpath(chemin)}:
        parts = [p for p in c.casefold().split(os.sep) if p not in ("", ".")]
        sous = c.split(os.sep)[max((i for i, p in enumerate(c.split(os.sep)) if p == "scratchpad"), default=-1) + 1:]
        if any(p.endswith(".jsonl") for p in parts) or any(r.search("/".join(sous)) for r in d2):
            return True
        for m in motifs:
            if any(all(map(fnmatch.fnmatchcase, parts[i:i + len(m)], m)) for i in range(len(parts) - len(m) + 1)):
                return True
    return False


def racine_dangereuse(racine, depot=None):
    """Racine qu'un parcours récursif ne prend jamais (E19) : /, le dépôt ou l'un de ses ancêtres, un dossier docs, un
    interdit."""
    r = os.path.realpath(racine)
    for d in {os.path.realpath(RACINE_OUTILS), os.path.realpath(depot or RACINE_OUTILS)}:
        if d == r or d.startswith(r.rstrip(os.sep) + os.sep):
            return True
    return "docs" in r.casefold().split(os.sep) or chemin_interdit(r)


def _chemin(x):
    x = x.split(chr(9))[0].strip().strip('"')
    return None if x == "/dev/null" else (x[2:] if x[:2] in ("a/", "b/") else x)


def analyser_diff(texte):
    """Diff unifié de git (-U0 ou avec contexte) : [{avant, apres, blocs [(a, b, c, d, lignes)], ajouts [(n, t)]}]."""
    fichiers, f, bloc, n = [], None, None, 0
    for ligne in texte.split(chr(10)):
        if ligne.startswith("diff --git "):
            f, bloc = {"avant": None, "apres": None, "blocs": [], "ajouts": []}, None
            fichiers.append(f)
        elif f is None:
            continue
        elif bloc is None and ligne.startswith(("--- ", "+++ ")):
            f["avant" if ligne[0] == "-" else "apres"] = _chemin(ligne[4:])
        elif ligne.startswith("@@ "):
            m = ENTETE.match(ligne)
            if not m:
                raise ValueError(f"en-tête de bloc illisible : {ligne[:80]}")
            bloc = (int(m[1]), int(m[2] or 1), int(m[3]), int(m[4] or 1), [])
            f["blocs"].append(bloc)
            n = bloc[2]
        elif bloc is not None and ligne[:1] in (" ", "-", "+"):
            bloc[4].append(ligne)
            if ligne[0] == "+":
                f["ajouts"].append((n, ligne[1:]))
            n += ligne[0] != "-"
    return fichiers


def etat_disque(chemin="/", min_gio=None):
    """(état, Gio libres) : refus sous max(3, min_gio) Gio (min_gio ne fait que serrer), avertissement sous 6."""
    libre = shutil.disk_usage(chemin).free / 2 ** 30
    if libre < max(SEUILS_GIO[0], min_gio or 0):
        return "refus", libre
    return ("avertissement" if libre < SEUILS_GIO[1] else "ok"), libre
