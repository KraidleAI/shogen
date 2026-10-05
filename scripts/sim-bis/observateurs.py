"""Observateurs du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-6 ; E-S-17 à E-S-22) : validité de
quatre observateurs par fenêtre, M_j, votes « écart » par (observateur, hôte, classe), défauts locaux, artefacts
simultanés, consolidation au quorum q_j = ⌊M_j/2⌋ + 1 (vote tout axe) et « ok » consolidé, en masques entiers (bit j =
fenêtre T_début + j·w, comme calendrier.py et sources.py). SB-6a : flux des composants pré-déclarés, comptage par plans
de bits, quorum par fenêtre, statuts et votes d'un observateur, consolidation (D, ok) de chaque série. SB-6b : couche
d'une réplication, validité des observateurs (absences D-1, dégradations D-2 à D-5, pannes de paires, perte, repli M =
3). Aucun flottant hors des tirages, aucune fonction transcendante, aucune puissance."""
import functools

import aleas
import commun
import sources


def flux(prm: dict, cellule: str, i: int, composant: str, indice: int):
    """aleas.flux d'un composant pré-déclaré dans observateurs.composants de parametres.json (liste fermée, disjointe de
    sources.composants), sinon OBSERVATEURS/composant."""
    if composant not in prm["observateurs"]["composants"]:
        raise commun.Refus("OBSERVATEURS/composant", f"{composant!r} : non déclaré dans parametres.json")
    return aleas.flux(prm["aleas"], cellule, i, composant, indice)


def compter(masques: list) -> list:
    """Plans de bits [p0, p1, p2] du nombre, fenêtre par fenêtre, de masques à 1 (additionneur à retenue sur trois
    plans ; au plus 7 masques, sinon OBSERVATEURS/compte)."""
    if len(masques) > 7:
        raise commun.Refus("OBSERVATEURS/compte", f"{len(masques)} masques : au plus 7")
    plans = [0, 0, 0]
    for x in masques:
        for b in range(3):
            plans[b], x = plans[b] ^ x, plans[b] & x
    return plans


def egal(plans: list, v: int, grille: int) -> int:
    """Fenêtres de la grille où le nombre compté par `plans` vaut v (0 ≤ v ≤ 7)."""
    m = grille
    for b in range(3):
        m &= plans[b] if v >> b & 1 else ~plans[b]
    return m


