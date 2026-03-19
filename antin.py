from datetime import date, timedelta
from faker import Faker

fake = Faker()


class Product:
    def __init__(
        self,
        name: str,
        price_buy: int,
        price_sell: int,
        date_buy: date,
        date_expire: date,
        amount: int,
    ):
        self.name: str = name
        self.price_buy: int = price_buy
        self.price_sell: int = price_sell
        self.date_buy: date = date_buy
        self.date_expire: date = date_expire
        self.amount: int = amount

    def __repr__(self) -> str:
        # return f"[{self.name} | Exp: {self.date_expire}]"
        return f"[{self.name}]"


class PNode(object):
    def __init__(
        self,
        data: Product | None = None,
        next: "PNode | None" = None,
        prev: "PNode | None" = None,
    ):
        self.data: Product | None = data
        self.prev: PNode | None = prev
        self.next: PNode | None = next


class PQueue:
    def __init__(self):
        self.head: PNode | None = None
        self.tail: PNode | None = None
        self.count: int = 0

    def enqueue(self, p: Product) -> None:
        new_node: PNode = PNode(p)

        if not self.tail:
            self.head = new_node
            self.tail = new_node
        # TODO: make it a priority queue, based on date_expiry
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.count += 1

    def dequeue(self) -> PNode:
        assert self.head is not None

        node: PNode = self.head

        self.head = self.head.next

        if self.head:
            self.head.prev = None
        else:
            self.tail = None

        self.count -= 1
        return node

    def __str__(self) -> str:
        if not self.head:
            return "List is empty."

        nodes = []
        current = self.head
        while current:
            if current == self.head:
                nodes.append(f"[HEAD: {current.data}]")
            elif current.next is None:
                nodes.append(f"[TAIL: {current.data}]")
            else:
                nodes.append(str(current.data))

            current = current.next

        return " <-> ".join(nodes)


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
    products.dequeue()
    products.dequeue()
    products.dequeue()
    print(products)
