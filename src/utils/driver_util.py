import os
from abc import ABC, abstractmethod

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from utils.logger import Logger, LogLevel

log = Logger(log_lvl=LogLevel.INFO).get_instance()


class Driver(ABC):
    @abstractmethod
    def create_driver(self):
        pass


class LocalDriver(Driver):
    def create_driver(self):
        try:
            driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(),
                options=init_driver_options(),
            )
        except Exception as e:
            log.error(f"Failed to install ChromeDriver: {e}")
            driver = webdriver.Chrome(
                executable_path=get_driver_path(), options=init_driver_options()
            )
        driver.maximize_window()
        log.info(f'Local Chrome driver created with session: {driver}')
        return driver


class ChromeDriver(Driver):

    def create_driver(self):
        pass


class RemoteDriver(Driver):

    def create_driver(self):
        pass


class FirefoxDriver(Driver):
    def create_driver(self):
        pass


def init_driver_options():
    opts = webdriver.ChromeOptions()
    # ... (options setup)
    # opts.add_argument("--headless")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    log.info(f'Driver options {opts.arguments}')
    return opts


def get_driver_path(driver_name="chromedriver"):
    # Adjust the path as needed
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    driver_path = os.path.join(project_dir, "resources", driver_name)
    return driver_path


class WebDriverFactory:
    @staticmethod
    def create_driver(driver_type="chrome"):
        if driver_type.lower() == "chrome":
            return ChromeDriver().create_driver()
        elif driver_type.lower() == "firefox":
            return FirefoxDriver().create_driver()
        elif driver_type.lower() == "remote":
            return RemoteDriver().create_driver()
        elif driver_type.lower() == "local":
            return LocalDriver().create_driver()
        else:
            raise ValueError(f"Unsupported driver type: {driver_type}")
