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

    # Date of purchase
    def get_dtbuy(self) -> date:
        return self.date_buy

    def set_dtbuy(self, value: date) -> None:
        self.date_buy = value

    # ID
    def get_id(self) -> int:
        return self.id

    # Price
    def get_sell_price(self) -> int:
        return self.price_sell

    def set_sell_price(self, value: int) -> None:
        self.price_sell = value

    def get_buy_price(self) -> int:
        return self.price_buy

    def set_buy_price(self, value: int) -> None:
        self.price_buy = value

    def print_admin(self) -> None:
        p_buy: str = f"{self.price_buy / 100:.2f}".replace(".", ",")
        p_sell: str = f"{self.price_sell / 100:.2f}".replace(".", ",")

        # Formatação de datas
        d_buy = self.date_buy.strftime("%d/%m/%Y")
        d_exp = self.date_expire.strftime("%d/%m/%Y")

        markers: int = 50

        print(
            f"{'-' * markers}\n"
            f"Produto:      {self.name}\n"
            f"ID:           {self.id}\n"
            f"Qtd:          {self.amount}\n"
            f"{'-' * markers}\n"
            f"Preço Venda:  R${p_sell}\n"
            f"Preço Compra: R${p_buy}\n"
            f"{'-' * markers}\n"
            f"Comprado em:  {d_buy}\n"
            f"Vence em:     {d_exp}\n"
            f"{'-' * markers}"
        )

    def get_attributes(self) -> dict[str, str]:
        return {
            "Nome": "name",
            "Preço de compra": "price_buy",
            "Preço de venda": "price_sell",
            "Data compra": "date_buy",
            "Data validade": "date_expire",
            "Quantidade": "amount",
        }

    def __repr__(self) -> str:
        # return f"[{self.name} | Exp: {self.date_expire}]"
        # return f"[{self.date_expire}]"
        # return f"[{self.name} - {self.id} - {self.amount}]"
        # return f"[{self.name} | Price: {self.price_buy}]"
        return f"[{self.name} | Am: {self.amount}]"
