# Crie estrutura de dados adequada para gerenciar cada pagamento realizado. Armazenar o nome de quem pagou, categoria ( aluno, servidor ou professor ), curso, valor pago, data e hora do pagamento.
from typing import Literal
from datetime import datetime

TypeUser = Literal["aluno", "servidor", "professor"]
TypeCourse = Literal["IA", "ESG"]


class Payment:
    def __init__(
        self,
        name: str,
        category: TypeUser,
        course: TypeCourse,
        # In cents
        value: int,
        dttime: datetime = datetime.now(),
    ) -> None:
        self.name: str = name
        self.category: TypeUser = category
        self.course: TypeCourse = course
        self.value: int = value
        self.dttime: datetime = dttime

    def __str__(self):
        return (
            f"Pagamento de {self.name} ({self.category}) - "
            f"Curso: {self.course} | Valor: R${self.value / 100:.2f} | "
            f"Data: {self.dttime.strftime('%d/%m/%Y %H:%M')}"
        )
