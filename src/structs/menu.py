from structs.menu_stack import MenuStack

from structs.payment_history import PaymentLedger

from structs.pqueue import PQueue

from ui import (main_menu, menu_admin, menu_admin_buy, menu_admin_see_payments, menu_admin_see_reports, menu_admin_stock, menu_admin_update_stock, menu_client, menu_client_buy, menu_client_get_info, screen_clear)

from utils.types import Screen, UserInfo


class MenuManager:
    def __init__(self, stock: PQueue, prods_available: PQueue, ledger: PaymentLedger):
        self.__stock: PQueue = stock
        self.__prods_available: PQueue = prods_available
        self.__ledger: PaymentLedger = ledger

        # TODO: encapsulate this
        self.__screen_history: MenuStack = MenuStack()
        self._client_info: UserInfo | None = None

        self.__is_running: bool = True
        self.__screen_history.push(Screen.MAIN)


    def run(self):
        screen: Screen | None = None
        new_sc: Screen = Screen.MAIN

        while self.__is_running and not self.__screen_history.is_empty():
            screen = self.__screen_history.peek()
            if not screen:
                break

            screen_clear()
            new_sc = self._handle_nav(screen)

            self._navigate(screen, new_sc)

    def _handle_nav(self, screen: Screen) -> Screen:
        match screen:
            case Screen.MAIN:
                return main_menu()
            
            # Admin
            # ------------------------
            case Screen.ADMIN:
                return menu_admin()

            case Screen.ADMIN_BUY:
                return menu_admin_buy(self.__prods_available, self.__stock)

            case Screen.ADMIN_SEE_STOCK:
                return menu_admin_stock(self.__stock)

            case Screen.ADMIN_UPDATE_STOCK:
                return menu_admin_update_stock(self.__prods_available)

            case Screen.ADMIN_SEE_PAYMENTS:
                return menu_admin_see_payments(self.__ledger)

            case Screen.ADMIN_REPORTS:
                return menu_admin_see_reports(self.__ledger)
            # ------------------------


            # Client
            # ------------------------
            case Screen.CLIENT:
                if not self._client_info:
                    return Screen.CLIENT_ASK_INFO
                return menu_client(self._client_info[0])

            case Screen.CLIENT_ASK_INFO:
                new_sc, info = menu_client_get_info()
                self._client_info = info
                return new_sc

            case Screen.CLIENT_BUY:
                if self._client_info:
                    return menu_client_buy(self.__stock, self.__ledger, self._client_info)
                return Screen.CLIENT_ASK_INFO

            case _:
                print("This screen does not exist")
                return Screen.EXIT
            # ------------------------


    def _navigate(self, current_sc: Screen, new_sc: Screen):
        if new_sc == current_sc:
            return

        if new_sc == Screen.MAIN:
            self.__screen_history.clear()
            self.__screen_history.push(Screen.MAIN)

        elif new_sc == Screen.EXIT:
            print("\nEncerrando o sistema...")
            self.__is_running = False
            self.__screen_history.clear()

        elif new_sc == Screen.BACK:
            self.__screen_history.pop()

        else:
            self.__screen_history.push(new_sc)