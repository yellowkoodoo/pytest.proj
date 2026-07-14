from playwright.sync_api import expect

from framework.enums.pages.pages import Pages
from framework.models.ui.purchase_item import PurchaseItem
from framework.pages.app_pages import AppPages


class CartFlow:
    def __init__(self, pages: AppPages):
        self.pages = pages

    def verify(self, items: list[PurchaseItem]):
        expected = sum(item.number for item in items)

        expect(self.pages.top_bar.cart_items).to_have_text(str(expected))

        self.pages.top_bar.navigate_to(Pages.CART)

        for item in items:
            expect(self.pages.cart.cart_item.get_quantity(item)).to_have_text(
                str(item.number)
            )

    def checkout(self):
        self.pages.cart.checkout()
