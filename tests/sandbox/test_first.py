import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from src.config import Config

pytestmark = pytest.mark.sandbox

TARGET_PROJECT: str = "python auto tests"


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    page.goto(configs.login_url)
    login_user(page, configs.email, configs.password)


def test_login_with_invalid_credentials(page: Page, configs: Config):
    open_home_page(page, configs)

    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()

    invalid_password = Faker().password(length=10)

    login_user(page, configs.email, invalid_password)

    expect(
        page.locator("#content-desktop").get_by_text("Invalid Email or password.")
    ).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text(
        "Invalid Email or password."
    )


def test_search_project_in_company(page: Page, login):
    search_for_project(page, TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_visible()


def test_open_free_project(page: Page, login):
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    search_for_project(page, TARGET_PROJECT)
    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_hidden()
    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)


def test_create_new_project(page: Page, login):
    fake = Faker()
    random_title = f"Project {fake.word()}"

    page.locator("#content-desktop").get_by_role("link", name="Create", exact=False).click()
    page.locator("#project_title").fill(random_title)
    page.get_by_role("button", name="Create", exact=True).click()

    expect(page.get_by_text("Let's do some testing!")).to_be_visible(timeout=10000)


def test_delete_existing_project(page: Page, login, configs: Config):
    faker = Faker()
    project_to_delete = f"Deleted project {faker.word()}"

    page.locator("#content-desktop").get_by_role("link", name="Create", exact=False).click()
    page.locator("#project_title").fill(project_to_delete)
    page.get_by_role("button", name="Create", exact=True).click()
    expect(page.get_by_text("Let's do some testing!")).to_be_visible(timeout=10000)

    page.goto(configs.login_url)
    page.get_by_role("link", name="Manage", exact=False).click()

    page.on("dialog", lambda dialog: dialog.accept())

    project_row = page.locator("tr", has_text=project_to_delete)

    project_row.locator(".bi-three-dots").dispatch_event("click")
    delete_button = project_row.get_by_text("Delete", exact=True)
    delete_button.wait_for(state="visible", timeout=10000)
    delete_button.click()

    page.reload()

    expect(page.get_by_text(project_to_delete)).to_be_hidden(timeout=10000)


def search_for_project(page: Page, TARGET_PROJECT):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(TARGET_PROJECT)


def open_home_page(page: Page, configs: Config):
    page.goto(configs.base_url)


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign in").click()
