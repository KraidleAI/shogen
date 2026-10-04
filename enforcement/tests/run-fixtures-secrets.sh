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
# Lot D8d (2026-10-04, lot DETTES-B2) : cas ajoutés et révisés sous des commentaires de bloc datés.
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
# r [-] : dépôt jetable neuf $R (isolé, sans crochets, sans signature), commit initial base.txt (sauf avec -).
r() {
  K=$((K + 1)); R="$W/r$K"; mkdir "$R" && git -C "$R" init -q -b main || fatal "init"
  [ -z "$(git -C "$R" rev-parse --show-prefix)" ] || fatal "préfixe non vide"
  for c in user.name=t user.email=t@example.invalid commit.gpgsign=false core.autocrlf=false "core.hooksPath=$W/nh"; do
    git -C "$R" config "${c%%=*}" "${c#*=}" || fatal "config"
  done
  [ "${1-}" = - ] || { echo base > "$R/base.txt"; ci init; }
}
ci() { git -C "$R" add -A && git -C "$R" commit -q -m "$1" || fatal "commit"; }
st() { git -C "$R" add -- "$@" || fatal "add"; }
# cas ID sortie jeton|fin-du-message-OK [requis] [interdit] : gate lancée depuis ${D:-$R}, arguments $A, PATH ${P:-$PATH}.
cas() {
  o="$(cd "${D:-$R}" && PATH="${P:-$PATH}" bash "$GATE" $A 2>&1)"; c=$?
  if [ "$2" = 0 ]; then e="OK (secrets) : $3"; else e="REFUS ($3)"; fi
  if [ "$c" = "$2" ] && printf '%s\n' "$o" | grep -qF -- "$e" && { [ -z "${4-}" ] || printf '%s\n' "$o" | grep -qE -- "$4"; } &&
     { [ -z "${5-}" ] || ! printf '%s\n' "$o" | grep -qE -- "$5"; }; then OK=$((OK + 1))
  else KO=$((KO + 1)); echo "ÉCHEC $1 : attendu $2 $3, obtenu $c" >&2; printf '%s\n' "$o" | head -3 >&2; fi
  D=; A=; P=
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
# Bornes, mode indexé, contrat d'exclusion (T-15 à T-30, T-68). Le fichier d'exclusion est suivi (ajouté à l'index)
# sauf en T-25 : dans l'amont, les cas 12 et 13 le laissaient non suivi et touchaient la branche « non suivi ».
r; printf 'k = "%s"\n' "$V" > "$R/l.py"; st l.py; TMPDIR="$W/absent" cas T-15 2 SECRETS/echec 'mktemp a échoué'
r; for i in 1 2 3 4 5 6 7 8 9 10 11 12; do printf '%s\n' "$G"; done > "$R/n.py"; st n.py; cas T-16 2 SECRETS/forme '\(\+4 ligne\(s\) non listée'
r; printf 'k = "%s"\n2\n3\n4\n5\n' "$V" > "$R/m.py"; ci m; printf 'k = "%s"\n2\n3\n4\ncinq\n' "$V" > "$R/m.py"; st m.py
cas T-17 2 SECRETS/forme '^m\.py:1: '
r; printf 'k = "%s"\n' "$V" > "$R/d.py"; ci d; git -C "$R" rm -q d.py || fatal rm; cas T-18 0 '0 fichier(s)'
r; forme G-09 > "$R/.env.example"; st .env.example; cas T-19 2 SECRETS/forme
ex() { printf '%s\n' "$1" > "$R/.vibegates-secretscan-exclude"; [ "${2-}" = - ] || st .vibegates-secretscan-exclude; }
r; printf 'k = "%s"\n' "$V" > "$R/l.py"; st l.py; ex '../out  # ADR-0001'; cas T-20 2 SECRETS/exclusion
ex 'fx/'; cas T-21 2 SECRETS/exclusion 'sans marqueur ADR-'
mkdir "$R/fx"; git -C "$R" mv l.py fx/l.py || fatal mv; ex 'fx/  # ADR-0001 fixtures'; cas T-22 0 '1 fichier(s)'
r; mkdir -p "$R/enforcement/tests" "$R/enforcementX"; printf 'k = "%s"\n' "$V" | tee "$R/enforcement/tests/f.py" > "$R/enforcementX/c.py"
st enforcement/tests/f.py; cas T-23 0 '0 fichier(s)' 'exclus par contrat'; st enforcementX/c.py; cas T-24 2 SECRETS/forme
r; printf 'k = "%s"\n' "$V" > "$R/l.py"; st l.py; ex 'fx/  # ADR-0001' -; cas T-25 2 SECRETS/exclusion 'sans être suivi'
r; printf 'k = "%s"\n' "$V" > "$R/l.py"; st l.py; ex '.  # ADR-0001 global'; cas T-26 2 SECRETS/exclusion 'pathspec global'
r; mkdir "$R/fx"; printf 'k = "%s"\n' "$V" > "$R/fx/l.py"; st fx/l.py; ex 'fx/  # ADR-0001 fixtures'
cas T-27 0 '1 fichier(s)' "l'exclusion 'fx/' retire 1 fichier\(s\) suivi"
r; printf 'k = "%s"\n' "$V" > "$R/l.py"; st l.py; ex './/  # ADR-0001'; cas T-28 2 SECRETS/exclusion 'pathspec global'
r; mkdir -p "$R/enforcement/policies"; printf 'k = "%s"\n' "$V" > "$R/enforcement/policies/p.py"; st enforcement; cas T-29 2 SECRETS/forme
r; mkdir "$R/fx"; printf 'k = "%s"\n' "$V" > "$R/fx/l.py"; st fx/l.py; ex 'fx/../fx/  # ADR-0001'; cas T-30a 2 SECRETS/exclusion traversant
ex '?*  # ADR-0001'; cas T-30b 2 SECRETS/exclusion 'toute la portée'; ex '/abs  # ADR-0001'; cas T-68 2 SECRETS/exclusion inutilisable
# Revue G2, chemins et objets : glob (T-71, T-71b), blob remplacé (T-72), nom masqué (T-77, T-79, T-80), casse des pathspecs (T-78).
r; b="$(printf 'k = "%s"\n' "$V" | git -C "$R" hash-object -w --stdin)" && l="$(printf 'c' | git -C "$R" hash-object -w --stdin)" || fatal objets
git -C "$R" update-index --add --cacheinfo "100644,$b,[A]x.py" --cacheinfo "120000,$l,Ax.py" || fatal index
cas T-71 2 SECRETS/forme '^\[A\]x\.py:1: '; A=--tree; cas T-71b 2 SECRETS/forme '^\[A\]x\.py:1: '
r; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci c; p="$(printf 'x' | git -C "$R" hash-object -w --stdin)" && git -C "$R" replace -f "$(git -C "$R" rev-parse HEAD:c.py)" "$p" || fatal replace
A=--tree; cas T-72 2 SECRETS/forme '^c\.py:1: '
r; printf 'k = "%s"\n' "$V" > "$R/$V.txt"; st "$V.txt"; cas T-77 2 SECRETS/forme '^\[forme masquée\];\.txt:1: ' QQQQ
r; b="$(printf 'k = "%s"\n' "$V" | git -C "$R" hash-object -w --stdin)" && git -C "$R" update-index --add --cacheinfo "100644,$b,Enforcement/Tests/x.py" || fatal index
A=--tree; GIT_ICASE_PATHSPECS=1 cas T-78 2 SECRETS/forme '^Enforcement/Tests/x\.py:1: '
r; l="$(printf 'c' | git -C "$R" hash-object -w --stdin)" && git -C "$R" update-index --add --cacheinfo "120000,$l,$V.lnk" || fatal lien; cas T-79 2 SECRETS/forme "'\[forme masquée\];\.lnk' ignoré" QQQQ
r; n="$(forme G-09)" || fatal "sonde G-09"; printf 'k = "%s"\n' "$V" > "$R/$n.txt"; st "$n.txt"; cas T-80 2 SECRETS/forme '^\[forme masquée\];\.txt:1: ' QQQQ
# Lot D8d (2026-10-04) : chemin d'étage (T-81, T-81b) ; grep en erreur (T-82, T-82b, T-83 : enveloppe de PATH posée pour la
# seule gate, sortie 2 sur l'appel VENDOR -anE ou GENERIC -aniE d'un fichier marqué ECHEC-GREP, grep réel sinon) ; messages
# masqués du contrat d'exclusion, des greffes et de git show (T-84 à T-90) ; noms de chemin (T-91 à T-93 ; T-79 en refus).
r; echo propre > "$R/x"; printf 'k = "%s"\n' "$V" > "$R/0:x"; st x 0:x; cas T-81 2 SECRETS/forme '^0:x:1: '; A=--tree; cas T-81b 2 SECRETS/forme '^0:x:1: '
G0="$(command -v grep)" || fatal "grep introuvable"
gr() { mkdir "$W/$1" && printf '#!/bin/sh\nfor a; do f="$a"; done\n[ "$1" = %s ] && [ -f "$f" ] && "%s" -q ECHEC-GREP "$f" && exit 2\nexec "%s" "$@"\n' \
  "$2" "$G0" "$G0" > "$W/$1/grep" && chmod +x "$W/$1/grep" || fatal "enveloppe grep"; }
gr gv -anE; gr gg -aniE
r; printf 'k = "%s" # ECHEC-GREP\n' "$V" > "$R/s.py"; st s.py; P="$W/gv:$PATH"; cas T-82 2 SECRETS/echec 'grep a échoué \(contenu\)'
r; echo x > "$R/ECHEC-GREP.txt"; st ECHEC-GREP.txt; P="$W/gg:$PATH"; cas T-82b 2 SECRETS/echec 'grep a échoué \(noms de chemin\)'
r; printf 'k = "%s" # ECHEC-GREP\n' "$V" > "$R/c.py"; ci c; P="$W/gg:$PATH"; A=--history; cas T-83 2 SECRETS/echec 'grep a échoué \(historique\)'
r; echo x > "$R/l.py"; st l.py; ex "$V"; cas T-84 2 SECRETS/exclusion 'sans marqueur ADR-' QQQQ
ex "$V/../x  # ADR-0001"; cas T-85 2 SECRETS/exclusion traversant QQQQ; ex "/$V  # ADR-0001"; cas T-86 2 SECRETS/exclusion inutilisable QQQQ
ex "$V/  # ADR-0001"; cas T-87 2 SECRETS/forme "l'exclusion '\[forme masquée\];/' retire" QQQQ
r -; echo x > "$R/$V.txt"; st "$V.txt"; ex "[$V.]*  # ADR-0001"; cas T-88 2 SECRETS/exclusion 'toute la portée' QQQQ
r; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci a; git -C "$R" rm -q c.py || fatal rm; ci r; g="$W/$V-greffes"
printf '%s %s\n' "$(git -C "$R" rev-parse HEAD)" "$(git -C "$R" rev-parse HEAD~2)" > "$g" || fatal greffe; A=--history; GIT_GRAFT_FILE="$g" cas T-89 2 SECRETS/tronque greffes QQQQ
r; echo x > "$R/$V.txt"; st "$V.txt"; b="$(git -C "$R" ls-files -s -- "$V.txt" | cut -d' ' -f2)" && rm -f "$R/.git/objects/${b:0:2}/${b:2}" || fatal objet
cas T-90 2 SECRETS/echec 'git show a échoué' QQQQ
r; echo x > "$R/$V.txt"; st "$V.txt"; cas T-91 2 SECRETS/forme '^\[forme masquée\];\.txt:\(chemin\)$' QQQQ; A=--tree; cas T-91b 2 SECRETS/forme '^\[forme masquée\];\.txt:\(chemin\)$' QQQQ
r; n="$(forme G-09)" || fatal "sonde G-09"; echo x > "$R/$n.txt"; st "$n.txt"; cas T-92 2 SECRETS/forme '^\[forme masquée\];\.txt:\(chemin\)$' QQQQ
r; printf 'k = "%s"\n' "$V" > "$R/$V.txt"; st "$V.txt"; cas T-93 2 SECRETS/forme "contenu en forme d'identifiant" QQQQ
# Table des sondes (T-31 : VENDOR, par alternative ; T-32 : GENERIC, par forme ; T-33 à T-35 : seuils ajoutés au G1).
for id in $(awk -F '\t' '!/^#/ { print $1 }' "$FX"); do
  case "$id" in V-*) l="T-31/$id" ;; G-*) l="T-32/$id" ;; *) l="$id" ;; esac
  r; forme "$id" > "$R/p.txt" || fatal "sonde $id"; st p.txt
  if [ "$(awk -F '\t' -v i="$id" '$1 == i { print $7 }' "$FX")" = 0 ]; then cas "$l" 0 '1 fichier(s)'; else cas "$l" 2 SECRETS/forme; fi
