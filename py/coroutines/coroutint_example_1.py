"""
Use a simple coroutine to manage and yield interest.
Yield allows data to be sent to the coroutine.
source: https://medium.com/swlh/what-is-yield-or-generator-in-python-4484a11362d0
"""


def bank_account(deposited, interest_rate):
    # loop forever and receive data
    while True:
        # suspend execution and return the value
        calculate_interest = interest_rate * deposited
        received = yield calculate_interest
        if received:
            deposited += received


if __name__ == '__main__':

    # The object is coroutine, no value is returned
    my_account = bank_account(1000, 0.05)
    print(my_account)
    # this is priming the coroutine to send subsequent values
    first_year_interest = next(my_account)
    print("interest earned: {}".format(first_year_interest))
    # send a new deposited value with the old interest of 0.05
    next_year_interest = my_account.send(first_year_interest + 1000)
    print("interest earned: {}".format(next_year_interest))
    interest_earned = 0
    for d in [1000, 1500, 2000, 2500, 3000]:
        deposit = d + interest_earned
        interest_earned = my_account.send(deposit)
        print("interest earned: {:4.2f} on deposit: {:6.2f}".format(interest_earned, deposit))


