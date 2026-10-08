#!/usr/bin/env python3
"""Extraction verbatim des lignes du descriptif D.5 du J28 (τ observé, censure) en lignes de table Markdown.
Aucun calcul. Rédacteur du rapport docs/11, 2026-10-04. Usage : python3 -B extraire_d5.py <rendu_j28>"""
import re, sys
T = open(sys.argv[1], encoding="utf-8").read().split("\n")
NUM = r"(-?[0-9]+(?:\.[0-9]+)?(?:E-?[0-9]+)?)"
print("| classe | τ_classe (committé) | N cellules | P99 observé | maximum observé | J28 |")
print("|---|---|---|---|---|---|")
for n in range(435526, 435531):
    l = T[n - 1]
    m = re.search(r"« (\w+) » : τ_classe = " + NUM + r" ; N = (\d+) ; P99 = " + NUM + r" ; maximum = " + NUM, l)
    if m:
        print(f"| `{m.group(1)}` | `{m.group(2)}` | {m.group(3)} | `{m.group(4)}` | `{m.group(5)}` | l.{n} |")
    else:
        m = re.search(r"« (\w+) » : τ_classe = " + NUM + r" ; N = (\d+) : non défini", l)
        print(f"| `{m.group(1)}` | `{m.group(2)}` | {m.group(3)} | non défini | non défini | l.{n} |")
print()
print("| strate | s (fenêtres sautées) | z_bas | z_haut | z_bas avec σ̂_bloc | z_haut avec σ̂_bloc | J28 |")
print("|---|---|---|---|---|---|---|")
for n in (435536, 435537):
    l = T[n - 1]
    m = re.search(r"« (\w+) » : s = (\d+) ; z_bas = " + NUM + r" ; z_haut = " + NUM + r" ; avec σ̂_bloc : z_bas = " + NUM + r" ; z_haut = " + NUM, l)
    print(f"| {m.group(1)} | {m.group(2)} | `{m.group(3)}` | `{m.group(4)}` | `{m.group(5)}` | `{m.group(6)}` | l.{n} |")
