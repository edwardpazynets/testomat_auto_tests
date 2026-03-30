import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from src.web.Application import Application
from web.pages.HomePage import HomePage
from web.pages.LoginPage import LoginPage

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    login_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv('BASE_URL'),
        login_url=os.getenv('BASE_APP_URL'),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD")
    )


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture()
def logged_in(page, configs: Config):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)


@pytest.fixture
def target_project():
    return "python auto tests"
