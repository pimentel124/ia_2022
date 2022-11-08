import enum
import random

import pygame

from ia_2022 import agent as agent_lib
from ia_2022 import entorn, joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio


class TipusCas(enum.Enum):
    LLIURE = 0
    PARET = 1


class Rana(agent_lib.Agent):
    random__used = set()

    def __init__(self, nom: str, path_img: str = "../assets/rana/rana.png"):
        super().__init__(long_memoria=1)

        posicio = random.randint(0, 7), random.randint(0, 7)

        while posicio in Laberint.PARETS or posicio in Rana.random__used:
            posicio = random.randint(0, 7), random.randint(0, 7)

        Rana.random__used.add(posicio)
        self.__posicio = posicio
        self.__botant = 0
        self.__dir_bot = None
        self.__nom = nom
        self.__path_img = path_img

    def pinta(self, display):
        pass

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        return AccionsRana.ESPERAR

    @property
    def path_img(self) -> str:
        return self.__path_img

    @property
    def nom(self):
        return self.__nom

    @property
    def posicio(self):
        return self.__posicio

    @posicio.setter
    def posicio(self, val: tuple[int, int]):
        self.__posicio = val

    def start_bot(self, dir_bot):
        self.__dir_bot = dir_bot
        self.__botant = 2

    def fer_bot(self):
        self.__botant -= 1

        return self.__dir_bot

    def esta_botant(self) -> bool:
        return self.__botant > 0


class Casella:
    def __init__(
            self,
            tipus: TipusCas = TipusCas.LLIURE,
            agent: Rana = None,
            menjar: bool = False,
    ):
        self.__tipus = tipus
        self.__agent = agent
        self.__menjar = menjar

    def put_agent(self, agent):
        ha_menjat = self.__menjar
        if self.__menjar:
            self.__menjar = False
        self.__agent = agent

        return ha_menjat

    def pop_agent(self) -> agent_lib.Agent:
        age = self.__agent
        self.__agent = None

        return age

    def pop_menjar(self):
        self.__menjar = None

    def push_menjar(self):
        if self.__tipus is TipusCas.PARET or self.__agent is not None:
            raise ValueError("No pots possar menjar, ja està ocupat")
        self.__menjar = True

    def is_accessible(self):
        return self.__tipus is TipusCas.LLIURE and self.__agent is None

    def is_lliure(self):
        return (
                (self.__tipus is TipusCas.LLIURE)
                and (self.__agent is None)
                and not self.__menjar
        )

    def draw(self, window, x, y):
        pygame.draw.rect(
            window,
            pygame.Color(0, 0, 0),
            pygame.Rect(x * 100, y * 100, 100, 100),
            2 if self.__tipus is TipusCas.LLIURE else 0,
        )
        if self.__agent is not None:
            img = pygame.image.load(self.__agent.path_img)
            img = pygame.transform.scale(img, (100, 100))
            window.blit(img, (x * 100, y * 100))

        if self.__menjar:
            img = pygame.image.load("../assets/rana/pizza.png")
            img = pygame.transform.scale(img, (100, 100))
            window.blit(img, (x * 100, y * 100))


class Laberint(joc.Joc):
    MOVS = {
        Direccio.BAIX: (0, 1),
        Direccio.DRETA: (1, 0),
        Direccio.DALT: (0, -1),
        Direccio.ESQUERRE: (-1, 0),
    }
    PARETS = [(2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (6, 6), (7, 6)]

    def __init__(self, agents: list[Rana], parets=False, mida_taulell: tuple[int, int] = (8, 8)):
        super(Laberint, self).__init__((800, 800), agents, title="Pràctica 1")

        self.__caselles = []
        self.__mida_taulell = mida_taulell
        self.__fer_parets = parets

        for x in range(mida_taulell[0]):
            aux = []
            for y in range(mida_taulell[1]):
                tipus = TipusCas.LLIURE
                if (x, y) in Laberint.PARETS and parets:
                    tipus = TipusCas.PARET
                aux.append(Casella(tipus))
            self.__caselles.append(aux)

        self.__agents = agents
        for a in self.__agents:
            x, y = a.posicio
            self.__caselles[x][y].put_agent(a)

        self.__pos_menjar = self.set_menjar()

    @property
    def posicio_agents(self):
        posicions = {}
        for a in self.__agents:
            posicions[a.nom] = a.posicio

        return posicions

    def set_menjar(self):
        pos_x, pos_y = random.randint(0, 7), random.randint(0, 7)

        while not self.__caselles[pos_x][pos_y].is_lliure():
            pos_x, pos_y = random.randint(0, 7), random.randint(0, 7)

        self.__caselles[pos_x][pos_y].push_menjar()

        return pos_x, pos_y

    @staticmethod
    def _calcula_casella(posicio: tuple[int, int], dir: Direccio, magnitut: int = 1):
        mov = Laberint.MOVS[dir]

        return posicio[0] + (mov[0] * magnitut), posicio[1] + (mov[1] * magnitut)

    def _aplica(
            self, accio: entorn.Accio, params=None, agent_actual: Rana = None
    ) -> None:
        if accio not in AccionsRana:
            raise ValueError(f"Acció no existent en aquest joc: {accio}")

        if accio is not AccionsRana.ESPERAR and (
                params is None or params not in Direccio
        ):
            raise ValueError("Paràmetres incorrectes")

        nc_x, nc_y, oc_x, oc_y = None, None, None, None
        if accio is AccionsRana.BOTAR or agent_actual.esta_botant():
            if agent_actual.esta_botant():
                direccio = agent_actual.fer_bot()
                if not agent_actual.esta_botant():  # bot acabat
                    oc_x, oc_y = agent_actual.posicio
                    nc_x, nc_y = Laberint._calcula_casella((oc_x, oc_y), direccio, 2)
            else:
                agent_actual.start_bot(params)
        elif accio is AccionsRana.MOURE:
            oc_x, oc_y = agent_actual.posicio
            nc_x, nc_y = Laberint._calcula_casella((oc_x, oc_y), params, 1)

        if nc_x is not None:
            if (not (8 > nc_y >= 0)) or (not (8 > nc_x >= 0)):
                raise agent_lib.Trampes()

            if self.__caselles[nc_x][nc_y].is_accessible():
                self.__caselles[oc_x][oc_y].pop_agent()
                ha_menjat = self.__caselles[nc_x][nc_y].put_agent(agent_actual)
                agent_actual.posicio = (nc_x, nc_y)

                if ha_menjat:
                    print(f"Agent {agent_actual.nom} ha guanyat")

    def _draw(self) -> None:
        super(Laberint, self)._draw()
        window = self._game_window
        window.fill(pygame.Color(255, 255, 255))

        for x in range(len(self.__caselles)):
            for y in range(len(self.__caselles[0])):
                self.__caselles[x][y].draw(window, x, y)

    def percepcio(self) -> entorn.Percepcio:
        percep_dict = {
            ClauPercepcio.OLOR: self.__pos_menjar,
            ClauPercepcio.POSICIO: self.posicio_agents,
            ClauPercepcio.MIDA_TAULELL: self.__mida_taulell
        }

        if self.__fer_parets:
            percep_dict[ClauPercepcio.PARETS] = self.PARETS

        return entorn.Percepcio(
            percep_dict
        )
