# Mission — préparer l'envoi des 17 préavis privés de Shōgen (le 2026-10-04)

Pour : l'agent Claude Code du PC de l'investisseur. De : l'orchestrateur de Shōgen (session cloud). Validé par l'investisseur le 2026-10-04 (« rapport validé. on l'envoie aujourd'hui »).

## Règles (à respecter strictement)

1. **Tu n'envoies rien toi-même.** Tu prépares chaque message dans la boîte **SHOGEN@monarkgate.tech** (brouillon), ou tu le présentes à l'investisseur, prêt à copier. **C'est l'investisseur qui clique sur « Envoyer ».**
2. **Un message par destinataire.** Jamais de copie (Cc) ni de copie cachée (Cci) vers un autre acteur. Jamais deux acteurs dans le même message.
3. **Copie le texte exactement**, sans rien changer, sans reformuler, sans ajouter d'emoji ni de formule. L'objet va dans le champ « Objet ».
4. **Pièce jointe** : seulement là où c'est indiqué, le fichier `Shogen-S2-pilot-measurements-DRAFT.pdf` ; avant de joindre, vérifie son empreinte : `sha256 = fd60b4e6c334bf8480f42679f2480a504136e6d0e7913f8a98c140650df27c88` (sous Windows : `certutil -hashfile Shogen-S2-pilot-measurements-DRAFT.pdf SHA256`). Si l'empreinte diffère, **arrête-toi** et préviens l'investisseur.
5. **Formulaires web** (CoinGecko, DefiLlama, PublicNode) : l'investisseur remplit lui-même le formulaire ; tu lui donnes l'adresse de la page, l'objet et le texte à coller ; aucun fichier joint ; adresse de contact à saisir : SHOGEN@monarkgate.tech.
6. **Après chaque envoi**, note dans un fichier `ENVOIS-PREAVIS.md` : acteur, adresse, date et heure d'envoi (UTC), objet, pièce jointe (oui/non). Ce fichier revient ensuite au dépôt.
7. **Confidentialité** : ne publie rien, ne partage ces textes nulle part ailleurs. Ne mentionne aucun autre sujet ni aucun autre projet dans ces messages.

## Calendrier

- Envoi : **dimanche 4 octobre 2026**, tous les messages le même jour.
- Fin du délai de réponse : **18 octobre 2026** (14 jours).
- Publication prévue : **25 octobre 2026** au plus tôt.
- Réponses attendues sur **SHOGEN@monarkgate.tech** : transmets-les telles quelles à l'orchestrateur ; n'y réponds pas toi-même.

## Tableau d'envoi

| n° | acteur | adresse ou formulaire | pièce jointe |
|---|---|---|---|
| 1 | Binance | pr@binance.com | oui (PDF) |
| 2 | Coinbase | press@coinbase.com | oui (PDF) |
| 3 | Kraken | press@kraken.com | oui (PDF) |
| 4 | OKX | Institutional@okx.com | oui (PDF) |
| 5 | Bitstamp | press@bitstamp.net | oui (PDF) |
| 6 | Gemini | institutional@gemini.com | oui (PDF) |
| 7 | Bitfinex | press@bitfinex.com | oui (PDF) |
| 8 | CoinGecko | https://support.coingecko.com/hc/en-us/requests/new (support request form) | non |
| 9 | DefiLlama | https://defillama.com/support (support page) | non |
| 10 | Pyth | press@pyth.network | oui (PDF) |
| 11 | Chainlink | press@chain.link | oui (PDF) |
| 12 | Cloudflare | press@cloudflare.com | oui (PDF) |
| 13 | Amazon Web Services | aws-pr@amazon.com | non |
| 14 | Imperva | impervaPR@imperva.com | non |
| 15 | PublicNode | https://www.publicnode.com/contact (contact form) | non |
| 16 | RIPE NCC | press@ripe.net | non |
| 17 | Team Cymru | media@cymru.com | non |

## 1. Binance

- **À** : pr@binance.com
- **Objet** : Private advance notice: report naming Binance, publication planned on 25 October 2026
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Binance PR and Communications team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Binance. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Binance:
- The binance feed carries no timestamp, so staleness is “not evaluable for binance, kraken and bitfinex” (Section 9.3).
- Section 3.5 counts 372 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays) and 46 out of 11,397 in the stress stratum (weekends), all outages.
- On the network (ASN) axis, api.binance.com forms a class of its own on AS16509 (Amazon), with a CNAME chain from “binance to CloudFront” (Sections 4.1 and 4.2).
- Section 6 describes the pairs binance×bitstamp and binance×gemini: “No significance per pair: this is descriptive”.
- Section 8.7 lists five readings of our raw journal missing from our main journal, “four from binance and one from okx_ticker”, in the range excluded from the analysis; this concerns our own record-keeping.
- Binance is also named in Sections 2.1, 4.1 and 7.1.

