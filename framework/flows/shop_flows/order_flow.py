from playwright.sync_api import expect

from framework.constants.shop import ShopConstants
from framework.pages.app_pages import AppPages


class OrderFlow:
    def __init__(self, pages: AppPages):
        self.pages = pages

    def verify_success(self):
        expect(self.pages.checkout.order_success.message).to_have_text(
            ShopConstants.ORDER_SUCCESS_MESSAGE
        )

    def open(self, order_id: str):
        self.pages.checkout.order_success.click_view_my_orders()
        self.pages.my_orders.order_item.view_order(order_id)
