"""SHOGEN-GARDE-NIVEAU-N-1 (lot DETTES-SIM, 2026-10-04) : niveau de z_s seul et distribution de la règle
SHOGEN-CRITERE-R1-1 près de la garde §5.4 pour n < 30·ℓ = 7 200 (n = 2 880 et 5 760 : bornes calendaires des strates
stress des J14, ADR-0028 §1 bis.2), sous le modèle nul synthétique de SIM-NIVEAU. Cas, R, graine et lecture : journal
G1 du lot (docs/G1-lot-DETTES-SIM.md, pré-enregistrement). Réplication sim_niveau_calc.replication, agrégation
sim_niveau.agreger, ajouts de l'étape S (sim_garde_niveau.suivre, completer, texte) : inchangés, aucune ligne recopiée.
Ajout : contrôle de la déduction de l'étape S §1.2 (sous la garde de blocs : REJETTE et discordance nulles, z_bloc
jamais publiée, rejet non qualifiable = z ≥ 2,33 garde tenue), fail-closed. Oracle : sim_garde_n_oracle_r1.py.
Usage : python3.13 -B sim_garde_n.py --sortie DOSSIER [--processus k] [--diviseur d]   Worker G1 DETTES-SIM."""
import argparse, contextlib, hashlib, json, multiprocessing, os, platform, sys, time
from collections import Counter
from statistics import NormalDist

import sim_garde_niveau as G
import sim_niveau as S
import sim_niveau_calc as C

GRILLE = ((2880, "0.008157", 10), (2880, "0.01006", 15), (2880, "0.01168", 20), (2880, "0.01445", 30),
          (5760, "0.005721", 10), (5760, "0.007038", 15), (5760, "0.008157", 20), (5760, "0.01006", 30))
CAS = ([(1, n, p, g, G.R_I) for n, p, g in GRILLE]
       + [(L, n, p, g, G.R_D) for L in (5, 20, 60) for n, p, g in GRILLE if g in (10, 30)])
V, ITEM = S.VALEURS, "SHOGEN-GARDE-NIVEAU-N-1"
CONSEQUENCE = ("Conséquence pré-déclarée (lot DETTES-SIM ; ADR-0028 §1 bis.1 pt 7, même principe) : cette sortie ne "
               "modifie ni ℓ, ni le seuil, ni la règle ; un niveau mesuré au-dessus de 0,01 devient une limite écrite, "
               "jamais une révision. Ajoutée après l'exécution unique ; synthétique ; hors décision. Niveau sous un "
               "modèle nul synthétique : rien n'est établi sur des sources réelles (doc 09).")


def deduction(k):
    """Étape S §1.2 sous la garde de blocs (n < 30·ℓ) : vrai si les comptes du cas la vérifient ; None si n ≥ 30·ℓ."""
    c = k["comptes"]
    if k["n"] >= C.N_MIN_BLOCS:
        return None
    return c[V[0]] == 0 and c[V[2]] == 0 and c["z_bloc non publiée"] == c["R"] and c[V[4]] == c["z ≥ 2,33"]


