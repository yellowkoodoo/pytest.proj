import pytest

from framework.data.users import Users
from framework.enums.pages.pages import Pages
from framework.pages.app import App


@pytest.mark.smoke
def test_successful_login(app_no_user: App):

    app_no_user.top_bar.navigate_to(Pages.LOGIN)
    app_no_user.login.login_as(Users.ALICE)

    assert "/dashboard" in app_no_user.page.url
