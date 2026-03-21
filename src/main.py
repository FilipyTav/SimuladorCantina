from payment import Payment, TypeUser, TypeCourse
from payment_history import PaymentLedger
from product import Product
from pqueue import PQueue

from faker import Faker
from datetime import timedelta, date
import random

fake = Faker()

# expiry_counter = 0


def gen_product() -> Product:
    # global expiry_counter
    # expiry_counter += 10

    d_buy = fake.date_between(start_date="-30d", end_date="today")
    d_exp = d_buy + timedelta(days=fake.random_int(min=1, max=100))

    # d_buy = date.today()
    # d_exp = d_buy + timedelta(days=expiry_counter)

    return Product(
        name=(
            fake.ecommerce_name()
            if hasattr(fake, "ecommerce_name")
            else fake.word().capitalize()
        ),
        price_buy=fake.random_int(min=5, max=50) * 100,
        price_sell=fake.random_int(min=60, max=150) * 100,
        date_buy=d_buy,
        date_expire=d_exp,
        amount=fake.random_int(min=1, max=100),
    )


def gen_payment() -> Payment:
    category: TypeUser = random.choice(["aluno", "servidor", "professor"])
    course: TypeCourse = random.choice(["IA", "ESG"])

    value_in_cents = random.randint(1000, 10000)

    return Payment(
        name=fake.name(),
        category=category,
        course=course,
        value=value_in_cents,
        # dttime=fake.date_time_between(start_date='-30d', end_date='now')
    )


if __name__ == "__main__":
    stock: PQueue = PQueue()
    for _ in range(5):
        stock.enqueue(gen_product())

    ledger: PaymentLedger = PaymentLedger()
    for _ in range(5):
        ledger.insert_at(gen_payment(), 0)

    # newp: Product = gen_product()
    # newp.set_name("Test")
    # newp.set_dtexp(date(2026, 4, 15))
    # stock.enqueue(newp)

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
