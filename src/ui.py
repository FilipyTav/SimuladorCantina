from pqueue import PQueue


def menu_admin():
    return


def menu_client(stock: PQueue):
    print("\n" + "=" * 40)
    print("\t--- CANTINA ---")
    print("  --- Bem-vindo(a), Cliente! ---")
    print("=" * 40)

    print("\nComo prosseguir?")
    print("1. Ver estoque")

    choice = input("\nEscolha uma opção: ")

    match choice:
        case "1":
            print(stock)
