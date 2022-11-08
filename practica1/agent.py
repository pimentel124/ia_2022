"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
    MIDA_TAULELL = 3
    
    

"""

import abc
import itertools

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio

COST_MOURE = 1
COST_ESPERAR = 0.5
COST_BOTAR = 6


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

    def pinta(self, display):
        print(self._posicio_pintar)
        
    @abc.abstractmethod
    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass

class Estat:
    
    #falta limitar las acciones
    acc_poss = [
        acc for acc in itertools.product([0, 1, 2], [0, 1, 2])
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
        return (
            self[ClauPercepcio.POSICIO] == other[ClauPercepcio.POSICIO]
            and self[ClauPercepcio.OLOR] == other[ClauPercepcio.OLOR]
            and self[ClauPercepcio.PARETS] == other[ClauPercepcio.PARETS]
            and self[ClauPercepcio.MIDA_TAULELL] == other[ClauPercepcio.MIDA_TAULELL]
        )
        
    def legal(self) -> bool:
        return True
        