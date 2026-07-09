from playwright.sync_api import Page, expect

from framework.models.user import User
from framework.pages.base.base_page import BasePage


class LoginPage(BasePage):
    URL = "/login"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("[data-testid='email-input']")
        self.password_input = page.locator("[data-testid='password-input']")
        self.login_button = page.locator("[data-testid='login-btn']")

    def open(self):
        super().open()        

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login_as(self, user: User):
        self.login(user.username, user.password)

    def is_loaded(self):
        expect(self.login_button).to_be_visible()

    def expect_login_failed(self, message: str):
        expect(self.error_message).to_have_text(message)