Context. Each anomaly is a reading by our own harness, “as observed by this instrument (host, DNS and network of the harness included)” (Section 1), not an established outage of your service: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft report is attached. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 2. Coinbase

- **À** : press@coinbase.com
- **Objet** : Private advance notice: report naming Coinbase, publication planned on 25 October 2026
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Coinbase Press team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Coinbase. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Coinbase:
- The coinbase feed (host api.exchange.coinbase.com) belongs to the class of exchanges whose feed carries a timestamp (place_horodatee, Section 2.1).
- Section 3.5 counts 56 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays) and 11 out of 11,397 in the stress stratum (weekends), all outages.
- On the network (ASN) axis, api.exchange.coinbase.com is one of the hosts that “share AS13335 (Cloudflare), on the delivery side” (Section 1): “the observed IP is the delivery layer, not the origin” (Section 4.4).
- The report lists the declared upstream “coinbase → pyth”, which does not merge classes (Section 4.2).
- Coinbase is also named in Section 4.1.

Context. Each anomaly is a reading by our own harness, “as observed by this instrument (host, DNS and network of the harness included)” (Section 1), not an established outage of your service: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft report is attached. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 3. Kraken

- **À** : press@kraken.com
- **Objet** : Private advance notice: report naming Kraken, publication planned on 25 October 2026
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Kraken Press team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Kraken. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Kraken:
- The kraken feed carries no timestamp, so staleness is “not evaluable for binance, kraken and bitfinex” (Section 9.3).
- Section 3.5 counts 34 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays) and 46 out of 11,397 in the stress stratum (weekends), all outages.
- On the network (ASN) axis, api.kraken.com is one of the hosts that “share AS13335 (Cloudflare), on the delivery side” (Section 1): “the observed IP is the delivery layer, not the origin” (Section 4.4).
- Section 7.5 gives φ ≈ 0.454 (calm) and ≈ 0.763 (stress) for kraken×bitfinex, noting “no pair dependence established”.
- Kraken is also named in Sections 2.1, 4.1, 4.2 and 7.1.

Context. Each anomaly is a reading by our own harness, “as observed by this instrument (host, DNS and network of the harness included)” (Section 1), not an established outage of your service: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft report is attached. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 4. OKX

- **À** : Institutional@okx.com
- **Objet** : Private advance notice: report naming OKX, publication planned on 25 October 2026
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear OKX Institutional team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names OKX. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about OKX:
- Two OKX feeds, okx_ticker and okx_index, are read from one host, www.okx.com (Section 2.1).
- Section 3.5 counts, for each feed, 64 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays) and 6 (okx_ticker) or 7 (okx_index) out of 11,397 in the stress stratum (weekends), all outages.
- On the network (ASN) axis, www.okx.com is one of the hosts that “share AS13335 (Cloudflare), on the delivery side” (Section 1): “the observed IP is the delivery layer, not the origin” (Section 4.4).
- Section 7.5 gives φ ≈ 0.452 for okx_ticker×okx_index in calm, noting “no pair dependence established”.
- Section 8.7 lists one okx_ticker reading of our raw journal missing from our main journal, in the range excluded from the analysis; this concerns our own record-keeping.
- OKX is also named in Sections 4.1 and 4.2.

Context. Each anomaly is a reading by our own harness, “as observed by this instrument (host, DNS and network of the harness included)” (Section 1), not an established outage of your service: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft report is attached. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 5. Bitstamp

- **À** : press@bitstamp.net
- **Objet** : Private advance notice: report naming Bitstamp, publication planned on 25 October 2026
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Bitstamp Press team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Bitstamp. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Bitstamp:
- The bitstamp feed (host www.bitstamp.net) belongs to the class of exchanges whose feed carries a timestamp (place_horodatee, Section 2.1).
- Section 3.5 counts 475 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays) and 39 out of 11,397 in the stress stratum (weekends), all outages.
- On the network (ASN) axis, www.bitstamp.net forms a class of its own on AS19551, with a CNAME chain from “bitstamp to Incapsula” (Sections 4.1 and 4.2).
- Section 6 describes the pairs binance×bitstamp and bitstamp×gemini: “No significance per pair: this is descriptive”.
- Section 11.1, an analysis added after the pre-registration, gives bitstamp the lowest rate of ok readings in the calm stratum, ≈ 0.981, and reports “no feed removed” (Section 11.1).
- Bitstamp is also named in Section 4.1.

