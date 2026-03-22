# Crie estrutura de dados adequada para gerenciar cada pagamento realizado. Armazenar o nome de quem pagou, categoria ( aluno, servidor ou professor ), curso, valor pago, data e hora do pagamento.
from typing import Literal, get_args
from datetime import datetime

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
