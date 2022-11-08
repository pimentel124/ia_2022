from ia_2022 import entorn
from practica1.agent import Rana, Estat
from practica1.entorn import AccionsRana

class RanaAmplada(Rana):
    def __init__(self):
        super(RanaAmplada, self).__init__()
        self.__oberts = None
        self.__tancats = None
        self.__accions = None
    
    def _cerca(self, estat: Estat):
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
        estat = Estat(percep.to_dict())
        
        
        #no lo tengo claro del todo
        if self.__accions is None:
            self._cerca(estat=estat)
        if self.__accions is not None:
            accio = self.__accions[0]
            self.__accions = self.__accions[1:]
            return accio
        return AccionsRana.ESPERAR
     