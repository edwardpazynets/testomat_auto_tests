import json
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from src.web.application import Application
from tests.fixtures.browser import build_browser_context
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import clear_browser_state

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEST_RESULT_DIR = PROJECT_ROOT / "test_result"
AUTH_DIR = TEST_RESULT_DIR / "auth"
FREE_AUTH_DIR = TEST_RESULT_DIR / "auth"

STORAGE_STATE_PATH = AUTH_DIR / "storage_state.json"
FREE_PROJECT_STORAGE_PATH = FREE_AUTH_DIR / "free_storage_state.json"
VIDEOS_DIR = PROJECT_ROOT / "videos"
TRACES_DIR = TEST_RESULT_DIR / "traces"


def get_or_create_context(
    browser: Browser,
    base_url: str,
    storage_state_path: Path | None = None,
) -> tuple[BrowserContext, bool]:
    has_state = storage_state_path is not None and storage_state_path.exists()

    kwargs = {
        "base_url": base_url,
        "viewport": {"width": 1320, "height": 980},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": str(VIDEOS_DIR),
        "permissions": ["geolocation"],
    }
    if has_state:
        kwargs["storage_state"] = str(storage_state_path)

    context = browser.new_context(**kwargs)
    return context, not has_state


def save_storage_state(context: BrowserContext, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=path)


def start_tracing(page: Page) -> None:
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)


def stop_tracing_on_failure(
    page: Page, request: pytest.FixtureRequest, traces_dir: Path = TRACES_DIR
) -> None:
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        trace_path = traces_dir / f"{request.node.name}.zip"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        page.context.tracing.stop(path=trace_path)
    else:
        page.context.tracing.stop()


def create_free_project_state() -> None:
    if not STORAGE_STATE_PATH.exists():
        return

    state = json.loads(STORAGE_STATE_PATH.read_text())
    for cookie in state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ""
            break

    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FREE_PROJECT_STORAGE_PATH.write_text(json.dumps(state, indent=2))


def open_login_and_authorize(config: Config, page: Page) -> Application:
    app = Application(page, config.base_url)
    app.login_page.open()
    app.login_page.expect_loaded()
    app.login_page.login_as(config.email, config.password)
    app.projects_page.expect_loaded()
    return app


@pytest.fixture(scope="session")
def shared_context(browser_instance: Browser, config: Config) -> BrowserContext:
    context = build_browser_context(browser_instance, config.app_base_url)
    context.new_page()
    yield context
    context.close()


@pytest.fixture(scope="function")
def shared_app(shared_context: BrowserContext, config: Config) -> Application:
    page = shared_context.pages[0]
    clear_browser_state(page)
    yield Application(page, config.base_url)
    clear_browser_state(page)


@pytest.fixture(scope="function")
def app(shared_app: Application) -> Application:
    return shared_app


@pytest.fixture(scope="session")
def logged_page(browser_instance: Browser, config: Config) -> Page:
    context, needs_login = get_or_create_context(
        browser_instance,
        config.app_base_url,
        STORAGE_STATE_PATH,
    )
    page = context.new_page()

    if needs_login:
        open_login_and_authorize(config, page)
        save_storage_state(context, STORAGE_STATE_PATH)
        create_free_project_state()

    page.goto("/projects/")
    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_page: Page, config: Config, request: pytest.FixtureRequest) -> Application:
    start_tracing(logged_page)
    logged_page.goto("/projects/")
    original_company = logged_page.locator("#company_id").locator("option:checked").inner_text()
    try:
        yield Application(logged_page, config.base_url)
    finally:
        try:
            logged_page.goto("/projects/")
            logged_page.locator("#company_id").select_option(label=original_company)
        finally:
            stop_tracing_on_failure(logged_page, request)


@pytest.fixture(scope="function")
def logged_context(logged_page: Page) -> BrowserContext:
    return logged_page.context


@pytest.fixture(scope="session")
def free_project_page(browser_instance: Browser, config: Config) -> Page:
    context, needs_login = get_or_create_context(
        browser_instance,
        config.app_base_url,
        FREE_PROJECT_STORAGE_PATH,
    )
    page = context.new_page()

    if needs_login:
        app = open_login_and_authorize(config, page)
        app.projects_page.header.select_company("Free Projects")
        expect(app.projects_page.header.free_plan_label).to_be_visible()
        save_storage_state(context, FREE_PROJECT_STORAGE_PATH)

    page.goto("/projects/")
    yield page
    context.close()


@pytest.fixture(scope="function")
def free_project_app(
    free_project_page: Page, config: Config, request: pytest.FixtureRequest
) -> Application:
    start_tracing(free_project_page)
    free_project_page.goto("/projects/")
    try:
        yield Application(free_project_page, config.base_url)
    finally:
        stop_tracing_on_failure(free_project_page, request)


@pytest.fixture(scope="session")
def free_project_context(free_project_page: Page) -> Page:
    return free_project_page
