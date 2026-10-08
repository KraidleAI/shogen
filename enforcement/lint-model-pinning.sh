#!/usr/bin/env bash
# Shōgen, gate G1 (R-1) : lint d'épinglage des modèles, en liste blanche exacte.
# Rattachement : ADR-0028 D8 et C-14, décision CB-10 du cp-1 bis, lot D8a (G0 :
# docs/adr-0028/G0-lot-D8a.md ; journal docs/G1-lot-D8a.md, qui nomme les écarts au
# blob source). Porté du blob 457565f (adb2213:enforcement/lint-model-pinning.sh),
# identique à celui du commit 0b4f3f9 de l'amont VibeGates.
# Liste blanche : roster des décisions 133, 267 et 280 et décision du fondateur du 2026-10-08 (Haiku 5.5, rôles
# de signal ; annexe B, bloc B.76) : CLAUDE.md l.23-49, point 7. Elle vit ici, sur une ligne ; la changer demande
# un lot (lot LINT-HAIKU : G0 docs/adr-0028/G0-lot-LINT-HAIKU.md). L'identifiant banni le 2026-08-14
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
# indenté ou non fermé, clé model imbriquée hors d'une ligne model, suite de valeur à toute
# profondeur), JSON non strict, clé JSON échappée, aucun agent lu (lot D8c : CH-12, CH-13).
# Limite : ce lint lit le texte versionné, pas le modèle qui tourne (paramètre
# d'invocation, environnement, réglages hors dépôt, substitution par la plateforme) ;
# le contrôle R-1 au lancement reste dû. Lecteur de Claude Code non lu : refus fail-closed,
# formes restantes (ancres, étiquettes, alias et échappements imbriqués) : SHOGEN-LINT-LECTEUR-CC-1.
# Rôle (lot LINT-HAIKU, E-LH-1 lu au G0 §7) : SIGNAL, en rôles de signal seulement (CLAUDE.md l.35-42), n'est
# admis que comme valeur de la clé model de premier niveau d'un frontmatter d'agent, de skill ou de commande. Il est
# refusé (R-1/role) partout dans un réglage JSON (clé, valeur ou sous-chaîne ; casse ignorée ; échappement u00XX de
# la minuscule ou de la majuscule lu) et, dans un frontmatter, sur une ligne model indentée ou en séquence, ou placée
# après une ligne du même frontmatter qui porte [ ou { (FL, jamais remis à 0 dans le fichier). Référence écrite :
# PyYAML 6.0.1, qui lit comme imbriquée une ligne model de colonne 0 dans un flux ouvert sur plusieurs lignes ; le
# lint ne suit pas la fermeture des flux (chaînes, apostrophes, tirets : revue du tour 3) et refuse sans la chercher.
# Locale (lot LINT-HAIKU, E-LH-5) : LC_ALL=C, exporté, sur tout hôte. Sous C.UTF-8, bash, grep et sed rangeaient
# dans [[:space:]] 15 blancs Unicode (BU, mesuré) : model:<U+3000>id passait. Pour que la locale fixée ne desserre
# rien : BU est refusé dans un frontmatter (R-1/cle-model) et compté comme blanc entre agent et ( ; l'UTF-8 invalide
# (hors U8) est refusé dans le commentaire d'une ligne model (R-1/hors-liste ; sous C.UTF-8, il y gardait le
# commentaire dans la valeur) et sur toute autre ligne du frontmatter (R-1/cle-model ; sous C.UTF-8, un octet
# invalide en tête de ligne masquait l'indentation). Prix : BU ou UTF-8 invalide dans un frontmatter ; SIGNAL cité
# dans un réglage JSON ; SIGNAL en clé model de premier niveau après toute ligne du frontmatter qui porte [ ou { (FL).
# Prix mesuré (revue G2 de D8c, 2026-10-01) : une description qui cite une forme de flux de la clé
# model est refusée (R-1/cle-model) ; ainsi l'agent global worker.md, l.3 : SHOGEN-LINT-HORS-DEPOT-1.
# Usage : lint-model-pinning.sh [racine]   Sortie : 0 aucun refus, 2 refus (stderr).

