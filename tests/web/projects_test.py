from faker import Faker
from playwright.sync_api import Page, expect

from src.web.pages.CreateNewProjectPage import CreateNewProjectPage
from src.web.pages.ManageProjects import ManageProjectsPage
from src.web.pages.ProjectsPage import ProjectsPage

TARGET_PROJECT: str = "python auto tests"


def test_search_project_in_company(page: Page, logged_in):
    project_page = ProjectsPage(page)

    project_page.is_loaded()
    project_page.search_project(TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_visible()


def test_delete_existing_project(page: Page, configs, logged_in):
    projects_page = ProjectsPage(page)
    create_project = CreateNewProjectPage(page)
    delete_project = ManageProjectsPage(page)

    faker = Faker()
    project_to_delete = f"Deleted project {faker.word()}"

    projects_page.is_loaded()

    create_project.open()
    create_project.is_loaded()
    create_project.create_new_project(project_to_delete)
    create_project.click_create()

    expect(page.get_by_text("Let's do some testing!")).to_be_visible(timeout=10000)

    page.goto(configs.login_url)
    delete_project.open_manage_projects()

    page.on("dialog", lambda dialog: dialog.accept())
    delete_project.delete_existing_project(project_to_delete)

    page.reload()
    expect(page.get_by_text(project_to_delete)).to_be_hidden(timeout=10000)
