from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
TEST_RESULT_DIR = PROJECT_ROOT / "test_result"


def pytest_configure(config: pytest.Config) -> None:
    if config.option.htmlpath:
        config.option.htmlpath = str(TEST_RESULT_DIR / "report.html")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


pytest_plugins = [
    "tests.fixtures.config",
    "tests.fixtures.api",
    "tests.fixtures.playwright",
    "tests.fixtures.cookie_helper",
    "tests.fixtures.app",
]
