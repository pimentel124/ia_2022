import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(DIR))

from practica1 import agent, joc


def main():
    rana = agent.Rana("Miquel")
    lab = joc.Laberint([rana], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
