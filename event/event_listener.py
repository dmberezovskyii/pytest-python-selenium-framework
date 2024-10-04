import os
import time
from selenium.webdriver.support.abstract_event_listener import (
    AbstractEventListener,
)


def take_screenshot_and_log(rp_logger, driver, screenshot_name) -> None:
    """Takes a screenshot

    :return: None
    """
    screenshot_file = screenshot_name
    if os.path.exists(screenshot_file):
        os.remove(screenshot_file)
    driver.save_screenshot(screenshot_file)
    time.sleep(4)
    with open(screenshot_file, "rb") as image_file:
        file_data = image_file.read()
        rp_logger.info(
            "SCREENSHOT TAKEN ON EXCEPTION",
            attachment={
                "name": screenshot_name,
                "data": file_data,
                "mime": "image/png",
            },
        )


class EventListener(AbstractEventListener):
    """Custom event listener for WebDriver"""

    pass