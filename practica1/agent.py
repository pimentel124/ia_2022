"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import agent, entorn
from practica1.entorn import AccionsRana, Direccio, ClauPercepcio
from practica1 import joc


class Rana(joc.Rana):
    def pinta(self, display):
        pass

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass
