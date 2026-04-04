from faker import Faker
from playwright.sync_api import Page, expect

from src.web.Application import Application


def test_search_project_in_company(logged_in, app: Application, target_project):
    app.projects_page.is_loaded()
    app.projects_page.search_project(target_project)
    app.projects_page.should_have_project(target_project)


def test_delete_existing_project(page: Page, configs, logged_in, app: Application):
    faker = Faker()
    project_to_delete = f"Deleted project {faker.word()}"

    app.projects_page.is_loaded()

    app.create_project_page.open()
    app.create_project_page.is_loaded()
    app.create_project_page.create_new_project(project_to_delete)
    app.create_project_page.click_create()

    expect(page.get_by_text("Let's do some testing!")).to_be_visible(timeout=10000)

    page.goto(configs.login_url)
    app.manage_page.open_manage_projects()

    page.on("dialog", lambda dialog: dialog.accept())
    app.manage_page.delete_existing_project(project_to_delete)

    page.reload()
    expect(page.get_by_text(project_to_delete)).to_be_hidden(timeout=10000)
