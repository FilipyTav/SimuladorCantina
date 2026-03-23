from product import Product
from datetime import date


class PNode(object):
    def __init__(
        self,
        data: Product | None = None,
    ):
        self.data: Product | None = data
        self.prev: PNode | None = None
        self.next: PNode | None = None

        def __repr__(self) -> str:
            return f"[{self.data.name}]"


# Doubly linked list - priority queue
class PQueue:
    def __init__(self):
        self.head: PNode | None = None
        self.tail: PNode | None = None
        self.count: int = 0

    def enqueue(self, p: Product) -> None:
        new_dtexp: date = p.date_expire

        # First
        if not (self.tail and self.head) or (new_dtexp <= self.head.data.get_dtexp()):  # type: ignore[reportOptionalMemberAccess]
            self.insert_first(p)
            return

        # Last
        assert self.tail.data
        if new_dtexp >= self.tail.data.get_dtexp():
            self.insert_last(p)
            return

        current: PNode = self.head
        while current and current.data.get_dtexp() <= new_dtexp:  # type: ignore[reportOptionalMemberAccess]
            assert current.next
            current = current.next

        self.insert_before(p, current)

    def dequeue(self) -> PNode | None:
        if not self.head:
            print("No element to dequeue - list empty")
            return None

        node: PNode = self.head

        self.head = self.head.next

        if self.head:
            self.head.prev = None
        else:
            self.tail = None

        self.count -= 1
        return node

    # pos: [0, self.count]
    def insert_at(self, product: Product, pos: int) -> bool:
        if pos < 0 or pos > self.count:
            print(f"Index out of range: {pos}, the list has {self.count} element(s)")
            return False

        new_node: PNode = PNode(product)

        # Empty
        if self.count == 0 or not (self.head and self.tail):
            self.head = self.tail = new_node
            self.count += 1
            return True

        # new_node is now the head
        if pos == 0:
            new_node.next = self.head
            self.head.prev = new_node

            self.head = new_node
        # new_node is now the tail
        elif pos == self.count:
            new_node.prev = self.tail
            self.tail.next = new_node

            self.tail = new_node
        else:
            current: PNode | None = self.head

            for _ in range(pos):
                if not current:
                    return False
                current = current.next

            # Because LSP
            assert current is not None
            assert current.prev is not None

            new_node.prev = current.prev
            new_node.next = current

            new_node.prev.next = new_node

            current.prev = new_node

        self.count += 1
        return True

    def insert_before(self, p: Product, node: PNode) -> None:
        if not (self.head and self.tail) or node == self.head:
            self.insert_first(p)
            return

        new_node: PNode = PNode(p)

        new_node.prev = node.prev
        new_node.next = node

        if node.prev:
            node.prev.next = new_node

        node.prev = new_node

        self.count += 1

    def insert_after(self, p: Product, node: PNode) -> None:
        if not (self.head and self.tail):
            self.insert_first(p)
            return
        if node == self.tail:
            self.insert_last(p)
            return

        new_node: PNode = PNode(p)

        new_node.prev = node
        new_node.next = node.next

        if node.next:
            node.next.prev = new_node

        node.next = new_node

        self.count += 1

    def insert_first(self, p: Product) -> bool:
        return self.insert_at(p, 0)

    def insert_last(self, p: Product) -> bool:
        return self.insert_at(p, self.count)

    def set_product_amount(self, pname: str, amount: int) -> bool:
        prod: Product | None = self.get_by_name(pname)
        if not prod:
            return False

        prod.set_amount(amount)
        return True

    def get_by_name(self, pname: str) -> Product | None:
        if not (self.head and self.tail):
            return

        current: PNode = self.head
        while current:
            assert current.data
            if current.data.get_name().lower() == pname.lower():
                return current.data
            current = current.next  # type: ignore[reportOptionalMemberAccess]

    def get_by_ids(self, ids: set[int]) -> list[Product]:
        if not (self.head and self.tail):
            return []

        prods: list[Product] = []
        current: PNode = self.head
        while current:
            assert current.data
            if current.data.get_id() in ids:
                prods.append(current.data)

                if len(prods) == len(ids):
                    break
            current = current.next  # type: ignore[reportOptionalMemberAccess]
        return prods

    def print_for_client(self) -> None:
        if not (self.head and self.tail):
            return

        current: PNode = self.head
        while current:
            if not current.data:
                break

            prod: Product = current.data
            # Convert cents to a decimal currency format
            display_price: str = f"R${prod.price_sell / 100:.2f}".replace(".", ",")

            # Format the date (e.g., Jan 01, 2024)
            expiry_str: str = prod.date_expire.strftime("%d/%m/%Y")

            print(
                f"--- {prod.name.upper()} ---\n"
                f"Preço:      {display_price}\n"
                f"Validade:   {expiry_str}\n"
                f"Quantidade: {prod.get_amount()} unidade(s)\n"
                f"ID:         {prod.get_id()}\n"
            )

            current = current.next  # type: ignore[reportOptionalMemberAccess]

    def __str__(self) -> str:
        if not self.head:
            return "List is empty."

        nodes = []
        current = self.head
        while current:
            if current == self.head:
                nodes.append(f"[HEAD: {current.data}]")
            elif current == self.tail:
                nodes.append(f"[TAIL: {current.data}] - L: {self.count}")
            else:
                nodes.append(str(current.data))

            current = current.next

        return " <-> ".join(nodes)
