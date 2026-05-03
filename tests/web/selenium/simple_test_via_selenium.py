import pytest
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.web.selenium.pages.login_page import LoginPage
from src.web.selenium.pages.login_page_v2 import LoginPageV2
from tests.fixtures.config import Config


@pytest.mark.web
def test_selenium_login_and_search(driver: WebDriver, config: Config):
    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException],
    )

    driver.get(config.app_base_url)
    driver.find_element(By.CSS_SELECTOR, value="#content-desktop #user_email").send_keys(
        config.email
    )
    driver.find_element(By.CSS_SELECTOR, value="#content-desktop #user_password").send_keys(
        config.password
    )
    driver.find_element(By.CSS_SELECTOR, value="#content-desktop [value='Sign In']").click()
    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#content-desktop .common-flash-success")
        )
    )

    target_project = "python auto tests"
    driver.find_element(By.CSS_SELECTOR, value="#content-desktop #search").send_keys(target_project)
    driver.find_element(
        By.CSS_SELECTOR, value=f"#content-desktop [title='{target_project}']"
    ).click()
    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, f".breadcrumbs-page [title='{target_project}']")
        )
    )


@pytest.mark.web
def test_login_with_page_object_v1(driver: WebDriver, configs: Config):
    login_page = LoginPage(driver)
    login_page.open(configs.app_base_url)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    login_page.should_see_success_message()


@pytest.mark.web
def test_login_with_page_object_v2(driver: WebDriver, configs: Config):
    login_page = LoginPageV2(driver)
    login_page.open(configs.app_base_url)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    login_page.should_see_success_message()


@pytest.mark.web
def test_login_with_invalid_password_v2(driver: WebDriver, configs: Config):
    login_page = LoginPageV2(driver)
    login_page.open(configs.app_base_url)
    login_page.is_loaded()
    login_page.login(configs.email, "invalid-password")
    login_page.should_see_invalid_login_error()


@pytest.mark.web
def test_login_with_invalid_password_v1(driver: WebDriver, configs: Config):
    login_page = LoginPage(driver)
    login_page.open(configs.app_base_url)
    login_page.is_loaded()
    login_page.login(configs.email, "invalid-password")
    login_page.should_see_invalid_login_error()
