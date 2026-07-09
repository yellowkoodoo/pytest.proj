import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from config.settings import runnerSettings, settings
from framework.pages.app import App


@pytest.fixture
def app(page: Page) -> App:
    app = App(page)
    app.open()
    return app


@pytest.fixture(scope="session")
def base_url():
    return settings.BASE_URL


# @pytest.fixture(scope="session")
# def browser_type_launch_args():
#     return {
#         "headless": True,
#         "slow_mo": 0,
#         "timeout": 30_000,
#         "args": [
#             "--start-maximized",
#             "--disable-dev-shm-usage",
#         ],
#     }

# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args):
#     return {
#         **browser_context_args,
#         "viewport": {
#             "width": 1920,
#             "height": 1080,
#         },
#         "locale": "en-US",
#         "timezone_id": "Europe/Kyiv",
#         "permissions": ["geolocation"],
#         "storage_state": "auth.json",
#     }


@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    browser = pytestconfig.getoption("--browser")

    if browser:
        return browser

    return runnerSettings.DEFAULT_BROWSER


@pytest.fixture
def context(browser: Browser):
    context = browser.new_context(
        base_url=settings.BASE_URL, viewport={"width": 1920, "height": 1080}
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    page = context.new_page()
    page.set_default_timeout(settings.TIMEOUT)
    yield page
    page.close()
