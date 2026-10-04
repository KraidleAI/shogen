#!/usr/bin/env python3
"""Recomptes de contrôle du rédacteur du rapport docs/11 (2026-10-04) sur les valeurs imprimées du rendu J28.

Ce script ne remplace aucune valeur imprimée : il recompte, à partir des entiers imprimés (n, K, écarts par flux,
fenêtres sautées) et de σ̂²_bloc imprimé, les valeurs dérivées par les formules du texte scellé (paquet §10.2 pts 2,
3, 5, 8 ; doc 10 §5.1 ; annexe D.5), et rapporte l'écart à la valeur imprimée. σ̂²_bloc lui-même n'est pas
recalculable sans la série I_t (bloc 2 / journal) : il est pris tel qu'imprimé.

Entrée : le rendu J28 versé à l'octet, lu par numéros de ligne (repérés au journal G1). Bibliothèque standard seule.
Arithmétique : fractions exactes ; racines en decimal, précision 80.
Usage : python3 -B controles_r1.py <rendu_j28> [--mutant]
  --mutant : P̂₁ amputé d'un terme, pour montrer que l'auto-test échoue.
"""
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from fractions import Fraction

getcontext().prec = 80
MUTANT = "--mutant" in sys.argv
SEUIL = Decimal("2.33")
Z_PUISSANCE = Decimal("0.8416")
ELL = 240

L = {  # numéros de ligne dans le rendu J28 (journal G1, lectures 5)
    "calme": {"tete": 435451, "sources": (435453, 435463), "P0": 435465, "P1": 435466, "Pm": 435467,
              "garde": 435468, "z": 435469, "g0": 435494, "fiv": 435495, "zb": 435496, "emd": 435518,
              "regle": 435516, "censure": 435536, "sens_ex": 435807, "sens_in": 435808, "sens_dz": 435809},
    "stress": {"tete": 435471, "sources": (435473, 435483), "P0": 435485, "P1": 435486, "Pm": 435487,
               "garde": 435488, "z": 435489, "g0": 435498, "fiv": 435499, "zb": 435500, "emd": 435521,
               "regle": 435519, "censure": 435537, "sens_ex": 435810, "sens_in": 435811, "sens_dz": 435812},
}
NUM = r"(-?[0-9]+(?:\.[0-9]+)?(?:E-?[0-9]+)?)"


def dec(fr):
    return Decimal(fr.numerator) / Decimal(fr.denominator)


def sqrt_fr(fr):
    return dec(fr).sqrt()


def probas(p):
    """P̂₀, P̂₁, P̂_more exacts (doc 10 §5.1 : P₁ = Σᵢ pᵢ·Πⱼ≠ᵢ(1 − pⱼ))."""
    p0 = Fraction(1)
    for x in p:
        p0 *= (1 - x)
    termes = []
    for i, x in enumerate(p):
        t = x
        for j, y in enumerate(p):
            if j != i:
                t *= (1 - y)
        termes.append(t)
    if MUTANT:
        termes = termes[1:]
    p1 = sum(termes, Fraction(0))
    return p0, p1, 1 - p0 - p1


def auto_test():
    """Valeurs calculées à la main : trois flux de taux 1/2 chacun.
    P₀ = 1/8 ; P₁ = 3·(1/2)·(1/4) = 3/8 ; P_more = 1/2.
    Avec n = 100, K = 60 : n·P(1−P) = 25 ; z = (60 − 50)/5 = 2.
    """
    p0, p1, pm = probas([Fraction(1, 2)] * 3)
    assert p0 == Fraction(1, 8), p0
    assert p1 == Fraction(3, 8), p1
    assert pm == Fraction(1, 2), pm
    garde = 100 * pm * (1 - pm)
    assert garde == 25
    assert dec(Fraction(60) - 100 * pm) / sqrt_fr(garde) == 2


def lire_val(ligne, motif):
    m = re.search(motif, ligne)
    if not m:
        raise SystemExit(f"motif absent : {motif!r} dans : {ligne[:120]}")
    return m


def ecart_rel(calcule, imprime):
    if imprime == 0:
        return abs(calcule)
    return abs((calcule - imprime) / imprime)


def sig(x, c=3):
    if x == 0:
        return "0"
    e = x.adjusted()
    return str(x.quantize(Decimal(1).scaleb(e - c + 1), rounding=ROUND_HALF_EVEN))


