#!/usr/bin/env bash
# Shōgen, lot D8c (ADR-0028 D8) : cas du hook pre-commit versionné, table du §7 du G0
# (docs/adr-0028/G0-lot-D8c.md) : H-01 à H-20 (étape R-13) ; ajoutés au G1 : H-21 (git grep en erreur),
# H-22 (lancement direct depuis un sous-dossier). Installeur et cas I : sous-lot D8c-1b.
# Ajouté à la revue G2 (2026-10-01) : H-23 (git commit --amend, consommateur 1 du G0 §10).
# Dépôt modèle sous mktemp, hors de tout dépôt : git init -b main, identité factice, commit.gpgsign=false,
# core.autocrlf=false ; commit de base avec deux agents valides (fixtures de D8a) et le hook sous test,
# copié dans le dossier des hooks du modèle. Chaque cas travaille sur une copie du modèle, puis git commit
# réel : sortie ET jeton vérifiés. Marqueurs formés à l'exécution ; ce fichier n'en porte aucun, ni les
# octets du hook local. Isolation : refus si une variable GIT_* de dépôt est posée ; ce runner ne pose
# jamais GIT_DIR ni GIT_WORK_TREE.
# Usage : run-fixtures-hooks.sh [hook]   Sortie : 0 tout passe, 1 un cas échoue, 3 erreur fatale.

set -u
fatal() { echo "ERREUR FATALE : $1" >&2; exit 3; }
for v in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR GIT_OBJECT_DIRECTORY; do
  [ -z "${!v+x}" ] || fatal "variable $v posée (isolation, incident du 2026-09-24)"
done
H="$(cd "$(dirname "$0")" && pwd)" || exit 3
HOOK="${1:-$H/../hooks/pre-commit}"
HOOK="$(cd "$(dirname "$HOOK")" && pwd)/$(basename "$HOOK")" || exit 3
GY="$H/../../.github/workflows/gates.yml"; FX="$H/fixtures/model-pinning"
[ -f "$HOOK" ] && [ -f "$GY" ] && [ -f "$FX/shogen-devops.md" ] && [ -f "$FX/shogen-orchestrator.md" ] ||
  fatal "hook, gates.yml ou fixtures introuvables"
W="$(mktemp -d)" || fatal "mktemp -d"
trap 'rm -rf "$W"' EXIT
git -C "$W" rev-parse --is-inside-work-tree >/dev/null 2>&1 && fatal "dossier de travail dans un dépôt"
M1="TO""DO"; M2="FIX""ME"; OK=0; KO=0; K=0; E=; D=
sha() { sha256sum < "$1" | cut -d' ' -f1; }
res() { if [ "$2" = 0 ]; then OK=$((OK + 1)); else KO=$((KO + 1)); echo "ÉCHEC $1${E:+ : $E}" >&2; fi; E=; }
# m0 : commit de base, sans hook ; m1 : m0 puis hook copié. c0, c1 : copies neuves de m0, de m1.
m="$W/m0"; mkdir -p "$m/.claude/agents" "$m/enforcement/hooks" && git -C "$m" init -q -b main || fatal init
for c in user.name=t user.email=t@example.invalid commit.gpgsign=false core.autocrlf=false; do git -C "$m" config "${c%%=*}" "${c#*=}" || fatal config; done
cp "$FX/shogen-devops.md" "$FX/shogen-orchestrator.md" "$m/.claude/agents/" && cp "$HOOK" "$m/enforcement/hooks/pre-commit" &&
  git -C "$m" add -A && git -C "$m" commit -qm base && cp -r "$m" "$W/m1" &&
  cp "$HOOK" "$W/m1/.git/hooks/pre-commit" && chmod 755 "$W/m1/.git/hooks/pre-commit" || fatal "dépôt modèle"
