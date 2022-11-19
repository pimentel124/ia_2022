from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio

COST_MOURE = 1
COST_ESPERAR = 0.5
COST_BOTAR = 6


class Estat:
    def __init__(self, pos_meta, pos_agent, parets, pes=0, pare=None):
        self.__pare = pare
        self.__pos_meta = pos_meta
        self.__pos_agent = pos_agent
        self.__pes = pes
        self.__parets = parets

    def __eq__(self, other):
        return self.__pos_agent == other.get_pos_agent()

    def __hash__(self):
        return hash(tuple(self.__pos_agent))

    def get_pos_agent(self):
        return self.__pos_agent

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, pare):
        self.__pare = pare

    def calc_heuristica(self, string: str):
        total = 0
        for i in range(2):
            total += abs(self.__pos_meta[i] - self.__pos_agent[string][i])
        return total + self.__pes

    def es_legal(self, string):
        for x in self.__parets:
            if (self.__pos_agent[string][0] == x[0]) and (
                self.__pos_agent[string][1] == x[1]
            ):
                return False

        return (
            (self.__pos_agent[string][0] <= 7)
            and (self.__pos_agent[string][0] >= 0)
            and (self.__pos_agent[string][1] <= 7)
            and (self.__pos_agent[string][1] >= 0)
        )

    # Check si los dos están en la meta
    def es_meta(self, string: str):
        return (self.__pos_agent[string][0] == self.__pos_meta[0]) and (
            self.__pos_agent[string][1] == self.__pos_meta[1]
        )

    def get_pos_meta(self):
        return self.__pos_meta

    def genera_fills(self, string: str):
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
        for i, j in enumerate(diccionari_moviments.values()):
            coordenades = {
                sum(location) for location in zip(self.__pos_agent[string], j)
            }
            cost = self.__pes + COST_MOURE
            actual = Estat(
                self.__pos_meta,
                coordenades,
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
            coordenades = {
                sum(location) for location in zip(self.__pos_agent[string], j)
            }
            cost = self.__pes + COST_BOTAR
            actual = Estat(
                self.__pos_meta,
                coordenades,
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
        self.turno = 0

    def cerca(self, estat: Estat, string: str):
        self.__tancats = set()
        self.__oberts = []

        self.__oberts.append(estat)

        actual = None
        while len(self.__oberts) > 0:

            actual = self.__oberts[0]
            self.__oberts = self.__oberts[1:]
            if actual in self.__tancats:
                continue

            if not actual.es_legal(string):
                continue

            estat_fills = actual.genera_fills(string)

            if actual.es_meta(string):
                break

            for estat_fill in estat_fills:
                self.__oberts.append(estat_fill)

            self.__tancats.add(actual)

        if actual is None:
            raise ValueError("ERR")
        
        if actual.es_meta(string):
            acciones = []
            iterator = actual

            while iterator.pare is not None:
                pare, accion = iterator.pare

                acciones.append(accion)
                iterator = pare
            self.__acciones = acciones
            return True
        else:
            return False


    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        percepciones = percepcio.to_dict()
        key = list(percepciones.keys())
        state = Estat(percepcio[key[0]], percepcio[key[1]], percepcio[key[2]])

        if self.__acciones is None:
            self.cerca(estat=state, string="Miquel")

        if self.__acciones:
            if self.__torn > 0:
                self.__torn -= 1
                return AccionsRana.ESPERAR
            else:
                acc = self.__acciones.pop()
                print("accion:" + str(acc))
                if acc[0] == AccionsRana.BOTAR:
                    self.__torn = 2
                return acc[0], acc[1]
        else:
            return AccionsRana.ESPERAR
