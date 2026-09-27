# 16 — Plan du test PRIVÉ des deux points sensibles de l'étude Pocket (doc 15 §5, lignes protocole §4.3 / P-11 et §4.5 / P-10)

- **Statut** : **G0 proposé — plan, rien exécuté.** Rédigé par l'orchestrateur MONARK `claude-fable-5-1` (session « POKT X SHOGEN », 2026-09-27 01:3x-01:5x UTC). Chemin AgileGates : ce G0 → **consultation formée C-1 (canal 2, agent `advisor`)** sur le raisonnement AVANT tout test (option (b) de l'archive protocole §10, retenue) → **checkpoint-1** (validateur-humain) → **go investisseur** (installation d'un outillage Go + lancement du worker) → G1/G2/oracle/G7 → **décision de divulgation = acte investisseur sous go**.
- **STATUT — SENSIBLE, USAGE INTERNE** (07-gtm §6 pt 3 : préavis privé avant toute mention ; doc 15 §0). Aucune ligne de ce plan, ni de ses résultats, ne sort du dépôt privé Shōgen avant la décision de divulgation. Le pointeur CHANTIERS (dépôt MONARK public) ne nomme que « test privé du point sensible, plan écrit ».
- **Décision 244** : aucun avis juridique n'est donné ici ; les points juridiques sont des questions formées pour le juriste (G-6).

## 1. Objets du test (deux hypothèses distinctes, deux tests distincts)

| id | hypothèse (doc 15 §5) | niveau actuel | ce que le test doit rendre |
|---|---|---|---|
| **T-A** (P-11, protocole §4.3) | la validation on-chain d'une preuve ne lie pas la **position** de la feuille prouvée au **hash de la relation** qu'elle porte (`VerifyClosestProof` prend `ClosestPath` tel que fourni ; seul usage du hash = difficulté) ⇒ un supplier détenant UNE relation valide pourrait remplir son arbre de copies/variantes à des chemins arbitraires ; la preuve établirait l'**existence**, pas le **compte** | [lu] confirmé par le réfutant (W1 P-11 : « confirmed » vaut pour l'ÉNONCÉ conditionnel, « ne confirme PAS l'exploitabilité : aucun test n'a été exécuté ») | **CONFIRMÉ** / **RÉFUTÉ** / **INDÉTERMINÉ**, par un test de keeper reproductible, au commit déployé `a109dd0` |
| **T-B** (P-10, protocole §4.5) | ≈ 764 sélections probabilistes observables sur ≈ 1 465 attendues à p = 0,001 (ratio 0,52, corrigé P-10) ; étiquette `PROBABILISTIC` absente du règlement ; **cause non établie** (piste : graine `binary.Varint` de `SeededFloat64`, `pkg/crypto/rand/float.go` L16-L25) | [mesure] sur l'indexeur PNF (témoin unique) | une **cause établie ou exclue** pour la piste graine (calcul déterministe rejouable) ; recoupement du 764 par une seconde source (`block_results`) si les conditions le permettent |

Les deux ne sont pas de même nature : T-A est une question de **sûreté du protocole** (divulgation responsable si confirmé) ; T-B est une question de **fidélité d'un paramètre** (p effectif ≠ p déclaré) — publiable comme mesure après recoupement, sans préavis de sécurité, mais sous la règle « corrigé + identifiant du réfutant » (Q-ORCH-1).

## 2. Protocole T-A (test local, jamais un réseau réel)

