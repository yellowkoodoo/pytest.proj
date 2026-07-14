from playwright.sync_api import Page, expect

from framework.enums.shop.goods import Goods
from framework.pages.base.base_page import BasePage
from framework.pages.shop_pages.components.product_item import ProductItemPage


class ProductsPage(BasePage):
    URL = "/"

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def search_input(self):
        return self._testid("search-input")

    @property
    def categories_dropdown(self):
        return self._testid("category-filter")

    @property
    def sorting_dropdown(self):
        return self._testid("sort-select")

    @property
    def product_item(self):
        return ProductItemPage(self.page)

    def check_loaded(self):
        expect(self.search_input).to_be_visible()

    def search_product(self, item: Goods):
        self.search_input.fill(item.value)
        expect(self.product_item.get_item(item.value)).to_have_count(1)
