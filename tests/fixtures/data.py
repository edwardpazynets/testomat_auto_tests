import pytest

from src.config import Config, load_config_from_env


@pytest.fixture
def target_project() -> str:
    return "python auto tests"


@pytest.fixture(scope="session")
def configs() -> Config:
    return load_config_from_env()
