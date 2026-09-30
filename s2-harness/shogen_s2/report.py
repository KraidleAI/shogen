"""Table de sortie §6 — recalculable offline (ADR-0003). COMPLÈTE (6 blocs) à M1c.

Conception : docs/10-mesures-pilotes-design.md §6 (« tout chiffre du rapport se
recalcule depuis le journal par un lecteur sans accès à Shōgen », ADR-0003).

Six blocs (§6), tous calculés à M1c :
  1. **Paramètres** — depuis `run_params` : pool, w, seuils, précision, version,
     dates, calendrier de strates committé, contrôle d'horloge, **composition de
     devise du pool** (§2, devise marquée) + résidu de peg USDT/USD = R2(2a) ρ_resid,
     CALCULÉ au bloc 5 (référence croisée).
  2. **Journal brut** — par fenêtre×source : valeur, devise, horodatage porté,
     statut d'écart, sha256 des octets bruts (ADR-0005 : hash toujours).
  3. **R1** — p̂ᵢ, n, K par strate, P̂₀/P̂₁/P̂_more, z **ou** la **queue binomiale
     exacte** sous la garde (§5.4) **ou** « historique insuffisant » nu (dégénéré),
     comptes non évaluables, A(window-stationarity).
  4. **L&M** — Ê(Θ), Ê(Θ²), Var̂(Θ) par strate, corrélations φ **signées** par
     paire de flux ; matrice de co-écarts complète (consommée par le drapeau 2 §5.6,
     bloc 6) ; corrélations entre CLUSTERS et agrégation flux→source réalisées au
     bloc 5 (requièrent la partition R2).
  5. **R2** (r2.py) — table ASN datée (§4.1) ; les 5 statistiques de contenu par
     paire (ρ_raw, ρ_resid, T/T_Δ, (K,z), δ), jamais fusionnées (§4.2) ; arêtes
     méthode `basis:doc` avec doc_url/doc_fetched (§4.3) ; les 7 résidus §4.1.
  6. **Tête de certificat** — partition NOMMÉE, **k_eff, k nominal**, les DEUX
     drapeaux (« historique insuffisant » §5.4 ; « co-défaillance non expliquée par
     R2 » §5.6, tri-état).

`render_report` ne lit QUE les fichiers de journal → recalculable par un tiers.
Sortie **déterministe** (mêmes fichiers → même texte) : répétition générale du
claim de recalculabilité (plan §5).
"""

from __future__ import annotations

import argparse
import os
import sys
from decimal import Decimal

from . import r2, records
from .lm import compute_lm
from .r1 import (
    A_WINDOW_STATIONARITY,
    analysis_pools,
    build_window_strate,
    classify_cells,
    compute_r1,
    parse_journal,
)
from .window import verify_markers_against_spec


def _fmt_dec(x) -> str:
    """Decimal → chaîne exacte (recalculable) ; None → tiret."""
    return "-" if x is None else str(x)


def _iso_utc(ts) -> str:
    """epoch → ISO-8601 UTC (déterministe) pour la colonne « heure » de la table ASN
    (§6 bloc 5 : « résolveur, heure »). None → tiret."""
    if ts is None:
        return "-"
    from datetime import datetime, timezone
    return datetime.fromtimestamp(float(ts), timezone.utc).isoformat()


def _comptes(recs, strates) -> list:
    """(marqueurs, clock_checks, asn) → fenêtres DISTINCTES par strate (dédup de n), asn, horloges."""
    ws = build_window_strate(recs[0])
    return [sum(1 for s in ws.values() if s == st) for st in strates] + [len(recs[2]), len(recs[1])]


def _retires(avant, apres, strates) -> str:
    """Comptes retirés d'`avant` à `apres` (bloc 1 ; ADR-0028 D5, SHOGEN-EXCL-COMPTE-1)."""
    d = [x - y for x, y in zip(_comptes(avant, strates), _comptes(apres, strates))]
    fen = ", ".join(f"{st} {k}" for st, k in zip(strates, d)) or "0 (aucune fenêtre au journal)"
    return f"fenêtres distinctes (window_close) {fen} ; asn_attribution {d[-2]} ; clock_check {d[-1]}"


