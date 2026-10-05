"""Boucle du pool (CB-4 ; E-C-09, E-C-11 à E-C-15 ; ADR-0029 §2.9 l.233-234). Dans la fenêtre ws, chaque lecture part
à son instant planifié (départ ws + w − δ, plus le décalage de sa forme) si une place du pool borné est libre, sinon
elle ne part pas : comptée, jamais écrite en panne de source (Q-C-02). Le fil principal attend l'échéance
E = ws + w − 1 s, relève alors une seule fois l'état des lectures et des sondes, puis écrit seul (l'écrivain ne se
partage pas) : une `lecture` par lecture partie (non finie au relevé, ou finie après E : `panne_transport`, `dns` si
la résolution n'avait pas rendu à E, sinon `delai`, `fin` = E ; son fil est abandonné), la `sante`, le marqueur (C-1
de la G2 de P1-B). Un résultat tardif est compté avec sa latence dans la santé suivante, jamais écrit (Q-C-15). Fils
démons et futurs de concurrent.futures, pas de ThreadPoolExecutor : il joint ses fils à la sortie, un fil pendu
bloquerait le processus (essai, 3.10 à 3.13). Sans sondes, la `sante` reste complète, champs des sondes nuls (O-7).
Chaque relevé lit aussi l'horloge murale et l'horloge monotone : la `sante` journalise, brut, le temps écoulé sur
chacune depuis le relevé précédent ; un recul de l'horloge murale s'y lit (C-4). CB-18b : départ et échéance
s'attendent sur l'horloge murale, relue au moins chaque seconde (SHOGEN-S2BIS-SOMMEIL-MURAL-1) ; le départ de chaque
lecture est aussi relevé sur l'horloge monotone et porté dans son suivi (limite E-4 levée) ; un nom du plan sans
lecture est refusé à la construction (SHOGEN-S2BIS-PLAN-CABLAGE-1) ; au relevé, une sonde finie après E vaut
null, sur l'horloge monotone, et disque et empreinte se relèvent après l'état des futurs
(SHOGEN-S2BIS-SONDES-ECHEANCE-1)."""
import concurrent.futures
import threading
import time

from shogen_s2bis.collecte.lecture import S, Lecture, horloge, monotone

DELTA, MARGE, PAR_HOTE = 20 * S, S, 5                     # δ, marge de l'échéance, lectures par hôte (ADR l.233-234)
PAS = S                                                 # attente d'un seul tenant au plus : l'horloge murale est relue
NULS = {"d3": None, "d4": [], "d5": [], "disque": None, "resolveur": None}           # santé sans sondes (O-7)


class RefusBoucle(ValueError):
    """Refus nommé (`code`) à la construction : BOUCLE/hote, BOUCLE/plan (CB-18b)."""
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


def planifier(formes, espaces=()):
    """[(décalage, nom)] trié depuis `formes` [(nom, hôte)] : sur un hôte de `espaces` (sa limite l'exige), la k-ième
    lecture part k s après le départ ; ailleurs, au départ. Plus de PAR_HOTE lectures sur un hôte : BOUCLE/hote."""
    rangs, plan = {}, []
    for nom, hote in formes:
        k = rangs[hote] = rangs.get(hote, -1) + 1
        if k >= PAR_HOTE:
            raise RefusBoucle("BOUCLE/hote", f"plus de {PAR_HOTE} lectures par fenêtre sur {hote} : regroupement")
        plan.append((k * S if hote in espaces else 0, nom))
    return sorted(plan)


def jusqu_a(t, horloge, attente):
    """Attend que l'horloge murale `horloge` atteigne `t` (µs), par attentes `attente(d)` d'au plus PAS µs, en la
    relisant après chacune : un recul de l'horloge prolonge l'attente, une avance l'abrège (CB-18b). Une attente qui
    rend vrai (futurs tous rendus) y met fin."""
    while (reste := t - horloge()) > 0:
        if attente(min(reste, PAS)):
            return


