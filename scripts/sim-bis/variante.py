"""Variante non enroulée de la rotation (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-9 ; E-S-33 ; Q-S-09 (a)
de la PROPOSITION, adoptée par l'AVIS ; ADR-0029 l.141, l.143, l.205) : forme approchée de Harris (décalages de −N à N,
segment central, aucun enroulement), à décalages indépendants par unité (correction « minus » de Mrkvička et al.), sur
la suite comprimée de la strate. SB-9a : N, segment central, décalages SHA-256, série décalée sans enroulement.
SB-9b : même R, même seuil, même garde que la rotation enroulée (regle.decider et regle.complet), garde évaluée sur le
segment central. regle.py n'est pas modifié : la variante en emprunte les contrôles des entrées (regle._cle,
regle._controler) et la décision. Séries : entiers, bit t = position t de la suite comprimée. Entiers seuls : aucun
flottant, aucune puissance."""
import hashlib

import calendrier
import commun
import regle

ETIQUETTE = "minus"                     # E-S-33 : chaîne hachée « <graine>:<strate>:minus:<r>:<u> »


def demi(n: int, diviseur, prm: dict) -> int:
    """N = ⌊n/diviseur⌋ (E-S-33 ; Q-S-09 (a) : N = ⌊n/4⌋, sensibilité N = ⌊n/8⌋) ; diviseur pris dans la section
    « variante » de parametres.json (diviseur ou sensibilite), sinon VARIANTE/diviseur."""
    v = prm["variante"]
    if type(diviseur) is not int or diviseur not in (v["diviseur"], v["sensibilite"]):
        raise commun.Refus("VARIANTE/diviseur", f"{diviseur!r} : {v['diviseur']} ou {v['sensibilite']} attendu")
    return n // diviseur


def segment(n: int, N: int) -> int:
    """Masque du segment central [N, n − N) de la suite comprimée de longueur n."""
    return ((1 << (n - N)) - 1) & ~((1 << N) - 1)


def decalage(graine: str, strate: str, r: int, u: str, N: int) -> int:
    """s(r, u) (E-S-33) : (entier big-endian des 32 octets de SHA-256 de la chaîne ASCII
    « <graine>:<strate>:minus:<r>:<u> ») modulo 2N + 1, moins N : un décalage de {−N, …, N}. Graine, strate et unité
    contrôlées par regle._cle (refus nommés de la rotation enroulée) ; r de 1 à 9 999, sinon REGLE/entier."""
    regle._cle(graine, strate, 2 * N + 1, [u])
    if type(r) is not int or not 1 <= r <= regle.R_MAX:
        raise commun.Refus("REGLE/entier", f"r = {r!r} : entier de 1 à {regle.R_MAX} attendu")
    chaine = regle.SEP.join([graine, strate, ETIQUETTE, str(r), u])
    return int.from_bytes(hashlib.sha256(chaine.encode("ascii")).digest(), "big") % (2 * N + 1) - N


def decaler(x: int, s: int, n: int, N: int) -> int:
    """Série décalée de s, sans enroulement, vue sur le segment central : la valeur de la position t va en t + s (sens
    de la rotation enroulée, Q-R-02) ; |s| ≤ N, donc chaque position du segment reçoit une position de [0, n)."""
    return (x << s if s >= 0 else x >> -s) & segment(n, N)


def _entrees(series: dict, premier, graine: str, strate: str, n: int, n_s: int, prm: dict, R: int, diviseur):
    """(base, arguments de regle.decider et regle.complet, générateur des (K_H^(r), None)) : entrées contrôlées par
    regle._controler, N = demi(n, diviseur) ; K_H^(0), runs de I et unités à au moins un écart, sur le segment central ;
    n′ ≥ n_s/2 sur la suite (2·n ≥ n_s) ; l'unité `premier` n'est pas décalée. Une série nulle sur le segment peut y
    entrer par décalage : seul « au plus une série non nulle sur toute la suite » donne K_H^(r) = 0 pour tout r,
    exactement, sans hachage."""
    regle._controler(series, premier, graine, strate, n, prm)
    N = demi(n, prm["variante"]["diviseur"] if diviseur is None else diviseur, prm)
    c = segment(n, N)
    vus = [x & c for x in series.values()]
    i, unites, pleines = regle.deux(vus), sum(1 for x in vus if x), sum(1 for x in series.values() if x)

    def ks():
        for r in range(1, R + 1):
            yield regle.deux([x & c if u == premier else decaler(x, decalage(graine, strate, r, u, N), n, N)
                              for u, x in series.items()] if pleines >= 2 else []).bit_count(), None
    base = {"K": i.bit_count(), "runs": calendrier.runs(i), "unites": unites, "N": N}
    return base, (base["K"], base["runs"], unites, 2 * n >= n_s), ks()


def tester(series: dict, premier, graine: str, strate: str, n: int, n_s: int, prm: dict, R: int, diviseur=None) -> dict:
    """Variante pour une classe dans une strate, avec l'arrêt anticipé exact de regle.decider (mêmes compteurs C et C1,
    non décroissants en r) : rend regle.decider(), plus K (= K_H^(0)), runs et unités sur le segment, et N. diviseur :
    None (N = ⌊n/4⌋) ou la sensibilité (N = ⌊n/8⌋)."""
    base, a, ks = _entrees(series, premier, graine, strate, n, n_s, prm, R, diviseur)
    return {**regle.decider(*a, ks, R, prm), **base}


def deux_modes(series: dict, premier, graine: str, strate: str, n: int, n_s: int, prm: dict, R: int,
               diviseur=None) -> tuple:
    """(arrêt anticipé, R complet) de la variante sur les mêmes R décalages, calculés une fois (oracle d'équivalence,
    forme d'E-S-29 ; loi des K_H^(r), K_crit et moyenne exacte par regle.complet)."""
    base, a, ks = _entrees(series, premier, graine, strate, n, n_s, prm, R, diviseur)
    vals = list(ks)
    return {**regle.decider(*a, vals, R, prm), **base}, {**regle.complet(*a, vals, R, prm), **base}
