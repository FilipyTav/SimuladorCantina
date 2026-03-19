from product import Product


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
        new_node: PNode = PNode(p)

        # Queue empty
        if not self.tail:
            self.head = self.tail = new_node
        # TODO: make it a priority queue, based on date_expiry
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.count += 1

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

    # pos: [0, self.count[
    def insert_before(self, product: Product, pos: int) -> bool:
        if pos < 0 or pos >= self.count:
            print(f"Index out of range: {pos}, the list has {self.count} element(s)")
            return False

        new_node: PNode = PNode(product)

        # Should exist
        assert self.head is not None

        # new_node is now the head
        if pos == 0:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            return True

        current: PNode = self.head
        index: int = 0
        while current != self.tail and index < pos:
            assert current.next is not None

            current = current.next
            index += 1

        print(current.data, index)

        return True

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
