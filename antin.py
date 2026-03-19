from datetime import date, timedelta
from faker import Faker

fake = Faker()

class Product:
    def __init__(self, name: str, price_buy: int, price_sell: int, date_buy: date, date_expire: date, amount: int):
        self.name:str = name
        self.price_buy:int = price_buy
        self.price_sell:int = price_sell
        self.date_buy: date = date_buy
        self.date_expire: date = date_expire
        self.amount:int =  amount

    def __repr__(self):
            return f"[{self.name} | Exp: {self.date_expire}]"

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

    def __str__(self):
        if not self.head:
            return "List is empty."
        
        nodes = []
        current = self.head
        while current:
            if current == self.head:
                nodes.append(f"[HEAD: {current.data}]")
            elif current.next is None:
                nodes.append(f"[TAIL: {current.data}]")
            else:
                nodes.append(str(current.data))
                
            current = current.next
            
        return " <-> ".join(nodes)

if __name__ == '__main__':
    products:PQueue = PQueue()
    for _ in range(5):
        d_buy = fake.date_between(start_date='-30d', end_date='today')
        d_exp = d_buy + timedelta(days=fake.random_int(min=10, max=100))
        
        p = Product(
            name=fake.ecommerce_name() if hasattr(fake, 'ecommerce_name') else fake.word().capitalize(),
            price_buy=fake.random_int(min=5, max=50),
            price_sell=fake.random_int(min=60, max=150),
            date_buy=d_buy,
            date_expire=d_exp,
            amount=fake.random_int(min=1, max=100)
        )
        products.enqueue(p)
    
    print(products)