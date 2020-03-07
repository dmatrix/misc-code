#
# Classic strategy design pattern invovles the following components.
# Example borrowed from "Fluent Python: Luciano Ramalho."
# Context:
# Provides the service by delegating certain computations to other
# components depending on their respective attributes. In our example below,
# the context is "Order."

# The class strategy design pattern invovles the following components.
# Example borrowed from "Fluent Python: Luciano Ramalho."
#
# Context:
# Provides the service by delegating certain computations to other
# components depending on their respective attributes. In our example below,
# the context is "Order."
#
# Strategy:
# An abstract class that provides abstract classes for different
# implememtation of algorithms
#
# Concrete Strategy:
# These are instances of an abstract class Promotion."
# For example, "FidelityPromo," "BulkPromo," and "LargerOrderPromo."
#
from collections import namedtuple
from abc import ABC, abstractmethod

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
            discount = self.promotion.discount(self)

        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due:{:2f}>'
        return fmt.format(self.total(), self.due())
#
# The Strategy as an Abstract base class
#
class Promotion(ABC):
    @abstractmethod
    def discount(self, order):
        """Return discount as a positive dollar amount"""
#
# Concrete Strategies: FidelityPromotion
#
class FidelityPromotion(Promotion):
    """5% discount for customers with 1000 or more fidelity points"""

    def discount(self, order):
        return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0

#
# Concrete Strategies: BulkItemPromotion
#
class BulkItemPromotion(Promotion):
    """10% discount for each LineItem with 20 or more units"""

    def discount(self, order):
        discount = 0
        for item in order.cart:
            if (item.quantity >= 20):
                discount = item.total() * .10
        return discount
#
# Concrete Strategies: LargeOrderPromotion
#
class LargeOrderPromotion(Promotion):
    """7% discount for orders with 10 or more distinct items"""

    def discount(self, order):
        # set of distinct items
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * 0.7
        return 0

#
# driver to test our stratgies
#
if __name__ == "__main__":
    # two customers John (fidelity points 0) and Ann (fidelity points 1,100)
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    # One shopping cart with three items
    cart = [LineItem('banana', 4, .5),
            LineItem('apple', 10, 1.5),
            LineItem('watermelon', 5, 5.0)]
    joe_order = Order(joe, cart, FidelityPromotion())
    ann_order = Order(ann, cart, FidelityPromotion())
    print(joe_order)
    print(ann_order)
    # create a banana cart
    banana_cart = [LineItem('banana', 30, .5),
                   LineItem('apple', 10, 1.5)]
    joe_bc_order = Order(joe, banana_cart, BulkItemPromotion())
    print(joe_bc_order)
    # ten different items, each at $1.00
    long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    joe_long_order = Order(joe, long_order, LargeOrderPromotion())
    print(joe_long_order)
    # use a different cart for joe
    joe_different = Order(joe, cart, LargeOrderPromotion())
    print(joe_different)
