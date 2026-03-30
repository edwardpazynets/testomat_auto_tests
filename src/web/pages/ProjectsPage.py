from playwright.sync_api import Page, expect


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self):
        expect(self.page.locator("#content-desktop").get_by_role("link", name="Create")).to_be_visible()
        expect(self.page.locator(".common-flash-success", has_text="Signed in successfully")).to_be_visible()

    def search_project(self, TARGET_PROJECT: str):
        expect(self.page.get_by_role("searchbox", name='Search')).to_be_visible()
        self.page.locator("#content-desktop #search").fill(TARGET_PROJECT)

    def open_free_project(self):
        self.page.locator("#company_id").click()
        self.page.locator("#company_id").select_option("Free Projects")

    # доробити деліт в окремій пейджі
    def delete_existing_project(self, project_to_delete: str):
        project_row = self.page.locator("tr", has_text=project_to_delete)

        project_row.locator(".bi-three-dots").dispatch_event("click")

        delete_button = project_row.get_by_text("Delete", exact=True)
        delete_button.wait_for(state="visible", timeout=10000)
        delete_button.click()

    def open_manage_projects(self):
        self.page.get_by_role("link", name="Manage", exact=False).click()
