"""
Use cooperative delegation for sub-coroutines
source: https://medium.com/swlh/what-is-yield-or-generator-in-python-4484a11362d0
money_manager function: manages the investment yield
investment_account: delegates to by money_manager
individual investments
"""


def money_manager(expected_rate):
    """
    manages the investment yield
    """
    under_management = yield  # must receive the deposited value
    while True:
        try:
            additional_investment = yield expected_rate * under_management
            if additional_investment:
                under_management += additional_investment
        except GeneratorExit:
            pass    # ignored
        finally:
            pass    # ignored


def investment_account(deposited, manager):
    """
    very simple model of an investment account that delegates to a manger
    """
    # prime the manager by queuing it
    next(manager)
    manager.send(deposited)
    while True:
        try:
            yield from manager
        except GeneratorExit:
            return manager.close()


if __name__ == '__main__':
    my_manager = money_manager(0.06)
    my_account = investment_account(1000, my_manager)
    # prime the coroutine to delegate the first account
    interest_earned = next(my_account)
    print("interest earned: {:4.2f} on deposit: {:6.2f}".format(interest_earned, 1000))
    for d in [1500, 2000, 2500, 3000]:
        deposit = d + interest_earned
        interest_earned = my_account.send(deposit)
        print("interest earned: {:4.2f} on deposit: {:6.2f}".format(interest_earned, deposit))
