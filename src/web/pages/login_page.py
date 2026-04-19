from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("/users/sign_in")

    def expect_loaded(self):
        expect(self.page.locator("#content-desktop form#new_user")).to_be_visible()

    def login_as(self, email: str, password: str):
        self.page.locator("#content-desktop #user_email").fill(email)
        self.page.locator("#content-desktop #user_password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()

    def expect_invalid_login_message(self):
        expect(
            self.page.locator("#content-desktop").get_by_text("Invalid Email or password.")
        ).to_be_visible()

    def expect_login_success_message(self):
        expect(
            self.page.locator(".common-flash-success", has_text="Signed in successfully")
        ).to_be_visible()