1. **Isolation** : bac à sable sur F: (`F:\tmp\pocket-test\`), **aucun réseau** pendant le test hors la récupération initiale du code source ; **jamais** MainNet, **jamais** Beta/Alpha TestNet, aucun claim réel, aucune clé de compte, aucun POKT. Le worker n'a pas accès aux variables d'environnement de la machine (lancement `env -i` avec `PATH`, `GOPATH`, `GOCACHE`, `GOMODCACHE` sur F:, `GOFLAGS=-mod=mod`, `GOPROXY` autorisé pour le seul téléchargement des modules puis `GOPROXY=off`).
2. **Source épinglée** : tarball `codeload.github.com/pokt-network/poktroll/tar.gz/a109dd0bae65c1d96b010d65f4cdc5bc77a50fc2` (commit déployé, protocole §1ter) ; sha256 du tarball consigné ; `smt` v0.14.1 tel que résolu par `go.mod` (sha du `proofs.go` attendu `be819710…`, P-11) ; `go.sum` fait foi (ADR-0012 : le lockfile fait foi).
3. **Outillage** : toolchain Go **exactement** celle de `go.mod` du commit (à lire ; installation depuis `go.dev/dl` avec sha256 publié vérifié — **R-8 : vérification registre préalable, décision orchestrateur, consignée**) ; installée sous `F:\tools\go\<version>\`, rien sur C:.
4. **Test écrit, pas une exploration** : un test Go dans `x/proof/keeper/` (copie de travail, jamais poussée nulle part) qui, en réutilisant le harnais de test existant du dépôt (`proof_validation_test.go` / `keeper_test.go`, à identifier au G1) :
   - (a) construit une session de test et UNE relation valide (requête signée en anneau par l'app de test, réponse signée par l'opérateur de test), sous la cible de difficulté ;
   - (b) construit un SMST où cette relation est insérée à **N chemins arbitraires** (N = 2, 16, 1 024) au lieu de son chemin canonique H(relation) ; variante (b') : N réponses différentes à la même requête, chacune signée (hash distinct) ;
   - (c) crée le claim (racine, compte de feuilles N) et soumet la preuve « closest » pour un chemin cible tiré par le keeper ;
   - (d) **oracle** : `EnsureValidProof` (ou l'équivalent au commit) rend **nil** ⇒ T-A **CONFIRMÉ** (la validation accepte une feuille dont la position ≠ H(relation), et le compte N est réclamé) ; rend une erreur nommant le chemin/hash ⇒ **RÉFUTÉ** (citer la ligne du contrôle) ; erreur d'une autre nature (montage de test) ⇒ **INDÉTERMINÉ**, jamais reclassé.
   - (e) **contrôle positif** obligatoire : la même relation à son chemin canonique passe (sinon le montage est faux) ; **contrôle négatif** : une signature invalide échoue.
5. **Ce que le test ne fait pas** : il ne mesure pas le gain (borné par le budget d'app, protocole §4.2), n'exécute rien contre un validateur, ne produit aucun outil réutilisable ; le code de test est **gardé dans le dépôt privé Shōgen sous `scratch/pocket-test/`**, jamais publié.
6. **Sorties** : rapport de mission (verdict + ligne de code de chaque contrôle + sha des fichiers lus + sortie brute `go test -run … -v`), et rien d'autre.

## 3. Protocole T-B (calcul déterministe + recoupement)

1. **Piste graine** : réimplémenter à l'identique `SeededFloat64` (Go, même dépôt, même fonction appelée directement dans un test) et l'appliquer à un échantillon de claims **réels** (≥ 1 000, tirés de la fenêtre 7 j de P-10) : la graine est fonction de `MsgCreateClaim` (octets) et du hash de bloc à la hauteur de règlement — les deux sont lisibles sur l'indexeur PNF (`data.pocket.network/graphql`, conditions lues le 21/09 ; usage « échantillon borné », à relire pour le volume) et la LCD (bloc). Oracle : proportion de `SeededFloat64 < 0,001` sur l'échantillon, IC binomial exact ; comparer à 0,52 × 0,001. Si la proportion reproduit ≈ 0,5 ‰ ⇒ cause **établie** (graine à entropie réduite) ; si ≈ 1 ‰ ⇒ piste **exclue**, cause reste non établie.
2. **Recoupement du 764** par `block_results` d'un bloc de règlement sur un RPC Tendermint : conditions d'usage de `sauron-rpc.infra.pocket.network` **non lues** ⇒ **procurement formé** (lecture sur place par l'orchestrateur avant tout appel) ; sinon, un nœud complet propre (hors budget de ce plan).
3. **Sorties** : rapport (proportion, IC, N, hauteurs, sha des réponses brutes), chiffre citable seulement sous la forme « corrigé P-10 (≈ 764) ; piste graine : établie/exclue (T-B) ».

## 4. Rôles, modèles, coût

| poste | qui | coût / durée estimés (jamais des faits) |
|---|---|---|
| Relecture adversariale du raisonnement T-A avant test (C-1) | agent `advisor` (Fable 5.1, canal 2, demande formée §7) | 1 consultation |
| Implémentation T-A + T-B | **un** worker `claude-opus-5-5`, effort **high** (décision 238), contexte frais, mission écrite, sans écriture hors `F:\tmp\pocket-test\` et `scratch/` | 2-4 h (installation Go comprise) ; garde-fou de réduction : mono-agent + oracle déterministe, pas de fan-out |
| Relecture G2 | relecteur `claude-opus-5-5` séparé, contexte frais : rejoue le test, vérifie les contrôles positif/négatif, les sha | 1 h |
| Oracle | le test lui-même (`go test`, exit code) + rejeu G2 | — |
| G7 + checkpoint-2 | orchestrateur ; validateur-humain rejoue le `go test` (Bash de vérification seule, AM-2) | — |
| Réseau / argent | téléchargements source + modules Go (une fois) ; ≤ 2 000 requêtes lecture seule à l'indexeur pour T-B ; **0 POKT, 0 compte, 0 clé** | 0 € hors temps de calcul |
| Disque | tout sur F: (`F:\tools\go`, `F:\tmp\pocket-test`, caches Go) ; rien sur C: (règle investisseur 27/09) | ~2 Go |

## 5. Arbre de décision après le test (chaque branche = acte investisseur sous go)

- **T-A CONFIRMÉ** → (i) doc 15 §5 ligne 1 passe à [testé, local] ; (ii) **divulgation privée** aux mainteneurs : le dépôt poktroll **n'a pas de `SECURITY.md`** et GitHub y affiche « No security policy detected » avec le bouton « Report a vulnerability » (signalement privé GitHub) — lu sur place le 2026-09-27 01:2x UTC, `https://github.com/pokt-network/poktroll/security` ; canal alternatif `directors@pokt.foundation` (doc 15 §10) ; contenu = reproduction minimale (test), pas d'outil ; **délai de préavis** à fixer par l'investisseur (pratique courante 90 j, à sourcer si retenue) ; (iii) **aucune mention publique**, même anonymisée, avant l'issue du préavis ; (iv) question juriste G-6 : un signalement privé est-il un « Feedback » sous licence irrévocable (ToS §8, P-5) ? — question formée, pas d'avis ici.
- **T-A RÉFUTÉ** → erratum daté au doc 15 §5 (ligne retirée, contrôle cité), à l'archive protocole §4.3 (note), au W1 P-11 (le verdict « confirmed » portait sur l'énoncé conditionnel : inchangé, la condition est levée négativement) ; `error_origin` = lecture (contrôle hors des fichiers lus).
- **T-A INDÉTERMINÉ** → seconde tentative **sur avis advisor uniquement** (R-26 : jamais deux fois la même approche sans consultation) ; sinon procurement formé auprès des mainteneurs (question technique publique **sans** l'hypothèse : « où le chemin de feuille est-il lié au hash de relation ? » — à valider par l'investisseur, car même la question peut orienter).
- **T-B cause établie** → mesure citable (forme corrigée + T-B) ; information privée à la PNF **optionnelle** (paramètre, pas une faille) ; **T-B exclue** → « cause non établie » demeure, procurement `block_results`.

