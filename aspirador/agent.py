""" Fitxer que conté els diferents agents aspiradors.

Percepcions:
    ClauPercepcio.LOC: [Localitzacio.HABITACIO_ESQ, Localitzacio.HABITACIO_DRET]
    ClauPercepcio.ESTAT: [EstatHabitacio.NET, EstatHabitacio.BRUT]

Accions:
    AccionsAspirador.DRETA
    AccionsAspirador.ESQUERRA
    AccionsAspirador.ATURA
    AccionsAspirador.ASPIRA

Autor: Miquel Miró Nicolau (UIB), 2022
"""
import abc

import pygame

from aspirador.entorn import (AccionsAspirador, ClauPercepcio, EstatHabitacio,
                              Localitzacio)
from ia_2022 import agent
from ia_2022 import entorn


class Aspirador(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        img = pygame.image.load("../assets/aspirador/sprite.png")
        img = pygame.transform.scale(img, (100, 100))
        display.blit(img, self._posicio_pintar)

    @abc.abstractmethod
    def actua(self, percep: entorn.Percepcio) -> entorn.Accio:
        pass


class AspiradorReflex(Aspirador):
    def actua(self, percep: entorn.Percepcio) -> entorn.Accio:
        """ IMPLEMENTAR """
        pass


class AspiradorTaula(Aspirador):
    TAULA = {
        (Localitzacio.HABITACIO_ESQ, EstatHabitacio.NET): AccionsAspirador.DRETA,
        (Localitzacio.HABITACIO_ESQ, EstatHabitacio.BRUT): AccionsAspirador.ASPIRA,
        (Localitzacio.HABITACIO_DRET, EstatHabitacio.NET): AccionsAspirador.ESQUERRA,
        (Localitzacio.HABITACIO_DRET, EstatHabitacio.BRUT): AccionsAspirador.ASPIRA,
    }

    def actua(self, percep: entorn.Percepcio) -> entorn.Accio:
        return AspiradorTaula.TAULA[
            (percep[ClauPercepcio.LOC], percep[ClauPercepcio.ESTAT])
        ]


class AspiradorMemoria(Aspirador):
    def actua(self, percep: entorn.Percepcio) -> entorn.Accio:
        """ IMPLEMENTAR """
        pass