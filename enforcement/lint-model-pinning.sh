#!/usr/bin/env bash
# Shōgen, gate G1 (R-1) : lint d'épinglage des modèles, en liste blanche exacte.
# Rattachement : ADR-0028 D8 et C-14, décision CB-10 du cp-1 bis, lot D8a (G0 :
# docs/adr-0028/G0-lot-D8a.md ; journal docs/G1-lot-D8a.md, qui nomme les écarts au
# blob source). Porté du blob 457565f (adb2213:enforcement/lint-model-pinning.sh),
# identique à celui du commit 0b4f3f9 de l'amont VibeGates.
# Liste blanche : roster des décisions 133, 267 et 280 (CLAUDE.md l.20-31). Elle vit
# ici, sur une ligne ; la changer demande un lot. L'identifiant banni le 2026-08-14
# (docs/DECISIONS.md l.2965-2968) est construit à l'exécution : ce dossier n'en porte
# jamais le littéral.
# Portée : frontmatter (premier bloc ---) des *.md situés sous un .claude/agents/, un
# .claude/skills/ ou un .claude/commands/ de l'arbre, à toute profondeur, corps non lu ;
# clés model et advisorModel de .claude/settings.json et de .claude/settings.local.json ;
# scripts de workflow (*.js, *.mjs, *.cjs) qui appellent agent(, refusés tant qu'aucun
# lint ne les lit. Élagués : target, .git, node_modules, mutants.out*, et, à la racine,
# .claude/worktrees et biblio.
# Tout ce qui n'est pas exactement dans la liste est refusé : tier nu, identifiant banni
# ou retiré, casse ou suffixe différents, clé model d'agent absente ou répétée, forme
# YAML hors du sous-ensemble lu (clé non nue, valeur sur plusieurs lignes, frontmatter
# indenté ou non fermé), clé JSON échappée, aucun agent lu.
# Limite : ce lint lit le texte versionné, pas le modèle qui tourne (paramètre
# d'invocation, environnement, réglages hors dépôt, substitution par la plateforme) ;
# le contrôle R-1 au lancement reste dû. Une clé model imbriquée écrite hors d'une ligne
# model (entrée de séquence, flux, suite de valeur) n'est pas lue : item SHOGEN-LINT-IMBRIQUE-1.
# Usage : lint-model-pinning.sh [racine]   Sortie : 0 aucun refus, 2 refus (stderr).

set -u
ROOT="${1:-.}"
[ "$ROOT" = / ] || ROOT="${ROOT%/}"
ALLOWED='claude-opus-5-5 claude-sonnet-5-5 claude-fable-5-1'
BANNED="claude-opus-""5"
RETIRED='claude-sonnet-5'
TIERS='opus|sonnet|haiku|fable|inherit|default|opusplan'
# Début de ligne de premier niveau qui forme une clé non nue, lue model par PyYAML 6.0.3
# (mesuré) : guillemets, ?, ancre &, étiquette !, alias *, flux {, clé de fusion <<. Le
# tiret et | > en colonne 0 restent des formes valides (séquence non indentée, bloc).
NON_NUE="^([\"'?&!*{]|<<)"
ELAG=( \( -name target -o -name .git -o -name node_modules -o -name 'mutants.out*' -o -path "$ROOT/.claude/worktrees" -o -path "$ROOT/biblio" \) -prune -o )
FAIL=0
N=0
NA=0