done
# Mode --history (T-51 à T-67, T-69, T-70 ; revue G2 : T-73 à T-76, T-74b ; re-revue : T-75b) ; h : les 12 premiers caractères du commit courant.
h() { git -C "$R" rev-parse --short=12 HEAD; }
r; printf 'k = "%s"\n' "$V" | tr A-Z a-z > "$R/c.py"; ci c; A=--history; cas T-51 0 'historique, 2 commit(s)'
r; printf 'l1\nk = "%s"\n' "$V" > "$R/résumé.py"; ci ajout; c1=$(h); git -C "$R" rm -q résumé.py || fatal rm; ci retrait
A=--tree; cas T-52a 0 '1 fichier(s)'; A=--history; cas T-52 2 SECRETS/historique "^$c1:résumé\.py:2\$" QQQQ
r; printf 'a\n\nc\nd\ne\n' > "$R/f.txt"; ci cinq; { printf 'a\n\nc\n'; printf '%s\n' "$G" | tr a-z A-Z; echo e; } > "$R/f.txt"; ci modif
A=--history; cas T-53 2 SECRETS/historique "^$(h):f\.txt:4\$"
r; git -C "$R" checkout -q -b cote; echo x > "$R/d.txt"; ci cote; git -C "$R" checkout -q main; echo m > "$R/e.txt"; ci m
git -C "$R" merge -q --no-ff --no-commit cote >/dev/null 2>&1; forme G-09 > "$R/f.env"; ci fusion; A=--history; cas T-54 2 SECRETS/historique
r; git -C "$R" checkout -q -b lat; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci a; git -C "$R" rm -q c.py || fatal rm; ci r
git -C "$R" checkout -q main; echo m > "$R/e.txt"; ci m; git -C "$R" merge -q --no-ff -m fus lat >/dev/null 2>&1 || fatal fusion
git -C "$R" branch -q -D lat || fatal branche; A=--history; cas T-55 2 SECRETS/historique
r -; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci racine; git -C "$R" rm -q c.py || fatal rm; ci retrait; git -C "$R" config log.showRoot false
A=--history; cas T-56 2 SECRETS/historique
r; printf '*.bin -diff\n' > "$R/.gitattributes"; printf 'x\000y %s\n' "$V" > "$R/g.bin"; ci bin; A=--history; cas T-57 2 SECRETS/historique
r; printf '*.txt diff=cache\n' > "$R/.gitattributes"; git -C "$R" config diff.cache.textconv 'sed d'; printf 'k = "%s"\n' "$V" > "$R/h.txt"; ci tc
A=--history; cas T-58 2 SECRETS/historique
r; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci ajout; git -C "$R" rm -q c.py || fatal rm; ci retrait
git -C "$W" clone -q --no-local --depth 1 "$R" sup 2>/dev/null && [ "$(git -C "$W/sup" rev-parse --is-shallow-repository)" = true ] ||
  fatal "clone superficiel (C-7)"
