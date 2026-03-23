from typing import Literal
from gen_dummy_data import gen_payment, gen_product
from payment import Payment, TypeCourse, TypeUser
from payment_history import PaymentLedger
from pqueue import PQueue
from product import Product


def process_sale(
    p: dict[int, int], client_info: tuple[str, TypeUser, TypeCourse], stock: PQueue
) -> Payment | None:
    prods: list[Product] = stock.get_by_ids(set(p.keys()))
    # If unavailable ID
    if len(prods) != len(p):
        missing: set[int] = set(p.keys()) - {pr.get_id() for pr in prods}
        print(f"Erro: Os seguintes IDs de produto não existem: {missing}")
        return

    total: int = 0
    amount: int = 0
    # Check stock
    for prod in prods:
        amount = p[prod.id]
        # TODO: activate later
        if amount > prod.get_amount() and False:
            print(
                f"{prod.get_name()} tem somente {prod.get_amount()} unidade(s) em estoque."
            )
            return

    # Update stock
    for prod in prods:
        amount = p[prod.id]
        prod.set_amount(prod.get_amount() - amount)

        total += prod.get_sell_price() * amount

    print(f"total: {total}")

    name, category, course = client_info
    return Payment(
        name,
        category,
        course,
        total,
        items=p.copy(),
    )


if __name__ == "__main__":
    stock: PQueue = PQueue()
    for _ in range(5):
        stock.enqueue(gen_product())

    ledger: PaymentLedger = PaymentLedger()
    for _ in range(5):
        ledger.push(gen_payment())

    # print(stock)
    #
    # prods: dict[int, int] = {
    #     #
    #     0: 4,
    #     2: 9,
    #     4: 6,
    # }
    #
    # if not process_sale(prods, ("", "aluno", "IA"), stock):
    #     print("Tente novamente")

    is_admin: bool = False
    is_running: bool = True
    while is_running:
        print("\n" + "=" * 40)
        print("\t--- CANTINA ---")
        print("=" * 40)

        print("Que usuário usar?\n")

        print("1. Admin")
        print("2. Cliente")
        print("q. Sair")

        choice: str = input("\nEscolha uma opção: ").strip().lower()

        if choice == "1":
            print("\n--- Modo Administrador ---")
            is_admin = True
        elif choice == "2":
            is_admin = False
            print("\n--- Bem-vindo, Cliente! ---")
        elif choice == "q":
            print("Encerrando o sistema...")
            is_running = False
            break
        else:
            print("Opção inválida! Escolha 1, 2 ou q.")

    print("")
