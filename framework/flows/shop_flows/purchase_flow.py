from framework.enums.pages.pages import Pages
from framework.models.ui.purchase_item import PurchaseItem
from framework.pages.app_pages import AppPages


class PurchaseFlow:
    def __init__(self, pages: AppPages):
        self.pages = pages

    def add_items(self, items: list[PurchaseItem]):
        self.pages.top_bar.navigate_to(Pages.PRODUCTS)

        for item in items:
            self.pages.products.search_product(item.item)
            self.pages.products.product_item.add_to_cart(item)
