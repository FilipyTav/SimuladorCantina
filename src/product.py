from datetime import date

current_id: int = 0


class Product:
    def __init__(
        self,
        name: str,
        # In cents
        price_buy: int,
        price_sell: int,
        date_buy: date,
        date_expire: date,
        amount: int,
        id: int = -1,
    ):
        self.name: str = name
        self.price_buy: int = price_buy
        self.price_sell: int = price_sell
        self.date_buy: date = date_buy
        self.date_expire: date = date_expire
        self.amount: int = amount

        global current_id
        self.id: int = current_id
        if id < 0:
            self.id = current_id
            current_id += 1
        else:
            self.id = id

    # Name
    def get_name(self) -> str:
        return self.name

    def set_name(self, value: str) -> None:
        self.name = value

    # Amount
    def get_amount(self) -> int:
        return self.amount

    def set_amount(self, value: int) -> None:
        if value < 0:
            value = 0

        self.amount = value

    # Date of expiry
    def get_dtexp(self) -> date:
        return self.date_expire

    def set_dtexp(self, value: date) -> None:
        self.date_expire = value

    # ID
    def get_id(self) -> int:
        return self.id

    # Price
    def get_sell_price(self) -> int:
        return self.price_sell

    def __repr__(self) -> str:
        # return f"[{self.name} | Exp: {self.date_expire}]"
        # return f"[{self.date_expire}]"
        return f"[{self.name} - {self.id} - {self.amount}]"
        # return f"[{self.name} | Price: {self.price_buy}]"
        # return f"[{self.name} | Am: {self.amount}]"
