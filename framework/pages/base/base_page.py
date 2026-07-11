from abc import ABC, abstractmethod

from playwright.sync_api import Locator, Page

from framework.enums.locators import LocatorsMatchOptions


class BasePage(ABC):
    URL = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    @abstractmethod
    def check_loaded(self) -> None:
        raise NotImplementedError

    def _testid(
        self,
        test_id: str,
        matchOption: LocatorsMatchOptions = LocatorsMatchOptions.EXACT,
        parent: Locator | None = None,
    ) -> Locator:
        root = parent or self.page
        return root.locator(f"[data-testid{matchOption.value}'{test_id}']")
