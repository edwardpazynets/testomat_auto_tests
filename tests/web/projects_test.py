import pytest
from faker import Faker
from playwright.sync_api import expect

from src.web.Application import Application


@pytest.mark.web
@pytest.mark.smoke
def test_search_project_in_company(logged_app: Application, target_project):
    logged_app.projects_page.is_loaded()
    logged_app.projects_page.search_project(target_project)
    logged_app.projects_page.should_have_project(target_project)


@pytest.mark.web
@pytest.mark.smoke
def test_delete_existing_project(logged_app: Application, configs):
    faker = Faker()
    project_to_delete = f"Deleted project {faker.word()}"
    page = logged_app.page

    logged_app.projects_page.is_loaded()

    logged_app.create_project_page.open()
    logged_app.create_project_page.is_loaded()
    logged_app.create_project_page.create_new_project(project_to_delete)
    logged_app.create_project_page.click_create()

    expect(page.get_by_text("Let's do some testing!")).to_be_visible(timeout=10000)

    page.goto(configs.login_url)
    logged_app.manage_page.open_manage_projects()

    page.on("dialog", lambda dialog: dialog.accept())
    logged_app.manage_page.delete_existing_project(project_to_delete)

    page.reload()
    expect(page.get_by_text(project_to_delete)).to_be_hidden(timeout=10000)
