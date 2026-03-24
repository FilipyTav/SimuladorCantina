from payment import (
    COURSES_AVAILABLE,
    USERS_CATEGORIES,
    Payment,
    process_sale,
    userInfo,
)
from payment_history import PaymentLedger
from pqueue import PQueue
from enum import Enum, auto
import os

from product import Product
from utils.input import get_valid_date, get_valid_index, get_valid_int, get_valid_price


def screen_clear():
    os.system("cls" if os.name == "nt" else "clear")


class Screen(Enum):
    # Admin
    # ------------------------
    ADMIN = auto()
    ADMIN_BUY = auto()
    ADMIN_SEE_STOCK = auto()
    ADMIN_UPDATE_STOCK = auto()
    ADMIN_SEE_PAYMENTS = auto()
    ADMIN_REPORTS = auto()
    # ------------------------

    # Client
    # ------------------------
    CLIENT = auto()
    CLIENT_BUY = auto()
    CLIENT_ASK_INFO = auto()
    # ------------------------

    # Helpers
    # ------------------------
    MAIN = auto()
    BACK = auto()
    EXIT = auto()
    # ------------------------


def main_menu() -> Screen:
    print("\n" + "=" * 40)
    print("\t--- CANTINA ---")
    print("=" * 40)

    print("Que usuário usar?\n")

    print("1. Admin")
    print("2. Cliente")
    print("Q. Sair")

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


# Admin
# ------------------------------------------------
def menu_admin() -> Screen:
    print("\n" + "=" * 40)
    print("--- PAINEL ADMINISTRADOR ---")
    print("=" * 40)

    print("Como prosseguir?\n")
    print(
        f"0. Voltar\n"
        f"1. Ver estoque\n"
        f"2. Adicionar ao estoque\n"
        f"3. Mostrar vendas\n"
        f"4. Relatório de vendas\n"
        f"Q. Sair\n"
    )
    choice: str = input("> ").strip().lower()

    match choice:
        case "q":
            return Screen.EXIT

        case "0":
            return Screen.BACK

        case "1":
            return Screen.ADMIN_SEE_STOCK

        case "2":
            return Screen.ADMIN_BUY

        case "3":
            return Screen.ADMIN_SEE_PAYMENTS

        case "4":
            return Screen.ADMIN_REPORTS

        case _:
            return Screen.BACK

    return Screen.MAIN


def menu_admin_buy(prods_available: PQueue) -> Screen:
    print_prods_screen(prods_available, True)

    while True:
        print("Escolha o que deseja comprar.")
        print("Formato: ID.quantidade, separados por espaço. Ex.: 0.2, 3.4")
        print("E. Mostrar produtos disponíveis")
        print("B. Voltar ao menu anterior")
        # (∞)
        choice: str = input("> ").strip()
        if choice == "b":
            return Screen.BACK
        elif choice == "e":
            print_prods_screen(prods_available)
            return Screen.ADMIN_BUY
        elif choice == "q":
            return Screen.EXIT

        try:
            print()
            parts: str = choice
            if not parts:
                raise ValueError("Entrada vazia.")

            s: list[str] = parts.split(" ")
            for item in s:
                if "." not in item:
                    raise ValueError(
                        f"Item '{item}' está fora do formato ID.quantidade"
                    )

            prods_dict: dict[int, int] = {}
            for p in s:
                k, v = p.split(".")
                prods_dict[int(k)] = int(v)

            products: list[Product] = prods_available.get_by_ids(set(prods_dict.keys()))
            for p in products:
                p.set_amount(p.get_amount() + prods_dict[p.get_id()])
                print(
                    f"Item '{p.get_name()}' (ID: {p.get_id()}) -> +{prods_dict[p.get_id()]} unidade(s)"
                )

            print()
        except ValueError:
            print(
                "[!] Entrada inválida. Use apenas números no formato ID.quantidade separados por espaço. [!]"
            )
            print("[Exemplo correto: 1.5 2.10]\n")

    return Screen.ADMIN_BUY


def menu_admin_stock(stock: PQueue) -> Screen:
    while True:
        print_prods_screen(stock)

        print(
            f"Escolha o que deseja fazer:\n"
            f"0. Voltar ao menu anterior\n"
            f"1. Mostrar estoque\n"
            f"2. Modificar estoque\n"
        )

        choice: str = input("> ").strip()
        match choice:
            case "0":
                return Screen.BACK
            case "1":
                print_prods_screen(stock)
                return Screen.ADMIN_SEE_STOCK
            case "2":
                return Screen.ADMIN_UPDATE_STOCK
            case "q":
                return Screen.EXIT
            case _:
                return Screen.ADMIN_SEE_STOCK

    return Screen.BACK


def menu_admin_see_payments(ledger: PaymentLedger) -> Screen:
    while True:
        screen_clear()
        ledger.print_admin()
        print(f"B. Voltar ao menu anterior")
        choice: str = input("> ").strip().lower()
        match choice:
            case "b":
                return Screen.BACK

            case "q":
                return Screen.EXIT

        return Screen.BACK


