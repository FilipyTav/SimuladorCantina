from typing import TypedDict
import matplotlib.pyplot as plt

from structs.payment import Payment
from utils.types import TypeUser, TypeCourse


class ReportData(TypedDict):
    by_category: dict[TypeUser, int]
    by_course: dict[TypeCourse, int]
    by_item: dict[int, int]
    total_profit: int
    total_prods: int
    total_transactions: int


class PaymentNode:
    def __init__(self, data: Payment) -> None:
        self.data: Payment | None = data
        self.next: PaymentNode | None = None


# Singly linked list
class PaymentLedger:
    def __init__(self):
        self.head: PaymentNode | None = None
        self.tail: PaymentNode | None = None
        self.count: int = 0

        self.report_info: ReportData = {
            "by_category": {},
            "by_course": {},
            "by_item": {},
            "total_profit": 0,
            "total_prods": 0,
            "total_transactions": 0,
        }

    def insert_at(self, p: Payment, pos: int) -> bool:
        if pos < 0 or pos > self.count:
            print(f"Index out of range: {pos}, the list has {self.count} element(s)")
            return False

        new_node: PaymentNode = PaymentNode(p)

        # Empty
        if self.is_empty():
            self.head = self.tail = new_node
            self.count += 1
            return True

        # new_node is now the head
        if pos == 0:
            new_node.next = self.head

            self.head = new_node
        # new_node is now the tail
        elif pos == self.count:
            assert self.tail
            self.tail.next = new_node

            self.tail = new_node
        else:
            current: PaymentNode | None = self.head

            for _ in range(pos - 1):
                if not current:
                    return False
                current = current.next

            # Because LSP
            assert current is not None
            assert current.next is not None

            new_node.next = current.next
            current.next = new_node

        self.count += 1
        return True

    def is_empty(self) -> bool:
        return not (self.head and self.tail) or self.count == 0

    def push(self, p: Payment) -> bool:
        cat, course = p.get_client_category(), p.get_client_course()
        val: int = p.get_value()
        prods: dict[int, int] = p.get_items()

        self.report_info["by_category"][cat] = (
            self.report_info["by_category"].get(cat, 0) + val
        )
        self.report_info["by_course"][course] = (
            self.report_info["by_course"].get(course, 0) + val
        )

        for pid, amount in prods.items():
            self.report_info["by_item"][pid] = (
                self.report_info["by_item"].get(pid, 0) + amount
            )

        self.report_info["total_prods"] += sum(prods.values())
        self.report_info["total_profit"] += val
        self.report_info["total_transactions"] += 1

        return self.insert_at(p, self.count)

    def print_admin(self) -> None:
        if not self.head:
            print("[!] O livro razão está vazio. Nenhuma venda registrada. [!]\n")
            return

        markers: int = 85
        print("\n" + "=" * markers)
        print(
            f"{'DATA/HORA':<18} | {'CLIENTE':<15} | {'CURSO':<10} | {'Categoria':<10} | {'TOTAL'}"
        )
        print("-" * markers)

        current: Pnode = self.head  # type: ignore
        total: int = 0

        while current:
            p: Payment = current.data

            if p:
                dt_fmt = p.get_dttime().strftime("%d/%m/%Y %H:%M")

                valor_fmt = f"R$ {p.get_value() / 100:>8.2f}".replace(".", ",")

                total_itens: int = sum(p.get_items().values())

                print(
                    f"{dt_fmt:<18} | {p.get_client_name()[:15]:<15} | {p.get_client_course()[:10]:<10} | {p.get_client_category():<10} | {valor_fmt}"
                )

                total += p.get_value()

            current = current.next

        total_final = (
            f"R$ {total / 100:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        print("-" * markers)
        print(f"{'FATURAMENTO TOTAL:':>65} {total_final}")
        print(f"{'TOTAL DE VENDAS:':>65} {self.count}")
        print("=" * markers + "\n")

    def print_report(self) -> None:
        data: ReportData = self.report_info
        markers: int = 45

        # --- Header ---
        print("\n" + "=" * markers)
        print(f"{'RELATÓRIO GERAL':^45}")
        print("=" * markers)

        profit_formatted: str = f"R${data['total_profit'] / 100:,.2f}".replace(".", ",")

        atv: float = 0
        if data["total_transactions"] > 0:
            atv = data["total_profit"] / data["total_transactions"]
        atv_fmt: str = f"{atv/100:,.2f}".replace(".", ",")

        print(f"    Renda Total:        {profit_formatted:>15}")
        print(f"    Unidades vendidas:  {data['total_prods']:>15}")
        print(f"    Transações:         {data['total_transactions']:>15}")
        print(f"    Renda média/venda:  {f'R${atv_fmt}':>15}")
        print("-" * markers)

        self.display_sub_report(
            "Renda por Categoria", data["by_category"], is_money=True
        )
        self.display_sub_report("Renda por Curso", data["by_course"], is_money=True)
        self.display_sub_report("Quantidade por Item", data["by_item"], is_money=False)

        print("=" * markers + "\n")

    def display_sub_report(self, title: str, mapping: dict, is_money: bool) -> None:
        if not mapping:
            return

        print(f"\n{title}:")
        for key, val in mapping.items():
            val_fmt: str = f"{val/100:,.2f}".replace(".", ",")
            display_val = f"R${val_fmt}" if is_money else str(val)
            print(f"  • {str(key).upper():<20} : {display_val:>15}")

    def save_report_graph(self, filename: str = "report.png") -> None:
        data: ReportData = self.report_info

        # 3 subplots (1 row, 3 columns)
        fig, axs = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle("Relatório Geral de Vendas", fontsize=20, fontweight="bold")

        # Category
        cats = list(data["by_category"].keys())
        cat_vals = [v / 100 for v in data["by_category"].values()]  # Convert to Reais
        axs[0].bar(cats, cat_vals, color="skyblue")
        axs[0].set_title("Renda por Categoria (R$)")
        axs[0].set_ylabel("Valor em R$")

        # Course
        courses = list(data["by_course"].keys())
        course_vals = [v / 100 for v in data["by_course"].values()]
        axs[1].bar(courses, course_vals, color="salmon")
        axs[1].set_title("Renda por Curso (R$)")

        # Item
        items = [f"ID {k}" for k in data["by_item"].keys()]
        item_vals = list(data["by_item"].values())
        axs[2].bar(items, item_vals, color="lightgreen")
        axs[2].set_title("Quantidade por Item")
        axs[2].set_ylabel("Unidades")

        # Layout adjustment to prevent labels from overlapping
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        plt.savefig(filename)
        plt.close()
        print(f"Gráfico salvo com sucesso como: {filename}")

    def __repr__(self) -> str:
        if not self.head:
            return "PaymentLedger: [Vazio]"

        items = []
        current = self.head

        while current:
            items.append(repr(current.data))
            current = current.next

        return " -> ".join(items)
