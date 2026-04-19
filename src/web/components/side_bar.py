import re

from playwright.sync_api import Page, expect


class SideBar:
    def __init__(self, page: Page):
        self.page = page
        self.menu = self.page.locator(".mainnav-menu")

        self.logo = self.page.locator(".btn-open.opacity-100")
        self.close_button = self.page.get_by_role("button", name="Close")

        self.tests = self.menu.locator("a.nav-item:has-text('Tests')")
        self.requirements = self.page.get_by_role("link", name="Requirements")
        self.runs = self.page.get_by_role("link", name="Runs")
        self.plans = self.page.get_by_role("link", name="Plans")
        self.steps = self.page.get_by_role("link", name="Steps")
        self.pulse = self.page.get_by_role("link", name="Pulse")
        self.imports = self.page.get_by_role("link", name="Imports")
        self.analytics = self.page.get_by_role("link", name="Analytics")
        self.branches = self.page.get_by_role("link", name="Branches")
        self.settings = self.page.get_by_role("link", name="Settings")

        self.help = self.page.get_by_role("link", name="Help")
        self.projects = self.page.get_by_role("link", name="Projects")
        self.profile = self.page.get_by_role("link", name="Profile")

    def expect_loaded(self):
        expect(self.logo).to_be_visible()
        expect(self.menu).to_be_visible()
        expect(self.tests).to_be_visible()
        expect(self.projects).to_be_visible()
        return self

    # def navigate_to(self, section: str):
    #     self.page.get_by_role("link", name=section).click()

    def expect_section_active(self, section: str):
        link = self.menu.locator(f"a.nav-item:has-text('{section}')")
        expect(link).to_have_class(re.compile("active"))