def main():
    chemin = [a for a in sys.argv[1:] if not a.startswith("--")][0]
    print("auto-test (trois flux à 1/2, valeurs à la main) :", end=" ")
    try:
        auto_test()
        print("OK")
    except AssertionError as erreur:
        print("ÉCHEC —", erreur)
        sys.exit(1)
    with open(chemin, encoding="utf-8") as f:
        T = f.read().split("\n")

    def ligne(n):
        return T[n - 1]

    pire = Decimal(0)
    sommes_num, sommes_var = Fraction(0), Fraction(0)
    sautees = {}
    m = lire_val(ligne(37), r"calme (\d+), stress (\d+)")  # bloc 1, fenetres_sautees
    sautees["calme"], sautees["stress"] = int(m.group(1)), int(m.group(2))
    for s, l in L.items():
        m = lire_val(ligne(l["tete"]), r"n = (\d+) fenêtres complétées ; K = (\d+)")
        n, K = int(m.group(1)), int(m.group(2))
        p = []
        for k in range(l["sources"][0], l["sources"][1] + 1):
            champs = ligne(k).split()
            nom, p_imp, ecart = champs[0], Decimal(champs[1]), int(champs[2])
            pf = Fraction(ecart, n)
            pire = max(pire, ecart_rel(dec(pf), p_imp))
            p.append(pf)
        p0, p1, pm = probas(p)
        imp = {c: Decimal(lire_val(ligne(l[c]), r"= " + NUM).group(1)) for c in ("P0", "P1", "Pm", "garde", "z")}
        garde = n * pm * (1 - pm)
        numer = K - n * pm
        z = dec(numer) / sqrt_fr(garde)
        g0 = Fraction(K * (n - K), n)
        mg = lire_val(ligne(l["g0"]), r"γ̂₀ = " + NUM + r" ; σ̂²_bloc = " + NUM + r" ; cv théorique = " + NUM)
        g0_imp, s2_imp, cv_imp = (Decimal(mg.group(i)) for i in (1, 2, 3))
        mf = lire_val(ligne(l["fiv"]), r"FIV = " + NUM + r" ; R_centrage = " + NUM + r" ; FIV_série = " + NUM)
        fiv_imp, rc_imp, fs_imp = (Decimal(mf.group(i)) for i in (1, 2, 3))
        zb_imp = Decimal(lire_val(ligne(l["zb"]), r"z_bloc = " + NUM).group(1))
        me = lire_val(ligne(l["emd"]), r"\) = " + NUM + r" fenêtres ; fraction de n_s = " + NUM)
        emd_imp, frac_imp = Decimal(me.group(1)), Decimal(me.group(2))
        sigma_b = s2_imp.sqrt()
        zb = dec(numer) / sigma_b
        fiv = s2_imp / dec(garde)
        rc = dec(g0) / dec(garde)
        fs = s2_imp / dec(g0)
        cv = sqrt_fr(Fraction(4 * ELL, 3 * n))
        emd = (SEUIL + Z_PUISSANCE) * max(sqrt_fr(garde), sigma_b)
        frac = emd / n
        valeur = ("REJETTE" if (z >= SEUIL and zb >= SEUIL) else
                  ("NE REJETTE PAS (discordance)" if z >= SEUIL else "NE REJETTE PAS"))
        regle_imp = ligne(l["regle"])
        valeur_imp = regle_imp.split("→ ")[-1].strip()
        controles = {
            "P̂₀": (dec(p0), imp["P0"]), "P̂₁": (dec(p1), imp["P1"]), "P̂_more": (dec(pm), imp["Pm"]),
            "n·P̂(1−P̂)": (dec(garde), imp["garde"]), "z_s": (z, imp["z"]), "γ̂₀ = K(n−K)/n": (dec(g0), g0_imp),
            "z_bloc (σ̂² imprimé)": (zb, zb_imp), "FIV": (fiv, fiv_imp), "R_centrage": (rc, rc_imp),
            "FIV_série": (fs, fs_imp), "cv théorique": (cv, cv_imp), "EMD_s": (emd, emd_imp),
            "fraction EMD_s/n_s": (frac, frac_imp),
        }
        print(f"== strate {s} : n = {n}, K = {K} (J28 l.{l['tete']})")
        for nom, (c, i) in controles.items():
            r = ecart_rel(c, i)
            pire = max(pire, r)
            print(f"   {nom:22s} écart relatif au rendu = {sig(r) if r else '0'}")
        print(f"   garde tenue (≥ 10) : {garde >= 10} ; z_s ≥ 2,33 : {z >= SEUIL} ; z_bloc ≥ 2,33 : {zb >= SEUIL}")
        print(f"   valeur recomptée : {valeur} ; valeur imprimée (l.{l['regle']}) : {valeur_imp} ; égales : {valeur == valeur_imp}")
        # Censure (annexe D.5) : bornes à P̂_more fixé, s = fenêtres sautées de la strate (bloc 1 l.37).
        sv = sautees[s]
        mc = lire_val(ligne(l["censure"]), r"s = (\d+) ; z_bas = " + NUM + r" ; z_haut = " + NUM +
                      r" ; avec σ̂_bloc : z_bas = " + NUM + r" ; z_haut = " + NUM)
        assert int(mc.group(1)) == sv
        var_ns = (n + sv) * pm * (1 - pm)
        zbas = dec(K - (n + sv) * pm) / sqrt_fr(var_ns)
        zhaut = dec(K + sv - (n + sv) * pm) / sqrt_fr(var_ns)
        zbas_b = dec(K - (n + sv) * pm) / sigma_b
        zhaut_b = dec(K + sv - (n + sv) * pm) / sigma_b
        for nom, c, i in (("z_bas", zbas, mc.group(2)), ("z_haut", zhaut, mc.group(3)),
                          ("z_bas (σ̂_bloc)", zbas_b, mc.group(4)), ("z_haut (σ̂_bloc)", zhaut_b, mc.group(5))):
            r = ecart_rel(c, Decimal(i))
            pire = max(pire, r)
            print(f"   censure {nom:16s} écart relatif au rendu = {sig(r) if r else '0'} (J28 l.{l['censure']})")
        # Sensibilité « plage incluse » : écart de z imprimé = z(incluse) − z(exclue).
        zex = Decimal(lire_val(ligne(l["sens_ex"]), r"z = " + NUM).group(1))
        zin = Decimal(lire_val(ligne(l["sens_in"]), r"z = " + NUM).group(1))
        dz = Decimal(lire_val(ligne(l["sens_dz"]), r"écart de z = " + NUM).group(1))
        r = ecart_rel(zin - zex, dz)
        pire = max(pire, r)
        print(f"   [SENSIBILITÉ] écart de z = z(incluse) − z(exclue) : écart relatif au rendu = {sig(r) if r else '0'}")
        sommes_num += numer
        sommes_var += garde
    zpool = dec(sommes_num) / sqrt_fr(sommes_var)
    zpool_imp = Decimal(lire_val(ligne(435510), r"z_pool  = " + NUM).group(1))
    r = ecart_rel(zpool, zpool_imp)
    pire = max(pire, r)
    print(f"== strate poolée (exploratoire) : z_pool écart relatif au rendu = {sig(r) if r else '0'} (J28 l.435510)")
    print(f"== écart relatif maximal sur tous les contrôles : {sig(pire)}")
    # Identités entières (bloc 1, bloc 3, [SENSIBILITÉ]).
    print("== identités entières")
    t0, tfin = 1787770800, 1790558880
    a, b = 1790273880, 1790435280
    grille = (tfin - t0) // 60
    grille_d5 = (b - a) // 60 + 1
    print(f"   24585 + 11397 = {24585 + 11397} ; 1709 + 909 = {1709 + 909} ; 38600 − 2618 = {38600 - 2618}")
    print(f"   grille du segment [t0 ; T_fin) : ({tfin} − {t0})/60 = {grille} fenêtres ; plage D5 fermée : {grille_d5} fenêtres")
    print(f"   grille − marqueurs (38600) − sans marqueur dans la plage (73) = {grille - 38600 - 73} ; 5701 + 2094 = {5701 + 2094}")
    print(f"   T_fin = dernier window_start (1790558820) + 60 = {1790558820 + 60}")
    print(f"   K décomposé : calme 153 + 1 + 0 = {153 + 1 + 0} ; stress 133 + 0 + 0 = {133}")
    for nom, e in (("t0", t0), ("T_fin", tfin), ("A (D5)", a), ("B (D5)", b), ("B + 60", b + 60)):
        print(f"   {nom} = {e} = {datetime.fromtimestamp(e, tz=timezone.utc).isoformat()}")
    print("== verdict du journal brut (…943.5-raw.out) : window_start des cinq lectures en cause dans [A ; B] ?")
    for e in (1790275920, 1790277780, 1790283600, 1790283840, 1790285940):
        print(f"   {e} = {datetime.fromtimestamp(e, tz=timezone.utc).isoformat()} ; dans [A ; B] : {a <= e <= b}")


if __name__ == "__main__":
    main()