refus() { # jeton, lieu, valeur, motif
  FAIL=1
  printf 'REFUS (%s) %s : %s — %s\n' "$1" "$2" "$3" "$4" >&2
}
dans_liste() { # égalité exacte, octet pour octet
  for a in $ALLOWED; do [ "$1" = "$a" ] && return 0; done
  return 1
}
norm() { # commentaire précédé d'un blanc, blancs finaux, une paire de guillemets appariée
  v="$(printf '%s' "$1" | sed -E -e 's/[ \t]+#.*$//' -e 's/[ \t]+$//')"
  case "$v" in
    \"*\") v="${v#\"}"; v="${v%\"}" ;;
    \'*\') v="${v#\'}"; v="${v%\'}" ;;
  esac
  printf '%s' "$v"
}
verdict() { # lieu, valeur normalisée ; base = minuscules, sans suffixe final [...]
  dans_liste "$2" && return 0
  b="$(printf '%s' "$2" | tr '[:upper:]' '[:lower:]' | sed -E 's/\[[^]]*\]$//')"
  if [ "$b" = "$BANNED" ]; then
    refus 'R-1/ban' "$1" "$2" "identifiant banni (2026-08-14) : aucune dérogation hors mainteneur"
  elif printf '%s\n' "$2" | grep -qixE "$TIERS"; then
    refus 'R-1/tier-nu' "$1" "$2" "tier nu : la plateforme choisit le modèle à l'appel"
  elif [ "$b" = "$RETIRED" ]; then
    refus 'R-1/retire' "$1" "$2" "retiré (décision 280), non banni : le réadmettre demande une décision de roster et un lot"
  elif [ "${2%%\[*}" != "$2" ] && dans_liste "${2%%\[*}"; then
    refus 'R-1/suffixe' "$1" "$2" "suffixe entre crochets : forme résolue, jamais une valeur épinglée"
  else
    refus 'R-1/hors-liste' "$1" "$2" "hors liste blanche ($ALLOWED)"
  fi
}

# 1) Frontmatter des agents, des skills et des commandes, sous tout .claude/ de l'arbre :
#    la découverte lit chaque .claude/agents/ entre le répertoire courant et la racine,
#    sous-dossiers compris (G0 §5.4 a ; journal G1 §15). Lu en bash, octet pour octet : les
#    sed et awk de Git Bash retirent le CR des fins CRLF (mesuré), ce qui masquerait en
#    local la règle du CR. BOM de la ligne 1 et CR final retirés ici ; numéros de ligne
#    conservés. Hors du sous-ensemble ligne à ligne lu ici, une forme YAML est refusée.
while IFS= read -r f; do
  [ -f "$f" ] || continue
  N=$((N + 1)); n=0; K=0; FM=0; SUITE=0; DEB=0
  while IFS= read -r x || [ -n "$x" ]; do
    n=$((n + 1)); x="${x%$'\r'}"
    if [ "$n" -eq 1 ]; then x="${x#$'\xEF\xBB\xBF'}"; [[ $x =~ ^---[[:space:]]*$ ]] || break; FM=1; DEB=1; continue; fi
    [[ $x =~ ^---[[:space:]]*$ ]] && { FM=2; break; }
    if [ "$DEB" -eq 1 ] && [[ $x =~ ^[[:space:]]*[^[:space:]#] ]]; then DEB=0
      [[ $x =~ ^[[:space:]] ]] && refus 'R-1/cle-model' "$f:$n" "$x" "frontmatter indenté : clés de premier niveau non lues"; fi
    if [ "$SUITE" -eq 1 ] && [[ $x =~ [^[:space:]] ]]; then SUITE=0
      [[ $x =~ ^[[:space:]]+[^[:space:]#] ]] && refus 'R-1/hors-liste' "$f:$n" "$x" "suite de la valeur model sur une autre ligne : non lue"; fi
    [[ $x =~ $NON_NUE ]] && refus 'R-1/cle-model' "$f:$n" "$x" "ligne de premier niveau qui n'est pas une clé nue : non lue"
    # Clé model de premier niveau comptée ; toute ligne model contrôlée, indentée ou non.
    [[ $x =~ ^model[[:space:]]*:([[:space:]]|$) ]] && { K=$((K + 1)); SUITE=1; }
    [[ $x =~ ^[[:space:]]*model[[:space:]]*: ]] &&
      verdict "$f:$n" "$(norm "$(printf '%s' "$x" | sed -E 's/^[[:space:]]*model[[:space:]]*:[[:space:]]*//')")"
  done < "$f"
  [ "$FM" -eq 1 ] && refus 'R-1/cle-model' "$f" "frontmatter non fermé" "aucune ligne --- de fin"
  # Agent : une seule clé model de premier niveau ; absente, c'est l'héritage du modèle de
  # session ; répétée, le modèle retenu dépend du lecteur YAML. Skills et commandes : sans
  # règle de compte (CH-7), leurs lignes model restent contrôlées.
  case "$f" in */.claude/agents/*) NA=$((NA + 1))
    [ "$K" -eq 1 ] || refus 'R-1/cle-model' "$f" "$K clé(s) model de premier niveau" "une seule exigée" ;; esac
done <<EOF_FILES
$(find "$ROOT" "${ELAG[@]}" -name '*.md' \( -path '*/.claude/agents/*' -o -path '*/.claude/skills/*' -o -path '*/.claude/commands/*' \) -print 2>/dev/null)
EOF_FILES

# 2) Réglages JSON, aplatis : une clé et sa valeur sur deux lignes sont lues. Une clé
#    dont la valeur n'est pas une chaîne est refusée : elle n'épingle rien. Une clé qui
#    porte une barre oblique inverse est refusée : un échappement peut former model.
for f in "$ROOT/.claude/settings.json" "$ROOT/.claude/settings.local.json"; do
  [ -f "$f" ] || continue
  N=$((N + 1))
  J="$(tr '\r\n' '  ' < "$f")"
  P="$(printf '%s' "$J" | grep -ioE '"(model|advisorModel)"[[:space:]]*:[[:space:]]*"[^"]*"')"
  [ "$(printf '%s' "$J" | grep -ioE '"(model|advisorModel)"[[:space:]]*:' | wc -l)" -eq "$(printf '%s' "$P" | grep -c .)" ] ||
    refus 'R-1/hors-liste' "$f" "valeur non chaîne" "clé model ou advisorModel sans identifiant entre guillemets"
  printf '%s' "$J" | grep -qE '"[^"]*\\[^"]*"[[:space:]]*:' &&
    refus 'R-1/hors-liste' "$f" "clé JSON avec échappement" "clé non lue : un échappement peut former model ou advisorModel"
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    verdict "$f ($(printf '%s' "$p" | sed -E 's/^"([^"]*)".*/\1/'))" "$(printf '%s' "$p" | sed -E 's/^"[^"]*"[[:space:]]*:[[:space:]]*"(.*)"$/\1/')"
  done <<EOF_JSON
$P
EOF_JSON
done

# 3) Scripts de workflow : le paramètre model d'un appel agent( prime sur le frontmatter.
#    Aucun lint ne les lit encore : tout script qui en contient un est refusé (item
#    SHOGEN-LINT-WORKFLOW-1). Élagage ELAG, commun aux passes 1 et 3.
while IFS= read -r f; do
  [ -n "$f" ] && refus 'R-1/workflow' "$f" "appel agent(" "script de workflow non couvert (item SHOGEN-LINT-WORKFLOW-1)"
done <<EOF_WF
$(find "$ROOT" "${ELAG[@]}" -type f \( -name '*.js' -o -name '*.mjs' -o -name '*.cjs' \) -exec grep -lE '(^|[^A-Za-z0-9_$.])agent[[:space:]]*\(' {} + 2>/dev/null)
EOF_WF

if [ "$NA" -eq 0 ]; then
  refus 'R-1/vide' "$ROOT/.claude" "0 agent" "aucun agent lu, quels que soient les réglages : pas de vert par absence"
fi
if [ "$FAIL" -ne 0 ]; then
  echo "Épingler un identifiant de la liste blanche : $ALLOWED (R-1)." >&2
  exit 2
fi
echo "OK (R-1) : $N fichier(s) ; liste blanche : $ALLOWED"
exit 0