Context. Each anomaly is a reading by our own harness, “as observed by this instrument (host, DNS and network of the harness included)” (Section 1), not an established outage of your service: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft report is attached. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 6. Gemini

- **À** : institutional@gemini.com
- **Objet** : Private advance notice: report naming Gemini, publication planned on 25 October 2026
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Gemini Institutional team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Gemini. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Gemini:
- The gemini feed (host api.gemini.com) belongs to the class of exchanges whose feed carries a timestamp (place_horodatee, Section 2.1).
- Section 3.5 counts 68 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays: 65 outages, 3 stale readings) and 21 out of 11,397 in the stress stratum (weekends: 19 outages, 2 stale readings); a stale reading carries a timestamp older than the class threshold.
- On the network (ASN) axis, api.gemini.com forms a class of its own on AS14618 (Amazon), with a CNAME chain from “gemini to an AWS load balancer” (Sections 4.1 and 4.2).
- Section 6 describes the pairs bitstamp×gemini and binance×gemini: “No significance per pair: this is descriptive”.
- Gemini is also named in Section 4.1.

Context. Each anomaly is a reading by our own harness, “as observed by this instrument (host, DNS and network of the harness included)” (Section 1), not an established outage of your service: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft report is attached. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 7. Bitfinex

- **À** : press@bitfinex.com
- **Objet** : Private advance notice: report naming Bitfinex, publication planned on 25 October 2026
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Bitfinex Press team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Bitfinex. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Bitfinex:
- The bitfinex feed (host api-pub.bitfinex.com) carries no timestamp, so staleness is “not evaluable for binance, kraken and bitfinex” (Section 9.3).
- Section 3.5 counts 32 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays: 30 outages and 2 out of envelope, with a relative difference from the other feeds' median beyond the class threshold) and 51 out of 11,397 in the stress stratum (weekends: all outages).
- On the network (ASN) axis, api-pub.bitfinex.com is one of the hosts that “share AS13335 (Cloudflare), on the delivery side” (Section 1): “the observed IP is the delivery layer, not the origin” (Section 4.4).
- Section 7.5 gives φ ≈ 0.454 (calm) and ≈ 0.763 (stress) for kraken×bitfinex, noting “no pair dependence established”.
- Bitfinex is also named in Sections 2.1, 4.1, 4.2, 5.1 and 7.1.

Context. Each anomaly is a reading by our own harness, “as observed by this instrument (host, DNS and network of the harness included)” (Section 1), not an established outage of your service: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft report is attached. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 8. CoinGecko

- **Formulaire** : https://support.coingecko.com/hc/en-us/requests/new (support request form)
- **Objet** : Private advance notice: report naming CoinGecko, publication planned on 25 October 2026
- **Pièce jointe** : aucune (formulaire : le rapport est « available on request »)

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear CoinGecko team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names CoinGecko. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about CoinGecko:
- The coingecko feed (host api.coingecko.com) belongs to the aggregator class (agregateur, Section 2.1).
- Section 3.5 counts 56 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays) and 127 out of 11,397 in the stress stratum (weekends), all outages.
- On the network (ASN) axis, api.coingecko.com is one of the hosts that “share AS13335 (Cloudflare), on the delivery side” (Section 1): “the observed IP is the delivery layer, not the origin” (Section 4.4).
- The report lists the declared upstreams “binance → coingecko” and “coingecko → defillama”, and an estimator declaration for coingecko; declared upstreams do not merge classes (Section 4.2).
- Section 7.5 gives φ ≈ 0.901 (coingecko×chainlink) and ≈ 0.686 (coingecko×defillama) in stress, noting “no pair dependence established”.
- CoinGecko is also named in Section 4.1.

Context. Each anomaly is a reading by our own harness, “as observed by this instrument (host, DNS and network of the harness included)” (Section 1), not an established outage of your service: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft is available on request. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 9. DefiLlama

