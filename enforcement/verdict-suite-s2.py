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
(Q-2 de la G2 de P1, job s2bis seul) : `--egal` exige Ran = plancher (SHOGEN-CI-PLANCHER-SUIVI-1 mécanisé). CB-18m
(G2 de la tranche C de P1, décision de l'orchestrateur) : le job s2-harness-unittest passe `--egal` à son tour, Ran =
PLANCHER. Le couplage avec le test de comptes de B-SEG-1, motif de l'inégalité au G0 de D8a-3, ne tient plus : ses deux
tests nommés lèvent SkipTest dans leur corps, et un test sauté compte dans Ran, variable posée ou non (`lancer` la
retire).
SHOGEN-S2BIS-LIGNE-JOB-LEURRE-1 (G2 de la tranche C de P1) : `etapes` et `lignes_du_job`, analyseur unique de la
ligne d'un job de gates.yml, partagé par les cas K du runner et par l'enregistreur de rôle
(s2-harness/tools/oracle_record.py).
SHOGEN-S2BIS-SUITE-MASQUE-UNITTEST-1 (lot OUT-2, OUT-2b) : `masques` ; une entrée de la racine de la suite au nom d'un
module de la bibliothèque standard est refusée avant tout lancement (sortie 1). Lancé de ce dossier, -m unittest
l'importerait à la place du module standard : unittest lui-même, ou l'un des 40 à 43 autres qu'il charge avant la
découverte (mesuré sous 3.10 à 3.13 ; -I les écarte, sans refus nommé), puis tout module qu'un test importe après la
découverte, qui met la racine en tête de sys.path (-I ne l'écarte pas).
Usage : python3 -B verdict-suite-s2.py [dossier] [--aucun-saut] [--egal] [--plancher N] ; sortie 0 conforme, 1 refus
(motifs sur stderr), 3 erreur."""
import os
import re
import subprocess
import sys

VARIABLE = "SHOGEN_S2_CAMPAGNE_CONTROL"
PLANCHER = 408      # tests de la suite après OUT-2b du lot OUT-2 (2026-10-08 ; 407 après OUT-1b du lot R-1) ; un lot
                    # qui ajoute des tests le relève (SHOGEN-CI-PLANCHER-SUIVI-1), ce que le job exige depuis CB-18m
                    # (--egal) ; l'abaisser desserre la gate : décision datée seulement
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


def masques(harnais: str) -> list:
    """Entrées de la racine `harnais` d'une suite au nom d'un module de la bibliothèque standard
    (sys.stdlib_module_names, Python 3.10 et plus ; nom pris avant le premier point), triées ; liste vide : aucune."""
    return sorted(x for x in os.listdir(harnais) if x.split(".")[0] in sys.stdlib_module_names)


def lancer(harnais: str, environ=None) -> tuple:
    """Suite -v dans `harnais`, environnement `environ` (défaut : os.environ) sans VARIABLE ; (stderr, stdout, code)."""
    env = {k: x for k, x in (os.environ if environ is None else environ).items() if k != VARIABLE}
    p = subprocess.run([sys.executable, *SUITE], cwd=harnais, capture_output=True, env=env)
    return p.stderr.decode("utf-8", "replace"), p.stdout.decode("utf-8", "replace"), p.returncode


CLE = re.compile("([a-z-]+):(?: (.*))?")
PREMIER = re.compile("(name|on|permissions|jobs):(?: .*)?")       # seules clés de premier niveau admises
SEPARATEURS = "".join(map(chr, (11, 12, 13, 28, 29, 30, 133, 8232, 8233)))      # fins de ligne autres que LF
JOB, ETAPE = {"name", "runs-on", "timeout-minutes", "steps"}, {"name", "shell", "run"}  # clés admises
LIBRES = ("python3 --version", f"unset {VARIABLE}")      # seules autres lignes admises dans le bloc de la ligne


def etapes(texte: str, job: str):
    """Étapes du job `job` du texte de gates.yml, dans l'ordre : les lignes du bloc `run:` (sans indentation, vides
    omises) de chaque étape admise, None pour les autres. Admise : clés de ETAPE seules, `shell: bash`, `run` en ligne
    ou en bloc littéral `|` ; seule la clé `run` est lue, jamais un `name: >` ; une étape `if:`, `continue-on-error`,
    `env:` ou `working-directory` est exclue. Clé de job hors de JOB, clé répétée, ligne d'indentation inattendue,
    commentaire entre une clé et sa suite : aucune étape admise ([]). Job absent ou répété, ligne de premier niveau
    hors de PREMIER (`defaults`, `env`, clé entre guillemets ou suivie d'une espace…) ou clé répétée, fin de ligne
    autre que LF : None."""
    lignes = texte.split(chr(10))
    hauts = [PREMIER.fullmatch(x) for x in lignes if x[:1] not in ("", " ", "#")]
    noms = [m[1] for m in hauts if m]                       # clés de premier niveau reconnues
    if (lignes.count(f"  {job}:") != 1 or any(c in texte for c in SEPARATEURS) or len(noms) != len(hauts)
            or len(set(noms)) != len(noms)):
        return None
    pas, cles, suite, sain = [], [], [], True
    for ligne in lignes[lignes.index(f"  {job}:") + 1:]:
        n, t = len(ligne) - len(ligne.lstrip(" ")), ligne.strip()
        m = CLE.fullmatch(t[2:] if n == 6 and t.startswith("- ") else t)
        if not t:
            continue
        if n < 4 and t[0] != "#":
            break                                           # clé du job suivant, ou du premier niveau
        if n > 8:
            suite.append(t)                                 # suite de la dernière clé : bloc, nom plié…
        elif t[0] == "#":
            suite = []                                      # un commentaire clôt la suite d'une clé
        elif m and n == 4:
            cles, suite = cles + [m[1]], []
        elif m and n in (6, 8) and cles[-1:] == ["steps"] and (n == 6) == t.startswith("- ") and (pas or n == 6):
            pas += [{}] if n == 6 else []
            sain, suite = sain and m[1] not in pas[-1], []
            pas[-1][m[1]] = (m[2], suite)
        else:
            sain = False
    if not sain or set(cles) - JOB or len(cles) != len(set(cles)):
        return []
    return [(e["run"][1] if e["run"][0] == "|" else [e["run"][0]] if e["run"][0] and not e["run"][1] else None)
            if set(e) <= ETAPE and "run" in e and e.get("shell") == ("bash", []) else None for e in pas]


def lignes_du_job(texte: str, job: str, motif: str):
    """Lignes du job qui satisfont `motif` (re.fullmatch), lues par `etapes` dans les blocs admis dont toute autre
    ligne est dans LIBRES (un bloc où la ligne côtoie `set +e`, `exit 0` ou un heredoc ne compte pas). None : job
    absent ou illisible (voir `etapes`)."""
    pas = etapes(texte, job)
    return None if pas is None else [x for b in pas if b for x in b if re.fullmatch(motif, x) and all(
        y in LIBRES or re.fullmatch(motif, y) for y in b)]


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
    masque = masques(harnais)                   # SUITE-MASQUE-UNITTEST-1 : refus avant tout lancement de la suite
    if masque:
        print(f"verdict-suite-s2 : refus : {masque} à la racine de {harnais} masque la bibliothèque standard pour -m "
              "unittest (sys.stdlib_module_names) : suite non lancée", file=sys.stderr)
        return 1
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
