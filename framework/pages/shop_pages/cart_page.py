from playwright.sync_api import Page

from framework.pages.base.base_page import BasePage
from framework.pages.shop_pages.components.cart_item import CartItemPage


class CartPage(BasePage):
    URL = "/cart"

    def __init__(self, page: Page):
        super().__init__(page)

    def check_loaded(self):
        # expect(self.login_button).to_be_visible()
        return

    @property
    def cart_item(self):
        return CartItemPage(self.page)
