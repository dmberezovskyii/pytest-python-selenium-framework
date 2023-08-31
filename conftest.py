import pytest
from dotenv import load_dotenv
from selenium import webdriver

from src.utils.driver_util import WebDriverFactory
from src.utils.logger import Logger, LogLevel

log = Logger(log_lvl=LogLevel.INFO).get_instance()


@pytest.fixture(scope="function", autouse=True)
def quit_driver(request, make_driver):
    yield
    if make_driver is not None:
        make_driver.quit()


@pytest.fixture(scope="function")
def make_driver(request) -> webdriver.Remote:
    load_dotenv(dotenv_path=f"{request.config.getoption('--env')}")
    env = request.config.getoption('--env')
    dr_type = request.config.getoption('--type')
    driver = None

    def _make_driver() -> webdriver.Remote:
        nonlocal driver
        driver = WebDriverFactory().create_driver(environment=env, driver_type=dr_type)
        return driver

    yield _make_driver()


# Rest of your code...

def pytest_addoption(parser):
    parser.addoption("--browser-version", action="store", default="116", help="Specify the browser version")
    parser.addoption("--env", action="store", default='stage', help="Run browser in headless mode")
    parser.addoption("--type", action="store", default='local', help="Run browser in os type")
