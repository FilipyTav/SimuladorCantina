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

    # newp: Product = gen_product()
    # newp.set_name("Test")
    # newp.set_dtexp(date(2026, 4, 15))
    # stock.enqueue(newp)

    print(stock)

    # ledger.insert_at(paym, 1)
    # print(ledger)

    prods: dict[int, int] = {
        #
        0: 4,
        2: 9,
        4: 6,
    }

    paym: Payment = Payment("Me Myself", "aluno", "IA", 1020, prods)
    print(paym)
    print()

    if not process_sale(prods, ("", "aluno", "IA"), stock):
        print("Tente novamente")

    for i in range(6):
        break
        node = stock.dequeue()
        print(f"Removed {node.data if node else 'nothing'}\n")
        print(stock)
