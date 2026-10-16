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
ajoutée avant elle (même jour sans heure : non jugée).
Phase 2, groupe A (E6) : `etat_items`, état fermé ou ouvert de chaque item SHOGEN-… ou MONARK-… d'un texte (l'annexe
B), lu par marqueurs : mot fermé ou clos non nié dans les FENETRE caractères qui suivent l'item (sans traverser une
barre de tableau, un point-virgule ni un autre item), cellule d'une ligne de tableau dont la première cellule nomme
l'item, ou portée d'un en-tête « Items fermés … : » jusqu'à la fin du paragraphe ou un autre en-tête ; reste ouvert,
rouvert : ouvert. La dernière décision du texte l'emporte ; un item sans décision est ouvert.
Phase 2, groupe A (E12) : `motifs_suspects`, détecteur statique de retour arrière exponentiel (arbre de l'analyseur de
re, jamais d'exécution du motif ; avis c.1 de la revue) : sous une répétition de borne haute > 10, une répétition de
longueur variable en queue du corps dont les caractères peuvent commencer le corps (quantificateurs imbriqués :
`(a+)+`, motif de DT5 cité par E12), une alternative de largeur variable en queue dont la fin des branches longues peut
commencer le corps (`(a|aa)*`), ou deux branches d'une alternative du corps que rien ne sépare à leurs premières
positions connues (alternatives ambiguës) ; caractères jugés sur l'ASCII, é et l'espace insécable ; prudent : un motif
sûr peut être signalé (`(?:a+b|ac)*`). `_absorbe` : répétition variable du corps qui peut lire tout ce qui la suit
et un début du corps (`(.*,)*`). `motifs_ajoutes` : motifs des lignes ajoutées d'un diff analysé (premier
argument littéral, entier sur la ligne, d'un appel re.compile, match, search… en .py ; valeur d'une clé regex, pattern
ou motif et argument entre guillemets de grep, egrep ou rg en .yml) ; un motif construit par concaténation n'est pas lu.
`lignes_ajoutees(depot, plage=(base, tete))` : lignes ajoutées d'une plage de commits (poussée), mêmes règles."""
import ast
import fnmatch
import functools
import importlib
import io
import os
import re
import shutil
import subprocess
import tokenize
import warnings
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


def lignes_ajoutees(depot, env=None, racine=None, plage=None):
    """Lignes ajoutées de l'index (ou de l'index temporaire d'env) par rapport à HEAD, ou de la plage (base, tête),
    hors interdits : noms d'abord, puis diff des seuls chemins admis (le contenu d'un interdit n'est jamais lu),
    préfixes a/ et b/ forcés ; rend (fichiers analysés, nombre de fichiers écartés) ; racine : arbre où juger les
    interdits (dépôt jetable, L-12)."""
    sel = list(plage) if plage else ["--cached", "HEAD"]
    noms = git(depot, "diff", "--no-renames", "--name-only", "-z", *sel, env=env).split(chr(0))
    noms = [x for x in noms if x]
    admis = [x for x in noms if not chemin_interdit(os.path.join(racine or depot, x))]
    texte = git(depot, "diff", "--no-renames", "--no-color", "--no-ext-diff", "--no-textconv", "--src-prefix=a/",
                "--dst-prefix=b/", "-U0", *sel, "--", *[":(literal)" + x for x in admis], env=env) if admis else ""
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


ITEM = re.compile("(?<![A-Za-z0-9-])((?:SHOGEN|MONARK)-[A-Z0-9]+(?:-[A-Z0-9]+)*)(?![A-Za-z0-9-])")
CLOS = re.compile("(?i)(?<![a-zà-ÿ])(?:fermée?s?|clos|closes?)(?![a-zà-ÿ])")
ROUVRE = re.compile("(?i)(?<![a-zà-ÿ])(?:rouverte?s?|réouverte?s?|reste(?:nt)? [*]*ouverte?s?)(?![a-zà-ÿ])")
NIE = re.compile("(?i)(?:non|pas|jamais|ni) [*]*$")
EN_TETE = re.compile("(?i)(?<![a-zà-ÿ])(?:items?|fermetures)(?![a-zà-ÿ])[^:|]{0,300}?:")
FENETRE = 50


def marque(texte):
    """fermé, ouvert ou None : premier marqueur non nié du texte (fermé, clos ; reste ouvert, rouvert)."""
    for m in sorted([*CLOS.finditer(texte), *ROUVRE.finditer(texte)], key=lambda m: m.start()):
        ferme = CLOS.fullmatch(m[0]) is not None
        if not (ferme and NIE.search(texte[max(0, m.start() - 10):m.start()])):
            return "fermé" if ferme else "ouvert"
    return None


