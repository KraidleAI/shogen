#!/usr/bin/env bash
# Shōgen, lot D8a (ADR-0028 D8, C-14) : cas du lint d'épinglage des modèles, table du §7
# du G0 (docs/adr-0028/G0-lot-D8a.md). Conçu d'après le runner de l'amont VibeGates
# (enforcement/tests/run-fixtures-model-pinning.sh, blob d9ad850), plus compact ; ses deux
# cas propres hors roster sont ici inversés, donc refusés (T-14, T-15).
# Fixtures : fixtures/model-pinning/, copies octet pour octet des frontmatters de
# .claude/agents/ à fb089dc (shogen-devops.md l.1-13, shogen-orchestrator.md l.1-15 ;
# sha256 au journal G1). Chaque cas bâtit un arbre sous mktemp, hors du dépôt, jamais sous
# un .claude/agents/ du dépôt, que Claude Code chargerait comme agent. B, l'identifiant
# banni, est construit à l'exécution. Chaque cas vérifie la sortie ET le jeton ; un cas
# « 0 » exige le message OK et son compte de fichiers. Un seul résumé fait foi.
# Usage : run-fixtures-model-pinning.sh [lint]   Sortie : 0 tout passe, 1 un cas échoue,
# 3 erreur fatale.

set -u
H="$(cd "$(dirname "$0")" && pwd)" || exit 3
LINT="${1:-$H/../lint-model-pinning.sh}"
FX="$H/fixtures/model-pinning"
[ -f "$LINT" ] && [ -f "$FX/shogen-devops.md" ] && [ -f "$FX/shogen-orchestrator.md" ] ||
  { echo "ERREUR : lint ou fixtures introuvables" >&2; exit 3; }
W="$(mktemp -d)" || exit 3
trap 'rm -rf "$W"' EXIT
B="claude-opus-""5"
OK=0; KO=0; K=0

# arbre D|O|- [ligne] : arbre neuf $T, copie $A de la fixture (D devops, O orchestrateur),
# sa ligne model remplacée par [ligne] (@SANS@ : supprimée ; @DEUX@ : doublée) ; - : vide.
arbre() {
  K=$((K + 1)); T="$W/t$K"; A="$T/.claude/agents/a.md"
  mkdir -p "$T/.claude/agents" || exit 3
  case "$1" in D) s="$FX/shogen-devops.md" ;; O) s="$FX/shogen-orchestrator.md" ;; *) return 0 ;; esac
  awk -v m="${2-}" '/^model:/ && !d { d = 1; if (m == "@SANS@") next
    if (m == "@DEUX@") { print; print; next } if (m != "") { print m; next } } { print }' "$s" > "$A" || exit 3
}
ins() { awk -v n="$1" -v l="$2" '{ print } NR == n { print l }' "$A" > "$T/x" && mv "$T/x" "$A"; }
# cas id sortie jeton|compte [jeton interdit]
cas() {
  o="$(bash "$LINT" "$T" 2>&1)"; r=$?
  if [ "$2" = 0 ]; then e="OK (R-1) : $3 fichier(s)"; else e="REFUS ($3)"; fi
  if [ "$r" = "$2" ] && printf '%s\n' "$o" | grep -qF "$e" &&
     { [ -z "${4-}" ] || ! printf '%s\n' "$o" | grep -qF "($4)"; }; then
    OK=$((OK + 1))
  else
    KO=$((KO + 1)); echo "ÉCHEC $1 : attendu $2 $3, obtenu $r" >&2; printf '%s\n' "$o" | head -3 >&2
  fi
}

arbre O; cas T-01 0 1
arbre D; cas T-02 0 1
arbre D 'model: claude-sonnet-5-5'; cas T-03 0 1
arbre D 'model: opus'; cas T-04 2 R-1/tier-nu
arbre D 'model: fable'; cas T-05 2 R-1/tier-nu
arbre D 'model: sonnet'; cas T-06 2 R-1/tier-nu
arbre D "model: $B"; cas T-07 2 R-1/ban
arbre D "model: $B[1m]"; cas T-08 2 R-1/ban
arbre D "model: ${B}x"; cas T-09 2 R-1/hors-liste
arbre D "model: ${B}0"; cas T-10 2 R-1/hors-liste
arbre D "model: ${B}-0"; cas T-11 2 R-1/hors-liste
arbre D "model: ${B}-50"; cas T-12 2 R-1/hors-liste
arbre D 'model: claude-opus-5-5[1m]'; cas T-13 2 R-1/hors-liste
arbre D 'model: claude-sonnet-5'; cas T-14 2 R-1/hors-liste R-1/ban
arbre D 'model: claude-opus-4-8'; cas T-15 2 R-1/hors-liste
arbre D "model: $(printf '%s' "$B" | tr '[:lower:]' '[:upper:]')"; cas T-16 2 R-1/ban
arbre D 'model: CLAUDE-OPUS-5-5'; cas T-17 2 R-1/hors-liste
arbre D 'model: fable   # ADR-0003'; cas T-18 2 R-1/tier-nu
arbre D "model: $B   # ADR-9999"; cas T-19 2 R-1/ban
arbre D @SANS@; cas T-21 2 R-1/cle-model
arbre D @DEUX@; cas T-22 2 R-1/cle-model
arbre O; ins 4 '  model: claude-opus-5-5'; cas T-23 0 1
arbre O; ins 4 "  model: $B"; cas T-24 2 R-1/ban
arbre O; printf '%s\n' 'corps' "model: $B" >> "$A"; cas T-25 0 1
arbre -; cas T-26 2 R-1/vide
arbre D; { printf '\357\273\277'; cat "$FX/shogen-devops.md"; } > "$A"; cas T-27 0 1
arbre D "model: $B"; { printf '\357\273\277'; cat "$A"; } > "$T/x" && mv "$T/x" "$A"; cas T-28 2 R-1/ban

echo "model-pinning : $OK ok, $KO échec"
[ "$KO" -eq 0 ]
