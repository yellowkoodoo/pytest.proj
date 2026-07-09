import pytest

from framework.data.users import Users
from framework.enums.top_panel import Buttons


# @pytest.mark.debug
def test_successful_login(app):

    app.login.open()
    app.login.is_loaded()
    app.login.login("alice@example.com", "pass123")

    assert "/dashboard" in app.page.url


@pytest.mark.debug
def test_successful_login_2(app):

    app.top_bar.click_button(Buttons.LOGIN)
    app.login.login_as(Users.ALICE)

    assert "/dashboard" in app.page.url
