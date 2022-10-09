""" Fitxer que conté l'agent Barca.

Percepcions:
    ClauPercepcio.LLOC
    ClauPercepcio.QUICA_ESQ
    ClauPercepcio.LLOP_ESQ
    ClauPercepcio.QUICA_DRETA
    ClauPercepcio.LLOP_DRETA

Accions:
    AccionsBarca.MOURE, (nombre_de_quiques, nombres_de_llop)
    AccionsBarca.ATURA
"""
import abc
import copy
import itertools

from ia_2022 import agent, entorn
from quiques.entorn import ClauPercepcio, Lloc


class Barca(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        print(self._posicio_pintar)

    @abc.abstractmethod
    def actua(self, percep: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass


class Estat:
    # QUIQUES, LLOPS
    acc_poss = [
        acc
        for acc in itertools.product([0, 1, 2], [0, 1, 2])
        if (acc[-1] + acc[-2]) < 3 and not (acc[-1] == 0 and acc[-2] == 0)
    ]

    def __init__(self, info: dict = None, pare=None):
        if info is None:
            info = {}

        self.__info = info
        self.__pare = pare

    def __hash__(self):
        return hash(tuple(self.__info.items()))

    def __getitem__(self, key):
        return self.__info[key]

    def __setitem__(self, key, value):
        self.__info[key] = value

    def __eq__(self, other):
        """Overrides the default implementation"""
        return (
                self[ClauPercepcio.QUICA_ESQ] == other[ClauPercepcio.QUICA_ESQ]
                and self[ClauPercepcio.QUICA_DRETA] == other[ClauPercepcio.QUICA_DRETA]
                and self[ClauPercepcio.LLOP_ESQ] == other[ClauPercepcio.LLOP_ESQ]
                and self[ClauPercepcio.LLOP_DRETA] == other[ClauPercepcio.LLOP_DRETA]
                and self[ClauPercepcio.LLOC] == other[ClauPercepcio.LLOC]
        )

    def legal(self) -> bool:
        """ Mètode per detectar si un estat és legal.

        Un estat és legal si no hi ha cap valor negatiu.

        Returns:
            Booleà indicant si és legal o no.
        """
        for key in [
            ClauPercepcio.QUICA_ESQ,
            ClauPercepcio.QUICA_DRETA,
            ClauPercepcio.LLOP_ESQ,
            ClauPercepcio.LLOP_DRETA,
        ]:
            if self.__info[key] < 0:
                return False

        return True

    def es_meta(self) -> bool:
        return self[ClauPercepcio.QUICA_ESQ] == 0 and self[ClauPercepcio.LLOP_ESQ] == 0

    def es_segur(self) -> bool:
        return (
                       self[ClauPercepcio.QUICA_ESQ] >= self[ClauPercepcio.LLOP_ESQ]
                       or self[ClauPercepcio.QUICA_ESQ] == 0
               ) and (
                       self[ClauPercepcio.QUICA_DRETA] >= self[ClauPercepcio.LLOP_DRETA]
                       or self[ClauPercepcio.QUICA_DRETA] == 0
               )

    def genera_fill(self) -> list:
        """ Mètode per generar els estats fills.

        Genera tots els estats fill a partir de l'estat actual.

        Returns:
            Llista d'estats fills generats.
        """
        estats_generats = []

        for accio in self.acc_poss:
            nou_estat = copy.deepcopy(self)
            nou_estat.pare = (self, accio)

            n_miss, n_canibals = accio

            if self[ClauPercepcio.LLOC] is Lloc.ESQ:
                n_miss = -n_miss
                n_canibals = -n_canibals

            nou_estat[ClauPercepcio.LLOC] = -self[ClauPercepcio.LLOC]
            nou_estat[ClauPercepcio.QUICA_ESQ] += n_miss
            nou_estat[ClauPercepcio.LLOP_ESQ] += n_canibals
            nou_estat[ClauPercepcio.QUICA_DRETA] -= n_miss
            nou_estat[ClauPercepcio.LLOP_DRETA] -= n_canibals

            if not nou_estat.legal():
                continue
            estats_generats.append(nou_estat)

        return estats_generats

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value

    def __str__(self):
        return str(self.__info.values())
