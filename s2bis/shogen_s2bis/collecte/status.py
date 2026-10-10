"""Commande `status` (CB-17 ; E-C-38 ; ADR-0029 §2.3 et §2.9 l.244 ; AVIS du G0, Q-D-03, point 3) : la santé seule,
lue au journal du pool (enregistrements `sante` de CB-11 et marqueurs), sans rien écrire ni prendre le verrou de
l'écrivain. CB-17a : lecture et jugement. Une ligne `lecture` est reconnue à ses premiers octets, sa première clé en
forme canonique (FORMAT §1.2, §9.1), et n'est jamais décodée : aucun statut de source, aucune valeur, aucun prix
n'entre au jugement. Jugement par fenêtre aux seuils scellés (ADR-0029 §2.3 ; égaux au bloc `degradation` de
`config/analyse.json`, test croisé) : D-1 aucun marqueur, ou aucune `sante` ; D-2 lecture partie plus de 5 s après
son instant planifié, ou non partie (règle Q-C-02 de l'AVIS, FORMAT §11.6) ; D-4 au moins 2 témoins sans réponse
retenue ; D-5 au moins 2 noms témoins non résolus (sans réponse retenue, rcode non nul, ou sans réponse A). DT6-e
(SHOGEN-S2BIS-CHRONYC-FORMAT-1) : D-3 jugé sur la sortie de `chronyc -n tracking`, forme lue sur pièce (FORMAT §13.3) :
aucun relevé lisible d'une fenêtre commencée moins de 120 s avant, borne d'erreur de plus de 1 s, ou statut de
synchronisation autre que Normal, Insert second, Delete second (FORMAT §17.2).
CB-17b : état par fenêtre (w = 60 s, FORMAT §3.1), de la première que le journal admet au dernier marqueur, sur les
fichiers présents (la rétention locale peut en avoir retiré) ; rapport (santé seule, aucun nombre à virgule) ;
strates : stress le samedi et le dimanche UTC, calme sinon (ADR-0029 l.196).
CB-17c (AVIS Q-D-03, point 2) : résumé par jour, `[ws, codes]` de chaque fenêtre, publié au dépôt par la commande
`resume` : une projection du journal, recalculable ; grille bornée par le jour des fichiers présents (C-3).
CB-17d (AVIS Q-D-03, point 3) : avec un dépôt, `status` ajoute le compte à quorum (au moins deux observateurs
valides, ADR-0029 §2.2 pt 5) sur les résumés lisibles des autres, lus strictement (liste blanche), avec leur âge.
DT6-c (SHOGEN-S2BIS-JOURNAL-FICHIER-SPECIAL-1) : un fichier du journal est ouvert sans attente et lu s'il est un fichier
ordinaire (`journal.ordinaire`) ; un tube nommé à son nom bloquait `status`. DT6-d (SHOGEN-S2BIS-STATUS-QUEUES-1) : un
fichier arrêté avant sa fin est nommé au rapport, avec son motif ; la grille compte GRILLE fenêtres au plus, au-delà le
refus STATUS/grille (un saut d'horloge en avant, que l'écrivain suit en nommant ses fichiers, faisait lever
MemoryError) ; un `disque` partiel est « non relevé »."""
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
GRILLE = 32 * 1440          # fenêtres jugées au plus (DT6-d) : 32 jours ; rétention locale de 7 jours (ADR-0029 §6)
D3_BORNE, D3_AGE = 10 ** 9, 120            # D-3 (DT6-e) : borne d'erreur, ns ; âge du dernier relevé lisible, s
CHRONY = re.compile("^(System time|Root delay|Root dispersion|Leap status) *: (.*)$", re.M)   # chronyc tracking
SYNCHRO, NS = ("Normal", "Insert second", "Delete second"), "([0-9]+)[.]([0-9]{9}) seconds"     # client.c, %L et %.9f
RESUME = re.compile("([a-z0-9]{1,16})-([0-9]{4}-[0-9]{2}-[0-9]{2})[.]resume")    # <observateur>-<jour>.resume


class RefusStatus(ValueError):
    """Refus nommé (`code`) : STATUS/journal, STATUS/grille."""
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


