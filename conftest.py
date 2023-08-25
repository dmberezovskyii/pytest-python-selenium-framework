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


@pytest.fixture(scope="session", autouse=True)
def make_driver() -> webdriver.Remote:
    driver = None

    def _make_driver() -> webdriver.Remote:
        nonlocal driver
        opts = webdriver.ChromeOptions()
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

        return driver

    yield _make_driver

    if driver is not None:
        driver.quit()


def test_example(make_driver):
    driver = make_driver()
    driver.get("https://softjourn.com")
