#!/usr/bin/env python3
"""Extraction verbatim des valeurs hors décision (J14 principal, J14 second, strate poolée, [SENSIBILITÉ], L&M du J28,
variante incluse du recalcul tiers) en lignes de table Markdown. Aucun calcul. Rédacteur du rapport docs/11, 2026-10-04.
Usage : python3 -B extraire_hd.py <dossier des rendus>"""
import json, re, sys
from pathlib import Path
D = Path(sys.argv[1]); P = "shogen-27b0e30-rendu-20261004T011129Z-943."
NUM = r"(-?[0-9]+(?:\.[0-9]+)?(?:E-?[0-9]+)?)"
def lignes(f): return (D / (P + f)).read_text(encoding="utf-8").split("\n")
def g(T, n, motif, i=1):
    m = re.search(motif, T[n - 1])
    if not m: raise SystemExit(f"l.{n} : motif absent {motif!r} : {T[n-1][:100]}")
    return m.group(i)
# J14 : n, K, P̂_more, garde, z, z_bloc, valeur
for nom, f, c, s in (("J14p", "1-j14-principal.out",
                      dict(tete=209555, Pm=209571, garde=209572, z=209573, zb=209601, regle=209620),
                      dict(tete=209575, Pm=209591, garde=209592, z=209593, zb=209605, regle=209622)),
                     ("J14s", "2-j14-second.out",
                      dict(tete=112112, Pm=112128, garde=112129, z=112130, zb=112159, regle=112178),
                      dict(tete=112133, Pm=112149, garde=112150, z=112151, zb=112163, regle=112179))):
    T = lignes(f)
    print(f"| {nom} : grandeur | calme | stress | {nom} |")
    print("|---|---|---|---|")
    for lib, cle, motif in (("n_s", "tete", r"n = (\d+) fenêtres"), ("K_s", "tete", r"K = (\d+)"),
                            ("P̂_more,s", "Pm", r"= " + NUM), ("garde (seuil 10)", "garde", r"= " + NUM)):
        print(f"| {lib} | `{g(T, c[cle], motif)}` | `{g(T, s[cle], motif)}` | l.{c[cle]} ; l.{s[cle]} |")
    def zval(n):
        m = re.search(r"z       = " + NUM, T[n - 1])
        return f"`{m.group(1)}`" if m else "non publié (garde §5.4)"
    def zbval(n):
        m = re.search(r"z_bloc = " + NUM, T[n - 1])
        return f"`{m.group(1)}`" if m else "non publié (garde de blocs, n_s < 7200)"
    print(f"| z_s | {zval(c['z'])} | {zval(s['z'])} | l.{c['z']} ; l.{s['z']} |")
    print(f"| z_bloc,s | {zbval(c['zb'])} | {zbval(s['zb'])} | l.{c['zb']} ; l.{s['zb']} |")
    vc = T[c["regle"] - 1].split("→ ")[-1].strip(); vs = T[s["regle"] - 1].split("→ ")[-1].strip()
    print(f"| valeur de la règle (hors décision) | {vc} | {vs} | l.{c['regle']} ; l.{s['regle']} |")
    print()
# [SENSIBILITÉ] du J28
T = lignes("3-j28.out")
print("| strate | variante | n | K | P̂_more | z | drapeau 1 | J28 |")
print("|---|---|---|---|---|---|---|---|")
for n in (435807, 435808, 435810, 435811):
    m = re.search(r"^  (\w+)\s+(exclue \(principale\)|incluse \(sensibilité\))\s+: n = (\d+) ; K = (\d+) ; P̂_more = " + NUM + r" ; z = " + NUM + r" ; drapeau 1 = (\w+)", T[n - 1])
    print(f"| {m.group(1)} | {m.group(2)} | {m.group(3)} | {m.group(4)} | `{m.group(5)}` | `{m.group(6)}` | {m.group(7)} | l.{n} |")
for n in (435809, 435812):
    print(f"écart de z (l.{n}) : `{g(T, n, r'écart de z = ' + NUM)}`")
print()
# Strate poolée du J28
MOT_VAR = r'; Σ_s n_s·P̂_more,s·\(1 − P̂_more,s\) = ' + NUM
zp = g(T, 435510, r'z_pool  = ' + NUM); sn = g(T, 435509, r'= ' + NUM); sv = g(T, 435509, MOT_VAR)
print(f"z_pool (l.435510) : `{zp}` ; Σ numérateurs (l.435509) : `{sn}` ; Σ variances : `{sv}`")
print()
# L&M du J28
print("| L&M (bloc 4) | calme | stress | J28 |")
print("|---|---|---|---|")
for lib, lc, ls, motif in (("Σ mⱼ", 435541, 435606, r"Σ mⱼ = (\d+)"), ("Ê(Θ)", 435542, 435607, r"= " + NUM),
                           ("Ê(Θ²)", 435543, 435608, r"= " + NUM), ("Var̂(Θ)", 435544, 435609, r"= " + NUM),
                           ("φ définies / 55", 435545, 435610, r"(\d+) définies"),
                           ("paires à co-écart (n11 > 0)", 435545, 435610, r"(\d+) paires à co-écart")):
    a, b = g(T, lc, motif), g(T, ls, motif)
    fmt = (lambda x: f"`{x}`") if "." in a else (lambda x: x)
    print(f"| {lib} | {fmt(a)} | {fmt(b)} | l.{lc} ; l.{ls} |")
print()
# φ les plus élevés par strate (rang par φ imprimé), et φ négatifs
for strate, (d0, d1) in (("calme", (435547, 435601)), ("stress", (435612, 435666))):
    rows = []
    for n in range(d0, d1 + 1):
        m = re.match(r"^\s+(\S+)\s+\[(\d+) (\d+) (\d+) (\d+)\]\s+φ=" + NUM, T[n - 1])
        rows.append((m.group(6), m.group(1), m.group(2), n))
    top = sorted(rows, key=lambda r: -float(r[0]))[:4]
    neg = [r for r in rows if r[0].startswith("-")]
    print(f"{strate} : φ les plus élevés : " + " ; ".join(f"{p} n11={n11} φ=`{v}` (l.{n})" for v, p, n11, n in top))
    print(f"{strate} : φ négatifs : {len(neg)} : " + " ; ".join(f"{p} (l.{n})" for v, p, n11, n in neg))
print()
# Recalcul tiers : variante incluse
rec = json.loads((D / (P + "4-recalcul-tiers.out")).read_text(encoding="utf-8"))
ji = rec["j28-incluse"]
print("RT j28-incluse etiquette :", ji["etiquette"])
for s in ("calme", "stress"):
    st = ji["r1"]["strates"][s]
    print(f"RT j28-incluse {s} : n={st['n']} K={st['K']} z=`{st['z']}` z_bloc=`{st['bloc']['z_bloc']}`")
dr = ji["r2"]["drapeau_2"]
print(f"RT j28-incluse drapeau_2 : etat={dr['etat']} r1_discrimine={dr['r1_discrimine']} rejette={dr['rejette']} raison={dr['raison']}")
