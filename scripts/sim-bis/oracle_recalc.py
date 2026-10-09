"""Adaptateur d'oracle croisé avec RECALC-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-13, première passe ;
E-S-01, E-S-51 ; contrat docs/adr-0029/s2bis/ROTATION-S2BIS.md ; SHOGEN-SIM-BIS-CONTRAT-RB6-1) : les fichiers épinglés
du paquet s2bis au commit cité (section « oracle_recalc » de parametres.json : shogen_s2bis.recalc.rotation de RB-6,
son chargeur config_analyse, config/analyse.json et les tests de RB-6, lus comme texte) sont lus dans le dépôt par
`git archive` (lecture seule, aucun verrou), extraits dans un dossier temporaire sous TMPDIR, contrôlés par sha256
avant tout chargement (forme d'oracle_r1), puis chargés sous le nom shogen_s2bis sans toucher sys.path ; seuls ces
fichiers peuvent être chargés. SB-13a : épingle et extraction. SB-13b : chargement. SB-13c : croiser, lois de rotation
de la réplique (regle, mode à R complet) contre celles de RB-6 extrait sur la même entrée (E-S-51). Adaptateur :
jamais importé par le moteur (E-S-01, tests/test_fitness.py) ; ni puissance, ni hasard, ni libm
(tests/test_fitness_tirages.py)."""
import atexit
import hashlib
import importlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

import commun
import regle

PAQUET = "shogen_s2bis"
_CHARGE: dict = {}
_EPINGLE: list = []


def epingle(prm: dict) -> tuple:
    """Épingle du paquet : commit, dossier, fichiers et leurs empreintes ; la source n'en est pas."""
    o = prm["oracle_recalc"]
    return o["commit"], o["dossier"], tuple(sorted(o["fichiers"].items()))


def extraire(prm: dict, dossier: str, depot: str = commun.RACINE) -> str:
    """Fichiers épinglés du paquet au commit de la section « oracle_recalc », lus par `git --no-optional-locks -C
    <depot> archive` et écrits sous `dossier` ; seuls les membres attendus, fichiers réguliers, sont lus (aucune
    extraction d'archive en bloc). Le dépôt doit porter le commit (historique complet en CI, Q-T4-11). Variable de la
    copie scellée posée : CAMPAGNE/variable ; git absent, commit ou fichier introuvable : ORACLE/extraction ; empreinte
    différente de l'épingle : ORACLE/sha256. Rend le chemin du dossier du paquet extrait (s2bis)."""
    commun.garde_campagne()
    o = prm["oracle_recalc"]
    chemins = {f"{o['dossier']}/{f}": f for f in sorted(o["fichiers"])}
    try:
        p = subprocess.run(["git", "--no-optional-locks", "-C", depot, "archive", "--format=tar", o["commit"], "--",
                            *chemins], capture_output=True, timeout=120, check=False)
    except (OSError, subprocess.SubprocessError) as e:
        raise commun.Refus("ORACLE/extraction", f"git : {type(e).__name__}") from None
    if p.returncode:
        raise commun.Refus("ORACLE/extraction", f"git archive {o['commit'][:12]} : sortie {p.returncode}")
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tar:
        lus = {m.name: tar.extractfile(m).read() for m in tar.getmembers() if m.isreg() and m.name in chemins}
    for chemin, f in chemins.items():
        if chemin not in lus or hashlib.sha256(lus[chemin]).hexdigest() != o["fichiers"][f]:
            raise commun.Refus("ORACLE/sha256", f"{chemin} : absent ou différent de l'épingle")
    for chemin, octets in lus.items():
        os.makedirs(os.path.dirname(os.path.join(dossier, chemin)), exist_ok=True)
        with open(os.path.join(dossier, chemin), "wb") as g:
            g.write(octets)
    return os.path.join(dossier, o["dossier"])


