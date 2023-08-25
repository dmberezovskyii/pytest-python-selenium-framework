import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

desired_caps = {"platform": "Windows 10", "browserName": "chrome", "version": "73"}


def get_driver_path(driver_name="chromedriver"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(script_dir, "resources")
    driver_path = os.path.join(resources_dir, driver_name)
    return driver_path


def create_driver():
    opts = webdriver.ChromeOptions()
    # ... (options setup)
    # opts.add_argument("--headless")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")

    try:
        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), options=opts
        )
    except Exception as e:
        print(f"Failed to install ChromeDriver: {e}")
        driver = webdriver.Chrome(executable_path=get_driver_path(), options=opts)
    driver.maximize_window()
    return driver


def quit_driver(driver):
    if driver is not None:
        driver.quit()


@pytest.fixture(scope="session", autouse=True)
def make_driver(request) -> webdriver.Remote:
    driver = None

    def _make_driver() -> webdriver.Remote:
        nonlocal driver
        driver = (
            create_driver()
        )  # Use the utility function to create the driver instance
        return driver

    yield _make_driver()
    quit_driver(driver)  # Use the utility function to quit the driver
