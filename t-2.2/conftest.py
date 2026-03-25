import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://cerulean-praline-8e5aa6.netlify.app/"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    yield driver
    driver.quit()


def pytest_terminal_summary(terminalreporter):
    failed = terminalreporter.stats.get("failed", [])
    if not failed:
        return

    terminalreporter.write_sep("=", "BUG SUMMARY")
    for report in failed:
        terminalreporter.write_line(f"BUG: {report.nodeid}")