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

    ledger: PaymentLedger = PaymentLedger()

    menu: MenuManager = MenuManager(stock, prods_available, ledger)
    menu.run()