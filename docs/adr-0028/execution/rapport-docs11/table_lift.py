#!/usr/bin/env python3
"""Mise en table Markdown de la sortie de d3_lift.py (aucun calcul : réécriture de chaînes).
Rédacteur du rapport docs/11, 2026-10-04. Usage : python3 -B table_lift.py d3_lift.sortie.txt"""
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
blocs = re.findall(
    r"  (calme|stress)\s+(\S+) \(J28 l\.(\d+)\) : \[n11 n10 n01 n00\] = \[([\d ]+)\] ; n = (\d+)\n"
    r"      p_A = (\S+) ; p_B = (\S+)\n"
    r"      lift = (\S+) = (\S+)\n"
    r"      √\(p_A·p_B/\(\(1−p_A\)\(1−p_B\)\)\) = (\S+)\n"
    r"      \(lift − 1\)·√\(…\) = (\S+) ; phi recalculé = (\S+) ; phi imprimé = (\S+) ; identité exacte : (\S+)", t)
print("| strate | paire | [n11 n10 n01 n00] (J28) | p_A ; p_B | lift (exact) | lift ≈ | √(p_A·p_B/((1−p_A)(1−p_B))) ≈ | (lift − 1)·√(…) ≈ | φ imprimé (bloc 4) | identité exacte |")
print("|---|---|---|---|---|---|---|---|---|---|")
for b in blocs:
    s, paire, l, comptes, n, pa, pb, lift, liftd, fac, ident, phir, phii, ok = b
    print(f"| {s} | {paire} | [{comptes}] (l.{l}) | {pa} ; {pb} | {lift} | {liftd} | {fac} | {ident} | `{phii}` | {ok} |")
print(f"\n{len(blocs)} lignes")
