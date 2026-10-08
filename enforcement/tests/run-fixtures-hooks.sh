#!/usr/bin/env bash
# Shōgen, lot D8c (ADR-0028 D8) : cas du hook pre-commit versionné et de son installeur, table du §7 du G0
# (docs/adr-0028/G0-lot-D8c.md) : H-01 à H-20 (étape R-13), I-01 à I-13 (installeur) ; ajoutés au G1 :
# H-21 (git grep en erreur), H-22 (lancement direct depuis un sous-dossier), I-14 (argument inconnu) ;
# C-01 à C-12 (branchement du lint d'épinglage de D8a et de la gate des secrets de D8b), C-13 (ajouté au
# G1 : extraction de l'index en échec), C-14 (ajouté au G1 : lancement direct, index inchangé, forme d'O-13).
# Ajouté à la revue G2 (2026-10-01) : H-23 (git commit --amend, consommateur 1 du G0 §10). Lot DETTES-B2 (2026-10-04) :
# H-24a à H-24c (étape de balayage du job g5, git grep en erreur : SHOGEN-G5-ERREUR-GREP-1), H-20 lu sur la forme captée.
# Dépôt modèle sous mktemp, hors de tout dépôt : git init -b main, identité factice, commit.gpgsign=false,
# core.autocrlf=false ; un commit avec deux agents valides (fixtures de D8a), puis le commit de base qui
# ajoute le lint et la gate de l'arbre, le hook et l'installeur sous test, dont ATTENDU est remplacé par
# le sha256 du hook sous test (identité pour les vrais : I-10). Formes d'identifiant : sondes de D8b.
# Chaque cas travaille sur une copie du modèle, hook installé par l'installeur (I-01), puis git commit réel :
# sortie ET jeton vérifiés. Marqueurs formés à l'exécution ; ce fichier n'en porte aucun, ni les octets du
# hook local (I-03 emploie un double de test). Isolation : refus si une variable GIT_* de dépôt est posée ;
# ce runner ne pose jamais GIT_DIR ni GIT_WORK_TREE (I-11 pose GIT_INDEX_FILE, vers un chemin inexistant,
# pour le seul appel de l'installeur).
# Usage : run-fixtures-hooks.sh [hook] [installeur]   Sortie : 0 tout passe, 1 un cas échoue, 3 erreur fatale.

set -u
fatal() { echo "ERREUR FATALE : $1" >&2; exit 3; }
for v in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR GIT_OBJECT_DIRECTORY; do
  [ -z "${!v+x}" ] || fatal "variable $v posée (isolation, incident du 2026-09-24)"
done
H="$(cd "$(dirname "$0")" && pwd)" || exit 3
HOOK="${1:-$H/../hooks/pre-commit}"; INST="${2:-$H/../hooks/install-pre-commit.sh}"
HOOK="$(cd "$(dirname "$HOOK")" && pwd)/$(basename "$HOOK")" && INST="$(cd "$(dirname "$INST")" && pwd)/$(basename "$INST")" || exit 3
GY="$H/../../.github/workflows/gates.yml"; FX="$H/fixtures/model-pinning"; SO="$H/fixtures/secrets/sondes.tsv"
for x in "$HOOK" "$INST" "$GY" "$FX/shogen-devops.md" "$FX/shogen-orchestrator.md" "$H/../lint-model-pinning.sh" "$H/../gate-secrets.sh" "$SO"; do
  [ -f "$x" ] || fatal "pièce introuvable : $x"; done
