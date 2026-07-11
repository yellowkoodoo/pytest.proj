from playwright.sync_api import Page

from framework.enums.locators import LocatorsMatchOptions
from framework.models.ui.purchase_item import PurchaseItem
from framework.pages.base.base_component_page import BaseComponent
from framework.utils.regex import Regex


class ProductItemPage(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

    def add_to_cart(self, item: PurchaseItem):
        self._add_to_cart_button(item.item.value).click(click_count=item.number)

    def _add_to_cart_button(self, name: str):
        return self._testid(
            "add-to-cart",
            match_option=LocatorsMatchOptions.STARTS,
            parent=self._item_by_name(name),
        )

    def _item_by_name(self, name: str):
        return self.page.locator(
            ".card", has=self.page.locator("h3", has_text=Regex.exact(name))
        )
