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
# Portée : frontmatter (premier bloc ---) de .claude/agents/**/*.md et de
# .claude/skills/**/*.md, corps non lu. Tout ce qui n'est pas exactement dans la liste
# est refusé : tier nu, identifiant banni, casse ou suffixe différents, clé model
# absente ou répétée, portée vide.
# Limite : ce lint lit le texte versionné, pas le modèle qui tourne (paramètre
# d'invocation, environnement, réglages hors dépôt, substitution par la plateforme) ;
# le contrôle R-1 au lancement reste dû.
# Usage : lint-model-pinning.sh [racine]   Sortie : 0 conforme, 2 refus (stderr).

set -u
ROOT="${1:-.}"
[ "$ROOT" = / ] || ROOT="${ROOT%/}"
ALLOWED='claude-opus-5-5 claude-sonnet-5-5 claude-fable-5-1'
BANNED="claude-opus-""5"
TIERS='opus|sonnet|haiku|fable|inherit|default|opusplan'
FAIL=0
N=0

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
  else
    refus 'R-1/hors-liste' "$1" "$2" "hors liste blanche ($ALLOWED)"
  fi
}

# 1) Frontmatter des agents et des skills, parcours récursif comme la découverte de
#    Claude Code. Lu en bash, octet pour octet : les sed et awk de Git Bash retirent le CR
#    des fins CRLF (mesuré), ce qui masquerait en local la règle du CR. BOM de la ligne 1
#    et CR final retirés ici ; numéros de ligne conservés.
while IFS= read -r f; do
  [ -f "$f" ] || continue
  N=$((N + 1)); n=0; K=0
  while IFS= read -r x || [ -n "$x" ]; do
    n=$((n + 1)); x="${x%$'\r'}"
    if [ "$n" -eq 1 ]; then x="${x#$'\xEF\xBB\xBF'}"; [[ $x =~ ^---[[:space:]]*$ ]] || break; continue; fi
    [[ $x =~ ^---[[:space:]]*$ ]] && break
    # Clé model de premier niveau comptée ; toute ligne model contrôlée, indentée ou non.
    [[ $x =~ ^model[[:space:]]*: ]] && K=$((K + 1))
    [[ $x =~ ^[[:space:]]*model[[:space:]]*: ]] &&
      verdict "$f:$n" "$(norm "$(printf '%s' "$x" | sed -E 's/^[[:space:]]*model[[:space:]]*:[[:space:]]*//')")"
  done < "$f"
  # Une seule clé model de premier niveau : absente, c'est l'héritage du modèle de
  # session ; répétée, le modèle retenu dépend du lecteur YAML.
  [ "$K" -eq 1 ] || refus 'R-1/cle-model' "$f" "$K clé(s) model de premier niveau" "une seule exigée"
done <<EOF_FILES
$(find "$ROOT/.claude/agents" "$ROOT/.claude/skills" -name '*.md' 2>/dev/null)
EOF_FILES

if [ "$N" -eq 0 ]; then
  refus 'R-1/vide' "$ROOT/.claude" "0 fichier" "aucun agent ni skill dans la portée : pas de vert par absence"
fi
if [ "$FAIL" -ne 0 ]; then
  echo "Épingler un identifiant de la liste blanche : $ALLOWED (R-1)." >&2
  exit 2
fi
echo "OK (R-1) : $N fichier(s) ; liste blanche : $ALLOWED"
exit 0
