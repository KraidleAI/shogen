"""Bibliothèque commune des contrôles avant l'acte (lot GARDE-FOUS-ORCH ; G0 docs/adr-0028/G0-lots-DETTES.md, ajout
GF-0 ; adjudication de l'orchestrateur du 2026-10-10). Bibliothèque standard seule (R-8), Python 3.10 à 3.13.
GF-1, horloge et heures (E14) : l'horloge est lue par `date -u` en sous-processus, jamais par celle de Python ; les
tests la fixent par un faux `date` en tête du PATH. `horodatages_fautifs` juge chaque ligne hors code (accents graves)
et hors guillemets français : heure-future, une date du jour suivie (25 caractères au plus, sans autre date entre)
d'une heure plus tard que l'horloge + TOLERANCE_S, sans mot de PLAN dans les 40 caractères d'avant ; heure-approchee,
une heure écrite HH:Mx ou HH:xx. Une date d'un autre jour n'est pas jugée (échéance, veille). Limite : une heure
passée fausse hors d'une entrée datée n'est pas vue (heure sans sa date : vue depuis la phase 2, ci-dessous).
GF-4 : interdits (E19, LA-N08 ; une seule source, jamais un nom de D.2 affiché), racines, analyse des lignes ajoutées
d'un diff, disque (E4 : refus sous 3 Gio libres, avertissement sous 6, avis Q-13 adopté).
GF-3 : citations (E16, LA-N08) ; seule la forme stricte « … » (chemin:N) est refusée, les autres formes donnent un
avertissement compté au journal (avis c.4 adopté), à durcir après mesure.
GF-4b : lignes ajoutées de l'index (git diff --cached), noms d'abord, contenu des seuls chemins admis.
Relecture G2, C-3 : lignes ajoutées d'un index temporaire (env), préfixes a/ et b/ forcés quelle que soit la
configuration ; citations lues d'abord dans une surcouche (fichiers d'après un diff).
Relecture G2, C-5 : la forme stricte admet la référence écrite en code, (`chemin:N`) ou (`chemin`:N).
Relecture G2, C-11 : toute heure écrite dans les 25 caractères qui suivent une date du jour est jugée, la seconde
heure d'une plage comprise (seule la première l'était) ; une heure approchée en X majuscule (19:5X) est vue.
Contre-contrôle, R-9 : la date se lit même en code ou citée ; l'heure, en code, reste masquée.
Phase 2, L-1 (SHOGEN-GARDE-DATE-PASSEE-1) : heure-sans-date, toute heure jugée qui ne suit pas une date à 25 caractères
au plus ; `dates_passees`, heure-passee, une entrée datée ajoutée (titre ou ligne qui commence par la date et l'heure,
ou par un mot en capitale suivi de « daté du ») antérieure à la dernière entrée datée du fichier ou d'une entrée
ajoutée avant elle (même jour sans heure : non jugée)."""
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
HEURE = re.compile(r"(?<![0-9])([01][0-9]|2[0-3]):([0-5][0-9])(?::([0-5][0-9]))?(?![0-9])")
APPROCHEE = re.compile(r"(?<![0-9:])(?:[01][0-9]|2[0-3]):(?:[0-5][xX]|[xX]{2})(?![0-9A-Za-z_])")
MASQUE = re.compile("`[^`]*`|«[^»]*»")
RACINE_OUTILS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEUILS_GIO = (3, 6)
ENTETE = re.compile("@@ -([0-9]+)(?:,([0-9]+))? [+]([0-9]+)(?:,([0-9]+))? @@")
ESPACE = "[ " + chr(160) + "]?"
STRICTE = re.compile("«([^«»]+)»" + ESPACE + "[(]`?([^ ():`]+)`?:([0-9]+)(?:-([0-9]+))?`?[)]")
LIBRE = re.compile("«([^«»]+)»" + ESPACE + "[(]([^():]*?) ?l[.] ?([0-9]+)(?:-([0-9]+))?[)]")
ALIAS = {"JOURNAL": "JOURNAL.md", "annexe B": "docs/adr-0028/ANNEXE-B-items.md",
         "ADR-0028": "docs/adr-0028/ADR-0028-decisions-sortie-S2.md"}
