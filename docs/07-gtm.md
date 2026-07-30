# Shōgen — Go-to-market (v0, 2026-07-30)

> **Statut des chiffres.** Toute figure marquée *(web 2026-07-30)* provient
> de recherches web de ce jour — pistes datées, non vérifiées sur artefact
> détenu ; sources en fin de document. Les figures issues de papiers
> détenus portent *(détenu)*. Aucun chiffre d'ici n'entre dans un document
> d'assurance ou une publication sans repasser par le protocole biblio.

## 1. La thèse de vente en une phrase

Le phénomène que Shōgen mesure est déjà **monétisé par les attaquants**
(Sevim & Torres : fenêtres d'exploitation cross-chain statistiquement
prédictibles créées par l'amont commun des DONs — *détenu*, p. 1) et déjà
**payé par les victimes** (les protocoles de prêt versent des millions
annuels en primes de liquidation et en contrats de gestion de risque) —
Shōgen vend l'instrument de mesure au côté qui saigne.

## 2. L'anti-cible d'abord : pourquoi pas Chainlink en premier

L'acheteur évident est l'acheteur conflité. Le récit commercial des
oracles installés repose sur l'indépendance proclamée de leurs réseaux ;
l'ensemble exact des agrégateurs amont d'un feed n'est pas même publié
(constat Chaos Labs, lead du balayage R-1). Un k_eff public les expose
avant de les servir. Leur moment d'achat viendra — défensif, quand la
métrique sera devenue la question qu'on leur pose. Le plan ne dépend pas
d'eux ; il les *atteint*.

## 3. Les acheteurs, séquencés

### Canal 1 — les cabinets de gestion de risque (revenu, mandats existants)

Le marché existe et paie déjà, chiffres de gouvernance publics
*(web 2026-07-30)* : Aave DAO a payé Gauntlet **1,6 M$/an** (ramené de
2 M$), Chaos Labs **~2 M$/an** après amendements ; Gauntlet a renouvelé
chez Compound pour **2,3 M$**. Deux cabinets rien que chez Aave — le
budget « risque » d'une grande DAO est de l'ordre de plusieurs M$/an, et
Chaos Labs a *nommé le manque* que Shōgen comble (diversité des sources
invérifiable par un tiers). L'offre : Shōgen comme **instrument des
cabinets** — le k_eff et la corrélation de co-mises-à-jour dans leurs
rapports, sous leur marque, notre certificat en preuve. Un partenariat =
tous les protocoles clients du cabinet.

### Canal 2 — les oracles challengers (distribution, différenciation)

Le marché des oracles n'est pas un monopole *(web 2026-07-30)* :
Chainlink ~33 Md$ de TVS sur ~505 protocoles (part estimée 60-70 % selon
les sources), mais Chronicle ~7,5 Md$, RedStone ~3,6 Md$ (le plus
rapide — ~×46 depuis début 2023), Pyth ~3,1 Md$. Un challenger n'a rien
à perdre à la transparence : « nos feeds sont livrés avec leur certificat
de diversité, vérifiable offline » est une arme contre l'incumbent qui ne
publie pas ses amonts. Les challengers achètent des armes ; les
incumbents achèteront des boucliers.

### Canal 3 — les protocoles de prêt eux-mêmes (la douleur chiffrée)

Ce que coûte le phénomène, en public *(web 2026-07-30)* : fuite OEV
cumulée estimée **>500 M$** ; Aave V3 a versé **23,4 M$ de primes de
liquidation en 2024** (~4 M$/mois), Venus 5,8 M$ ; la journée record des
2-3 février 2025 a liquidé **>10 Md$** en 24 h (dont >200 M$ sur Aave).
L'existence d'API3 OEV Network (recapture d'OEV, adoptée par Compound et
d'autres) prouve que les protocoles *paient* pour reprendre cette valeur —
Shōgen est complémentaire : API3 recapture l'enchère, Shōgen mesure et
certifie la cause amont (la fausse indépendance qui rend l'exploitation
prédictible — Sevim & Torres, *détenu*).

### Canal 4 — assureurs et souscripteurs on-chain

Un k_eff est un paramètre actuariel : primes fonction de la diversité
mesurée du feed qui garde le protocole assuré. S'ouvre après le
benchmark ; même logique que l'assurance d'agents côté Kraidle (00-idees,
idée différée).

### Canal transverse — le client commun avec Kraidle

L'opérateur d'agents de trading, dès S3-S4 : *bounded authority,
attested perception*, une seule vente.

## 4. Le mouvement d'ouverture : le benchmark public

Avant de vendre : **publier la mesure, gratuitement**. Les k_eff et
corrélations de co-mises-à-jour des feeds majeurs, recalculables par
quiconque — un « L2Beat des sources de données ». Le précédent est
éprouvé : L2Beat (rollups) et clientdiversity.org (clients Ethereum) sont
des tableaux de mesure indépendants devenus des institutions citées par
tout l'écosystème, qui forcent les projets mesurés à répondre. Effets :

1. **La demande** : chaque feed mal noté est un prospect chez tous ses
   consommateurs.
2. **La neutralité** : un certificat vendu par le mesuré ne vaut rien ;
   un tiers vérifiable offline, si. C'est le moat structurel — un oracle
   qui voudrait « faire son propre Shōgen » produirait un bulletin
   d'auto-notation.
3. **Les données de S2** : le benchmark *est* le prototype qui tranche —
   Sevim & Torres démontrent que les données publiques suffisent (63
   feeds, 12 009 mises à jour analysées — *détenu*, p. 1).
4. **L'antériorité du papier S5** : la mesure publiée date le travail.

## 5. Le modèle de revenu (esquisse, à ADR quand S2 aura tranché)

- **Gratuit** : le benchmark public, les scores agrégés, le vérificateur
  (cohérent avec « sans confiance dans Shōgen » — jamais payant).
- **Payant** : le monitoring continu par feed avec alertes (dégradation de
  k_eff, apparition d'un amont commun) ; les certificats à la demande sur
  un pool de sources choisi par le client (le cas cabinet de risque et le
  cas challenger) ; l'API d'intégration dans les rapports tiers.
- **Plus tard** : la souscription (canal 4) et le tier entreprise du duo
  Kraidle+Shōgen.

## 6. Risques de ce plan

1. **Représailles narratives de l'incumbent** (« méthodologie biaisée ») —
   parade : tout est recalculable offline, le certificat embarque ses
   témoignages ; la neutralité n'est pas déclarée, elle est vérifiable.
2. **Un cabinet de risque internalise la métrique** — parade : notre
   instrument est publié et vérifiable, le leur serait un dire d'expert ;
   et le benchmark public nous donne l'avance du nom.
3. **Le benchmark fâche avant de payer** — séquencement : les premiers
   contacts cabinets se font *avant* la publication des scores nominatifs
   (offre de préavis privé, pratique standard du responsible disclosure).
4. **Chiffres de marché mouvants** — toutes les figures ci-dessus sont
   datées 2026-07-30 et re-mesurables ; aucune ne porte de mécanisme de
   fraîcheur, donc aucune ne doit être re-citée sans re-vérification.

## Sources (web 2026-07-30 — pistes, non détenues)

Contrats risque : [CoinDesk — Gauntlet quitte Aave](https://www.coindesk.com/tech/2024/02/27/days-after-ditching-aave-risk-manager-gauntlet-moves-to-rival-lender-morpho) ·
[Aave Governance — Chaos Labs renewals](https://governance.aave.com/t/arfc-chaos-labs-aave-risk-management-service-renewal/19306) ·
[Protos — Gauntlet/Compound 2,3 M$](https://protos.com/gauntlets-2-3m-contract-renewal-with-compound-faces-backlash/).
Marché oracles : [CoinLaw — Chainlink Statistics 2026](https://coinlaw.io/chainlink-statistics/) ·
[RedStone — Oracles Comparison 2026](https://blog.redstone.finance/2026/03/30/blockchain-oracles-comparison-chainlink-vs-pyth-vs-redstone-2026/) ·
[Messari — Chainlink vs Pyth](https://messari.io/compare/chainlink-vs-pyth-network).
OEV : [Gate Ventures — OEV In-Depth](https://medium.com/@gate_ventures/oracle-extractable-value-oev-the-hidden-revenue-and-new-frontier-in-defi-in-depth-analysis-3fc796664045) ·
[Decrypt — API3 OEV Network](https://decrypt.co/239092/api3s-oev-network-to-recapture-oracle-extractable-value-for-lending-protocols) ·
[Chorus One — Introduction to OEV](https://chorus.one/reports-research/an-introduction-to-oracle-extractable-value-oev) ·
[RedStone — What is OEV](https://blog.redstone.finance/2026/05/05/what-is-oracle-extractable-value-oev/).
Détenus : Sevim & Torres 2026, Chainlink whitepaper v1 2017, DECO — voir
`biblio/INDEX.md`.
