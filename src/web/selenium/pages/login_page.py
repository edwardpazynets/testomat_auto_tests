from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.core.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = (By.CSS_SELECTOR, "#content-desktop #user_email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#content-desktop #user_password")
    REMEMBER_ME_CHECKBOX = (By.CSS_SELECTOR, "#user_remember_me")
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, "#content-desktop [value='Sign In']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#content-desktop .common-flash-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "#content-desktop .common-flash-alert")
    INVALID_LOGIN_TEXT = "Invalid email or password."

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def open(self, base_url: str = "") -> Self:
        self.driver.get(f"{base_url}/users/sign_in")
        return self

    def is_loaded(self) -> Self:
        self.wait.for_visible(self.EMAIL_INPUT)
        self.wait.for_visible(self.PASSWORD_INPUT)
        return self

    def login(self, email: str, password: str, remember_me: bool = False) -> Self:
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        if remember_me and not self.find(self.REMEMBER_ME_CHECKBOX).is_selected():
            self.click(self.REMEMBER_ME_CHECKBOX)
        self.click(self.SIGN_IN_BUTTON)
        return self

    def should_see_success_message(self) -> Self:
        self.wait.for_visible(self.SUCCESS_MESSAGE)
        return self

    def should_see_invalid_login_error(self) -> Self:
        self.wait.for_text_present((By.TAG_NAME, "body"), self.INVALID_LOGIN_TEXT)
        return self
