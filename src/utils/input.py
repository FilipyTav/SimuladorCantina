from datetime import date, datetime


def get_valid_date(label: str) -> date:
    while True:
        raw_val = input(f"{label} (DD/MM/AAAA): ").strip()

        if not raw_val:
            print("\n[!] A data não pode estar vazia. [!]\n")
            continue

        try:
            dt_obj = datetime.strptime(raw_val, "%d/%m/%Y")

            return dt_obj.date()

        except ValueError:
            print(
                "\n[!] Formato inválido ou data inexistente. Use o padrão DIA/MÊS/ANO (ex: 01/01/1970). [!]\n"
            )
