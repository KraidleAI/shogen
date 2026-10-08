# Vérification sur pièce des citations de RFC (diffs CB-11c..g et p1b/diffs)

Gate 0 : modèle sous lequel je tourne = `claude-sonnet-5-5` (effort high attendu). Date de lecture : 2026-10-05, 02:14 UTC (`date -u`).
Sources lues : rfc-editor.org/rfc/rfc{1035,7301,8446,9110}.txt (curl), copies dans ce dossier. Numéros de ligne = lignes du .txt.

## Tableau

| # | Mention (diff, texte) | RFC / section existe ? | Phrase de la RFC (ligne .txt) | Verdict |
|---|---|---|---|---|
| 1 | RFC 1035 §4.1 comme « format » du client DNS (CB-10a l.36, CB-11f l.83 : « en-tête de 12 octets, une question… », ID, bit QR, drapeau TC) | Oui, §4.1 « Format » (l.1351), sous-sections 4.1.1 en-tête (l.1401), 4.1.2 question (l.1530) | « All communications inside of the domain protocol are carried in a single format called a message. » (l.1353) ; en-tête : ID, QR, TC, QDCOUNT… (l.1408-1418) | EXACT |
| 2 | RFC 1035 §4.1 accolé à « l'adresse est une IPv4 littérale » / « sans résolution et sans envoi » (CB-10b l.36, CB-11b l.18, CB-11c l.62, CB-11d l.35, CB-11e l.61, CB-11f l.42-49) | Section existe | §4.1 ne parle ni d'adresse IPv4 littérale ni d'absence de résolution ; il décrit le format des messages (l.1353-1383) | À CORRIGER (placement) : la RFC ne soutient que la phrase précédente (« même identifiant, bit QR, même question »). Proposé : mettre « (RFC 1035 §4.1.1-4.1.2) » après « même question », et ne laisser que « ADR-0029 l.109 » après la phrase IPv4 littérale. Si la parenthèse est censée couvrir tout le paragraphe, la laisser est tolérable mais ambiguë. |
| 3 | RFC 1035 §4.1.4, pointeur de compression (CB-10a l.119, CB-10b l.109, CB-11e l.375, CB-11f l.150 : « §4.1, pointeur §4.1.4 ») | Oui, §4.1.4 « Message compression » (l.1634) | « The pointer takes the form of a two octet sequence » (l.1642) ; « The first two bits are ones. » (l.1648) | EXACT |
| 4 | RFC 1035 §4.1.4, « octet d'étiquette de 0x40 à 0xBF (combinaisons 01 et 10 réservées) » (CB-11f l.173) | Oui | « (The 10 and 01 combinations are reserved for future use.) » (l.1650-1651) ; contexte : « the label must begin with two zero bits » (l.1649). 01 = 0x40-0x7F, 10 = 0x80-0xBF ; 0xC0 et plus = pointeur (11) : plage exacte. | EXACT |
| 5 | RFC 7301 §3.1, « liste de 9 octets, nom de 8 » pour `http/1.1` (CB-11g l.170 ; test attend `00 09 08 "http/1.1"`) | Oui, §3.1 (l.141) | « opaque ProtocolName<1..2^8-1>; » (l.155) ; « ProtocolNameList protocol_name_list<2..2^16-1> » (l.158) ; « 0x68 0x74 0x74 0x70 0x2f 0x31 0x2e 0x31 ("http/1.1") » (l.374, §6, 8 octets) | EXACT, avec réserve : les chiffres 9 et 8 ne sont pas écrits dans §3.1, ils se déduisent de la syntaxe (nom préfixé sur 1 octet : 1+8 = 9 ; liste préfixée sur 2 octets : valeur 0x0009). La RFC n'a pas d'exemple d'octets pour `http/1.1` ; la longueur 8 se lit à l'identifiant de §6 (l.374). Aucune correction obligatoire ; si l'on veut être précis : « §3.1 (syntaxe), §6 (identifiant) ». |
| 6 | RFC 8446 §4.1.2, ClientHello, extensions « lues à la main » (CB-11g l.129) | Oui, §4.1.2 « Client Hello » (l.1485) | « Extension extensions<8..2^16-1>; » en fin de structure, après `legacy_version`, `random`(32), `legacy_session_id`, `cipher_suites`, `legacy_compression_methods` (l.1546-1553) | EXACT (le décalage `5+4+2+32` du code = enregistrement, en-tête de poignée, version, aléa ; la structure de §4.1.2 le confirme pour version 2 et aléa 32 ; les 5 et 4 octets relèvent de §5.1 et §4, non cités) |
| 7 | RFC 8446 §4.2.6, « extension 49, vide » (post_handshake_auth) (CB-11g l.170-171) | Oui, §4.2.6 « Post-Handshake Client Authentication » (l.2583) | « The "extension_data" field of the "post_handshake_auth" extension is zero length. » (l.2593-2594) ; numéro : « post_handshake_auth(49), » (l.1941, dans §4.2, pas §4.2.6) | À CORRIGER (mineur) : « vide » est bien en §4.2.6 ; le numéro 49 ne figure pas dans §4.2.6 mais dans l'énumération ExtensionType de §4.2 (l.1941). Proposé : « RFC 8446 §4.2 (numéro 49), §4.2.6 (vide) ». Le fait lui-même est exact. |
| 8 | RFC 9110 §12.5.3, absence d'en-tête Accept-Encoding : « sans lui, tout codage est admis » (CB-3a l.37 et l.67, CB-3b l.67, CB-11g l.85) | Oui, §12.5.3 « Accept-Encoding » (l.5525) | « If no Accept-Encoding header field is in the request, any content coding is considered acceptable by the user agent. » (l.5560-5561). Pour `identity` : « An "identity" token is used as a synonym for "no encoding" » (l.5537-5538) | EXACT (nuance : « acceptable by the user agent », sans objet pour la validité du texte) |

