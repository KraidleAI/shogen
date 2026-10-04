# Shōgen — kit logo (direction 3B « Amont commun »)

Choix validé. Accroche : **Comptez vos sources. Vraiment.** (EN : *Count your sources. For real.*)

Symbole : trois sources indépendantes convergeant vers un agrégateur unique (corail).

## Contenu
- `Shogen Brand Guidelines.dc.html` — spec complète (ouvrir dans un navigateur)
- `logo/symbol.svg`, `symbol-dark.svg` — symbole statique, fond clair / sombre
- `logo/symbol-animated.svg`, `symbol-animated-dark.svg` — boucle 2.6s, respecte prefers-reduced-motion
- `logo/lockup.svg`, `lockup-dark.svg` — symbole + logotype + accroche (texte en Sora : charger la police ou vectoriser)
- `logo/favicon.svg` — plaque #0E3B34, rayon 22 %
- `tokens.css` — variables couleur / typo

## Règles clés
1. Viewbox 0 0 64 64. Sources (14,16) (32,10) (50,16) r=6 ; récepteur (32,50) r=8 ; traits 3px arrondis.
2. Le corail #FF6B4A n'apparaît que sur le nœud récepteur — jamais en accent UI.
3. Animation : hero / loader / splash seulement. Statique partout ailleurs (nav, listes, favicon).
4. Taille min : 20px symbole, 24px lockup. Zone de protection = 6px (à l'échelle 64).
5. Typo : Sora 700 (logotype, -0.03em), Sora 400/500 (UI), IBM Plex Mono (data/code).
6. Ne pas recolorer, tourner, refléter ; pas sur photo sans plaque pleine.

## Animation
| Élément | Effet | Délai |
|---|---|---|
| Trait gauche | stroke-dashoffset 38→0 | 0s |
| Trait central | idem | 0.15s |
| Trait droit | idem | 0.3s |
| Récepteur | scale 1→1.35→1 | 0.9s |

Fonts : https://fonts.google.com/specimen/Sora

## Provenance (versement de l'orchestrateur, 2026-10-04 02:59:27 UTC)

Remis par l'investisseur le 2026-10-04 (« voici la charte graphique de SHOGEN »), archive `CHARTE_SHOGEN.zip` (sha256 `f515f2284bb65819768905a69a6b489a8001328eb02b467fe09791f0f701e75c`), export Claude Design ; versé ici le seul kit retenu (`project/shogen-brand/`, direction 3B « Amont commun »), à l'octet sauf ce paragraphe ; les explorations (`Logos Shogen.dc.html`) et les doublons ne sont pas versés. `support.js` est le runtime généré qui affiche `Shogen Brand Guidelines.dc.html` ; il n'est pas du code produit. Empreintes : `SHA256SUMS` (calculées avant l'ajout de ce paragraphe pour `README.md`).
