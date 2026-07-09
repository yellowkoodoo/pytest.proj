from playwright.sync_api import Page, expect

from framework.models.user import User
from framework.pages.base.base_page import BasePage


class LoginPage(BasePage):
    URL = "/login"

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def username_input(self):
        return self._testid("email-input")

    @property
    def password_input(self):
        return self._testid("password-input")

    @property
    def login_button(self):
        return self._testid("login-btn")

    def is_loaded(self):
        expect(self.login_button).to_be_visible()

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login_as(self, user: User):
        self.login(user.username, user.password)

    def expect_login_failed(self, message: str):
        expect(self.error_message).to_have_text(message)
