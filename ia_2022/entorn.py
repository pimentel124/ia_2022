import enum


class Accio(enum.Enum):
    pass


class Percepcio:
    def __init__(self, percepcions: dict[enum.Enum, enum.Enum]):
        self.__percepcions = percepcions

    def __getitem__(self, key):
        return self.__percepcions[key]

    def to_dict(self):
        return self.__percepcions
