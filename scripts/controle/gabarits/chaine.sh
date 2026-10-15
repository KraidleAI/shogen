#!/usr/bin/env bash
# Modèle de chaîne de commits de l'orchestrateur (lot GARDE-FOUS-ORCH, GF-9 ; erreurs E3, E8, E25, LA-N04, LA-N05), à
# copier par lot. Lancement détaché, avec un délai (E3), attente dans un appel séparé ; un lancement lié est refusé
# au-delà de 100 min estimées (DUREE_PAS : durée mesurée d'un pas en minutes, 6 par défaut) :
#   DETACHE=1 setsid nohup timeout <s> bash chaine.sh > chaine.log 2>&1 &   (<s> = 120 × pas × minutes d'un pas)
# PLAN : une ligne par commit, champs séparés par | : id|diff1,diff2|fichier de message|source1,source2. Un diff rouge
# seul ne forme jamais une ligne : il va avec le diff qui le rend vert (E11). Le message est un fichier écrit après la
# dernière retouche des sources, avec une ligne Source-Sha: <sha256> par source et la ligne Diff-Id: <id> ; la chaîne
# ne l'écrit jamais (E8). Reprise : un id dont la ligne Diff-Id est déjà dans l'historique est sauté. CC : rapport du
# contre-contrôle, à la ligne fixe GROUPES : de gabarits/rapport-cc.md, lue avant tout pas (E11).
set -euo pipefail
DEPOT=${DEPOT:-/home/user/shogen}
PLAN=${PLAN:?PLAN : fichier de plan}
CC=${CC:?CC : rapport du contre-contrôle}
OUTILS=${OUTILS:-$DEPOT/scripts/controle}
PYTHON=${PYTHON:-python3}
DELAI=${DELAI:-2400}
acte() { "$PYTHON" -I -B "$OUTILS/avant_acte.py" --depot "$DEPOT" "$@"; }

# Vérification complète, comme la forge (à relire par lot) : xtask (verdict seul lu), cargo test de xtask à la cible
# cargo par défaut de la copie (règle I-1), lignes python3 -B enforcement/ de gates.yml, lint R-1 et ses cas. Appelée
# par verif && sceller, la fonction tourne hors de set -e : chaque pas sort en 1 à son échec (relecture G2, C-1) ;
# cargo tourne sans CARGO_TARGET_DIR ni CARGO_BUILD_TARGET_DIR, à la cible par défaut (E5, règle I-1 ; C-15).
verif() {
  local j sans="-u CARGO_TARGET_DIR -u CARGO_BUILD_TARGET_DIR"
  j="$(dirname "$PLAN")/verif-$1"
  ( cd "$DEPOT" || exit 1
    timeout "$DELAI" env $sans cargo --locked xtask verify > "$j-xtask.log" 2>&1 || true
    grep -F "VERDICT GLOBAL : VERT" "$j-xtask.log" > /dev/null || exit 1
    timeout "$DELAI" env $sans cargo --locked test -p xtask > "$j-cargo.log" 2>&1 || exit 1
    grep -E '^ *(run: )?(/usr/bin/)?python3 -B enforcement/' .github/workflows/gates.yml | sed -E 's/^ *(run: )?//' |
      while read -r ligne; do
        env -u SHOGEN_S2_CAMPAGNE_CONTROL timeout "$DELAI" bash -c "$ligne" < /dev/null > /dev/null 2>&1 || exit 1
      done || exit 1
    timeout "$DELAI" bash enforcement/tests/run-fixtures-model-pinning.sh < /dev/null > /dev/null 2>&1 || exit 1
    timeout "$DELAI" bash enforcement/lint-model-pinning.sh . < /dev/null > /dev/null 2>&1 )
}
# --- fin de verif

acte chaine --plan "$PLAN" --cc "$CC" ${DUREE_PAS:+--duree-pas "$DUREE_PAS"} ${DETACHE:+--detache}
acte disque --min-go "${DISQUE_MIN_GO:-0}"
while IFS='|' read -r -u 3 id diffs message sources; do
  [ -n "$id" ] || continue
  if git -C "$DEPOT" log --format=%B | grep -Fx "Diff-Id: $id" > /dev/null; then echo "déjà commis : $id"; continue; fi
  [ -z "$(git -C "$DEPOT" status --porcelain)" ] || { echo "arbre non propre avant $id : arrêt" >&2; exit 1; }
  options=(--message "$message" --id "$id")
  for d in ${diffs//,/ }; do git -C "$DEPOT" apply --index "$d"; options+=(--diff "$d"); done
  for s in ${sources//,/ }; do options+=(--source "$s"); done
  verif "$id" && acte sceller || { echo "vérification rouge avant $id : arrêt, rien de commis" >&2; exit 1; }
  acte commit "${options[@]}" && git -C "$DEPOT" commit -q -F "$message" || { echo "refus du commit $id" >&2; exit 1; }
  git -C "$DEPOT" log --oneline -1
done 3< "$PLAN"
echo FIN
