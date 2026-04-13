import pytest
from faker import Faker

from src.web.Application import Application


@pytest.mark.web
@pytest.mark.smoke
def test_create_new_project(logged_app: Application):
    fake = Faker()
    random_project_title = f"Project {fake.company()}"

    (logged_app.create_project_page
     .open()
     .is_loaded()
     .create_new_project(random_project_title)
     .click_create())

    (logged_app.project_detail_page
     .is_loaded()
     .empty_project_name_is(random_project_title)
     .close_read_me())

    (logged_app.project_detail_page.side_bar
     .is_loaded()
     .is_active("Tests"))
