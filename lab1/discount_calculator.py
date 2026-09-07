"""Small discount calculator used in CS413 Lab 1."""


def calculate_total(prices, discount_percent):
    """Return the total after applying a percentage discount."""
    subtotal = sum(prices)
    return subtotal * (1 - discount_percent / 100.0)


def main():
    prices = [50.0, 40.0, 60.0]
    discount_percent = 20
    expected_total = 120.0
    actual_total = calculate_total(prices, discount_percent)

    print("Subtotal:       ${:.2f}".format(sum(prices)))
    print("Discount:        {}%".format(discount_percent))
    print("Expected total: ${:.2f}".format(expected_total))
    print("Program output: ${:.2f}".format(actual_total))


if __name__ == "__main__":
    main()
