from playwright.sync_api import Page


class ManageProjectsPage:
    def __init__(self, page: Page):
        self.page = page

    def delete_existing_project(self, project_to_delete: str):
        project_row = self.page.locator("tr", has_text=project_to_delete)

        project_row.locator(".bi-three-dots").dispatch_event("click")

        delete_button = project_row.get_by_text("Delete", exact=True)
        delete_button.wait_for(state="visible", timeout=10000)
        delete_button.click()

    def click_manage_projects(self):
        self.page.get_by_role("link", name="Manage", exact=False).click()
