import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv

load_dotenv()


class Projects:
    SEARCH_PROJECT = "python auto tests"
    EXPECTED_PLAN = "Enterprise Plan"


class Companies:
    QA_CLUB_LVIV = "QA Club Lviv"


@dataclass(frozen=True)
class Config:
    base_url: str
    app_base_url: str
    email: str
    password: str
    testomat_api_token: str | None

    @property
    def login_url(self) -> str:
        return self.base_url


@pytest.fixture(scope="session")
def config() -> Config:
    return Config(
        base_url=os.getenv("BASE_URL"),
        app_base_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        testomat_api_token=os.getenv("TESTOMAT_API_TOKEN"),
    )


@pytest.fixture
def target_project() -> str:
    return Projects.SEARCH_PROJECT


@pytest.fixture
def expected_plan() -> str:
    return Projects.EXPECTED_PLAN


@pytest.fixture
def configs(config: Config) -> Config:
    return config
