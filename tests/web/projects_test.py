from faker import Faker
from playwright.sync_api import Page, expect

from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.ProjectPage import ProjectPage

TARGET_PROJECT: str = "python auto tests"


def test_search_project_in_company(page: Page, configs):
    project_page = ProjectPage(page)
    login_page = LoginPage(page)
    home_page = HomePage(page)

    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page.is_loaded()
    login_page.login(configs.email, configs.password)

    project_page.is_loaded()
    project_page.search_project(TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_visible()


def test_create_new_project(page: Page, configs):
    project_page = ProjectPage(page)
    login_page = LoginPage(page)
    home_page = HomePage(page)
    fake = Faker()
    random_title = f"Project {fake.word()}"

    home_page.open()
    home_page.click_login()

    login_page.is_loaded()
    login_page.login(configs.email, configs.password)

    project_page.is_loaded()
    project_page.create_new_project(random_title)

    expect(page.get_by_text("Let's do some testing!")).to_be_visible(timeout=10000)


def test_delete_existing_project(page: Page, configs):
    project_page = ProjectPage(page)
    login_page = LoginPage(page)
    home_page = HomePage(page)
    faker = Faker()
    project_to_delete = f"Deleted project {faker.word()}"

    home_page.open()
    home_page.click_login()

    login_page.is_loaded()
    login_page.login(configs.email, configs.password)

    project_page.is_loaded()
    project_page.create_new_project(project_to_delete)
    expect(page.get_by_text("Let's do some testing!")).to_be_visible(timeout=10000)

    page.goto(configs.login_url)
    project_page.open_manage_projects()

    page.on("dialog", lambda dialog: dialog.accept())
    project_page.delete_existing_project(project_to_delete)

    page.reload()
    expect(page.get_by_text(project_to_delete)).to_be_hidden(timeout=10000)
