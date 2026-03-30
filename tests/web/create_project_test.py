from faker import Faker
from playwright.sync_api import Page

from src.web.pages.CreateNewProjectPage import CreateNewProjectPage
from src.web.pages.ProjectDetailPage import ProjectDetailPage


def test_create_new_project(page: Page, logged_in):
    fake = Faker()
    random_project_title = f"Project {fake.company()}"

    (CreateNewProjectPage(page)
     .open()
     .is_loaded()
     .create_new_project(random_project_title)
     .click_create())

    (ProjectDetailPage(page)
     .is_loaded().
     empty_project_name_is(random_project_title)
     .close_read_me())
