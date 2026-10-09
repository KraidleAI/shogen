"""Processus secondaire de l'observateur (CB-13 ; E-C-30 à E-C-33 ; ADR-0029 l.235 ; AQT Q1 ; Q-C-04 ; FORMAT §15) :
la carte et le relevé ASN, hors du processus du pool, dans un journal à lui (préfixe `secondaire`, son propre
dossier). CB-13a : les lectures de la carte suivent la boucle du pool (CB-4), départ à ws + w − δ, hors de la fenêtre
δ du pool (5 s scellées, CB-13b), sans sondes : D-1 à D-5 restent ceux du pool. Le relevé ASN ne tourne jamais sur un
fil qui écrit. Il est dû à la première fenêtre de l'exécution, puis à la première fenêtre lue qui suit un instant de la
cadence scellée (ws mod `periode` = `decalage`) : un instant sauté (fenêtre sautée, arrêt) est rattrapé, en mémoire
seule, sans relecture du journal (E-C-15 ; C-4 de la G2 de P2A). Un `releve_asn` note le relevé dû et s'il part
(`lance`) ; il part sur un fil démon si le relevé précédent a rendu, sinon il est sauté (au plus un fil de relevé, comme
les sondes, C-5). Chaque hôte relevé (`asn.releve`, CB-12b ; hôtes dans l'ordre des points de code)
est remis par une file au fil de la boucle, seul écrivain (CB-18a), qui l'écrit en `asn` en tête de la fenêtre
suivante ; un défaut imprévu du relevé d'un hôte s'écrit `asn` à `a` null, et le relevé continue."""
import queue
import threading

from shogen_s2bis.collecte import asn, boucle


class Secondaire(boucle.Boucle):
    def __init__(self, journal, lectures, plan, places, hotes, resolveur, periode, decalage, releve=asn.releve, **kw):
        """Boucle de la carte (`boucle.Boucle`, mêmes paramètres) ; `hotes` à relever par le résolveur `resolveur`
        (adresse IPv4 du descripteur), à la cadence (`periode`, `decalage`, secondes) ; `releve` injectable."""
        super().__init__(journal, lectures, plan, places, **kw)
        self.hotes, self.resolveur, self.periode, self.decalage = sorted(hotes), resolveur, periode, decalage
        self.releve, self.file, self.fil, self.vu = releve, queue.Queue(), None, None    # vu : dernière fenêtre lue

    def fenetre(self, ws):
        while not self.file.empty():                                # relevés rendus : écrits par le fil de la boucle
            self.journal.ecrire("asn", ws, **self.file.get())
        du = self.vu is None or (ws - self.decalage) // self.periode > (self.vu - self.decalage) // self.periode
        self.vu = ws                                                # démarrage, ou instant de la cadence dans (vu, ws]
        if du:
            lance = self.fil is None or not self.fil.is_alive()
            self.journal.ecrire("releve_asn", ws, hotes=self.hotes, lance=lance)
            if lance:
                self.fil = threading.Thread(target=self._relever, daemon=True)
                self.fil.start()
        super().fenetre(ws)

    def _relever(self):
        """Fil du relevé : chaque hôte, dans l'ordre, remis à la file ; il n'écrit jamais."""
        for h in self.hotes:
            try:
                champs = self.releve(h, self.resolveur)
            except Exception:                                       # défaut imprévu : noté, le relevé continue
                champs = {"hote": h, "a": None, "ip": None, "ripestat": None, "cymru": None}
            self.file.put(champs)