set -u
export LC_ALL=C   # E-LH-5 (lot LINT-HAIKU) : verdict indépendant de la locale, comme enforcement/gate-secrets.sh
ROOT="${1:-.}"
[ "$ROOT" = / ] || ROOT="${ROOT%/}"
ALLOWED='claude-opus-5-5 claude-sonnet-5-5 claude-fable-5-1 claude-haiku-5-5'
SIGNAL='claude-haiku-5-5'   # rôles de signal seulement : clé model de premier niveau d'un frontmatter (G0 §7)
# SIGX : SIGNAL dans un texte JSON, casse ignorée (grep -i), chaque caractère en clair ou en échappement u00XX de
# sa minuscule (h) ou de sa majuscule (g) : grep -i ne replie pas le code d'un échappement (revue du tour 3, C-2).
SIGX=; for ((j = 0; j < ${#SIGNAL}; j++)); do c="${SIGNAL:j:1}"
  printf -v h '%02x' "'$c"; printf -v g '%02x' "'${c^^}"; SIGX+="($c|"'\\'"u00($h|$g))"; done
BANNED="claude-opus-""5"
RETIRED='claude-sonnet-5'
TIERS='opus|sonnet|haiku|fable|inherit|default|opusplan'
# BU : blancs Unicode de [[:space:]] sous C.UTF-8 (bash, grep et sed, mesuré au lot LINT-HAIKU) : U+1680, U+2000
# à U+2006, U+2008 à U+200A, U+2028, U+2029, U+205F et U+3000 ; motif des octets UTF-8, écrits en octal.
BU="$(printf '\341\232\200|\342\200[\200-\206\210-\212\250\251]|\342\201\237|\343\200\200')"
# U8 : suite d'octets UTF-8 bien formée (RFC 3629), écrite en octal ; sur 1 201 300 formes de commentaire (tout point
# de code, substituts, surlongs, au-delà de U+10FFFF, tronqués, octets seuls), même partage que glibc 2.39 sous
# C.UTF-8 (mesuré au lot LINT-HAIKU).
U8="$(printf '^([\001-\177]|[\302-\337][\200-\277]|\340[\240-\277][\200-\277]|[\341-\354\356\357][\200-\277]{2}')"
U8="$U8$(printf '|\355[\200-\237][\200-\277]|\360[\220-\277][\200-\277]{2}|[\361-\363][\200-\277]{3}')"
U8="$U8$(printf '|\364[\200-\217][\200-\277]{2})*$')"
# FL (rôle) : 1 dès qu'une ligne précédente du même frontmatter porte [ ou { (FO), à toute place (valeur, chaîne,
# commentaire, bloc), jamais remis à 0 dans le fichier : les fermants ne se comptent pas ligne à ligne (revue du
# tour 3, C-1). Échec fermé.
FO='[[{]'
# Début de ligne de premier niveau qui forme une clé non nue, lue model par PyYAML 6.0.3
# (mesuré) : guillemets, ?, ancre &, étiquette !, alias *, flux {, clé de fusion <<. Le
# tiret et | > en colonne 0 restent des formes valides (séquence non indentée, bloc).
NON_NUE="^([\"'?&!*{]|<<)"
# Clé model hors de la forme lue (ligne canonique, entrée de séquence comprise) : entre guillemets à
# toute profondeur, ou après [, { ou , (flux). Une prose où model suit un mot n'est pas prise.
SENT="(^[[:space:]]*(-[[:space:]]+)*|[[{,][[:space:]]*)[\"']?model[\"']?[[:space:]]*:"
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
  N=$((N + 1)); n=0; K=0; FM=0; SUITE=0; DEB=0; I=0; FL=0
  while IFS= read -r x || [ -n "$x" ]; do
    n=$((n + 1)); x="${x%$'\r'}"
    if [ "$n" -eq 1 ]; then x="${x#$'\xEF\xBB\xBF'}"
      [[ $x =~ ^--- && $x =~ $BU ]] && refus 'R-1/cle-model' "$f:$n" "$x" "blanc Unicode (BU) : forme non lue"
      [[ $x =~ ^---[[:space:]]*$ ]] || break; FM=1; DEB=1; continue; fi
    [[ $x =~ ^---[[:space:]]*$ ]] && { FM=2; break; }
    [[ $x =~ $BU ]] && refus 'R-1/cle-model' "$f:$n" "$x" "blanc Unicode (BU) : forme non lue"
    if [ "$DEB" -eq 1 ] && [[ $x =~ ^[[:space:]]*[^[:space:]#] ]]; then DEB=0
      [[ $x =~ ^[[:space:]] ]] && refus 'R-1/cle-model' "$f:$n" "$x" "frontmatter indenté : clés de premier niveau non lues"; fi
    # Suite d'une valeur model, à toute profondeur : première ligne ni vide ni commentaire, plus
    # indentée que la clé (colonne I).
    if [ "$SUITE" -eq 1 ] && [[ $x =~ ^([[:space:]]*)[^[:space:]#] ]]; then SUITE=0
      [ "${#BASH_REMATCH[1]}" -gt "$I" ] && refus 'R-1/hors-liste' "$f:$n" "$x" "suite de la valeur model sur une autre ligne : non lue"; fi
    [[ $x =~ $NON_NUE ]] && refus 'R-1/cle-model' "$f:$n" "$x" "ligne de premier niveau qui n'est pas une clé nue : non lue"
    # Clé model de premier niveau comptée ; ligne model contrôlée à toute profondeur, entrée de
    # séquence comprise ; hors de cette forme, une clé model est refusée (sentinelle SENT).
    [[ $x =~ ^model[[:space:]]*:([[:space:]]|$) ]] && K=$((K + 1))
    if [[ $x =~ ^([[:space:]]*(-[[:space:]]+)*)model[[:space:]]*: ]]; then SUITE=1; I=${#BASH_REMATCH[1]}
      [[ $x =~ [[:blank:]]#(.*) ]] && { [[ ${BASH_REMATCH[1]} =~ $U8 ]] ||
        refus 'R-1/hors-liste' "$f:$n" "$x" "commentaire en UTF-8 invalide (U8) : gardé dans la valeur sous C.UTF-8"; }
      v="$(printf '%s' "$x" | sed -E 's/^[[:space:]]*(-[[:space:]]+)*model[[:space:]]*:[[:space:]]*//')"
      v="$(norm "$v")"
      if [ "$v" = "$SIGNAL" ] && [ $((I + FL)) -gt 0 ]; then
        refus 'R-1/role' "$f:$n" "$v" "rôle de signal seulement : admis en seule clé model de premier niveau"
      else verdict "$f:$n" "$v"; fi
    elif [[ $x =~ $SENT ]]; then
      refus 'R-1/cle-model' "$f:$n" "$x" "clé model hors de la forme lue (flux, guillemets) : non lue"
    elif ! [[ $x =~ $U8 ]]; then refus 'R-1/cle-model' "$f:$n" "$x" "UTF-8 invalide (U8) : forme non lue"; fi
    # FL : posé après le jugement de la ligne ; une ligne model ne se juge pas sous ses propres crochets.
    [[ $x =~ $FO ]] && FL=1
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

# 2) Réglages JSON, aplatis, lus comme une suite de chaînes JSON entières (RX, LC_ALL=C) : une clé est
#    une chaîne suivie de deux-points (lot D8c, CH-13). Refusés : un résidu hors chaînes autre que
#    ponctuation, nombres et littéraux (JSON non strict : commentaire, clé sans guillemets) ; une clé
#    qui porte une barre oblique inverse (un échappement peut former model) ; une clé model ou
#    advisorModel dont la valeur n'est pas une chaîne (elle n'épingle rien). Virgule finale admise.
#    SIGNAL y est refusé partout (R-1/role) : clé, valeur ou sous-chaîne, casse ignorée, échappements u00XX lus (SIGX).
RX='"([^"\\]|\\.)*"'
for f in "$ROOT/.claude/settings.json" "$ROOT/.claude/settings.local.json"; do
  [ -f "$f" ] || continue
  N=$((N + 1))
  J="$(tr '\r\n' '  ' < "$f")"
  printf '%s' "$J" | grep -qiE "$SIGX" &&
    refus 'R-1/role' "$f" "$SIGNAL" "rôle de signal seulement : jamais dans un réglage JSON (G0 §7)"
  [ -z "$(printf '%s' "$J" | LC_ALL=C sed -E "s/$RX//g; s/true|false|null//g; s/[][{}:,0-9eE.+[:space:]-]//g")" ] ||
    refus 'R-1/hors-liste' "$f" "JSON non strict" "hors chaînes, autre chose que ponctuation, nombres et littéraux : non lu"
  P="$(printf '%s' "$J" | LC_ALL=C grep -oE "$RX([[:space:]]*:[[:space:]]*($RX|.))?" | LC_ALL=C grep -E "^$RX[[:space:]]*:")"
  printf '%s\n' "$P" | grep -qE '^"[^"]*\\' &&
    refus 'R-1/hors-liste' "$f" "clé JSON avec échappement" "clé non lue : un échappement peut former model ou advisorModel"
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    k="$(printf '%s' "$p" | sed -E 's/^"([^"]*)".*/\1/')"; v="$(printf '%s' "$p" | LC_ALL=C sed -E "s/^$RX[[:space:]]*:[[:space:]]*//")"
    case "$v" in \"*\") verdict "$f ($k)" "${v:1:${#v}-2}" ;;
      *) refus 'R-1/hors-liste' "$f ($k)" "valeur non chaîne" "clé model ou advisorModel sans identifiant entre guillemets" ;; esac
  done <<EOF_JSON
$(printf '%s\n' "$P" | LC_ALL=C grep -iE '^"(model|advisorModel)"[[:space:]]*:')
EOF_JSON
done

# 3) Scripts de workflow : le paramètre model d'un appel agent( prime sur le frontmatter.
#    Aucun lint ne les lit encore : tout script qui en contient un est refusé (item
#    SHOGEN-LINT-WORKFLOW-1). Élagage ELAG, commun aux passes 1 et 3. Entre agent et ( : blancs ASCII et BU.
JS=( \( -name '*.js' -o -name '*.mjs' -o -name '*.cjs' \) )
WF='(^|[^A-Za-z0-9_$.])agent([[:space:]]|'"$BU"')*\('
while IFS= read -r f; do
  [ -n "$f" ] && refus 'R-1/workflow' "$f" "appel agent(" "script de workflow non couvert (item SHOGEN-LINT-WORKFLOW-1)"
done <<EOF_WF
$(find "$ROOT" "${ELAG[@]}" -type f "${JS[@]}" -exec grep -lE "$WF" {} + 2>/dev/null)
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
