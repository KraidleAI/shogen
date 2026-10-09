"""Commande `status` (CB-17 ; E-C-38 ; ADR-0029 §2.3 et §2.9 l.244 ; AVIS du G0, Q-D-03, point 3) : la santé seule,
lue au journal du pool (enregistrements `sante` de CB-11 et marqueurs), sans rien écrire ni prendre le verrou de
l'écrivain. CB-17a : lecture et jugement. Une ligne `lecture` est reconnue à ses premiers octets, sa première clé en
forme canonique (FORMAT §1.2, §9.1), et n'est jamais décodée : aucun statut de source, aucune valeur, aucun prix
n'entre au jugement. Jugement par fenêtre aux seuils scellés (ADR-0029 §2.3 ; égaux au bloc `degradation` de
`config/analyse.json`, test croisé) : D-1 aucun marqueur, ou aucune `sante` ; D-2 lecture partie plus de 5 s après
son instant planifié, ou non partie (règle Q-C-02 de l'AVIS, FORMAT §11.6) ; D-4 au moins 2 témoins sans réponse
retenue ; D-5 au moins 2 noms témoins non résolus (sans réponse retenue, rcode non nul, ou sans réponse A). D-3 n'est
pas jugé : le format de la sortie de `chronyc` n'est pas lu sur pièce (SHOGEN-S2BIS-CHRONYC-FORMAT-1) ; seuls les
relevés absents ou en erreur sont comptés.
CB-17b : état par fenêtre (w = 60 s, FORMAT §3.1), de la première que le journal admet au dernier marqueur, sur les
fichiers présents (la rétention locale peut en avoir retiré) ; rapport (santé seule, aucun nombre à virgule) ;
strates : stress le samedi et le dimanche UTC, calme sinon (ADR-0029 l.196).
CB-17c (AVIS Q-D-03, point 2) : résumé par jour, `[ws, codes]` de chaque fenêtre, publié au dépôt par la commande
`resume` : une projection du journal, recalculable ; grille bornée par le jour des fichiers présents (C-3).
CB-17d (AVIS Q-D-03, point 3) : avec un dépôt, `status` ajoute le compte à quorum (au moins deux observateurs
valides, ADR-0029 §2.2 pt 5) sur les résumés lisibles des autres, lus strictement (liste blanche), avec leur âge."""
import calendar
import hashlib
import json
import os
import re
import time

from shogen_s2bis.collecte import journal, tetes
from shogen_s2bis.collecte.journal import LIMITE
from shogen_s2bis.collecte.lecture import S

LECTURE, W = b'{"adresse":', 60                      # première clé d'une `lecture` canonique ; largeur des fenêtres
D2, D4, D5 = 5 * S, 2, 2                             # retard (µs), témoins sans réponse, noms non résolus
CODES, TAILLE = ("D-1", "D-2", "D-3", "D-4", "D-5"), 1 << 17                 # codes d'un résumé ; octets au plus
RESUME = re.compile("([a-z0-9]{1,16})-([0-9]{4}-[0-9]{2}-[0-9]{2})[.]resume")    # <observateur>-<jour>.resume


class RefusStatus(ValueError):
    """Refus nommé (`code`) : STATUS/journal."""
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


def fichiers(dossier, prefixe="pool"):
    """[(début du jour UTC, k, nom)] des fichiers du journal, dans l'ordre (jour, k entier) de la grammaire du FORMAT
    §6.1 ; un nom dont le jour n'est pas au calendrier est écarté (C-3) ; aucun fichier : STATUS/journal."""
    motif, r = re.compile(re.escape(prefixe) + "-([0-9]{4}-[0-9]{2}-[0-9]{2})-(0|[1-9][0-9]*)[.]jsonl"), []
    for n in os.listdir(dossier):
        try:
            if x := motif.fullmatch(n):
                r.append((calendar.timegm(time.strptime(x[1], "%Y-%m-%d")), int(x[2]), n))
        except ValueError:
            continue
    if not r:
        raise RefusStatus("STATUS/journal", f"aucun fichier du journal « {prefixe} »")
    return sorted(r)


def _au_dela(e, fin):
    """Enregistrement d'un jour postérieur à celui de son fichier (FORMAT §6.1 ; C-3) : `ws` à la fin du jour `fin`
    ou au-delà, ou `suivante` au-delà de `fin`."""
    return type(e.get("ws")) is int and e["ws"] >= fin or type(e.get("suivante")) is int and e["suivante"] > fin