W="$(mktemp -d)" || fatal "mktemp -d"
trap 'rm -rf "$W"' EXIT
git -C "$W" rev-parse --is-inside-work-tree >/dev/null 2>&1 && fatal "dossier de travail dans un dépôt"
M1="TO""DO"; M2="FIX""ME"; OK=0; KO=0; K=0; E=; D=
sha() { sha256sum < "$1" | cut -d' ' -f1; }
res() { if [ "$2" = 0 ]; then OK=$((OK + 1)); else KO=$((KO + 1)); echo "ÉCHEC $1${E:+ : $E}" >&2; fi; E=; }
# m0 : commit de base, sans hook ; m1 : m0 puis hook installé (I-01). c0, c1 : copies neuves de m0, de m1.
m="$W/m0"; mkdir -p "$m/.claude/agents" "$m/enforcement/hooks" && git -C "$m" init -q -b main || fatal init
for c in user.name=t user.email=t@example.invalid commit.gpgsign=false core.autocrlf=false; do git -C "$m" config "${c%%=*}" "${c#*=}" || fatal config; done
cp "$FX/shogen-devops.md" "$FX/shogen-orchestrator.md" "$m/.claude/agents/" && git -C "$m" add -A && git -C "$m" commit -qm agents &&
  cp "$H/../lint-model-pinning.sh" "$H/../gate-secrets.sh" "$m/enforcement/" && cp "$HOOK" "$m/enforcement/hooks/pre-commit" &&
  sed "s/^ATTENDU=.*/ATTENDU='$(sha "$HOOK")'/" "$INST" > "$m/enforcement/hooks/install-pre-commit.sh" &&
  git -C "$m" add -A && git -C "$m" commit -qm base && cp -r "$m" "$W/m1" || fatal "dépôt modèle"
c0() { K=$((K + 1)); R="$W/r$K"; D=; cp -r "$W/m0" "$R" || fatal copie; }
c1() { K=$((K + 1)); R="$W/r$K"; D=; cp -r "$W/m1" "$R" || fatal copie; }
# f chemin texte : écrit le fichier sous ${D:-$R} et l'indexe. ci attendu jeton[+jeton...] [arguments] :
# git commit réel ; 0 exige OK (hook), 1 exige chaque jeton. forme ID : valeur de la sonde ID de D8b.
f() { p="${D:-$R}/$1"; mkdir -p "${p%/*}" && printf '%s\n' "$2" > "$p" && git -C "${D:-$R}" add -- "$1" || fatal add; }
ci() { a="$1"; j="$2"; shift 2; o="$(cd "${D:-$R}" && git commit -qm c "$@" 2>&1)"; r=$?; E=
  [ "$r" = "$a" ] || E=" sortie $r au lieu de $a ;"
  if [ "$a" = 0 ]; then l="OK (hook)"; else l="$(printf 'REFUS (%s)\n' ${j//+/ })"; fi
  while IFS= read -r e; do printf '%s\n' "$o" | grep -qF "$e" || E="$E $e absent ;"; done <<< "$l"
  [ -z "$E" ] && return 0; E="commit :$E $(printf '%s\n' "$o" | grep -m1 -E 'REFUS|OK|fatal|error')"; return 1; }
forme() { awk -F '\t' -v i="$1" '$1 == i { s = $2 $3; for (k = 0; k < $5; k++) s = s $4; print s $6; t = 1 } END { exit !t }' "$SO"; }
# inst attendu fragment [arguments] : installeur lancé depuis ${D:-$R} ; sortie et fragment du message vérifiés.
inst() { a="$1"; t="$2"; shift 2; o="$(cd "${D:-$R}" && bash enforcement/hooks/install-pre-commit.sh "$@" 2>&1)"; r=$?
  [ "$r" = "$a" ] && printf '%s\n' "$o" | grep -qF "$t" && return 0
  E="installeur : attendu $a, $t ; obtenu $r, $(printf '%s\n' "$o" | head -1)"; return 1; }
# etat : empreinte du dossier des hooks de $R (noms, tailles, dates, sha256 du hook) ; ho : sha256 du hook installé.
etat() { { ls -lA --full-time "$R/.git/hooks"; sha "$R/.git/hooks/pre-commit" 2>/dev/null; } | sha256sum; }
ho() { sha "$R/.git/hooks/pre-commit" 2>/dev/null; }
# pr message : commit de préparation dans $R, sortie tue ; un refus fait échouer le cas.
pr() { git -C "$R" commit -qm "$1" >/dev/null 2>&1 || { E="commit de préparation refusé"; return 1; }; }

