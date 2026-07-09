from playwright.sync_api import Page


class BasePage:
    URL = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def _testid(self, test_id: str):
        return self.page.locator(f"[data-testid='{test_id}']")
