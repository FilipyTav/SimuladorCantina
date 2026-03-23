from pqueue import PQueue
from enum import Enum, auto
import os


def screen_clear():
    os.system("cls" if os.name == "nt" else "clear")


class Screen(Enum):
    MAIN = auto()

    ADMIN = auto()

    CLIENT = auto()
    CLIENT_BUY = auto()

    BACK = auto()
    EXIT = auto()


def menu_admin() -> Screen:
    return Screen.MAIN


# Returns if the program should exit
def menu_client() -> Screen:
    print("\n" + "=" * 40)
    print("\t--- CANTINA ---")
    print("  --- Bem-vindo(a), Cliente! ---")
    print("=" * 40)

    print("Como prosseguir?\n")
    print("0. Voltar")
    print("1. Ver estoque")
    print("q. Sair")

    choice = input("\nEscolha uma opção: ")

    match choice:
        case "0":
            return Screen.BACK

        case "1":
            return Screen.CLIENT_BUY

        case "q":
            return Screen.EXIT

        case _:
            print("Essa não é uma opção. Tente novamente")
            return Screen.CLIENT
