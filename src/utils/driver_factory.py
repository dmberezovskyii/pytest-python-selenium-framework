from src.utils.driver import ChromeRemoteDriver, FirefoxDriver, LocalDriver


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
