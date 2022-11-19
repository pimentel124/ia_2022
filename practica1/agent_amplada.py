# pylint: disable=E1101,C0116,C0114,C0115
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio

COST_MOURE = 1
COST_ESPERAR = 0.5
COST_BOTAR = 6
G_SIZE = (8, 8)


class Estat:
    def __init__(self, pos_meta, pos_agent, size, parets, pes=0, pare=None):
        self.__pare = pare
        self.__pos_meta = pos_meta
        self.__pos_agent = pos_agent
        self.__size = size
        global G_SIZE
        G_SIZE = self.__size
        self.__parets = parets
        self.__pes = pes

        print("pos_meta: " + str(self.__pos_meta))
        print("pos_agent: " + str(self.__pos_agent))
        print("size: " + str(self.__size))
        print("parets: " + str(self.__parets))
        print("pes: " + str(self.__pes))
        print("pare: " + str(self.__pare))

    def __eq__(self, other):
        return self.__pos_agent == other.get_pos_agent()

    def __hash__(self):
        return hash(tuple(self.__pos_agent))

    def get_pos_agent(self):
        return self.__pos_agent

    def get_pos_meta(self):
        return self.__pos_meta

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, pare):
        self.__pare = pare

    def calc_heuristica(self, string: str):
        """
        Calcula el valor heurístico de un estado dado.

        :param string: la cadena que identifica al agente
        :type string: str
        :return: El valor heurístico del estado.
        """
        total = 0
        for i in range(2):
            total += abs(self.__pos_meta[i] - self.__pos_agent[string][i])
        return total + self.__pes

    def es_legal(self, string: str):
        """
        Comprueba si la posición del agente es válida: Que no esté fuera de los límites del tablero y que no esté dentro de paredes.
        :param string: cadena = "Nombre del agente"
        :type string: str
        :return: El valor devuelto es una lista de tuplas.
        """
        print("es_legal --> self._parets = " + str(self.__parets))
        for i in self.__parets:
            if (self.__pos_agent[string][0] == i[0]) and (
                self.__pos_agent[string][1] == i[1]
            ):
                return False

        return (
            (self.__pos_agent[string][0] <= (self.__size[0] - 1))
            and (self.__pos_agent[string][0] >= 0)
            and (self.__pos_agent[string][1] <= (self.__size[1] - 1))
            and (self.__pos_agent[string][1] >= 0)
        )

    # Check si los dos están en la meta
    def es_meta(self, string: str):
        """
        Devuelve True si el agente está en la misma posición que el meta y False en caso contrario.
        
        :param string: cadena = 'A' o 'B'
        :type string: str
        :return: un valor booleano.
        """
        return (self.__pos_agent[string][0] == self.__pos_meta[0]) and (
            self.__pos_agent[string][1] == self.__pos_meta[1]
        )

    def genera_fills(self, string: str):
        """
        Genera todos los movimientos posibles para una rana dada.
        :param string: str = "nombre de la rana"
        :type string: str
        :return: una lista de posibles movimientos.
        """
        fills = []
        # generate dicctionary
        diccionari_moviments = {
            "DALT": (0, -1),
            "BAIX": (0, +1),
            "ESQUERRE": (-1, 0),
            "DRETA": (+1, 0),
        }

        # en el caso de movimientos normales
        claus = list(diccionari_moviments.keys())
        print("self.__pos_agent[string] = " + str(self.__pos_agent))
        for i, j in enumerate(diccionari_moviments.values()):
            coords = [sum(tup) for tup in zip(self.__pos_agent[string], j)]
            coordenades = {string: coords}
            cost = self.__pes + COST_MOURE
            actual = Estat(
                self.__pos_meta,
                coordenades,
                self.__size,
                self.__parets,
                cost,
                (self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i]))),
            )
            if actual.es_legal(string):
                fills.append(actual)

        # en el caso de saltos
        diccionari_bots = {
            "DALT": (0, -2),
            "BAIX": (0, +2),
            "ESQUERRE": (-2, 0),
            "DRETA": (+2, 0),
        }

        claus = list(diccionari_bots.keys())
        for i, j in enumerate(diccionari_bots.values()):
            coords = [sum(tup) for tup in zip(self.__pos_agent[string], j)]
            coordenades = {string: coords}
            cost = self.__pes + COST_MOURE
            actual = Estat(
                self.__pos_meta,
                coordenades,
                self.__size,
                self.__parets,
                cost,
                (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))),
            )
            if actual.es_legal(string):
                fills.append(actual)

        return fills


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None
        self.__turno = 0

    def _cerca(self, estat: Estat, string: str):
        """
        Toma un estado inicial, una cadena, y devuelve una lista de acciones que lo llevarán desde el
        estado inicial a un estado objetivo

        :param estat: Estado, string: str
        :type estat: Estat
        :param string: la cadena a buscar
        :type string: str
        :return: un valor booleano.
        """
        self.__oberts = []
        self.__tancats = set()

        self.__oberts.append(estat)
        actual = None
        while len(self.__oberts) > 0:
            actual = self.__oberts[0]
            self.__oberts = self.__oberts[1:]

            if actual in self.__tancats:
                continue

            estats_fills = actual.genera_fills(string)

            if actual.es_meta(string):
                break
            for estat_f in estats_fills:
                self.__oberts.append(estat_f)

            self.__tancats.add(actual)
        if actual is None:
            raise ValueError("Error impossible")
        if actual.es_meta(string):
            accions = []
            iterador = actual

            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions
            return True

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        """
        El entorno llama a la función actua() para obtener la siguiente acción del agente

        :param percep: entorno.Percepcion
        :type percep: entorn.Percepcio
        :return: La acción que realizará el agente.
        """

        percepcions = percep.to_dict()
        key_list = list(percepcions.keys())

        print("key_list = " + str(key_list))

        estat = Estat(
            percep[key_list[ClauPercepcio.POSICIO.value]],
            percep[key_list[ClauPercepcio.OLOR.value]],
            G_SIZE,
            percep[key_list[ClauPercepcio.PARETS.value]],
        )

        # no lo tengo claro del todo
        if self.__accions is None:
            self._cerca(estat=estat, string="Alvaro")

        if len(self.__accions) > 0:
            if self.__turno > 0:
                self.__turno -= 1
                return AccionsRana.ESPERAR
            else:
                accio = self.__accions[0]
                if accio[0] == AccionsRana.BOTAR:
                    self.__turno = 2
                self.__accions = self.__accions[1:]
                return accio
        return AccionsRana.ESPERAR
