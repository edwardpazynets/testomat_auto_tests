import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from src.web.Application import Application
from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage

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


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "headless": False,
        "slow_mo": 150,
        "timeout": 30000,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": "https://app.testomat.io",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        # "record_video_dir": "videos/",
        "permissions": ["geolocation"],
    }


@pytest.fixture(scope="function")
def app(page: Page, configs: Config) -> Application:
    return Application(page, configs.base_url)


@pytest.fixture()
def logged_in(page, configs: Config):
    home_page = HomePage(page, configs.base_url)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)


@pytest.fixture
def target_project():
    return "python auto tests"
