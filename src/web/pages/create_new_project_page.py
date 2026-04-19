from typing import Self

from playwright.sync_api import Page, expect


class CreateNewProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.__form_container = page.locator("#content-desktop [action='/projects']")

    def open(self) -> Self:
        self.page.goto("/projects/new")
        return self

    def expect_loaded(self) -> Self:
        expect(self.__form_container).to_be_visible()
        expect(self.__form_container.locator("#classical")).to_be_visible()
        expect(self.__form_container.locator("#classical")).to_contain_text("Classical")
        expect(self.__form_container.locator("#bdd")).to_be_visible()
        expect(self.__form_container.locator("#bdd")).to_contain_text("BDD")
        expect(self.__form_container.locator("#project_title")).to_be_visible()
        expect(self.__form_container.locator("#demo-btn")).to_be_visible()
        expect(self.__form_container.locator("#project-create-btn")).to_be_visible()
        expect(self.page.get_by_text("How to start?")).to_be_visible()
        expect(self.page.get_by_text("New Project")).to_be_visible()
        return self

    def fill_project_title(self, project_title: str) -> Self:
        self.__form_container.locator("#project_title").fill(project_title)
        return self

    def click_create_project(self) -> Self:
        self.__form_container.locator("#project-create-btn input").click()
        expect(self.__form_container.locator("#project-create-btn input")).to_be_hidden(
            timeout=10000
        )
        self.page.wait_for_url("**/projects/**", timeout=10000)
        return self
