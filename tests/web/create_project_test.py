import pytest
from faker import Faker

from src.web.application import Application


@pytest.mark.web
@pytest.mark.smoke
def test_create_new_project(logged_app: Application):
    fake = Faker()
    random_project_title = f"Project {fake.company()}"

    (
        logged_app.create_project_page.open()
        .expect_loaded()
        .fill_project_title(random_project_title)
        .click_create_project()
    )

    (
        logged_app.project_detail_page.expect_loaded()
        .expect_project_name(random_project_title)
        .close_read_me()
    )

    (logged_app.project_detail_page.side_bar.expect_loaded().expect_section_active("Tests"))
