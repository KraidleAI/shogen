"""Shōgen, sous-lot D8a-3 (SHOGEN-CI-S2-SAUT-1 ; ADR-0028 annexe B.4 l.79 ; docs/adr-0028/G0-lot-D8a.md §11 item 13 ;
lot DETTES-B1, docs/adr-0028/G0-lots-DETTES.md) : verdict du job s2-harness-unittest sur la sortie de la suite, et non
sur le seul code de sortie de unittest, qui reste 0 avec un saut ajouté, un module sorti du motif test*.py ou une
sortie par os._exit(0) avant le résumé (rejeux R8, MT-5, MT-6, MT-7, MT-9 du lot CI-S2). Lance la suite de s2-harness
(python3 -B -m unittest discover -s tests -t . -v), SHOGEN_S2_CAMPAGNE_CONTROL retirée de son environnement, recopie
sa sortie, puis exige : code de sortie 0 ; à la fin du flux de unittest (stderr), le résumé final (tirets, « Ran N
tests in …s », ligne vide, « OK » ou « OK (skipped=k) ») ; exactement k lignes « … skipped '<motif>' », chaque motif
nommant SHOGEN_S2_CAMPAGNE_CONTROL (annexe D.4 a) ; N ≥ PLANCHER, plancher committé, sans égalité figée (choix du G0
de D8a-3 : plancher, et non manifeste des modules ; journal G1 du lot DETTES-B1). Bibliothèque standard seule (R-8).
Lot COLLECTE-BIS, CB-0 (G0 docs/adr-0029/g0-collecte/, PROPOSITION §1 pt 6) : `--aucun-saut` refuse tout saut, même
nommant la variable (suite s2bis) ; `--plancher N` remplace PLANCHER ; sans option, verdict de S2 inchangé. CB-2e
(Q-2 de la G2 de P1, job s2bis seul) : `--egal` exige Ran = plancher (SHOGEN-CI-PLANCHER-SUIVI-1 mécanisé).
Usage : python3 -B verdict-suite-s2.py [dossier] [--aucun-saut] [--egal] [--plancher N] ; sortie 0 conforme, 1 refus
(motifs sur stderr), 3 erreur."""
import os
import re
import subprocess
import sys

VARIABLE = "SHOGEN_S2_CAMPAGNE_CONTROL"
PLANCHER = 406      # tests de la suite après le diff ENREG-ROLE de CB-18 (2026-10-05 ; 405 après DETTES-B1) ; un lot
                    # qui ajoute des tests le relève (SHOGEN-CI-PLANCHER-SUIVI-1) ; l'abaisser desserre la gate :
                    # décision datée seulement
SUITE = ["-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"]
FIN = re.compile(r"\n-{70}\nRan (\d+) tests? in \d+\.\d+s\n\n(OK(?: \(skipped=(\d+)\))?)\n*\Z")
SAUT = re.compile(r" \.\.\. skipped (['\"])(.*)\1$", re.M)


def verdict(texte: str, code: int, plancher: int = PLANCHER, variable=VARIABLE, egal=False) -> list:
    """Motifs de refus du flux `texte` (stderr) d'une suite unittest -v sortie avec `code` ; liste vide : conforme.
    `variable` None : aucun saut admis ; `egal` : Ran = plancher exigé."""
    refus = [f"code de sortie {code}, 0 exigé"] if code else []
    m = FIN.search(texte)
    if not m:
        return refus + ["résumé final absent : tirets, « Ran N tests in …s », puis « OK » ou « OK (skipped=k) », en "
                        "fin de flux"]
    n, k, sauts = int(m.group(1)), int(m.group(3) or 0), SAUT.findall(texte)
    if len(sauts) != k:
        refus.append(f"{len(sauts)} ligne(s) « skipped » lue(s), {k} annoncée(s) par le résumé")
    refus += [f"saut dont le motif ne nomme pas {variable} : {r!r}" if variable else f"saut, aucun admis : {r!r}"
              for _q, r in sauts if not variable or variable not in r]
    if n < plancher:
        refus.append(f"Ran {n} < plancher {plancher} : module sorti du motif test*.py ou tests retirés")
    elif egal and n > plancher:
        refus.append(f"Ran {n} > plancher {plancher} (--egal) : plancher à relever au compte des tests")
    return refus


def lancer(harnais: str, environ=None) -> tuple:
    """Suite -v dans `harnais`, environnement `environ` (défaut : os.environ) sans VARIABLE ; (stderr, stdout, code)."""
    env = {k: x for k, x in (os.environ if environ is None else environ).items() if k != VARIABLE}
    p = subprocess.run([sys.executable, *SUITE], cwd=harnais, capture_output=True, env=env)
    return p.stderr.decode("utf-8", "replace"), p.stdout.decode("utf-8", "replace"), p.returncode


def main(argv: list) -> int:
    reste, plancher, variable = list(argv), PLANCHER, VARIABLE
    egal = "--egal" in reste
    if egal:
        reste.remove("--egal")
    if "--aucun-saut" in reste:
        reste.remove("--aucun-saut")
        variable = None
    if "--plancher" in reste:
        i = reste.index("--plancher")
        plancher = int(reste[i + 1]) if re.fullmatch(r"[0-9]+", "".join(reste[i + 1:i + 2])) else -1
        del reste[i:i + 2]
    if plancher < 0 or len(reste) > 1 or any(x.startswith("-") for x in reste):
        print(f"verdict-suite-s2 : erreur : arguments illisibles {argv!r}", file=sys.stderr)
        return 3
    harnais = reste[0] if reste else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                  "s2-harness")
    if not os.path.isdir(os.path.join(harnais, "tests")):
        print(f"verdict-suite-s2 : erreur : {os.path.join(harnais, 'tests')} introuvable", file=sys.stderr)
        return 3
    err, out, code = lancer(harnais)
    sys.stdout.write(err + out)
    sys.stdout.flush()
    refus = verdict(err, code, plancher, variable, egal)
    for r in refus:
        print(f"verdict-suite-s2 : refus : {r}", file=sys.stderr)
    if not refus:
        sauts = f"sauts nommant {variable}" if variable else "aucun saut"
        print(f"verdict-suite-s2 : conforme (code 0, résumé final, {sauts}, Ran {'=' if egal else '≥'} {plancher})")
    return 1 if refus else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
