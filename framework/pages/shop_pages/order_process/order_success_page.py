from playwright.sync_api import Page

from framework.pages.base.base_page import BasePage


class OrderSuccessPage(BasePage):
    URL = "/"

    def __init__(self, page: Page):
        super().__init__(page)

    def check_loaded(self):
        return

    @property
    def message(self):
        return self._testid("success-msg")

    @property
    def order_id(self) -> str:
        return str(self._testid("order-id").text_content())

    def payment_status(self):
        return self._testid("payment-status")

    @property
    def _view_my_orders_button(self):
        return self.page.locator("button", has_text="View My Orders")

    @property
    def _continue_shopping_button(self):
        return self.page.locator("button", has_text="Continue Shopping")

    def click_view_my_orders(self):
        return self._view_my_orders_button.click()
