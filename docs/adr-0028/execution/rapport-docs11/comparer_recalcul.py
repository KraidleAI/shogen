#!/usr/bin/env python3
"""Comparaison, à la chaîne près, des valeurs du run « recalcul-tiers » (JSON des points d'entrée recompute_*) avec
les valeurs imprimées par les rendus J28, J14 principal et J14 second (bloc 3, bloc 6). Rédacteur du rapport docs/11,
2026-10-04. Bibliothèque standard seule ; aucune lecture de journal. Ne calcule rien : compare des chaînes.

Usage : python3 -B comparer_recalcul.py <dossier des rendus> [--mutant]
  --mutant : altère une valeur du JSON en mémoire (dernier chiffre de z calme du J28) pour montrer que la comparaison
  la détecte.
"""
import json
import re
import sys
from pathlib import Path

MUTANT = "--mutant" in sys.argv
D = Path([a for a in sys.argv[1:] if not a.startswith("--")][0])
P = "shogen-27b0e30-rendu-20261004T011129Z-943."
RENDUS = {"j28": P + "3-j28.out", "j14-principal": P + "1-j14-principal.out", "j14-second": P + "2-j14-second.out"}
NUM = r"(-?[0-9]+(?:\.[0-9]+)?(?:E-?[0-9]+)?)"


def bloc3(texte):
    debut = texte.index("[BLOC 3]")
    fin = texte.index("[BLOC 4]")
    return texte[debut:fin]


def valeurs_rendu(b3, strate):
    v = {}
    m = re.search(r"── strate « " + strate + r" » : n = (\d+) fenêtres complétées ; K = (\d+)", b3)
    v["n"], v["K"] = m.group(1), m.group(2)
    seg = b3[m.end():]
    seg = seg[: seg.index("── ")] if "── " in seg else seg
    v["P_more"] = re.search(r"P̂_more  = " + NUM, seg).group(1)
    v["gate_value"] = re.search(r"n·P̂_more·\(1−P̂_more\) = " + NUM, seg).group(1)
    mz = re.search(r"z       = " + NUM, seg)
    v["z"] = mz.group(1) if mz else None
    mb = re.search(r"« " + strate + r" » : ℓ = 240 ; γ̂₀ = " + NUM + r" ; σ̂²_bloc = " + NUM + r" ; cv théorique = " + NUM, b3)
    v["gamma0"], v["sigma2_bloc"], v["cv_theorique"] = mb.group(1), mb.group(2), mb.group(3)
    mf = re.search(r"« " + strate + r" » : FIV = " + NUM + r" ; R_centrage = " + NUM + r" ; FIV_série = " + NUM, b3)
    v["FIV"], v["R_centrage"], v["FIV_serie"] = mf.group(1), mf.group(2), mf.group(3)
    mzb = re.search(r"« " + strate + r" » : z_bloc = " + NUM, b3)
    v["z_bloc"] = mzb.group(1) if mzb else None
    mr = re.search(r"« " + strate + r" » : diagnostic de runs de I_t \(hors décision\) : nombre = (\d+) ; longueur moyenne = " + NUM + r" ; run maximal = (\d+)", b3)
    v["runs.nombre"], v["runs.longueur_moyenne"], v["runs.run_max"] = mr.group(1), mr.group(2), mr.group(3)
    md = re.search(r"« " + strate + r" » : K = (\d+) = K\[≥ 2 panne_transport\] (\d+) \+ K\[1\] (\d+) \+ K\[0\] (\d+) ; K\[tous les écarts hors_enveloppe\] = (\d+) ; c_s = (\d+)", b3)
    v["decomposition_K.pt_2_plus"], v["decomposition_K.pt_1"], v["decomposition_K.pt_0"] = md.group(2), md.group(3), md.group(4)
    v["decomposition_K.tous_hors_enveloppe"], v["decomposition_K.c"] = md.group(5), md.group(6)
    return v


def valeurs_json(j, strate):
    s = j["r1"]["strates"][strate]
    b = s["bloc"]
    v = {"n": str(s["n"]), "K": str(s["K"]), "P_more": s["P_more"], "gate_value": s["gate_value"], "z": s["z"],
         "gamma0": b["gamma0"], "sigma2_bloc": b["sigma2_bloc"], "cv_theorique": b["cv_theorique"], "FIV": b["FIV"],
         "R_centrage": b["R_centrage"], "FIV_serie": b["FIV_serie"], "z_bloc": b["z_bloc"],
         "runs.nombre": str(b["runs"]["nombre"]), "runs.longueur_moyenne": b["runs"]["longueur_moyenne"],
         "runs.run_max": str(b["runs"]["run_max"])}
    d = s["decomposition_K"]
    for k in ("pt_2_plus", "pt_1", "pt_0", "tous_hors_enveloppe", "c"):
        v["decomposition_K." + k] = str(d[k])
    return v


def main():
    rec = json.loads((D / (P + "4-recalcul-tiers.out")).read_text(encoding="utf-8"))
    if MUTANT:
        z = rec["j28"]["r1"]["strates"]["calme"]["z"]
        rec["j28"]["r1"]["strates"]["calme"]["z"] = z[:-1] + ("0" if z[-1] != "0" else "1")
    total, egaux, differents = 0, 0, []
    for nom, fichier in RENDUS.items():
        texte = (D / fichier).read_text(encoding="utf-8")
        b3 = bloc3(texte)
        for strate in ("calme", "stress"):
            vr = valeurs_rendu(b3, strate)
            vj = valeurs_json(rec[nom], strate)
            for cle in vr:
                total += 1
                if vr[cle] == vj[cle]:
                    egaux += 1
                else:
                    differents.append((nom, strate, cle, vr[cle], vj[cle]))
        # Bloc 6 : état du drapeau 2 et « R1 discrimine ».
        etat = re.search(r"DRAPEAU 2 .* : état = (\S+)", texte).group(1)
        total += 1
        if etat.lower() == rec[nom]["r2"]["drapeau_2"]["etat"].lower():
            egaux += 1
        else:
            differents.append((nom, "-", "drapeau_2.etat", etat, rec[nom]["r2"]["drapeau_2"]["etat"]))
        rd = re.search(r"« R1 discrimine » \(§1 bis\.1 pt 6 ; déclencheur de D6 \(vi\) et D9\) = (VRAI|FAUX|NON ÉVALUABLE)", texte).group(1)
        total += 1
        if rd == rec[nom]["r2"]["drapeau_2"]["r1_discrimine"]:
            egaux += 1
        else:
            differents.append((nom, "-", "r1_discrimine", rd, rec[nom]["r2"]["drapeau_2"]["r1_discrimine"]))
    print(f"valeurs comparées : {total} ; égales à la chaîne près : {egaux} ; différentes : {len(differents)}")
    for x in differents:
        print("  DIFFÉRENTE :", x)
    sys.exit(0 if not differents else 1)


if __name__ == "__main__":
    main()
