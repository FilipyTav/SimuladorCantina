from product import Product
from pqueue import PQueue

from faker import Faker
from datetime import timedelta

fake = Faker()


def gen_product() -> Product:
    d_buy = fake.date_between(start_date="-30d", end_date="today")
    d_exp = d_buy + timedelta(days=fake.random_int(min=1, max=100))

    return Product(
        name=(
            fake.ecommerce_name()
            if hasattr(fake, "ecommerce_name")
            else fake.word().capitalize()
        ),
        price_buy=fake.random_int(min=5, max=50),
        price_sell=fake.random_int(min=60, max=150),
        date_buy=d_buy,
        date_expire=d_exp,
        amount=fake.random_int(min=1, max=100),
    )


if __name__ == "__main__":
    products: PQueue = PQueue()
    for _ in range(5):
        products.enqueue(gen_product())

    print(products)
    newp: Product = gen_product()
    products.insert(newp, 0)
    print(products)

    for i in range(6):
        break
        node = products.dequeue()
        print(f"Removed {node.data if node else 'nothing'}\n")
        print(products)