def modify_prod(p: Product) -> bool:
    attributes: dict[str, str] = p.get_attributes()
    while True:
        screen_clear()
        print("\n" + "=" * 30)
        p.print_admin()
        print("=" * 30)

        options = list(attributes.keys())
        menu_opcoes = " | ".join([f"{i}. {op}" for i, op in enumerate(options)])

        print(f"\nModificando: {p.name} (ID: {p.id})")
        print(f"{menu_opcoes} | C. Cancelar | S. Próximo/Sair")

        op: str = input("Selecione o campo: ").strip().lower()
        new_val: str = ""

        match op:
            case "c":
                return False

            case "s":
                break

            # Nome
            case "0":
                new_val = input("Novo nome: ")
                p.set_name(new_val)

            # Preço de compra
            case "1":
                p.set_buy_price(get_valid_price("Novo preço de compra(R$): "))

            # Preço de venda
            case "2":
                p.set_sell_price(get_valid_price("Novo preço de venda(R$): "))

            # 3. Data compra
            case "3":
                p.set_dtbuy(get_valid_date("Nova data de compra: "))

            # 4. Data validade
            case "4":
                p.set_dtexp(get_valid_date("Nova data de validade: "))

            # Quantidade
            case "5":
                p.set_amount(get_valid_int("Nova quantidade: ", min=0, max=999999))

            case _:
                continue

    return True


def menu_admin_update_stock(stock: PQueue) -> Screen:
    print_prods_screen(stock)

    while True:
        print(
            f"Escolha os IDs dos produtos que deseja modificar, separados pro espaço:"
        )

        choice: str = input("> ").strip()

        if not choice:
            print("\n[!] Erro: Você deve digitar ao menos um ID. [!]\n")
            continue

        match choice:
            case "b":
                return Screen.BACK
            case "q":
                return Screen.EXIT

        ids: list[int] = []
        try:
            ids = [int(s.strip()) for s in choice.split(" ") if s.strip()]

            if not ids:
                raise ValueError

        except ValueError:
            print(
                "\n[!] Erro: Digite apenas NÚMEROS separados por espaço (ex: 1  2  5).\n"
            )
            continue

        prods: list[Product] = stock.get_by_ids(set(ids))

        if len(prods) != len(ids):
            missing: set[int] = set(ids) - {pr.get_id() for pr in prods}
            print(f"[!] Erro: Os seguintes IDs de produto não existem: {missing} [!]\n")
            continue

        for p in prods:
            if not modify_prod(p):
                break

        print("\nTodas as edições da lista foram concluídas.\n")

        return Screen.ADMIN_UPDATE_STOCK

    return Screen.BACK


# ------------------------------------------------


# Client
# ------------------------------------------------
def menu_client(client_name: str) -> Screen:
    print("\n" + "=" * 40)
    print("\t--- CANTINA ---")
    print(f"  --- Bem-vindo(a), {client_name.capitalize()}! ---")
    print("=" * 40)

    print("Como prosseguir?\n")
    print("0. Voltar")
    print("1. Ver estoque")
    print("Q. Sair")

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


def menu_client_buy(
    stock: PQueue, ledger: PaymentLedger, user_info: userInfo
) -> Screen:
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

            payment: Payment | None = process_sale(prods, user_info, stock, True)

            if payment:
                screen_clear()
                print("Compra confirmada!")
                ledger.push(payment)
                payment.print_for_client()

            print()
        except ValueError:
            print(
                "[!] Entrada inválida. Use apenas números no formato ID.quantidade separados por vírgula. [!]"
            )
            print("[Exemplo correto: 1.5, 2.10]\n")

    return Screen.CLIENT_BUY


def menu_client_get_info() -> tuple[Screen, userInfo]:
    print("\n--- Cadastro de Cliente ---")

    name = input("Qual seu nome?\n> ").strip()
    while not name:
        name = input("O nome não pode ser vazio. Qual seu nome?\n> ").strip()

    print("\nQual sua função?")
    for i, cat in enumerate(USERS_CATEGORIES):
        print(f"{i}. {cat}")

    idx_cat = get_valid_index("> ", list(USERS_CATEGORIES))
    tp_usr = USERS_CATEGORIES[idx_cat]

    print("\nQual seu curso?")
    for i, course in enumerate(COURSES_AVAILABLE):
        print(f"{i}. {course}")

    idx_course = get_valid_index("> ", list(COURSES_AVAILABLE))
    tp_course = COURSES_AVAILABLE[idx_course]

    return (Screen.BACK, (name, tp_usr, tp_course))


# ------------------------------------------------


# Utils
# ------------------------------------------------
def print_prods_screen(stock: PQueue, for_admin=False) -> None:
    print("\n" + "=" * 40)
    print("\t--- Estoque ---")
    print("=" * 40)
    if for_admin:
        stock.print_for_admin()
    else:
        stock.print_for_client()


# ------------------------------------------------
