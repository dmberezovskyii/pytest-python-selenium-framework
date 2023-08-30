import os
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from src.utils.logger import Logger, LogLevel
from src.utils.properties import Properties
from src.utils.yaml_reader import YamlReader

log = Logger(log_lvl=LogLevel.INFO).get_instance()


def _init_driver_options():
    opts = webdriver.ChromeOptions()
    # ... (options setup)
    opts.add_argument("--headless")
    opts.add_argument("--max-window-size")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    log.info(f'Driver options {opts.arguments}')
    return opts


def _get_driver_path(driver_os="arm64"):
    # Adjust the path as needed
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    driver_path = os.path.join(project_dir, "resources", driver_os)
    return driver_path


class Driver(ABC):
    @abstractmethod
    def create_driver(self):
        pass

    @abstractmethod
    def get_desired_caps(self, browser):
        pass


class LocalDriver(Driver):
    def get_desired_caps(self, browser):
        pass

    def create_driver(self, environment=None):
        try:
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=_init_driver_options(),
            )
        except Exception as e:
            log.error(f"Run local driver: {e}")
            driver = webdriver.Chrome(
                executable_path=_get_driver_path(), options=_init_driver_options()
            )
        driver.maximize_window()
        driver.implicitly_wait(15)
        driver.get(Properties.get_base_url(environment))
        log.info(f'Local Chrome driver created with session: {driver}')
        return driver


class ChromeRemoteDriver(Driver):
    def create_driver(self, environment=None):
        caps = self.get_desired_caps()
        driver = webdriver.Remote(
            command_executor=RemoteConnection("your remote URL"),
            desired_capabilities={"LT:Options": caps})
        driver.maximize_window()
        log.info(f'Local Chrome driver created with session: {driver}')
        return driver

    def get_desired_caps(self, browser="chrome"):
        caps = YamlReader.read_caps(browser)
        return caps


class FirefoxDriver(Driver):
    def get_desired_caps(self, browser):
        pass

    def create_driver(self, environment=None):
        pass


class WebDriverFactory:
    @staticmethod
    def create_driver(driver_type="local", environment=None):
        if driver_type.lower() == "chrome":
            return ChromeRemoteDriver().create_driver(environment)
        elif driver_type.lower() == "firefox":
            return FirefoxDriver().create_driver(environment)
        elif driver_type.lower() == "local":
            return LocalDriver().create_driver(environment)
        else:
            raise ValueError(f"Unsupported driver type: {driver_type} or {environment}")