class Boucle:
    def __init__(self, journal, lectures, plan, places, w=60, delta=DELTA, marge=MARGE, horloge=horloge,
                 dormir=None, attendre=None, sondes=None, monotone=monotone):
        """`lectures` {nom: lire(suivi)} ; `plan` de `planifier` ; `places` : taille scellée du pool ; attentes à t ;
        `sondes` (sante.Sondes, CB-11) : lancées au départ, jointes avant l'échéance, versées à `sante` ; `monotone` :
        horloge monotone du relevé (C-4), des départs et des fins de sondes (CB-18b). Nom du plan sans lecture :
        BOUCLE/plan."""
        manquants = sorted({nom for _d, nom in plan} - lectures.keys())
        if manquants:
            raise RefusBoucle("BOUCLE/plan", f"noms du plan sans lecture : {manquants}")
        self.journal, self.lectures, self.plan, self.horloge, self.w = journal, lectures, plan, horloge, w
        self.sondes, self.monotone, self.repere = sondes, monotone, None    # repère : relevé (murale, monotone), C-4
        self.delta, self.marge, self.places, self.abandons = delta, marge, threading.BoundedSemaphore(places), []
        self.dormir = dormir or (lambda t: jusqu_a(t, horloge, lambda d: time.sleep(d / S)))
        self.attendre = attendre or (lambda futurs, t: jusqu_a(t, horloge, lambda d: not concurrent.futures.wait(
            futurs, d / S).not_done))

    def tourner(self, n=None):
        """`n` fenêtres (sans fin si None) depuis la première que le journal admet ; une fenêtre dont l'échéance est
        passée est sautée : l'écrivain déclare le trou au marqueur suivant."""
        ws = self.journal.suivante
        while n is None or n > 0:
            ws = max(ws, (self.horloge() + self.marge) // (S * self.w) * self.w)
            self.fenetre(ws)
            ws, n = ws + self.w, None if n is None else n - 1

    def fenetre(self, ws):
        depart, echeance = (ws + self.w) * S - self.delta, (ws + self.w) * S - self.marge
        lancees, non_parties, retards, sondes = [], 0, [], []
        if self.sondes:                                             # sondes de santé au départ (Q-C-03)
            self.dormir(depart)
            sondes = self.sondes.lancer(self.monotone)
        for decalage, nom in self.plan:
            self.dormir(depart + decalage)
            if not self.places.acquire(blocking=False):
                non_parties += 1
                continue
            suivi, futur = {"depart": self.horloge(), "monotone": self.monotone()}, concurrent.futures.Future()
            retards.append(suivi["depart"] - depart - decalage)
            threading.Thread(target=self._lire, args=(nom, suivi, futur), daemon=True).start()
            lancees.append((nom, depart + decalage, suivi, futur))
        self.attendre([f for *_x, f in lancees] + [f for _c, f in sondes if f is not None], echeance)
        murale, mono = self.horloge(), self.monotone()            # relevé unique (C-1) : instant, lectures, sondes
        releve = [(nom, prevu, suivi["depart"], futur, futur.result() if futur.done() else None,
                   dict(suivi.get("phases", {})), suivi.get("adresse")) for nom, prevu, suivi, futur in lancees]
        champs, vivantes = dict(NULS), 0
        if self.sondes:                                             # E sur l'horloge monotone, lue au relevé
            champs, vivantes = self.sondes.joindre(sondes, mono - (murale - echeance)), self.sondes.vivantes()
        horloges = None if self.repere is None else {"murale": murale - self.repere[0],
                                                     "monotone": mono - self.repere[1]}
        self.repere = murale, mono
        finis, vivants = concurrent.futures.wait(self.abandons, timeout=0)
        tardives, self.abandons = sorted(f.result().fin - f.result().depart for f in finis), list(vivants)
        for nom, prevu, dep, futur, lu, phases, adresse in releve:
            if lu is None or lu.fin > echeance:                     # non finie à l'échéance : état atteint à E
                phases = {k: t for k, t in phases.items() if t <= echeance}
                lu = Lecture("panne_transport", dep, echeance, phases, adresse if "dns" in phases else None,
                             sous_type="delai" if "dns" in phases else "dns")
                self.abandons.append(futur)
            self.journal.ecrire("lecture", ws, forme=nom, prevu=prevu, **lu.enregistrement())
        self.journal.ecrire("sante", ws, d2={"retard_max": max(retards, default=None), "non_parties": non_parties},
                            fils={"abandonnes": len(self.abandons), "tardives": tardives, "sondes": vivantes},
                            horloges=horloges, **champs)
        self.journal.marqueur(ws)

    def _lire(self, nom, suivi, futur):
        """Fil d'une lecture. Le futur rend toujours, une `Lecture` : une BaseException suit son cours (O-5)."""
        lu = None
        try:
            lu = self.lectures[nom](suivi)
        except Exception:                                           # attrape-tout : une lecture ne lève jamais
            pass
        finally:
            self.places.release()
            futur.set_result(lu if isinstance(lu, Lecture) else Lecture(
                "panne_transport", suivi["depart"], self.horloge(), suivi.get("phases"), suivi.get("adresse"),
                sous_type="autre"))