- **Formulaire** : https://defillama.com/support (support page)
- **Objet** : Private advance notice: report naming DefiLlama, publication planned on 25 October 2026
- **Pièce jointe** : aucune (formulaire : le rapport est « available on request »)

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear DefiLlama team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names DefiLlama. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about DefiLlama:
- Section 3.5 counts, for the defillama feed, 159 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays: 158 outages, 1 stale reading) and 226 out of 11,397 in the stress stratum (weekends: all outages).
- Section 11.1, added after the pre-registration, gives defillama the lowest rate of ok readings in stress, ≈ 0.980, with “no feed removed” (Section 11.1).
- On the network (ASN) axis, coins.llama.fi is one of the hosts that “share AS13335 (Cloudflare), on the delivery side” (Section 1): “the observed IP is the delivery layer, not the origin” (Section 4.4).
- The declared upstream “coingecko → defillama”, documented from docs.llama.fi/llms-full.txt, does not merge classes (Section 4.1).
- Section 7.5 gives φ ≈ 0.691 (defillama×chainlink) and ≈ 0.686 (coingecko×defillama) in stress, noting “no pair dependence established”.
- DefiLlama is also named in Sections 2.1 and 4.2.

Context. Each anomaly is a reading by our own harness, “as observed by this instrument (host, DNS and network of the harness included)” (Section 1), not an established outage of your service: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft is available on request. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 10. Pyth

- **À** : press@pyth.network
- **Objet** : Private advance notice: report naming Pyth, publication planned on 25 October 2026
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Pyth team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Pyth. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Pyth:
- The pyth feed was configured but removed from the analysis pool: the report records no reading with status ok out of 40,804, with HTTP 401 from 2026-08-26 (Section 2.2).
- Section 9.3 states: “No price data was received from Pyth over the whole campaign: access to the queried service was refused (HTTP 401) from the first day”.
- The report lists the declared upstream “coinbase → pyth” and an estimator declaration for pyth (Section 4.2).
- Pyth is also named in the report header, in the reading conventions and in Sections 1, 2.1, 4.1, 4.3, 5.1, 7.1 and 7.2.

Context. The report places Pyth outside the analysis pool and states that “no measurement of this report bears on it” (Section 4.4) and that “nothing shows an outage of Pyth” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft report is attached. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 11. Chainlink

- **À** : press@chain.link
- **Objet** : Private advance notice: report naming Chainlink, publication planned on 25 October 2026
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Chainlink Press team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Chainlink. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Chainlink:
- Our harness read the chainlink feed by eth_call through the public RPC ethereum-rpc.publicnode.com, which shares AS13335 (Cloudflare) with other hosts (Section 4.2): “The classification of chainlink in the AS13335 cluster therefore bears on the reading infrastructure.” (Section 4.4).
- Section 3.5 counts 71 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays: 69 outages and 2 out of envelope, with a relative difference from the other feeds' median beyond the class threshold) and 113 out of 11,397 in the stress stratum (weekends: all outages).
- Section 7.5 gives φ ≈ 0.901 (coingecko×chainlink) and ≈ 0.691 (defillama×chainlink) in stress, noting “no pair dependence established”.
- Section 9.3 notes that “chainlink is observed only through a public RPC”.
- Chainlink is also named in Sections 2.1, 4.1 and 5.1.

Context. Each anomaly is a reading by our own harness, “as observed by this instrument (host, DNS and network of the harness included)” (Section 1), not an established outage of your service: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1). “Nothing is said about the accuracy of a price” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft report is attached. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 12. Cloudflare

- **À** : press@cloudflare.com
- **Objet** : Private advance notice: report naming Cloudflare, publication planned on 25 October 2026
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Cloudflare Press team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Cloudflare. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Cloudflare:
- The report states that “7 of the 10 hosts of the pool share AS13335 (Cloudflare), on the delivery side” (Section 1); the partition merges them into “a cluster of seven hosts and eight feeds” (Section 4.1).
- The printed CNAME chains include “okx to Cloudflare's CDN” (Section 4.2).
- Our probe relied on “one DNS resolver (Cloudflare DoH) per probe record” (Section 9.3), namely cloudflare-dns.com (Section 2.7).
- Section 2.4 excludes 24 to 26 September 2026, when failed resolutions of our probe reached 15.3% against 1.85% outside that range; the report calls this “health of the DNS harness, not a source statistic” and states “causality not established” (Section 2.4); the report does not attribute these failures to the resolver.

Context. The report notes that “the observed IP is the delivery layer, not the origin” (Section 4.4), and it attributes no anomaly to a network operator: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft report is attached. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 13. Amazon Web Services

- **À** : aws-pr@amazon.com
- **Objet** : Private advance notice: report naming Amazon Web Services, publication planned on 25 October 2026
- **Pièce jointe** : aucune (rapport « available on request »)

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear AWS Press team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names AWS, CloudFront and two Amazon networks. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Amazon Web Services:
- Two hosts of the pool form classes of their own on Amazon networks (Section 4.1): api.binance.com on AS16509, printed as “AMAZON-02 - Amazon.com, Inc.”, and api.gemini.com on AS14618, printed as “AMAZON-AES - Amazon.com, Inc.” (Section 4.1).
- The printed CNAME chains include “binance to CloudFront, gemini to an AWS load balancer” (Section 4.2).

