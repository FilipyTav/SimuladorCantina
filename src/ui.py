from payment import Payment, process_sale
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


def print_prods_screen(stock: PQueue) -> None:
    print("\n" + "=" * 40)
    print("\t--- Estoque ---")
    print("=" * 40)
    stock.print_for_client()


def menu_client_buy(stock: PQueue) -> Screen:
    print_prods_screen(stock)

    while True:
        print("Escolha o que deseja comprar.")
        print("Formato: ID.quantidade, separados por espaço. Ex.: 0.2, 3.4")
        print("E. Mostrar estoque")
        print("B. Voltar ao menu anterior")

        choice: str = input("> ").strip()
        if choice == "b":
            return Screen.BACK
        elif choice == "e":
            print_prods_screen(stock)
            return Screen.CLIENT_BUY
        elif choice == "q":
            return Screen.EXIT

        try:
            print()
            parts: str = choice.replace(" ", "")
            if not parts:
                raise ValueError("Entrada vazia.")

            s: list[str] = parts.split(",")
            for item in s:
                if "." not in item:
                    raise ValueError(
                        f"Item '{item}' está fora do formato ID.quantidade"
                    )

            prods: dict[int, int] = {}
            for p in s:
                k, v = p.split(".")
                prods[int(k)] = int(v)

            payment: Payment | None = process_sale(
                prods, ("TTTTTTTT", "aluno", "IA"), stock, True
            )

            if payment:
                screen_clear()
                print("Compra confirmada!")
                payment.print_for_client()

            print()
        except ValueError:
            print(
                "[!] Entrada inválida. Use apenas números no formato ID.quantidade separados por vírgula. [!]"
            )
            print("[Exemplo correto: 1.5, 2.10]\n")

    return Screen.CLIENT_BUY