D="$W/sup"; A=--history; cas T-59 2 SECRETS/tronque
r; printf '%s\n' '++i;' '++ b/HIJACK.txt' "$G" > "$R/f.c"; ci f; A=--history; cas T-60 2 SECRETS/historique "^$(h):f\.c:3\$" HIJACK
r; printf 'k = "%s"\n' "$V" | iconv -f UTF-8 -t UTF-16LE > "$R/w.ps1" || fatal iconv; ci u; git -C "$R" rm -q w.ps1 || fatal rm; ci rm
A=--history; cas T-61 2 SECRETS/historique
r; mkdir -p "$R/enforcement/tests"; printf 'k = "%s"\n' "$V" > "$R/enforcement/tests/x.py"; ci t; A=--history; cas T-62a 0 'historique, 2 commit(s)'
mkdir "$R/enforcementX"; git -C "$R" mv enforcement/tests/x.py enforcementX/x.py || fatal mv; ci x; A=--history; cas T-62b 2 SECRETS/historique
r; git -C "$R" checkout -q -b cote; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci c; git -C "$R" checkout -q main; A=--history; cas T-63 2 SECRETS/historique
r; git -C "$R" notes add -m '+ligne' -m 'commit 0000' HEAD || fatal notes; A=--history; cas T-64a 0 'historique, 2 commit(s)'
r; printf 'l1\nk = "%s"\n' "$V" > "$R/résumé.py"; ci ajout; c1=$(h); git -C "$R" notes add -m '+ligne' -m 'commit 0000' HEAD || fatal notes
git -C "$R" rm -q résumé.py || fatal rm; ci retrait; A=--history; cas T-64b 2 SECRETS/historique "^$c1:résumé\.py:2\$"
r; for c in color.ui=always diff.noprefix=true diff.suppressBlankEmpty=true core.quotePath=true diff.mnemonicPrefix=true diff.dstPrefix=zz/; do
  git -C "$R" config "${c%%=*}" "${c#*=}" || fatal config; done
