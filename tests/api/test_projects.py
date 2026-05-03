from unittest.mock import Mock, patch

import pytest
import requests

from src.api.client import Project, ProjectsClient
from tests.fixtures.config import Config


@pytest.mark.smoke
@pytest.mark.api
def test_get_projects_returns_200(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    assert projects.status_code == 200


@pytest.mark.api
def test_get_projects_response_is_json(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    assert "application" in projects.headers["Content-Type"].lower()
    assert "json" in projects.headers["Content-Type"].lower()


@pytest.mark.api
def test_get_projects_response_is_iterable(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    assert hasattr(projects, "__iter__")


@pytest.mark.api
def test_get_projects_list_is_not_empty(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    assert len(projects) > 0


@pytest.mark.api
def test_get_projects_items_have_required_fields(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    for project in projects:
        assert isinstance(project, Project)
        assert project.id
        assert project.type
        assert project.attributes


@pytest.mark.api
def test_get_projects_items_type_is_project(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    for project in projects:
        assert project.type == "project"


@pytest.mark.api
def test_get_projects_items_have_title(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    for project in projects:
        assert isinstance(project.title, str)
        assert len(project.title) > 0


@pytest.mark.api
def test_get_projects_items_have_slug(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    for project in projects:
        if project.slug is not None:
            assert isinstance(project.slug, str)
            assert len(project.slug) > 0


@pytest.mark.api
def test_get_projects_unauthorized(config: Config):
    try:
        projects = ProjectsClient.unauthorized(config.app_base_url).get_projects()
    except requests.RequestException as exc:
        pytest.skip(f"Testomat API is unavailable from this environment: {exc}")

    assert projects.status_code == 403


def test_authentication_sets_session_header():
    session = Mock()
    session.headers = {}
    session.post.return_value.json.return_value = {"jwt": "jwt-token"}
    session.post.return_value.raise_for_status.return_value = None

    with patch("src.api.client.requests.Session", return_value=session):
        ProjectsClient(base_url="https://app.testomat.io", api_token="token")

    session.post.assert_called_once_with(
        "https://app.testomat.io/api/login",
        json={"api_token": "token"},
        timeout=30,
    )
    assert session.headers["Authorization"] == "jwt-token"
