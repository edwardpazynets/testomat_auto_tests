from faker import Faker

from web.Application import Application


def test_create_new_project(logged_in, app: Application):
    fake = Faker()
    random_project_title = f"Project {fake.company()}"

    (app.create_project_page
     .open()
     .is_loaded()
     .create_new_project(random_project_title)
     .click_create())

    (app.project_detail_page
     .is_loaded()
     .empty_project_name_is(random_project_title)
     .close_read_me())

    (app.project_detail_page.side_bar
     .is_loaded()
     .is_active("Tests"))
