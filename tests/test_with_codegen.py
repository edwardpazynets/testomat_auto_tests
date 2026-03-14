import re
from playwright.sync_api import Page, expect


def test_login_example(page: Page) -> None:
    page.goto("https://testomat.io/")

    page.get_by_role("link", name="Log in").click()
    page.get_by_role("textbox", name="name@email.com").fill("edwardpazynets@gmail.com")

    page.locator("#content-desktop").locator("#user_password").fill("Qwerty77")

    page.locator("#content-desktop").get_by_role("checkbox").check()
    page.get_by_role("button", name="Sign In").click()

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()

#codegen version
# def test_example(page: Page) -> None:
#     page.goto("https://testomat.io/")
#     expect(page.get_by_role("link", name="AI orchestration AI")).to_be_visible()
#
#     page.get_by_role("link", name="Log in").click()
#     expect(page.get_by_role("heading", name="Test Management System for")).to_be_visible()
#
#     page.get_by_role("textbox", name="name@email.com").click()
#     page.get_by_role("textbox", name="name@email.com").fill("edwardpazynets@gmail.com")
#     page.get_by_role("textbox", name="name@email.com").press("Tab")
#     page.get_by_role("textbox", name="********").fill("Qwerty77")
#     page.get_by_role("checkbox").check()
#     page.get_by_role("button", name="Sign In").click()
#     expect(page.get_by_role("heading", name="Test Management System for")).to_be_visible()
#
#     page.locator("#content-desktop").get_by_text("Invalid Email or password.").click()
