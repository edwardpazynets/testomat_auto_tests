from playwright.sync_api import Page

from web.Application import Application

TARGET_PROJECT: str = "python auto tests"
LABEL_NAME: str = "Auto test"
TEST_TITLE: str = "auto"


# created by claude
def test_filter_by_label(page: Page, configs, logged_in, app: Application):
    app.projects_page.is_loaded()
    app.projects_page.search_project(TARGET_PROJECT)
    app.projects_page.page.get_by_role("heading", name=TARGET_PROJECT).click()

    app.project_detail_page.is_loaded()
    app.project_detail_page.open_filter()
    app.project_detail_page.select_field_label(LABEL_NAME)
    app.project_detail_page.apply_filter()
    app.project_detail_page.test_visible_by_title(TEST_TITLE)
