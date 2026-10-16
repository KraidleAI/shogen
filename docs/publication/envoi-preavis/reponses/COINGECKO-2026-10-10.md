# Préavis du rapport de S2 : réponse de CoinGecko et réponse envoyée (2026-10-10)

> Versé par l'orchestrateur le 2026-10-10 11:11:25 UTC (`date -u`). Correspondance privée, confidentielle jusqu'à la publication. Préavis d'origine : `../MISSION-AGENT-PC.md` §8 et `../ENVOIS-PREAVIS.md` (ticket CoinGecko n° 139007).

## 1. Reçu

- **Date** : 2026-10-10 08:19 UTC (affichage `Oct 10, 2026, 4:19 PM GMT+8`).
- **Expéditeur** : Devie (CoinGecko), dans le fil du ticket n° 139007.
- **Transmission** : courriel transmis par l'investisseur dans la session, par copier-coller, à 09:2x UTC.
- **Texte** : tel que collé, en donnée externe.

```text
Devie (CoinGecko)
Oct 10, 2026, 4:19 PM GMT+8
Hi Shogen,

Thank you for the advance notice. We have reviewed the passages you quoted and have the following points. Please see them below.

1. Coverage of the measurement window: the period 2026-08-26 to 2026-09-28 contains 24 weekdays (34,560 minutes) and 10 weekend days (14,400 minutes). The report counts 24,585 calm-stratum windows and 11,397 stress-stratum windows, which is roughly 71% and 79% of those minutes. Your notice does not explain the missing coverage. Could you tell us why?
2. "Outages": the report describes the anomalous windows as outages, but we have no reported outages during that period. Failed or missed readings would be a fairer description. We also do not know how your harness queries the data, so the problem is more likely to have been on the measurement side. Could you share how the data was queried?
3. Declared upstreams: the declared upstream "binance → coingecko" suggests Binance feeds our data. Binance is only one of the many sources we use. Please amend this so the report does not imply otherwise.
4. Section 7.5: φ ≈ 0.901 for coingecko×chainlink is a very strong link, yet the report states "no pair dependence established". CoinGecko and Chainlink are completely different systems, so if both appear to have failed together that often, the most likely common factor is your own machine or network.

Could you please send us the full draft so we can check it?

Regards,
Devie
```

## 2. Envoyé

- **Expéditeur** : l'investisseur, depuis SHOGEN@monarkgate.tech, dans le même fil.
- **Texte** : celui du projet de l'orchestrateur, tel quel. Confirmé par l'investisseur dans la session vers 11:1x UTC (« oui » à la question « parti, et avec le texte tel quel ? »).
- **Pièce jointe** : `Shogen-S2-pilot-measurements-DRAFT.pdf`, sha256 `fd60b4e6c334bf8480f42679f2480a504136e6d0e7913f8a98c140650df27c88`. C'est le même fichier que pour les autres préavis ; il a été contrôlé avant l'envoi.

```text
Subject: Re: Private advance notice: report naming CoinGecko, publication planned on 25 October 2026

Dear Devie,

Thank you for your careful reading and for your four points. Our answers follow, and the full draft is attached, as you requested.

1. Coverage. The measurement period does not cover whole days at either end: it runs from Wednesday 26 August 2026, 19:00 UTC, to Monday 28 September 2026, 01:28 UTC. It therefore contains 32,068 weekday minutes and 14,400 weekend minutes. The report analyses 24,585 of the first (76.7%) and 11,397 of the second (79.1%). All of the missing minutes are on our side, and they affect every feed in the same way:
- in 7,868 minutes, our collection harness recorded nothing because it was stopped or restarting (it started 4,093 times over the campaign, on a single collection host);
- 2,618 further minutes, between 24 September 18:18 and 26 September 15:08 UTC, were measured but excluded, because the DNS resolution of our own host was degraded during that period.
None of these minutes is counted as an anomaly for any feed: they reduce coverage, nothing else. The report sets this out in Sections 2.3 to 2.6; our notice should have said so.

2. "Outages". You are right. In the report, the word means only that our harness did not obtain a valid reading in a given minute. It does not mean a failure of your service, and our data does not establish one. Before publication, we will replace "outage" with "failed reading" wherever the English text uses it in this sense.
The data was queried as follows:
- once per one-minute window, near its end, our harness sent a single unauthenticated HTTPS GET request to the public endpoint https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_last_updated_at=true;
- requests went out from a single collection host, with a 10-second time-out, no retry and no API key;
- the twelve feeds of the campaign were read in sequence, one request each per minute;
- a reading counts as failed if no HTTP response was received (time-out, DNS or connection error), if the HTTP status was not 200, or if the response could not be decoded.
Almost all the minutes in which two or more feeds failed together contain at least two failures of the first kind: no response reached our harness.

3. Declared upstream. You are right that the wording can mislead. The entry "binance → coingecko" records only that Binance is one of the exchanges whose markets CoinGecko integrates. It does not mean that Binance is CoinGecko's only or main source, and it has no effect on any result. The line is copied verbatim from a sealed output and cannot be edited, so we will add a note next to it saying that Binance is one of the many sources CoinGecko aggregates.

4. Section 7.5. We agree with your reading. φ ≈ 0.901 describes how often our harness failed to obtain both readings in the same weekend minute: 108 times, against 19 failures for CoinGecko alone and 5 for Chainlink alone. It is not evidence of a dependence between CoinGecko and Chainlink. Several facts point to a common cause on the measurement side:
- in 118 of the 133 weekend minutes with two or more failed readings, three or more feeds failed at once;
- more than half of those minutes (74 of 133) fall in collection periods in which a DNS check on our own host had failed;
- Chainlink was read through a third-party public Ethereum RPC provider, so a failed "chainlink" reading is not a failure of the Chainlink network either.
The phrase "no pair dependence established" was meant in this sense. We will state it explicitly in Section 7.5.

None of these changes alters a measured value or the verdict, which is computed under the sealed rule. Our next campaign runs on several servers at different hosting providers, precisely so that failures on the measurement side can be told apart from those of a source.

Please keep the draft confidential until publication. We would welcome any further comment by 18 October.

Yours sincerely,

The MONARK Team
```