HHMM = "(?:[ T](?:à )?([01][0-9]|2[0-3]):([0-5][0-9])(?::([0-5][0-9]))?)"
ENTREE = re.compile("^[>*#_ -]*(?P<x>(" + DATE + ")" + HHMM + ")|^[^a-zà-ÿ|]*(?P<y>[A-Z][a-zéèê]+ dat[ée]e? du `?("
                    + DATE + ")`?" + HHMM + "?)")
COUPE = re.compile("|".join(map(re.escape, ["[…]", "[...]", "…", "..."])))


def maintenant():
    """Heure UTC lue par `date -u` (règle de l'investisseur : lire l'horloge avant d'écrire une date)."""
    s = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True, check=True).stdout
    return datetime.strptime(s.strip(), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def horodatages_fautifs(texte, horloge):
    """[(ligne, code, extrait)] : heure-future et heure-approchee, lignes comptées depuis 1."""
    fautes, borne, jour = [], horloge + timedelta(seconds=TOLERANCE_S), horloge.strftime("%Y-%m-%d")
    for n, ligne in enumerate(texte.split(chr(10)), 1):
        nue = MASQUE.sub(lambda m: " " * len(m.group()), ligne)
        dates = list(re.finditer(DATE, ligne))      # date lue même en code ou citée (R-9)
        for m in HEURE.finditer(nue):
            d = next((d for d in reversed(dates) if d.end() <= m.start()), None)
            if not d or m.start() - d.end() > 25:
                fautes.append((n, "heure-sans-date", m.group(0)))
                continue
            if d.group(0) != jour:
                continue
            if PLAN.search(nue[max(0, d.start() - 40):d.start()]):
                continue
            h = datetime.strptime(f"{d.group(0)} {m.group(1)}:{m.group(2)}:{m.group(3) or '00'}", "%Y-%m-%d %H:%M:%S")
            if h.replace(tzinfo=timezone.utc) > borne:
                fautes.append((n, "heure-future", ligne[d.start():m.end()].strip()))
        fautes += [(n, "heure-approchee", m.group(0)) for m in APPROCHEE.finditer(nue)]
    return fautes


def entree_datee(ligne):
    """(extrait, (date, (h, m, s) ou None)) d'une entrée datée, sinon None."""
    m = ENTREE.match(ligne)
    if not m:
        return None
    g = m.groups()[1:5] if m["x"] else m.groups()[6:10]
    return m["x"] or m["y"], (g[0], tuple(int(x or 0) for x in g[1:]) if g[1] else None)


def dates_passees(avant, ajouts):
    """[(ligne, heure-passee, extrait)] : entrées datées ajoutées (ajouts [(n, texte)]) antérieures à la dernière entrée
    datée du texte d'avant ou d'une entrée ajoutée avant elle ; date seule : jugée sur le jour seulement."""
    fautes, cle = [], lambda k: (k[0], k[1] or (-1,))
    vues = [e[1] for e in map(entree_datee, avant.split(chr(10))) if e]
    ref = max(vues, key=cle, default=None)
    for n, x in sorted(ajouts):
        e = entree_datee(x)
        if not e:
            continue
        k = e[1]
        if ref and (k[0] < ref[0] or (k[0] == ref[0] and k[1] and ref[1] and k[1] < ref[1])):
            fautes.append((n, "heure-passee", e[0]))
        ref = max([k] + ([ref] if ref else []), key=cle)
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


def git(depot, *args, env=None):
    return subprocess.run(["git", "-C", depot, "-c", "core.quotePath=false", *args], capture_output=True, text=True,
                          check=True, env=env).stdout


def lignes_ajoutees(depot, env=None):
    """Lignes ajoutées de l'index (ou de l'index temporaire d'env) par rapport à HEAD, hors interdits : noms d'abord,
    puis diff des seuls chemins admis (le contenu d'un interdit n'est jamais lu), préfixes a/ et b/ forcés ; rend
    (fichiers analysés, nombre de fichiers écartés)."""
    noms = git(depot, "diff", "--cached", "--no-renames", "--name-only", "-z", "HEAD", env=env).split(chr(0))
    noms = [x for x in noms if x]
    admis = [x for x in noms if not chemin_interdit(os.path.join(depot, x))]
    texte = git(depot, "diff", "--cached", "--no-renames", "--no-color", "--no-ext-diff", "--no-textconv",
                "--src-prefix=a/", "--dst-prefix=b/", "-U0", "HEAD", "--", *[":(literal)" + x for x in admis],
                env=env) if admis else ""
    return analyser_diff(texte), len(noms) - len(admis)


def etat_disque(chemin="/", min_gio=None):
    """(état, Gio libres) : refus sous max(3, min_gio) Gio (min_gio ne fait que serrer), avertissement sous 6."""
    libre = shutil.disk_usage(chemin).free / 2 ** 30
    if libre < max(SEUILS_GIO[0], min_gio or 0):
        return "refus", libre
    return ("avertissement" if libre < SEUILS_GIO[1] else "ok"), libre


def plier(t):
    """Texte comparable : apostrophes et guillemets courbes pliés, `*` et accents graves retirés, blancs réduits."""
    return " ".join(t.translate({0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"', 0x2A: None, 0x60: None}).split())


def citation_lue(racine, chemin, n, m, citation, surcouche=None):
    """None si la citation se lit dans l'ordre entre les lignes n-2 et m+2 du fichier, sinon le code de la faute ;
    un chemin interdit n'est jamais ouvert ; le fichier de la surcouche (état d'après un diff) passe avant."""
    p, s = os.path.join(racine, chemin), os.path.join(surcouche or racine, chemin)
    if chemin_interdit(p) or chemin_interdit(s):
        return "citation-interdite"
    p = s if os.path.isfile(s) else p
    if not os.path.isfile(p):
        return "reference-introuvable"
    with open(p, encoding="utf-8", errors="replace") as f:
        lignes = f.read().split(chr(10))
    lignes = lignes[:-1] if lignes[-1] == "" else lignes
    if not 1 <= n <= m <= len(lignes):
        return "reference-hors-fichier"
    zone, pos = plier(" ".join(lignes[max(0, n - 3):m + 2])), 0
    for fragment in map(plier, COUPE.split(citation)):
        pos = zone.find(fragment, pos) if fragment else pos
        if pos < 0:
            return "citation-absente"
        pos += len(fragment)
    return None


def citations(texte, racine, surcouche=None):
    """(refus, avertissements), listes de (ligne, code, référence). Forme stricte « … » (chemin:N) ou (chemin:N-M) :
    refus si la citation ne se lit pas, si la ligne sort du fichier ou si le fichier est interdit ; chemin introuvable :
    avertissement. Forme libre « … » (nom l.N), nom résolu par ALIAS : avertissement (citation-libre, ou
    citation-libre-absente), refus si le fichier est interdit."""
    refus, avert = [], []
    for forme, motif in (("stricte", STRICTE), ("libre", LIBRE)):
        for x in motif.finditer(texte):
            ligne, nom = texte.count(chr(10), 0, x.start()) + 1, x[2].strip().strip("`")
            chemin, n = ALIAS.get(nom, nom), int(x[3])
            code = citation_lue(racine, chemin, n, int(x[4] or n), x[1], surcouche)
            if code == "citation-interdite" or (forme == "stricte" and code not in (None, "reference-introuvable")):
                refus.append((ligne, code, "une référence interdite" if code == "citation-interdite" else nom))
            elif forme == "stricte" and code:
                avert.append((ligne, code, nom))
            elif forme == "libre":
                avert.append((ligne, "citation-libre-absente" if code == "citation-absente" else "citation-libre", nom))
    return refus, avert
