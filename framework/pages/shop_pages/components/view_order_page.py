from playwright.sync_api import Page

from framework.pages.base.base_page import BasePage


class ViewOrderPage(BasePage):
    URL = "/"

    def __init__(self, page: Page):
        super().__init__(page)

    def check_loaded(self):
        return

    @property
    def order_id(self):
        return self._testid("h1")