def etat_items(texte):
    """{item: (état, ligne de la décision)} : voir la docstring du module (E6)."""
    etats, portee = {}, None
    for n, ligne in enumerate(texte.split(chr(10)), 1):
        if not ligne.strip() or ligne.startswith(("#", "|")):
            portee = None
        if ligne.startswith("|"):
            cellules = [c.strip().strip("*").strip() for c in ligne.strip().strip("|").split("|")]
            if any(CLOS.match(c) for c in cellules[1:]):
                etats.update((i, ("fermé", n)) for i in ITEM.findall(cellules[0]))
        evts = [(m.end(), 0, m) for m in EN_TETE.finditer(ligne)] + [(m.start(), 1, m) for m in ROUVRE.finditer(ligne)]
        for pos, genre, m in sorted(evts + [(m.start(), 2, m) for m in ITEM.finditer(ligne)], key=lambda x: x[0]):
            if genre == 0:
                portee = "fermé" if marque(m[0]) == "fermé" or m[0].lower().startswith("fermetures") else None
            elif genre == 1:
                portee = None
            else:
                suite = re.split("[|;]|" + ITEM.pattern, ligne[m.end():m.end() + FENETRE])[0]
                etat = marque(suite) or portee
                etats[m[1]] = (etat, n) if etat else etats.get(m[1], ("ouvert", n))
    return etats


UNIVERS = frozenset(map(chr, range(128))) | {"é", chr(160)}
CATEGORIES = {"DIGIT": str.isdigit, "SPACE": str.isspace, "WORD": lambda c: c.isalnum() or c == "_",
              "LINEBREAK": lambda c: c == chr(10)}
UN = ("LITERAL", "NOT_LITERAL", "ANY", "IN")      # nœuds d'un caractère
REPETE = ("MAX_REPEAT", "MIN_REPEAT")              # répétitions qui reviennent en arrière (possessives exclues)
APPEL_RE = re.compile("(?<![A-Za-z0-9_.])re[.](?:compile|match|search|fullmatch|findall|finditer|sub|subn|split)[(]")
CLE_YAML = re.compile("^[ -]*[A-Za-z_-]*(?:regex|pattern|motif)s?: *(.+)$")
GREP = re.compile("(?<![A-Za-z0-9_-])(?:grep|egrep|rg)(?: +-[A-Za-z]+)* +(?:'([^']+)'|" + chr(34) + "([^" + chr(34)
                  + "]+)" + chr(34) + ")")


def _jeu(o, av):
    """Caractères (sur UNIVERS) qu'un nœud d'un caractère accepte."""
    if o != "IN":      # ANY : av vaut None, aucun caractère à lire
        return set(UNIVERS) if o == "ANY" else ({chr(av)} & UNIVERS or {"é"}) if o == "LITERAL" else set(
            UNIVERS - {chr(av)})
    s, nie = set(), False
    for op, x in av:
        if str(op) in ("LITERAL", "RANGE"):
            bas, haut = (x, x) if str(op) == "LITERAL" else x
            s |= {c for c in UNIVERS if bas <= ord(c) <= haut} or {"é"}
        elif str(op) == "CATEGORY":
            nom = str(x).replace("CATEGORY_", "")
            f = CATEGORIES.get(nom.replace("NOT_", ""), lambda c: True)
            s |= {c for c in UNIVERS if f(c) != nom.startswith("NOT_")}
        nie = nie or str(op) == "NEGATE"
    return set(UNIVERS) - s if nie else s


def _enfants(o, av):
    """Sous-séquences d'un nœud de l'arbre."""
    if o == "BRANCH":
        return list(av[1])
    if o == "GROUPREF_EXISTS":
        return [x for x in av[1:] if x is not None]
    return [av] if o == "ATOMIC_GROUP" else [av[-1]] if o in ("SUBPATTERN", "ASSERT", "ASSERT_NOT") + REPETE else []


def _premiers(seq, sens=1):
    """(caractères qui peuvent commencer seq, ou la finir avec sens=-1 ; seq peut être vide)."""
    acc = set()
    for op, av in list(seq)[::sens]:
        o = str(op)
        if o in UN:
            return acc | _jeu(o, av), False
        if o in ("AT", "ASSERT", "ASSERT_NOT"):
            continue
        parts = [_premiers(x, sens) for x in _enfants(o, av)] or [(set(UNIVERS), True)]      # renvoi : tout
        acc |= set().union(*(p[0] for p in parts))
        ou = o in ("BRANCH", "GROUPREF_EXISTS")
        if not ((any if ou else all)(p[1] for p in parts) or (o.endswith("REPEAT") and av[0] == 0)):
            return acc, False
    return acc, True


def _tous(seq):
    """Caractères que seq peut consommer."""
    return set().union(set(), *(_jeu(str(op), av) if str(op) in UN else _tous_noeud(str(op), av) for op, av in seq))


def _tous_noeud(o, av):
    return set() if o in ("ASSERT", "ASSERT_NOT") else set().union(set(), *(_tous(x) for x in _enfants(o, av)))


