import random

import pygame

from aspirador.entorn import (
    AccionsAspirador,
    ClauPercepcio,
    EstatHabitacio,
    Localitzacio,
)
from ia_2022 import agent, entorn, joc


class AspiradorRomput(Exception):
    """Excepció aixecada quan l'aspirador es romp."""

    def __init__(self):
        self.message = "L'aspirador ha caigut i s'ha romput"
        super().__init__(self.message)


class Casa(joc.Joc):
    """Accions disponibles:
    - AccionsAspirador.ASPIRA
    - AccionsAspirador.DRETA
    - AccionsAspirador.ESQUERRA
    - AccionsAspirador.ATURA
    """

    def __init__(self, agents: list[agent.Agent]):
        super(Casa, self).__init__((512, 512), agents, title="Casa")

        self.__habitacions = {
            Localitzacio.HABITACIO_ESQ: EstatHabitacio.aleatori(),
            Localitzacio.HABITACIO_DRET: EstatHabitacio.aleatori(),
        }

        self.__localitzacio = Localitzacio.aleatori()

    def _aplica(self, accio: entorn.Accio, params=None, agent_actual=None) -> None:
        if accio is AccionsAspirador.ASPIRA:
            self.__habitacions[self.__localitzacio] = EstatHabitacio.NET
        elif accio is AccionsAspirador.DRETA:
            if self.__localitzacio is Localitzacio.HABITACIO_DRET:
                raise AspiradorRomput
            self.__localitzacio = Localitzacio.HABITACIO_DRET
        elif accio is AccionsAspirador.ESQUERRA:
            if self.__localitzacio is Localitzacio.HABITACIO_ESQ:
                raise AspiradorRomput
            self.__localitzacio = Localitzacio.HABITACIO_ESQ
        elif accio is AccionsAspirador.ATURA:
            pass
        else:
            raise Exception(f"Acció no existent en aquest joc: {accio}")

    def _draw(self) -> None:
        super(Casa, self)._draw()
        window = self._game_window
        window.fill(pygame.Color(255, 255, 255))
        pygame.draw.line(
            window,
            pygame.Color(0, 0, 0),
            (self._mida_pantalla[0] // 2, 0),
            (self._mida_pantalla[0] // 2, self._mida_pantalla[1]),
            2,
        )

        for i, hab in enumerate(self.__habitacions.values()):
            if hab is EstatHabitacio.BRUT:
                pygame.draw.rect(
                    window,
                    pygame.Color(0, 0, 0),
                    pygame.Rect((i * self._mida_pantalla[0] // 2) + 50, 50, 10, 10),
                )

        for a in self._agents:
            if self.__localitzacio is Localitzacio.HABITACIO_ESQ:
                a.set_posicio((50, self._mida_pantalla[1] // 2))
            else:
                a.set_posicio(
                    ((self._mida_pantalla[0] // 2) + 50, self._mida_pantalla[1] // 2)
                )
            a.pinta(window)

    def percepcio(self) -> entorn.Percepcio:
        return entorn.Percepcio(
            {
                ClauPercepcio.LOC: self.__localitzacio,
                ClauPercepcio.ESTAT: self.__habitacions[self.__localitzacio],
            }
        )


class HabitacioView:
    pass


class Casal(joc.Joc):
    def __init__(self, agents: list[agent.Agent], mida_casa: tuple[int, int]):
        super(Casa, self).__init__((512, 512), agents, title="Casal")

        self.__habitacions = [
            [EstatHabitacio.aleatori() for _ in range(mida_casa[0])]
            for _ in range(mida_casa[1])
        ]

        self.__localitzacio = random.randint(0, mida_casa[0] * mida_casa[1])
