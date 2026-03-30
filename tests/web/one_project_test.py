from playwright.sync_api import Page

from src.web.pages.ProjectDetailPage import ProjectDetailPage
from src.web.pages.ProjectsPage import ProjectsPage

TARGET_PROJECT: str = "python auto tests"
LABEL_NAME: str = "Auto test"
TEST_TITLE: str = "auto"


# created by claude
def test_filter_by_label(page: Page, configs, logged_in):
    projects_page = ProjectsPage(page)
    detail_page = ProjectDetailPage(page)

    projects_page.is_loaded()
    projects_page.search_project(TARGET_PROJECT)
    page.get_by_role("heading", name=TARGET_PROJECT).click()

    detail_page.is_loaded()
    detail_page.open_filter()
    detail_page.select_field_label(LABEL_NAME)
    detail_page.apply_filter()
    detail_page.test_visible_by_title(TEST_TITLE)
