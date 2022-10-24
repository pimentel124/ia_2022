""" Mòdul que conté l'agent per jugar al joc de les monedes.

Percepcions:
    ClauPercepcio.MONEDES
Solució:
    " XXXC"
"""
from queue import PriorityQueue

from ia_2022 import agent, entorn
from monedes.entorn import AccionsMoneda, ClauPercepcio

SOLUCIO = " XXXC"


class Estat:
    def __init__(self, info: str, pes: int, pare=None):
        self.__info = info
        self.__pare = pare
        self.__pes = pes

    def __hash__(self):
        return hash(tuple(self.__info))

    @property
    def info(self):
        return self.__info

    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.__info == other.info

    def es_meta(self) -> bool:
        return self.__info == SOLUCIO

    def genera_fills(self):
        fills = []

        buit = self.__info.find(" ")

        despls = [buit - 1, buit + 1]
        for desp in despls:
            if -1 < desp < len(self.__info):
                info_aux = list(self.__info)
                info_aux[buit] = self.__info[desp]
                info_aux[desp] = " "

                fills.append(
                    Estat(
                        "".join(info_aux),
                        self.__pes + 1,
                        (self, (AccionsMoneda.DESPLACAR, desp)),
                    )
                )

        for i in range(len(self.__info)):
            info_aux = list(self.__info)
            info_aux[i] = self.gira(info_aux[i])
            fills.append(
                Estat(
                    "".join(info_aux), self.__pes + 2, (self, (AccionsMoneda.GIRAR, i))
                )
            )

        despls = [buit - 2, buit + 2]
        for desp in despls:
            if -1 < desp < len(self.__info):
                info_aux = list(self.__info)
                info_aux[buit] = self.gira(self.__info[desp])
                info_aux[desp] = " "

                fills.append(
                    Estat(
                        "".join(info_aux),
                        self.__pes + 2,
                        (self, (AccionsMoneda.BOTAR, desp)),
                    )
                )

        return fills

    def calc_heuristica(self):
        pos = self.__info.find(" ")
        heuristica = 0
        for lletra_es, lletra_sol in zip(self.__info, SOLUCIO):
            if lletra_sol != " ":
                heuristica += int(lletra_es != lletra_sol)

        heuristica += pos

        return heuristica + self.__pes

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value

    def __str__(self):
        return str(self.__info)

    def __lt__(self, other):
        return False

    @staticmethod
    def gira(moneda):
        if moneda == "C":
            return "X"
        elif moneda == "X":
            return "C"
        else:
            return " "


class AgentMoneda(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=0)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def cerca(self, estat_inicial):
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((estat_inicial.calc_heuristica(), estat_inicial))

        actual = None
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()
            if actual in self.__tancats:
                continue

            if actual.es_meta():
                break

            estats_fills = actual.genera_fills()

            for estat_f in estats_fills:
                self.__oberts.put((estat_f.calc_heuristica(), estat_f))

            self.__tancats.add(actual)

        if actual.es_meta():
            accions = []
            iterador = actual

            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat_inicial = Estat(percep[ClauPercepcio.MONEDES], 0, pare=None)

        if self.__accions is None:
            self.cerca(estat_inicial)

        if self.__accions:
            acc = self.__accions.pop()

            return acc[0], acc[1]
        else:
            return AccionsMoneda.RES