mkdir "$R/b"; printf 'l1\nk = "%s"\n' "$V" > "$R/b/résumé.py"; ci ajout; c1=$(h); git -C "$R" rm -q b/résumé.py || fatal rm; ci retrait
A=--history; cas T-65 2 SECRETS/historique "^$c1:b/résumé\.py:2\$"
r; for i in $(seq 1 25); do printf '%s\n' "$G"; done > "$R/g.py"; ci g; c1=$(h)
A=--history; cas T-66 2 SECRETS/historique ': 25 ligne\(s\) ajoutée' ':g\.py:21$'; A=--history; cas T-66b 2 SECRETS/historique "^$c1:g\.py:20\$"
r; mkdir "$R/fx"; printf 'k = "%s"\n' "$V" > "$R/fx/l.py"; printf 'fx/  # ADR-0001 fixtures\n' > "$R/.vibegates-secretscan-exclude"; ci fx
A=--history; cas T-67 0 'historique, 2 commit(s)' "l'exclusion 'fx/' retire 1 fichier"
r; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci c; b="$(git -C "$R" rev-parse HEAD:c.py)" && rm -f "$R/.git/objects/${b:0:2}/${b:2}" || fatal objet
A=--history; cas T-69 2 SECRETS/echec 'erreur git \(historique\)'
r; git -C "$R" config diff.suppressBlankEmpty true; printf 'a\n\nc\nd\ne\n' > "$R/f.txt"; ci cinq
{ printf 'a\n\nc\n'; printf '%s\n' "$G"; echo e; } > "$R/f.txt"; ci modif; A=--history; cas T-70 2 SECRETS/historique "^$(h):f\.txt:4\$"
r; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci a; c1=$(h); git -C "$R" rm -q c.py || fatal rm; ci r
p="$(git -C "$R" commit-tree 'HEAD~2^{tree}' -p HEAD~2 -m p)" && git -C "$R" replace "$(git -C "$R" rev-parse HEAD~1)" "$p" || fatal replace
A=--history; cas T-73 2 SECRETS/historique "^$c1:c\.py:1\$"
r; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci a; git -C "$R" rm -q c.py || fatal rm; ci r
mkdir -p "$R/.git/info" && printf '%s %s\n' "$(git -C "$R" rev-parse HEAD)" "$(git -C "$R" rev-parse HEAD~2)" > "$R/.git/info/grafts" || fatal greffe; A=--history; cas T-74 2 SECRETS/tronque greffes
r; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci a; git -C "$R" rm -q c.py || fatal rm; ci r; g="$W/greffes-$K"
printf '%s %s\n' "$(git -C "$R" rev-parse HEAD)" "$(git -C "$R" rev-parse HEAD~2)" > "$g" || fatal greffe; A=--history; GIT_GRAFT_FILE="$g" cas T-74b 2 SECRETS/tronque greffes
r; git -C "$R" tag tb "$(printf 'k = "%s"\n' "$V" | git -C "$R" hash-object -w --stdin)" || fatal tag; A=--history; cas T-75 2 SECRETS/historique '^refs/tags/tb:\(objet\)$' QQQQ
r; echo x > "$R/$V.txt"; ci nom; git -C "$R" rm -q -- "$V.txt" || fatal rm; ci r
A=--history; cas T-76 2 SECRETS/historique ':\[forme masquée\];\.txt:\(chemin\)$' QQQQ
r; git -C "$R" tag -a ta -m t || fatal tag; A=--history; cas T-75b 0 'historique, 1 commit(s)'
# Lot D8d (2026-10-04) : refs vers un blob ou un arbre balayées au lieu du refus (T-75 en refus d'historique, T-75c, T-75d,
# T-75e : exclusion du contrat dans l'arbre) ; messages de commit et de tag annoté (T-94 à T-96) ; objets hors refs (T-97 à
# T-99, T-101 : --hors-refs) ; bundle de custodie, cloné puis balayé par --history (T-100).
r; git -C "$R" tag tc "$(printf 'propre\n' | git -C "$R" hash-object -w --stdin)" || fatal tag; A=--history; cas T-75c 0 'historique, 1 commit(s)'
r; b="$(printf 'k = "%s"\n' "$V" | git -C "$R" hash-object -w --stdin)" && s="$(printf '100644 blob %s\tx.py\n' "$b" | git -C "$R" mktree)" &&
  s="$(printf '040000 tree %s\ttests\n' "$s" | git -C "$R" mktree)" && s="$(printf '040000 tree %s\tenforcement\n' "$s" | git -C "$R" mktree)" &&
  git -C "$R" update-ref refs/arbres/e "$s" || fatal arbre; A=--history; cas T-75e 0 'historique, 1 commit(s)'
