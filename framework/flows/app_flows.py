from functools import cached_property

from framework.flows.shop_flows.cart_flow import CartFlow
from framework.flows.shop_flows.checkout_flow import CheckoutFlow
from framework.flows.shop_flows.order_flow import OrderFlow
from framework.flows.shop_flows.purchase_flow import PurchaseFlow
from framework.pages.app_pages import AppPages


class AppFlows:
    def __init__(self, pages: AppPages):
        self.pages = pages

    @cached_property
    def purchase(self):
        return PurchaseFlow(self.pages)

    @cached_property
    def cart(self):
        return CartFlow(self.pages)

    @cached_property
    def checkout(self):
        return CheckoutFlow(self.pages)

    @cached_property
    def order(self):
        return OrderFlow(self.pages)
