"""Exécution unique du rendu S2, en refus par défaut (ADR-0028 annexe D.4 b ; SHOGEN-RENDU-UNIQUE-1, EX-E1-1 ; G0
docs/adr-0028/G0-partie-2.md §C). Bibliothèque standard seule ; git et openssl lancés par listes d'arguments, jamais
par un shell ; rien n'est écrit (sorties : sous-lot C3). Une garde non construite, ou qui ne peut s'évaluer, refuse."""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone

SCRIPT = os.path.abspath(__file__)
LANGAGE = "shogen-paquet-v1"
HEX64, NOM = re.compile(r"[0-9a-f]{64}"), re.compile(r"[\w-][\w.-]*(/[\w-][\w.-]*)*", re.A)
CLES = {"commit_analyse": re.compile(r"[0-9a-f]{40}"),
        **dict.fromkeys(("sha256_script", "sommes", "cacert_sha256", "tsa_crt_sha256"), HEX64)}
N_JOURNAUX, CHEMINS = 3, ("s2-harness/shogen_s2", "s2-harness/tools")      # garde (2) : code d'analyse
SCEAU, DELAI = "docs/adr-0028/sceau", timedelta(hours=24)                  # gardes (5) et (6), G0 §C
PREFIXES = {"cacert_sha256": "2151b611", "tsa_crt_sha256": "8bfb0305"}     # annexe D.4 c (FreeTSA, FAITS §2)
MOIS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


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


def g_bloc(c: dict):
    """Paquet lu en octets (sha256 complet), puis son bloc machine (UTF-8 strict)."""
    with open(c["paquet"], "rb") as f:
        octets = f.read()
    c["sha_paquet"] = hashlib.sha256(octets).hexdigest()
    c["bloc"] = lire_bloc(octets.decode("utf-8"))


def g1(c: dict):
    """(1) sha256 complet du paquet présent dans JOURNAL.md à HEAD (git show HEAD:JOURNAL.md, blob brut)."""
    p = git(racine(c), "show", "HEAD:JOURNAL.md")
    if p.returncode:
        return f"JOURNAL.md illisible à HEAD ({p.stderr.decode('utf-8', 'replace').strip()})"
    c["journal_md"] = p.stdout.decode("utf-8", "replace")
    if not lignes_avec(c["journal_md"], c["sha_paquet"]):
        return f"sha256 du paquet {c['sha_paquet']} absent de JOURNAL.md à HEAD"


def g2(c: dict):
    """(2) git diff --quiet <commit_analyse> HEAD -- CHEMINS sort 0, et arbre de travail propre sur CHEMINS (git
    status : aucune modification, indexée ou non, aucun fichier non suivi ni ignoré)."""
    r, commit = racine(c), c["bloc"]["commit_analyse"]
    d = git(r, "diff", "--quiet", "--no-ext-diff", "--no-textconv", commit, "HEAD", "--", *CHEMINS)
    if d.returncode:
        return f"git diff --quiet {commit} HEAD -- {' '.join(CHEMINS)} : code {d.returncode}"
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
    """(4) sha256 de ce script égal à sha256_script du bloc (garde contre une édition accidentelle, pas une preuve)."""
    reel = sha256_fichier(SCRIPT)
    if reel != c["bloc"]["sha256_script"]:
        return f"sha256 du script {reel} ≠ sha256_script du bloc"


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


VOIES = (("a", voie_a),)                    # voie (b), fichier de go : sous-lot C2b


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


def verifier_gardes(depot: str, paquet: str, journaux: str, sommes: str, maintenant=None) -> list:
    """Évalue toutes les gardes de GARDES, dans l'ordre ; rend [(nom, motif)] des refus, liste vide si toutes sont
    levées. Une exception pendant une garde (fichier absent, bloc illisible, git en échec) est un refus. maintenant
    (datetime UTC) : horloge injectée en processus par les tests ; None en production (heure système)."""
    c, refus = {"depot": depot, "paquet": paquet, "journaux": journaux, "sommes": sommes, "maintenant": maintenant}, []
    for nom, garde in GARDES:
        try:
            motif = garde(c)
        except Exception as e:          # fail-closed : une garde qui ne s'évalue pas refuse
            motif = f"non évaluée ({type(e).__name__} : {e})"
        if motif:
            refus.append((nom, motif))
    return refus


def main(argv: list, maintenant=None) -> int:
    """--depot, --paquet, --journaux (dossier des journaux scellés), --sommes (fichier de sommes), --sortie (C3 ; rien
    n'y est écrit ici). Refus : gardes refusées sur stderr, code 2 ; sinon « gardes levées », code 0. L'horloge n'est
    jamais une option : maintenant n'est passé qu'en processus, par les tests."""
    p = argparse.ArgumentParser(prog="rendu_unique.py", description="exécution unique du rendu S2 (ADR-0028 D.4 b)")
    for opt in ("--depot", "--paquet", "--journaux", "--sommes", "--sortie"):
        p.add_argument(opt, required=True)
    a = p.parse_args(argv)
    refus = verifier_gardes(a.depot, a.paquet, a.journaux, a.sommes, maintenant)
    for nom, motif in refus:
        print(f"rendu_unique : refus {nom} : {motif}", file=sys.stderr)
    if refus:
        return 2
    print("gardes levées")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
