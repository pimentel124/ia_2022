import enum

from ia_2022 import entorn


class ClauPercepcio(enum.Enum):
    POSICIO = 0
    OLOR = 1
    PARETS = 2


class AccionsRana(entorn.Accio, enum.Enum):
    MOURE = 0
    ESPERAR = 1
    BOTAR = 2


class Direccio(enum.Enum):
    ESQUERRE = 0
    DRETA = 1
    DALT = 2
    BAIX = 3