def enregistrements(dossier, prefixe="pool"):
    """(enregistrement, ligne) hors `lecture`, dans l'ordre de `fichiers` ; un fichier s'arrête à sa première ligne
    coupée, illisible, sans `type` ni `seq`, ou d'un jour postérieur au sien (`_au_dela`)."""
    for debut, _k, n in fichiers(dossier, prefixe):
        with open(os.path.join(dossier, n), "rb") as f:
            while (ligne := f.readline(LIMITE)).endswith(b"\n"):
                if ligne.startswith(LECTURE):
                    continue
                try:
                    e = json.loads(ligne)
                except (ValueError, RecursionError):
                    break
                if type(e) is not dict or type(e.get("type")) is not str or type(e.get("seq")) is not int or _au_dela(
                        e, debut + 86400):
                    break
                yield e, ligne


def _repond(v):
    return type(v) is dict and v.get("statut") == "reponse"


def _resolu(v):
    return _repond(v) and v.get("rcode") == 0 and any(type(r) is list and r[1:2] == [1] for r in v["reponses"] or ())


def juger(sante):
    """(codes, relevé D-3 absent ou en erreur) d'une fenêtre close dont `sante` est la santé (None : aucune) ; sans
    santé lisible : D-1."""
    try:
        d2, d3, codes = sante["d2"], sante["d3"], []
        if d2["non_parties"] or d2["retard_max"] is not None and d2["retard_max"] > D2:
            codes.append("D-2")
        codes += ["D-4"] * (sum(not _repond(v) for v in sante["d4"]) >= D4)
        codes += ["D-5"] * (sum(not _resolu(v) for v in sante["d5"]) >= D5)
        return codes, type(d3) is not dict or "erreur" in d3 or d3.get("code") != 0
    except (KeyError, TypeError, AttributeError):
        return ["D-1"], False


def etat(dossier, prefixe="pool"):
    """{ws : codes} des fenêtres de la première admise au dernier marqueur, dernière `sante`, tête (seq, sha256) du
    dernier enregistrement lu, nombre de relevés D-3 absents ou en erreur."""
    plancher = fichiers(dossier, prefixe)[0][0] - 86400       # C-3 : jour du premier fichier, moins un jour (§6.1)
    premiere, en_cours, juges, derniere, tete, absents = None, {}, {}, None, None, 0
    for e, ligne in enregistrements(dossier, prefixe):
        tete = e["seq"], hashlib.sha256(ligne).hexdigest()
        if premiere is None and e["type"] in ("ouverture", "reprise") and type(e.get("suivante")) is int:
            premiere = e["suivante"]
        if e["type"] == "sante":
            en_cours[e.get("ws")] = derniere = e
        elif e["type"] == "marqueur" and type(e.get("ws")) is int:
            juges[e["ws"]], absent = juger(en_cours.pop(e["ws"], None))
            absents += absent
    debut = max(min([x for x in (premiere,) if x is not None] + list(juges), default=0), plancher)
    grille = {ws: juges.get(ws, ["D-1"]) for ws in range(debut, max(juges) + W, W)} if juges else {}
    return grille, derniere, tete, absents


def heure(ws):
    return time.strftime("%Y-%m-%d %H:%M", time.gmtime(ws))


def strate(ws):
    return "stress" if time.gmtime(ws).tm_wday in (5, 6) else "calme"


def resumes(dossier, observateur, prefixe="pool"):
    """{nom : octets} des résumés du journal, un par jour UTC : ligne canonique {jour, observateur, fenetres}, où
    `fenetres` liste [ws, codes] de chaque fenêtre du jour (codes vides : fenêtre valide)."""
    jours = {}
    for ws, codes in sorted(etat(dossier, prefixe)[0].items()):
        jours.setdefault(journal.jour(ws), []).append([ws, codes])
    return {f"{observateur}-{j}.resume": journal.canonique({"jour": j, "observateur": observateur, "fenetres": f})
            for j, f in jours.items()}


