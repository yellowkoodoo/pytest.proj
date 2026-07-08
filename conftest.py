import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from config.settings import runnerSettings, settings

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

    # If --browser was provided, respect it.
    if browser:
        return browser

    return runnerSettings.DEFAULT_BROWSER


@pytest.fixture
def context(browser: Browser):
    context = browser.new_context(
        viewport = {
            "width": 1920,
            "height": 1080
        }
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    page = context.new_page()
    page.set_default_timeout(
        settings.TIMEOUT
    )
    yield page
    page.close()