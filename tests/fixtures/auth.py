import pytest
from playwright.sync_api import BrowserContext

from src.config import Config
from src.web.application import Application
from tests.fixtures.browser import clear_browser_state


@pytest.fixture(scope="function")
def app(shared_context: BrowserContext, configs: Config) -> Application:
    clear_browser_state(shared_context)
    page = shared_context.pages[0]
    yield Application(page, configs.base_url)
    clear_browser_state(shared_context)


@pytest.fixture(scope="function")
def logged_app(logged_context: BrowserContext, configs: Config) -> Application:
    clear_browser_state(logged_context)
    page = logged_context.pages[0]
    application = Application(page, configs.base_url)

    application.home_page.open()
    application.home_page.click_login()
    application.login_page.expect_loaded()
    application.login_page.login_as(configs.email, configs.password)
    application.login_page.expect_login_success_message()

    yield application
    clear_browser_state(logged_context)
