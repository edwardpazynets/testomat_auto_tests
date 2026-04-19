import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Playwright

load_dotenv()

BROWSER_LAUNCH_ARGS = {
    "headless": False,
    "slow_mo": 150,
    "timeout": 30000,
}


def _browser_context_args() -> dict:
    base_app_url = os.getenv("BASE_APP_URL")
    if not base_app_url:
        raise RuntimeError("BASE_APP_URL is not set. Check your .env file.")

    return {
        "base_url": base_app_url,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "permissions": ["geolocation"],
    }


@pytest.fixture(scope="session")
def browser_instance(playwright: Playwright) -> Browser:
    browser = playwright.chromium.launch(**BROWSER_LAUNCH_ARGS)
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def shared_context(browser_instance: Browser) -> BrowserContext:
    ctx = browser_instance.new_context(**_browser_context_args())
    ctx.new_page()
    yield ctx
    ctx.close()


@pytest.fixture(scope="session")
def logged_context(browser_instance: Browser) -> BrowserContext:
    ctx = browser_instance.new_context(**_browser_context_args())
    ctx.new_page()
    yield ctx
    ctx.close()


def clear_browser_state(context: BrowserContext) -> None:
    for page in context.pages:
        try:
            page.evaluate("localStorage.clear()")
            page.evaluate("sessionStorage.clear()")
        except Exception:
            pass
    for page in context.pages:
        page.goto("about:blank")
    context.clear_cookies()
