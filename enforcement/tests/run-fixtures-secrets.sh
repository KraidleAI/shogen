#!/usr/bin/env bash
# Shōgen, lot D8b (ADR-0028 D8) : cas de la gate des secrets, table du §7 du G0
# (docs/adr-0028/G0-lot-D8b.md). Conçu d'après le runner amont (VibeGates
# enforcement/tests/run-fixtures.sh, blob 7960238, section secrets), sans en recopier aucune
# valeur : chaque forme d'identifiant est formée à l'exécution depuis les fragments tronqués de
# fixtures/secrets/sondes.tsv (aucun fragment, aucune ligne ne répond seul aux motifs).
# Isolation (TEST-GIT-ENV-ISOLATION-1) : refus si une variable de dépôt GIT_* est posée ; chaque
# cas dans un dépôt jetable sous mktemp, hors de tout dépôt, config locale, crochets neutralisés
# par core.hooksPath (jamais --no-verify), toute commande git en -C <dépôt jetable>.
# Chaque cas vérifie la sortie ET le jeton, ou le message OK et son compte ; un motif requis ou
# interdit précise le message quand le jeton seul ne tranche pas. Un seul résumé fait foi.
# Usage : run-fixtures-secrets.sh [gate]   Sortie : 0 tout passe, 1 un cas échoue, 3 erreur fatale.

set -u
fatal() { echo "ERREUR FATALE : $1" >&2; exit 3; }
for v in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_COMMON_DIR GIT_NAMESPACE GIT_ALTERNATE_OBJECT_DIRECTORIES; do
  [ -z "${!v+x}" ] || fatal "variable $v posée (isolation)"
done
H="$(cd "$(dirname "$0")" && pwd)" || exit 3
GATE="${1:-$H/../gate-secrets.sh}"; FX="$H/fixtures/secrets/sondes.tsv"
[ -f "$GATE" ] && [ -f "$FX" ] || fatal "gate ou fixture introuvable"
GATE="$(cd "$(dirname "$GATE")" && pwd)/$(basename "$GATE")"
command -v iconv >/dev/null || fatal "iconv absent (T-06)"
W="$(mktemp -d)" || fatal "mktemp -d"
trap 'rm -rf "$W"' EXIT
git -C "$W" rev-parse --is-inside-work-tree >/dev/null 2>&1 && fatal "dossier de travail dans un dépôt"
mkdir "$W/nh" || fatal "mkdir"
OK=0; KO=0; K=0; D=; A=

# forme ID : valeur de la sonde ID (p1 p2, remplissage répété n fois, suffixe), formée à l'exécution.
forme() { awk -F '\t' -v i="$1" '$1 == i { s = $2 $3; for (k = 0; k < $5; k++) s = s $4; print s $6; t = 1 } END { exit !t }' "$FX"; }
V="$(forme V-01)" && G="$(forme G-06)" || fatal "sondes V-01 ou G-06 introuvables"
# r : dépôt jetable neuf $R (isolé, sans crochets, sans signature), commit initial base.txt.
r() {
  K=$((K + 1)); R="$W/r$K"; mkdir "$R" && git -C "$R" init -q -b main || fatal "init"
  [ -z "$(git -C "$R" rev-parse --show-prefix)" ] || fatal "préfixe non vide"
  for c in user.name=t user.email=t@example.invalid commit.gpgsign=false core.autocrlf=false "core.hooksPath=$W/nh"; do
    git -C "$R" config "${c%%=*}" "${c#*=}" || fatal "config"
  done
  echo base > "$R/base.txt"; ci init
}
ci() { git -C "$R" add -A && git -C "$R" commit -q -m "$1" || fatal "commit"; }
st() { git -C "$R" add -- "$@" || fatal "add"; }
# cas ID sortie jeton|fin-du-message-OK [requis] [interdit] : gate lancée depuis ${D:-$R}, arguments $A.
cas() {
  o="$(cd "${D:-$R}" && bash "$GATE" $A 2>&1)"; c=$?
  if [ "$2" = 0 ]; then e="OK (secrets) : $3"; else e="REFUS ($3)"; fi
  if [ "$c" = "$2" ] && printf '%s\n' "$o" | grep -qF -- "$e" && { [ -z "${4-}" ] || printf '%s\n' "$o" | grep -qE -- "$4"; } &&
     { [ -z "${5-}" ] || ! printf '%s\n' "$o" | grep -qE -- "$5"; }; then OK=$((OK + 1))
  else KO=$((KO + 1)); echo "ÉCHEC $1 : attendu $2 $3, obtenu $c" >&2; printf '%s\n' "$o" | head -3 >&2; fi
  D=; A=
}

r; printf 'k = "%s"\n' "$V" > "$R/s.py"; st s.py; cas T-01 2 SECRETS/forme
r; printf '%s\n' "$G" | tr a-z A-Z > "$R/s.py"; st s.py; cas T-02 2 SECRETS/forme
r; printf 'k = "%s"\n' "$V" | tr A-Z a-z > "$R/s.py"; st s.py; cas T-03 0 '1 fichier(s)'
r; printf 'x = 1\n' > "$R/ok.py"; st ok.py; cas T-04 0 '1 fichier(s)'
r; printf 'X = "a\000b"\nkey = "%s"\n' "$V" > "$R/cfg.py"; st cfg.py; cas T-05 2 SECRETS/forme
r; printf 'k = "%s"\n' "$V" | iconv -f UTF-8 -t UTF-16LE > "$R/w.ps1" || fatal iconv; st w.ps1; cas T-06 2 SECRETS/forme
r; printf '%s\n' "$G" > "$R/résumé.py"; st résumé.py; cas T-07 2 SECRETS/forme '^résumé\.py:1: \[contenu masqué\]' 'QQQQ|pass|word'
r; printf '%s\n' '++i;' '++ b/HIJACK.txt' "$G" > "$R/f.c"; st f.c; cas T-08 2 SECRETS/forme '^f\.c:3: ' HIJACK
r; mkdir "$R/sub" "$R/other"; printf 'k = "%s"\n' "$V" > "$R/other/leak.py"; echo 'x=1' > "$R/sub/fine.py"; st .
D="$R/sub"; cas T-09 2 SECRETS/forme; D="$R/sub"; A=--tree; cas T-10 2 SECRETS/forme
r; git -C "$R" update-index --add --cacheinfo "160000,$(git -C "$R" rev-parse HEAD),vendor/mod" || fatal gitlink
echo 'x=1' > "$R/t.py"; st t.py; cas T-11 0 '1 fichier(s)' "'vendor/mod' ignoré, entrée non-blob"
r; b="$(printf 'cible' | git -C "$R" hash-object -w --stdin)" && git -C "$R" update-index --add --cacheinfo "120000,$b,lien" || fatal lien
cas T-12 0 '0 fichier(s)' "'lien' ignoré, entrée non-blob"
D="$W/nh"; cas T-13 2 SECRETS/echec "hors d.un arbre de travail"
r; A=--hstory; cas T-14 2 SECRETS/echec 'argument inconnu'

echo "secrets : $OK ok, $KO échec"
[ "$KO" -eq 0 ]
