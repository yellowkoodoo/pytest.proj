import pytest
from playwright.sync_api import expect

from framework.enums.pages.pages import Pages
from framework.models.ui.purchase_item import PurchaseItem
from framework.pages.app import App
from framework.utils.data_generation.products_gen import UserGenerator


@pytest.mark.debug
def test_purchase_success(app_logged_in: App):
    item: PurchaseItem = UserGenerator.purchase_item()

    app_logged_in.top_bar.navigate_to(Pages.PRODUCTS)
    app_logged_in.products.product_item.add_to_cart(item)
    expect(app_logged_in.top_bar.cart_items).to_have_text(str(item.number))

    app_logged_in.top_bar.navigate_to(Pages.CART)
    expect(app_logged_in.cart.cart_item.get_quantity(item)).to_have_text(
        str(item.number)
    )

    app_logged_in.page.pause()
