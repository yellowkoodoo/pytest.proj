from functools import cached_property

from playwright.sync_api import Page

from framework.flows.app_flows import AppFlows
from framework.pages.app_pages import AppPages


class App:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("/")

    @cached_property
    def PAGES(self):
        return AppPages(self.page)

    @cached_property
    def FLOWS(self):
        return AppFlows(self.page)
