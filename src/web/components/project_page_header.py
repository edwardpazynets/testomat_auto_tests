from playwright.sync_api import Page, expect


class ProjectsPageHeader:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.locator(".common-page-header")
        self.title = self.header.locator("h2")
        self.enterprise_plan_label = self.header.locator(".tooltip-project-plan")
        self.free_plan_label = self.header.locator(".tooltip-project-plan")
        self.company_select = self.header.locator("#company_id")
        self.plan = self.header.locator(".tooltip-project-plan span")
        self.search_input = self.header.locator("input#search")
        self.create_button = self.header.locator("a.common-btn-primary")
        self.grid_view_button = self.header.locator("#grid-view")
        self.table_view_button = self.header.locator("#table-view")

    def should_be_loaded(self):
        expect(self.header).to_be_visible(timeout=15000)
        expect(self.title).to_have_text("Projects")

    def get_title(self) -> str:
        return self.title.inner_text()

    def get_selected_company(self) -> str:
        return self.company_select.locator("option:checked").inner_text()

    def select_company(self, name: str):
        self.company_select.select_option(label=name)

    def get_plan(self) -> str:
        return self.plan.inner_text().strip()

    def search(self, text: str):
        self.search_input.fill(text)

    def clear_search(self):
        self.search_input.fill("")

    def click_create(self):
        self.create_button.click()

    def switch_to_grid_view(self):
        self.grid_view_button.click()

    def switch_to_table_view(self):
        self.table_view_button.click()

    def should_have_plan(self, plan_name: str):
        expect(self.plan).to_have_text(plan_name)
