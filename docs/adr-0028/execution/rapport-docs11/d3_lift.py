#!/usr/bin/env python3
"""SHOGEN-D3-LIFT-1 (ADR-0028 annexe B.42, B-2) : lift et identité phi de D3 (paquet §5), recalculés en
arithmétique exacte à partir des quatre comptes [n11 n10 n01 n00] imprimés au bloc 4 du rendu J28.

Rédacteur frais du rapport docs/11 (2026-10-04). Bibliothèque standard seule (fractions, decimal, re).
Aucune lecture de journal : la seule entrée est le rendu J28 versé à l'octet (bloc 4), lu par numéro de ligne.

Définitions (paquet §5 ; ADR-0028 D3) :
  n   = n11 + n10 + n01 + n00
  p_A = (n11 + n10)/n ; p_B = (n11 + n01)/n ; p_AB = n11/n
  lift = p_AB/(p_A·p_B) = n11·n/((n11 + n10)(n11 + n01))
  phi  = (n11·n00 − n10·n01)/√((n11 + n10)(n01 + n00)(n11 + n01)(n10 + n00))
  identité : phi = (lift − 1)·√(p_A·p_B/((1 − p_A)(1 − p_B)))
Contrôle exact de l'identité : phi² (rationnel) égal à (lift − 1)²·p_A·p_B/((1 − p_A)(1 − p_B)) (rationnel),
et signe de phi égal au signe de (lift − 1). Valeurs décimales : decimal, précision 80, puis arrondi d'affichage.

Usage : python3 -B d3_lift.py <rendu_j28> [--mutant]
  --mutant : remplace l'identité par une forme fausse (racine sans (1 − p)) pour montrer que l'auto-test échoue.
"""
import re
import sys
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from fractions import Fraction

getcontext().prec = 80

MUTANT = "--mutant" in sys.argv

# Plages de lignes du bloc 4 (repérées par grep -n, journal G1) : paires par strate.
PLAGES = {"calme": (435547, 435601), "stress": (435612, 435666)}
N_STRATE = {"calme": 24585, "stress": 11397}  # bloc 3, l.435451 et l.435471
SINGLETONS = {"binance", "gemini", "bitstamp"}  # bloc 6, l.435790, l.435792, l.435793
MOTIF = re.compile(
    r"^\s+(?P<a>[a-z_]+)×(?P<b>[a-z_]+)\s+\[(?P<n11>\d+) (?P<n10>\d+) (?P<n01>\d+) (?P<n00>\d+)\]\s+"
    r"φ=(?P<phi>-?[0-9.E-]+) \((?P<signe>[+−])\)\s*$"
)


def calcul(n11, n10, n01, n00):
    n = n11 + n10 + n01 + n00
    pa = Fraction(n11 + n10, n)
    pb = Fraction(n11 + n01, n)
    lift = Fraction(n11 * n, (n11 + n10) * (n11 + n01))
    num = n11 * n00 - n10 * n01
    den2 = (n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00)
    phi2 = Fraction(num * num, den2)
    if MUTANT:
        facteur2 = pa * pb  # forme fausse : sans (1 − p_A)(1 − p_B)
    else:
        facteur2 = pa * pb / ((1 - pa) * (1 - pb))
    ident2 = (lift - 1) ** 2 * facteur2
    signe_phi = (num > 0) - (num < 0)
    signe_lift = (lift > 1) - (lift < 1)
    identite_exacte = (phi2 == ident2) and (signe_phi == signe_lift)
    phi_dec = Decimal(num) / Decimal(den2).sqrt()
    ident_dec = (Decimal(lift.numerator) / Decimal(lift.denominator) - 1) * (
        Decimal(facteur2.numerator) / Decimal(facteur2.denominator)
    ).sqrt()
    return {
        "n": n, "pa": pa, "pb": pb, "lift": lift, "phi_dec": phi_dec, "ident_dec": ident_dec,
        "identite_exacte": identite_exacte,
    }


def auto_test():
    """Table calculée à la main, hors code : [2 1 1 6].
    n = 10 ; p_A = p_B = 3/10 ; p_AB = 2/10 ; lift = (2/10)/(9/100) = 20/9 ;
    phi = (2·6 − 1·1)/√(3·7·3·7) = 11/21 ; identité : (20/9 − 1)·√((9/100)/(49/100)) = (11/9)·(3/7) = 11/21.
    Seconde table : [0 5 5 90] (co-écart nul) : lift = 0 ; phi = (0 − 25)/√(5·95·5·95) = −25/475 = −1/19 ;
    identité : (0 − 1)·√((1/400)/(361/400)) = −1/19.
    """
    r = calcul(2, 1, 1, 6)
    assert r["n"] == 10
    assert r["lift"] == Fraction(20, 9), r["lift"]
    assert r["identite_exacte"], "identité fausse sur [2 1 1 6]"
    assert abs(r["phi_dec"] - Decimal(11) / Decimal(21)) < Decimal("1e-70")
    assert abs(r["ident_dec"] - Decimal(11) / Decimal(21)) < Decimal("1e-70"), r["ident_dec"]
    r = calcul(0, 5, 5, 90)
    assert r["lift"] == 0
    assert r["identite_exacte"], "identité fausse sur [0 5 5 90]"
    assert abs(r["phi_dec"] + Decimal(1) / Decimal(19)) < Decimal("1e-70")
    return True


