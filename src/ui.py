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


def main_menu() -> Screen:
    print("\n" + "=" * 40)
    print("\t--- CANTINA ---")
    print("=" * 40)

    print("Que usuário usar?\n")

    print("1. Admin")
    print("2. Cliente")
    print("q. Sair")

    choice: str = input("\nEscolha uma opção: ").strip().lower()

    match choice:
        case "1":
            return Screen.ADMIN
        case "2":
            return Screen.CLIENT
        case "q":
            return Screen.EXIT
        case _:
            print("Opção inválida! Escolha 1, 2 ou q.")
            return Screen.MAIN


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

    choice: str = input("\nEscolha uma opção: ")

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


def menu_client_buy(stock: PQueue) -> Screen:
    print("\n" + "=" * 40)
    print("\t--- Estoque ---")
    print("=" * 40)
    stock.print_for_client()

    print("Escolha o que deseja comprar.")
    print("Formato: ID.quantidade, separados por espaço. Ex.: 0.2, 3.4")
    print("Ou pressione 'b' para voltar ao menu anterior")

    choice: str = input("> ").strip()
    if choice == "b":
        return Screen.BACK

    choice = choice.replace(" ", "")
    s: list[str] = choice.split(",")
    prods: dict[int, int] = {}
    for p in s:
        k, v = p.split(".")
        k = int(k)
        v = int(v)
        prods[k] = v

    print(prods)

    return Screen.CLIENT_BUY
