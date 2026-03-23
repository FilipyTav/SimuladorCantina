from gen_dummy_data import gen_payment, gen_product
from payment import Payment, TypeCourse, TypeUser
from payment_history import PaymentLedger
from pqueue import PQueue
from product import Product
from ui import Screen, main_menu, menu_admin, menu_client, menu_client_buy, screen_clear


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
    # TODO: make it a custom stack struct
    history: list[Screen] = [Screen.MAIN]
    while is_running and history:
        screen: Screen = history[-1]
        new_sc: Screen = screen

        screen_clear()
        print(f"\t--------{screen}--------\t")
        match screen:
            case Screen.MAIN:
                new_sc = main_menu()

            case Screen.ADMIN:
                new_sc = menu_admin()

            case Screen.CLIENT:
                new_sc = menu_client()

            case Screen.CLIENT_BUY:
                new_sc = menu_client_buy(stock)

            case _:
                print("This screen does not exist")
                break

        if new_sc == screen:
            continue

        elif new_sc == Screen.MAIN:
            history = [Screen.MAIN]

        elif new_sc == Screen.EXIT:
            print("\nEncerrando o sistema...")
            history.clear()

        elif new_sc == Screen.BACK:
            print("Should go back")
            history.pop()

        else:
            history.append(new_sc)
