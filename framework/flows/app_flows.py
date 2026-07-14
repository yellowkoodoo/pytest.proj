from functools import cached_property

from playwright.sync_api import Page

from framework.pages.shop_pages.cart_page import CartPage
from framework.pages.shop_pages.login_page import LoginPage
from framework.pages.shop_pages.my_orders_page import MyOrdersPage
from framework.pages.shop_pages.order_process.checkout_page import CheckoutPage
from framework.pages.shop_pages.order_process.order_success_page import OrderSuccessPage
from framework.pages.shop_pages.products_page import ProductsPage
from framework.pages.shop_pages.top_bar_panel import TopBarPanel


class AppFlows:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("/")

    @cached_property
    def login(self):
        return LoginPage(self.page)

    @cached_property
    def top_bar(self):
        return TopBarPanel(self.page)

    @cached_property
    def products(self):
        return ProductsPage(self.page)

    @cached_property
    def cart(self):
        return CartPage(self.page)

    @cached_property
    def checkout(self):
        return CheckoutFlow(self.page)

    @cached_property
    def my_orders(self):
        return MyOrdersPage(self.page)


class CheckoutFlow:
    def __init__(self, page: Page):
        self.page = page

    @cached_property
    def make_checkout(self):
        return CheckoutPage(self.page)

    @cached_property
    def order_success(self):
        return OrderSuccessPage(self.page)
