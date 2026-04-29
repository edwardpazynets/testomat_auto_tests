import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ProjectAttributes:
    title: str
    slug: str | None
    url: str | None
    description: str | None
    private: bool
    enabled: bool
    status: str | None
    tests_count: int | None
    created_at: str | None
    updated_at: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectAttributes":
        return cls(
            title=data["title"],
            slug=data.get("slug"),
            url=data.get("testomatio-url"),
            description=data.get("description"),
            private=data.get("private", False),
            enabled=data.get("enabled", True),
            status=data.get("status"),
            tests_count=data.get("tests-count"),
            created_at=data.get("created-at"),
            updated_at=data.get("updated-at"),
        )


@dataclass
class Project:
    id: str
    type: str
    attributes: ProjectAttributes

    @property
    def url(self) -> str | None:
        return self.attributes.url

    @property
    def title(self) -> str:
        return self.attributes.title

    @property
    def slug(self) -> str | None:
        return self.attributes.slug

    @property
    def status(self) -> str | None:
        return self.attributes.status

    @property
    def tests_count(self) -> int | None:
        return self.attributes.tests_count

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        return cls(
            id=str(data["id"]),
            type=data["type"],
            attributes=ProjectAttributes.from_dict(data["attributes"]),
        )


@dataclass
class ProjectsResponse:
    data: list[Project]
    status_code: int
    headers: dict
    url: str

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    @classmethod
    def from_response(cls, response: requests.Response) -> "ProjectsResponse":
        data = []
        if response.ok:
            data = [Project.from_dict(item) for item in response.json().get("data", [])]
        return cls(
            data=data,
            status_code=response.status_code,
            headers=dict(response.headers),
            url=response.url,
        )


class ProjectsClient:
    def __init__(self, base_url: str, api_token: str):
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        jwt = self._login(api_token)
        self._session.headers.update({"Authorization": jwt})

    @classmethod
    def from_env(cls) -> "ProjectsClient":
        base_url = os.getenv("BASE_APP_URL", "https://app.testomat.io/")
        api_token = os.getenv("TESTOMAT_API_TOKEN")
        if not api_token:
            raise ValueError("TESTOMAT_API_TOKEN is required")
        return cls(base_url=base_url, api_token=api_token)

    def _login(self, api_token: str) -> str:
        response = self._session.post(
            f"{self._base_url}/api/login",
            json={"api_token": api_token},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["jwt"]

    def get_projects(self) -> ProjectsResponse:
        response = self._session.get(f"{self._base_url}/api/projects", timeout=30)
        return ProjectsResponse.from_response(response)

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "ProjectsClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    @classmethod
    def unauthorized(cls, base_url: str) -> "ProjectsClient":
        instance = object.__new__(cls)
        instance._base_url = base_url.rstrip("/")
        instance._session = requests.Session()
        instance._session.headers.update({"Authorization": "invalid_token"})
        return instance


__all__ = [
    "ProjectsClient",
    "Project",
    "ProjectAttributes",
    "ProjectsResponse",
]