## 6. Ce que ce plan n'autorise pas

Aucun test contre un réseau (Main/Beta/Alpha), aucune création de compte, aucun stake, aucun envoi à quiconque, aucune installation d'outillage avant le go, aucun tweet/brouillon/diagramme portant l'hypothèse. Ni Shōgen ni MONARK ne tirent de revenu d'un mesuré (D11, ADR-0027) : un éventuel « bug bounty » Pocket, s'il existait, **ne serait pas réclamé** tant qu'une mesure de Pocket est publiée (question formée à l'investisseur, à trancher avant la divulgation, pas après).

## 7. Demande de consultation formée C-1 (canal 2, à router par l'orchestrateur AVANT le checkpoint-1)

- **Problème (une phrase)** : la lecture de `x/proof/keeper/proof_validation.go` (a109dd0) et `smt/proofs.go` (v0.14.1) conclut qu'aucun contrôle ne lie `ClosestPath` à H(relation) ; avant un test local, y a-t-il un contrôle que la lecture aurait manqué (ante-handler, `x/proof` `msg_server`, `smt` `VerifySumProof` via `spec.ph.Path(key)`, unicité imposée par la racine SMST ou par le compte de feuilles), et le protocole de test §2 pt 4 discrimine-t-il réellement CONFIRMÉ/RÉFUTÉ ?
- **Tentatives** : grep `ClosestPath|GetRelayHashFromBytes|PathHasher` dans `x/` (aucune comparaison) ; balayage de 1 237 fichiers (P-11 : `ClosestPath` lu nulle part hors un outil hors chaîne) ; audit smt (périmètre bibliothèque, hypothèse de constructeur honnête).
- **Options** : (a) tester tel quel ; (b) ajouter au test un cas « `nilPathHasher` : la clé EST le chemin » pour vérifier que `VerifySumProof` ne recalcule pas le chemin depuis la valeur ; (c) ne pas tester, demander aux mainteneurs (déconseillé : faux positif possible, et la question oriente).
- **Artefacts joints** : ce plan ; archive protocole §4.1-§4.3 ; W1 P-11 (note du réfutant). **Jamais le transcript.**

## 8. Provenance

Archive protocole §4.3, §4.5, §10 C-1/C-2, §11 pt 1-2 (sha `27608e75…`) ; W1 P-10/P-11 (`refutations/RESULTATS.json`, sha `51ae25e4…`, lus par script le 27/09 01:2x UTC) ; doc 15 §5, §10, §11 ; page GitHub Security de poktroll lue sur place (navigateur interne, 01:2x UTC) ; décisions 230, 238, 244 ; règle disque « rien sur C: » (investisseur, 27/09 01:3x UTC). Advisor intégré indisponible dans la session de rédaction — consigné, non contourné ; la consultation passe par le canal 2 (§7).
