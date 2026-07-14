from playwright.sync_api import Page

from framework.enums.shop.payment_methods import PaymentMethods
from framework.pages.base.base_page import BasePage
from framework.pages.shop_pages.components.cart_item import CartItemPage


class CheckoutPage(BasePage):
    URL = "/"

    def __init__(self, page: Page):
        super().__init__(page)

    def check_loaded(self):
        return

    @property
    def checkout_total(self):
        return self._testid("checkout-total")

    @property
    def payment_method_CC_button(self):
        return self._testid("payment-credit_card")

    @property
    def payment_method_paypal_button(self):
        return self._testid("payment-paypal")

    @property
    def payment_method_invalid_card_button(self):
        return self._testid("payment-invalid_card")

    @property
    def place_order_button(self):
        return self._testid("place-order-btn")

    @property
    def cart_item(self):
        return CartItemPage(self.page)

    def select_payment_method(self, method: PaymentMethods):
        payment_buttons = {
            PaymentMethods.CreditCard: self.payment_method_CC_button,
            PaymentMethods.PayPal: self.payment_method_paypal_button,
            PaymentMethods.DeclinedCard: self.payment_method_invalid_card_button,
        }

        button = payment_buttons.get(method)

        if button is None:
            raise ValueError(f"Unsupported payment method: {method}")

        return button.click()

    def create_order(self):
        self.place_order_button.click()
