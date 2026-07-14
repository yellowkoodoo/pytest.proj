from framework.enums.shop.user_currency import Currency


def money(currency: Currency, amount: float):
    return f"{currency.value}{amount}"
