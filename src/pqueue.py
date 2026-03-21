from product import Product
from datetime import date


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

        def __repr__(self) -> str:
            return f"[{self.data.name}]"


class PQueue:
    def __init__(self):
        self.head: PNode | None = None
        self.tail: PNode | None = None
        self.count: int = 0

    def enqueue(self, p: Product) -> None:
        new_dtexp: date = p.date_expire

        # First
        if not (self.tail and self.head) or (new_dtexp <= self.head.data.date_expire):
            self.insert_at(p, 0)
            return
        # Last
        if new_dtexp >= self.tail.data.date_expire:
            self.insert_at(p, self.count)
            return

        current: PNode | None = self.head
        index: int = 0
        while current and current.data.date_expire <= new_dtexp:
            current = current.next
            index += 1

        self.insert_at(p, index)

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
            self.insert_at(p, 0)
            return

        new_node: PNode = PNode(p)

        new_node.prev = node.prev
        new_node.next = node

        if node.prev:
            node.prev.next = new_node

        node.prev = new_node

        self.count += 1

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
