from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio

COST_MOURE = 1
COST_ESPERAR = 0.5
COST_BOTAR = 6


class Estat:
    def __init__(self, pos_meta, pos_agent, parets, rana_Max, pes=0, pare=None):
        self.__pare = pare
        self.__rana_max = rana_Max
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
    
    def get_othername(self):
        claus = list(self.__pos_agent.keys())  # {Alvaro: (),Andreu: ();

        for i in range(2):
            if (self.__rana_max != claus[i]):
                return claus[i]

        return None

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
        return total+self.__pes
    
    def es_legal(self):
        for x in self.__parets:
            if (self.__pos_agent[self.get_othername()][0] == x[0]) and (self.__pos_agent[self.get_othername()][1] == x[1]):
                return False

        return (self.__pos_agent[self.get_othername()][0] <= 7) and (self.__pos_agent[self.get_othername()][0] >= 0) \
               and (self.__pos_agent[self.get_othername()][1] <= 7) and (self.__pos_agent[self.get_othername()][1] >= 0)
    
    
    #Check si los dos están en la meta
    def es_meta(self, string: str):
        return (self.__pos_agent[string][0] == self.__pos_meta[0]) and (self.__pos_agent[string][1] == self.__pos_meta[1])
    
    def get_pos_meta(self):
        return self.__pos_meta
    
    def genera_fills(self):
        claves = list(self.__pos_agent.keys())
        if self.__rana_max == claves[0]:
            nom_rana = claves[1]
        else:
            nom_rana = claves[0]
        fills = []
        #generate dicctionary
        diccionari_moviments = {"DALT": (0, -1),
                                "BAIX": (0, +1),
                                "ESQUERRE": (-1, 0),
                                "DRETA": (+1, 0) }
        
        
        #en el caso de movimientos normales
        claus = list(diccionari_moviments.keys())
        for i, j in enumerate(diccionari_moviments.values()):
            coordenades = {sum(location) for location in zip(self.__pos_agent[self.__rana_max], j)}
            cost = self.__pes + COST_MOURE
            actual = Estat(self.__pos_meta, coordenades, self.__parets, nom_rana, cost, (self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i]))))
            if actual.es_legal():
                fills.append(actual)
        
        #en el caso de saltos       
        diccionari_bots = {"DALT": (0, -2),
                           "BAIX": (0, +2),
                           "ESQUERRE": (-2, 0),
                           "DRETA": (+2, 0) }
        
        claus = list(diccionari_bots.keys())
        for i, j in enumerate(diccionari_bots.values()):
            coordenades = {sum(location) for location in zip(self.__pos_agent[self.__rana_max], j)}
            cost = self.__pes + COST_BOTAR
            actual = Estat(self.__pos_meta, coordenades, self.__parets, nom_rana, cost, (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))))
            if actual.es_legal():
                fills.append(actual)
                
        return fills

class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None
    
    
    def minimax(self, estat:Estat, turno_max: bool, recurs: int):

        score = estat.calc_heuristica(self.nom)
        if recurs == 3 or estat.es_meta(self.nom):
            return score, estat
        point_fills = [self.minimax(estat_fill, not turno_max, recurs+1) for estat_fill in estat.genera_fills()]
        if turno_max:
            return max(point_fills)
        else:
            return min(point_fills)
    #El max i el min els programam per a poder agafar el de la primera part que representa el valor
    def max(self, llista):
        max = 0
        element = None
        for e in llista:
            if (e[1] > max):
                max = e[1]
                element = e

        return max, element

    def min(self, llista):
        min = 9999
        element = None
        for e in llista:
            if (e[1] < min):
                min = e[1]
                element = e

        return min, element

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

            percepciones = percep.to_dict()
            key = list(percepciones.keys())

            state = Estat(percep[key[0]], percep[key[1]], percep[key[2]], self.nom)

            #Obtenemos la mejor opción según lo que diga el minmax
            now = self.minimax(estat=state, turno_max=True, recurs=0)

            agents=percep[key[1]].keys()
            for a in agents:
                if (percep[key[1]][a] == percep[key[0]]):
                    self.META = 1

            if self.META==1:
                return AccionsRana.ESPERAR

            decision = now[1]
            pare, accio = decision.pare
            decision = pare

            if(self.__torn>0):
                self.__torn-=1
                return AccionsRana.ESPERAR
            else:
                #print("accion:"+str(accio))
                if(accio[0]==AccionsRana.BOTAR):
                    self.__torn=2
                    #retornam acció i direcció
                return accio[0],accio[1]