R="$W/m1"; inst 0 "OK (installation)" && [ -x "$R/.git/hooks/pre-commit" ] && [ "$(ho)" = "$(sha "$HOOK")" ]; res I-01 $?
# Étape R-13 (§7.1).
c1; f docs/x.md "# $M1 reprendre"; ci 1 HOOK/g5; res H-01 $?
c1; f docs/x.md "texte propre"; ci 0 -; res H-02 $?
c1; f src/a.rs "// $M2: corriger"; ci 1 HOOK/g5; res H-03 $?
c1; f docs/x.md "$M1: sans délimiteur"; ci 1 HOOK/g5; res H-04 $?
c1; f enforcement/x.sh "# $M1 balayé"; ci 1 HOOK/g5; res H-05 $?
c1; f .github/workflows/x.yml "# $M1 balayé"; ci 1 HOOK/g5; res H-06 $?
c1; f docs/x.md "<!-- $M1 -->"; ci 1 HOOK/g5; res H-07 $?
c1; f docs/x.md "prose : un $M1 sans délimiteur"; ci 0 -; res H-08 $?
c1; f .claude/agents/b.md "$(cat "$FX/shogen-devops.md"; echo "# $M1 dans le corps")"; ci 0 -; res H-09 $?
c1; f .github/workflows/gates.yml "# $M1 exclu"; ci 0 -; res H-10 $?
c1; f biblio/x.md "# $M1 exclu"; ci 0 -; res H-11 $?
c0; f docs/v.md "# $M1 ancien"; pr v && inst 0 "OK (installation)" && f docs/y.md propre && ci 1 HOOK/g5; res H-12 $?
c1; f docs/x.md "# $M1"; echo propre > "$R/docs/x.md"; ci 1 HOOK/g5; res H-13 $?
c1; f docs/w.md propre; pr w && echo "# $M1" >> "$R/docs/w.md" && echo "# $M1" > "$R/docs/z.md" && f docs/y.md propre && ci 0 -; res H-14 $?
c1; mkdir -p "$R/docs" && printf 'a\000b\n# %s\n' "$M1" > "$R/docs/b.bin" && git -C "$R" add docs/b.bin && ci 1 HOOK/g5; res H-15 $?
c1; f docs/w.md propre; pr w && echo "# $M1" >> "$R/docs/w.md" && ci 1 HOOK/g5 -a; res H-16 $?
c1; f docs/w.md propre; pr w && echo "# $M1" >> "$R/docs/w.md" && ci 1 HOOK/g5 -- docs/w.md; res H-17 $?
c1; git -C "$R" worktree add -q -b wt "$R.wt" || fatal worktree; D="$R.wt"; f docs/x.md "# $M1"; ci 1 HOOK/g5 && f docs/x.md propre && ci 0 -; res H-18 $?
mkdir "$W/hors" || fatal hors; o="$(cd "$W/hors" && bash "$HOOK" < /dev/null 2>&1)"; [ $? = 2 ] && printf '%s\n' "$o" | grep -qF "REFUS (HOOK/echec)"; res H-19 $?
g="$(sed -n "s/^ *g=0; git grep -nE '\([^']*\)' \(-- [^|]*\) || g=\$?\$/\1 \2/p" "$GY")"
k="$(sed -n "s/^M='\([^']*\)'\$/\1/p" "$HOOK") $(sed -n 's/^O="$(git grep --cached -nE "$M" \(-- [^)]*\))"; g=$?$/\1/p' "$HOOK")"
E="motif ou exclusions différents du job g5"; [ -n "$g" ] && [ "$g" = "$k" ]; res H-20 $?
c1; : > "$R/.git/index"; o="$(cd "$R" && bash "$HOOK" < /dev/null 2>&1)"; [ $? = 2 ] && printf '%s\n' "$o" | grep -qF "REFUS (HOOK/echec) : git grep"; res H-21 $?
c1; f docs/x.md "# $M1" && f sub/a.txt propre && o="$(cd "$R/sub" && bash "$HOOK" < /dev/null 2>&1)"; [ $? = 2 ] && printf '%s\n' "$o" | grep -qF "REFUS (HOOK/g5)"; res H-22 $?
c1; f docs/w.md propre; pr w && echo "# $M1" >> "$R/docs/w.md" && git -C "$R" add docs/w.md && ci 1 HOOK/g5 --amend; res H-23 $?
# H-24 (lot DETTES-B2, SHOGEN-G5-ERREUR-GREP-1) : le bloc run: du job g5 qui porte git grep -nE, extrait de gates.yml et lancé
# par bash -e (shell d'une étape sans shell:, inféré) : propre 0 et OK, marqueur 1, git grep en erreur (index vide) ni 0 ni OK.
awk 'function f() { if (b ~ /git grep -nE/) { printf "%s", b; b = ""; exit } b = ""; n = 0 } /^        run: \|$/ { f(); n = 1; next }
  n && (/^          / || /^$/) { b = b substr($0, 11) "\n"; next } n { f() } END { f() }' "$GY" > "$W/g5.sh" || fatal "extraction g5"
