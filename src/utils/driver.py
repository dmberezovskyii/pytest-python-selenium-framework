import os
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.remote_connection import RemoteConnection
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

from src.utils.driver_options import _init_driver_options
from src.utils.logger import Logger, LogLevel
from src.utils.properties import Properties
from src.utils.yaml_reader import YamlReader
from utils.error_handler import ErrorHandler, ErrorType

log = Logger(log_lvl=LogLevel.INFO).get_instance()


def _get_driver_path(driver_type=None):
    # Check if driver_type is provided
    if driver_type is None:
        raise ValueError("Driver type must be specified.")

    project_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    driver_path = os.path.join(project_dir,
                               "resources")

    # Check if the resources directory exists
    if not os.path.exists(driver_path):
        ErrorHandler.raise_error(ErrorType.ENV_ERROR,
                                 f"Resources directory not found at {driver_path}.",
                                 custom_message="Please ensure it exists.")

    # Check if any driver binaries exist in the resources directory
    driver_files = [f for f in os.listdir(driver_path) if
                    os.path.isfile(os.path.join(driver_path, f))]
    print(driver_files)
    if not driver_files:
        ErrorHandler.raise_error(ErrorType.EMPTY_URL_ERROR,
                                 "No WebDriver binaries found in the resources directory.")


def _configure_driver(driver, environment):
    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.get(Properties.get_base_url(environment))
    log.info(f"Local Chrome driver created with session: {driver}")


class Driver(ABC):
    @abstractmethod
    def create_driver(self, environment, dr_type):
        pass

    def get_desired_caps(self, browser="chrome"):
        caps = YamlReader.read_caps(browser)
        return caps


class LocalDriver(Driver):
    def create_driver(self, environment=None, dr_type=None):
        """ChromeDriverManager doesn't include latest versions of ChromeDriver,
        so we need to manually upload chrome driver from
        https://googlechromelabs.github.io/chrome-for-testing/#stable to use with
        Latest version of Chrome, so at first we try to use ChromeDriverManager
        to upload latest driver and if it fails, we try to use local driver stored
        in resources if you want to use drivermanager,
        use selenium version 4.11.0 and higher
        """
        try:
            driver_path = ChromeDriverManager(
                chrome_type=ChromeType.GOOGLE
            ).install()
            driver = webdriver.Chrome(
                service=ChromeService(executable_path=driver_path)
            )
        except Exception as e:
            log.error(f"Run local driver: {e}")
            driver = webdriver.Chrome(
                service=ChromeService(_get_driver_path(dr_type)),
                options=_init_driver_options(dr_type=dr_type),
            )
        _configure_driver(driver, environment)
        log.info(f"Local Chrome driver created with session: {driver}")
        return driver


class ChromeRemoteDriver(Driver):
    def create_driver(self, environment=None, dr_type=None):
        caps = self.get_desired_caps()
        driver = webdriver.Remote(
            command_executor=RemoteConnection("your remote URL"),
            desired_capabilities={"LT:Options": caps}, # noqa
        )
        log.info(f"Local Chrome driver created with session: {driver}")
        return driver


class FirefoxDriver(Driver):
    def create_driver(self, environment=None, dr_type=None):
        try:
            driver = webdriver.Firefox(options=_init_driver_options(dr_type))
        except Exception as e:
            driver = webdriver.Chrome(
                service=ChromeService(_get_driver_path(dr_type)),
                options=_init_driver_options(),
            )
            log.error(f"Run local firefox driver: {e}")
        _configure_driver(driver, environment)
        return driver
