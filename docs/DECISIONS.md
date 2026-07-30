# Shōgen — registre des décisions (ADRs)

| ADR | titre | statut | date |
|---|---|---|---|
| ADR-0001 | Les transports d'attestation sont des adapters — Shōgen n'en construit aucun | acceptée | 2026-07-30 |

---

## ADR-0001 — Les transports d'attestation sont des adapters — Shōgen n'en construit aucun

**Statut** : acceptée · 2026-07-30

### Contexte

Le champ zkTLS (« web proofs ») est passé des papiers aux SDKs : TLSNotary
(MPC, open source), Reclaim (proxy-witness, production), zkPass (hybride),
Opacity (réseau MPC), vlayer — recensés par l'index « zkTLS Canon » de
Reclaim et confirmés par la présence d'un « zkTLS Day » à Devconnect
(recherche du 2026-07-30, `docs/01-precedents.md`). La racine académique est
DECO (Zhang, Maram, Malvai, Goldfeder, Juels, CCS '20, détenue :
`biblio/deco-2019.pdf`) : prouver « that a piece of data accessed via TLS
came from a particular website », sans matériel de confiance ni coopération
du serveur. Les attestations TEE (lignée Marlin/Phala/Automata) couvrent le
cas calcul. La question : Shōgen doit-il construire son propre transport
attesté ?

### Décision

Non, jamais. Les transports — zkTLS proxy, zkTLS MPC, attestation TEE,
signature native de la source quand elle existe — sont des **adapters
interchangeables sous Shōgen**, au sens architectural que Kraidle donne à ce
mot : ils apportent les témoignages bruts, sont testés et jamais prouvés, et
la couche Shōgen (typage des faits, fraîcheur, quorum, mesure de diversité,
vérification du lot) ne dépend d'aucun d'eux en particulier. Le vocabulaire
de faits de Shōgen ne nomme aucun transport (l'analogue de R2 Kraidle).

### Alternative considérée

Construire un transport propriétaire (un notaire Shōgen). Rejetée : (a) le
champ est industrialisé et concurrentiel — y entrer coûterait l'essentiel de
l'effort pour un composant non différenciant ; (b) chaque transport porte un
modèle de menace distinct (la FAQ TLSNotary détenue : la preuve vaut envers
un vérificateur désigné et exige « trust in the notary's neutrality » si le
vérificateur n'a pas conduit le MPC lui-même) — en épouser un seul
importerait ses limites dans toute la pile ; (c) la valeur du projet est
au-dessus : c'est le gap §3 de `01-precedents.md`.

### La source qui tranche

TLSNotary, FAQ (détenue, grep vérifié) : le projet lui-même écrit qu'il
« does not solve the "Oracle Problem" ». Le transport le plus mûr du champ
déclare que la couche que Shōgen vise n'est pas son objet. DECO (abstract)
revendique la provenance, pas la vérité. La couche au-dessus est vacante.

### Ce que la décision coûte

- Une **hypothèse par transport**, au rang d'assumption nommée :
  A(transport-tlsnotary), A(transport-tee), etc. — chacune avec le résidu
  propre du mécanisme (neutralité du notaire, intégrité de l'enclave,
  honnêteté du proxy). Shōgen hérite de ces résidus et doit les publier par
  transport, jamais fusionnés — la règle des trois latences de Kraidle,
  transposée.
- La qualité des témoignages bruts est bornée par l'écosystème externe
  (couverture TLS 1.2/1.3, sources supportées).
- Un travail d'interface : la forme canonique de témoignage que tous les
  adapters produisent — c'est le premier objet technique à spécifier.

### Registres touchés

Crée le besoin des registres : assumptions par transport (à ouvrir avec la
vision), forme canonique de témoignage (spec à venir).