def lire_resume(chemin, observateur, jour):
    """{ws : valide} du résumé d'un autre observateur, ou le code de son refus : RESUME/taille (plus de TAILLE octets),
    RESUME/forme (pas une ligne canonique aux clés exactes), RESUME/champs (observateur ou jour autre que le nom,
    fenêtre hors du jour ou de la grille, codes hors de CODES, en double ou non triés, aucune fenêtre). Les codes
    sont reconnus avant d'être triés : un code qui n'est pas un texte est un refus, jamais une exception."""
    octets = tetes.lire_borne(chemin, TAILLE)                # fichier ordinaire seul, sans attente (CB-15f)
    if len(octets) > TAILLE:
        return "RESUME/taille"
    try:
        r = json.loads(octets)
        if type(r) is not dict or set(r) != {"fenetres", "jour", "observateur"} or journal.canonique(r) != octets:
            return "RESUME/forme"
        debut = calendar.timegm(time.strptime(jour, "%Y-%m-%d"))
    except (ValueError, RecursionError, journal.ErreurJournal):
        return "RESUME/forme"
    f = r["fenetres"]
    if (r["jour"], r["observateur"]) != (jour, observateur) or type(f) is not list or not f or not all(
            type(x) is list and len(x) == 2 and type(x[0]) is int and debut <= x[0] < debut + 86400 and x[0] % W == 0
            and type(x[1]) is list and all(c in CODES for c in x[1]) and x[1] == sorted(set(x[1])) for x in f):
        return "RESUME/champs"
    return {x[0]: not x[1] for x in f}


def quorum(grille, depot, observateur, maintenant):
    """Lignes du compte à quorum sur les fenêtres de `grille` : résumés des autres observateurs pour les jours de la
    grille, lus strictement ; M_j = 1 si la fenêtre est valide ici, plus un par autre observateur qui la dit valide ;
    âge (s) de chaque résumé lu, au bout de sa dernière fenêtre, à `maintenant` (µs). Dépôt illisible : une ligne qui
    le dit, le compte local reste (CB-15f)."""
    jours, autres, refus = {journal.jour(ws) for ws in grille}, {}, []
    try:
        noms = sorted(os.listdir(depot))
    except OSError as e:
        return [f"quorum : dépôt illisible ({type(e).__name__})"]
    for n in noms:
        if (x := RESUME.fullmatch(n)) and x[1] != observateur and x[2] in jours:
            try:
                lu = lire_resume(os.path.join(depot, n), x[1], x[2])
            except OSError:
                lu = "RESUME/lecture"
            refus.append(f"{n} ({lu})") if type(lu) is str else autres.setdefault(x[1], {}).update(lu)
    lignes = ["quorum : aucun résumé d'un autre observateur lisible"]
    if autres:
        compte = {"calme": 0, "stress": 0}
        for ws, codes in grille.items():
            compte[strate(ws)] += (not codes) + sum(v.get(ws, False) for v in autres.values()) >= 2
        lignes = [f"quorum hors D-3 (au moins 2 observateurs valides) : calme {compte['calme']} ; stress "
                  f"{compte['stress']}",
                  "résumés lus : " + " ; ".join(f"{o} jusqu'à {heure(max(v))} UTC (âge {maintenant // S - max(v) - W}"
                                                f" s)" for o, v in sorted(autres.items()))]
    return lignes + (["résumés refusés : " + " ; ".join(refus)] if refus else [])


def rapport(dossier, prefixe="pool", depot=None, observateur=None, maintenant=None):
    """Lignes du rapport : fenêtres, tête, disque, dégradations par code, dernière fenêtre, valides par strate ; avec
    un dépôt, le compte à quorum (`quorum`)."""
    grille, sante, tete, absents = etat(dossier, prefixe)
    lignes = [f"status : journal « {prefixe} », lecture seule"]
    if not grille:
        return lignes + ["fenêtres : aucune fenêtre close", f"tête : {tete and f'seq {tete[0]}, sha256 {tete[1]}'}"]
    debut, fin = min(grille), max(grille)
    disque = (sante or {}).get("disque")
    compte = {c: sum(c in x for x in grille.values()) for c in ("D-1", "D-2", "D-4", "D-5")}
    strates = {s: sum(not x and strate(ws) == s for ws, x in grille.items()) for s in ("calme", "stress")}
    return lignes + [
        f"fenêtres : de {heure(debut)} à {heure(fin)} UTC, {len(grille)} ; dernier marqueur : {heure(fin)} UTC",
        f"tête : seq {tete[0]}, sha256 {tete[1]}",
        f"disque : {disque['libre']} octets libres sur {disque['total']}" if type(disque) is dict and "libre" in disque
        else f"disque : non relevé ({disque})",
        f"dégradations : D-1 {compte['D-1']} ; D-2 {compte['D-2']} ; D-3 non jugé (SHOGEN-S2BIS-CHRONYC-FORMAT-1 ; "
        f"relevé absent ou en erreur : {absents}) ; D-4 {compte['D-4']} ; D-5 {compte['D-5']}",
        "dernière fenêtre : " + (f"dégradée ({', '.join(grille[fin])})" if grille[fin] else "valide"),
        f"fenêtres valides hors D-3 (compte local) : calme {strates['calme']} ; stress {strates['stress']}"] + (
        quorum(grille, depot, observateur, maintenant) if depot else [])
