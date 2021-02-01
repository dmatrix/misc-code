import descriptors as dsc


def print_items(item):
    print("description: {}, weight: {}, price: {}, number: {}, subtotal: {}"
          .format(item.description, item.weight,
                  item.price, item.number, item.subtotal()))
    print(sorted(vars(item).items()))


if __name__ == '__main__':
    berries = dsc.LineItem("Brazilian berries", 20, 17.95)
    print_items(berries)
    print("--" * 5)
    # set the number
    berries.number = 10
    print_items(berries)
