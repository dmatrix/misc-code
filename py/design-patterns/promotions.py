#
# Concrete Strategies function: BulkItemPromotion
#
def fidelity_promotion(order):
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0
#
# Concrete Strategies function: BulkItemPromotion
#
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
def large_order_promotion(order):
    """7% discount for orders with 10 or more distinct items"""
    # set of distinct items
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * 0.7
    return 0
