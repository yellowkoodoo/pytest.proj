from playwright.sync_api import Page, expect

from framework.enums.pages.pages import Pages
from framework.enums.pages.top_panel import Buttons
from framework.pages.base.base_page import BasePage


class TopBarPanel(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def nav_panel(self):
        return self.page.locator("nav")

    @property
    def products_button(self):
        return self.nav_panel.get_by_role("link", name="Products")

    @property
    def logout_button(self):
        return self.nav_panel.get_by_role("button", name="Logout")

    @property
    def greeting_text(self):
        return self.nav_panel.locator("span")

    @property
    def cart_items(self):
        return self._button(Buttons.CART).locator("button").locator("span")

    def check_loaded(self):
        expect(self._button(Buttons.PRODUCTS)).to_be_visible()

    def navigate_to(self, page: Pages):
        button = self._page_to_button_mapping(page)

        if button == Buttons.LOGOUT:
            return self.logout_button.click()
        if button == Buttons.PRODUCTS:
            return self.products_button.click()

        return self._button(button).click()

    def _button(self, button: Buttons):
        return self.nav_panel.locator(f"a[href='/{button.value}']")

    def _page_to_button_mapping(self, page: Pages) -> Buttons:
        mapping = {
            Pages.PRODUCTS: Buttons.PRODUCTS,
            Pages.CART: Buttons.CART,
            Pages.ORDERS: Buttons.ORDERS,
            Pages.LOGIN: Buttons.LOGIN,
            Pages.LOGOUT: Buttons.LOGOUT,
        }

        return mapping[page]
