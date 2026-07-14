from playwright.sync_api import Page, expect

from framework.pages.base.base_page import BasePage
from framework.pages.shop_pages.components.product_item import ProductItemPage


class MyOrdersPage(BasePage):
    URL = "/orders"

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def statuses_dropdown(self):
        return self._testid("status-filter")

    @property
    def product_item(self):
        return ProductItemPage(self.page)

    def check_loaded(self):
        expect(self.statuses_dropdown).to_be_visible()
