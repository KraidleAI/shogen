#!/usr/bin/env python3
"""Calculs divers du rédacteur du rapport docs/11 (2026-10-04), cités [calc] dans le texte. Entrées : chaînes
recopiées des rendus (ligne citée en commentaire). Bibliothèque standard ; decimal précision 60.
Usage : python3 -B calc_divers.py [<rendu_j28>]   (avec le rendu : sommes des écarts par type, bloc 3)
"""
from datetime import datetime
from decimal import Decimal, getcontext, ROUND_HALF_EVEN

getcontext().prec = 60


def s3(x, c=3):
    x = Decimal(x)
    e = x.adjusted()
    return str(x.quantize(Decimal(1).scaleb(e - c + 1), rounding=ROUND_HALF_EVEN))


# J28 l.435494, l.435498 (σ̂²_bloc) ; l.435468, l.435488 (garde)
s2 = {"calme": Decimal("3837.3644239148386709307388556071047850697416032311"),
      "stress": Decimal("4444.2268779663177986090438425985366511755710614584")}
garde = {"calme": Decimal("33.462466216157713120610261901717310599417168320476"),
         "stress": Decimal("16.688041699661428674928415017858500902580981925520")}
for s in ("calme", "stress"):
    print(f"{s} : √σ̂²_bloc = {s3(s2[s].sqrt())} ; √garde = {s3(garde[s].sqrt())} ; max = "
          f"{'σ̂_bloc' if s2[s].sqrt() > garde[s].sqrt() else '√garde'}")
# J28 l.435497, l.435501 : runs ; l.435451, l.435471 : K
print(f"K/nombre de runs : calme 154/119 = {s3(Decimal(154) / 119, 12)} ; stress 133/130 = {s3(Decimal(133) / 130, 12)}")
# J28 l.39, l.41 : sautées non attribuées ; l.38, l.40 : harnais vivant
print(f"sautées non attribuées : 5684 + 1944 = {5684 + 1944} ; harnais vivant : 17 + 150 = {17 + 150}")
# JOURNAL l.314 : production 01:11:27 → 01:33:47 UTC
d = datetime(2026, 10, 4, 1, 33, 47) - datetime(2026, 10, 4, 1, 11, 27)
print(f"durée de la production : {d} ({int(d.total_seconds())} s)")
# J28 l.435526-435530 : τ observé contre τ committé
tau = {"agregateur": ("0.026", "0.0029870446819581321147177994146356252452815395638463",
                      "0.017649908208186827670019929236496737002324764533848"),
       "oracle_chainlink": ("0.0165", "0.0045133817598667881395689083527158792588820593853894",
                            "0.017842859661860400175061719273882056236385914669308"),
       "place_horodatee": ("0.0045", "0.00084986241659292805372128990214331880618269790009557",
                           "0.0031005971796576586758169290273558058198265570013814"),
       "sans_horodatage": ("0.0045", "0.0016680227037502354455795456531406013037374194387754",
                           "0.0084293722922191923975621436933888192128120065521140")}
for c, (t, p99, mx) in tau.items():
    t, p99, mx = Decimal(t), Decimal(p99), Decimal(mx)
    print(f"τ {c} : P99/τ = {s3(p99 / t)} ; max/τ = {s3(mx / t)} ; P99 < τ : {p99 < t} ; max > τ : {mx > t}")
# J28 l.435509 : Σ numérateurs et Σ variances de la strate poolée
print(f"z_pool recompté = {s3(Decimal('236.77931489141074698973370238916004307092589875631') / Decimal('50.150507915819141795538676919575811501998150245996').sqrt(), 12)}")
# J14p l.209592, J14s l.112129, l.112150 : gardes sous le seuil 10
for nom, v in (("J14p stress", "1.3891374858460684507352497516803467029217226329697"),
               ("J14s calme", "0.11626063253151037288958691789311493515448564399261"),
               ("J14s stress", "0.024474839280311532597570565581073686929332258857146")):
    print(f"garde {nom} = {s3(v)} < 10 : {Decimal(v) < 10}")
# J28 l.435453-435463 (calme) et l.435473-435483 (stress) : écart, panne, stale, horsE, nonÉv par flux (lus du rendu)
import sys as _sys
if len(_sys.argv) > 1:
    T = open(_sys.argv[1], encoding="utf-8").read().split("\n")
    for strate, d0, sm in (("calme", 435453, 1451), ("stress", 435473, 693)):
        tot = [0, 0, 0, 0, 0]
        for k in range(11):
            ch = T[d0 + k - 1].split()
            for i in range(5):
                tot[i] += int(ch[2 + i])
        print(f"{strate} : Σ écarts = {tot[0]} (Σ mⱼ imprimé {sm} : égal = {tot[0] == sm}) ; pannes {tot[1]} ; "
              f"staleness {tot[2]} ; hors-enveloppe {tot[3]} ; non évaluables {tot[4]} ; "
              f"pannes + staleness + hors-env = {tot[1] + tot[2] + tot[3]}")