Mentions repérées par `grep -n RFC` : 23 lignes, toutes couvertes ci-dessus (celles des lignes de contexte reprises de CB-10a/10b dans CB-11e/f comptent pour la ligne 3). Aucune autre RFC citée dans ces diffs. Les mentions de CB-3a/3b/4/5/10/11a hors RFC 1035 / 9110 : aucune.

## Journal G1

[lu] (lu moi-même sur le .txt, ligne citée)
- RFC 1035 : §4.1 (l.1351-1383), §4.1.1 (l.1401-1418), §4.1.2 (l.1530-1541), §4.1.4 (l.1634-1654). Aussi l.535-540 (§3.1) : « The high order two bits of every length octet must be zero » (non cité par les diffs, utile en appui de #4).
- RFC 7301 : §3.1 (l.141-165), §6 (l.370-375).
- RFC 8446 : §4.1.2 (l.1485-1553), §4.2 énumération (l.1911, l.1925-1945), §4.2.6 (l.2583-2594).
- RFC 9110 : §12.5.3 (l.5525-5613).
- Diffs : contexte (quelques lignes) autour de chaque ligne repérée par `grep -n RFC`, dans CB-11c..g, CB-3a, CB-10a/b, CB-11b.

[2nd] (seconde main) : aucun.

[abs] (absent de la source)
- Les valeurs « 9 » et « 8 » ne sont écrites nulle part dans RFC 7301 §3.1 (déduites de la syntaxe et de l'identifiant de §6).
- Le numéro 49 est absent du texte de §4.2.6 de la RFC 8446.
- Aucune mention d'adresse IPv4 littérale ni d'absence de résolution dans RFC 1035 §4.1.

Limites : aucune page manquante, aucune source illisible. Rien n'a été lu hors des diffs nommés et des 4 RFC ; aucune pièce de la liste D.2 ni journal de campagne ouverts.
