from typing import Self

from playwright.sync_api import Page, expect

from src.web.components.test_for_suite_popup import TestForSuitePopup

from ..components import SideBar


class ProjectDetailPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)
        self.test_for_suite_popup = TestForSuitePopup(page)
        self.header = self.page.locator(".sticky-header")
        self.main_menu = self.page.locator(".mainnav-menu")
        self.filter_button = self.page.get_by_role("button").filter(
            has=self.page.locator(".md-icon-filter")
        )
        self.field_dropdown = self.page.locator(
            "li.filter-width", has=self.page.get_by_text("Field", exact=True)
        ).locator(".ember-power-select-trigger")
        self.apply_button = self.page.get_by_role("button", name="Apply")

    def expect_loaded(self) -> Self:
        expect(self.header).to_be_visible()
        expect(self.main_menu).to_be_visible()
        return self

    def open_by_id(self, project_id: int):
        self.page.goto(f"/projects/{project_id}")
        return self

    def expect_project_name(self, expected_name: str) -> Self:
        expect(self.page.locator(".sticky-header h2")).to_have_text(expected_name)
        return self

    def close_read_me(self) -> Self:
        self.page.locator(".back .third-btn").click()
        return self

    def create_test_via_popup(self) -> Self:
        self.page.locator(".sticky-header").get_by_role("button", name="Test", exact=True).click()
        return self

    def create_suite_via_popup(self) -> Self:
        self.page.get_by_role("button", name="Suite", exact=True).click()
        return self

    def has_first_suite_placeholder(self) -> bool:
        return self.page.locator("[placeholder='First Suite']").is_visible()

    def create_first_suite(self, suite_name: str) -> Self:
        self.page.locator("[placeholder='First Suite']").fill(suite_name)
        self.page.keyboard.press("Enter")
        return self

    def create_test_suite_via_popup(self):
        self.page.locator(".md-icon-chevron-down").click()
        self.page.get_by_text("Collection of test cases").click()

    def suite_with_name_is_visible(self, test_suite_name: str):
        expect(
            self.page.locator(".nested-item-row-suite").get_by_text(test_suite_name)
        ).to_be_visible()

    def open_filter(self):
        self.filter_button.click()

    def select_field_label(self, label_name: str):
        self.field_dropdown.click()
        self.page.get_by_text(label_name, exact=True).click()

    def apply_filter(self):
        self.apply_button.click()

    def expect_test_visible_by_title(self, title: str):
        expect(self.page.get_by_role("link", name=title, exact=True)).to_be_visible()
