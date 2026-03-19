from datetime import date


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
        return f"[{self.date_expire}]"
