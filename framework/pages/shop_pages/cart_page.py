from playwright.sync_api import Page

from framework.pages.base.base_page import BasePage
from framework.pages.shop_pages.components.cart_item import CartItemPage


class CartPage(BasePage):
    URL = "/cart"

    def __init__(self, page: Page):
        super().__init__(page)

    def check_loaded(self):
        return

    @property
    def total_text(self):
        return self._testid("cart-total")

    @property
    def checkout_button(self):
        return self._testid("checkout-btn")

    @property
    def cart_item(self):
        return CartItemPage(self.page)

    def checkout(self):
        self.checkout_button.click()
