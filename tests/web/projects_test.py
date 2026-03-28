from faker import Faker
from playwright.sync_api import Page, expect

from src.web.pages.ProjectDetailPage import ProjectDetailPage
from src.web.pages.ProjectPage import ProjectPage

TARGET_PROJECT: str = "python auto tests"
LABEL_NAME: str = "Auto test"
TEST_TITLE: str = "auto"


def test_search_project_in_company(page: Page, logged_in):
    project_page = ProjectPage(page)

    project_page.is_loaded()
    project_page.search_project(TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_visible()


def test_create_new_project(page: Page, logged_in):
    project_page = ProjectPage(page)
    fake = Faker()
    random_title = f"Project {fake.word()}"
    project_page.is_loaded()
    project_page.create_new_project(random_title)

    expect(page.get_by_text("Let's do some testing!")).to_be_visible(timeout=10000)


def test_delete_existing_project(page: Page, configs, logged_in):
    project_page = ProjectPage(page)

    faker = Faker()
    project_to_delete = f"Deleted project {faker.word()}"

    project_page.is_loaded()
    project_page.create_new_project(project_to_delete)
    expect(page.get_by_text("Let's do some testing!")).to_be_visible(timeout=10000)

    page.goto(configs.login_url)
    project_page.open_manage_projects()

    page.on("dialog", lambda dialog: dialog.accept())
    project_page.delete_existing_project(project_to_delete)

    page.reload()
    expect(page.get_by_text(project_to_delete)).to_be_hidden(timeout=10000)


# created by claude
def test_filter_by_label(page: Page, configs, logged_in):
    project_page = ProjectPage(page)
    detail_page = ProjectDetailPage(page)

    project_page.is_loaded()
    project_page.search_project(TARGET_PROJECT)
    page.get_by_role("heading", name=TARGET_PROJECT).click()

    detail_page.is_loaded()
    detail_page.open_filter()
    detail_page.select_field_label(LABEL_NAME)
    detail_page.apply_filter()
    detail_page.test_visible_by_title(TEST_TITLE)
