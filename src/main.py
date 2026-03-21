from gen_dummy_data import gen_payment, gen_product
from payment import Payment
from payment_history import PaymentLedger
from pqueue import PQueue

if __name__ == "__main__":
    stock: PQueue = PQueue()
    for _ in range(5):
        stock.enqueue(gen_product())

    ledger: PaymentLedger = PaymentLedger()
    for _ in range(5):
        ledger.push(gen_payment())

    # newp: Product = gen_product()
    # newp.set_name("Test")
    # newp.set_dtexp(date(2026, 4, 15))
    # stock.enqueue(newp)

    print(stock)
    paym: Payment = Payment("Me Myself", "aluno", "IA", 1020)
    print(paym)
    print()

    ledger.insert_at(paym, 1)
    print(ledger)

    for i in range(6):
        break
        node = stock.dequeue()
        print(f"Removed {node.data if node else 'nothing'}\n")
        print(stock)
