# Delivery-infrastructure concentration report — pool of `<libre.client>` (template)
> Template filed on 2026-10-15 (`date -u`, PRODUIT-R2), English version of `RAPPORT-CONCENTRATION-POOL.md` (French prevails;
> basis and rules as there); check: `scripts/publication/gabarit_controle.py`. Each field names the harness output that
> produces it (`path:line` at the template's commit); a filled report keeps the fixed text byte for byte, fields all filled or all empty.

## 1. Pool identity and date
- Client (declaration, rank R3: never changes k_eff, doc 04 §3): `<libre.client>`
- Date of the report (`date -u`, form `YYYY-MM-DDTHH:MM:SSZ`): `<date.rapport>`
- Configured pool, line `pool` of block 1 of the rendering (`s2-harness/shogen_s2/report.py:203` (`{key:24} = {params[key]}`)):
  `<rendu.pool>`; feeds without any `ok` reading leave the analysis pool (ADR-0028 D1, `s2-harness/shogen_s2/report.py:268`
  (`pool_analyse_retrait`)), and the partition bears on the analysis pool only.
- Segment and excluded ranges, line `segment` of block 1 (`s2-harness/shogen_s2/report.py:224` (`{'segment':24}`)), then
  each line `exclusion_window_start` (`s2-harness/shogen_s2/report.py:232` (`exclusion_window_start`)): `<rendu.segment>`

## 2. Method
- **k_eff on the delivery side**: number of classes of the partition of the hosts by the measured R2 overlaps
  (`s2-harness/shogen_s2/r2.py:772` (`def compute_partition`)); nominal k = number of distinct hosts. The observed address
  is that of the delivery layer (CDN, anycast), not of the origin (residual 1, `s2-harness/shogen_s2/r2.py:87`
  (`RESIDUS_ASN`)). k_eff is not an independence count.
- **Nominal k**, a method detail outside the head (doc 04 l.172: only k_eff is published at the head), line
  `k nominal` of block 6 (`s2-harness/shogen_s2/report.py:623` (`k nominal = `)): `<rendu.k-nominal>`
- **Dated, cross-confirmed ASN partition**: one probe per host (`s2-harness/shogen_s2/r2.py:345` (`def collect_asn`)),
  DNS-over-HTTPS then RIPEstat and Team Cymru (`s2-harness/shogen_s2/r2.py:315` (`def resolve_host_real`)); a host merges
  only if both bases agree, otherwise it is an unconfirmed singleton and k_eff an upper bound
  (`s2-harness/shogen_s2/r2.py:381` (`def _asn_state`)). Date: last retained probe record per host.
- **Declared upstreams `basis:doc`**: named, they do not merge (ADR-0008); they point to where content is measured
  (`s2-harness/shogen_s2/r2.py:120` (`METHOD_EDGES`)).
- **Content corroborations**: five statistics per pair of feeds; exact identity alone merges (`s2-harness/shogen_s2/r2.py:709`
  (`def compute_content`); `s2-harness/shogen_s2/r2.py:199` (`MERGE_CRITERION_V0`)).
- **Outside this report**: measured co-failure (R1, doc 04 §2); blocks 3 and 4 and the flags of block 6 are not copied.

## 3. Head (block 6 of the rendering)
- k_eff and its note (`s2-harness/shogen_s2/report.py:631` (`k_eff     = `); upper bound:
  `s2-harness/shogen_s2/report.py:627` (`BORNE SUPÉRIEURE`)): `<rendu.k-eff>`
- Date of the partition (`s2-harness/shogen_s2/report.py:635` (`date de la partition`)): `<rendu.date-partition>`
- Named partition, declared upstreams, caveats (`s2-harness/shogen_s2/report.py:645` (`PARTITION NOMMÉE`)):
```text
<rendu.partition>
```

## 4. Observables (block 5 of the rendering)
Copied lines: (a) dated ASN, CNAME, divergences (`s2-harness/shogen_s2/report.py:525` (`(a) AXE ASN`)); (b) per-pair
lines (`s2-harness/shogen_s2/report.py:565` (`(b) AXE CONTENU`)); (c) `basis:doc` edges
(`s2-harness/shogen_s2/report.py:596` (`(c) AXE MÉTHODE`)); (e) residuals (`s2-harness/shogen_s2/report.py:616` (`(e) LES 7`)).
```text
--- (a)
<rendu.table-asn>
--- (b)
<rendu.contenu>
--- (c)
<rendu.amonts>
--- (e)
<rendu.residus>
```

## 5. Axes not measured (mandatory field)
Doc 04 l.129-139, copied in the original French (gloss: an unmeasured axis remains a possible common mode; the list
of measured axes is exhaustive and mandatory):
> Chaque certificat embarque, en clair, son périmètre :
>
> 1. Un axe non mesuré reste un mode commun possible. La liste des axes
>    mesurés est exhaustive dans le certificat ; tout le reste est hors
>    mesure. (Knight & Leveson appliqué à nous-mêmes : nos axes sont nos
>    deux universités.) **Cette exhaustivité est un champ NON OPTIONNEL du
>    certificat** (ADR-0019 D7, GTM canal 2) : c'est la parade au seul canal de
>    conflit que ni la vérification offline ni le benchmark public ne ferment —
>    le jeu sur les axes ; le canal 2 payant (oracle certifiant son propre feed)
>    n'est défendable que si chaque certificat publie ce qu'il n'a **pas** mesuré.
>    Exigence ferme en S4, candidate à un ADR de spec du certificat.

Measured axes, exhaustive list: the ASN of the delivery address of each host (R2, cross-confirmed); exact content identity
between feeds (R2). Not measured, at least: (1) co-failure of the feeds (R1); (2) the origin behind a CDN or anycast, and
the operator (residuals 1 and 2); (3) plural vantage points and resolvers (residuals 3 and 5); (4) ASN and CNAME between
two probe records (residuals 4 and 7); (5) IPv6: only A records are resolved, and the Cymru form does not cover IPv6
(`s2-harness/shogen_s2/r2.py:292` (`def _cymru_asn`)); (6) the TLS certificate issuer and the attestors (doc 04 §1); (7) a
common method outside the copied `basis:doc` edges, an upstream that adds noise to its copies (doc 04 §5); (8) the
quality of the upstream market (doc 04 §4 pt 6) and redacted entries (pt 5); (9) R3 declarations, published, never
counted. Specific to this pool (unattributed hosts, feeds removed by D1, others): `<libre.axes-pool>`

## 6. Offline recomputation recipe
Fingerprints: `control.jsonl` `<sha256.control>`; `journal.jsonl` `<sha256.journal>`; `raw.jsonl` `<sha256.raw>`;
rendering (output of command 3) `<sha256.rendu>`. Harness commit `<commit.harnais>`; Python `<version.python>`.
Variables: `J` (folder of the three journals), `DEPOT` (repository), `H` (extraction), `S` (output), `O` (options of the rendering).
```bash
cd "$J" && sha256sum control.jsonl journal.jsonl raw.jsonl        # 1. equal to the fingerprints
git -C "$DEPOT" archive <commit.harnais> s2-harness | tar -x -C "$H"     # 2. extraction of the commit
cd "$H/s2-harness" && env -u SHOGEN_S2_CAMPAGNE_CONTROL python3 -B -m shogen_s2.report "$J" $O > "$S/rendu.txt"  # 3.
sha256sum "$S/rendu.txt"                                           # 4. equal to the fingerprint of the rendering
```
Command 3: `s2-harness/shogen_s2/report.py:755` (`def main`); `O` is read from the segment field (§1): `--segment-from`
with `--segment-to` or `--segment-n-fixe` (line `segment`), then one `--exclude-window-start-range` per line
`exclusion_window_start`, in their order; `O` is empty without segment or range. R2 is
computed there by `s2-harness/shogen_s2/r2.py:1030` (`def compute_r2`), as in the recomputable entry point
`s2-harness/shogen_s2/r2.py:1068` (`def recompute_r2_from_journal`). Journals of the client pool only, never the sealed
journals of S2 (SHOGEN-RENDU-CLI-REPORT-1).

## 7. Limitations and vocabulary
- Collection: the harness collects only the frozen pool of `s2-harness/shogen_s2/sources.py:239` (`SPECS`), with the
  `basis:doc` edges of that pool; a client pool needs an attached work package, without which this template cannot be filled.
- Snapshot partition; one observer, one resolver per probe record (residual 5); k_eff counted on the delivery side:
  nothing is said about the origin, the accuracy or the depth of a feed (doc 09 l.24 and l.30), nor outside the named
  pool, segment and observer. The byte-for-byte equality of a rendering replayed elsewhere is not measured.
- No R1 claim until S2-bis has rendered; no regulatory sentence (no DORA or MiCA text held, AVIS-PRODUIT-APRES-S2 §3).
  Vocabulary: all of doc 09; the check mechanizes only part of it.
