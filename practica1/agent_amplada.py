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
    
    def get_pos_meta(self):
        return self.__pos_meta
    
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
    
    def es_legal(self, string: str):
        for x in self.__parets:
            if (self.__pos_agent[string][0] == x[0]) and (self.__pos_agent[string][1] == x[1]):
                return False

        return (self.__pos_agent[string][0] <= 7) and (self.__pos_agent[string][0] >= 0) \
               and (self.__pos_agent[string][1] <= 7) and (self.__pos_agent[string][1] >= 0)
    
    
    #Check si los dos están en la meta
    def es_meta(self, string: str):
        return (self.__pos_agent[string][0] == self.__pos_meta[0]) and (self.__pos_agent[string][1] == self.__pos_meta[1])
        
    
    def genera_fills(self, string: str):
        fills = []
        #generate dicctionary
        diccionari_moviments = {"DALT": (0, -1),
                                "BAIX": (0, +1),
                                "ESQUERRE": (-1, 0),
                                "DRETA": (+1, 0) }
        
        
        #en el caso de movimientos normales
        claus = list(diccionari_moviments.keys())
        for i, j in enumerate(claus.values()):
            coordenades = {string: sum(location) for location in zip(self.__pos_agent[string], j)}
            cost = self.__pes + COST_MOURE
            actual = Estat(self.__pos_meta, coordenades, self.__parets, cost, (self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i]))))
            if actual.es_legal(string):
                fills.append(actual)
        
        #en el caso de saltos       
        diccionari_bots = {"DALT": (0, -2),
                           "BAIX": (0, +2),
                           "ESQUERRE": (-2, 0),
                           "DRETA": (+2, 0) }
        
        claus = list(diccionari_bots.keys())
        for i, j in enumerate(claus.values):
            coordenades = {string: sum(location) for location in zip(self.__pos_agent[string], j)}
            cost = self.__pes + COST_BOTAR
            actual = Estat(self.__pos_meta, coordenades, self.__parets, cost, (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))))
            if actual.es_legal(string):
                fills.append(actual)
                
        return fills

class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None
    
    def _cerca(self, estat: Estat, string: str):
        self.__oberts = []
        self.__tancats = set()
        
        self.__oberts.append(estat)
        actual = None
        while len(self.__oberts) > 0:
            actual = self.__oberts[0]
            self.__oberts = self.__oberts[1:]
            
            if actual in self.__tancats:
                continue
            
            estats_fills = actual.genera_fill()
            
            if actual.es_meta():
                break
            
            for estat_f in estats_fills:
                self.__oberts.append(estat_f)
            
            self.__tancats.add(actual)
        if actual is None:
            raise ValueError("Error impossible")
        if actual.es_meta():
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
        percepcions = percep.to_dict()
        key_list = list(percepcions.keys())
        estat = Estat(percep[key_list[0]], percep[key_list[1]], percep[key_list[2]])
        
        
        #no lo tengo claro del todo
        if self.__accions is None:
            self._cerca(estat=estat)
        if self.__accions is not None:
            accio = self.__accions[0]
            self.__accions = self.__accions[1:]
            return accio
        return AccionsRana.ESPERAR

