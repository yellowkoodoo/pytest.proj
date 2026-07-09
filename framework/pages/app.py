from functools import cached_property

from playwright.sync_api import Page

from framework.pages.shop_pages.login_page import LoginPage
from framework.pages.shop_pages.top_bar_panel import TopBarPanel


class App:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("/")

    @cached_property
    def top_bar(self):
        return TopBarPanel(self.page)

    @cached_property
    def login(self):
        return LoginPage(self.page)