g5() { o="$(cd "$R" && bash -e "$W/g5.sh" 2>&1)"; r=$?; }
c1; g5; E="étape g5 sur un dépôt propre"; [ "$r" = 0 ] && printf '%s\n' "$o" | grep -qF "OK: aucun marqueur"; res H-24a $?
c1; f docs/x.md "# $M1 reprendre"; g5; E="étape g5 sur un marqueur"; [ "$r" = 1 ] && printf '%s\n' "$o" | grep -qF "::error::Marqueur"; res H-24b $?
c1; : > "$R/.git/index"; g5; E="étape g5, git grep en erreur : sortie $r"; [ "$r" != 0 ] && printf '%s\n' "$o" | grep -qF "::error::git grep a échoué" &&
  ! printf '%s\n' "$o" | grep -qF "OK: aucun"; res H-24c $?
# Installeur (§7.2).
c1; e0="$(etat)"; inst 0 "déjà conforme" && [ "$(etat)" = "$e0" ]; res I-02 $?
c0; printf '#!/bin/sh\nexit 0\n' > "$R/.git/hooks/pre-commit"; d="$(ho)"
sed -i "s/^CONNUS=.*/CONNUS='$d'/" "$R/enforcement/hooks/install-pre-commit.sh" && git -C "$R" add -u && pr connus &&
  inst 0 "sauvegarde" && [ "$(sha "$R/.git/hooks/pre-commit.${d:0:12}")" = "$d" ] && [ "$(ho)" = "$(sha "$HOOK")" ]; res I-03 $?
c0; printf '#!/bin/sh\nexit 0 # autre\n' > "$R/.git/hooks/pre-commit"; e0="$(etat)"; inst 2 "empreinte inconnue" && [ "$(etat)" = "$e0" ]; res I-04 $?
c0; git -C "$R" config core.hooksPath .h; e0="$(etat)"; inst 2 "core.hooksPath" && [ "$(etat)" = "$e0" ] && [ ! -e "$R/.h" ]; res I-05 $?
c0; git -C "$R" worktree add -q -b wt "$R.wt" || fatal worktree; e0="$(etat)"; D="$R.wt"; inst 2 "arbre lié" && [ "$(etat)" = "$e0" ]; res I-06 $?
c0; echo "# autre" >> "$R/enforcement/hooks/pre-commit"; git -C "$R" add -u && pr h && inst 2 "différent d'ATTENDU" && [ -z "$(ho)" ]; res I-07 $?
c0; echo "# autre" >> "$R/enforcement/hooks/pre-commit"; inst 0 "OK (installation)" && [ "$(ho)" = "$(sha "$HOOK")" ]; res I-08 $?
c1; e0="$(etat)"; inst 0 "conforme" --verifier && [ "$(etat)" = "$e0" ] && echo "# x" >> "$R/.git/hooks/pre-commit" && e0="$(etat)" &&
  inst 2 "différent d'ATTENDU" --verifier && [ "$(etat)" = "$e0" ] && rm "$R/.git/hooks/pre-commit" && e0="$(etat)" &&
  inst 2 "aucun hook installé" --verifier && [ "$(etat)" = "$e0" ]; res I-09 $?
E="constantes de l'installeur"; grep -qE "^CONNUS='([0-9a-f]{64} )*1da91c723b7f4747edb35dcc2cce7492e334b648c5e00c41f239cca5ab61277d[ ']" "$INST" &&
  [ "$(sed -n "s/^ATTENDU='\([0-9a-f]\{64\}\)'\$/\1/p" "$INST")" = "$(sha "$H/../hooks/pre-commit")" ]; res I-10 $?
