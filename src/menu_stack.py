from ui import Screen


class MNode:
    def __init__(self, data: Screen):
        self.data: Screen | None = data
        self.prev: MNode | None = None


class MenuStack:
    def __init__(self):
        self.top: MNode | None = None

        self.count: int = 0

    def is_empty(self) -> bool:
        return not self.top and self.count <= 0

    def clear(self) -> None:
        self.top = None
        self.count = 0

    def push(self, screen: Screen) -> None:
        new_node: MNode = MNode(screen)

        new_node.prev = self.top
        self.top = new_node
        self.count += 1

    def pop(self) -> Screen | None:
        if self.is_empty():
            return

        assert self.top
        popped: MNode = self.top

        self.top = popped.prev
        self.count -= 1
        return popped.data

    def peek(self) -> Screen | None:
        return self.top.data if self.top else None

