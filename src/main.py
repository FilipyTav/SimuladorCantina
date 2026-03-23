from gen_dummy_data import gen_payment, gen_product
from payment import Payment, typeCourse, userInfo
from payment_history import PaymentLedger
from pqueue import PQueue
from product import Product
from ui import (
    Screen,
    main_menu,
    menu_admin,
    menu_admin_buy,
    menu_admin_stock,
    menu_admin_update_stock,
    menu_client,
    menu_client_buy,
    menu_client_get_info,
    screen_clear,
)

if __name__ == "__main__":
    stock: PQueue = PQueue()
    prods_available: PQueue = PQueue()
    for i in range(5):
        prod: Product = gen_product()
        if i < 3:
            stock.enqueue(prod)
        prods_available.enqueue(prod)

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
    client_info: userInfo | None = None
    while is_running and history:
        screen: Screen = history[-1]
        new_sc: Screen = screen

        screen_clear()
        # print(f"\t--------{screen}--------\t")
        print(history)
        match screen:
            case Screen.MAIN:
                new_sc = main_menu()

            # Admin
            # ------------------------
            case Screen.ADMIN:
                # TODO: print payments
                # TODO: add to stock
                # TODO: change stock product info
                # TODO: show payment graph
                # TODO: password verification
                new_sc = menu_admin()

            case Screen.ADMIN_BUY:
                new_sc = menu_admin_buy(prods_available)

            case Screen.ADMIN_SEE_STOCK:
                new_sc = menu_admin_stock(prods_available)

            case Screen.ADMIN_UPDATE_STOCK:
                new_sc = menu_admin_update_stock(prods_available)
            # ------------------------

            # Client
            # ------------------------
            case Screen.CLIENT:
                if not client_info:
                    new_sc = Screen.CLIENT_ASK_INFO
                else:
                    # TODO: make a new struct for client_info
                    new_sc = menu_client(client_info[0])

            case Screen.CLIENT_ASK_INFO:
                new_sc, client_info = menu_client_get_info()

            case Screen.CLIENT_BUY:
                if client_info:
                    new_sc = menu_client_buy(stock, client_info)
            # ------------------------

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
