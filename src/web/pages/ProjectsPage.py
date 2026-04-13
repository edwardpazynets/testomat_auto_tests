from playwright.sync_api import Page, expect


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self):
        expect(self.page.locator("#content-desktop").get_by_role("link", name="Create")).to_be_visible()

    def search_project(self, TARGET_PROJECT: str):
        expect(self.page.get_by_role("searchbox", name='Search')).to_be_visible()
        self.page.locator("#content-desktop #search").fill(TARGET_PROJECT)

    def open_free_project(self):
        self.page.locator("#company_id").click()
        self.page.locator("#company_id").select_option("Free Projects")

    def should_have_project(self, project_name: str):
        expect(self.page.get_by_role("heading", name=project_name)).to_be_visible()

    def open_manage_projects(self):
        self.page.get_by_role("link", name="Manage", exact=False).click()
