import pickle

from structs.payment_history import PaymentLedger
from structs.pqueue import PQueue
from typing import TypeAlias

StructsSaved: TypeAlias = tuple[PQueue, PQueue, PaymentLedger]

savefile: str = "structs.pkl"
savepath: str = "../"
fullpath: str = savepath + savefile

def save_structs(structs: StructsSaved) -> bool:
    try:
        with open(fullpath, 'wb') as f:
            pickle.dump(structs, f)
        return True
    except Exception as e:
        print(f"Falha ao salvar: {e}")
        return False

def load_structs() -> StructsSaved | None:
    try:
        with open(fullpath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Arquivo {savefile} não encontrado.")
        return None