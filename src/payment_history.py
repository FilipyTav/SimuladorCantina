from payment import Payment


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

    def insert_at(self, p: Payment, pos: int) -> bool:
        if pos < 0 or pos > self.count:
            print(f"Index out of range: {pos}, the list has {self.count} element(s)")
            return False

        new_node: PaymentNode = PaymentNode(p)

        # Empty
        if self.count == 0 or not (self.head and self.tail):
            self.head = self.tail = new_node
            self.count += 1
            return True

        # new_node is now the head
        if pos == 0:
            new_node.next = self.head

            self.head = new_node
        # new_node is now the tail
        elif pos == self.count:
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

    def push(self, p: Payment) -> bool:
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

                total_itens = sum(p.get_items().values())

                print(
                    f"{dt_fmt:<18} | {p.get_client_name()[:15]:<15} | {p.get_client_course()[:10]:<10} | {p.get_client_category():<10} | {valor_fmt}"
                )

                total += p.value

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

    def __repr__(self) -> str:
        if not self.head:
            return "PaymentLedger: [Vazio]"

        items = []
        current = self.head

        while current:
            items.append(repr(current.data))
            current = current.next

        return " -> ".join(items)
