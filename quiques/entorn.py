""" Fitxer amb tota la informació de l'entorn de l'aspirador.

Autor: Miquel Miró Nicolau (UIB), 2022
"""

import enum

from ia_2022 import entorn


class ClauPercepcio(enum.Enum):
    QUICA_DRETA = 0
    LLOP_DRETA = 1
    LLOC = 2
    QUICA_ESQ = 3
    LLOP_ESQ = 4


class Lloc(enum.Enum):
    ESQ = 0
    DRET = 1

    def __neg__(self):
        if self is Lloc.ESQ:
            return Lloc.DRET
        else:
            return Lloc.ESQ

    def __hash__(self):
        return self.value


class AccionsBarca(entorn.Accio, enum.Enum):
    MOURE = 0
    ATURAR = 1
