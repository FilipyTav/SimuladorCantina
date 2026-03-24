# Crie estrutura de dados adequada para gerenciar cada pagamento realizado. Armazenar o nome de quem pagou, categoria ( aluno, servidor ou professor ), curso, valor pago, data e hora do pagamento.
from typing import Literal, TypeAlias, get_args
from datetime import datetime

from pqueue import PQueue
from product import Product

typeUser = Literal["aluno", "servidor", "professor"]
typeCourse = Literal["IA", "ESG"]
userInfo: TypeAlias = tuple[str, typeUser, typeCourse]

USERS_CATEGORIES = get_args(typeUser)
COURSES_AVAILABLE = get_args(typeCourse)


class Payment:
    def __init__(
        self,
        name: str,
        category: typeUser,
        course: typeCourse,
        value: int,
        items: dict[int, int],
        dttime: datetime = datetime.now(),
    ) -> None:
        # Client info
        self.name: str = name
        self.category: typeUser = category
        self.course: typeCourse = course

        # In cents
        self.value: int = value

        self.items: dict[int, int] = items
        self.dttime: datetime = dttime

    def get_price_formatted(self) -> str:
        return f"{self.value / 100:.2f}".replace(".", ",")

    def print_for_client(self) -> None:
        dt_formatted = self.dttime.strftime("%d/%m/%Y - %H:%M")

        title: str = "COMPROVANTE DE VENDA"
        markers: int = 25

        print(
            f"\n" + "=" * markers,
            f"{title}",
            f"=" * markers + "\n",
            f"Cliente: {self.name}\n",
            f"Data:    {dt_formatted}\n",
            f"-" * 30 + "\n",
            f"Total:   R${self.get_price_formatted()}\n",
            f"Itens:   {self.items}",
            f"\n" + "=" * (markers * 2 + len(title) + 2) + "\n",
        )

    # Name
    def get_client_name(self) -> str:
        return self.name

    # User type
    def get_client_category(self) -> typeUser:
        return self.category

    # User course
    def get_client_course(self) -> typeCourse:
        return self.course

    # Value
    def get_value(self) -> int:
        return self.value

    # Items
    def get_items(self) -> dict[int, int]:
        return self.items

    # Datetime
    def get_dttime(self) -> datetime:
        return self.dttime

    def __repr__(self) -> str:
        return f"[{self.name} - {self.value}]"

    def __str__(self):
        return (
            f"Pagamento de {self.name} ({self.category}) - "
            f"Curso: {self.course} | Valor: R${self.value / 100:.2f} | "
            f"Data: {self.dttime.strftime('%d/%m/%Y %H:%M')} | "
            f"Items: {self.items}"
        )


def process_sale(
    p: dict[int, int],
    client_info: userInfo,
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
