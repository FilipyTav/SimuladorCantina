from datetime import date

class Product:
    def __init__(self, name: str, price_buy: int, price_sell: int, date_buy: date, date_expire: date, amount: int):
        self.name:str = name
        self.price_buy:int = price_buy
        self.price_sell:int = price_sell
        self.date_buy: date = date_buy
        self.date_expire: date = date_expire
        self.amount:int =  amount

class PNode(object):
    def __init__(self, data:Product=None, next:PNode=None, prev:PNode=None):
        self.data:Product = data
        self.prev:PNode = prev
        self.next:PNode = next

class PQueue:
    def __init__(self):
        self.head:PNode = None
        self.tail:PNode = None
        self.count: int = 0

    def enqueue(self, p:Product):
        new_node: PNode = PNode(p)
        
        if not self.head:
            self.head = new_node
            self.tail = new_node
        # TODO: make it a priority queue, based on date_expiry
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.count += 1

if __name__ == '__main__':
    print("Teste")