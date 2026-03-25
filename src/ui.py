import os

from structs.payment import (
    COURSES_AVAILABLE,
    USERS_CATEGORIES,
    Payment,
    process_sale,
)
from structs.payment_history import PaymentLedger
from structs.pqueue import PQueue
from structs.product import Product

from utils.types import Screen, UserInfo
from utils.input import get_valid_date, get_valid_index, get_valid_int, get_valid_price


def screen_clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_main_options(back: bool = True, main: bool = True, stop: bool = True) -> None:
    if back:
        print("B. Voltar ao menu anterior")
    if main:
        print("M. Voltar ao menu inicial")
    if stop:
        print("Q. Fechar programa")


def main_menu() -> Screen:
    print("\n" + "=" * 40)
    print("\t--- CANTINA ---")
    print("=" * 40)

    print("Que usuário usar?\n")

    print("1. Admin")
    print("2. Cliente")
    print()
    print_main_options(back=False, main=False, stop=True)

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
        f"0. Ver estoque\n"
        f"1. Adicionar ao estoque\n"
        f"2. Mostrar vendas\n"
        f"3. Relatório de vendas\n"
    )
    print_main_options(back=True, main=False, stop=True)
    choice: str = input("> ").strip().lower()

    match choice:
        case "q":
            return Screen.EXIT

        case "b":
            return Screen.BACK

        case "0":
            return Screen.ADMIN_SEE_STOCK

        case "1":
            return Screen.ADMIN_BUY

        case "2":
            return Screen.ADMIN_SEE_PAYMENTS

        case "3":
            return Screen.ADMIN_REPORTS

        case _:
            return Screen.BACK

    return Screen.MAIN


def menu_admin_buy(prods_available: PQueue, stock: PQueue) -> Screen:
    print_prods_screen(prods_available, True)

    while True:
        print("Escolha o que deseja comprar.")
        print("Formato: ID.quantidade, separados por espaço. Ex.: 0.2  3.4")
        print("E. Mostrar produtos disponíveis\n")

        print_main_options(back=True, main=True, stop=True)
        # (∞)
        choice: str = input("> ").strip()
        if choice == "b":
            return Screen.BACK
        elif choice == "q":
            return Screen.EXIT
        elif choice == "m":
            return Screen.MAIN
        elif choice == "e":
            print_prods_screen(prods_available)
            return Screen.ADMIN_BUY

        try:
            print()
            parts: str = choice
            if not parts:
                raise ValueError("Entrada vazia.")

            prods_dict: dict[int, int] = {}
            s: list[str] = parts.split(" ")

            # Type and format
            for item in s:
                if "." not in item:
                    raise ValueError(f"Formato incorreto em '{item}'.")

                k, v = item.split(".")
                id_prod, qtd_prod = int(k), int(v)

                if qtd_prod <= 0:
                    raise ValueError(
                        f"Quantidade de '{id_prod}' deve ser maior que zero."
                    )

                prods_dict[id_prod] = qtd_prod

            request_ids: set[int] = set(prods_dict.keys())
            products: list[Product] = prods_available.get_by_ids(request_ids)

            # ID not found
            if len(products) != len(request_ids):
                found_ids: set[int] = {p.get_id() for p in products}
                missing: set[int] = request_ids - found_ids
                raise ValueError(f"ID(s) não encontrado(s): {missing}")

            for p in products:
                current_id: int = p.get_id()
                qtd_to_add: int = prods_dict[current_id]

                p.set_amount(p.get_amount() + qtd_to_add)
                if stock.enqueue(p):
                    p.set_amount(qtd_to_add)

                print(
                    f"Item '{p.get_name()}' (ID: {p.get_id()}) -> +{prods_dict[p.get_id()]} unidade(s)"
                )

            print()

        except ValueError as e:
            print(f"[!] Erro de validação: {e} [!]")
            print("[Exemplo correto: 1.5 2.10 (ID.quantidade)]\n")

    return Screen.ADMIN_BUY


def menu_admin_stock(stock: PQueue) -> Screen:
    while True:
        print_prods_screen(stock)

        print(
            f"Escolha o que deseja fazer:\n"
            f"0. Mostrar estoque\n"
            f"1. Modificar estoque\n"
        )
        print_main_options(back=True, main=True, stop=True)

        choice: str = input("> ").strip()
        match choice:
            case "b":
                return Screen.BACK
            case "m":
                return Screen.MAIN
            case "q":
                return Screen.EXIT
            case "0":
                print_prods_screen(stock)
                return Screen.ADMIN_SEE_STOCK
            case "1":
                return Screen.ADMIN_UPDATE_STOCK
            case _:
                return Screen.ADMIN_SEE_STOCK

    return Screen.BACK


def menu_admin_see_payments(ledger: PaymentLedger) -> Screen:
    while True:
        screen_clear()
        ledger.print_admin()
        print_main_options(back=True, main=True, stop=True)
        choice: str = input("> ").strip().lower()
        match choice:
            case "b":
                return Screen.BACK
            case "m":
                return Screen.MAIN
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

        print(f"\nModificando: {p.get_name()} (ID: {p.get_id()})")
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


def menu_admin_see_reports(ledger: PaymentLedger) -> Screen:
    while True:
        screen_clear()
        ledger.print_report()
        print(f"P. Salvar gráfico em arquivo\n")
        print_main_options(back=True, main=True, stop=True)
        choice: str = input("> ").strip().lower()
        match choice:
            case "b":
                return Screen.BACK

            case "q":
                return Screen.EXIT

            case "m":
                return Screen.MAIN

            case "p":
                ledger.save_report_graph()
                continue

        return Screen.BACK
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
    print("0. Ver estoque\n")
    print_main_options(back=True, main=False, stop=True)

    choice: str = input("\nEscolha uma opção: ")

    match choice:
        case "q":
            return Screen.EXIT
        case "b":
            return Screen.BACK

        case "0":
            return Screen.CLIENT_BUY

        case _:
            print("Essa não é uma opção. Tente novamente")
            return Screen.CLIENT


def menu_client_buy(
    stock: PQueue, ledger: PaymentLedger, user_info: UserInfo
) -> Screen:
    print_prods_screen(stock)

    while True:
        print("Escolha o que deseja comprar.")
        print("Formato: ID.quantidade, separados por espaço. Ex.: 0.2 3.4")
        print("E. Mostrar estoque\n")
        print_main_options(back=True, main=False, stop=True)

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
            parts: str = choice
            if not parts:
                raise ValueError("Entrada vazia.")

            s: list[str] = parts.split(" ")
            for item in s:
                if "." not in item:
                    raise ValueError(f"Formato incorreto em '{item}'.")

                k, v = item.split(".")
                id_prod, qtd_prod = int(k), int(v)

                if qtd_prod <= 0:
                    raise ValueError(
                        f"Quantidade de '{id_prod}' deve ser maior que zero."
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
        except ValueError as e:
            print(f"[!] Erro de validação: {e} [!]")
            print("[Exemplo correto: 1.5 2.10 (ID.quantidade)]\n")

    return Screen.CLIENT_BUY


def menu_client_get_info() -> tuple[Screen, UserInfo]:
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
