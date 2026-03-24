from ui import Screen


class MNode:
    def __init__(self, data: Screen):
        self.data: Screen | None = data
        self.prev: MNode | None = None


class MenuStack:
    def __init__(self):
        self.__top: MNode | None = None

        self.__count: int = 0

    def is_empty(self) -> bool:
        return not self.__top

    def clear(self) -> None:
        self.__top = None
        self.__count = 0

    def push(self, screen: Screen) -> None:
        new_node: MNode = MNode(screen)

        new_node.prev = self.__top
        self.__top = new_node
        self.__count += 1

    def pop(self) -> Screen | None:
        if self.is_empty():
            return

        assert self.__top
        popped: MNode = self.__top

        self.__top = popped.prev
        self.__count -= 1
        return popped.data

    def peek(self) -> Screen | None:
        return self.__top.data if self.__top else None

