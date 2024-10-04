from driver.driver import ChromeRemoteDriver, FirefoxDriver, LocalDriver
from src.utils.error_handler import ErrorHandler, ErrorType


class WebDriverFactory:
    DRIVER_MAPPING = {
        "chrome": ChromeRemoteDriver,
        "firefox": FirefoxDriver,
        "local": LocalDriver,
    }

    @staticmethod
    def create_driver(environment=None, driver_type="local"):
        driver_type = driver_type.lower()
        if driver_type in WebDriverFactory.DRIVER_MAPPING:
            driver_class = WebDriverFactory.DRIVER_MAPPING[driver_type]
            return driver_class().create_driver(environment, driver_type)
        else:
            raise ErrorHandler.raise_error(
                ErrorType.ENV_ERROR, environment, driver_type
            )
