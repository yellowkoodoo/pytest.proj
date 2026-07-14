from enum import Enum


class PaymentMethods(Enum):
    CreditCard = "Credit Card (Visa ending 4242)"
    PayPal = "PayPal"
    DeclinedCard = "Test: Declined Card"
