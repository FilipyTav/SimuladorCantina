# Crie estrutura de dados adequada para gerenciar cada pagamento realizado. Armazenar o nome de quem pagou, categoria ( aluno, servidor ou professor ), curso, valor pago, data e hora do pagamento.
from typing import Literal, get_args
from datetime import datetime

from pqueue import PQueue
from product import Product

TypeUser = Literal["aluno", "servidor", "professor"]
TypeCourse = Literal["IA", "ESG"]

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
        self.name: str = name
        self.category: TypeUser = category
        self.course: TypeCourse = course

        # In cents
        self.value: int = value

        self.items: dict[int, int] = items
        self.dttime: datetime = dttime

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
    p: dict[int, int], client_info: tuple[str, TypeUser, TypeCourse], stock: PQueue
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
        if amount > prod.get_amount():
            print(
                f"ID: {prod.get_id()}({prod.get_name()}) tem somente {prod.get_amount()} unidade(s) em estoque."
            )
            return

    # Update stock
    for prod in prods:
        amount = p[prod.id]
        prod.set_amount(prod.get_amount() - amount)

        total += prod.get_sell_price() * amount

    print(f"total: {total}")

    name, category, course = client_info
    return Payment(
        name,
        category,
        course,
        total,
        items=p.copy(),
    )