class Quorum:
    """Quorum par fenêtre (E-S-22) des observateurs de masques de validité `valides` sur la grille : nombre[m] =
    fenêtres à M_j = m observateurs valides ; q_j = ⌊M_j/2⌋ + 1 (3 sur 4, 2 sur 3, 2 sur 2) ; fenêtre évaluable
    si M_j ≥ 2."""

    def __init__(self, valides: list, grille: int):
        self.valides, self.grille, pv = valides, grille, compter(valides)
        self.nombre = [egal(pv, m, grille) for m in range(len(valides) + 1)]
        self.evaluables = 0
        for m in range(2, len(valides) + 1):
            self.evaluables |= self.nombre[m]

    def atteint(self, masques: list) -> int:
        """Fenêtres évaluables où au moins q_j observateurs valides ont leur masque à 1 (le masque d'un observateur non
        valide n'est jamais compté)."""
        pc, out = compter([v & x for v, x in zip(self.valides, masques)]), 0
        for m in range(2, len(self.valides) + 1):
            for k in range(m // 2 + 1, m + 1):
                out |= self.nombre[m] & egal(pc, k, self.grille)
        return out


def consolider(etat: dict, quorum: Quorum, vues: dict) -> dict:
    """{(hôte, classe) : (D, ok)} (E-S-19, E-S-20, E-S-22). Pour l'observateur o et la série (u, c) de l'état vrai
    (sources.Replication.etat : panne, écart hors panne) : panne vue = panne & ~cache (o, u) (panne régionale non vue)
    & ~manque (o, u) (manque β, par hôte) ; écart vu = écart & ~manque (o, u, c) ; statut « panne » = panne vue | chemin
    (o, u) (échec de chemin seul, ε) | local (o) (défaut local : toutes les unités de toutes les classes) | artefact (o,
    u) ; vote « écart » = statut « panne » | écart vu (vote tout axe, deux types, Q-S-22). D : au moins q_j votes
    d'observateurs valides ; ok : au moins q_j observateurs valides à statut non panne. `vues` : masques de clés
    ("cache", o, u), ("manque", o, u), ("manque", o, u, c), ("chemin", o, u), ("local", o), ("artefact", o, u) ; clé
    absente : 0."""
    out, v = {}, vues.get
    for (u, c), (panne, ecart) in etat.items():
        votes, ok = [], []
        for o in range(len(quorum.valides)):
            p = ((panne & ~v(("cache", o, u), 0) & ~v(("manque", o, u), 0)) | v(("chemin", o, u), 0)
                 | v(("local", o), 0) | v(("artefact", o, u), 0))
            votes.append(p | (ecart & ~v(("manque", o, u, c), 0)))
            ok.append(quorum.grille & ~p)
        out[u, c] = (quorum.atteint(votes), quorum.atteint(ok))
    return out


@functools.lru_cache(maxsize=None)
def _uniforme(n: int):
    return aleas.Empirique([(j, 1) for j in range(n)])        # j uniforme sur 0..n − 1 (seuils exacts j/n)


def debuts(prm: dict, u, rho, horizon: int) -> list:
    """Débuts d'épisodes sur [0, horizon), dans l'ordre : tirages de Bernoulli de paramètre ρ·w/86 400 par fenêtre de
    grille, ρ par jour (forme de sources.incidents, pauses géométriques par table exacte)."""
    g, t, out = sources.Geometrique(rho * prm["calendrier"]["w"] / 86400, prm["aleas"]), -1, []
    while True:
        d = g.tirer(u, horizon - 1 - t)
        if d is None:
            return out
        t += d
        out.append(t)


class Couche:
    """Couche d'observateurs d'une réplication (E-S-17 à E-S-21) : paramètres, spécification de la cellule (`couche` :
    absences et dégradations, parts stationnaires par observateur ; paires, pannes de paires par jour ; perte, None ou
    durée nominale en fenêtres sur laquelle l'instant de la perte est tiré ; repli, M = 3), nom de cellule, indice i ≥
    0 et horizon T_max en fenêtres ; essais : {(composant, indice) : u} remplace les flux nommés (tests pas à pas)."""

    def __init__(self, prm, couche, cellule, i, horizon, essais=None):
        self.prm, self.couche, self.cellule, self.i, self.horizon = prm, couche, cellule, i, horizon
        self.essais, self.grille = essais or {}, (1 << horizon) - 1

    def u(self, composant, indice):
        return self.essais.get((composant, indice)) or flux(self.prm, self.cellule, self.i, composant, indice)

    def validites(self) -> list:
        """Masques de validité des M observateurs (E-S-17, E-S-18 ; grille de Q-S-11). Non valide : absence D-1
        (renouvellement stationnaire de part `absences`, longueurs observateurs.absences, flux « obs-absences » d'indice
        o) ; dégradation D-2 à D-5 (tirages indépendants par fenêtre de part `degradations`, flux « obs-degradations »
        d'indice o) ; panne de paire (débuts à `paires` par jour, flux « obs-paires » 0 ; paire uniforme parmi celles
        des observateurs présents, flux « obs-paires » 1 ; durée observateurs.duree_paire) ; perte définitive
        (observateur uniforme parmi les présents, instant uniforme sur la durée `perte`, jour puis fenêtre du jour, flux
        « obs-perte ») ; repli (observateur observateurs.repli absent toute la campagne, E-S-18). Durée de perte non
        multiple d'un jour : OBSERVATEURS/perte."""
        op, c, a = self.prm["observateurs"], self.couche, self.prm["aleas"]
        presents = [o for o in range(op["M"]) if not (c["repli"] and o == op["repli"])]
        inv, loi = [0 if o in presents else self.grille for o in range(op["M"])], sources.Empirique(op["absences"])
        for o in presents:
            if c["absences"]:
                q = sources.pause(c["absences"], loi.moyenne)
                inv[o] |= sources.masque(sources.alterner(self.u("obs-absences", o), loi, q, a, self.horizon))
            if c["degradations"]:
                p = c["degradations"]
                inv[o] |= sources.masque(sources.markov(self.u("obs-degradations", o), p, p, a, self.horizon))
        if c["paires"]:
            paires, v = [(x, y) for x in presents for y in presents if x < y], self.u("obs-paires", 1)
            for t in debuts(self.prm, self.u("obs-paires", 0), c["paires"], self.horizon):
                x, y = paires[_uniforme(len(paires)).tirer(v)]
                inv[x] |= ((1 << op["duree_paire"]) - 1) << t
                inv[y] |= ((1 << op["duree_paire"]) - 1) << t
        if c["perte"] is not None:
            fpj, n, u = 86400 // self.prm["calendrier"]["w"], c["perte"], self.u("obs-perte", 0)
            if n % fpj or n < fpj:
                raise commun.Refus("OBSERVATEURS/perte", f"{n} fenêtres : multiple entier d'un jour ({fpj}) attendu")
            o = presents[_uniforme(len(presents)).tirer(u)]
            t = fpj * _uniforme(n // fpj).tirer(u) + _uniforme(fpj).tirer(u)
            inv[o] |= self.grille >> t << t
        return [self.grille & ~x for x in inv]
