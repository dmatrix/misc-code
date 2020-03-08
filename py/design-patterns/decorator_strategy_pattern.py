from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity
#
# The Context for the Strategy
#
class Order:

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        # check if the __total has been computed
        # compute it lazily
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            # invoke the concrete strategy class implementation
            # of the discount function
            discount = self.promotion(self)


        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due:{:2f}>'
        return fmt.format(self.total(), self.due())

#
# Decorators for each promotion
#

# start with an empty decorated list of flyweight function
# this decorators will be loaded at load time.

promos = []

# Define a decorator
def promotion(promo_func):
    """
    Define the decorator and return the function unchanged
    """
    promos.append(promo_func)
    return promo_func

# Decorate each promotion function
@promotion
def fidelity_promotion(order):
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0
#
# Concrete Strategies function: BulkItemPromotion
#
@promotion
def bulk_item_promotion(order):
    """10% discount for each LineItem with 20 or more units"""
    discount = 0
    for item in order.cart:
        if (item.quantity >= 20):
            discount = item.total() * .10
    return discount
#
# Concrete Strategies function: LargeOrderPromotion
#
@promotion
def large_order_promotion(order):
    """7% discount for orders with 10 or more distinct items"""
    # set of distinct items
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * 0.7
    return 0

def best_promo(order):
    """
    select the best discount available
    """
    return max(promo(order) for promo in promos)

if __name__ == "__main__":
    # Decorators are bounded or loaded when the file is read.
    print(promos)
    # two customers John (fidelity points 0) and Ann (fidelity points 1,100)
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    # One shopping cart with three items
    cart = [LineItem('banana', 4, .5),
            LineItem('apple', 10, 1.5),
            LineItem('watermelon', 5, 5.0)]

    # ten different items, each at $1.00
    long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    banana_cart = [LineItem('banana', 30, .5),
                   LineItem('apple', 10, 1.5)]
    # Test the meta-strategy
    print("-" * 35)
    print(Order(joe, long_order, best_promo))
    print(Order(joe, banana_cart, best_promo))
    print(Order(ann, cart, best_promo))
