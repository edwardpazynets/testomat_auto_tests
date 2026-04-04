import pytest
from faker import Faker

from src.web.Application import Application
from tests.conftest import Config


@pytest.mark.smoke
def test_login_invalid(configs: Config, app: Application):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(configs.email, Faker().password(length=10))
    app.login_page.invalid_login_message_visible()


def test_login_with_valid_creds(logged_in, app: Application):
    app.login_page.valid_message_visible()
