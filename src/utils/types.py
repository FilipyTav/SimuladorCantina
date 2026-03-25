from typing import Literal, TypeAlias
from enum import Enum, auto

TypeUser = Literal["aluno", "servidor", "professor"]
TypeCourse = Literal["IA", "ESG"]
UserInfo: TypeAlias = tuple[str, TypeUser, TypeCourse]


class Screen(Enum):
    # Admin
    # ------------------------
    ADMIN = auto()
    ADMIN_BUY = auto()
    ADMIN_SEE_STOCK = auto()
    ADMIN_UPDATE_STOCK = auto()
    ADMIN_SEE_PAYMENTS = auto()
    ADMIN_REPORTS = auto()
    # ------------------------

    # Client
    # ------------------------
    CLIENT = auto()
    CLIENT_BUY = auto()
    CLIENT_ASK_INFO = auto()
    # ------------------------

    # Helpers
    # ------------------------
    MAIN = auto()
    BACK = auto()
    EXIT = auto()
    # ------------------------