t="$(printf '100644 blob %s\tc.py\n' "$b" | git -C "$R" mktree)" && git -C "$R" update-ref refs/arbres/x "$t" || fatal arbre
A=--history; cas T-75d 2 SECRETS/historique '^refs/arbres/x:\(objet\)$' QQQQ
# Ref vers un arbre dont une entrée porte un nom en forme d'identifiant, contenu propre (T-75f ; revue G2, C-3).
r; b="$(printf 'propre\n' | git -C "$R" hash-object -w --stdin)" && t="$(printf '100644 blob %s\t%s.txt\n' "$b" "$V" | git -C "$R" mktree)" &&
  git -C "$R" update-ref refs/arbres/n "$t" || fatal arbre; A=--history; cas T-75f 2 SECRETS/historique '^refs/arbres/n:\(objet\)$' QQQQ
r; echo x > "$R/a.txt"; git -C "$R" add a.txt && git -C "$R" commit -qm "k = $V" || fatal commit; c1=$(h); A=--history; cas T-94 2 SECRETS/historique "^$c1:\(message\)\$" QQQQ
r; git -C "$R" tag -a tm -m "$G" || fatal tag; A=--history; cas T-95 2 SECRETS/historique '^refs/tags/tm:\(message\)$' QQQQ
r; echo x > "$R/a.txt"; git -C "$R" add a.txt && git -C "$R" commit -qm sujet -m "commit 0000000000000000000000000000000000000000" -m "$V" || fatal commit
c1=$(h); A=--history; cas T-96 2 SECRETS/historique "^$c1:\(message\)\$" '^000000000000:'
# Tag annoté imbriqué (tag d'un tag ; seul le tag externe a une ref) : message intérieur balayé (T-105), propre (T-105b).
r; git -C "$R" tag -a ti -m "$G" && git -C "$R" tag -a tx ti -m propre 2>/dev/null && git -C "$R" tag -d ti >/dev/null || fatal tag
A=--history; cas T-105 2 SECRETS/historique '^refs/tags/tx:\(message\)$' QQQQ
r; git -C "$R" tag -a ti -m propre && git -C "$R" tag -a tx ti -m propre 2>/dev/null && git -C "$R" tag -d ti >/dev/null || fatal tag
A=--history; cas T-105b 0 'historique, 1 commit(s)'
r; printf 'k = "%s"\n' "$V" | git -C "$R" hash-object -w --stdin >/dev/null || fatal objet; A=--hors-refs; cas T-97 2 SECRETS/hors-refs ' dans 1 objet\(s\) hors refs' QQQQ
r; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci c; git -C "$R" reset -q --hard HEAD~1 || fatal reset; A=--history; cas T-98a 0 'historique, 1 commit(s)'
A=--hors-refs; cas T-98b 2 SECRETS/hors-refs ' dans 3 objet\(s\) hors refs'
r; A=--hors-refs; cas T-99 0 'hors refs, 0 objet(s) hors refs sur 3'
r; printf 'k = "%s"\n' "$V" > "$R/c.py"; ci a; git -C "$R" rm -q c.py || fatal rm; ci r; git -C "$R" bundle create -q "$W/b$K.bundle" --all 2>/dev/null &&
  git clone -q "$W/b$K.bundle" "$W/bc$K" 2>/dev/null || fatal bundle; D="$W/bc$K"; A=--history; cas T-100 2 SECRETS/historique
D="$W/sup"; A=--hors-refs; cas T-101 2 SECRETS/tronque superficiel
# grep en erreur sur les flux de D8d-2 (enveloppe gv de T-82) : hors refs (T-102), objet d'une ref (T-103), message (T-104).
r; printf 'k # ECHEC-GREP\n' | git -C "$R" hash-object -w --stdin >/dev/null || fatal objet; P="$W/gv:$PATH"; A=--hors-refs; cas T-102 2 SECRETS/echec 'grep a échoué \(hors refs\)'
r; git -C "$R" tag te "$(printf 'k # ECHEC-GREP\n' | git -C "$R" hash-object -w --stdin)" || fatal tag; P="$W/gv:$PATH"; A=--history; cas T-103 2 SECRETS/echec 'grep a échoué \(refs\)'
r; git -C "$R" commit -q --allow-empty -m 'k # ECHEC-GREP' || fatal commit; P="$W/gv:$PATH"; A=--history; cas T-104 2 SECRETS/echec 'grep a échoué \(messages\)'

echo "secrets : $OK ok, $KO échec"
[ "$KO" -eq 0 ]
