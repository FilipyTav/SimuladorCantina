from pqueue import PQueue
from enum import Enum, auto


class Screen(Enum):
    MAIN = auto()
    ADMIN = auto()
    CLIENT = auto()
    CLIENT_BUY = auto()
    EXIT = auto()


def menu_admin():
    return


# Returns if the program should exit
def menu_client(stock: PQueue) -> Screen:
    print("\n" + "=" * 40)
    print("\t--- CANTINA ---")
    print("  --- Bem-vindo(a), Cliente! ---")
    print("=" * 40)

    print("\nComo prosseguir?")
    print("1. Ver estoque")
    print("q. Sair")

    choice = input("\nEscolha uma opção: ")

    match choice:
        case "1":
            print("Should be")
            return Screen.CLIENT_BUY

        case "q":
            print("Should back")
            return Screen.MAIN

        case _:
            print("Essa não é uma opção. Tente novamente")
            return Screen.CLIENT
