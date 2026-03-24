from structs.product import Product
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
        self.__head: PNode | None = None
        self.__tail: PNode | None = None
        self.__count: int = 0

        # Avoid repetition
        # TODO: uncomment later
        # self.__ids: list[int] = []

    def enqueue(self, p: Product) -> bool:
        """Returns false if product.id already in the queue"""
        # if p.get_id() in self.__ids:
        #     return False

        if self.__exists(p.get_id()):
            return False

        new_dtexp: date = p.date_expire

        # First
        if not (self.__tail and self.__head) or (new_dtexp <= self.__head.data.get_dtexp()):  # type: ignore[reportOptionalMemberAccess]
            self.__insert_first(p)
            return True

        # Last
        assert self.__tail.data
        if new_dtexp >= self.__tail.data.get_dtexp():
            self.__insert_last(p)
            return True

        current: PNode = self.__head
        while current and current.data.get_dtexp() <= new_dtexp:  # type: ignore[reportOptionalMemberAccess]
            assert current.next
            current = current.next

        self.__insert_before(p, current)
        return True

    def dequeue(self) -> PNode | None:
        if not self.__head:
            print("No element to dequeue - list empty")
            return None

        node: PNode = self.__head

        self.__head = self.__head.next

        if self.__head:
            self.__head.prev = None
        else:
            self.__tail = None

        self.__count -= 1
        return node

    # pos: [0, self.count]
    def _insert_at(self, product: Product, pos: int) -> bool:
        if pos < 0 or pos > self.__count:
            print(f"Index out of range: {pos}, the list has {self.__count} element(s)")
            return False

        new_node: PNode = PNode(product)

        # Empty
        if self.is_empty():
            self.__head = self.__tail = new_node
            self.__count += 1
            # self.__ids.append(product.get_id())
            return True

        assert self.__head
        assert self.__tail
        # new_node is now the head
        if pos == 0:
            new_node.next = self.__head
            self.__head.prev = new_node

            self.__head = new_node
        # new_node is now the tail
        elif pos == self.__count:
            new_node.prev = self.__tail
            self.__tail.next = new_node

            self.__tail = new_node
        else:
            current: PNode | None = self.__head

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

        self.__count += 1
        # self.__ids.append(product.get_id())
        return True

    def __insert_before(self, p: Product, node: PNode) -> None:
        if self.is_empty() or node == self.__head:
            self.__insert_first(p)
            return

        new_node: PNode = PNode(p)

        new_node.prev = node.prev
        new_node.next = node

        if node.prev:
            node.prev.next = new_node

        node.prev = new_node

        self.__count += 1
        # self.__ids.append(p.get_id())

    def __insert_after(self, p: Product, node: PNode) -> None:
        if self.is_empty():
            self.__insert_first(p)
            return
        if node == self.__tail:
            self.__insert_last(p)
            return

        new_node: PNode = PNode(p)

        new_node.prev = node
        new_node.next = node.next

        if node.next:
            node.next.prev = new_node

        node.next = new_node

        self.__count += 1
        # self.__ids.append(p.get_id())

    def __insert_first(self, p: Product) -> bool:
        return self._insert_at(p, 0)

    def __insert_last(self, p: Product) -> bool:
        return self._insert_at(p, self.__count)

    def __exists(self, id: int) -> bool:
        current = self.__head
        while current:
            if current.data.get_id() == id:  # type: ignore
                return True
            current = current.next
        return False

    def is_empty(self) -> bool:
        return not (self.__head and self.__tail)

    def set_product_amount(self, pname: str, amount: int) -> bool:
        prod: Product | None = self.get_by_name(pname)
        if not prod:
            return False

        prod.set_amount(amount)
        return True

    def get_by_name(self, pname: str) -> Product | None:
        if self.is_empty():
            return

        current: PNode | None = self.__head
        while current:
            assert current.data
            if current.data.get_name().lower() == pname.lower():
                return current.data
            current = current.next  # type: ignore[reportOptionalMemberAccess]

    def get_by_ids(self, ids: set[int]) -> list[Product]:
        if self.is_empty():
            return []

        prods: list[Product] = []
        current: PNode | None = self.__head
        while current:
            assert current.data
            if current.data.get_id() in ids:
                prods.append(current.data)

                if len(prods) == len(ids):
                    break
            current = current.next  # type: ignore[reportOptionalMemberAccess]
        return prods

    def print_for_admin(self) -> None:
        if self.is_empty():
            return

        current: PNode | None = self.__head
        while current:
            if not current.data:
                break

            prod: Product = current.data
            # Convert cents to a decimal currency format
            display_price: str = f"R${prod.price_sell / 100:.2f}".replace(".", ",")

            # Format the date (e.g., Jan 01, 2024)
            expiry_str: str = prod.date_expire.strftime("%d/%m/%Y")

            print(
                f"-------- {prod.name.upper()} --------\n"
                f"Preço:      {display_price}\n"
                f"Validade:   {expiry_str}\n"
                f"Quantidade: ∞ unidades\n"
                f"ID:         {prod.get_id()}\n"
            )

            current = current.next  # type: ignore[reportOptionalMemberAccess]

    def print_for_client(self) -> None:
        if self.is_empty():
            return

        current: PNode | None = self.__head
        while current:
            if not current.data:
                break

            prod: Product = current.data
            # Convert cents to a decimal currency format
            display_price: str = f"R${prod.price_sell / 100:.2f}".replace(".", ",")

            # Format the date (e.g., Jan 01, 2024)
            expiry_str: str = prod.date_expire.strftime("%d/%m/%Y")

            print(
                f"-------- {prod.name.upper()} --------\n"
                f"Preço:      {display_price}\n"
                f"Validade:   {expiry_str}\n"
                f"Quantidade: {prod.get_amount()} unidade(s)\n"
                f"ID:         {prod.get_id()}\n"
            )

            current = current.next  # type: ignore[reportOptionalMemberAccess]

    def __str__(self) -> str:
        if not self.__head:
            return "List is empty."

        nodes = []
        current = self.__head
        while current:
            if current == self.__head:
                nodes.append(f"[HEAD: {current.data}]")
            elif current == self.__tail:
                nodes.append(f"[TAIL: {current.data}] - L: {self.__count}")
            else:
                nodes.append(str(current.data))

            current = current.next

        return " <-> ".join(nodes)