def charger(prm: dict) -> dict:
    """{"rotation", "config_analyse", "analyse"} du paquet extrait (extraire), une fois par processus, dans un dossier
    temporaire de TMPDIR retiré à la sortie : modules rotation et config_analyse chargés par importlib sous le nom
    shogen_s2bis, et config/analyse.json lu (JSON). Un shogen_s2bis déjà chargé d'ailleurs, ou un module chargé hors des
    fichiers épinglés : ORACLE/modules. Cache indexé sur l'épingle : même épingle, mêmes modules ; autre épingle dans le
    même processus : ORACLE/epingle (un seul paquet shogen_s2bis par processus)."""
    if not _CHARGE:
        dossier = tempfile.mkdtemp(prefix="oracle_recalc_")
        atexit.register(shutil.rmtree, dossier, True)
        racine = extraire(prm, dossier)
        if PAQUET in sys.modules:
            raise commun.Refus("ORACLE/modules", f"{PAQUET} déjà chargé hors de l'extraction")
        paquet = os.path.join(racine, PAQUET)
        spec = importlib.util.spec_from_file_location(PAQUET, os.path.join(paquet, "__init__.py"),
                                                      submodule_search_locations=[paquet])
        sys.modules[PAQUET] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sys.modules[PAQUET])
        mods = {n: importlib.import_module(f"{PAQUET}.recalc.{n}") for n in ("rotation", "config_analyse")}
        epingles = {os.path.realpath(os.path.join(racine, f)) for f in prm["oracle_recalc"]["fichiers"]}
        charges = {os.path.realpath(m.__file__) for n, m in list(sys.modules.items()) if n.split(".")[0] == PAQUET}
        if charges - epingles:
            raise commun.Refus("ORACLE/modules", f"modules hors des fichiers épinglés : {sorted(charges - epingles)}")
        with open(os.path.join(racine, "config", "analyse.json"), "rb") as f:
            mods["analyse"] = json.loads(f.read().decode("utf-8"))
        _CHARGE.update(mods)
        _EPINGLE.append(epingle(prm))
    if _EPINGLE != [epingle(prm)]:
        raise commun.Refus("ORACLE/epingle", "paquet déjà chargé sous une autre épingle dans ce processus")
    return dict(_CHARGE)


CLES = ("K", "S", "K_r", "S_r", "C", "C1", "C_S", "K_crit", "K_moyen")


def replique(prm: dict, graine: str, strate: str, n: int, n_s: int, classes: dict, premiere, R: int) -> dict:
    """Lois de la réplique sur l'entrée de lois() de RB-6, par classe triée (clés CLES) : la suite des (K^(r), S^(r)),
    r = 1 … R, que reçoivent decider et complet (regle._entrees, comme deux_modes), puis le mode à R complet (E-S-29,
    jamais l'arrêt anticipé, propre à SIM-BIS) : C, C1, C_S, K_crit et moyenne exacte K̄_rot."""
    out = {}
    for c in sorted(classes):
        base, a, ks, S = regle._entrees(classes[c], premiere, graine, strate, n, n_s, prm, R, True)
        vals = list(ks)
        f = regle.complet(*a, vals, R, prm, S)
        out[c] = {"K": base["K"], "S": S, "K_r": [k for k, _s in vals], "S_r": [x for _k, x in vals], "C": f["C"],
                  "C1": f["C1"], "C_S": f["C_S"], "K_crit": f["K_crit"], "K_moyen": f["moyenne"]}
    return out


def recalcul(prm: dict, h: dict, graine: str, strate: str, n: int, classes: dict, premiere, R: int) -> dict:
    """Lois de RB-6 extrait (rotation.lois) au seuil de la règle pour R (regle.seuil : SIM-BIS calcule, RB-6 reçoit ;
    contrat ROTATION-S2BIS.md §8 pt 4) ; C1 = #{r : K^(r) ≥ k_crit − 1} par rotation.resume, k_crit de la garde
    d'analyse.json ; S_crit et S_moyen non comparés (E-S-32 ne demande que C_S ; P-5 de l'avis de la tranche 3)."""
    s, g, rot = regle.seuil(R, prm["regle"]["alpha"]), h["analyse"]["gardes"]["k_crit"], h["rotation"]
    return {c: dict({k: x[k] for k in CLES if k != "C1"}, C1=rot.resume(g - 1, x["K_r"], s)[0])
            for c, x in rot.lois(graine, strate, n, classes, premiere, R, s).items()}


def croiser(prm: dict, h: dict, graine: str, strate: str, n: int, n_s: int, classes: dict, premiere, R: int) -> tuple:
    """Oracle croisé (E-S-51) sur une entrée {classe: {unité: masque}} : (écarts, réplique, RB-6). Écarts : (classe,
    clé) dont les valeurs diffèrent (CLES, classes des deux côtés), puis ("o", r, u) pour chaque r = 1 … R et chaque
    unité décalée dont o(r, u) diffère (regle.decalage contre rotation.decalage). Mêmes noms d'unité (même chaîne
    hachée), même première unité, même R des deux côtés (contrat §8 ; avis de la tranche 3, §4)."""
    a, b = replique(prm, graine, strate, n, n_s, classes, premiere, R), recalcul(prm, h, graine, strate, n, classes,
                                                                                 premiere, R)
    ecarts = [(c, k) for c in sorted(set(a) | set(b)) for k in CLES if c not in a or c not in b or a[c][k] != b[c][k]]
    unites, rot = sorted({u for s in classes.values() for u in s} - {premiere}), h["rotation"]
    ecarts += [("o", r, u) for r in range(1, R + 1) for u in unites
               if regle.decalage(graine, strate, r, u, n) != rot.decalage(graine, strate, r, u, n)]
    return ecarts, a, b
