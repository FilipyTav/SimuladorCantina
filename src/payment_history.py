from payment import Payment


class PaymentNode:
    def __init__(self, data: Payment) -> None:
        self.data: Payment | None = data
        self.prev: PaymentNode | None = None
        self.next: PaymentNode | None = None

        def __repr__(self) -> str:
            return f"[{self.name} - {self.data.value}]"
