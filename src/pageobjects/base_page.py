from enum import Enum
from typing import Tuple

from appium.webdriver import WebElement
from selenium.common import ElementNotVisibleException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

Locator = Tuple[By, str]


class WaitType(Enum):
    DEFAULT = 20
    SHORT = 5
    LONG = 60
    FLUENT = 10


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(driver, WaitType.DEFAULT.value)
        self._short_wait = WebDriverWait(driver, WaitType.SHORT.value)
        self._long_wait = WebDriverWait(driver, WaitType.LONG.value)
        self._fluent_wait = WebDriverWait(driver, WaitType.FLUENT.value, poll_frequency=1,
                                          ignored_exceptions=[ElementNotVisibleException])

    def wait(self, locator: Locator, waiter: WebDriverWait = None) -> WebElement:
        if waiter is None:
            waiter = self._wait
        try:
            return waiter.until(ec.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not found after {waiter._timeout} seconds")

    def find(self, locator: Locator):
        self.driver.find_element(*locator)

    def click(self, locator: Locator):
        element = self.wait(locator)
        element.click()

    def set(self, locator: Locator, text: str):
        element = self.wait(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: Locator):
        element = self.wait(locator)
        return element.text

    def get_title(self):
        return self.driver.title
