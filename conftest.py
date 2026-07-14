from collections.abc import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright
from pytest import Config

from config.settings import runnerSettings, settings
from framework.api.auth_api import AuthApi
from framework.data.users import Users
from framework.pages.app import App
from framework.utils.session.session import read_session

# import fixtures from other files
# pytest_plugins = ["tests.fixtures"]


@pytest.fixture
def app_no_user(page: Page) -> App:
    app = App(page)
    app.open()
    return app


@pytest.fixture
def app_logged_in_v0(page: Page) -> App:
    app = App(page)
    app.open()
    app.login.login_as(Users.ALICE)
    return app


@pytest.fixture
def app_logged_in(playwright: Playwright, page: Page) -> Generator[App]:

    BASE_API_URL = settings.BASE_API_URL
    request = playwright.request.new_context(base_url=BASE_API_URL)
    auth = AuthApi(request)

    user = Users.ALICE
    auth.login(user)

    token = read_session()
    page.add_init_script(
        f"""
        window.localStorage.setItem("token", "{token}");
        """
    )

    app = App(page)
    app.open()

    try:
        yield app
    finally:
        auth.logout(user)


@pytest.fixture
def app_logged_admin(page: Page) -> App:
    app = App(page)
    app.open()
    app.login.login_as(Users.ADMIN)
    return app


@pytest.fixture(scope="session")
def base_url():
    return settings.BASE_URL


# @pytest.fixture(scope="session")
# def browser_type_launch_args():
#     return {
#         # "headless": True,
#         #"slow_mo": 5000,
#         # "timeout": 30_000,
#         # "args": [
#         #     "--start-maximized",
#         #     "--disable-dev-shm-usage",
#         # ],
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
def browser_name(pytestconfig: Config) -> str:
    browser = pytestconfig.getoption("--browser")

    if browser:
        return browser

    return runnerSettings.DEFAULT_BROWSER.value


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