def sig(x, chiffres):
    """Arrondi d'affichage à `chiffres` chiffres significatifs (ROUND_HALF_EVEN)."""
    if x == 0:
        return "0"
    e = x.adjusted()
    q = Decimal(1).scaleb(e - chiffres + 1)
    return str(x.quantize(q, rounding=ROUND_HALF_EVEN))


def main():
    chemin = [a for a in sys.argv[1:] if not a.startswith("--")][0]
    print("auto-test (tables [2 1 1 6] et [0 5 5 90], valeurs calculées à la main) :", end=" ")
    try:
        auto_test()
        print("OK")
    except AssertionError as erreur:
        print("ÉCHEC —", erreur)
        sys.exit(1)
    with open(chemin, encoding="utf-8") as f:
        lignes = f.read().split("\n")
    total = 0
    identites = 0
    ecart_phi_max = Decimal(0)
    singletons = []
    for strate, (debut, fin) in PLAGES.items():
        n_attendu = N_STRATE[strate]
        for numero in range(debut, fin + 1):
            texte = lignes[numero - 1]
            m = MOTIF.match(texte)
            if not m:
                print(f"ligne {numero} non reconnue : {texte[:80]}")
                sys.exit(2)
            n11, n10, n01, n00 = (int(m.group(k)) for k in ("n11", "n10", "n01", "n00"))
            r = calcul(n11, n10, n01, n00)
            if r["n"] != n_attendu:
                print(f"ligne {numero} : n = {r['n']} ≠ {n_attendu}")
                sys.exit(3)
            total += 1
            identites += r["identite_exacte"]
            phi_imprime = Decimal(m.group("phi"))
            ecart = abs(r["phi_dec"] - phi_imprime)
            ecart_phi_max = max(ecart_phi_max, ecart)
            signe_ok = (m.group("signe") == "+") == (r["phi_dec"] > 0)
            if not signe_ok:
                print(f"ligne {numero} : signe imprimé incohérent")
            a, b = m.group("a"), m.group("b")
            if a in SINGLETONS and b in SINGLETONS:
                singletons.append((strate, numero, a, b, n11, n10, n01, n00, r, phi_imprime))
    print(f"tables lues : {total} (55 par strate attendues) ; identité exacte vérifiée sur {identites}/{total}")
    print(f"écart maximal |phi recalculé (prec 80) − phi imprimé| sur {total} tables : {sig(ecart_phi_max, 3) if ecart_phi_max else '0'}")
    print()
    print("Paires de singletons de la partition R2 du J28 (bloc 6 : {binance}, {gemini}, {bitstamp}) :")
    for strate, numero, a, b, n11, n10, n01, n00, r, phi_imprime in singletons:
        lift = r["lift"]
        lift_dec = Decimal(lift.numerator) / Decimal(lift.denominator)
        facteur = (Decimal((r["pa"] * r["pb"]).numerator) / Decimal((r["pa"] * r["pb"]).denominator)
                   / (Decimal(((1 - r["pa"]) * (1 - r["pb"])).numerator)
                      / Decimal(((1 - r["pa"]) * (1 - r["pb"])).denominator))).sqrt()
        print(f"  {strate:6s} {a}×{b} (J28 l.{numero}) : [n11 n10 n01 n00] = [{n11} {n10} {n01} {n00}] ; n = {r['n']}")
        print(f"      p_A = {r['pa'].numerator}/{r['pa'].denominator} ; p_B = {r['pb'].numerator}/{r['pb'].denominator}")
        print(f"      lift = {lift.numerator}/{lift.denominator} = {sig(lift_dec, 12)}")
        print(f"      √(p_A·p_B/((1−p_A)(1−p_B))) = {sig(facteur, 12)}")
        print(f"      (lift − 1)·√(…) = {sig(r['ident_dec'], 12)} ; phi recalculé = {sig(r['phi_dec'], 12)} ;"
              f" phi imprimé = {phi_imprime} ; identité exacte : {'oui' if r['identite_exacte'] else 'NON'}")


if __name__ == "__main__":
    main()
