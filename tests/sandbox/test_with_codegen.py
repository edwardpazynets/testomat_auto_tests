import pytest
from playwright.sync_api import Page, expect
from src.config import Config

from src.web.application import Application

pytestmark = pytest.mark.sandbox


def test_login_example(app: Application, configs: Config) -> None:
    page = app.page
    app.home_page.open()
    app.home_page.click_login()
    app.login_page.expect_loaded()

    page.get_by_role("textbox", name="name@email.com").fill(configs.email)
    page.locator("#content-desktop").locator("#user_password").fill("invalid_password_123")
    page.get_by_role("button", name="Sign in").click()

    expect(
        page.locator("#content-desktop").get_by_text("Invalid Email or password.")
    ).to_be_visible()

    # codegen version


def test_example(page: Page) -> None:
    page.goto("https://testomat.io/")
    expect(page.get_by_role("link", name="AI orchestration AI")).to_be_visible()

    page.get_by_role("link", name="Log in").click()


pytest.skip("Sandbox tests are disabled; use web tests only.", allow_module_level=True)
