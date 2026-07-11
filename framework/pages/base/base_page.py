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
        *,
        match_option: LocatorsMatchOptions = LocatorsMatchOptions.EXACT,
        has_text: str | None = None,
        parent: Locator | None = None,
    ) -> Locator:
        root = parent or self.page
        selector = f"[data-testid{match_option.value}'{test_id}']"

        if has_text is None:
            return root.locator(selector)

        return root.locator(selector, has_text=has_text)

    def _locator(
        self,
        selector: str,
        *,
        match_option: LocatorsMatchOptions = LocatorsMatchOptions.EXACT,
        has_text: str | None = None,
        parent: Locator | None = None,
    ) -> Locator:
        root = parent or self.page

        if has_text is None:
            return root.locator(selector)

        return root.locator(selector, has_text=has_text)
