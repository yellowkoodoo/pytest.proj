from playwright.sync_api import Page


def test_navigate_to_google(page: Page):
    page.goto("https://www.google.com")

    assert page.title() == "Google1"

    # app_no_user.page.pause()
