from functools import cached_property

from playwright.sync_api import Page

from framework.pages.shop_pages.login_page import LoginPage


class App:
    def __init__(self, page: Page):
        self.page = page

    # @property 
    @cached_property
    def login(self):
        return LoginPage(self.page)