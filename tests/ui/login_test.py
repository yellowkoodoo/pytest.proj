import pytest

from framework.pages.shop_pages.login_page import LoginPage


@pytest.mark.debug
def test_successful_login(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.is_loaded()
    login_page.login("alice@example.com", "pass123")

    assert "/dashboard" in page.url