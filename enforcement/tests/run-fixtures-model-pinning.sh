#!/usr/bin/env bash
# Shōgen, lot D8a (ADR-0028 D8, C-14) : cas du lint d'épinglage des modèles, table du §7
# du G0 (docs/adr-0028/G0-lot-D8a.md), puis cas de la revue G2 (T-46 à T-76, journal G1
# §15). Écrit d'après la table du G0 §7 et les traits du runner amont relevés au G0 §5.1
# (blob d9ad850, non relu au G1 : E-7) ; les deux cas propres hors roster de l'amont sont
# ici inversés, donc refusés (T-14, T-15).
# Fixtures : fixtures/model-pinning/, copies octet pour octet des frontmatters de
# .claude/agents/ à fb089dc (shogen-devops.md l.1-13, shogen-orchestrator.md l.1-15 ;
# sha256 au journal G1). Chaque cas bâtit un arbre sous mktemp, hors du dépôt, jamais sous
# un .claude/agents/ du dépôt, que Claude Code chargerait comme agent. B, l'identifiant
# banni, est construit à l'exécution. Chaque cas vérifie la sortie ET le jeton ; un cas
# « 0 » exige le message OK et son compte de fichiers. Un seul résumé fait foi.
# Lot D8c (ADR-0028 D8) : cas T-77 à T-92, table du G0 de D8c §7.4 (docs/adr-0028/G0-lot-D8c.md) ; T-93 à T-95 (revue G2).
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
# ins n ligne : insère la ligne, telle quelle (ENVIRON : sans échappements d'awk), après la
# ligne n de $A. md chemin ligne... : frontmatter sous $T. vers chemin : déplace $A sous $T,
# puis remet en $A la fixture D telle quelle.
ins() { L="$2" awk -v n="$1" '{ print } NR == n { print ENVIRON["L"] }' "$A" > "$T/x" && mv "$T/x" "$A"; }
md() { m="$T/$1"; shift; mkdir -p "${m%/*}" && printf '%s\n' '---' "$@" '---' > "$m" || exit 3; }
vers() { mkdir -p "$T/${1%/*}" && mv "$A" "$T/$1" && cp "$FX/shogen-devops.md" "$A" || exit 3; }
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
arbre D 'model: claude-opus-5-5[1m]'; cas T-13 2 R-1/suffixe
arbre D 'model: claude-sonnet-5'; cas T-14 2 R-1/retire R-1/ban
arbre D 'model: claude-opus-4-8'; cas T-15 2 R-1/hors-liste
arbre D "model: $(printf '%s' "$B" | tr '[:lower:]' '[:upper:]')"; cas T-16 2 R-1/ban
arbre D 'model: CLAUDE-OPUS-5-5'; cas T-17 2 R-1/hors-liste
arbre D 'model: fable   # ADR-0003'; cas T-18 2 R-1/tier-nu
arbre D "model: $B   # ADR-9999"; cas T-19 2 R-1/ban
arbre D; echo '{ "advisorModel": "fable" }' > "$T/.claude/settings.json"
echo 'advisorModel=fable ADR-0003' > "$T/.claude/model-exceptions.txt"; cas T-20 2 R-1/tier-nu
arbre D @SANS@; cas T-21 2 R-1/cle-model
arbre D @DEUX@; cas T-22 2 R-1/cle-model
arbre O; ins 4 '  model: claude-opus-5-5'; cas T-23 0 1
arbre O; ins 4 "  model: $B"; cas T-24 2 R-1/ban
arbre O; printf '%s\n' 'corps' "model: $B" >> "$A"; cas T-25 0 1
arbre -; cas T-26 2 R-1/vide
arbre D; { printf '\357\273\277'; cat "$FX/shogen-devops.md"; } > "$A"; cas T-27 0 1
arbre D "model: $B"; { printf '\357\273\277'; cat "$A"; } > "$T/x" && mv "$T/x" "$A"; cas T-28 2 R-1/ban
# Normalisation (CH-8), skills (CH-12), réglages JSON (CH-10), fil de workflow (CH-9).
arbre D 'model: "claude-opus-5-5"'; cas T-29 0 1
arbre O "model: 'claude-fable-5-1'"; cas T-30 0 1
arbre D "model: \"claude-opus-5-5'"; cas T-31 2 R-1/hors-liste
arbre D 'model: claude-opus-5-5  # note'; cas T-32 0 1
arbre D 'model: claude-opus-5-5#x'; cas T-33 2 R-1/hors-liste
arbre D 'model : claude-opus-5-5'; cas T-34 0 1
arbre D; sed 's/$/\r/' "$FX/shogen-devops.md" > "$A"; cas T-35 0 1
arbre D 'model:'; cas T-36 2 R-1/hors-liste
arbre D; mkdir -p "$T/.claude/skills/s"; printf '%s\n' '---' 'name: s' "model: $B" '---' > "$T/.claude/skills/s/SKILL.md"; cas T-37 2 R-1/ban
arbre D; echo '{ "advisorModel": "claude-fable-5-1" }' > "$T/.claude/settings.json"; cas T-38 0 2
arbre D; echo "{ \"model\": \"$B\" }" > "$T/.claude/settings.json"; cas T-39 2 R-1/ban
arbre D; echo "{ \"model\": \"$B\" }" > "$T/.claude/settings.local.json"; cas T-40 2 R-1/ban
arbre D; printf '{\n  "model":\n    "%s"\n}\n' "$B" > "$T/.claude/settings.json"; cas T-41 2 R-1/ban
arbre D; echo '{ "model": "claude-opus-5-5[1m]" }' > "$T/.claude/settings.json"; cas T-42 2 R-1/suffixe
arbre D; echo "await agent('p', {model: 'claude-opus-5-5'})" > "$T/wf.mjs"; cas T-43 2 R-1/workflow
arbre D; echo 'const u = useragent(1); x.agent(2)' > "$T/x.js"; cas T-44 0 1
arbre D; echo '{ "model": null }' > "$T/.claude/settings.json"; cas T-45 2 R-1/hors-liste
# Revue G2 (2026-09-30) : C-5 (T-46 à T-50), C-1 (T-51, T-52, T-63, T-64), C-2 (T-53, T-54),
# C-3 (T-55 à T-59, T-62), C-4 (T-60), C-6 (T-61) ; C-3 (a) élargi et ses gardes (T-65 à
# T-74) ; C-1 hors de la racine (T-75, T-76).
arbre D 'model: inherit'; cas T-46 2 R-1/tier-nu
arbre D 'model: claude-fable-5'; cas T-47 2 R-1/hors-liste
arbre D 'model: haiku'; cas T-48 2 R-1/tier-nu
arbre D; echo "await agent('p', {model: 'claude-opus-5-5'})" > "$T/wf.js"; cas T-49 2 R-1/workflow
arbre D "model: $B"; vers .claude/agents/team/b.md; cas T-50 2 R-1/ban
arbre D 'model: opus'; vers sub/.claude/agents/b.md; cas T-51 2 R-1/tier-nu
arbre D 'model: opus'; vers .claude/worktrees/w/.claude/agents/b.md; cas T-52 0 1
arbre D; md .claude/skills/s/SKILL.md 'name: s' 'description: x'; cas T-53 0 2
arbre D; md .claude/skills/s/SKILL.md 'name: s' 'model: claude-sonnet-5-5'; echo '# ref' > "$T/.claude/skills/s/reference.md"; cas T-54 0 3
arbre D; ins 10 '"model": opus'; cas T-55 2 R-1/cle-model
arbre D; ins 10 '? model'; ins 11 ': opus'; cas T-56 2 R-1/cle-model
arbre D; ins 10 '  [1m]'; cas T-57 2 R-1/hors-liste
arbre D 'model:claude-opus-5-5'; cas T-58 2 R-1/cle-model
arbre D; sed -i '$d' "$A"; cas T-59 2 R-1/cle-model
arbre D; printf '%s\n' '{ "mod\u0065l": "opus" }' > "$T/.claude/settings.json"; cas T-60 2 R-1/hors-liste
arbre -; echo '{}' > "$T/.claude/settings.json"; cas T-61 2 R-1/vide
arbre D; ins 10 '"mod\x65l": opus'; cas T-62 2 R-1/cle-model
arbre D; md .claude/commands/c.md 'description: c' "model: $B"; cas T-63 2 R-1/ban
arbre D; md .claude/commands/c.md 'description: c'; cas T-64 0 2
arbre D; ins 10 '&a model: opus'; cas T-65 2 R-1/cle-model
arbre D; ins 10 '!!str model: opus'; cas T-66 2 R-1/cle-model
arbre D; ins 10 'k: &k model'; ins 11 '*k : opus'; cas T-67 2 R-1/cle-model
arbre D; md .claude/skills/s/SKILL.md 'name: s' '<<: {model: opus}'; cas T-68 2 R-1/cle-model
arbre D; md .claude/skills/s/SKILL.md '{name: s, model: opus}'; cas T-69 2 R-1/cle-model
arbre D; ins 10 '  # note'; cas T-70 0 1
arbre D; md .claude/skills/s/SKILL.md 'name: s' 'allowed-tools:' '- Read' '- "Bash(git:*)"' 'description:' '|' '  x' 'metadata:' '  "k": [x]'; cas T-71 0 2
arbre D; ins 10 ''; ins 11 '  [1m]'; cas T-72 2 R-1/hors-liste
arbre D; ins 10 "'model': opus"; cas T-73 2 R-1/cle-model
arbre D; md .claude/skills/s/SKILL.md '# c' '  name: s' '  "model": opus'; cas T-74 2 R-1/cle-model
arbre D; md sub/.claude/skills/s/SKILL.md 'name: s' "model: $B"; cas T-75 2 R-1/ban
arbre D; md sub/.claude/commands/c.md 'description: c' 'model: opus'; cas T-76 2 R-1/tier-nu
# Lot D8c (2026-09-30, G0 de D8c §7.4) : formes imbriquées, CH-12 (T-77 à T-84, T-92) ; lecture JSON à
# jetons et garde de résidu, CH-13 (T-85 à T-91). Barres obliques inverses écrites en octal par printf.
arbre D; ins 12 'hooks:'; ins 13 '  Stop:'; ins 14 '    - model: opus'; cas T-77 2 R-1/tier-nu
arbre D; ins 12 'hooks:'; ins 13 '  Stop:'; ins 14 '    - model: claude-opus-5-5'; cas T-78 0 1
arbre D; ins 12 'hooks: {Stop: [{type: prompt, model: opus}]}'; cas T-79 2 R-1/cle-model
arbre D; ins 12 'hooks:'; ins 13 '  s:'; ins 14 '    "model": opus'; cas T-80 2 R-1/cle-model
arbre D; ins 12 'hooks:'; ins 13 '  - {model: opus}'; cas T-81 2 R-1/cle-model
arbre D; ins 12 'hooks:'; ins 13 '  s:'; ins 14 '    model: claude-opus-5-5'; ins 15 '      x'; cas T-82 2 R-1/hors-liste
arbre D; ins 12 'hooks:'; ins 13 '  s:'; ins 14 '    model: claude-opus-5-5'; ins 15 '    # c'; ins 16 '      x'; cas T-83 2 R-1/hors-liste
arbre D; ins 9 '  choisir le model: opus pour ce cas.'; cas T-84 0 1
arbre D; printf '{"permissions": {"allow": ["Bash(python -c \134"d={\134\134\134"a\134\134\134": 1}\134")"]}, "advisorModel": "claude-fable-5-1"}\n' > "$T/.claude/settings.local.json"; cas T-85 0 2
arbre D; printf '{ "mod\134u0065l": "opus" }\n' > "$T/.claude/settings.local.json"; cas T-86 2 R-1/hors-liste
arbre D; printf '{ "advisorModel": "claude-fable-5-1", // note\n "model": "opus" }\n' > "$T/.claude/settings.local.json"; cas T-87 2 R-1/hors-liste
arbre D; printf '{ "advisorModel": "claude-fable-5-1", // it"s\n "model": "opus" }\n' > "$T/.claude/settings.local.json"; cas T-88 2 R-1/hors-liste
arbre D; printf '{ model: "opus", "advisorModel": "claude-fable-5-1" }\n' > "$T/.claude/settings.local.json"; cas T-89 2 R-1/hors-liste
arbre D; printf '{ "a": "x\134"y", "advisorModel": "claude-fable-5-1" }\n' > "$T/.claude/settings.local.json"; cas T-90 0 2
arbre D; printf '{ "advisorModel": "claude-fable-5-1", }\n' > "$T/.claude/settings.local.json"; cas T-91 0 2
arbre D; ins 10 '# c'; ins 11 '  x'; cas T-92 2 R-1/hors-liste
arbre D; ins 12 'hooks: [model: opus]'; cas T-93 2 R-1/cle-model
arbre D; ins 12 'hooks: {Stop: [model: opus]}'; cas T-94 2 R-1/cle-model
arbre D; ins 12 'hooks:'; ins 13 '  Stop:'; ins 14 '    - model: claude-opus-5-5'; ins 15 '      type: prompt'; cas T-95 0 1

echo "model-pinning : $OK ok, $KO échec"
[ "$KO" -eq 0 ]