## 3. Vérification faite par l'orchestrateur avant l'envoi (chaque chiffre, avec sa source)

| affirmation du courriel | source | niveau |
|---|---|---|
| bornes 26/08 19:00 → 28/09 01:28 UTC (mercredi, lundi) | rapport anglais l.104 ; script de contrôle du point 1 | [lu] [calc] |
| 32 068 minutes de semaine, 14 400 de week-end (grille de 46 468) | rapport l.125 ; script de contrôle du point 1 (deux calculs indépendants de la grille, mutant tué), dossier de travail de l'orchestrateur | [calc] |
| 24 585 = 76,7 % ; 11 397 = 79,1 % | rapport l.118 ; sortie du script de contrôle du point 1 | [calc] |
| 7 868 minutes sans mesure = 5 701 + 2 094 sautées hors plage + 73 sans marqueur dans la plage | rapport l.123, l.125, l.416 | [lu] [calc] |
| 4 093 démarrages, un seul hôte | rapport l.126, §2.7 l.131-132 | [lu] |
| 2 618 minutes exclues, du 24/09 18:18 au 26/09 15:08 UTC, DNS dégradé de notre hôte | rapport l.110-113 | [lu] |
| une fenêtre sans marqueur n'est panne pour personne, et aucune lecture ne manque dans une fenêtre marquée | code de collecte `ed479c5:s2-harness/shogen_s2/collector.py` l.15-19 ; rapport l.416 | [lu] |
| requête : GET sans clé, URL exacte, délai de 10 s, aucune nouvelle tentative, lecture en fin de fenêtre, 12 flux en séquence | `ed479c5:s2-harness/shogen_s2/sources.py` l.36-41, l.48-58, l.264-267, l.378-402 ; `collector.py` l.235-246 | [lu] |
| échec = pas de réponse HTTP, statut ≠ 200, ou corps illisible | `sources.py` l.384-399 (`PANNE_TRANSPORT`, `PANNE_HTTP`, `PANNE_DECODE`) | [lu] |
| les co-échecs portent au moins deux échecs de transport | rapport §5.2 l.291-292 (153 sur 154 en semaine, 133 sur 133 le week-end) | [lu] |
| amont `binance → coingecko` = intégration des marchés de Binance par CoinGecko | `ed479c5:s2-harness/shogen_s2/r2.py`, arête `"kind": "upstream"`, champ `relation` ; rapport l.244, l.253 | [lu] |
| ligne copiée d'une sortie scellée | rapport l.220-242 (bloc 6 copié par `sed`) | [lu] |
| table coingecko × chainlink, week-end : [108 19 5 11 265] | rapport l.212, l.214 (marges 127 et 113), l.437 (φ ≈ 0,901) ; seule table entière compatible (φ = 0,9005) | [calc] |
| 118 des 133 minutes à au moins deux échecs en ont trois ou plus | rapport l.619 (m ≥ 3 : 118 en stress) ; K stress = 133 | [lu] [calc] |
| plus de la moitié pendant des démarrages dont la sonde DNS a échoué (`resolve_failed`) : 74 sur 133 | rapport l.613, l.622 | [lu] |
| Chainlink lu par un RPC public tiers | rapport §2.1 l.91, §4.4 l.263 | [lu] |
| campagne suivante sur plusieurs serveurs chez des hébergeurs différents | décision S2-bis, « 4 petits serveurs chez 4 hébergeurs » (JOURNAL l.382) | [lu] |

À ne jamais mettre dans un courriel : le User-Agent du harnais, qui porte l'adresse d'un dépôt.

## 4. Engagements pris dans la réponse

Ils sont pris avant publication, sans aucune valeur mesurée ni verdict changé :
- (i) `outage` devient `failed reading` dans le texte anglais, partout où le mot désigne une lecture manquée. Lignes du rapport anglais : 23, 62, 90, 202, 547, 672, 714 et 715. La l.553 (Pyth) parle d'une panne de fournisseur et reste.
- (ii) Une note est placée près de l'amont déclaré `binance → coingecko` : Binance est une source parmi les nombreuses que CoinGecko agrège. La sortie scellée copiée ne change pas.
- (iii) Le §7.5 dit explicitement qu'un φ élevé décrit des lectures manquées en même temps par le harnais, et non une dépendance entre fournisseurs.

Item : SHOGEN-PUBLICATION-S2-AMENDEMENTS-1 (annexe B d'ADR-0028).

## 5. Hypothèse interne, non mise dans le courriel

Les quatre derniers flux lus à chaque minute sont, dans l'ordre, coingecko, defillama, pyth et chainlink. Les φ les plus élevés du week-end relient justement trois d'entre eux (0,901, 0,691 et 0,686).

Explication possible : une coupure ou une mise en veille du PC au milieu de la séquence ferait échouer surtout les flux lus en dernier.

C'est seulement une hypothèse [inféré] :
- kraken × bitfinex (0,763) ne rentre pas dans ce schéma ;
- le journal ne date pas chaque requête : une seule heure de lecture par fenêtre ;
- elle n'est pas vérifiable sans les journaux.

La campagne S2-bis peut la vérifier en datant chaque requête.