def enregistrements(dossier, prefixe="pool", arrets=None):
    """(enregistrement, ligne) hors `lecture`, dans l'ordre de `fichiers` ; un fichier s'arrête à sa première ligne
    coupée, illisible, sans `type` ni `seq`, ou d'un jour postérieur au sien (`_au_dela`) ; un fichier qui n'est pas un
    fichier ordinaire n'est pas lu (DT6-c). Chaque fichier arrêté avant sa fin est noté dans `arrets`, (nom, motif)
    (DT6-d)."""
    arrets = [] if arrets is None else arrets
    for debut, _k, n in fichiers(dossier, prefixe):
        try:                                                    # DT6-c : fichier ordinaire, ouvert sans attente
            fd = journal.ordinaire(os.path.join(dossier, n))
        except (journal.ErreurJournal, OSError) as x:
            arrets.append((n, "pas un fichier ordinaire" if type(x) is journal.ErreurJournal else
                           f"illisible ({type(x).__name__})"))
            continue
        with open(fd, "rb") as f:
            while (ligne := f.readline(LIMITE)).endswith(b"\n"):
                if ligne.startswith(LECTURE):
                    continue
                try:
                    e = json.loads(ligne)
                except (ValueError, RecursionError):
                    arrets.append((n, "ligne illisible"))
                    break
                if type(e) is not dict or type(e.get("type")) is not str or type(e.get("seq")) is not int:
                    arrets.append((n, "hors FORMAT"))
                    break
                if _au_dela(e, debut + 86400):
                    arrets.append((n, "jour postérieur au sien"))
                    break
                yield e, ligne
            else:
                if ligne:
                    arrets.append((n, "ligne coupée"))


def _repond(v):
    return type(v) is dict and v.get("statut") == "reponse"


def _resolu(v):
    return _repond(v) and v.get("rcode") == 0 and any(type(r) is list and r[1:2] == [1] for r in v["reponses"] or ())


def juger(sante):
    """Codes D-2, D-4, D-5 d'une fenêtre close dont `sante` est la santé (None : aucune) ; sans santé lisible : D-1.
    D-3 se juge sur les relevés de plusieurs fenêtres (`etat`, `trois`)."""
    try:
        d2, codes = sante["d2"], []
        if d2["non_parties"] or d2["retard_max"] is not None and d2["retard_max"] > D2:
            codes.append("D-2")
        codes += ["D-4"] * (sum(not _repond(v) for v in sante["d4"]) >= D4)
        codes += ["D-5"] * (sum(not _resolu(v) for v in sante["d5"]) >= D5)
        return codes
    except (KeyError, TypeError, AttributeError):
        return ["D-1"]


def chrony(d3):
    """(deux fois la borne d'erreur en ns, statut) d'un relevé D-3 lisible : `code` 0 (entier, booléen exclu), sortie
    de `chronyc -n tracking` où les lignes System time, Root delay, Root dispersion et Leap status figurent une fois
    chacune, valeurs en secondes à neuf décimales ; borne de la documentation de chrony, |System time| + Root
    dispersion + Root delay / 2 (FORMAT §13.3, §17.2 ; DT6-e) ; None sinon."""
    if type(d3) is not dict or type(d3.get("code")) is not int or d3["code"] != 0 or type(d3.get("sortie")) is not str:
        return None
    lus = CHRONY.findall(d3["sortie"])
    c = dict(lus)
    if len(lus) != 4 or len(c) != 4:
        return None
    formes = (("System time", " (slow|fast) of NTP time"), ("Root delay", ""), ("Root dispersion", ""))
    o, r, d = (re.fullmatch(NS + x, c[cle]) for cle, x in formes)
    if not (o and r and d):
        return None
    ns = [int(x[1]) * 10 ** 9 + int(x[2]) for x in (o, r, d)]
    return 2 * ns[0] + ns[1] + 2 * ns[2], c["Leap status"]


def trois(releve, ws):
    """D-3 de la fenêtre `ws` (ADR-0029 §2.3 ; DT6-e) : `releve` (ws de sa santé, deux fois la borne, statut), le
    dernier relevé lisible à elle, manque ou vient d'une fenêtre commencée D3_AGE s ou plus avant elle, ou dit une borne
    de plus de D3_BORNE, ou un statut hors SYNCHRO."""
    return releve is None or ws - releve[0] >= D3_AGE or releve[1] > 2 * D3_BORNE or releve[2] not in SYNCHRO