def main():
    ap = argparse.ArgumentParser(description=ITEM + " (lot DETTES-SIM)")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--processus", type=int, default=1, help="paramètre d'exécution, écrit au .log.txt seulement")
    ap.add_argument("--diviseur", type=int, default=1, help="R = R0/d par cas : bit-identité, essais")
    a = ap.parse_args()
    noms = [os.path.join(a.sortie, "garde_n." + x) for x in ("json", "txt", "log.txt")]
    if any(map(os.path.exists, noms)):
        sys.exit("refus : un fichier de sortie existe deja (jamais d'ecrasement)")
    shas = {os.path.basename(f): S.sha256_fichier(f) for f in (os.path.abspath(__file__), G.__file__, S.__file__,
                                                                C.__file__)}
    debut, journal, tous, res = time.gmtime(), [], set(), []
    with (multiprocessing.Pool(a.processus) if a.processus > 1 else contextlib.nullcontext()) as pool:
        for L, n, p, g, R0 in CAS:
            R, x = R0 // a.diviseur, {"classes": [Counter() for _ in G.CLASSES], "bornes": [[] for _ in G.CLASSES],
                                      V[0]: [], V[2]: [], V[4]: []}
            t0, taches = time.perf_counter(), ((float(p), L, n, r) for r in range(R))
            recs = pool.imap(C.tache, taches, 20) if pool else map(C.tache, taches)
            try:
                k, pids = S.agreger(float(p), L, n, R, G.suivre(recs, x, R))
            except RuntimeError as exc:
                sys.exit(f"ECHEC D'ORACLE, aucun fichier ecrit : {exc}")
            k = G.completer(k, p, g, x)
            k["deduction_etape_S"] = deduction(k)
            if k["deduction_etape_S"] is False:
                sys.exit(f"ECHEC : deduction de l'etape S par. 1.2 non tenue, L={L} n={n} p={p} ; aucun fichier ecrit")
            res.append(k)
            tous |= pids
            journal.append(f"cas L={L} n={n} p={p} R={R} : {time.perf_counter() - t0:.1f} s (horloge murale) ; "
                           f"PID distincts {len(pids)}")
            print(journal[-1], file=sys.stderr, flush=True)
    ent = {"schema": "shogen.sim-garde-n.v1", "item": ITEM, "script_sha256": shas,
           "journal": "docs/G1-lot-DETTES-SIM.md, pré-enregistrement", "etiquette": "ajoutée après l'exécution unique ; "
           "synthétique ; hors décision",
           "parametres": {"N": C.NSRC, "cas": [list(x) for x in CAS], "diviseur": a.diviseur, "ell": C.ELL,
                          "seuil_z": str(C.SEUIL_Z), "comparaison": "≥, Decimal non arrondi",
                          "garde_seuil": str(C.SEUIL_HIST), "garde_blocs_n_min": C.N_MIN_BLOCS, "graine": C.GRAINE,
                          "chaine_graine": C.CHAINE, "chaine_effective_r0": C.CHAINE.format(
                              g=C.GRAINE, p=float(CAS[0][2]), L=CAS[0][0], n=CAS[0][1], r=0),
                          "decimal_prec": C.PREC, "classes_garde": [nom for nom, _ in G.CLASSES],
                          "prefixe": f"R/{G.DIV_PREFIXE}", "seuil_lecture": str(G.SEUIL_LECTURE)},
           "alpha_nominal": 1 - NormalDist().cdf(2.33), "consequence_predeclaree": CONSEQUENCE, "cas": res}
    tx = G.texte(ent).replace("SHOGEN-CRITERE-GARDE-NIVEAU-1 (", ITEM + " (", 1)
    tx += (f"Déduction de l'étape S §1.2 sous la garde de blocs (REJETTE = discordance = 0 ; z_bloc non publiée = R ; "
           f"rejet non qualifiable = #{{garde tenue ∧ z ≥ 2,33}}) : vérifiée dans "
           f"{sum(k['deduction_etape_S'] is True for k in res)} cas sur {len(res)} (tous à n < 7 200).\n")
    js = json.dumps(ent, ensure_ascii=False, indent=1) + "\n"
    log = [f"script {os.path.abspath(__file__)} ; sha256 {shas}", f"python {sys.version} ; {sys.executable}",
           f"plateforme {platform.platform()} ; cpu_count {os.cpu_count()} ; processus {a.processus}",
           f"ligne de commande {sys.argv}", time.strftime("debut %Y-%m-%dT%H:%M:%SZ", debut)
           + time.strftime(" ; fin %Y-%m-%dT%H:%M:%SZ", time.gmtime()), *journal,
           f"PID distincts ayant servi des réplications, sur l'exécution : {len(tous)}",
           f"sha256 garde_n.json {hashlib.sha256(js.encode('utf-8')).hexdigest()}",
           f"sha256 garde_n.txt {hashlib.sha256(tx.encode('utf-8')).hexdigest()}"]
    os.makedirs(a.sortie, exist_ok=True)
    for nom, contenu in zip(noms, (js, tx, "\n".join(log) + "\n")):
        with open(nom, "xb") as f:
            f.write(contenu.encode("utf-8"))


if __name__ == "__main__":
    main()
