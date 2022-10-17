""" Fitxer amb tota la informació de l'entorn de l'aspirador.

Autor: Miquel Miró Nicolau (UIB), 2022
"""

import enum

from ia_2022 import entorn


class ClauPercepcio(enum.Enum):
    MONEDES = 0


class AccionsMoneda(entorn.Accio, enum.Enum):
    DESPLACAR = 0
    GIRAR = 1
    BOTAR = 2
    RES = 3
