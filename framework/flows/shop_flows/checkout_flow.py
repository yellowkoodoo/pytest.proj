from framework.enums.shop.payment_methods import PaymentMethods
from framework.pages.app_pages import AppPages


class CheckoutFlow:
    def __init__(self, pages: AppPages):
        self.pages = pages

    def place_order(
        self,
        payment: PaymentMethods,
    ) -> str:

        self.pages.checkout.make_checkout.select_payment_method(payment)
        self.pages.checkout.make_checkout.create_order()

        return self.pages.checkout.order_success.order_id