def render_report(control_path: str, journal_path: str, exclude_ranges=(), segment=None) -> str:
    ranges = records.exclusion_ranges(exclude_ranges)   # ADR-0025 ; défaut : aucune
    params_list, clock_checks, markers = records.parse_control(control_path)
    asn_records = records.parse_asn(control_path)
    # Concordance des run_params successifs (fail-closed, §E) — même garde que
    # l'oracle. La table M1c calcule les 6 blocs → clés R1 **ET** R2 exigées présentes
    # (un run_params amputé d'une clé de partition n'est pas recalculable, §E).
    params = records.effective_run_params(
        params_list,
        load_bearing=records.LOAD_BEARING_KEYS + records.R2_LOAD_BEARING_KEYS,
    )
    # Strates journalées == calendrier committé (fail-closed, §5.3) — même garde
    # que l'oracle : une table sur des strates trafiquées serait un mensonge. Clés
    # porteuses PRÉSENTES (garanties par effective_run_params), lues sans défaut.
    div = verify_markers_against_spec(markers, params["strate_calendar"])
    if div:
        raise ValueError(
            f"strates journalées incohérentes avec le calendrier committé (§5.3) : {div[:5]}"
        )
    # Filtre de lecture unique APRÈS la garde §5.3 (ADR-0028 D5) : blocs 1-6 sur les enregistrements retenus.
    tous = (markers, clock_checks, asn_records)      # assiette des comptes et dates du bloc 1 (avant filtre)
    markers, clock_checks, asn_records, seg = records.filtre_lecture(params, *tous, ranges, segment)
    readings = parse_journal(journal_path)
    pool = list(params["pool"])
    w = int(params["w"])
    # σ PAR CLASSE + τ RELATIF (ADR-0021) — même décodage partagé que les 3 autres
    # lecteurs recalculables (records.sigma_tau_from_params), zéro divergence.
    sigma_by_class, sigma_class_of_flux, tau = records.sigma_tau_from_params(params)
    seuil_hist = Decimal(str(params["seuil_historique_valeur"]))
    n_min = int(params["n_min_hors_enveloppe"])
    # Pool d'analyse (ADR-0028 D1) APRÈS l'exclusion : blocs 3-6 ; bloc 2 (journal brut) : pool.
    pools, pool_an, retraits = analysis_pools(markers, readings, pool)
    cas_b = any(ps != pool_an for ps in pools.values())

    r1 = compute_r1(markers, readings, pool_an, w, sigma_by_class, sigma_class_of_flux,
                    tau, seuil_hist, n_min, pools)
    cells = classify_cells(markers, readings, pool, w, sigma_by_class,
                           sigma_class_of_flux, tau, n_min)
    reading_map = {(int(r["window_start"]), r["flux_id"]): r for r in readings}
    # R2 complet (partition/k_eff, contenu, méthode, clusters, drapeau 2) — recalculé
    # depuis les mêmes enregistrements (ADR-0003). Le peg (bloc 1) le référence.
    r2_out = r2.compute_r2(markers, readings, asn_records, pool_an, w, sigma_by_class,
                           sigma_class_of_flux, tau, params, n_min_horsenv=n_min,
                           pool_by_strate=pools)

    out: list[str] = []
    ap = out.append

    # ── Bloc 1 : Paramètres ────────────────────────────────────────────────
    ap("=" * 78)
    ap("TABLE §6 (S2 Phase A — M1c, COMPLÈTE 6 blocs) — recalculable depuis le "
       "journal seul (ADR-0003)")
    ap("=" * 78)
    ap("\n[BLOC 1] PARAMÈTRES")
    for key in ("harness_version", "classe", "pool", "w", "sample_lead",
                "sigma_classe", "sigma_class_of_flux", "tau_classe", "kappa",
                "seuil_historique_valeur",
                "n_min_hors_enveloppe", "strate_defaut", "decimal_prec",
                "seuil_historique", "seuil_z", "residu_staleness",
                "n_windows_demande", "started_utc", "note_skeleton"):
        if key in params:
            ap(f"  {key:24} = {params[key]}")
    ap(f"  {'run_params_demarrages':24} = {len(params_list)} (concordants sur les "
       f"champs porteurs — §E)")
    if "strate_calendar" in params:
        sc = params["strate_calendar"]
        ap(f"  {'strate_calendar':24} = kind={sc.get('kind')} "
           f"{sc.get('note', '')}".rstrip())
    ws_tous = build_window_strate(tous[0])          # HS2-05 : journal entier, avant segment et exclusion
    strates, deb = sorted(set(ws_tous.values())), sorted(ws_tous)
    ap(f"  {'campagne_fenetres':24} = {len(deb)} fenêtres distinctes au journal (window_close, avant "
       "segment et exclusion)" + (f" : première {deb[0]} = {_iso_utc(deb[0])} ; dernière {deb[-1]} = "
                                  f"{_iso_utc(deb[-1])} (window_start)" if deb else "") + " — HS2-05")
    ap(f"  {'portee_run_params':24} = journal entier, jamais segmenté ni exclu (§E) : run_params_demarrages"
       " = tous les démarrages ; started_utc, n_windows_demande = dernier démarrage (HS2-05)")
    dans_seg = records.filtre_lecture(params, *tous, (), segment)[:3]   # assiette des comptes par plage
    if seg is not None:
        ap(f"  {'segment':24} = [{seg[0]} ; {seg[1]}) = [{_iso_utc(seg[0])} ; {_iso_utc(seg[1])}) "
           "semi-ouvert, fin exclue, même borne sur window_start, ts, harness_ts (run_params conservés) ; "
           f"n fixe = {_fmt_dec(segment.get('n_fixe'))} — ADR-0028 D4, D2 pt 6")
        ap(f"  {'segment_retraits':24} = hors segment : {_retires(tous, dans_seg, strates)} — ADR-0028 D4")
    else:
        ap(f"  {'segment':24} = aucun (journal entier) — ADR-0028 D4")
    for a, b in ranges:        # uniquement si filtre (sans option : aucune ligne ajoutée)
        ap(f"  {'exclusion_window_start':24} = [{a} ; {b}] = [{_iso_utc(a)} ; "
           f"{_iso_utc(b)}] fermée, bornes incluses : hors n, K, P̂_more de toutes les "
           "strates (filtre du lecteur, journal intact) — harnais dégradé, ADR-0025")
        ap(f"  {'exclusion_ts_harness_ts':24} = [{a} ; {b + w}) = [{_iso_utc(a)} ; {_iso_utc(b + w)}) "
           "semi-ouvert : asn_attribution (ts), clock_check (harness_ts), "
           f"w = {w} s de run_params — ADR-0028 D5")
        seule = records.filtre_lecture(params, *dans_seg, [(a, b)])[:3]
        ap(f"  {'exclusion_retraits':24} = [{a} ; {b}] seule (assiette : ligne segment) : "
           f"{_retires(dans_seg, seule, strates)}")
    if ranges:                 # C-4 (i) : chaque plage seule, puis l'union (chevauchement compté une fois)
        ap(f"  {'exclusion_retraits_union':24} = {len(ranges)} plage(s), union (assiette : ligne segment) : "
           f"{_retires(dans_seg, (markers, clock_checks, asn_records), strates)} — SHOGEN-EXCL-COMPTE-1")
    for st, f, k_ok, k_tot, n_s in retraits:   # ADR-0028 D1 (c) : uniquement si retrait
        cas = "(a), hors R2 aussi" if f not in pool_an else "(b), gardé par R2"
        ap(f"  {'pool_analyse_retrait':24} = {f} strate « {st} » : ok = {k_ok} / {k_tot} "
           f"lectures, n = {n_s} — hors R1 et L&M de la strate, cas {cas} (ADR-0028 D1)")
    for st, ps in (pools.items() if retraits else ()):
        ap(f"  {'k_nominal_strate':24} = « {st} » : "
           f"{len(r2.hosts_of_pool(params['flux_hosts'], ps))} sources / {len(ps)} "
           "flux (pool d'analyse, ADR-0028 D1)")
    # Devise MARQUÉE par flux (§2, décision 4) : composition du pool + résidu peg
    # (le démêlage USDT/USD est R2(2a) ρ_resid, CALCULÉ au bloc 5 — référencé ici).
    cur_by_flux: dict = {}
    for r in readings:
        c = r.get("currency")
        if c is not None and r["flux_id"] in pool_an:   # pool d'analyse (ADR-0028 D1)
            cur_by_flux.setdefault(r["flux_id"], c)
    n_usd = sum(1 for c in cur_by_flux.values() if c == "USD")
    n_usdt = sum(1 for c in cur_by_flux.values() if c == "USDT")
    ap(f"  {'devise_composition':24} = {n_usd} USD / {n_usdt} USDT (classe "
       f"« BTC/USD-stable », devise marquée par flux — 10 §2/§9.4)")
    peg_keys = [k for k, v in r2_out["content"]["pairs"].items() if v["is_peg_usdt_usd"]]
    ap(f"  {'residu_peg_usdt_usd':24} = écart de peg USDT/USD = résidu R2(2a) ρ_resid — "
       f"CALCULÉ au bloc 5 (paires USDT×USD : {len(peg_keys)}) (10 §2/§9.4)")
    for cc in clock_checks:
        ap(f"  {'controle_horloge':24} = phase={cc['phase']} médiane_offset(s)="
           f"{_fmt_dec(cc['median_offset'])} "
           f"sources={list(cc['offsets'])} {cc['note'] or ''}".rstrip())

    # ── Bloc 2 : Journal brut ──────────────────────────────────────────────
    ap("\n[BLOC 2] JOURNAL BRUT (par fenêtre × source)")
    hdr = (f"  {'window_start':>12} {'flux':10} {'cur':4} {'statut_ecart':16} "
           f"{'price':>16} {'source_ts':>18} {'sha256[:12]'}")
    ap(hdr)
    ap("  " + "-" * (len(hdr) - 2))
    for (ws, flux) in sorted(cells):
        rd = reading_map.get((ws, flux), {})
        cur = rd.get("currency") or "-"
        price = rd.get("price") or "-"
        src = rd.get("source_ts")
        src_s = _fmt_dec(src)
        sha = (rd.get("sha256_raw") or "-")[:12]
        ap(f"  {ws:>12} {flux:10} {cur:4} {cells[(ws, flux)].value:16} "
           f"{price:>16} {src_s:>18} {sha}")

    # ── Bloc 3 : R1 ────────────────────────────────────────────────────────
    ap("\n[BLOC 3] R1 (test K&L §5 transposé — 10 §5.1/§5.2/§5.4)")
    if r1.get("note"):
        ap(f"  {r1['note']}")
        ap(f"  drapeau « historique insuffisant » = {r1['flag_historique_insuffisant']}")
    for st, blk in r1.get("strates", {}).items():
        ap(f"\n  ── strate « {st} » : n = {blk['n']} fenêtres complétées ; "
           f"K = {blk['K']} (fenêtres à ≥ 2 écarts)")
        ph = (f"    {'source':10} {'p̂ᵢ':>26} {'écart':>6} "
              f"{'panne':>6} {'stale':>6} {'horsE':>6} {'nonÉv':>6} "
              f"{'axes évaluables'}")
        ap(ph)
        for f in blk["per_source"]:            # pool d'analyse de la strate (ADR-0028 D1)
            s = blk["per_source"][f]
            ap(f"    {f:10} {_fmt_dec(s['phat']):>26} {s['ecart']:>6} "
               f"{s['panne']:>6} {s['staleness']:>6} {s['hors_enveloppe']:>6} "
               f"{s['non_eval_hors_env']:>6} {','.join(s['axes_evaluables'])}")
        residu = blk.get("residu_staleness_fail_open", [])
        if residu:
            ap(f"    résidu staleness fail-open (répond sans horodatage porté, (ii) "
               f"non évaluable) : {','.join(residu)} (§G ; 03 §1)")
        ap(f"    P̂₀      = {_fmt_dec(blk['P0'])}")
        ap(f"    P̂₁      = {_fmt_dec(blk['P1'])}")
        ap(f"    P̂_more  = {_fmt_dec(blk['P_more'])}")
        ap(f"    n·P̂_more·(1−P̂_more) = {_fmt_dec(blk['gate_value'])} "
           f"(seuil {_fmt_dec(blk['seuil_historique'])})")
        if blk["flag_historique_insuffisant"]:
            ap("    z       = non publié (garde §5.4 : n·P̂_more·(1−P̂_more) < 10) — "
               "aucun z non significatif présenté comme absence de dépendance (04 §2)")
            if blk.get("queue_exacte_applicable"):
                ap(f"    queue exacte P(K ≥ K_obs={blk['K']} | Bin(n={blk['n']}, P̂_more)) "
                   f"= {_fmt_dec(blk['queue_binomiale_P_K_ge_Kobs'])} "
                   f"({blk.get('queue_note', '')})")
            else:
                ap(f"    HISTORIQUE INSUFFISANT — queue {blk.get('queue_note', '')}")
        else:
            ap(f"    z       = {_fmt_dec(blk['z'])} (seuil {_fmt_dec(blk['seuil_z'])}, "
               f"unilatéral — 10 §5.1)")
    ap(f"\n  {A_WINDOW_STATIONARITY}")

    # ── Bloc 4 : L&M (§5.5) ────────────────────────────────────────────────
    lm_out = compute_lm(markers, readings, pool_an, w, sigma_by_class,
                        sigma_class_of_flux, tau, n_min, pools)
    ap(f"\n[BLOC 4] L&M (§5.5) — fonction de difficulté Θ ; N = {lm_out['N']} flux "
       + ("(pool d'analyse ; N par strate ci-dessous, ADR-0028 D1)" if cas_b else "(pool)"))
    for st, blk in lm_out["strates"].items():
        ap(f"\n  ── strate « {st} » : n = {blk['n']} ; Σ mⱼ = {blk['sum_m']}"
           + (f" ; N = {blk['N']}" if cas_b else ""))
        ap(f"    Ê(Θ)    = {_fmt_dec(blk['E_theta'])}  (= (1/N)·Σᵢ p̂ᵢ — cohérence R1)")
        ap(f"    Ê(Θ²)   = {_fmt_dec(blk['E_theta2'])}  (forme par paires mⱼ(mⱼ−1)/(N(N−1)))")
        ap(f"    Var̂(Θ)  = {_fmt_dec(blk['Var_theta'])}  (= Ê(Θ²) − Ê(Θ)² ; écart au "
           "modèle d'indépendance, L&M éq.16 ; Cov<0 possible)")
        pair_items = list(blk["pair_phi"].items())
        n_defined = sum(1 for _, v in pair_items if v["phi"] is not None)
        n_none = len(pair_items) - n_defined
        n_coecart = sum(1 for _, v in pair_items if v["n11"] > 0)
        ap(f"    corrélations φ signées (indicatrices d'écart) : {n_defined} définies, "
           f"{n_none} non définies (indicatrice constante) / {len(pair_items)} paires de "
           f"flux ; {n_coecart} paires à co-écart (n11>0)")
        # Matrice de co-écarts COMPLÈTE (10 §6 bloc 4, l.544) : TOUTES les paires,
        # y compris φ=None (indicatrice constante — ex. une source en panne partout,
        # le co-écart le plus extrême) et φ=0. CONSOMMÉE par le DRAPEAU 2 (§5.6) au
        # bloc 6 (localisation inter-clusters) ; la donnée (n11..n00) est livrée ici.
        ap("    matrice de co-écarts COMPLÈTE (§6 bloc 4 ; consommée par le drapeau 2 "
           "§5.6 au bloc 6) — par paire [n11 n10 n01 n00] φ (co-écarts en tête) :")
        for k, v in sorted(pair_items, key=lambda kv: (-kv[1]["n11"], kv[0])):
            phi_s = _fmt_dec(v["phi"]) if v["phi"] is not None else "non_définie"
            ap(f"      {k:26} [{v['n11']} {v['n10']} {v['n01']} {v['n00']}] "
               f"φ={phi_s} ({v['signe']})")
        ap(f"    réalisé M1c (bloc 5) : {blk['renvoi_m1c_clusters']}")
        ap(f"    réalisé M1c (bloc 5) : {blk['renvoi_m1c_flux_source']}")
        ap(f"    caveat : {blk['caveat_non_eval']}")

    # ── Bloc 5 : R2 (ASN / contenu / méthode) — §4.1/§4.2/§4.3 ─────────────
    part = r2_out["partition"]
    ap("\n[BLOC 5] R2 — observables de diversité (10 §4)")

    # 5a. Table ASN datée (§4.1) — par hôte : IP, préfixe, ASN (2 bases), résolveur, heure
    ap("\n  (a) AXE ASN (§4.1) — attribution croisée ≥ 2 bases BGP (RIPEstat, Team Cymru)")
    if not part["asn_measured"] and not tous[2]:
        ap("      axe ASN NON MESURÉ : aucun enregistrement asn_attribution au journal "
           "(collect_asn non lancé — c'est l'orchestrateur qui le lance à la campagne).")
    elif not part["asn_measured"]:     # des sondes au journal, aucune retenue pour le pool (G2 B-SEG-1, (c))
        ap(f"      axe ASN NON MESURÉ : aucun enregistrement asn_attribution retenu pour les hôtes du pool — "
           f"{len(tous[2])} au journal, {len(asn_records)} retenus par le filtre de lecture (bloc 1).")
    ahdr = (f"      {'hôte':30} {'flux':18} {'résolveur':18} {'heure(UTC)':26} "
            f"{'IP':16} {'préfixe':16} {'RIPEstat':9} {'Cymru':7} {'holder':14} {'état'}")
    ap(ahdr)
    ap("      " + "-" * (len(ahdr) - 6))
    for h in part["hosts"]:
        rec = part["attribution_by_host"].get(h, {})
        st = part["asn_states"][h]
        flux = ",".join(part["flux_by_host"].get(h, []))
        ap(f"      {h:30} {flux:18} {str(rec.get('resolver') or '-'):18} "
           f"{_iso_utc(rec.get('ts')):26} {str(rec.get('ip') or '-'):16} "
           f"{str(rec.get('prefix') or '-'):16} {str(rec.get('asn_ripestat') or '-'):9} "
           f"{str(rec.get('asn_cymru') or '-'):7} {str(rec.get('holder') or '-'):14} "
           f"{st['kind']}")
        chain = rec.get("cname_chain") or []
        if chain:
            # chaîne CNAME datée (résidu 7) — le narratif ex. Binance → CloudFront (§4.1)
            ap(f"          CNAME: {h} → {' → '.join(chain)}")
    for dv in part["asn_divergences"]:
        ap(f"      DIVERGENCE ASN (résidu 4, instantanéité) hôte {dv['host']} : "
           f"{dv['avant']} → {dv['apres']} (publiée, jamais écrasée)")
    if part["merge_reasons"]:
        ap("      recouvrements MEASURED (fusionnent — jamais basis:doc seul, ADR-0008) :")
        for m in part["merge_reasons"]:
            if m["axis"] == "asn_measured":
                ap(f"        ASN partagé cross-confirmé AS{m['asn']} {m.get('holder') or ''} : "
                   f"{m['hosts']}")
            else:
                ap(f"        identité-copie contenu : flux {m['flux_pair']} → hôtes {m['hosts']}")
    else:
        ap("      aucun recouvrement measured (partition = singletons sur cet axe)")

    # 5b. Axe contenu (§4.2) — 5 statistiques PAR PAIRE, jamais fusionnées
    content = r2_out["content"]
    ap(f"\n  (b) AXE CONTENU (§4.2) — {content['n_windows']} fenêtres ; N_min = "
       f"{content['n_min']} (Fisher)")
    ap(f"      {content['grid_note']}")
    ap(f"      critère de fusion contenu v0 : {content['merge_criterion']}")
    ap(f"      {content['coab_staleness_note']}")
    ap("      par paire [ρ_raw ρ_resid | T T_Δ | co-aberrance K,z | δ lag] — jamais fusionnées :")
    for key in sorted(content["pairs"]):
        pr = content["pairs"][key]
        raw, res, tk, co, dl = (pr["rho_raw"], pr["rho_resid"], pr["tick"],
                                pr["coaberrance"], pr["delta"])
        tags = []
        if pr["basis_doc_triggered"]:
            tags.append("basis:doc→(b)")
        if pr["is_peg_usdt_usd"]:
            tags.append("peg USDT/USD=ρ_resid")
        if tk["exact_copy_merge"]:
            tags.append("COPIE-EXACTE→fusion")
        tagstr = (" {" + ", ".join(tags) + "}") if tags else ""
        if not raw["sufficient"] and not res["sufficient"]:
            ap(f"      {key:26} historique de contenu insuffisant "
               f"(ρ_raw n={raw['n']}, ρ_resid n={res['n']} < N_min){tagstr}")
        else:
            zc = (_fmt_dec(co['z']) if co.get('z') is not None
                  else (f"queue={_fmt_dec(co['queue'])}" if co.get('queue') is not None
                        else "insuff"))
            ap(f"      {key:26} ρ_raw={_fmt_dec(raw['rho'])} ρ_resid={_fmt_dec(res['rho'])} | "
               f"T={_fmt_dec(tk['T'])} T_Δ={_fmt_dec(tk['T_delta'])} | K={co['K']} z/{zc} | "
               f"δlag={dl['best_lag']}{tagstr}")

    # 5c. Axe méthode (§4.3) — 5 arêtes basis:doc, déclenchent (b), ne fusionnent pas
    ap("\n  (c) AXE MÉTHODE (§4.3) — arêtes `basis:doc` (ADR-0008 : déclenchent (b), "
       "ne partitionnent pas)")
    for e in r2_out["method_edges"]:
        if e["kind"] == "upstream":
            ap(f"      {e['from']} → {e['to']} [basis:{e['basis']}] {e['relation']}")
        else:
            ap(f"      {e['node']} estimateur [basis:{e['basis']}] : {e['estimator']}")
        ap(f"          doc_url={e['doc_url']} doc_fetched={e['doc_fetched']}")

    # 5d. Corrélations entre CLUSTERS (§5.5 pt 4) — réalisées ici (partition requise)
    cc = r2_out["cluster_correlations"]
    ap(f"\n  (d) CORRÉLATIONS ENTRE CLUSTERS (§5.5 pt 4) — {cc['convention']}")
    if cc["cluster_pairs"]:
        for k, v in sorted(cc["cluster_pairs"].items()):
            ap(f"      {k} : ρ(Θ̂)={_fmt_dec(v['rho'])} ({v['signe']}) [{v['note']}]")
    else:
        ap(f"      aucun cluster à ≥ 2 flux ({cc['n_multi_clusters']}) → tout reste au φ "
           "par paire de flux (bloc 4)")

    # 5e. Les 7 résidus de l'axe ASN (§4.1) — publiés avec l'observable
    ap("\n  (e) LES 7 RÉSIDUS DE L'AXE ASN (§4.1) — un observable est un témoignage "
       "avec ses résidus (04 §4) :")
    for r in r2_out["residus_asn"]:
        ap(f"      {r}")

    # ── Bloc 6 : Tête de certificat — k_eff, k nominal, les 2 drapeaux ─────
    ap("\n[BLOC 6] TÊTE DE CERTIFICAT (10 §5.6 / 04 §3)")
    ap(f"  k nominal = {part['k_nominal']} (hôtes distincts du pool)")
    if part.get("k_eff_is_upper_bound"):
        # BORNE SUPÉRIEURE (C-A) : ≥1 hôte non attribué gonfle k_eff — jamais lu comme
        # un compte d'indépendance CONFIRMÉ (04 §4.1).
        ap(f"  k_eff     ≤ {_fmt_dec(part['k_eff'])}  (BORNE SUPÉRIEURE ; "
           f"{part['n_unattributed']} hôte(s) non attribué(s) : {part['unattributed']}) "
           f"— {part['k_eff_note']}")
    else:
        ap(f"  k_eff     = {_fmt_dec(part['k_eff'])}  — {part['k_eff_note']}")
    ap("  R3 (déclaration : entité légale, juridiction, méthodologie annoncée) ne "
       "modifie JAMAIS k_eff (§5.6 / 04 §3) — seuls les recouvrements R2 measured partitionnent.")
    ap("  PARTITION NOMMÉE (ADR-0007 : nomme l'amont, jamais un compte anonyme) :")
    for c in part["clusters"]:
        ap(f"    cluster = {c['name']} ; flux = {c['flux']}")
        for up in c["declared_upstreams"]:
            ap(f"        amont déclaré (basis:doc, ne fusionne pas) : {up['from']} → "
               f"{up['to']} ({up['doc_url']})")
        for cav in c["caveats"]:
            ap(f"        caveat : {cav}")
    # Drapeau 1 : historique insuffisant (§5.4), par strate (déjà au bloc 3)
    flags1 = {st: blk["flag_historique_insuffisant"]
              for st, blk in r1.get("strates", {}).items()}
    if r1.get("note"):
        flags1["(global)"] = r1["flag_historique_insuffisant"]
    ap(f"  DRAPEAU 1 « historique insuffisant » (§5.4) par strate : {flags1}")
    # Drapeau 2 : co-défaillance non expliquée par R2 (§5.6), tri-état
    d2 = r2_out["drapeau_2"]
    ap(f"  DRAPEAU 2 « co-défaillance observée non expliquée par les axes R2 » (§5.6) : "
       f"état = {d2['etat'].upper()}")
    ap(f"      {d2['raison']}")
    loc = d2.get("localisation_inter_clusters")
    if loc:
        ap(f"      localisation ({loc['note']}) — consomme la matrice de co-écarts M1b :")
        for st, rows in loc["par_strate"].items():
            top = rows[:5]
            ap(f"        strate « {st} » : "
               + (", ".join(f"{r['pair']}(n11={r['n11']})" for r in top) if top
                  else "aucune paire inter-clusters à co-écart"))
    ap("=" * 78)
    return "\n".join(out)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="python -m shogen_s2.report")
    p.add_argument("journal_dir")
    p.add_argument("--exclude-window-start-range", nargs=2, type=int, action="append",
                   default=[], metavar=("FROM_EPOCH", "TO_EPOCH"),
                   help="plage FERMEE de window_start hors n, K, P_more (repetable, ADR-0025)")
    p.add_argument("--segment-from", type=int, metavar="T0_EPOCH", help="segment [T0 ; fin) (ADR-0028 D4)")
    fin = p.add_mutually_exclusive_group()
    fin.add_argument("--segment-to", type=int, metavar="T_FIN_EPOCH", help="fin exclue du segment")
    fin.add_argument("--segment-n-fixe", type=int, metavar="N",
                     help="fin = window_start de la N-ieme fenetre distincte >= T0, + w (ADR-0024)")
    args = p.parse_args(argv[1:])
    if (args.segment_from is None) != (args.segment_to is None and args.segment_n_fixe is None):
        p.error("segment : --segment-from avec --segment-to ou --segment-n-fixe (ADR-0028 D4)")
    neg = [x for x in [args.segment_from, args.segment_to, *sum(args.exclude_window_start_range, [])]
           if x is not None and x < 0]
    if neg:                    # avant l'API (ValueError, rc 1) : rc 2, rien sur stdout (SHOGEN-NEG-EPOCH-1)
        p.error(f"epoch negatif refuse {neg} (segment ou exclusion ; SHOGEN-NEG-EPOCH-1, ADR-0028 D5)")
    seg = None if args.segment_from is None else {
        "t0": args.segment_from, "t_fin": args.segment_to, "n_fixe": args.segment_n_fixe}
    d = args.journal_dir
    text = render_report(os.path.join(d, "control.jsonl"),
                         os.path.join(d, "journal.jsonl"),
                         exclude_ranges=args.exclude_window_start_range, segment=seg)
    # Émission UTF-8 explicite : la table porte la notation de doc 10 (P̂₀, p̂ᵢ…)
    # dont des diacritiques combinants qu'une console cp1252 (Windows) ne peut
    # encoder ; l'artefact recalculable est UTF-8, indépendant du code-page.
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
