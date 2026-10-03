"""Exécution unique du rendu S2, en refus par défaut (ADR-0028 annexe D.4 b ; SHOGEN-RENDU-UNIQUE-1, EX-E1-1 ; G0
docs/adr-0028/G0-partie-2.md §C). Bibliothèque standard seule ; git et openssl lancés par listes d'arguments, jamais
par un shell. Une garde qui ne peut s'évaluer refuse ; gardes levées : runs nommés de l'enregistreur (sorties de D.4 b)
dans un répertoire temporaire voisin de --sortie, renommé en une fois ; tout échec : rien ne reste. --produire :
commande nommée de l'enregistreur (sortie de la table, recalcul-tiers, raw ; G0 §C, décisions Q1 à Q8)."""
from __future__ import annotations

import argparse
import contextlib
import glob
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from decimal import Decimal, localcontext

SCRIPT = os.path.abspath(__file__)
LANGAGE = "shogen-paquet-v1"
HEX64, NOM = re.compile(r"[0-9a-f]{64}"), re.compile(r"[\w-][\w.-]*(/[\w-][\w.-]*)*", re.A)
CLES = {"commit_analyse": re.compile(r"[0-9a-f]{40}"),
        **dict.fromkeys(("sha256_script", "sommes", "cacert_sha256", "tsa_crt_sha256"), HEX64)}
N_JOURNAUX, CHEMINS = 3, ("s2-harness/shogen_s2", "s2-harness/tools")      # garde (2) : code d'analyse
SCEAU, DELAI = "docs/adr-0028/sceau", timedelta(hours=24)                  # gardes (5) et (6), G0 §C
PREFIXES = {"cacert_sha256": "2151b611", "tsa_crt_sha256": "8bfb0305"}     # annexe D.4 c (FreeTSA, FAITS §2)
MOIS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
GO = re.compile(r"date: (\d{4}-\d\d-\d\dT\d\d:\d\d(?::\d\d(?:\.\d{1,6})?)?(?:Z|\+00:00))\nordre: exécuter sans ancre\n"
                r"signataire: investisseur\n")                          # fichier de go, voie (b) de (6), G0 §C
HARNAIS = os.path.dirname(os.path.dirname(SCRIPT))      # s2-harness du script : code scellé de l'extraction
NOMS_JOURNAUX = ("control.jsonl", "journal.jsonl", "raw.jsonl")   # exigés au bloc avant tout rendu (G0 §C, L3)
JETON = "SHOGEN_RENDU_PRODUCTION"    # temporaire voisin posé par produire_tout ; --produire refuse sans lui (G2, C-1)
# --- table des sorties (ADR-0028 D4, D2 pt 6, D5 ; G0 §C, décisions Q1 à Q4 du 2026-10-02) ---
T0, PLAGE_D5 = 1787770800, (1790273880, 1790435280)     # 2026-08-26T19:00:00Z ; plage fermée sur window_start
HORS_J28 = " ; plage D5 non passée : hors du segment (D2 pt 6 l'applique au J28)"      # décision Q2
SORTIES = (
    ("j14-principal", {"t0": T0, "t_fin": 1788980400}, (),       # [2026-08-26T19:00Z ; 2026-09-09T19:00Z) (D4)
     "hors décision, non confirmatoire (ADR-0028 D4, §1 bis.1 pt 9)" + HORS_J28),
    ("j14-second", {"t0": T0, "t_fin": 1788480060}, (),          # coupe ≤ 2026-09-04T00:00Z, plus w (D4, Q3)
     "sensibilité de la liste fermée (seconde coupe, décision 270), hors décision, non confirmatoire" + HORS_J28),
    ("j28", {"t0": T0, "n_fixe": 38600}, (PLAGE_D5,),            # 38 600e fenêtre distincte, plus w (D2 pt 6)
     "segment confirmatoire de la règle SHOGEN-CRITERE-R1-1 (D2 pt 6) ; la section [SENSIBILITÉ] (plage incluse) "
     "est hors décision, biaisée vers le haut par construction ; hors décision aussi (§1 bis.1 pt 9) : L&M (bloc 4), "
     "queues exactes, strate poolée, diagnostic de runs et drapeau « run maximal ≥ ℓ »"),        # G2 C-7, Q-3
)
# --- fin de la table des sorties ---
INCLUSE = ("sensibilité « plage incluse » de la liste fermée (D2 pt 7), hors décision, biaisée vers le haut par "
           "construction")                         # étiquette de la variante incluse du recalcul tiers (G2 C-7)
