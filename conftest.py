import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from config.settings import settings

# @pytest.fixture(scope="session")
# def browser_type_launch_args():
#     return {
#         "headless": settings.HEADLESS
#     }


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