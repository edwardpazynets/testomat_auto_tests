from playwright.sync_api import Page

from src.web.pages import (
    CreateNewProjectPage,
    HomePage,
    LoginPage,
    ManageProjectsPage,
    ProjectDetailPage,
    ProjectsPage,
)


class Application:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.home_page = HomePage(page, base_url)
        self.login_page = LoginPage(page)
        self.projects_page = ProjectsPage(page)
        self.project_detail_page = ProjectDetailPage(page)
        self.create_project_page = CreateNewProjectPage(page)
        self.manage_page = ManageProjectsPage(page)
