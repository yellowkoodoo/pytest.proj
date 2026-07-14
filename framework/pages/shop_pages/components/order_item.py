from playwright.sync_api import Page

from framework.enums.locators import LocatorsMatchOptions
from framework.pages.base.base_component_page import BaseComponent


class OrderItemPage(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

    def get_order_status(self, order: str):
        return self._testid(
            "status-ord",
            match_option=LocatorsMatchOptions.STARTS,
            parent=self._order_item(order),
        )

    def view_order(self, order: str):
        return self._order_item(order).locator("button", has_text="View").click()

    def _order_item(self, order: str):
        return self._testid(
            "order-ord", match_option=LocatorsMatchOptions.STARTS, has_text=order
        )
