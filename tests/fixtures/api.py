import pytest
import requests

from src.api.client import ProjectsClient
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def projects_client(config: Config) -> ProjectsClient:
    if not config.testomat_api_token:
        pytest.skip("TESTOMAT_API_TOKEN is not configured")

    try:
        with ProjectsClient(
            base_url=config.app_base_url,
            api_token=config.testomat_api_token,
        ) as client:
            yield client
    except requests.RequestException as exc:
        pytest.skip(f"Testomat API is unavailable from this environment: {exc}")


@pytest.fixture(scope="session")
def unauthorized_projects_client(config: Config) -> ProjectsClient:
    with ProjectsClient.unauthorized(config.app_base_url) as client:
        yield client
