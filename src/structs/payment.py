from typing import get_args
from datetime import datetime

from utils.types import TypeUser, TypeCourse, UserInfo

from structs.pqueue import PQueue
from structs.product import Product

USERS_CATEGORIES = get_args(TypeUser)
COURSES_AVAILABLE = get_args(TypeCourse)


class Payment:
    def __init__(
        self,
        name: str,
        category: TypeUser,
        course: TypeCourse,
        value: int,
        items: dict[int, int],
        dttime: datetime = datetime.now(),
    ) -> None:
        # Client info
        self.__name: str = name
        self.__category: TypeUser = category
        self.__course: TypeCourse = course

        # In cents
        self.__value: int = value

        self.__items: dict[int, int] = items
        self.__dttime: datetime = dttime

    def get_price_formatted(self) -> str:
        return f"{self.__value / 100:.2f}".replace(".", ",")

    def print_for_client(self) -> None:
        dt_formatted = self.__dttime.strftime("%d/%m/%Y - %H:%M")

        title: str = "COMPROVANTE DE VENDA"
        markers: int = 25

        print(
            f"\n" + "=" * markers,
            f"{title}",
            f"=" * markers + "\n",
            f"Cliente: {self.__name}\n",
            f"Data:    {dt_formatted}\n",
            f"-" * 30 + "\n",
            f"Total:   R${self.get_price_formatted()}\n",
            f"Itens:   {self.__items}",
            f"\n" + "=" * (markers * 2 + len(title) + 2) + "\n",
        )

    # Name
    def get_client_name(self) -> str:
        return self.__name

    # User type
    def get_client_category(self) -> TypeUser:
        return self.__category

    # User course
    def get_client_course(self) -> TypeCourse:
        return self.__course

    # Value
    def get_value(self) -> int:
        return self.__value

    # Items
    def get_items(self) -> dict[int, int]:
        return self.__items

    # Datetime
    def get_dttime(self) -> datetime:
        return self.__dttime

    def __repr__(self) -> str:
        return f"[{self.__name} - {self.__value}]"

    def __str__(self):
        return (
            f"Pagamento de {self.__name} ({self.__category}) - "
            f"Curso: {self.__course} | Valor: R${self.__value / 100:.2f} | "
            f"Data: {self.__dttime.strftime('%d/%m/%Y %H:%M')} | "
            f"Items: {self.__items}"
        )


def process_sale(
    p: dict[int, int],
    client_info: UserInfo,
    stock: PQueue,
    needs_confirmation: bool = False,
) -> Payment | None:
    prods: list[Product] = stock.get_by_ids(set(p.keys()))
    # If unavailable ID
    if len(prods) != len(p):
        missing: set[int] = set(p.keys()) - {pr.get_id() for pr in prods}
        print(f"[!] Erro: Os seguintes IDs de produto não existem: {missing} [!]")
        return

    total: int = 0
    amount: int = 0
    # Check stock
    for prod in prods:
        amount = p[prod.id]
        total += prod.get_sell_price() * amount
        if amount > prod.get_amount():
            print(
                f"ID: {prod.get_id()}({prod.get_name()}) tem somente {prod.get_amount()} unidade(s) em estoque."
            )
            return

    if needs_confirmation:
        print(f"Total: R${total/100:.2f}".replace(".", ","))
        print("Confirmar compra? (s/n)")
        confirmed: str = input("> ").strip().lower()
        if confirmed == "n":
            print("\nCompra cancelada!")
            return None
        elif confirmed == "s":
            pass

    # Update stock
    for prod in prods:
        amount = p[prod.id]
        prod.set_amount(prod.get_amount() - amount)

    name, category, course = client_info
    return Payment(
        name,
        category,
        course,
        total,
        items=p.copy(),
    )
