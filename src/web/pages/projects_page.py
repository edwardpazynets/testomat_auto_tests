from playwright.sync_api import Page, expect


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page

    def expect_loaded(self):
        expect(
            self.page.locator("#content-desktop").get_by_role("link", name="Create", exact=True)
        ).to_be_visible()

    def search_project(self, target_project: str):
        expect(self.page.get_by_role("searchbox", name="Search")).to_be_visible()
        self.page.locator("#content-desktop #search").fill(target_project)

    def open_free_project(self):
        self.page.locator("#company_id").click()
        self.page.locator("#company_id").select_option("Free Projects")

    def expect_project_visible(self, project_name: str):
        expect(self.page.get_by_role("heading", name=project_name)).to_be_visible()

    def click_manage_projects(self):
        self.page.get_by_role("link", name="Manage", exact=False).click()
