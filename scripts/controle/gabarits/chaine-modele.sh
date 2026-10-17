#!/usr/bin/env bash
# Modèle de chaîne de commits de l'orchestrateur (GARDE-FOUS phase 3, groupe A ; SHOGEN-GARDE-CHAINE-ORCH-MODELE-1 ;
# erreurs E3, E8, E11, E25, E30, E31, E34, E36), à copier par chaîne à la place de gabarits/chaine.sh, qui garde la
# fonction verif scellée (C1). La chaîne n'écrit aucune verif : elle la tire par source du modèle des outils, celle que
# le sceau et acte commit jugent ; l'isolement réseau et le retrait des variables de mandataire sont dans cette verif.
# Plan, rapport du contre-contrôle et lancement : comme gabarits/chaine.sh (voir son en-tête). Avant tout pas, avant_acte
# chaine --blanc juge ce script (K1 à K4, K7) et les diffs du plan, dans l'ordre, sur une copie creuse (K0, K5, K6, G5) ;
# toute sortie en erreur écrit sa ligne ROUGE (trap ERR, E36).
set -Eeuo pipefail
trap 'echo "ROUGE l.$LINENO : $BASH_COMMAND (code $?)" >&2' ERR
DEPOT=${DEPOT:-/home/user/shogen}
PLAN=${PLAN:?PLAN : fichier de plan}
CC=${CC:?CC : rapport du contre-contrôle}
OUTILS=${OUTILS:-$DEPOT/scripts/controle}
PYTHON=${PYTHON:-python3}
DELAI=${DELAI:-2400}
acte() { "$PYTHON" -I -B "$OUTILS/avant_acte.py" --depot "$DEPOT" "$@"; }
source <(sed -n '/^verif() {/,/^# --- fin de verif/p' "$OUTILS/gabarits/chaine.sh")
declare -F verif > /dev/null || { echo "ROUGE : verif introuvable dans $OUTILS/gabarits/chaine.sh" >&2; exit 1; }

acte chaine --plan "$PLAN" --cc "$CC" --blanc --script "$(realpath "$0")" ${DUREE_PAS:+--duree-pas "$DUREE_PAS"} ${DETACHE:+--detache}
while IFS='|' read -r -u 3 id diffs message sources; do
  [ -n "$id" ] || continue
  if git -C "$DEPOT" log --format=%B | grep -Fx "Diff-Id: $id" > /dev/null; then echo "déjà commis : $id"; continue; fi
  [ -z "$(git -C "$DEPOT" status --porcelain)" ] || { echo "arbre non propre avant $id : arrêt" >&2; exit 1; }
  acte disque --min-go "${DISQUE_MIN_GO:-0}" || { echo "ROUGE disque avant $id (LN-1) : arrêt, rien appliqué" >&2; exit 1; }
  options=(--message "$message" --id "$id")
  for d in ${diffs//,/ }; do git -C "$DEPOT" apply --index "$d"; options+=(--diff "$d"); done
  for s in ${sources//,/ }; do options+=(--source "$s"); done
  verif "$id" && declare -f verif | acte sceller --verif - || { echo "vérification rouge avant $id : arrêt, rien de commis" >&2; exit 1; }
  acte commit "${options[@]}" && git -C "$DEPOT" commit -q -F "$message" || { echo "refus du commit $id" >&2; exit 1; }
  git -C "$DEPOT" log --oneline -1
done 3< "$PLAN"
echo FIN
