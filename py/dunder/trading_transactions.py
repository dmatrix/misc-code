class Transaction:
    def __init__(self, user_id: str, symbol:str, quantity:int, price:float) -> None:
        self.user_id = user_id
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.cost = self.total_cost()

    def total_cost(self):
        return self.quantity * self.price * 1.00

    def __repr__(self):
        return f'Transaction({self.user_id!r} {self.symbol!r}, {self.quantity!r}, {self.price!r}, {self.cost!r})'

    def __str__(self):
        return f'{self.user_id}: {self.quantity} shares of {self.symbol} at {self.price:.2f} incurring cost of {self.cost:.2f}' 
    
    def __eq__(self, __value: object) -> bool:
        return self.__dict__ == __value.__dict__
    
    def __gt__(self, __value: object) -> bool:
        return self.cost > __value.cost
    
    def __lt__(self, __value: object) -> bool:
        return self.cost < __value.cost
    
    def __ge__(self, __value: object) -> bool: 
        return self.cost >= __value.cost
    
    def __le__(self, __value: object) -> bool:
        return self.cost <= __value.cost
    
    def __ne__(self, __value: object) -> bool:
        return self.__dict__ != __value.__dict__
    
    def __hash__(self) -> int:
        return hash(self.__dict__)
    
    def dict(self) -> dict:
        return self.__dict__
    
class TranscationBook:
    def __init__(self, user_id: str, transactions: list[Transaction]) -> None:
        self.transactions = transactions

    def __repr__(self):
        return f'TranscationBook({self.transactions!r})'

    def __str__(self):
        return f'{self.transactions}'
    
    def __hash__(self) -> int:
        return hash(self.__dict__)
    
    def __getitem__(self, index: int) -> Transaction:
        return self.transactions[index]
    
    def dict(self) -> dict:
        return self.__dict__
    
    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
        
    def remove_transaction(self, transaction: Transaction) -> None:
        self.transactions.remove(transaction)
        
    def total_cost(self) -> float:
        return sum([transaction.cost for transaction in self.transactions])
    
    def total_shares(self) -> int:
        return sum([transaction.quantity for transaction in self.transactions])
    
    def dict(self) -> dict:
        return self.__dict__

# Test the dunder methods for Transaction and TranscationBook

if __name__ == "__main__":
    from faker import Faker
    from random import randint, choice

    fake = Faker()
    transaction_book_entries = []
    symbols = ["AAPL", "GOOGL", "TSLA", "AMZN", "MSFT", "FB", "TWTR", "NFLX", "NVDA", "INTC"]
    for _ in range(10):
        user_id = fake.uuid4()
        transaction_entries = []
        for _ in range(randint(2,5)):
            symbol = choice(symbols)
            quantity = randint(1, 100)
            price = randint(100, 1000)
            transaction = Transaction(user_id, symbol, quantity, price)
            transaction_entries.append(transaction)
        transaction_book = TranscationBook(user_id, transaction_entries)
        transaction_book_entries.append(transaction_book)
    
    print("Transaction Book Entries:")
    print(transaction_book_entries)
    print("Transaction Book Entry 1:")
    print(transaction_book_entries[0])

    # Use Transaction methods to calculate total cost and total shares
    print("Total Cost and Total Shares for Transaction Book Entry 1:")
    print(transaction_book_entries[0].total_cost())
    print(transaction_book_entries[0].total_shares())

    # Use dunder methods to get the first transaction in the transaction book
    print(transaction_book_entries[0][0])

    # Use dunder methods to compare transaction to the transaction book  
    print("-- compare transaction entries in the transaction book --")  
    print(transaction_book_entries[0][0] == transaction_book_entries[0][1])
    print(transaction_book_entries[0][0] != transaction_book_entries[0][1])

    # sort the transaction book by total cost

    print("-- sorted by total cost --")
    sorted_transaction_book = sorted(transaction_book_entries, key=lambda x: x.total_cost())
    print(sorted_transaction_book)

    print(" -- add and remove transactions from the transaction book --")
    # use dunder methods to add and remove transactions from the transaction book
    transaction = Transaction(fake.uuid4(), "AAPL", 10, 100)
    transaction_book_entries[0].add_transaction(transaction)
    print(transaction_book_entries[0])
    
