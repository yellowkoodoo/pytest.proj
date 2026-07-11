import pytest
from playwright.sync_api import expect

from framework.enums.pages.pages import Pages
from framework.enums.shop.goods import Goods
from framework.pages.app import App


@pytest.mark.debug
def test_purchase_success(app_logged_in: App):

    itemsNumber: int = 2

    app_logged_in.top_bar.navigate_to(Pages.PRODUCTS)
    app_logged_in.products.product_item.add_to_cart(
        Goods.BluetoothSpeaker.value, itemsNumber
    )

    expect(app_logged_in.top_bar.cart_items).to_have_text(str(itemsNumber))

    app_logged_in.page.pause()
