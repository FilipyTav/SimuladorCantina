from structs.menu import MenuManager

from structs.payment_history import PaymentLedger
from structs.pqueue import PQueue

if __name__ == "__main__":
    stock: PQueue = PQueue()
    prods_available: PQueue = PQueue()

    ledger: PaymentLedger = PaymentLedger()

    menu: MenuManager = MenuManager(stock, prods_available, ledger)
    menu.run()
