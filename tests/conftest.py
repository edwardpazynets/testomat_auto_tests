import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, Playwright

from src.web.Application import Application

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    login_url: str
    email: str
    password: str


BROWSER_LAUNCH_ARGS = {
    "headless": False,
    "slow_mo": 150,
    "timeout": 30000,
}

BROWSER_CONTEXT_ARGS = {
    "base_url": os.getenv("BASE_APP_URL"),
    "viewport": {"width": 1920, "height": 1080},
    "locale": "uk-UA",
    "timezone_id": "Europe/Kyiv",
    "permissions": ["geolocation"],
}


@pytest.fixture(scope="session")
def configs() -> Config:
    return Config(
        base_url=os.getenv("BASE_URL"),
        login_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
    )


@pytest.fixture(scope="session")
def browser_instance(playwright: Playwright) -> Browser:
    browser = playwright.chromium.launch(**BROWSER_LAUNCH_ARGS)
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def auth_state(browser_instance: Browser, configs: Config) -> dict:
    ctx = browser_instance.new_context(**BROWSER_CONTEXT_ARGS)
    page = ctx.new_page()

    app = Application(page, configs.base_url)
    app.home_page.open()
    app.home_page.click_login()
    app.login_page.login_user(configs.email, configs.password)
    app.login_page.valid_message_visible()

    storage = ctx.storage_state()
    ctx.close()
    return storage


@pytest.fixture(scope="function")
def app(browser_instance: Browser, configs: Config) -> Application:
    ctx = browser_instance.new_context(**BROWSER_CONTEXT_ARGS)
    page = ctx.new_page()
    yield Application(page, configs.base_url)
    ctx.close()


@pytest.fixture(scope="function")
def logged_app(browser_instance: Browser, auth_state: dict, configs: Config) -> Application:
    ctx = browser_instance.new_context(
        **BROWSER_CONTEXT_ARGS,
        storage_state=auth_state,
    )
    page = ctx.new_page()
    page.goto(configs.login_url)
    application = Application(page, configs.base_url)
    yield application
    ctx.close()


@pytest.fixture
def target_project() -> str:
    return "python auto tests"
