from typing import Literal

from playwright.sync_api import Page

from framework.enums.locators import LocatorsMatchOptions
from framework.models.ui.purchase_item import PurchaseItem
from framework.pages.base.base_component_page import BaseComponent
from framework.utils.regex import Regex


class CartItemPage(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

    def get_quantity(self, item: PurchaseItem):
        return self._testid(
            "qty",
            match_option=LocatorsMatchOptions.STARTS,
            parent=self._item_by_name(item.item.value),
        )

    def increase_quantity(self, item: PurchaseItem, number: int):
        self._change_quantity(item=item, number=number, operation="+")

    def decrease_quantity(self, item: PurchaseItem, number: int):
        self._change_quantity(item=item, number=number, operation="-")

    def remove_item(self, item: PurchaseItem):
        self._testid(
            "remove",
            match_option=LocatorsMatchOptions.STARTS,
            parent=self._item_by_name(item.item.value),
        ).text_content()

    def _item_by_name(self, name: str):
        return self.page.locator(
            ".card", has=self.page.locator("p", has_text=Regex.exact(name))
        )

    def _change_quantity(
        self, item: PurchaseItem, number: int, operation: Literal["+", "-"]
    ):
        self._locator(
            "button",
            has_text=f"{operation}",
            parent=self._item_by_name(item.item.value),
        ).click(click_count=number)
