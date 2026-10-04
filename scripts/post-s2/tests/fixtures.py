"""Journaux synthétiques des tests du lot POST-PREREG (annexe D.4 a : aucun journal réel n'est lu par un test), au
format du collecteur (records.run_params_record, records.window_close_record, journal.journal_entry). σ géant et
τ = 0,5 par défaut : seules les pannes font des écarts, sauf mention."""
import json
import os

import commun  # noqa: F401  (chemin de s2-harness)
from shogen_s2 import records, window

W = 60
VEN = 1787875200          # 2026-08-28T00:00Z, vendredi (calme) ; samedi VEN + 86400 (stress)
POOL = ["a", "b", "c", "d", "e"]


def params(pool=POOL, **sur):
    p = {"pool": list(pool), "w": W, "sigma_classe": {"place": "1000000000"},
         "sigma_class_of_flux": {f: "place" for f in pool}, "tau_classe": {"place": "0.5"}, "decimal_prec": 50,
         "seuil_historique_valeur": 10, "n_min_hors_enveloppe": 4, "strate_calendar": window.WEEKEND_STRATE_SPEC,
         "flux_hosts": {f: f"h-{f}" for f in pool}}
    p.update(sur)
    return records.run_params_record(p)


def marqueur(ws):
    return records.window_close_record(ws, window.strate_from_spec(ws, window.WEEKEND_STRATE_SPEC), ws + 55.0)


def lecture(ws, f, etat="ok", prix="100", source_ts=None):
    """etat : « ok », « nul » (statut ok sans prix) ou un statut de panne ; source_ts frais (ws + 50) par défaut."""
    return {"window_start": ws, "flux_id": f, "kind": "place", "currency": "USD",
            "status": "ok" if etat == "nul" else etat, "http_status": 200, "price": None if etat == "nul" else prix,
            "source_ts": ws + 50.0 if source_ts is None else source_ts, "fetch_ts": ws + 55.0, "sha256_raw": None,
            "extra": {}}


def ecrire(dossier, controle, lectures):
    for nom, lignes in (("control.jsonl", controle), ("journal.jsonl", lectures)):
        with open(os.path.join(dossier, nom), "w", encoding="utf-8") as f:
            f.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in lignes)
    return dossier


def journaux(dossier, fenetres, motif, pool=POOL, avant=(), **sur):
    """Un démarrage (enregistrements `avant`, puis run_params, clés `sur` comprises) puis, par fenêtre, les lectures du
    pool (motif(i, f) → état, ou (état, source_ts[, prix]) ; None : lecture absente) et le marqueur."""
    controle, lectures = [*avant, params(pool, **sur)], []
    for i, ws in enumerate(fenetres):
        for f in pool:
            if (e := motif(i, f)) is not None:
                etat, ts, prix = (*e, "100")[:3] if isinstance(e, tuple) else (e, None, "100")
                lectures.append(lecture(ws, f, etat, prix, source_ts=ts))
        controle.append(marqueur(ws))
    return ecrire(dossier, controle, lectures)
