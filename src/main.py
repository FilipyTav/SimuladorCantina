from product import Product
from pqueue import PQueue

from faker import Faker
from datetime import timedelta

fake = Faker()

if __name__ == "__main__":
    products: PQueue = PQueue()
    for _ in range(5):
        d_buy = fake.date_between(start_date="-30d", end_date="today")
        d_exp = d_buy + timedelta(days=fake.random_int(min=10, max=100))

        p = Product(
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
        products.enqueue(p)

    print(products)

    for i in range(5):
        node = products.dequeue()
        print(f"Removed {node.data if node else 'nothing'}\n")
        print(products)
