#
# Function strategy design pattern, aka flyweight pattern, refactored from the classic
# strategy pattern invovles the following components.
#
# Context:
# Provides the service by delegating certain computations to other
# components depending on their respective attributes. In our example below,
# the context is "Order."
#
# Concrete Flyweight Strategy:
# These are now functions instead of instances of an abstract class."
# For example, "FidelityPromo," "BulkPromo," and "LargerOrderPromo."
#
#
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:
    """
    The Context for the Strategy
    """

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
# define a meta-strategy that computes the best promotion for each
# Order
#


import inspect
import promotions

# Use list comprehension and introspection to build the function list

promos = [func for name, func in
          inspect.getmembers(promotions, inspect.isfunction)]


def best_promo(order):
    """Select the best discount available"""
    # use generator expression to compute each promotion and return
    # the maximum
    return max(promo(order) for promo in promos)

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
    joe_order = Order(joe, cart, promotions.bulk_item_promotion)
    ann_order = Order(ann, cart, promotions.fidelity_promotion)
    print(joe_order)
    print(ann_order)
    # create a banana cart
    banana_cart = [LineItem('banana', 30, .5),
                   LineItem('apple', 10, 1.5)]
    joe_bc_order = Order(joe, banana_cart, promotions.bulk_item_promotion)
    print(joe_bc_order)
    # ten different items, each at $1.00
    long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    joe_long_order = Order(joe, long_order, promotions.large_order_promotion)
    print(joe_long_order)
    # use a different cart for joe
    joe_different = Order(joe, cart, promotions.large_order_promotion)
    print(joe_different)
    # Test the meta-strategy
    print("-" * 35)
    print(Order(joe, long_order, best_promo))
    print(Order(joe, banana_cart, best_promo))
    print(Order(ann, cart, best_promo))
