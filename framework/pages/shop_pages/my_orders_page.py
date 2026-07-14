from functools import cached_property

from playwright.sync_api import Page, expect

from framework.pages.base.base_page import BasePage
from framework.pages.shop_pages.components.order_item import OrderItemPage
from framework.pages.shop_pages.components.view_order_page import ViewOrderPage


class MyOrdersPage(BasePage):
    URL = "/orders"

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def statuses_dropdown(self):
        return self._testid("status-filter")

    @property
    def order_item(self):
        return OrderItemPage(self.page)

    @cached_property
    def view_order(self):
        return ViewOrderPage(self.page)

    def check_loaded(self):
        expect(self.statuses_dropdown).to_be_visible()
