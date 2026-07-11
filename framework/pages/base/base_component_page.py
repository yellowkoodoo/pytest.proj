from playwright.sync_api import Page

from framework.pages.base.base_page import BasePage


class BaseComponent(BasePage):
    URL = "/"

    def __init__(self, page: Page):
        self.page = page

    def check_loaded(self):
        return None
