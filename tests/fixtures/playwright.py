import pytest
from playwright.sync_api import Browser

BROWSER_LAUNCH_ARGS = {
    "headless": False,
    "slow_mo": 700,
    "timeout": 30000,
}


@pytest.fixture(scope="session")
def browser_instance(playwright) -> Browser:
    browser = playwright.chromium.launch(**BROWSER_LAUNCH_ARGS)
    yield browser
    browser.close()