RUNS = ("suite", *(s[0] for s in SORTIES), "recalcul-tiers", "raw")     # Q8 : suite d'abord ; puis ordre de D.4 b
_SPEC = importlib.util.spec_from_file_location("oracle_record", os.path.join(HARNAIS, "tools", "oracle_record.py"))
orc = importlib.util.module_from_spec(_SPEC)            # enregistreur voisin (liste fermée des commandes)
_SPEC.loader.exec_module(orc)


def git(racine: str, *args: str) -> subprocess.CompletedProcess:
    """git en lecture seule sur racine, sans verrou optionnel ; variables GIT_* retirées (un GIT_DIR hérité
    désignerait un autre dépôt)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "--no-optional-locks", "-C", racine, *args], capture_output=True, env=env)


def openssl(*args: str) -> subprocess.CompletedProcess:
    """openssl résolu dans l'ordre du PATH (shutil.which), lancé sans shell ; absent : FileNotFoundError (refus)."""
    return subprocess.run([shutil.which("openssl") or "openssl", *args], capture_output=True)


def sha256_fichier(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()      # lecture par blocs (journaux volumineux)


def lignes_avec(texte: str, sha: str) -> list:
    """Numéros (base 0) des lignes de texte qui portent sha entier : ni chiffre hexadécimal avant, ni après."""
    motif = re.compile(rf"(?<![0-9a-fA-F]){sha}(?![0-9a-fA-F])")
    return [i for i, ligne in enumerate(texte.split("\n")) if motif.search(ligne)]


def lire_bloc(texte: str) -> dict:
    """Bloc machine du paquet (format fixé au G0 §C) : une seule ligne d'ouverture de bloc clôturé qui nomme le
    langage, de forme exacte « ```shogen-paquet-v1 », fermée par la première ligne « ``` » qui suit ; une clé par
    ligne, champs séparés par une espace : chaque clé de CLES une fois, « journal <nom> <sha256> » N_JOURNAUX fois à
    noms distincts ; hexadécimal en minuscules, sha complets. Clé absente, dupliquée, inconnue ou malformée :
    ValueError."""
    lignes = texte.split("\n")
    ouv = [i for i, x in enumerate(lignes) if re.match(r"\s*(`{3,}|~{3,})\s*" + LANGAGE, x)]
    if len(ouv) != 1 or lignes[ouv[0]] != "```" + LANGAGE or "```" not in lignes[ouv[0] + 1:]:
        raise ValueError(f"{len(ouv)} ouverture(s) de bloc {LANGAGE} ; une seule exigée, « ```{LANGAGE} », fermée")
    bloc, journaux = {}, {}
    for x in lignes[ouv[0] + 1:lignes.index("```", ouv[0] + 1)]:
        cle, *v = x.split(" ")
        if cle == "journal" and len(v) == 2 and NOM.fullmatch(v[0]) and HEX64.fullmatch(v[1]) and v[0] not in journaux:
            journaux[v[0]] = v[1]
        elif cle in CLES and len(v) == 1 and CLES[cle].fullmatch(v[0]) and cle not in bloc:
            bloc[cle] = v[0]
        else:
            raise ValueError(f"ligne du bloc malformée, dupliquée ou inconnue : {x!r}")
    absentes = [k for k in CLES if k not in bloc]
    if absentes or len(journaux) != N_JOURNAUX:
        raise ValueError(f"clé(s) absente(s) {absentes} ; lignes journal : {len(journaux)}, {N_JOURNAUX} exigées")
    return {**bloc, "journal": journaux}


def lire_sommes(chemin: str) -> dict:
    """Fichier de sommes au format de sha256sum : « <sha256> <espace ou *><nom> » par ligne, fin de ligne LF ou CRLF,
    lignes vides ignorées, hexadécimal rendu en minuscules ; ligne non conforme ou nom répété : ValueError."""
    table = {}
    with open(chemin, "rb") as f:
        for x in f.read().decode("utf-8").split("\n"):
            m = re.fullmatch(r"([0-9a-fA-F]{64}) [ *](.+?)\r?", x)
            if x.strip() and (not m or m.group(2) in table):
                raise ValueError(f"ligne du fichier de sommes non conforme ou nom répété : {x!r}")
            if m:
                table[m.group(2)] = m.group(1).lower()
    return table


def racine(c: dict) -> str:
    """Racine du dépôt (git rev-parse --show-toplevel), lue une fois ; dépôt illisible : ValueError."""
    if "racine" not in c:
        p = git(c["depot"], "rev-parse", "--show-toplevel")
        if p.returncode:
            raise ValueError(f"dépôt git illisible : {c['depot']}")
        c["racine"] = p.stdout.decode().strip()
    return c["racine"]


def head(c: dict) -> str:
    """Commit gardé : HEAD résolu une fois (git rev-parse --verify HEAD^{commit}, sha complet), lu par (1), (2), (4),
    la voie (b), l'enregistreur et la relecture (G2, C-2) ; illisible : ValueError."""
    if "head" not in c:
        p = git(racine(c), "rev-parse", "--verify", "HEAD^{commit}")
        if p.returncode:
            raise ValueError(f"HEAD illisible : {c['depot']}")
        c["head"] = p.stdout.decode().strip()
    return c["head"]


def g_bloc(c: dict):
    """Paquet lu en octets (sha256 complet), puis son bloc machine (UTF-8 strict)."""
    with open(c["paquet"], "rb") as f:
        octets = f.read()
    c["sha_paquet"] = hashlib.sha256(octets).hexdigest()
    c["bloc"] = lire_bloc(octets.decode("utf-8"))


def g1(c: dict):
    """(1) sha256 complet du paquet présent dans JOURNAL.md à HEAD (git show <head>:JOURNAL.md, blob brut)."""
    p = git(racine(c), "show", f"{head(c)}:JOURNAL.md")
    if p.returncode:
        return f"JOURNAL.md illisible à HEAD ({p.stderr.decode('utf-8', 'replace').strip()})"
    c["journal_md"] = p.stdout.decode("utf-8", "replace")
    if not lignes_avec(c["journal_md"], c["sha_paquet"]):
        return f"sha256 du paquet {c['sha_paquet']} absent de JOURNAL.md à HEAD"


def g2(c: dict):
    """(2) git diff --quiet <commit_analyse> <head> -- CHEMINS sort 0 ; arbre de travail jugé contre le commit gardé
    (git diff --quiet <head> -- CHEMINS sort 0 : RENDU-STATUS-HEAD-1) ; git status sur CHEMINS vide (aucune
    modification, indexée ou non, aucun fichier non suivi ni ignoré)."""
    r, commit = racine(c), c["bloc"]["commit_analyse"]
    d = git(r, "diff", "--quiet", "--no-ext-diff", "--no-textconv", commit, head(c), "--", *CHEMINS)
    if d.returncode:
        return f"git diff --quiet {commit} {head(c)} -- {' '.join(CHEMINS)} : code {d.returncode}"
    a = git(r, "diff", "--quiet", "--no-ext-diff", "--no-textconv", head(c), "--", *CHEMINS)
    if a.returncode:
        return f"arbre de travail ≠ commit gardé {head(c)} sur {' '.join(CHEMINS)} (git diff : code {a.returncode})"
    s = git(r, "status", "--porcelain", "--untracked-files=all", "--ignored", "--", *CHEMINS)
    if s.returncode or s.stdout:
        return f"arbre de travail modifié sur {' '.join(CHEMINS)} : {s.stdout.decode('utf-8', 'replace')[:300]!r}"


def g3(c: dict):
    """(3) et EX-E1-1 : sha256 du fichier de sommes égal à sommes du bloc ; sha256 complet de chaque journal du bloc
    (dossier des journaux scellés) égal à celui du bloc et à celui du fichier de sommes."""
    if sha256_fichier(c["sommes"]) != c["bloc"]["sommes"]:
        return "sha256 du fichier de sommes ≠ sommes du bloc"
    table, ecarts = lire_sommes(c["sommes"]), []
    for nom, attendu in c["bloc"]["journal"].items():
        reel = sha256_fichier(os.path.join(c["journaux"], nom))
        if not reel == attendu == table.get(nom):
            ecarts.append(f"{nom} : fichier {reel}, bloc {attendu}, sommes {table.get(nom)}")
    return "; ".join(ecarts) or None


def g4(c: dict):
    """(4) sha256 de ce script égal à sha256_script du bloc (garde contre une édition accidentelle, pas une preuve) et à
    celui de s2-harness/tools/rendu_unique.py au commit gardé ; enregistreur chargé (orc) égal à
    s2-harness/tools/oracle_record.py au commit gardé (G2, C-2)."""
    reel = sha256_fichier(SCRIPT)
    if reel != c["bloc"]["sha256_script"]:
        return f"sha256 du script {reel} ≠ sha256_script du bloc"
    lances = {"rendu_unique.py": c["bloc"]["sha256_script"], "oracle_record.py": sha256_fichier(orc.__file__)}
    for nom, attendu in lances.items():
        p = git(racine(c), "cat-file", "blob", f"{head(c)}:s2-harness/tools/{nom}")
        if p.returncode or hashlib.sha256(p.stdout).hexdigest() != attendu:
            return f"s2-harness/tools/{nom} au commit gardé {head(c)} ≠ fichier lancé ou chargé"


def gentime(texte: str) -> datetime:
    """genTime lu dans la sortie de openssl ts -reply -text : une seule ligne « Time stamp: », forme d'OpenSSL
    (« Oct  2 07:32:34 2026 GMT ») ou ISO 8601 (« 2026-10-02 07:32:34Z »), LF ou CRLF ; fraction de seconde : seconde
    suivante (T0 jamais avancé). Sinon ValueError."""
    x, = re.findall(r"^Time stamp: (.*?)\r?$", texte, re.M)
    m = re.fullmatch(r"(?P<b>[A-Z][a-z]{2}) +(?P<d>\d{1,2}) (?P<H>\d\d):(?P<M>\d\d):(?P<S>\d\d)(?P<f>\.\d+)? "
                     r"(?P<Y>\d{4}) GMT", x) or re.fullmatch(r"(?P<Y>\d{4})-(?P<m>\d\d)-(?P<d>\d\d) (?P<H>\d\d):"
                                                           r"(?P<M>\d\d):(?P<S>\d\d)(?P<f>\.\d+)?Z", x)
    if not m:
        raise ValueError(f"genTime illisible : {x!r}")
    g = m.groupdict()
    t = datetime(int(g["Y"]), MOIS.index(g["b"]) + 1 if "b" in g else int(g["m"]), int(g["d"]), int(g["H"]),
                 int(g["M"]), int(g["S"]), tzinfo=timezone.utc)
    return t + timedelta(seconds=1) if g["f"] and int(g["f"][1:]) else t


def voie_a(c: dict) -> datetime:
    """(6) voie (a) : chain/cacert.pem et chain/tsa.crt du dossier de sceau aux sha256 du bloc, valeurs du bloc aux
    préfixes de D.4 c ; openssl ts -verify aux arguments de scripts/sceau/verify.sh sort 0 ; serrage (journal G1) :
    le jeton porte sur les octets de PAQUET.sha256 (-data), manifeste qui liste le sha256 du paquet. Rend genTime."""
    d = os.path.join(racine(c), SCEAU)
    ca, tsa, tsr = (os.path.join(d, x) for x in ("chain/cacert.pem", "chain/tsa.crt", "paquet.tsr"))
    for chemin, cle in ((ca, "cacert_sha256"), (tsa, "tsa_crt_sha256")):
        if sha256_fichier(chemin) != c["bloc"][cle] or not c["bloc"][cle].startswith(PREFIXES[cle]):
            raise ValueError(f"{chemin} : sha256 ≠ {cle} du bloc, ou bloc hors du préfixe {PREFIXES[cle]} (D.4 c)")
    for objet in (("-queryfile", os.path.join(d, "paquet.tsq")), ("-data", os.path.join(d, "PAQUET.sha256"))):
        p = openssl("ts", "-verify", "-in", tsr, *objet, "-CAfile", ca, "-untrusted", tsa)
        if p.returncode:
            raise ValueError(f"openssl ts -verify {objet[0]} : code {p.returncode}")
    with open(os.path.join(d, "PAQUET.sha256"), "rb") as f:
        if not re.search(rb"^" + c["sha_paquet"].encode() + rb" [ *]", f.read(), re.M):
            raise ValueError("PAQUET.sha256 ne liste pas le sha256 du paquet")
    return gentime(openssl("ts", "-reply", "-in", tsr, "-text").stdout.decode("utf-8", "replace"))


def voie_b(c: dict) -> datetime:
    """(6) voie (b) : SCEAU/GO-sans-ancre.txt en UTF-8 strict, sans BOM, LF, les trois lignes exactes de GO (date ISO
    8601 UTC du calendrier) ; son sha256 complet dans JOURNAL.md à HEAD, première occurrence sur une ligne postérieure
    à la première qui porte le sha du paquet (scellement). S et Gc : premiers commits dont une ligne de JOURNAL.md
    porte le sha du paquet, celui du go (premier) ; refus si Gc = S, si S n'est pas ancêtre de Gc, si ct(Gc) ≤ ct(S),
    ou si la date du go n'est pas dans [ct(S) ; ct(Gc)] (D.4 c ; SHOGEN-GO-ORDRE-1, G2 C-3). Rend ct(Gc)."""
    with open(os.path.join(racine(c), SCEAU, "GO-sans-ancre.txt"), "rb") as f:
        octets = f.read()
    m = GO.fullmatch(octets.decode("utf-8"))
    if not m:
        raise ValueError("fichier de go hors du format du G0 §C")
    date = datetime.fromisoformat(m.group(1))           # date du calendrier, sinon ValueError
    sha = hashlib.sha256(octets).hexdigest()
    go, scelle = lignes_avec(c["journal_md"], sha), lignes_avec(c["journal_md"], c["sha_paquet"])
    if not (go and scelle and go[0] > scelle[0]):
        raise ValueError(f"sha256 du go {sha} absent de JOURNAL.md à HEAD, ou pas après la ligne du scellement")
    (s, ts), (gc, tg) = premier(c, c["sha_paquet"]), premier(c, sha)
    if gc == s or git(racine(c), "merge-base", "--is-ancestor", s, gc).returncode or tg <= ts:
        raise ValueError(f"commit du go {gc} : ni descendant strict ni postérieur au commit du scellement {s} (D.4 c)")
    if not ts <= date <= tg:
        raise ValueError(f"date du go {m.group(1)} hors de [{ts:%Y-%m-%dT%H:%M:%SZ} ; {tg:%Y-%m-%dT%H:%M:%SZ}] "
                         "(commit du scellement ; commit qui épingle le go)")
    return tg


def premier(c: dict, sha: str) -> tuple:
    """Premier commit dont JOURNAL.md porte une ligne qui contient sha entier (lignes_avec, comme (1) ; GO-PICKAXE-1) :
    candidats de git log --no-textconv --reverse --format="%H %ct" -G<sha> <head> -- JOURNAL.md (lignes ajoutées ou
    retirées qui contiennent sha), chacun confirmé sur git show <commit>:JOURNAL.md ; (sha du commit, date de commit
    UTC) ; aucun : ValueError."""
    p = git(racine(c), "log", "--no-textconv", "--reverse", "--format=%H %ct", "-G" + sha, head(c), "--", "JOURNAL.md")
    for commit, ct in (x.split() for x in (p.stdout.decode().splitlines() if not p.returncode else [])):
        j = git(racine(c), "show", f"{commit}:JOURNAL.md")
        if not j.returncode and lignes_avec(j.stdout.decode("utf-8", "replace"), sha):
            return commit, datetime.fromtimestamp(int(ct), timezone.utc)
    raise ValueError(f"aucun commit n'introduit une ligne qui porte {sha} dans JOURNAL.md à {head(c)}")


VOIES = (("a", voie_a), ("b", voie_b))


def preuves(c: dict) -> dict:
    """Voies d'ouverture de (6), évaluées une fois : {voie : (T0 ou None, motif)} ; une voie qui ne s'établit pas
    n'ouvre pas."""
    if "preuves" not in c:
        c["preuves"] = {}
        for v, f in VOIES:
            try:
                c["preuves"][v] = (f(c), "")
            except Exception as e:      # la voie ne s'établit pas
                c["preuves"][v] = (None, f"{type(e).__name__} : {e}")
    return c["preuves"]


def g5(c: dict):
    """(5) T_now ≥ T0 + 24 h, T0 le plus tardif des voies établies (genTime du jeton ; commit qui épingle le go) ; sans
    voie établie, T0 est indéterminé : refus. T_now : heure système, ou horloge injectée par les tests."""
    t0 = [t for t, _ in preuves(c).values() if t is not None]
    t = c["maintenant"] or datetime.now(timezone.utc)
    if not t0 or t < max(t0) + DELAI:
        return f"T_now {t:%Y-%m-%dT%H:%M:%SZ} < T0 + 24 h (T0 : {max(t0) if t0 else 'indéterminé'})"


def g6(c: dict):
    """(6) ouverture sur un jeton vérifié (voie a) ou sur un go épinglé (voie b) ; l'horloge seule n'ouvre jamais."""
    p = preuves(c)
    if all(t is None for t, _ in p.values()):
        return "ni jeton vérifié ni go épinglé : " + " ; ".join(f"voie ({v}) {m}" for v, (_, m) in p.items())


GARDES = (("bloc", g_bloc), ("(1)", g1), ("(2)", g2), ("(3)", g3), ("(4)", g4), ("(5)", g5), ("(6)", g6))


def evaluer_gardes(depot: str, paquet: str, journaux: str, sommes: str, maintenant=None) -> tuple:
    """Évalue toutes les gardes de GARDES, dans l'ordre ; rend ([(nom, motif)] des refus, liste vide si toutes sont
    levées ; contexte des gardes, lu par ouverture). Une exception pendant une garde (fichier absent, bloc illisible,
    git en échec) est un refus. maintenant (datetime UTC) : horloge injectée en processus par les tests ; None en
    production (heure système)."""
    c, refus = {"depot": depot, "paquet": paquet, "journaux": journaux, "sommes": sommes, "maintenant": maintenant}, []
    for nom, garde in GARDES:
        try:
            motif = garde(c)
        except Exception as e:          # fail-closed : une garde qui ne s'évalue pas refuse
            motif = f"non évaluée ({type(e).__name__} : {e})"
        if motif:
            refus.append((nom, motif))
    return refus, c


def verifier_gardes(depot: str, paquet: str, journaux: str, sommes: str, maintenant=None) -> list:
    """Refus de evaluer_gardes seuls."""
    return evaluer_gardes(depot, paquet, journaux, sommes, maintenant)[0]


def ouverture(c: dict) -> dict:
    """SHOGEN-RENDU-T0-1, gardes levées : voie(s) établie(s) de (6), T0 (le plus tardif, celui de la garde (5)) et
    genTime du jeton (voie (a), sinon None), en ISO 8601 UTC."""
    t = {v: d for v, (d, _m) in preuves(c).items() if d is not None}
    iso = lambda d: f"{d:%Y-%m-%dT%H:%M:%SZ}"
    return {"voie": "+".join(sorted(t)), "T0": iso(max(t.values())), "genTime": iso(t["a"]) if "a" in t else None}


def destination(sortie: str, motif) -> str:
    """Répertoire de sortie (D.4 b, G0 §C) : --sortie s'il est absent ; présent : refus, sauf --deviation <motif>
    (seconde exécution déclarée, motif d'une ligne non vide) : premier <sortie>.deviation-<k> libre, la première sortie
    n'est jamais touchée ; --deviation sans première exécution : refus ; entrée .<nom de --sortie>.* dans le dossier
    parent (débris d'une tentative interrompue, G2 C-4) : refus, avec ou sans --deviation. Refus : ValueError."""
    parent, nom = os.path.split(os.path.abspath(sortie))
    debris = sorted(glob.glob(os.path.join(glob.escape(parent), glob.escape(f".{nom}.") + "*")))
    if debris:
        raise ValueError(f"{', '.join(debris)} : tentative interrompue, à consigner au JOURNAL (heure, motif ; Q8), "
                         "puis à retirer à la main")
    if motif is None:
        if os.path.lexists(sortie):
            raise ValueError(f"{sortie} déjà présent : une seconde exécution est une déviation déclarée (--deviation)")
        return sortie
    if not os.path.lexists(sortie) or not motif.strip() or "\n" in motif or "\r" in motif:
        raise ValueError("--deviation exige une première exécution (--sortie présent) et un motif d'une ligne non vide")
    k = 1
    while os.path.lexists(f"{sortie}.deviation-{k}"):
        k += 1
    return f"{sortie}.deviation-{k}"


def _decimal(x) -> str | list:
    if isinstance(x, Decimal):
        return str(x)                                   # Decimal en chaîne, sous le contexte nommé (appelant)
    if isinstance(x, (set, frozenset)):
        return sorted(x)                                # r2, copie exacte : liste triée (SHOGEN-RECALCUL-JSON-COPIE-1)
    raise TypeError(f"{type(x).__name__} hors du JSON du recalcul tiers")


def produire(argv: list) -> int:
    """Commande nommée de l'enregistreur (liste fermée de oracle_record), lancée sur l'extraction du commit : une
    sortie de SORTIES (étiquette en tête, puis render_report avec ses seules options ; Q1, Q2, Q4), recalcul-tiers
    (JSON des quatre recompute_* par sortie, variante sans plage comprise ; Q6) ou raw (verdict de
    records.verifier_raw, code 0 quel que soit le verdict ; Q7, SHOGEN-RAW-FIN-1). Octets UTF-8 sur la sortie
    standard, capturée par l'enregistreur. Réservée à l'exécution unique (C-1) : JETON absent ou hors d'un répertoire
    existant dont le nom commence par un point, refus, code 2, sortie standard vide. Avertissements du lecteur capturés
    pendant le calcul, réécrits sans le dossier des journaux, écrits dans la sortie (C-5) : lignes [AVERTISSEMENT DU
    LECTEUR] après l'étiquette (ou le verdict), clé avertissements du JSON de recalcul-tiers."""
    v = os.environ.get(JETON, "")
    if not (os.path.isdir(v) and os.path.basename(v).startswith(".")):
        print(f"rendu_unique : refus production : commande nommée réservée à l'exécution unique ({JETON} absente ou "
              "hors d'un répertoire temporaire de production)", file=sys.stderr)
        return 2
    p = argparse.ArgumentParser(prog="rendu_unique.py --produire")
    p.add_argument("nom", choices=[s[0] for s in SORTIES] + ["recalcul-tiers", "raw"])
    p.add_argument("--journaux", required=True)
    a = p.parse_args(argv)
    if HARNAIS not in sys.path:
        sys.path.insert(0, HARNAIS)
    from shogen_s2 import lm, r1, r2, records, report
    c, j, raw = (os.path.join(a.journaux, n) for n in NOMS_JOURNAUX)
    with contextlib.redirect_stderr(io.StringIO()) as err:      # avertissements du lecteur, hors de stderr (C-5)
        if a.nom == "raw":
            try:
                v = records.verifier_raw(raw, j)
                texte = f"conforme — lectures {v['lectures']} ; avec octets {v['avec_octets']}"
            except ValueError as e:                     # verdict de refus : imprimé, l'exécution continue
                texte = f"refus — {e}"
            tete, corps = f"verdict raw.jsonl (records.verifier_raw ; SHOGEN-RAW-FIN-1) : {texte}", []
        elif a.nom == "recalcul-tiers":
            var = [*SORTIES, *((n + "-incluse", s, (), INCLUSE) for n, s, pl, _ in SORTIES if pl)]
            out = {n: {"etiquette": e, "segment": s, "plages": [list(x) for x in pl], **{k: f(c, j, pl, s) for k, f in (
                ("r1", r1.recompute_from_journal), ("d5", r1.recompute_d5_from_journal),
                ("lm", lm.recompute_lm_from_journal), ("r2", r2.recompute_r2_from_journal))}} for n, s, pl, e in var}
        else:
            nom, seg, pl, etiquette = next(x for x in SORTIES if x[0] == a.nom)
            tete, corps = f"[ÉTIQUETTE] {nom} : {etiquette}", [report.render_report(c, j, exclude_ranges=pl,
                                                                                     segment=seg)]
    avert = [x for x in err.getvalue().replace(os.path.join(a.journaux, ""), "").splitlines() if x.strip()]
    if a.nom == "recalcul-tiers":
        with localcontext(r1.contexte_decimal()):
            texte = json.dumps({**out, "avertissements": avert}, ensure_ascii=False, indent=1, sort_keys=True,
                               default=_decimal)
    else:                                           # étiquette (ou verdict), avertissements, puis le rendu
        texte = "\n".join([tete, *(f"[AVERTISSEMENT DU LECTEUR] {x}" for x in avert), *corps])
    sys.stdout.buffer.write((texte + "\n").encode("utf-8"))
    return 0


def produire_tout(c: dict, a, cible: str) -> int:
    """Gardes levées (G0 §C, Q5 à Q8) : runs RUNS de l'enregistreur sur l'extraction de HEAD, arrêt au premier échec,
    dans un répertoire temporaire voisin de la cible ; motif de déviation écrit ; enregistrement de rôle « rendu »
    (paquet.sha256, sceau.genTime, base = commit_analyse) relu par verifier (tree.sha256 recalculé) ; renommage en une
    fois, qui refuse une cible présente à cet instant (POSIX : création exclusive de la cible, puis renommage sur cette
    réserve vide ; Windows : os.rename ne remplace jamais ; RENDU-RENAME-POSIX-1). Tout échec : rien ne reste, code 1,
    heure et motif sur stderr. Sortie standard : chemins et sha256 seulement, aucun contenu de sortie."""
    tmp, fait = tempfile.mkdtemp(prefix=f".{os.path.basename(cible)}.", dir=os.path.dirname(os.path.abspath(cible))), 0
    reserve = None
    try:
        if a.deviation is not None:
            with open(os.path.join(tmp, "DEVIATION.txt"), "x", encoding="utf-8", newline="\n") as f:
                f.write(f"seconde exécution déclarée (ADR-0028 annexe D.4 b) ; première : {a.sortie} ; motif : "
                        f"{a.deviation}\n")
        o, r = ouverture(c), racine(c)
        os.environ[JETON] = tmp                     # hérité par les runs --produire (C-1)
        chemin, code = orc.enregistrer(tmp, "rendu", a.auteur, r, c["head"], RUNS, base=c["bloc"]["commit_analyse"],
                                       paquet_sha256=c["sha_paquet"], sceau_gentime=o["genTime"], journaux=a.journaux,
                                       arret_premier_echec=True)
        if code:                                    # motif nommé pour la ligne du JOURNAL (Q8), sans contenu
            with open(chemin, encoding="utf-8") as f:
                echecs = [(x["nom"], x["exit"]) for x in json.load(f)["runs"] if x["exit"]]
            raise RuntimeError(f"run en échec : {echecs}")
        rec = orc.verifier(chemin, "rendu", c["head"], r)          # exit 0, sha256 de chaque sortie, commit gardé
        if os.name != "nt":                         # POSIX : os.rename remplacerait une cible vide apparue
            os.mkdir(cible)                         # création exclusive : FileExistsError si la cible existe
            reserve = cible
        os.rename(tmp, cible)                       # sur la réserve vide ; Windows : FileExistsError si elle existe
        fait = 1
    except Exception as e:
        print(f"rendu_unique : échec de production à {datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ} : "
              f"{type(e).__name__} : {e} ; aucun répertoire de sortie", file=sys.stderr)
        return 1
    finally:
        os.environ.pop(JETON, None)
        if not fait:
            shutil.rmtree(tmp, ignore_errors=True)
            if reserve:
                with contextlib.suppress(OSError):
                    os.rmdir(reserve)               # réserve vide retirée ; non vide, elle n'est plus la nôtre
    print(f"sorties : {cible} (voie {o['voie']} ; T0 {o['T0']} ; genTime {o['genTime'] or '-'})")
    for x in rec["runs"]:
        print(f"  {x['nom']} {x['sortie']['sha256']} {x['sortie']['chemin']}")
    nom = os.path.basename(chemin)
    print(f"  enregistrement {sha256_fichier(os.path.join(cible, nom))} {nom}")
    return 0


def main(argv: list, maintenant=None) -> int:
    """--depot, --paquet, --journaux (dossier des journaux scellés), --sommes (fichier de sommes), --sortie, --auteur
    (identifiant de la liste blanche du lint) ; --deviation MOTIF (seconde exécution déclarée) ; --gardes-seules (rien
    de produit). Refus (auteur, sortie, gardes, noms des journaux, L3) sur stderr, code 2, rien d'écrit ; sinon
    « gardes levées », puis production (produire_tout). L'horloge n'est jamais une option : maintenant n'est passé
    qu'en processus, par les tests.
    --produire : commande nommée."""
    if argv[:1] == ["--produire"]:
        return produire(argv[1:])
    p = argparse.ArgumentParser(prog="rendu_unique.py", description="exécution unique du rendu S2 (ADR-0028 D.4 b)")
    for opt in ("--depot", "--paquet", "--journaux", "--sommes", "--sortie", "--auteur"):
        p.add_argument(opt, required=True)
    p.add_argument("--deviation", metavar="MOTIF")
    p.add_argument("--gardes-seules", action="store_true")
    a, refus = p.parse_args(argv), []
    try:
        cible = destination(a.sortie, a.deviation)
    except ValueError as e:
        refus.append(("sortie", str(e)))
    try:
        if not orc.auteur_admis(a.auteur):
            raise ValueError(f"{a.auteur!r} hors de la liste blanche de {orc.LINT}")
    except ValueError as e:                 # liste illisible comprise
        refus.append(("auteur", str(e)))
    if not refus:
        refus, c = evaluer_gardes(a.depot, a.paquet, a.journaux, a.sommes, maintenant)
        if not refus and sorted(c["bloc"]["journal"]) != sorted(NOMS_JOURNAUX):
            refus = [("noms", f"journaux du bloc {sorted(c['bloc']['journal'])}, exigés {list(NOMS_JOURNAUX)}")]
    for nom, motif in refus:
        print(f"rendu_unique : refus {nom} : {motif}", file=sys.stderr)
    if refus:
        return 2
    print("gardes levées", flush=True)
    return 0 if a.gardes_seules else produire_tout(c, a, cible)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
