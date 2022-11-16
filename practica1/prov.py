
"""
CONSTANTS PER MOURE I ELS REUS COSTOS
"""
COST_DESPL = 1
COST_ESPERAR = 0.5
COST_BOTAR = 6

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio
from queue import PriorityQueue

class Estat:
    def __init__(self,posPizza,posAgent,parets,pes=0,pare=None):
        self.__pos_ag = posAgent
        self.__pos_pizza = posPizza
        self.__parets = parets
        self.__pes = pes
        self.__pare = pare

    def __eq__(self, other):
        return self.__pos_ag == other.get_pos_ag()
    def __lt__(self, other):
        return False
    def __hash__(self):
        return hash(tuple(self.__pos_ag))

    def get_pos_ag(self):
        return self.__pos_ag

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value


    def calcula_heuristica(self,string: str):
        sum=0
        for i in range(2):
            sum+=abs(self.__pos_pizza[i] - self.__pos_ag[string][i])
        return self.__pes+sum

    def es_valid(self,string: str):
        #claus = list(self.__pos_ag.keys())
        # mirar si hi ha parets
        for x in self.__parets:
            if (self.__pos_ag[string][0] == x[0]) and (self.__pos_ag[string][1] == x[1]):
                return False

        return (self.__pos_ag[string][0] <= 7) and (self.__pos_ag[string][0] >= 0) \
               and (self.__pos_ag[string][1] <= 7) and (self.__pos_ag[string][1] >= 0)
               
    #explain what the es_valid function does
    #the es_valid function checks if the position of the agent is valid, that is, if it is not in a wall

    def es_meta(self,string: str):
        return (self.__pos_ag[string][0] == self.__pos_pizza[0])and(self.__pos_ag[string][1] == self.__pos_pizza[1])

    def get_pos_pizza(self):
        return self.__pos_pizza

    def genera_fills(self,string: str):
        fills = []
        print(str(self.__pos_ag)+": pos padre")
        #Moviments
        movs={"ESQUERRE":(-1,0),"DRETA":(+1,0), "DALT": (0,-1), "BAIX": (0,+1)}
        claus=list(movs.keys())
        for i, m in enumerate(movs.values()):
            coords = [sum(tup) for tup in zip(self.__pos_ag[string], m)]
            coord = {string: coords}
            cost = self.__pes + COST_DESPL
            print(coord)
            actual = Estat(self.__pos_pizza, coord, self.__parets, cost,
                           (self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i]))))
            if (actual.es_valid(string)):
                fills.append(actual)

        #BOTS
        movs = {"ESQUERRE": (-2,0),"DRETA": (+2,0), "DALT": (0,-2), "BAIX": (0,+2)}
        claus = list(movs.keys())
        for i, m in enumerate(movs.values()):
            coords = [sum(tup) for tup in zip(self.__pos_ag[string], m)]
            coord = {string: coords}
            cost = self.__pes + COST_BOTAR
            print(coord)
            actual = Estat(self.__pos_pizza, coord, self.__parets, cost,
                           (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))))
            if (actual.es_valid(string)):
                fills.append(actual)

        return fills



class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__tancats = None
        self.__oberts = None
        self.__accions = None
        self.__torn = 0

    def pinta(self, display):
        pass

    def cerca_prof(self, estat: Estat, string:str):
        self.__oberts = []
        self.__tancats = set()

        self.__oberts.append(estat)

        actual = None
        while len(self.__oberts) > 0:

            actual = self.__oberts[0]
            self.__oberts = self.__oberts[1:]
            if actual in self.__tancats:
                continue

            if not actual.es_valid(string):
                self.__tancats.add(actual)
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
        else:
            return False


    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

            percepciones = percep.to_dict()
            key = list(percepciones.keys())
            state = Estat(percep[key[0]],percep[key[1]], percep[key[2]])

            if self.__accions is None:
                self.cerca_prof(estat=state,string='Miquel')

            if self.__accions:
                if(self.__torn>0):
                    self.__torn-=1
                    return AccionsRana.ESPERAR
                else:
                    acc=self.__accions.pop()
                    print("accion:"+str(acc))
                    if(acc[0]==AccionsRana.BOTAR):
                        self.__torn=2
                    #retornam acció i direcció
                    return acc[0],acc[1]
            else:
                return AccionsRana.ESPERAR