"""Aléas du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-1 ; E-S-41, E-S-42, E-S-43) : flux par
(cellule, réplication, composant, indice) dérivés de SHA-256, tables de seuils exactes et tirages par comparaison de
random() à ces seuils (Bernoulli, loi empirique, loi géométrique), sans aucune fonction transcendante. seuil(x) est le
plus petit flottant binaire64 au moins égal au rationnel x : pour tout flottant u, u < seuil(x) ⇔ u < x, donc chaque
tirage tranche exactement contre la valeur rationnelle."""
import bisect
import hashlib
import math
import random
from fractions import Fraction

import commun


def _texte(v, nom: str) -> str:
    if type(v) is str and v != "" and v.isascii() and "|" not in v:
        return v
    raise commun.Refus("ALEAS/champ", f"{nom} = {v!r} : texte ASCII non vide, sans « | »")


def _rang(v, nom: str) -> str:
    if type(v) is int and v >= 0:
        return str(v)
    raise commun.Refus("ALEAS/champ", f"{nom} = {v!r} : entier ≥ 0")


def chaine(a: dict, cellule: str, i: int, composant=None, indice=None) -> str:
    """« <prefixe>|<graine>|<cellule>|<i> », suivie de « |<composant>|<indice> » pour un flux (E-S-41) ; entiers en
    décimal sans zéro de tête. `a` : section « aleas » de parametres.json."""
    champs = [a["prefixe"], str(a["graine"]), _texte(cellule, "cellule"), _rang(i, "i")]
    if composant is not None or indice is not None:
        champs += [_texte(composant, "composant"), _rang(indice, "indice")]
    return "|".join(champs)


def graine_flux(a: dict, cellule: str, i: int, composant: str, indice: int) -> int:
    """Entier big-endian des 8 premiers octets de SHA-256 de la chaîne ASCII du flux (E-S-41) ; composant et indice
    exigés tous deux (sinon ALEAS/champ : sans eux, la chaîne serait celle de la graine de règle ; C-4 de la G2)."""
    c = chaine(a, cellule, i, _texte(composant, "composant"), indice)
    return int.from_bytes(hashlib.sha256(c.encode("ascii")).digest()[:8], "big")


def flux(a: dict, cellule: str, i: int, composant: str, indice: int):
    """Méthode random() liée d'un random.Random semé par graine_flux : la seule méthode appelée (E-S-42)."""
    return random.Random(graine_flux(a, cellule, i, composant, indice)).random


def graine_regle(a: dict, cellule: str, i: int) -> str:
    """Graine de règle de la réplication : SHA-256 hexadécimal (minuscules) de « <prefixe>|<graine>|<cellule>|<i> »."""
    return hashlib.sha256(chaine(a, cellule, i).encode("ascii")).hexdigest()


def seuil(x: Fraction) -> float:
    """Plus petit flottant binaire64 ≥ x, x rationnel de [0, 1] : quotient entier arrondi (au plus proche, ou au moins
    à l'un des deux voisins), puis un pas vers le haut s'il est sous x ; comparaison exacte en Fraction (E-S-43)."""
    if not (type(x) is Fraction and 0 <= x <= 1):
        raise commun.Refus("ALEAS/seuil", f"{x!r} : Fraction de [0, 1] attendue")
    f = x.numerator / x.denominator
    return f if Fraction(f) >= x else math.nextafter(f, 2.0)


def bernoulli(u, s: float) -> bool:
    """Tirage de Bernoulli de paramètre p, s = seuil(p) : vrai ⇔ u() < p."""
    return u() < s


class Empirique:
    """Loi empirique d'un histogramme [(valeur, nombre)] à nombres entiers > 0 : seuils cumulés exacts
    C_j = (n_1 + … + n_j)/N, j < m ; tirage : valeur du plus petit j tel que u() < C_j (bisect)."""

    def __init__(self, histogramme: list):
        if not histogramme or any(type(n) is not int or n <= 0 for _v, n in histogramme):
            raise commun.Refus("ALEAS/empirique", f"{histogramme!r} : nombres entiers > 0 attendus")
        total, cumul, self.seuils = sum(n for _v, n in histogramme), 0, []
        for _v, n in histogramme[:-1]:
            cumul += n
            self.seuils.append(seuil(Fraction(cumul, total)))
        self.valeurs = [v for v, _n in histogramme]

    def tirer(self, u):
        return self.valeurs[bisect.bisect_right(self.seuils, u())]


class Geometrique:
    """Loi géométrique sur {1, 2, …} de paramètre p rationnel, 0 < p ≤ 1 : P(L = k) = p(1 − p)^(k − 1). Seuils
    C_k = 1 − (1 − p)^k, k = 1..m, m = `rangs` (ou le premier rang dont le seuil vaut 1) : (1 − p)^k encadré en entiers
    sur 2^-(53 + garde), arrondi par défaut et par excès, et seuil(C_k) retenu si les deux bornes le donnent (sinon
    refus nommé, jamais un seuil deviné). Au-delà du rang m, la loi est sans mémoire : L = m + L′, L′ tiré à nouveau."""

    def __init__(self, p: Fraction, rangs: int, garde: int):
        if not (type(p) is Fraction and 0 < p <= 1 and type(rangs) is int and rangs >= 1):
            raise commun.Refus("ALEAS/geometrique", f"p = {p!r}, rangs = {rangs!r} : Fraction de ]0, 1], rangs ≥ 1")
        q, echelle = 1 - p, 1 << (53 + garde)
        bas = haut = echelle
        self.seuils = []
        while len(self.seuils) < rangs:
            bas = bas * q.numerator // q.denominator
            haut = -(-haut * q.numerator // q.denominator)
            s = seuil(1 - Fraction(haut, echelle))
            if s != seuil(1 - Fraction(bas, echelle)):
                raise commun.Refus("ALEAS/seuil-ambigu", f"p = {p}, rang {len(self.seuils) + 1}, garde {garde}")
            self.seuils.append(s)
            if s == 1.0:
                break
        self.m = len(self.seuils)

    def tirer(self, u, borne: int):
        """L si L ≤ borne, None sinon ; un appel de u() par tranche de m rangs."""
        base = 0
        while base < borne:
            j = bisect.bisect_right(self.seuils, u())
            if j < self.m:
                return base + j + 1 if base + j + 1 <= borne else None
            base += self.m
        return None
