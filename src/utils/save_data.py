import pickle
import pathlib

from structs.payment_history import PaymentLedger
from structs.pqueue import PQueue
from typing import TypeAlias

StructsSaved: TypeAlias = tuple[PQueue, PQueue, PaymentLedger]

BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.resolve()
fullpath: pathlib.Path = BASE_DIR.parent / "structs.pkl"


def save_structs(structs: StructsSaved) -> bool:
    """stock, prods_available, ledger"""
    try:
        fullpath.parent.mkdir(parents=True, exist_ok=True)
        with open(fullpath, "wb") as f:
            pickle.dump(structs, f)
        return True
    except Exception as e:
        print(f"Falha ao salvar: {e}")
        return False


def load_structs() -> StructsSaved | None:
    """stock, prods_available, ledger"""
    try:
        with open(fullpath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Arquivo não encontrado em {fullpath}.")
        return None

