# lint_ignore=E501

import sys
from pathlib import Path


DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(DIR))


from practica1 import agent_amplada, joc


def main():
    rana1 = agent_amplada.Rana("Alvaro")
    rana2 = agent_amplada.Rana("Andreu")
    lab = joc.Laberint([rana1, rana2], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