c0; e0="$(etat)"; o="$(cd "$R" && GIT_INDEX_FILE="$W/nulle" bash enforcement/hooks/install-pre-commit.sh 2>&1)"
[ $? = 2 ] && printf '%s\n' "$o" | grep -qF "GIT_INDEX_FILE posée" && [ "$(etat)" = "$e0" ]; res I-11 $?
mkdir "$W/hors2" && cp "$INST" "$W/hors2/i.sh" || fatal hors2; o="$(cd "$W/hors2" && bash i.sh 2>&1)"; [ $? = 2 ] && printf '%s\n' "$o" | grep -qF "hors d'un dépôt"; res I-12 $?
c0; echo "# x" >> "$R/enforcement/hooks/install-pre-commit.sh"; inst 2 "installeur différent" && [ -z "$(ho)" ]; res I-13 $?
c0; e0="$(etat)"; inst 2 "argument inconnu" --verify && [ "$(etat)" = "$e0" ]; res I-14 $?
# Branchement (§7.3) : lint d'épinglage et gate des secrets, pris dans l'index du commit.
A=.claude/agents/shogen-devops.md; B="claude-opus-""5"; V="$(forme V-01)" || fatal "sonde V-01 introuvable"
op() { sed 's/^model: .*/model: opus/' "$FX/shogen-devops.md" > "$R/$A"; }
c1; op && git -C "$R" add -- "$A" && cp "$FX/shogen-devops.md" "$R/$A" && ci 1 HOOK/lint+R-1/tier-nu; res C-01 $?
c1; f docs/y.md propre && op && ci 0 -; res C-02 $?
c1; op && git -C "$R" add -- "$A" && echo 'exit 0' > "$R/enforcement/lint-model-pinning.sh" && ci 1 HOOK/lint; res C-03 $?
c1; f docs/y.md propre && printf '{ "model": "%s" }\n' "$B" > "$R/.claude/settings.local.json" && ci 0 -; res C-04 $?
c1; f s.py "k = \"$V\"" && ci 1 HOOK/secrets+SECRETS/forme; res C-05 $?
c1; f s.py "k = \"$V\"" && echo 'exit 0' > "$R/enforcement/gate-secrets.sh" && ci 1 HOOK/secrets; res C-06 $?
c1; git -C "$R" rm -q --cached enforcement/lint-model-pinning.sh && f docs/y.md propre && ci 1 HOOK/echec && printf '%s\n' "$o" | grep -qF "avancer la base"; res C-07 $?
c1; git -C "$R" rm -q --cached enforcement/gate-secrets.sh && f docs/y.md propre && ci 1 HOOK/echec; res C-08 $?
c1; f docs/x.md "# $M1" && f s.py "k = \"$V\"" && op && git -C "$R" add -- "$A" && ci 1 HOOK/g5+HOOK/lint+HOOK/secrets; res C-09 $?
c1; git -C "$R" worktree add -q -b wt "$R.wt" || fatal worktree; D="$R.wt"; f docs/y.md propre && ci 0 -; res C-10 $?
c1; op && ci 1 HOOK/lint+R-1/tier-nu -a; res C-11 $?
c1; git -C "$R" worktree add -q -b vieux "$R.wt" HEAD~1 || fatal worktree; D="$R.wt"; f docs/y.md propre && ci 1 HOOK/echec &&
  printf '%s\n' "$o" | grep -qF "avancer la base"; res C-12 $?
c1; f .claude/agents/b.md "$(cat "$FX/shogen-devops.md"; echo corps)" && x="$(git -C "$R" ls-files -s -- .claude/agents/b.md | cut -d' ' -f2)" &&
  rm -f "$R/.git/objects/${x:0:2}/${x:2}" && o="$(cd "$R" && bash "$HOOK" < /dev/null 2>&1)"; [ $? = 2 ] &&
  printf '%s\n' "$o" | grep -qF "REFUS (HOOK/echec) : extraction"; res C-13 $?
c1; E="index réécrit ou refus"; x="$(sha "$R/.git/index")"; o="$(cd "$R" && GIT_OPTIONAL_LOCKS=0 bash .git/hooks/pre-commit < /dev/null 2>&1)"; [ $? = 0 ] &&
  printf '%s\n' "$o" | grep -qF "OK (hook)" && [ "$(sha "$R/.git/index")" = "$x" ]; res C-14 $?

echo "hooks : $OK ok, $KO échec"
[ "$KO" -eq 0 ]
