from playwright.sync_api import Page, expect


class LoginPage:
    URL = "/login"

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.username_input = page.locator("[data-testid='email-input']")
        self.password_input = page.locator("[data-testid='password-input']")
        self.login_button = page.locator("[data-testid='login-btn']")

    def open(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login_as(self, user):
        """Accepts a user object with username/password attributes."""
        self.login(user.username, user.password)

    def is_loaded(self):
        expect(self.login_button).to_be_visible()

    def expect_login_failed(self, message: str):
        expect(self.error_message).to_have_text(message)