def _queues(seq):
    """(code, caractères de fin) des nœuds de longueur variable en queue de seq, suivis de nœuds qui peuvent être
    vides : répétitions (tout leur corps), alternatives de largeurs différentes (fin des plus longues)."""
    out = []
    for op, av in reversed(list(seq)):
        o = str(op)
        if o in REPETE and av[1] > av[0]:
            out.append(("quantificateurs-imbriques", _tous(av[2])))
        largeurs = [x.getwidth() for x in av[1]] if o == "BRANCH" else []
        if len(set(largeurs)) > 1:
            court = min(lo for lo, _hi in largeurs)
            out.append(("alternatives-ambigues", set().union(
                *(_premiers(x, -1)[0] for x, (_lo, hi) in zip(av[1], largeurs) if hi > court))))
        if o in REPETE + ("SUBPATTERN", "BRANCH"):
            out += [q for x in _enfants(o, av) for q in _queues(x)]
        if not _premiers([(op, av)])[1]:
            return out
    return out


def _lineaire(seq, k=6):
    """Caractères possibles aux k premières positions de seq ; None : inconnu au-delà (répétition, alternative)."""
    out = []
    for op, av in seq:
        o = str(op)
        if o in UN and len(out) < k:
            out.append(_jeu(o, av))
        elif o == "SUBPATTERN" and len(out) < k:
            out += _lineaire(av[-1], k - len(out))
            if out and out[-1] is None:
                return out
        elif o not in ("AT", "ASSERT", "ASSERT_NOT"):
            debut, vide = _premiers([(op, av)])
            return out + ([None] if vide or len(out) >= k else [debut, None])
    return out


def _ambigues(seq):
    """Une alternative du corps (hors répétitions imbriquées) dont deux branches peuvent être vides, ou peuvent lire
    un même début (rien ne les sépare aux premières positions connues ; un préfixe strict relève de _queues)."""
    for op, av in seq:
        if str(op) == "BRANCH":
            lin = [(_lineaire(x), _premiers(x)[1]) for x in av[1]]
            for i, (a, va) in enumerate(lin):
                for b, vb in lin[:i]:
                    ouvert = None in a[:len(b)] + b[:len(a)] or len(a) == len(b)
                    if va and vb or a and b and ouvert and not any(x and y and not x & y for x, y in zip(a, b)):
                        return True
        if str(op) in ("SUBPATTERN", "BRANCH") and any(_ambigues(x) for x in _enfants(str(op), av)):
            return True
    return False


def _deplie(seq):
    return [x for op, av in seq for x in (_deplie(av[-1]) if str(op) == "SUBPATTERN" else [(op, av)])]


def _absorbe(seq, debut):
    """Répétition variable du corps (groupes simples dépliés) qui peut lire tout ce qui la suit dans le corps et un
    début du corps : une itération peut en contenir plusieurs (`(.*,)*`)."""
    plat = _deplie(seq)
    return any(str(op) in REPETE and av[1] > av[0] and _tous(plat[k + 1:]) <= _tous(av[2]) and _tous(av[2]) & debut
               for k, (op, av) in enumerate(plat))


def motifs_suspects(motif):
    """Codes des formes à retour arrière exponentiel du motif (E12) : quantificateurs-imbriques,
    alternatives-ambigues, sous une répétition de borne haute > 10 ; motif-illisible si l'analyseur le refuse."""
    analyseur = getattr(re, "_parser", None) or importlib.import_module("sre_parse")      # 3.11+ ; 3.10
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pile, codes = [list(analyseur.parse(motif))], set()
    except Exception:
        return ["motif-illisible"]
    while pile:
        for op, av in pile.pop():
            pile += _enfants(str(op), av)
            if str(op) in REPETE and (av[1] == analyseur.MAXREPEAT or av[1] > 10):
                debut = _premiers(av[2])[0]
                codes |= {code for code, fin in _queues(av[2]) if fin & debut}
                codes |= {"alternatives-ambigues"} if _ambigues(av[2]) else set()
                codes |= {"quantificateurs-imbriques"} if _absorbe(av[2], debut) else set()
    return sorted(codes)


def _litteral(reste):
    """Premier argument de l'appel s'il est fait de littéraux de chaîne suivis de , ou ) sur la ligne, sinon None."""
    vus = []
    try:
        for jeton in tokenize.generate_tokens(io.StringIO(reste).readline):
            if jeton.type != tokenize.STRING:
                return "".join(vus) if vus and jeton.string in (",", ")") else None
            x = ast.literal_eval(jeton.string)
            vus.append(x.decode("latin-1") if isinstance(x, bytes) else x)
    except (tokenize.TokenError, SyntaxError, ValueError):
        return None
    return None


def motifs_ajoutes(fichiers):
    """[(chemin, ligne, motif, texte de la ligne)] des motifs écrits aux lignes ajoutées d'un diff analysé (E12)."""
    out = []
    for f in fichiers:
        chemin = f["apres"] or ""
        for n, x in f["ajouts"]:
            if chemin.endswith(".py"):
                vus = [_litteral(x[m.end():]) for m in APPEL_RE.finditer(x)]
            elif chemin.endswith((".yml", ".yaml")):
                cle = CLE_YAML.match(x)
                vus = [m[1] or m[2] for m in GREP.finditer(x)] + ([cle[1].strip().strip("'" + chr(34))] if cle else [])
            else:
                vus = []
            out += [(chemin, n, m, x) for m in vus if m]
    return out
