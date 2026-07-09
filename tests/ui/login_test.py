import pytest


@pytest.mark.debug
def test_successful_login(app):

    app.login.open()
    app.login.is_loaded()
    app.login.login("alice@example.com", "pass123")

    assert "/dashboard" in app.page.url