def etat(dossier, prefixe="pool", arrets=None):
    """{ws : codes} des fenêtres de la première admise au dernier marqueur, GRILLE au plus (sinon STATUS/grille, DT6-d),
    dernière `sante`, tête (seq, sha256) du dernier enregistrement lu ; fichiers arrêtés avant leur fin notés dans
    `arrets`. D-3 (DT6-e) : sur le dernier relevé lisible (`chrony`, `trois`)."""
    plancher = fichiers(dossier, prefixe)[0][0] - 86400       # C-3 : jour du premier fichier, moins un jour (§6.1)
    premiere, en_cours, juges, derniere, tete, releve = None, {}, {}, None, None, None
    for e, ligne in enregistrements(dossier, prefixe, arrets):
        tete = e["seq"], hashlib.sha256(ligne).hexdigest()
        if premiere is None and e["type"] in ("ouverture", "reprise") and type(e.get("suivante")) is int:
            premiere = e["suivante"]
        if e["type"] == "sante":
            en_cours[e.get("ws")] = derniere = e
            if type(e.get("ws")) is int and (lu := chrony(e.get("d3"))):
                releve = e["ws"], *lu
        elif e["type"] == "marqueur" and type(e.get("ws")) is int:
            codes = juger(en_cours.pop(e["ws"], None))
            juges[e["ws"]] = codes if codes == ["D-1"] or not trois(releve, e["ws"]) else sorted(codes + ["D-3"])
    debut = max(min([x for x in (premiere,) if x is not None] + list(juges), default=0), plancher)
    if juges and (max(juges) - debut) // W + 1 > GRILLE:                # DT6-d : avant d'allouer la grille
        raise RefusStatus("STATUS/grille", f"{(max(juges) - debut) // W + 1} fenêtres de {heure(debut)} à "
                          f"{heure(max(juges))} UTC, plus que {GRILLE} (32 jours) : saut d'horloge, ou journal "
                          "non purgé")
    grille = {ws: juges.get(ws, ["D-1"]) for ws in range(debut, max(juges) + W, W)} if juges else {}
    return grille, derniere, tete


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
        lignes = [f"quorum (au moins 2 observateurs valides) : calme {compte['calme']} ; stress {compte['stress']}",
                  "résumés lus : " + " ; ".join(f"{o} jusqu'à {heure(max(v))} UTC (âge {maintenant // S - max(v) - W}"
                                                f" s)" for o, v in sorted(autres.items()))]
    return lignes + (["résumés refusés : " + " ; ".join(refus)] if refus else [])


def rapport(dossier, prefixe="pool", depot=None, observateur=None, maintenant=None):
    """Lignes du rapport : fenêtres, tête, disque, dégradations par code, dernière fenêtre, valides par strate ; avec
    un dépôt, le compte à quorum (`quorum`)."""
    arrets = []
    grille, sante, tete = etat(dossier, prefixe, arrets)
    lignes = [f"status : journal « {prefixe} », lecture seule"]
    arretes = ["fichiers arrêtés avant leur fin : " + " ; ".join(f"{n} ({m})" for n, m in arrets)] if arrets else []
    if not grille:
        return lignes + ["fenêtres : aucune fenêtre close", f"tête : {tete and f'seq {tete[0]}, sha256 {tete[1]}'}",
                         *arretes]
    debut, fin = min(grille), max(grille)
    disque = (sante or {}).get("disque")
    compte = {c: sum(c in x for x in grille.values()) for c in CODES}
    strates = {s: sum(not x and strate(ws) == s for ws, x in grille.items()) for s in ("calme", "stress")}
    return lignes + [
        f"fenêtres : de {heure(debut)} à {heure(fin)} UTC, {len(grille)} ; dernier marqueur : {heure(fin)} UTC",
        f"tête : seq {tete[0]}, sha256 {tete[1]}",
        f"disque : {disque['libre']} octets libres sur {disque['total']}" if type(disque) is dict and {
            "libre", "total"} <= disque.keys() else f"disque : non relevé ({disque})",
        "dégradations : " + " ; ".join(f"{c} {compte[c]}" for c in CODES),
        "dernière fenêtre : " + (f"dégradée ({', '.join(grille[fin])})" if grille[fin] else "valide"),
        f"fenêtres valides (compte local) : calme {strates['calme']} ; stress {strates['stress']}",
        *arretes] + (quorum(grille, depot, observateur, maintenant) if depot else [])
