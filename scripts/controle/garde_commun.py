"""Bibliothèque commune des contrôles avant l'acte (lot GARDE-FOUS-ORCH ; G0 docs/adr-0028/G0-lots-DETTES.md, ajout
GF-0 ; adjudication de l'orchestrateur du 2026-10-10). Bibliothèque standard seule (R-8), Python 3.10 à 3.13.
GF-1, horloge et heures (E14) : l'horloge est lue par `date -u` en sous-processus, jamais par celle de Python ; les
tests la fixent par un faux `date` en tête du PATH. `horodatages_fautifs` juge chaque ligne hors code (accents graves)
et hors guillemets français : heure-future, une date du jour suivie (25 caractères au plus, sans autre date entre)
d'une heure plus tard que l'horloge + TOLERANCE_S, sans mot de PLAN dans les 40 caractères d'avant ; heure-approchee,
une heure écrite HH:Mx ou HH:xx. Une date d'un autre jour n'est pas jugée (échéance, veille). Limite : une heure
écrite sans sa date, ou une heure passée fausse, n'est pas vue."""
import re
import subprocess
from datetime import datetime, timedelta, timezone

TOLERANCE_S = 120
PLAN = re.compile(r"(?i)(prévue?s?|échéance|jalon|d['’]ici|à partir de)")
DATE = r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
DATE_HEURE = re.compile("(" + DATE + ")(?:(?!" + DATE + ").){0,25}?"
                        r"(?<![0-9])([01][0-9]|2[0-3]):([0-5][0-9])(?::([0-5][0-9]))?(?![0-9])")
APPROCHEE = re.compile(r"(?<![0-9:])(?:[01][0-9]|2[0-3]):(?:[0-5]x|xx)(?![0-9A-Za-z_])")
MASQUE = re.compile("`[^`]*`|«[^»]*»")


def maintenant():
    """Heure UTC lue par `date -u` (règle de l'investisseur : lire l'horloge avant d'écrire une date)."""
    s = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True, check=True).stdout
    return datetime.strptime(s.strip(), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def horodatages_fautifs(texte, horloge):
    """[(ligne, code, extrait)] : heure-future et heure-approchee, lignes comptées depuis 1."""
    fautes, borne, jour = [], horloge + timedelta(seconds=TOLERANCE_S), horloge.strftime("%Y-%m-%d")
    for n, ligne in enumerate(texte.split(chr(10)), 1):
        nue = MASQUE.sub(lambda m: " " * len(m.group()), ligne)
        for m in DATE_HEURE.finditer(nue):
            if m.group(1) != jour or PLAN.search(nue[max(0, m.start() - 40):m.start()]):
                continue
            h = datetime.strptime(f"{m.group(1)} {m.group(2)}:{m.group(3)}:{m.group(4) or '00'}", "%Y-%m-%d %H:%M:%S")
            if h.replace(tzinfo=timezone.utc) > borne:
                fautes.append((n, "heure-future", m.group(0).strip()))
        fautes += [(n, "heure-approchee", m.group(0)) for m in APPROCHEE.finditer(nue)]
    return fautes
