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


def get_valid_price(label: str) -> int:
    while True:
        raw_val = input(f"{label}").strip().replace(",", "")

        if not raw_val:
            print("\n[!] O valor não pode estar vazio. [!]\n")
            continue

        try:
            cents: int = int(raw_val)

            if cents < 0:
                print("\n[!] O preço não pode ser negativo. [!]\n")
                continue

            return cents

        except ValueError:
            print("\n[!] Formato inválido. Use números como: 10,50\n")


def get_valid_int(label: str, min: int = 0, max: int = 10) -> int:
    """Prompts the user for an int in the range [min, max]"""
    while True:
        raw_val = input(f"{label}").strip()

        if not raw_val:
            print("\n[!] O valor não pode estar vazio. [!]\n")
            continue

        try:
            value: int = int(raw_val)

            if value < min:
                print(f"\n[!] O número não pode ser menor que {min}. [!]\n")
                continue
            elif value > max:
                print(f"\n[!] O número não pode ser maior que {max}. [!]\n")
                continue

            return value

        except ValueError:
            print("\n[!] Formato inválido. Digite apenas um número.\n")
