from playwright.sync_api import Page, expect

from framework.enums.top_panel import Buttons
from framework.pages.base.base_page import BasePage


class TopBarPanel(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def nav_panel(self):
        return self.page.locator("nav")

    @property
    def logout_button(self):
        return self.nav_panel.get_by_role("button", name="Logout")
    
    @property
    def greeting_text(self):
        return self.nav_panel.locator("span")
    

    def is_loaded(self):
        expect(self.button(Buttons.LOGIN)).to_be_visible()

    def button(self, button: Buttons):
        print("button.value")
        print(button.value)
        return self.nav_panel.locator(f"a[href='/{button.value}']")

    def click_button(self, button: Buttons):
        self.is_loaded()

        if button == Buttons.LOGOUT:
            return self.logout_button.click()
        
        return self.button(button).click()
                

