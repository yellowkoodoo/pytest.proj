import pytest
from playwright.sync_api import expect

from framework.constants.login import LoginConstants
from framework.data.users import Users
from framework.enums.pages.pages import Pages
from framework.pages.app import App
from framework.utils.data_generation.user_gen import UserGenerator


@pytest.mark.smoke
def test_successful_login(app_no_user: App):
    user = Users.ALICE

    app_no_user.top_bar.navigate_to(Pages.LOGIN)
    app_no_user.login.login_as(user)

    greeting: str = f"Hi, {user.name}"
    expect(app_no_user.top_bar.greeting_text).to_have_text(greeting)


@pytest.mark.smoke
def test_login_failed_wrong_password(app_no_user: App):
    user = UserGenerator.create_user()

    app_no_user.top_bar.navigate_to(Pages.LOGIN)
    app_no_user.login.login(Users.ALICE.email, user.password)

    expect(app_no_user.login.login_error).to_have_text(
        LoginConstants.INVALID_CREDENTIALS_ERROR
    )


@pytest.mark.smoke
def test_login_failed_wrong_user(app_no_user: App):
    user = UserGenerator.create_user()

    app_no_user.top_bar.navigate_to(Pages.LOGIN)
    app_no_user.login.login(user.email, Users.ALICE.password)

    expect(app_no_user.login.login_error).to_have_text(
        LoginConstants.INVALID_CREDENTIALS_ERROR
    )