Context. The report notes that “the observed IP is the delivery layer, not the origin” (Section 4.4), and it attributes no anomaly to a network operator: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft is available on request. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 14. Imperva

- **À** : impervaPR@imperva.com
- **Objet** : Private advance notice: report naming Incapsula (Imperva), publication planned on 25 October 2026
- **Pièce jointe** : aucune (rapport « available on request »)

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Imperva Press team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Incapsula, which we understand to be part of Imperva. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Incapsula:
- The host www.bitstamp.net forms a class of its own, one of “three singletons” (Section 4.1), on AS19551, printed as “INCAPSULA - Incapsula Inc” (Section 4.1).
- The printed CNAME chains include “bitstamp to Incapsula” (Section 4.2).

Context. The report notes that “the observed IP is the delivery layer, not the origin” (Section 4.4), and it attributes no anomaly to a network operator: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft is available on request. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 15. PublicNode

- **Formulaire** : https://www.publicnode.com/contact (contact form)
- **Objet** : Private advance notice: report naming PublicNode, publication planned on 25 October 2026
- **Pièce jointe** : aucune (formulaire : le rapport est « available on request »)

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear PublicNode team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names PublicNode. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about PublicNode:
- Our harness read the chainlink feed by eth_call through ethereum-rpc.publicnode.com (Section 4.4).
- On the network (ASN) axis, this endpoint is one of the hosts that “share AS13335 (Cloudflare), on the delivery side” (Section 1). Section 4.4 adds: “The classification of chainlink in the AS13335 cluster therefore bears on the reading infrastructure.”
- Section 3.5 counts, for the chainlink feed read through this endpoint, 71 anomalous one-minute windows out of 24,585 in the calm stratum (weekdays) and 113 out of 11,397 in the stress stratum (weekends); Section 9.3 notes that “chainlink is observed only through a public RPC”.
- The endpoint is also named in Sections 2.1, 4.1 and 4.2 and in the glossary.

Context. The report describes your endpoint as “a reading infrastructure, not the upstream of the feed” (Section 4.4), and it attributes no anomaly to the reading path: “These counts describe; they identify no cause.” (Section 9.3). The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft is available on request. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 16. RIPE NCC

- **À** : press@ripe.net
- **Objet** : Private advance notice: report naming RIPEstat (RIPE NCC), publication planned on 25 October 2026
- **Pièce jointe** : aucune (rapport « available on request »)

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear RIPE NCC Press Team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names RIPEstat, a service of the RIPE NCC. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about RIPEstat:
- Section 4.2 records a “cross attribution RIPEstat and Team Cymru « concordant » for the 10” hosts of the pool: the report used RIPEstat to cross-check the network (ASN) attributed to each host.
- This is the only passage of the report that names RIPEstat.

Context. The report uses these attributions as an input and does not assess the service itself. The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft is available on request. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```

## 17. Team Cymru

- **À** : media@cymru.com
- **Objet** : Private advance notice: report naming Team Cymru, publication planned on 25 October 2026
- **Pièce jointe** : aucune (rapport « available on request »)

Texte à copier (du « Dear » à la signature incluse) :

```text
Dear Team Cymru media team,

We write on behalf of Shōgen, a measurement project, to give you private advance notice of a report that names Team Cymru. We plan to publish it on 25 October 2026.

The report, “The S2 pilot measurements — campaign report”, presents a pre-registered analysis of BTC/USD and BTC/USDT price feeds measured from 2026-08-26 to 2026-09-28. Its decision rule was sealed with a third-party RFC 3161 timestamp before the analysis (Section 8.1), which was run once (Section 8.8).

What the report says about Team Cymru:
- Section 4.2 records a “cross attribution RIPEstat and Team Cymru « concordant » for the 10” hosts of the pool: the report used Team Cymru data to cross-check the network (ASN) attributed to each host.
- This is the only passage of the report that names Team Cymru.

Context. The report uses these attributions as an input and does not assess the service itself. The overall verdict is negative (“R1 discriminates” = false, Section 1): the report “neither establishes nor excludes a co-failure of the sources” (Section 1).

Any factual error in these passages may be reported to SHOGEN@monarkgate.tech within 14 days. We will correct those we can confirm before publication; the measured values remain those computed under the sealed rule. The full draft is available on request. Please keep this notice and any draft material confidential until publication.

Yours sincerely,

The MONARK Team
https://monarkgate.tech
```
