# Contre-contrôle et relecture G2 neuve — LINT-HAIKU, vague 3 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 17:39:28 UTC du rapport rendu par l'agent a72b3bd4bae9db292 (workflow wf_ae64f812-f4d) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0 : `claude-opus-5-5`.** C'est l'identifiant exact donné par le contexte système de la session, avec le préfixe attendu ; l'effort `max` ne se voit pas de l'intérieur. Je suis réviseur neuf : je n'ai écrit aucun des diffs relus ni aucune relecture précédente de ce lot.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-3), C-1 bloquante

- Horloge (`date -u`) : de 2026-10-08T16:03:00Z à 17:37:33Z. `<R>` = `<scratchpad>/lot-haiku/corr3/revue`, seul dossier où j'ai écrit.
- Base e6657dc, extraite par `git archive` avec les 7 exclusions : c1f09c21…, 991 entrées (871 fichiers et 120 dossiers).
- SHA256SUMS du correcteur : 190 lignes, `-c` OK, empreinte dc2c5131… ; LH-1 fdedb729…, LH-2 e76eac74….
- `patch -p1` puis `git apply` en série donnent des arbres identiques : lint ffb790b0…, runner 76a1d7a4…, fiche 1974e9f9….

Sont acquis : C-1 à C-3 de la revue de la vague 2, le refus de Haiku dans les réglages JSON (sauf C-2), le contrôle du commentaire, l'indépendance de la locale, la forme, l'absence de cas retiré ou affaibli et l'absence de desserrement par rapport à la base. **C-1 bloque** : le lint affirme refuser Haiku dans un flux ouvert sur plusieurs lignes, et des formes ordinaires passent.

