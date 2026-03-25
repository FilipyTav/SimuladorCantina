from structs.menu import MenuManager
from utils.types import UserInfo, Screen

from utils.gen_dummy_data import gen_payment, gen_product

from structs.menu_stack import MenuStack
from structs.payment_history import PaymentLedger
from structs.pqueue import PQueue
from structs.product import Product

if __name__ == "__main__":
    stock: PQueue = PQueue()
    prods_available: PQueue = PQueue()
    for i in range(5):
        prod: Product = gen_product()
        if i < 3:
            stock.enqueue(prod)
        prods_available.enqueue(prod)

    ledger: PaymentLedger = PaymentLedger()
    for _ in range(15):
        ledger.push(gen_payment())

    menu: MenuManager = MenuManager(stock, prods_available, ledger)
    menu.run()