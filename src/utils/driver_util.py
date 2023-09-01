import os
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.remote_connection import RemoteConnection

from src.utils.logger import Logger, LogLevel
from src.utils.properties import Properties
from src.utils.yaml_reader import YamlReader

log = Logger(log_lvl=LogLevel.INFO).get_instance()


# def _get_driver_type(dr_type=None):
#     os_arch_mapping = {
#         "arm64": "chrome_arm64",
#         "x86_64": "chrome_x86_64",
#         "ubuntu": "ubuntu",  # Add additional mappings as needed
#     }
#
#
#     default_driver_type = dr_type
#     os_arch = platform.machine()
#     os_name = platform.system().lower()
#
#     driver_type = os_arch_mapping.get(os_arch, default_driver_type)
#     if os_name in os_arch_mapping:
#         driver_type = os_arch_mapping[os_name]
#
#     return driver_type
#

def _get_driver_path(driver_type=None):
    # Adjust the path as needed
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    driver_path = os.path.join(project_dir, "resources", driver_type)
    return driver_path


def _configure_driver(driver, environment):
    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.get(Properties.get_base_url(environment))
    log.info(f'Local Chrome driver created with session: {driver}')


def _init_driver_options():
    opts = webdriver.ChromeOptions()
    # ... (options setup)
    opts.add_argument("--headless") # use headless with --no-sandbox
    opts.add_argument("--no-sandbox")
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-dev-shm-usage")
    log.info(f'Driver options {opts.arguments}')
    return opts


class Driver(ABC):
    @abstractmethod
    def create_driver(self, environment, dr_type):
        pass

    @abstractmethod
    def get_desired_caps(self, browser):
        pass


class LocalDriver(Driver):
    def get_desired_caps(self, browser):
        pass

    def create_driver(self, environment=None, dr_type=None):
        # ChromeDriverManager doesn't include latest versions of ChromeDriver, so we need to manually
        # upload chrome driver from https://googlechromelabs.github.io/chrome-for-testing/#stable to use with Latest
        # version of Chrome, so at first we try to use ChromeDriverManager to upload latest driver
        # and if it fails, we try to use local driver stored in resources
        # if you want to use drivermanager, use selenium version 4.11.0 and higher
        try:
            driver = webdriver.Chrome(options=_init_driver_options())
        except Exception as e:
            log.error(f"Run local driver: {e}")
            driver = webdriver.Chrome(
                service=ChromeService(_get_driver_path(dr_type)), options=_init_driver_options()
            )
        _configure_driver(driver, environment)
        log.info(f'Local Chrome driver created with session: {driver}')
        return driver


class ChromeRemoteDriver(Driver):
    def create_driver(self, environment=None, dr_type=None):
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

    def create_driver(self, environment=None, dr_type=None):
        pass


class WebDriverFactory:
    DRIVER_MAPPING = {
        "chrome": ChromeRemoteDriver,
        "firefox": FirefoxDriver,
        "local": LocalDriver
    }

    @staticmethod
    def create_driver(environment=None, driver_type="local"):
        driver_type = driver_type.lower()
        if driver_type in WebDriverFactory.DRIVER_MAPPING:
            driver_class = WebDriverFactory.DRIVER_MAPPING[driver_type]
            return driver_class().create_driver(environment, driver_type)
        else:
            raise ValueError(f"Unsupported driver type: {driver_type} or {environment}")
