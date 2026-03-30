from typing import Self

from playwright.sync_api import Page, expect


class ProjectDetailPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = self.page.locator(".sticky-header")
        self.main_menu = self.page.locator(".mainnav-menu")
        self.filter_button = self.page.get_by_role("button").filter(has=self.page.locator(".md-icon-filter"))
        self.field_dropdown = self.page.locator("li.filter-width",
                                                has=self.page.get_by_text("Field", exact=True)).locator(
            ".ember-power-select-trigger")
        self.apply_button = self.page.get_by_role("button", name="Apply")

    def is_loaded(self) -> Self:
        expect(self.header).to_be_visible()
        expect(self.main_menu).to_be_visible()
        return self

    def empty_project_name_is(self, expected_name: str) -> Self:
        expect(self.page.locator(".sticky-header h2")).to_have_text(expected_name)
        return self

    def close_read_me(self) -> Self:
        self.page.locator(".back .third-btn").click()
        return self

    def open_filter(self):
        self.filter_button.click()

    def select_field_label(self, label_name: str):
        self.field_dropdown.click()
        self.page.get_by_text(label_name, exact=True).click()

    def apply_filter(self):
        self.apply_button.click()

    def test_visible_by_title(self, title: str):
        expect(self.page.get_by_role("link", name=title, exact=True)).to_be_visible()
