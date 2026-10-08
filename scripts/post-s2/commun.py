"""Commun du lot POST-PREREG : analyses ajoutées après le pré-enregistrement, hors décision, sur les journaux scellés
(G0 `docs/adr-0028/G0-lots-DETTES.md`, ligne POST-PREREG ; items de l'annexe B d'ADR-0028, cités par chaque script).

Lecteurs du harnais réutilisés par import, sans modifier `s2-harness` : mêmes appels que `r1.recompute_from_journal`.
Chaque sortie porte ETIQUETTE en première ligne, puis sa provenance et le contrôle de cohérence contre le bloc 3 du
rendu J28 (n, K, P̂_more par strate, chaîne pour chaîne) ; en écart, aucune valeur d'analyse (fail-closed). Aucune
sortie ne remplace une valeur des rendus ; aucun contenu de journal n'est imprimé."""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from decimal import Decimal, localcontext

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
HARNAIS = os.path.join(RACINE, "s2-harness")
if HARNAIS not in sys.path:
    sys.path.insert(0, HARNAIS)
from shogen_s2 import r1, records, window  # noqa: E402

ETIQUETTE = ("ajoutée après le pré-enregistrement, hors décision ; ne change pas le verdict de la règle scellée "
             "(« R1 discrimine » = FAUX, docs/11 §3)")
T0, N_FIXE, PLAGE_D5 = 1787770800, 38600, (1790273880, 1790435280)   # rendu_unique.SORTIES « j28 » (D2 pt 6 ; D5)
SEGMENT = {"t0": T0, "n_fixe": N_FIXE}
RENDU_J28 = os.path.join(RACINE, "docs", "adr-0028", "execution", "rendu-2026-10-04",
                         "shogen-27b0e30-rendu-20261004T011129Z-943.3-j28.out")


def dec(x) -> str:
    """Decimal en chaîne sous le contexte nommé du harnais (forme des rendus) ; None : « - »."""
    with localcontext(r1.contexte_decimal()):
        return "-" if x is None else str(x)