| C | fichier:ligne (copie finale) | preuve | remède |
|---|---|---|---|
| **C-1** | lint l.27-31 (ce que l'en-tête affirme), l.64-68 (QS, FB, FLS), l.150-152 (calcul de FL) ; runner l.218-219 et l.254 (T-152) | Le calcul de FL est faux de trois façons (détail sous le tableau). | **R1** (`<R>/proposition/R1/C1-C3.diff`) : FL passe à 1 dès qu'une ligne précédente du frontmatter porte `[` ou `{`, et n'est jamais remis à 0 dans le fichier. QS, FB et FLS sont retirés, l'en-tête est corrigé. T-152 est inversé (à adjuger) ; T-156, T-157, T-160 et T-161 sont ajoutés. |
| **C-2** | lint l.49-51 (SIGX) ; l.29 (« casse ignorée, échappement u00XX lu ») | `{"env": {"ANTHROPIC_MODEL": "CL<u0041>UDE-H<u0041>IKU-5-5"}}` est admis (sortie 0). La forme en clair `CLAUDE-HAIKU-5-5` et l'échappement minuscule `<u0061>` sont, eux, refusés (R-1/role) : `grep -i` ne replie pas le code d'un échappement. J30 n'est refusé que par hors-liste. | SIGX lit aussi l'échappement de la majuscule (`u00` suivi du code de la minuscule ou de la majuscule) ; cas T-158. Le mutant PV-05 n'est tué que par T-158. |
| **C-3** | runner l.222-238 (aucun cas à deux dièses) ; lint l.140 | Le mutant V-20 lit le commentaire depuis le dernier dièse. Il survit au runner final (212 ok, sous P et U) et admet `model: claude-opus-5-5 # x<FF> # y`, que la base refusait sous C.UTF-8 (2 hors-liste) : desserrement que rien n'épingle. | T-159 : `ml "model: claude-opus-5-5 # x$FF # y"; casl T-159 2 R-1/hors-liste`. Il tue V-20 sous les 4 locales. |

**C-1 : les trois défauts de FL**
- **Tirets, le plus grave.** La projection FLS garde les `-` et `+` du texte : chaque tiret d'un scalaire compte comme un fermant. Exemple, un hook réel (F55) : `hooks: {Stop: [{hooks: [{type: prompt, prompt: re-run-the-full-check-suite,` suivi de `model: claude-haiku-5-5` en colonne 0. La projection donne `+++++-----`, donc FL = 0 et le lint sort 0. PyYAML lit pourtant ce `model` dans le hook, sans `model` de premier niveau.
- **Apostrophes et guillemets de scalaires** (`it's`, `y's`, `a"b`) : QS les apparie à tort et masque un ouvrant (F20a, F20b, F20d, H2).
- **Chaînes entre guillemets sur plusieurs lignes** : leurs lignes de suite apportent de faux fermants (F20c, H1, F51/T-161).
- **Portée.** Ces 8 formes de skill sont admises sous les 19 environnements ; la base les refuse toutes. F20e (agent) n'est refusée que par K = 2. Sur un fuzz de 4 000 formes, le final admet 102 des 1 101 formes que PyYAML lit imbriquées.
- **Nuance mesurée.** J'ai émulé le lecteur de Claude Code 2.1.42 sous Bun (Bun.YAML.parse 1.3.14, puis son repli `_M5`). Il ne charge aucune de ces formes : 101 frontmatters vides et 1 premier niveau sur les 102. Mais la référence écrite du lint (PyYAML, l.31) est contournée, et le comptage des tirets est un défaut de code en soi.

**Preuve du remède R1**
- Runner : 221 cas, verts sous les 19 environnements ; 6 rouges contre le final (T-152, T-156, T-157, T-158, T-160, T-161).
- Mutants : 32 tués, 64 runs sur 64 ; témoin vivant.
- Formes hostiles : 119 sur 119 ; fuzz : 0 violation sur 1 101 formes imbriquées.
- Arbre OK (7 fichiers) ; E-LH-3 : 95 ok ; verify identique à la base.
- Prix : Haiku de premier niveau est refusé après toute ligne qui porte `[` ou `{`.

**Variante R7b** (`<R>/proposition/R7b/`, lint seul ; il manque son runner) : fuzz à 0 violation, 1 730 admissions de premier niveau sur 2 899 (R1 : 456), formes hostiles 119 sur 119, runners de R1 et de R7 verts. Sa campagne de mutants n'a pas été lancée.

## 1. Contre-contrôle de la revue de la vague 2 (point a)

Portages et classement faits par moi, sur le runner final.

| mutant | portage | P | U | cas qui le tuent |
|---|---|---|---|---|
| M-01 | `export LC_CTYPE=C` | tué | tué | T-113 à T-117/LC_ALL, T-127/LC_ALL |
| M-02 | `export LANG=C` | tué | tué | variantes /LC_ALL et /LC_CTYPE |
| M-10 | caractères de contrôle refusés | tué | tué | T-131 |
| M-11 | `#(.?)` | tué | tué | T-126, T-130 et autres |
| M-14 | un blanc au plus | tué | tué | T-128 (×4) |
| M-15 | sans `*.cjs` | tué | tué | T-129 |
| M-16 | espace seul avant `#` | tué | tué | T-126 (×4) |

Les trois corrections sont soldées : `casl` couvre LC_ALL et LC_CTYPE (runner l.192-193) ; T-126, T-127, T-130 et T-131 bornent le contrôle du commentaire ; T-128 et T-129 sont présents.

## 2. Relecture G2 neuve (point b)

**Formes hostiles.** 119 formes à attendu écrit à la main, lancées sous 19 environnements : sans locale, POSIX, C.UTF-8 par LANG, LC_ALL et LC_CTYPE, tr_TR, GB18030, EUC-JP, BIG5, BIG5-HKSCS, ISO-8859-1, EUC-KR, LC_ALL invalide, LOCPATH absent, mélanges, LC_COLLATE, LC_MESSAGES. Final : 109 conformes, 10 non conformes (J30 et les formes de C-1), **0 instable**.

| domaine | résultat |
|---|---|
| JSON : J01-J32 (compact, multiligne, CRLF, hooks imbriqués, clé répétée, env, clé, échappements, BOM, permission…) | R-1/role partout sauf J30 (C-2) |
| frontmatter, premier niveau (agent, skill, commande, guillemets, commentaire valide, BOM, CRLF, TAB, NBSP) | admis |
| frontmatter imbriqué (hook, séquence, flux) | R-1/role, sauf les formes de C-1 |
| commentaire (I-R-4) | valides admis (décision, CJK, émoji, U+10FFFF, DEL, SOH, U+FEFF, U+FFFE, bornes) ; invalides refusés |
| BU dans un commentaire | R-1/cle-model, par Q-1 |

**Autres mesures**
- U8 contre le décodeur strict de Python : 154 887 formes, 0 désaccord.
- Différentiel généré : 6 278 formes, 0 instable, 0 desserrement. 1 431 admissions de plus, toutes en Haiku avec une jumelle opus admise par la base ; 352 serrages, tous des prix écrits (BU et UTF-8 invalide).
- Mes mutants neufs sur le lint final : 23 tués sur 25. V-20 vit (d'où C-3). V-23 vit aussi, mais il est plus strict et n'a plus d'objet avec R1.

**Contrôles de livraison**
- Forme de LH-1 : 111 lignes de code ajoutées (au plus 200), 119 caractères au plus, 0 TODO ni littéral banni ; octets 92 : lint 43 → 98, runner 48 → 142.
- Runner final : 212 ok sous les 19 environnements. Rouges : 26 contre la vague 2, 59 contre la base.
- Cas de la base : les 95 sont identiques, le diff du runner est +101 −0 ; E-LH-3 : 95 ok.
- Arbre : `OK (R-1) : 7 fichier(s)`.
- Hooks : 54 ok. s2-harness : Ran 407, OK (skipped=2), `--egal` conforme.
- Gate des secrets `--tree` : OK sur 863 fichiers, sur une copie git jetable.
- verify (final, R1 et base identiques) : S-G1 à S-G8 VERT, S-G9 ROUGE, fmt, no_std et clippy VERT, verdict global ROUGE ; sections S-G9 identiques par empreinte.

## 3. Confrontation avec le rapport du correcteur

Ses chiffres concordent avec mes recomptes, et je confirme son E-4 et son L-1. Trois points le démentent : son « G0 §7 tenu » (C-1), son « casse ignorée, échappement lu » (C-2), et V-20 (C-3). Son différentiel ne croisait ni tiret dans un flux, ni chaîne sur plusieurs lignes, ni apostrophe ; et son excuse par la jumelle opus masque l'imbrication.

## Écarts du réviseur

- **R3-1** : ma 1re campagne (setsid nohup) est invalide : PID mal relevé, sorties effacées pendant qu'elle tournait. Non comptée, relancée.
- **R3-2** : mon premier portage de M-10 était faux ; refait.
- **R3-3** : 1er différentiel arrêté par moi (trop lent) ; non compté, relancé réduit.
- **R3-4** : mes attendus de F23 et F23b étaient faux ; corrigés.
- **R3-5** : mon premier remède R7 avait le défaut des tirets ; retiré, remplacé par R7b.
- **R3-6** : des heures de mes notes écrites avant de lire l'horloge ; corrigées.
- **R3-7** : des barres obliques inverses tapées, et un échappement unicode du rapport changé par le harnais (rendu « A »). Rapport réparé par script, 0 octet 92 ; mes scripts de mesure n'en ont aucun.
- **R3-8** : localedef et `git init` jetable, uniquement sous `<R>/tmp`.
- **R3-9** : le dépôt réel a avancé pendant ma passe ; HEAD vaut maintenant b46672b0, 13 commits après e6657dc. Rien n'a bougé sous `enforcement/`, `.claude/`, `.github/` ni `CLAUDE.md`. Aucune écriture git, aucun `.claude/` créé, ni D.2, ni `*.jsonl`, ni Pocket.
- **R3-10** : verify n'a tourné que sur les copies avec exclusions.

## Items à former

- **I-R3-1** : quel lecteur fait référence pour le lint, PyYAML ou celui de Claude Code ? Le chemin Bun est mesuré par émulation ; le chemin node (`yaml` d'eemeli) ne l'est pas [abs].
- **I-R3-2** : campagne de mutants de R7b, si elle est retenue.
- **I-R3-3** : prix de R1, par exemple une commande en Haiku dont `argument-hint: [x]` précède `model:` est refusée.
- **I-R3-4** : un BU dans un commentaire valide est refusé (par Q-1).
- Toujours ouverts : L-1, I-R-2, I-2, I-c, I-d, I-R-3, I-e, I-f, I-3, I-4, I-5.

**Avis sur les questions du correcteur**
- Q-1 : garder E-4.
- Q-2 : ni l'un ni l'autre tel quel ; adopter R1, ou R7b après sa campagne.
- Q-3 : garder.
- Q-4 : oui.

## Fichiers produits

Sous `<scratchpad>/lot-haiku/corr3/revue/` :
- `RAPPORT-REVUE.md` (sha256 5a307e0a0ca7fdd6b68aa66c3b043e986ddb45750dc9a176458bfb8ea7dad4b0) — ce rendu, plus le journal de provenance
- `NOTES.md` (bbf82bc1b471e49013aa872433226024e42a45142e55f27b060d25e29c8e6570)
- `proposition/R1/C1-C3.diff` (69941b92…), avec ses fichiers : lint 9c2cea92…, runner 8cf9619f…
- `proposition/R7b/` : lint 2510ca5b…, diff 71b20b3d…
- `scripts/`, `mutants/`, `mutants-prop/`, `mutants-prop2/`, `logs/`, `tmp/` (archive de base et copies)
- `SHA256SUMS` : 725 lignes, `sha256sum -c` OK, empreinte 0202f30d25d1e14b624ffd0d1bc9008538d753f0906bef9152cb5b10545dc9ce. Il couvre tout sauf lui-même et les copies de `tmp/` ; l'archive de base y est.
