import pygame

from ia_2022 import agent, entorn, joc
from quiques.entorn import AccionsBarca, ClauPercepcio, Lloc


class Illes(joc.Joc):
    def __init__(self, agents: list[agent.Agent]):
        super(Illes, self).__init__((1024, 512), agents, title="Casa")

        self.__illes = {
            Lloc.ESQ: {"LLOP": 3, "POLL": 3},
            Lloc.DRET: {"LLOP": 0, "POLL": 0},
        }

        self.__localitzacio = Lloc.ESQ

    def _aplica(self, accio: entorn.Accio, params=None, agent_actual=None) -> None:
        if accio not in (AccionsBarca.ATURAR, AccionsBarca.MOURE):
            raise ValueError(f"Acció no existent en aquest joc: {accio}")

        if accio is AccionsBarca.MOURE:
            if params is None or len(params) != 2:
                raise ValueError(
                    "Paràmetres incorrectes: has d'indicar el nombre de llops i polls a moure"
                )

            moviment_polls, moviment_llop = params

            if moviment_llop + moviment_polls > 2:
                raise agent.Trampes()

            self.__illes[self.__localitzacio]["LLOP"] -= moviment_llop
            self.__illes[-self.__localitzacio]["LLOP"] += moviment_llop

            self.__illes[self.__localitzacio]["POLL"] -= moviment_polls
            self.__illes[-self.__localitzacio]["POLL"] += moviment_polls

            self.__localitzacio = -self.__localitzacio

            for illa in self.__illes.values():
                if (illa["LLOP"] > illa["POLL"]) and (illa["POLL"] != 0):
                    raise joc.HasPerdut("Els llops s'han menjat els polls")

    def _draw(self) -> None:
        super(Illes, self)._draw()
        window = self._game_window
        window.fill(pygame.Color(88, 189, 247))

        pygame.draw.rect(
            window, pygame.Color(5, 243, 255), pygame.Rect(0, 256, 1024, 256)
        )
        img = pygame.image.load("../assets/llop/illa.png")
        img = pygame.transform.scale(img, (200, 200))
        window.blit(img, (20, 150))

        img = pygame.image.load("../assets/llop/illa-r.png")
        img = pygame.transform.scale(img, (200, 200))
        window.blit(img, (824, 150))

        barca = pygame.image.load("../assets/llop/barca.png")
        barca = pygame.transform.scale(barca, (100, 100))

        if self.__localitzacio is Lloc.ESQ:
            window.blit(barca, (240, 250))
        else:
            window.blit(barca, (824 - 100, 250))

        llop = pygame.image.load("../assets/llop/llop.png")
        llop = pygame.transform.scale(llop, (100, 50))

        poll = pygame.image.load("../assets/llop/gallina.png")
        poll = pygame.transform.scale(poll, (50, 50))

        for i, illa in enumerate(self.__illes.values()):
            for i_llop in range(illa["LLOP"]):
                if i == 0:
                    window.blit(llop, (20 + (i_llop * 25), 300))
                else:
                    window.blit(llop, (824 - (i_llop * 25), 300))
            for i_poll in range(illa["POLL"]):
                if i == 0:
                    window.blit(poll, (20 + (i_poll * 25), 300))
                else:
                    window.blit(poll, (824 - (i_poll * 25), 300))

    def percepcio(self) -> entorn.Percepcio:
        return entorn.Percepcio(
            {
                ClauPercepcio.LLOC: self.__localitzacio,
                ClauPercepcio.QUICA_ESQ: self.__illes[Lloc.ESQ]["POLL"],
                ClauPercepcio.LLOP_ESQ: self.__illes[Lloc.ESQ]["LLOP"],
                ClauPercepcio.QUICA_DRETA: self.__illes[Lloc.DRET]["POLL"],
                ClauPercepcio.LLOP_DRETA: self.__illes[Lloc.DRET]["LLOP"],
            }
        )