def sha256(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def charger(journaux: str, segment=SEGMENT, plages=(PLAGE_D5,)) -> dict:
    """Journaux lus comme par r1.recompute_from_journal (garde §5.3, filtre de lecture, pool D1) ; « base » : sortie de
    r1.compute_r1 de la règle scellée sur cette portée."""
    c, j = (os.path.join(journaux, n) for n in ("control.jsonl", "journal.jsonl"))
    plist, clock, tous = records.parse_control(c)
    p = records.effective_run_params(plist)
    if window.verify_markers_against_spec(tous, p["strate_calendar"]):
        raise ValueError("strates journalées incohérentes avec le calendrier committé (fail-closed, §5.3)")
    m, cl, asn, seg = records.filtre_lecture(p, tous, clock, records.parse_asn(c), ranges=plages, segment=segment)
    d = {"control": c, "journal": j, "params": p, "plist": plist, "tous": tous, "markers": m, "clock": cl, "asn": asn,
         "seg": seg, "plages": [tuple(x) for x in plages], "readings": r1.parse_journal(j), "w": int(p["w"]),
         "seuil": Decimal(str(p["seuil_historique_valeur"])), "n_min": int(p["n_min_hors_enveloppe"])}
    d["sbc"], d["scf"], d["tau"] = records.sigma_tau_from_params(p)
    d["pools"], d["pool"], d["retraits"] = r1.analysis_pools(m, d["readings"], list(p["pool"]))
    d["base"] = calculer(d, m, d["pools"])
    return d


def calculer(d: dict, markers: list, pools: dict) -> dict:
    """r1.compute_r1 sur `markers`, pool de chaque strate `pools` ; pool du segment : leur union (ordre du pool)."""
    seg = [f for f in d["params"]["pool"] if any(f in v for v in pools.values())]
    return r1.compute_r1(markers, d["readings"], seg, d["w"], d["sbc"], d["scf"], d["tau"], d["seuil"], d["n_min"],
                         pool_by_strate=pools)


def lire_bloc3(chemin: str) -> dict:
    """{strate : (n, K, P̂_more en chaîne)} lus au bloc 3 d'un rendu : en-tête de strate, puis première ligne
    « P̂_more  = » (deux espaces) ; la ligne de strate poolée (« P̂_more = », un espace) n'est pas lue."""
    with open(chemin, encoding="utf-8") as f:
        b3 = f.read().split("\n[BLOC 3]", 1)[1].split("\n[BLOC 4]", 1)[0]
    out, st = {}, None
    for x in b3.split("\n"):
        if m := re.match(r"  ── strate « (\w+) » : n = (\d+) fenêtres complétées ; K = (\d+) ", x):
            st, out[m.group(1)] = m.group(1), [int(m.group(2)), int(m.group(3)), None]
        elif (m := re.fullmatch("    P̂_more  = (\\S+)", x)) and st and out[st][2] is None:
            out[st][2] = m.group(1)
    return {s: tuple(v) for s, v in out.items()}


def controle_j28(base: dict, chemin: str) -> tuple:
    """n, K, P̂_more de `base` (sortie de r1.compute_r1) contre le bloc 3 du rendu, chaîne pour chaîne : (égaux,
    lignes) ; une strate absente d'un côté est un écart ; rendu sans strate : écart."""
    attendu, lignes, ok = lire_bloc3(chemin), [], True
    for st in sorted(set(attendu) | set(base["strates"])):
        b = base["strates"].get(st)
        nous = None if b is None else (b["n"], b["K"], dec(b["P_more"]))
        ok &= nous == attendu.get(st)
        lignes.append(f"contrôle de cohérence (rendu, bloc 3) « {st} » : recompté (n, K, P̂_more) = {nous} ; rendu = "
                      f"{attendu.get(st)} : {'égaux' if nous == attendu.get(st) else 'ÉCART'}")
    return ok and bool(attendu), lignes


def executer(nom: str, items: str, analyse, argv=None) -> int:
    """CLI commune : --journaux (dossier des journaux scellés), --sortie, --rendu (défaut : rendu J28 versé) ; --t0,
    --n-fixe, --plage A B (portée ; défaut : celle du J28). Écrit ETIQUETTE, la provenance, le contrôle de cohérence,
    puis analyse(d) si le contrôle est égal (code 0) ; sinon une ligne de refus (code 1)."""
    p = argparse.ArgumentParser(prog=nom)
    for opt in ("--journaux", "--sortie"):
        p.add_argument(opt, required=True)
    p.add_argument("--rendu", default=RENDU_J28)
    p.add_argument("--t0", type=int, default=T0)
    p.add_argument("--n-fixe", type=int, default=N_FIXE)
    p.add_argument("--plage", type=int, nargs=2, action="append")
    a = p.parse_args(argv)
    plages = [tuple(x) for x in a.plage] if a.plage else [PLAGE_D5]
    d = charger(a.journaux, {"t0": a.t0, "n_fixe": a.n_fixe}, plages)
    ok, ctrl = controle_j28(d["base"], a.rendu)
    script = sys.modules[analyse.__module__].__file__
    tete = [f"{nom} — {items}", f"script {os.path.basename(script)} sha256 {sha256(script)} ; commun.py sha256 "
            f"{sha256(__file__)}", f"journaux : control.jsonl {sha256(d['control'])} ; journal.jsonl "
            f"{sha256(d['journal'])}", f"rendu de contrôle : {os.path.basename(a.rendu)} sha256 {sha256(a.rendu)}",
            f"portée : segment [{d['seg'][0]} ; {d['seg'][1]}) (t0 = {a.t0}, n fixe = {a.n_fixe}), plages exclues "
            f"{plages} ; pool D1 : " + " ; ".join(f"« {s} » {len(v)} flux" for s, v in d["pools"].items())]
    corps = analyse(d) if ok else ["contrôle de cohérence en ÉCART : aucune valeur d'analyse imprimée (fail-closed)"]
    with open(a.sortie, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join([ETIQUETTE, *tete, *ctrl, *corps]) + "\n")
    return 0 if ok else 1
