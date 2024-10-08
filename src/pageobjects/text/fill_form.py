from src.locators.locators import TextFields
from src.pageobjects.base_page import BasePage
from utils.logger import log


class FillForm(BasePage):
    @log()
    def enter_username(self, name: str):
        """Enter username"""
        self.set(TextFields.USER_NAME, name)