c0() { K=$((K + 1)); R="$W/r$K"; D=; cp -r "$W/m0" "$R" || fatal copie; }
c1() { K=$((K + 1)); R="$W/r$K"; D=; cp -r "$W/m1" "$R" || fatal copie; }
# f chemin texte : écrit le fichier sous ${D:-$R} et l'indexe. ci attendu jeton [arguments] : git commit réel.
f() { p="${D:-$R}/$1"; mkdir -p "${p%/*}" && printf '%s\n' "$2" > "$p" && git -C "${D:-$R}" add -- "$1" || fatal add; }
ci() { a="$1"; j="$2"; shift 2; o="$(cd "${D:-$R}" && git commit -qm c "$@" 2>&1)"; r=$?
  [ "$a" = 0 ] && e="OK (hook)" || e="REFUS ($j)"
  [ "$r" = "$a" ] && printf '%s\n' "$o" | grep -qF "$e" && return 0
  E="commit : attendu $a, $e ; obtenu $r, $(printf '%s\n' "$o" | grep -m1 -E 'REFUS|OK|fatal|error')"; return 1; }
# pr message : commit de préparation dans $R, sortie tue ; un refus fait échouer le cas.
pr() { git -C "$R" commit -qm "$1" >/dev/null 2>&1 || { E="commit de préparation refusé"; return 1; }; }

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
c0; f docs/v.md "# $M1 ancien"; pr v && cp "$HOOK" "$R/.git/hooks/pre-commit" && f docs/y.md propre && ci 1 HOOK/g5; res H-12 $?
c1; f docs/x.md "# $M1"; echo propre > "$R/docs/x.md"; ci 1 HOOK/g5; res H-13 $?
c1; f docs/w.md propre; pr w && echo "# $M1" >> "$R/docs/w.md" && echo "# $M1" > "$R/docs/z.md" && f docs/y.md propre && ci 0 -; res H-14 $?
c1; mkdir -p "$R/docs" && printf 'a\000b\n# %s\n' "$M1" > "$R/docs/b.bin" && git -C "$R" add docs/b.bin && ci 1 HOOK/g5; res H-15 $?
c1; f docs/w.md propre; pr w && echo "# $M1" >> "$R/docs/w.md" && ci 1 HOOK/g5 -a; res H-16 $?
c1; f docs/w.md propre; pr w && echo "# $M1" >> "$R/docs/w.md" && ci 1 HOOK/g5 -- docs/w.md; res H-17 $?
c1; git -C "$R" worktree add -q -b wt "$R.wt" || fatal worktree; D="$R.wt"; f docs/x.md "# $M1"; ci 1 HOOK/g5 && f docs/x.md propre && ci 0 -; res H-18 $?
mkdir "$W/hors" || fatal hors; o="$(cd "$W/hors" && bash "$HOOK" < /dev/null 2>&1)"; [ $? = 2 ] && printf '%s\n' "$o" | grep -qF "REFUS (HOOK/echec)"; res H-19 $?
g="$(sed -n "s/^ *if git grep -nE '\([^']*\)' \(-- [^;]*\); then\$/\1 \2/p" "$GY")"
k="$(sed -n "s/^M='\([^']*\)'\$/\1/p" "$HOOK") $(sed -n 's/^O="$(git grep --cached -nE "$M" \(-- [^)]*\))"; g=$?$/\1/p' "$HOOK")"
E="motif ou exclusions différents du job g5"; [ -n "$g" ] && [ "$g" = "$k" ]; res H-20 $?
c1; : > "$R/.git/index"; o="$(cd "$R" && bash "$HOOK" < /dev/null 2>&1)"; [ $? = 2 ] && printf '%s\n' "$o" | grep -qF "REFUS (HOOK/echec) : git grep"; res H-21 $?
c1; f docs/x.md "# $M1" && f sub/a.txt propre && o="$(cd "$R/sub" && bash "$HOOK" < /dev/null 2>&1)"; [ $? = 2 ] && printf '%s\n' "$o" | grep -qF "REFUS (HOOK/g5)"; res H-22 $?
c1; f docs/w.md propre; pr w && echo "# $M1" >> "$R/docs/w.md" && git -C "$R" add docs/w.md && ci 1 HOOK/g5 --amend; res H-23 $?
echo "hooks : $OK ok, $KO échec"
[ "$KO" -eq 0 ]
