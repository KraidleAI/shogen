"""Journaux synthétiques des tests du lot PLAN-S2BIS, au format du collecteur (run_params, window_close, lectures de
journal.journal_entry), contre le harnais du commit d'analyse (s2-harness d'une extraction de f35a70c, PLAN_S2BIS_HARNAIS,
modules contrôlés contre les épingles de parametres.json). Aucune barre oblique inverse : saut de ligne par chr(10)."""
import json
import os
import shutil
import tempfile

import commun

HARNAIS = os.environ.get("PLAN_S2BIS_HARNAIS")
if not HARNAIS:
    raise RuntimeError("PLAN_S2BIS_HARNAIS non posée : dossier s2-harness d'une extraction du commit d'analyse (README)")
PRM = commun.lire_parametres()
commun.importer_harnais(HARNAIS, PRM["harnais_sha256"])
r1, records, window = (commun.H[n] for n in ("r1", "records", "window"))

W = 60
VEN = 1787875200            # 2026-08-28T00:00Z, vendredi (calme) ; samedi VEN + 86400 (stress)
NL = chr(10)
GEANT = "1000000000"        # σ qui ne déclenche jamais l'axe staleness


def dossier(test, prefixe):
    """Dossier temporaire (sous TMPDIR) retiré à la fin du test."""
    d = tempfile.mkdtemp(prefix=prefixe)
    test.addCleanup(shutil.rmtree, d, True)
    return d


def params(pool, classes, sigma, tau):
    """run_params : pool, classe de chaque flux, σ et τ par classe (chaînes), calendrier calme/stress du week-end UTC."""
    return records.run_params_record({
        "pool": list(pool), "w": W, "sigma_classe": dict(sigma), "sigma_class_of_flux": dict(classes),
        "tau_classe": dict(tau), "decimal_prec": 50, "seuil_historique_valeur": 10, "n_min_hors_enveloppe": 4,
        "strate_calendar": window.WEEKEND_STRATE_SPEC})


def marqueur(ws):
    return records.window_close_record(ws, window.strate_from_spec(ws, window.WEEKEND_STRATE_SPEC), ws + 55.0)


def lecture(ws, f, etat="ok", prix="100", age=10):
    """etat : « ok », « nul » (statut ok sans prix) ou un statut de panne ; age : staleness t_fin − source_ts en
    secondes (entier), None : aucun horodatage porté."""
    return {"window_start": ws, "flux_id": f, "kind": "place", "currency": "USD",
            "status": "ok" if etat == "nul" else etat, "http_status": 200, "price": None if etat == "nul" else prix,
            "source_ts": None if age is None else ws + W - age, "fetch_ts": ws + 55.0, "sha256_raw": None,
            "extra": {}}


def journaux(dossier, fenetres, motif, pool, classes=None, sigma=None, tau=None):
    """Un démarrage (run_params) puis, par fenêtre i, les lectures du pool (motif(i, f) : None, lecture absente ; un
    état ; ou un dict d'arguments de `lecture`) et le marqueur. Par défaut : une classe « place », σ géant, τ = 0,5."""
    classes = classes or {f: "place" for f in pool}
    sigma = sigma or {c: GEANT for c in set(classes.values())}
    tau = tau or {c: "0.5" for c in set(classes.values())}
    controle, lus = [params(pool, classes, sigma, tau)], []
    for i, ws in enumerate(fenetres):
        for f in pool:
            e = motif(i, f)
            if e is not None:
                lus.append(lecture(ws, f, **(e if isinstance(e, dict) else {"etat": e})))
        controle.append(marqueur(ws))
    for nom, lignes in (("control.jsonl", controle), ("journal.jsonl", lus)):
        with open(os.path.join(dossier, nom), "w", encoding="utf-8", newline=NL) as f:
            f.writelines(json.dumps(x, ensure_ascii=False) + NL for x in lignes)
    return dossier


def prm(**sur):
    """parametres.json du lot, clés de premier niveau remplacées par `sur` (copie profonde)."""
    p = json.loads(json.dumps(PRM))
    p.update(sur)
    return p


def prm_fixture(pool, bloc3, rendu_sha, t0, n_fixe, plages=(), **sur):
    """Paramètres d'une fixture : unités « u<flux> » du pool, classe « place », bloc 3 et sha256 du faux rendu."""
    return prm(pool_d1bis={"unites": {f"u{f}": f for f in pool}, "seuil_presque_mort": True},
               classes={f: "place" for f in pool},
               rendu_j28={"chemin": "-", "sha256": rendu_sha, "bloc3": {s: list(v) for s, v in bloc3.items()}},
               segment={"t0": t0, "n_fixe": n_fixe, "plages_exclues": [list(x) for x in plages]}, **sur)


def ecrire_prm(chemin, p):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False)
    return chemin


def rendu(chemin, valeurs):
    """Faux rendu : bloc 3 (en-tête de strate, « P̂_more  = » à deux espaces, ligne de strate poolée à un espace), bloc 4,
    puis une section de sensibilité qui répète un bloc 3 : seul le premier bloc 3 doit être lu."""
    lignes = ["[ÉTIQUETTE] j28", "[BLOC 3] R1"]
    for st, (n, k, p) in valeurs.items():
        lignes += [f"  ── strate « {st} » : n = {n} fenêtres complétées ; K = {k} (fenêtres à ≥ 2 écarts)",
                   f"    P̂_more  = {p}", f"    « {st} » : n = {n} ; K = {k} ; P̂_more = 0.5 ; pool = 5 flux"]
    lignes += ["[BLOC 4] L&M", "[SENSIBILITÉ] PLAGE INCLUSE", "[BLOC 3] R1"]
    lignes += [f"  ── strate « {st} » : n = 1 fenêtres complétées ; K = 0 (fenêtres à ≥ 2 écarts)" for st in valeurs]
    with open(chemin, "w", encoding="utf-8", newline=NL) as f:
        f.write(NL.join(lignes) + NL)
    return chemin
