from ui import Screen

class MNode:
    def __init__(self):
        self.data: Screen | None = None
        self.next: Mnode | None = None

class MenuStack:
    def __init__(self):
        self.top: MNode = None

        self.count: int = 0
    
    def is_empty(self) -> bool:
        return not self.top and self.count <= 0
    
    def clear(self) -> None:
        pass

    def push(self) -> None:
        pass

    def pop(self) -> None:
        pass