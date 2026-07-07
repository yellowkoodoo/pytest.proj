import os
from enum import Enum

from dotenv import load_dotenv

ENV = os.getenv(
    "ENV",
    "qa"
)

load_dotenv(
    f'config/.env.{ENV}'
)

class Settings:

    # Environment
    ENV = ENV

    # Application
    BASE_URLS = {
        "dev": "https://dev.example.com",
        "qa": "https://qa.example.com",
        "staging": "https://staging.example.com",
        "prod": "https://example.com"
    }

    @property
    def BASE_URL(self):
        return self.BASE_URLS[self.ENV]
    
    # Playwright settings
    TIMEOUT = int(
        os.getenv(
            "TIMEOUT",
            "30000"
        )
    )

    NAVIGATION_TIMEOUT = int(
        os.getenv(
            "NAVIGATION_TIMEOUT",
            "30000"
        )
    )    

class RunnerSettings:

    class Browser(Enum):
        CHROMIUM = "chromium"
        FIREFOX = "firefox"
        WEBKIT = "webkit"
    
    # BROWSER = os.getenv(
    #     "BROWSER",
    #     "firefox"
    # )
    DEFAULT_BROWSER = Browser.FIREFOX

    # DEFAULT_HEADLESS_MODE = (
    #     os.getenv(
    #         "HEADLESS",
    #         "false"
    #     ).lower() == "true"
    # )
    DEFAULT_HEADLESS = bool(0)

    DEFAULT_VIEWPORT = {
        "width": 1920,
        "height": 1080
    }

settings = Settings()
runnerSettings = RunnerSettings()